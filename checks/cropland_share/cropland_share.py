"""CHECK (decision 3): how much of GFM's spring false alarm, and of the real Sept 2024 flood, is cropland?

Rule fixed 18 Nov 2026 in docs/research/briefs/3-cropland-caveat.md, before this ran:
build option A (cropland caveat field) by 29 Nov only if (a) - (b) >= 20 percentage points.
  (a) share of pixels GFM flags at >= 1 pass in 20 Apr-5 May 2024, on the spring test's land
      (seen at least once, not JRC permanent water), that ESA WorldCover 2021 labels cropland (class 40)
  (b) share of pixels GFM flags at >= 1 pass in 12-25 Sept 2024 inside the EMSR758 AOI03 observed
      flood outline (correct detections) that WorldCover 2021 labels cropland
Pixels where WorldCover has no data are left out of both shares (counted and printed).
WorldCover is partly derived from Sentinel-1: it describes land cover here, it never validates GFM.

  uv run --frozen python -u checks/cropland_share/cropland_share.py

GFM counts are cached in run/ next to this file, with the printed results. run/ is not to be pushed.
"""
import sys
from datetime import date
from pathlib import Path

import numpy as np
import rasterio

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
import flood_common  # noqa: E402
import gfm_score  # noqa: E402
from flood_earthengine import PERMANENT_WATER  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "data" / "raw" / "reference" / "EMSR758_AOI03_DEL_PRODUCT_v1.zip"
# One 3°x3° tile (45-48 N, 27-30 E) holds the whole Galați AOI. CC BY 4.0, © ESA WorldCover project 2021.
WORLDCOVER = ("https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/"
              "ESA_WorldCover_10m_2021_v200_N45E027_Map.tif")
CLASSES = {10: "tree cover", 20: "shrubland", 30: "grassland", 40: "cropland", 50: "built-up",
           60: "bare/sparse", 70: "snow/ice", 80: "permanent water", 90: "herbaceous wetland",
           95: "mangroves", 100: "moss/lichen"}
WINDOWS = {"spring": (date(2024, 4, 20), date(2024, 5, 6)),   # end exclusive: 20 Apr-5 May
           "sept": (date(2024, 9, 12), date(2024, 9, 26))}    # end exclusive: 12-25 Sept
RULE_PP = 20
OUT = Path(__file__).parent / "run"


def gfm_counts(name):
    """n_flooded, n_passes for one window, read once from EODC and then from the run/ cache."""
    cache = OUT / f"gfm_{name}.npz"
    if cache.exists():
        z = np.load(cache)
        return z["n_flooded"], z["n_passes"]
    start, end = WINDOWS[name]
    feats = gfm_score.items(start, end)
    print(f"GFM {name} {start}..{end}: {len(feats)} items", flush=True)
    n_flooded, n_passes = gfm_score.counts(feats, verbose=False)
    np.savez_compressed(cache, n_flooded=n_flooded, n_passes=n_passes)
    return n_flooded, n_passes


def share(name, flagged, cover):
    """Print the WorldCover make-up of the flagged pixels; return the cropland share (no-data left out)."""
    labelled = flagged & (cover > 0)
    n, n_nodata = int(labelled.sum()), int((flagged & ~(cover > 0)).sum())
    print(f"\n{name}: {flagged.sum() / 100:.0f} ha flagged, {n_nodata / 100:.0f} ha without WorldCover data")
    values, px = np.unique(cover[labelled], return_counts=True)
    for v, c in sorted(zip(values, px), key=lambda t: -t[1]):
        print(f"  {CLASSES.get(int(v), int(v)):<20} {c / 100:9.0f} ha  {c / n:6.1%}")
    return float((cover[labelled] == 40).mean()) if n else float("nan")


def main():
    OUT.mkdir(exist_ok=True)
    if not REFERENCE.exists():
        sys.exit(f"Reference missing at {REFERENCE}")
    spring_flooded, spring_passes = gfm_counts("spring")
    sept_flooded, sept_passes = gfm_counts("sept")
    permanent, _ = flood_common.masks(hand_max_m=None, permanent_water=PERMANENT_WATER)
    observed, _ = flood_common.ems(REFERENCE)
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"), rasterio.open(WORLDCOVER) as src:
        cover = np.nan_to_num(flood_common.to_grid(src), nan=0).astype("uint8")  # 0 = no data

    land = (spring_passes > 0) & ~permanent
    a = share("(a) spring 20 Apr-5 May 2024, flagged >= 1 pass on land", land & (spring_flooded >= 1), cover)
    b = share("(b) Sept 12-25 2024, flagged >= 1 pass inside EMSR758 outline",
              observed & (sept_passes > 0) & ~permanent & (sept_flooded >= 1), cover)
    gap = (a - b) * 100
    print(f"\n(a) {a:.1%}   (b) {b:.1%}   (a) - (b) = {gap:.1f} pp   rule: >= {RULE_PP} pp")
    print("RESULT: build option A" if gap >= RULE_PP else "RESULT: stay with C', log the negative result")


if __name__ == "__main__":
    main()
