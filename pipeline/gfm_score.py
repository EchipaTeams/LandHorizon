"""Score Copernicus Global Flood Monitoring (GFM) the same way as our own flood method (prototype).

GFM maps floods on every Sentinel-1 scene worldwide since 2015, with an ensemble of three
algorithms, plus an exclusion mask (where Sentinel-1 can't see floods) and a reference water
mask (permanent and seasonal water). This script reads its per-scene layers for the AOI from
the EODC STAC catalogue (no account), turns them into our n_flooded / n_passes counts, and
prints the same scores as `flood_local.py --evaluate`, so GFM and v0.2 can be compared.

  uv run python pipeline/gfm_score.py 2023-09-12 2023-09-25                  # dry-date test
  uv run python pipeline/gfm_score.py 2024-09-12 2024-09-25 \\
      --reference data/raw/reference/EMSR758_AOI03_DEL_PRODUCT_v1.zip       # vs Copernicus EMS
  add --write to also save data/processed/flood_<start>_<end>_gfm.tif for QGIS
  add --area-from-reference to score another region (e.g. a second EMS event) on its EMS area of interest
  add --save-passes to also keep one map per pass in data/processed/gfm_passes/<start>_<end>/ (1 flood, 0 dry, no data = not seen)

Excluded pixels, and pixels under a GFM advisory flag (unreliable that pass), don't count as a pass,
so where GFM can't see, n_passes stays 0 ("unknown").
Contains modified Copernicus Emergency Management Service information.
"""
import argparse
import http.client
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from collections import defaultdict
from datetime import date

import numpy as np
import rasterio
from rasterio._err import CPLE_BaseError

import flood_local
from flood_local import OUT, masks, report, to_grid, write_counts

STAC = "https://stac.eodc.eu/api/v1/collections/GFM/items"


def items(start, end):
    """GFM items (one per Sentinel-1 scene per Equi7 tile) touching the AOI in [start, end)."""
    url = STAC + "?" + urllib.parse.urlencode({
        "bbox": ",".join(map(str, flood_local.AOI)), "limit": 100,
        "datetime": f"{start.isoformat()}T00:00:00Z/{end.isoformat()}T00:00:00Z"})
    out = []
    while url:
        page = get_json(url)
        out += [f for f in page["features"] if f["properties"]["datetime"] < f"{end.isoformat()}T00:00:00Z"]
        url = next((link["href"] for link in page.get("links", []) if link.get("rel") == "next"), None)
    return out


def get_json(url, attempts=5):
    """A catalogue request, retried: the EODC catalogue is sometimes slow or briefly unreachable."""
    for attempt in range(1, attempts + 1):
        try:
            return json.load(urllib.request.urlopen(url, timeout=120))
        except (OSError, http.client.HTTPException) as e:  # timeouts, resets, DNS hiccups
            if attempt == attempts:
                raise
            print(f"  catalogue request failed ({str(e)[:60]}), retry {attempt}/{attempts - 1}", flush=True)
            time.sleep(15 * attempt)


def ems_bbox(path):
    """Bounding box (lon/lat) of an EMS zip's area of interest."""
    with zipfile.ZipFile(path) as zf:
        name = next(n for n in zf.namelist() if n.endswith("areaOfInterestA_v1.json"))
        coords = np.array([xy for f in json.loads(zf.read(name))["features"]
                           for ring in _rings(f["geometry"]) for xy in ring])
    (lon0, lat0), (lon1, lat1) = coords.min(axis=0), coords.max(axis=0)
    return [round(float(v), 5) for v in (lon0, lat0, lon1, lat1)]


def _rings(geom):
    return geom["coordinates"] if geom["type"] == "Polygon" else [r for poly in geom["coordinates"] for r in poly]


def read(href, attempts=10):
    """One GFM layer warped onto our AOI grid (nearest neighbour; 20 m -> 10 m).

    A connection can die mid-download (e.g. a wifi switch) and GDAL would wait on it forever.
    LOW_SPEED aborts a download that gets under 1 kB/s for 30 s; then we retry with a fresh connection.
    """
    env = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_TIMEOUT=120,
               GDAL_HTTP_LOW_SPEED_TIME=30, GDAL_HTTP_LOW_SPEED_LIMIT=1000,
               GDAL_HTTP_MAX_RETRY=3, GDAL_HTTP_RETRY_DELAY=5, GDAL_HTTP_TCP_KEEPALIVE="YES",
               VSI_CACHE="FALSE")
    for attempt in range(1, attempts + 1):
        try:
            with rasterio.Env(**env), rasterio.open(href) as src:
                return to_grid(src)
        except (rasterio.errors.RasterioError, CPLE_BaseError, OSError) as e:  # GDAL's HTTP errors are CPLE_*
            if attempt == attempts or "404" in str(e):  # a missing file won't come back: see read_asset
                raise
            print(f"  read failed ({str(e)[:80]}), retry {attempt}/{attempts - 1}", flush=True)
            time.sleep(min(15 * attempt, 60))  # ~8 min of patience in total for a slow patch


def read_asset(item, key):
    """Read one of an item's GFM layers. EODC moves older files to an archive folder from time to
    time (seen 10 Nov 2026: GFM_LAYERS -> GFM_ARCHIVE), so on a 404 ask the catalogue for the
    item's current link and read that instead."""
    href = item["assets"][key]["href"]
    try:
        return read(href)
    except (rasterio.errors.RasterioError, CPLE_BaseError, OSError) as e:
        if "404" not in str(e):
            raise
        fresh = get_json(f"{STAC}/{item['id']}")
        if fresh["assets"][key]["href"] == href:
            raise
        item["assets"] = fresh["assets"]
        print(f"  {item['id']}: file moved, now at {fresh['assets'][key]['href'].split('/collections/')[1][:40]}...",
              flush=True)
        return read(fresh["assets"][key]["href"])


