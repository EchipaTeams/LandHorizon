"""What every flood script shares: the AOI and its grid, the water masks, EMS references, scoring.

Used by flood_gfm.py, gfm_score.py and flood_local.py (and the AOI by flood_earthengine.py and hand.py).
Thresholds stay in flood_earthengine.py, next to ALGORITHM_VERSION.

set_area() changes the AOI for the whole run (e.g. to score a second EMS event), so read it as
flood_common.AOI. `from flood_common import AOI` would keep the old value.
"""
import json
import math
import os
import sys
import zipfile
from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.features import rasterize
from rasterio.transform import from_origin
from rasterio.warp import reproject, transform_bounds, transform_geom

# Provisional AOI around Galați (lon_min, lat_min, lon_max, lat_max); region locks on 15 Nov.
AOI = [27.5, 45.35, 28.25, 45.85]
CRS, SCALE = "EPSG:32635", 10  # UTM 35N, metres

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"
HAND = OUT / "hand.tif"  # from pipeline/hand.py (GLO-30); stands in for Earth Engine's MERIT HAND
# ponytail: the one 10°x10° JRC tile covering 20–30°E, 40–50°N, which holds the Galați AOI.
JRC = "https://storage.googleapis.com/global-surface-water/downloads2021/occurrence/occurrence_20E_50Nv1_4_2021.tif"


# --- The AOI and its grid ----------------------------------------------------------------------

def set_area(bbox):
    """Work on another area (lon_min, lat_min, lon_max, lat_max), e.g. a second validation event.
    The default is the Galați AOI above. The grid stays UTM 35N, so the area must lie within 24–30°E."""
    global AOI
    AOI = list(bbox)


def aoi_wkt():
    """The AOI as a WKT polygon, for the Copernicus catalogue and SNAP."""
    lon0, lat0, lon1, lat1 = AOI
    return f"POLYGON(({lon0} {lat0},{lon1} {lat0},{lon1} {lat1},{lon0} {lat1},{lon0} {lat0}))"


def grid():
    """The fixed output grid: the AOI in UTM 35N, snapped to 10 m, like flood_earthengine.py's export."""
    x0, y0, x1, y1 = transform_bounds("EPSG:4326", CRS, *AOI)
    x0, y1 = math.floor(x0 / SCALE) * SCALE, math.ceil(y1 / SCALE) * SCALE
    return from_origin(x0, y1, SCALE, SCALE), math.ceil((x1 - x0) / SCALE), math.ceil((y1 - y0) / SCALE)


def to_grid(src, band=1, resampling=Resampling.nearest):
    """One band of an open raster, warped onto the AOI grid as float32 with NaN for no data."""
    transform, width, height = grid()
    dst = np.full((height, width), np.nan, dtype="float32")
    reproject(rasterio.band(src, band), dst, dst_transform=transform, dst_crs=CRS,
              src_nodata=src.nodata, dst_nodata=np.nan, resampling=resampling)
    return dst


# --- Inputs that aren't Sentinel-1 -------------------------------------------------------------

def masks(hand_max_m, permanent_water):
    """(permanent water, can flood) on the AOI grid, from JRC occurrence and our HAND layer."""
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"), rasterio.open(JRC) as src:
        occurrence = np.nan_to_num(to_grid(src), nan=0)  # like EE's unmask(0)
    hand = None
    if hand_max_m is not None:
        if not HAND.exists():
            sys.exit(f"HAND layer missing at {HAND}; run pipeline/hand.py")
        with rasterio.open(HAND) as src:
            hand = np.nan_to_num(to_grid(src, resampling=Resampling.bilinear), nan=0)  # like EE's unmask(0)
    return water_masks(occurrence, hand, permanent_water, hand_max_m)


def water_masks(occurrence, hand, permanent_water, hand_max_m):
    """Permanent water = JRC occurrence (% of time water, 1984-2021) above the threshold.
    It's never flood and isn't counted as land in the false-alarm rate. Can flood = not
    permanent water and, if hand_max_m is set, at most that high above drainage."""
    permanent = occurrence > permanent_water
    can_flood = ~permanent
    if hand_max_m is not None:
        can_flood &= hand <= hand_max_m
    return permanent, can_flood


def ems(path):
    """(flooded, area of interest) of a Copernicus EMS delineation zip, rasterized on the AOI grid."""
    transform, width, height = grid()
    out = []
    with zipfile.ZipFile(path) as zf:
        for suffix in ("observedEventA", "areaOfInterestA"):
            name = next(n for n in zf.namelist() if n.endswith(f"{suffix}_v1.json"))
            geoms = [transform_geom("EPSG:4326", CRS, f["geometry"]) for f in json.loads(zf.read(name))["features"]]
            out.append(rasterize(geoms, out_shape=(height, width), transform=transform).astype(bool))
    return tuple(out)


# --- Scoring and output ------------------------------------------------------------------------

def scores(n_flooded, n_passes, permanent, ref=None, ref_aoi=None):
    """Share of land flagged at >=1/2/3 passes; with a reference, precision and recall inside ref_aoi."""
    land = (n_passes > 0) & ~permanent
    out = {"share": {k: float((n_flooded[land] >= k).mean()) if land.any() else float("nan") for k in (1, 2, 3)}}
    if ref is not None:
        valid = ref_aoi & (n_passes > 0)
        truth = ref & valid
        out["ref_px"] = int(truth.sum())
        for k in (1, 2, 3):
            pred = (n_flooded >= k) & valid
            tp = int((pred & truth).sum())
            out[k] = {"pred_px": int(pred.sum()), "precision": tp / pred.sum() if pred.any() else float("nan"),
                      "recall": tp / truth.sum() if truth.any() else float("nan")}
    return out


def report(n_flooded, n_passes, permanent, reference=None):
    """Print the dry-date share and, with an EMS zip, precision and recall (like flood_earthengine.py --evaluate)."""
    ref, ref_aoi = ems(reference) if reference else (None, None)
    s = scores(n_flooded, n_passes, permanent, ref, ref_aoi)
    print("land flagged flooded:  " + "  ".join(f">={k} pass: {s['share'][k]:6.2%}" for k in (1, 2, 3)))
    if ref is not None:
        print(f"reference {os.path.basename(reference)}: {s['ref_px'] / 100:.0f} ha flooded")
        for k in (1, 2, 3):
            print(f"  flooded in >= {k} pass(es): predicted {s[k]['pred_px'] / 100:8.0f} ha  "
                  f"precision {s[k]['precision']:6.1%}  recall {s[k]['recall']:6.1%}")


def write_counts(out, n_flooded, n_passes):
    """The n_flooded / n_passes COG on the AOI grid, the same format as flood_earthengine.py's export."""
    transform, width, height = grid()
    out.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(out, "w", driver="COG", dtype="uint16", count=2, crs=CRS, transform=transform,
                       width=width, height=height, compress="deflate") as dst:
        dst.write(np.stack([n_flooded, n_passes]))
        dst.descriptions = ("n_flooded", "n_passes")
    print(f"wrote {out}")
