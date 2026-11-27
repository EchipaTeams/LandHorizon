"""Flood history for the AOI from Copernicus Global Flood Monitoring (GFM): the file the API reads.

GFM maps floods on every Sentinel-1 pass (ensemble of three algorithms, archive from 2015) and
marks where Sentinel-1 can't see floods (exclusion mask: high ground, cities, forest, radar
shadow) and where its result is unreliable that pass (advisory flags: dry or tilled soil, frost,
snow, wind on water). Both count as "not seen". Validated against Copernicus EMS on two events:
docs/flood-validation.md.

  uv run python pipeline/flood_gfm.py 2015-01-01 2025-05-01   # stops on 2025-04-14 (v3 -> v4), ~1¼ h

Writes data/processed/flood_gfm.tif on the AOI grid (UTM 35N, 10 m):
  band 1  n_flooded   passes that saw flood water on the pixel
  band 2  n_passes    passes that could see the pixel (0 = never seen: "unknown", never "dry")
  band 3+ one band per pass that saw any flood in the AOI: 1 = flood on that pixel, else 0.
          The band description is the pass time (e.g. 2024-09-14T04), which gives the API its flood dates.
The period goes into the file's tags, so the API can say what it covers. The history stops at a change of
GFM's major version (decision 1b: such layers can't be used together), and period_end then says so. The tag
gfm_versions records, per pass, the GFM version and the algorithms that contributed to all the scenes that
counted (a scene without an advisory layer doesn't count, decision 1a; a pass with none that counted isn't listed).
Contains modified Copernicus Emergency Management Service information.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date

import numpy as np
import rasterio
from rasterio.shutil import copy as rio_copy

from flood_common import CRS, OUT, grid
from gfm_score import items, passes

PATH = OUT / "flood_gfm.tif"
WORKERS = 8  # passes read at once: June 2019 took 36 s instead of 189 s, identical file, 7.6 GB peak memory


def major(feat):
    """GFM major version of a scene; the catalogue writes it as 'GFM v3.1.0' or 'v4.0.0'."""
    version = feat["properties"].get("processing:version")
    match = re.search(r"v(\d+)\.", version or "")
    if not match:
        raise ValueError(f"{feat['id']}: no readable GFM version ({version!r})")
    return int(match[1])


def before_version_change(feats):
    """(scenes before the first day GFM's major version changes, that day), or (all scenes, None)."""
    feats = sorted(feats, key=lambda f: f["properties"]["datetime"])
    first, *rest = [major(f) for f in feats]
    change = next((f["properties"]["datetime"][:10] for f, m in zip(feats[1:], rest) if m != first), None)
    return [f for f in feats if change is None or f["properties"]["datetime"] < change], change


def versions(feats):
    """Per pass key: [GFM version(s), algorithms that contributed to all its scenes], from the catalogue.
    Give it only the scenes that counted (gfm_score.passes' `used`)."""
    found, members = defaultdict(set), {}
    for f in feats:
        p = f["properties"]
        key = p["datetime"][:13]
        found[key].add(p["processing:version"])
        on = {m for m, used in p.get("flood_members", {}).items() if used}
        members[key] = members.get(key, on) & on
    return {k: [", ".join(sorted(v)), " ".join(sorted(members[k]))] for k, v in sorted(found.items())}


def load_checkpoint(path, shape):
    """(n_flooded, n_passes, flood_bands, done pass keys, used scene ids), from a checkpoint or fresh.
    used is None for a checkpoint written before it was recorded."""
    if not path.exists():
        return np.zeros(shape, "uint16"), np.zeros(shape, "uint16"), [], set(), set()
    c = np.load(path)
    idx = np.split(c["flood_idx"], c["flood_split"])
    used = set(c["used"].tolist()) if "used" in c.files else None
    return (c["n_flooded"], c["n_passes"], list(zip(c["flood_keys"].tolist(), idx)), set(c["done"].tolist()), used)


def save_checkpoint(path, n_flooded, n_passes, flood_bands, done, used):
    """Progress so far, so a crash or network failure resumes here instead of from the start."""
    sizes = [len(i) for _, i in flood_bands]
    tmp = path.with_suffix(".tmp.npz")
    np.savez(tmp, n_flooded=n_flooded, n_passes=n_passes, done=np.array(sorted(done)), used=np.array(sorted(used)),
             flood_keys=np.array([k for k, _ in flood_bands]),
             flood_idx=np.concatenate([i for _, i in flood_bands]) if flood_bands else np.array([], "int64"),
             flood_split=np.cumsum(sizes)[:-1] if sizes else np.array([], "int64"))
    tmp.replace(path)  # only a complete checkpoint gets the real name; replace (not rename) also works on Windows


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("start", type=date.fromisoformat)
    p.add_argument("end", type=date.fromisoformat)
    a = p.parse_args()

    feats = items(a.start, a.end)
    if not feats:
        sys.exit(f"No GFM items over the AOI in {a.start}..{a.end}.")
    feats, change = before_version_change(feats)
    end = change or a.end.isoformat()
    if change:
        print(f"GFM's major version changes on {change}: the history stops before that day", flush=True)
    if not feats:
        sys.exit(f"No GFM items left before {change}.")
    print(f"GFM {a.start}..{end}: {len(feats)} items", flush=True)

    transform, width, height = grid()
    OUT.mkdir(parents=True, exist_ok=True)  # before the loop: the first checkpoint is saved at pass 10
    # "1a" keeps a checkpoint from before that decision (missing advisory layer = no warnings) from being resumed
    checkpoint = OUT / f"flood_gfm_1a_{a.start}_{end}.checkpoint.npz"
    n_flooded, n_passes, flood_bands, done, used = load_checkpoint(checkpoint, (height, width))
    if done:
        print(f"resuming from {checkpoint.name}: {len(done)} passes already done", flush=True)
    if used is None:  # its passes' dropped scenes weren't recorded: count them all, as before
        print("  this checkpoint doesn't record dropped scenes: gfm_versions lists all scenes of its passes",
              flush=True)
        used = {f["id"] for f in feats if f["properties"]["datetime"][:13] in done}
    for key, seen, flooded, frames in passes(feats, skip=done, workers=WORKERS):
        n_passes += seen
        n_flooded += flooded
        if flooded.any():
            flood_bands.append((key, np.flatnonzero(flooded)))
        done.add(key)
        used |= {f["id"] for f in frames}
        if len(done) % 10 == 0:
            save_checkpoint(checkpoint, n_flooded, n_passes, flood_bands, done, used)

    tmp = PATH.with_suffix(".part.tif")
    with rasterio.open(tmp, "w", driver="GTiff", dtype="uint16", count=2 + len(flood_bands), crs=CRS,
                       transform=transform, width=width, height=height, compress="deflate", tiled=True,
                       interleave="band", BIGTIFF="IF_SAFER") as dst:  # pixel (the default) rewrites every band per band
        dst.write(n_flooded, 1)
        dst.write(n_passes, 2)
        for i, (_, idx) in enumerate(flood_bands, start=3):
            band = np.zeros((height, width), "uint16")
            band.flat[idx] = 1
            dst.write(band, i)
        dst.descriptions = ("n_flooded", "n_passes", *(key for key, _ in flood_bands))
        dst.update_tags(source="Copernicus GFM ensemble flood extent + exclusion mask",
                        period_start=a.start.isoformat(), period_end=end,
                        gfm_versions=json.dumps(versions([f for f in feats if f["id"] in used]), separators=(",", ":")))
    # No overviews (26 Nov 2026, F3): at ~1,200 bands GDAL's overview step ran over 49 min without finishing
    # (5.7 min without it), and the API reads full resolution only. Revert by deleting OVERVIEWS="NONE";
    # TiTiler would need overviews, built with nearest resampling (0/1 bands). See architecture.md, "Why these choices".
    rio_copy(tmp, PATH, driver="COG", compress="deflate", interleave="band", BIGTIFF="IF_SAFER", OVERVIEWS="NONE")
    tmp.unlink()
    checkpoint.unlink(missing_ok=True)
    seen = n_passes > 0
    print(f"wrote {PATH}: {len(flood_bands)} passes with flood; AOI seen by >=1 pass: {seen.mean():.0%}; "
          f"ever flooded: {(n_flooded[seen] > 0).mean():.2%} of the seen area")


if __name__ == "__main__":
    main()