def passes(feats, verbose=False, skip=()):
    """Per Sentinel-1 pass, in time order: (pass key 'YYYY-MM-DDTHH', seen, flooded) on the AOI grid.

    Frames of one pass (same date and hour) are merged. seen = GFM had data and didn't exclude the
    pixel; flooded = seen and GFM's ensemble says flood. Excluded or no data is not seen ("unknown").
    Passes whose key is in `skip` (already done, e.g. from a checkpoint) aren't read again.
    """
    groups = defaultdict(list)
    for f in feats:
        groups[f["properties"]["datetime"][:13]].append(f)
    for key, frames in sorted(groups.items()):
        if key in skip:
            continue
        flood = excluded = advisory = None
        for f in frames:
            a = read_asset(f, "ensemble_flood_extent")
            e = read_asset(f, "exclusion_mask")
            try:
                v = read_asset(f, "advisory_flags")
            except (rasterio.errors.RasterioError, CPLE_BaseError, OSError, KeyError) as err:
                if not isinstance(err, KeyError) and "404" not in str(err):
                    raise
                v = np.zeros_like(a)  # older archive passes (e.g. 2018) have no advisory layer: no warnings
                if verbose:
                    print(f"  {f['id']}: no advisory flags for this pass", flush=True)
            if verbose:  # the documented encoding is 0/1 + no data; show what the files really hold
                print(f"  {f['id']}: flood values {np.unique(a[np.isfinite(a)]).tolist()[:6]}, "
                      f"exclusion values {np.unique(e[np.isfinite(e)]).tolist()[:6]}", flush=True)
            flood = a if flood is None else np.where(np.isin(flood, (0, 1)), flood, a)
            excluded = e if excluded is None else np.where(np.isfinite(excluded), excluded, e)
            advisory = v if advisory is None else np.where(np.isfinite(advisory), advisory, v)
        # Advisory flags (1 low regional backscatter: dry soil, frost, snow; 2 wind-roughened water; 3 both)
        # mark where GFM itself says its result is unreliable. Treat them as not seen for this pass:
        # on 30 Apr 2024 they covered 40 % of a false "flood" on tilled fields, but 0.7 % of the real Sept flood.
        seen = np.isin(flood, (0, 1)) & (excluded != 1) & ~np.isin(advisory, (1, 2, 3))
        flooded = seen & (flood == 1)
        print(f"pass {key}h: {len(frames)} frame(s), sees {seen.mean():.0%} of the AOI, "
              f"flood in {flooded.sum() / max(seen.sum(), 1):.2%} of it", flush=True)
        yield key, seen, flooded


def counts(feats, verbose=True, save_dir=None):
    """n_flooded, n_passes from GFM items; with save_dir, also one GeoTIFF per pass that saw the AOI."""
    n_flooded = n_passes = None
    for key, seen, flooded in passes(feats, verbose):
        if n_passes is None:
            n_flooded, n_passes = np.zeros(seen.shape, "uint16"), np.zeros(seen.shape, "uint16")
        n_passes += seen
        n_flooded += flooded
        if save_dir and seen.any():
            save_pass(save_dir / f"gfm_{key}.tif", seen, flooded)
    return n_flooded, n_passes


def save_pass(path, seen, flooded):
    """One pass as uint8: 1 flood, 0 seen and dry, 255 (no data) not seen."""
    transform, width, height = flood_local.grid()
    path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(path, "w", driver="GTiff", dtype="uint8", count=1, crs=flood_local.CRS, transform=transform,
                       width=width, height=height, nodata=255, compress="deflate", tiled=True) as dst:
        dst.write(np.where(seen, flooded, 255).astype("uint8"), 1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("start", type=date.fromisoformat)
    p.add_argument("end", type=date.fromisoformat)
    p.add_argument("--reference", help="Copernicus EMS delineation zip to score against")
    p.add_argument("--write", action="store_true", help="also write the counts as a COG for QGIS")
    p.add_argument("--save-passes", action="store_true", help="also keep one map per pass (for QGIS)")
    p.add_argument("--area-from-reference", action="store_true",
                   help="use the reference's EMS area of interest (bounding box) instead of flood.py's AOI")
    a = p.parse_args()
    if a.reference and not os.path.exists(a.reference):
        sys.exit(f"No such reference file: {a.reference}")
    if a.area_from_reference:
        if not a.reference:
            sys.exit("--area-from-reference needs --reference")
        flood_local.set_area(ems_bbox(a.reference))
        print(f"area: {flood_local.AOI} (from {os.path.basename(a.reference)})")

    feats = items(a.start, a.end)
    if not feats:
        sys.exit(f"No GFM items over the AOI in {a.start}..{a.end}.")
    print(f"GFM {a.start}..{a.end}: {len(feats)} items", flush=True)
    save_dir = OUT / "gfm_passes" / f"{a.start}_{a.end}" if a.save_passes else None
    n_flooded, n_passes = counts(feats, save_dir=save_dir)

    # Land is defined as in the pre-registered criteria (not JRC permanent water above 80 %), so the
    # numbers compare directly with v0.2. GFM already sets its own reference water to "no flood".
    permanent, _ = masks(hand_max_m=None)
    report(n_flooded, n_passes, permanent, a.reference)
    print(f"no pass could see {np.mean(n_passes == 0):.1%} of the AOI (excluded or no data: unknown)")
    if a.write:
        write_counts(OUT / f"flood_{a.start}_{a.end}_gfm.tif", n_flooded, n_passes)
    if save_dir:
        print(f"saved {len(list(save_dir.glob('gfm_*.tif')))} per-pass maps in {save_dir}")


if __name__ == "__main__":
    main()
