"""EXPLORATION (decision 2, step 1): did GFM's three algorithms disagree on the spring 2024 false alarm?

Not a validation. Whatever rule this suggests is in-sample for these dates and must then pass the
held-out test fixed in docs/research/briefs/2-held-out-test.md (written 18 Nov 2026, before this ran).

  uv run --frozen python -u checks/per_algorithm/explore.py [--reference EMSR758_AOI03_DEL_PRODUCT_v1.zip]

Part 1, per scene, for 30 Apr + 1 May 2024 (false alarm) and 12-25 Sept 2024 (real flood):
  hectares each layer (ensemble, DLR, LIST, TUW) flags in the tilled polder north of Lake Brates
  (lat 45.51-45.62, lon 28.07-28.15) and, with --reference, inside the EMSR758 flood outline.
  Only pixels the pipeline counts as seen (data, not excluded, no advisory flag).
Part 2, catalogue only: in each 20 Apr-5 May window of 2018-2023, how many scenes carry all three
  algorithms (flood_members). A pass with fewer than three counts as unknown in the held-out test.

Results go to run/ next to this file (not to be pushed).
"""
import argparse
import csv
import sys
from datetime import date
from pathlib import Path

import numpy as np
from rasterio.features import rasterize
from rasterio.warp import transform_geom

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
import flood_common  # noqa: E402
import gfm_score  # noqa: E402

flood_common.SCALE = 20  # GFM's own pixel size
LAYERS = {"ensemble": "ensemble_flood_extent", "DLR": "dlr_flood_extent",
          "LIST": "list_flood_extent", "TUW": "tuw_flood_extent"}
WINDOWS = {"false alarm": (date(2024, 4, 30), date(2024, 5, 2)), "Sept flood": (date(2024, 9, 12), date(2024, 9, 26))}
POLDER = {"type": "Polygon", "coordinates": [[[28.07, 45.51], [28.15, 45.51], [28.15, 45.62], [28.07, 45.62], [28.07, 45.51]]]}
OUT = Path(__file__).parent / "run"


def box_mask(geom):
    transform, width, height = flood_common.grid()
    return rasterize([transform_geom("EPSG:4326", flood_common.CRS, geom)], (height, width),
                     transform=transform).astype(bool)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--reference", help="EMSR758 AOI03 PRODUCT zip, for the 'inside the flood outline' column")
    a = p.parse_args()
    OUT.mkdir(exist_ok=True)
    polder = box_mask(POLDER)
    outline = flood_common.ems(a.reference)[0] if a.reference else None
    ha = (flood_common.SCALE ** 2) / 1e4

    with (OUT / "per_algorithm.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["window", "scene", "flood_members", "area"] + list(LAYERS))
        for window, (start, end) in WINDOWS.items():
            print(f"\n== {window} {start}..{end} (ha flagged, seen pixels only)")
            for item in gfm_score.items(start, end):
                layers = {k: gfm_score.read_asset(item, v) for k, v in LAYERS.items()}
                excl = gfm_score.read_asset(item, "exclusion_mask")
                try:
                    adv = gfm_score.read_asset(item, "advisory_flags")
                except Exception:
                    adv = np.ones_like(excl)  # no advisory layer: not seen (decision 1a, option B)
                seen = np.isin(layers["ensemble"], (0, 1)) & (excl != 1) & ~np.isin(adv, (1, 2, 3))
                if not seen.any():
                    continue
                members = "".join(k[0] for k, v in item["properties"].get("flood_members", {}).items() if v)
                for area, m in (("polder", polder), ("EMS outline", outline)):
                    if m is None:
                        continue
                    vals = [float((seen & m & (layers[k] == 1)).sum() * ha) for k in LAYERS]
                    w.writerow([window, item["id"], members, area] + [f"{v:.0f}" for v in vals])
                    print(f"  {item['properties']['datetime'][:16]} [{members}] {area:11s} "
                          + "  ".join(f"{k} {v:7.0f}" for k, v in zip(LAYERS, vals)), flush=True)
                print(f"    values seen: " + ", ".join(
                    f"{k} {np.unique(v[np.isfinite(v)]).tolist()[:4]}" for k, v in layers.items()), flush=True)

    print("\n== Part 2: scenes per spring window carrying all three algorithms (catalogue only)")
    for year in range(2018, 2024):
        feats = gfm_score.items(date(year, 4, 20), date(year, 5, 6))
        full = sum(all(f["properties"].get("flood_members", {}).get(k) for k in ("DLR", "LIST", "TUW")) for f in feats)
        print(f"  {year}: {full} of {len(feats)} scenes have all three", flush=True)


if __name__ == "__main__":
    main()
