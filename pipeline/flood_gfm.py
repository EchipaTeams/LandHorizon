"""Flood history for the AOI from Copernicus Global Flood Monitoring (GFM): the file the API reads.

GFM maps floods on every Sentinel-1 pass (ensemble of three algorithms, archive from 2015) and
marks where Sentinel-1 can't see floods (exclusion mask: high ground, cities, forest, radar
shadow) and where its result is unreliable that pass (advisory flags: dry or tilled soil, frost,
snow, wind on water). Both count as "not seen". Validated against Copernicus EMS on two events:
docs/flood-validation.md.

  uv run python pipeline/flood_gfm.py 2024-01-01 2025-01-01

Writes data/processed/flood_gfm.tif on the AOI grid (UTM 35N, 10 m):
  band 1  n_flooded   passes that saw flood water on the pixel
  band 2  n_passes    passes that could see the pixel (0 = never seen: "unknown", never "dry")
  band 3+ one band per pass that saw any flood in the AOI: 1 = flood on that pixel, else 0.
          The band description is the pass time (e.g. 2024-09-14T04), which gives the API its flood dates.
The period goes into the file's tags, so the API can say what it covers.
Contains modified Copernicus Emergency Management Service information.
"""
import argparse
import sys
from datetime import date

import numpy as np
import rasterio
from rasterio.shutil import copy as rio_copy

from flood_local import CRS, OUT, grid
from gfm_score import items, passes

PATH = OUT / "flood_gfm.tif"


def load_checkpoint(path, shape):
    """(n_flooded, n_passes, flood_bands, done pass keys), from a checkpoint or fresh."""
    if not path.exists():
        return np.zeros(shape, "uint16"), np.zeros(shape, "uint16"), [], set()
    c = np.load(path)
    idx = np.split(c["flood_idx"], c["flood_split"])
    return (c["n_flooded"], c["n_passes"], list(zip(c["flood_keys"].tolist(), idx)), set(c["done"].tolist()))


def save_checkpoint(path, n_flooded, n_passes, flood_bands, done):
    """Progress so far, so a crash or network failure resumes here instead of from the start."""
    sizes = [len(i) for _, i in flood_bands]
    tmp = path.with_suffix(".tmp.npz")
    np.savez(tmp, n_flooded=n_flooded, n_passes=n_passes, done=np.array(sorted(done)),
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
    print(f"GFM {a.start}..{a.end}: {len(feats)} items", flush=True)

    transform, width, height = grid()
    checkpoint = OUT / f"flood_gfm_{a.start}_{a.end}.checkpoint.npz"
    n_flooded, n_passes, flood_bands, done = load_checkpoint(checkpoint, (height, width))
    if done:
        print(f"resuming from {checkpoint.name}: {len(done)} passes already done", flush=True)
    for key, seen, flooded in passes(feats, skip=done):
        n_passes += seen
        n_flooded += flooded
        if flooded.any():
            flood_bands.append((key, np.flatnonzero(flooded)))
        done.add(key)
        if len(done) % 10 == 0:
            save_checkpoint(checkpoint, n_flooded, n_passes, flood_bands, done)

    tmp = PATH.with_suffix(".part.tif")
    OUT.mkdir(parents=True, exist_ok=True)
    with rasterio.open(tmp, "w", driver="GTiff", dtype="uint16", count=2 + len(flood_bands), crs=CRS,
                       transform=transform, width=width, height=height, compress="deflate", tiled=True,
                       BIGTIFF="IF_SAFER") as dst:
        dst.write(n_flooded, 1)
        dst.write(n_passes, 2)
        for i, (_, idx) in enumerate(flood_bands, start=3):
            band = np.zeros((height, width), "uint16")
            band.flat[idx] = 1
            dst.write(band, i)
        dst.descriptions = ("n_flooded", "n_passes", *(key for key, _ in flood_bands))
        dst.update_tags(source="Copernicus GFM ensemble flood extent + exclusion mask",
                        period_start=a.start.isoformat(), period_end=a.end.isoformat())
    rio_copy(tmp, PATH, driver="COG", compress="deflate", BIGTIFF="IF_SAFER")
    tmp.unlink()
    checkpoint.unlink(missing_ok=True)
    seen = n_passes > 0
    print(f"wrote {PATH}: {len(flood_bands)} passes with flood; AOI seen by >=1 pass: {seen.mean():.0%}; "
          f"ever flooded: {(n_flooded[seen] > 0).mean():.2%} of the seen area")


if __name__ == "__main__":
    main()
