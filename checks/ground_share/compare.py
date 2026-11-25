"""CHECK (L3): which denominator should the ground share rule use?

Both rules call ground `measured` only when (cells with data) / denominator >= GROUND_MIN_SHARE (0.5),
and `unknown` when no cell with data has its centre inside the plot. They differ in the denominator:
  fit   (PR #11, in api/main.py today): the EGMS cells whose centre is inside the plot
  area  (DECISIONS.md #5, 23 Nov):      max(1, round(area_ha)); a 100 m cell is 1 ha

Where they can disagree:
  - a plot that catches fewer cell centres than its area (a thin strip, an odd shape, placement on the
    grid): `area` expects more cells than can fit, so it is stricter;
  - a plot that catches more centres than its area: `area` is laxer, and its share can exceed 1;
  - Python's round() rounds halves to even: 2.5 ha -> 2, 3.5 ha -> 4.

Part 1 runs the 20 test plots. Part 2 drops rectangles of several sizes, shapes and rotations on cells
that have data in ground.tif, counts where the two rules disagree, and writes up to 50 of those plots
as WGS84 GeoJSON into run/ next to this file (not to be pushed), to draw them on the map.

  uv run python checks/ground_share/compare.py
  uv run python checks/ground_share/compare.py --per-shape 500 --seed 1
"""
import argparse
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.features import bounds, geometry_mask
from rasterio.transform import array_bounds
from rasterio.warp import transform_geom

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
from ground import CRS, OUT, ring_area  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PLOTS = ROOT / "data" / "sample" / "plots.geojson"
RUN = Path(__file__).resolve().parent / "run"
MIN_SHARE = 0.5  # GROUND_MIN_SHARE in api/main.py
SIZES_HA = (0.5, 1, 1.5, 2, 3, 5, 8, 12)
ASPECTS = (1, 4, 10)  # length / width
ROTATIONS = (0, 30)  # degrees


def judge(geom_3035, band, transform):
    """(area_ha, cells that fit, cells with data, status under `fit`, status under `area`) for one plot."""
    rings = geom_3035["coordinates"]
    area_ha = (ring_area(rings[0]) - sum(ring_area(h) for h in rings[1:])) / 10_000
    inside = geometry_mask([geom_3035], out_shape=band.shape, transform=transform, all_touched=False, invert=True)
    fit = int(inside.sum())
    with_data = int(np.isfinite(band[inside]).sum())

    def status(denominator):
        return "measured" if with_data and with_data / denominator >= MIN_SHARE else "unknown"
    return area_ha, fit, with_data, status(max(fit, 1)), status(max(1, round(area_ha)))


def rectangle(cx, cy, area_ha, aspect, degrees):
    """A rotated rectangle of that area and length/width ratio around (cx, cy), in metres."""
    width = math.sqrt(area_ha * 10_000 / aspect)
    length = width * aspect
    a = math.radians(degrees)
    corners = [(-length / 2, -width / 2), (length / 2, -width / 2), (length / 2, width / 2), (-length / 2, width / 2)]
    ring = [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in corners]
    return {"type": "Polygon", "coordinates": [ring + ring[:1]]}


def test_plots(band, transform):
    features = json.loads(PLOTS.read_text())["features"]
    print(f"Part 1: the {len(features)} test plots")
    print(f"{'name':<24} {'area_ha':>7} {'fit':>4} {'data':>4}  {'fit rule':<9} {'area rule':<9}")
    for f in features:
        area, fit, data, by_fit, by_area = judge(transform_geom("EPSG:4326", CRS, f["geometry"]), band, transform)
        flag = "   <- differ" if by_fit != by_area else ""
        print(f"{f['properties']['name']:<24} {area:7.2f} {fit:4d} {data:4d}  {by_fit:<9} {by_area:<9}{flag}")


def sweep(band, transform, per_shape, rng):
    """Rectangles placed so that at least the cell under their centre has data; both rules then have a case."""
    rows, cols = np.nonzero(np.isfinite(band))
    edges = rasterio.coords.BoundingBox(*array_bounds(*band.shape, transform))
    if rows.size == 0:
        sys.exit("ground.tif has no cell with data")
    print(f"\nPart 2: {per_shape} rectangles per size, shape and rotation, each centred within a cell that has data")
    print(f"{'size_ha':>7} {'aspect':>6} {'rot':>4}  {'both meas.':>10} {'both unk.':>9} "
          f"{'fit only':>8} {'area only':>9}  {'fit cells (min-max)':>19}")
    examples = []
    for size in SIZES_HA:
        for aspect in ASPECTS:
            for degrees in ROTATIONS:
                tally = {(m1, m2): 0 for m1 in (True, False) for m2 in (True, False)}
                fits = []
                for _ in range(per_shape):
                    while True:  # the API refuses a plot not wholly inside the raster (422), so skip those
                        i = rng.randrange(rows.size)
                        x, y = transform * (cols[i] + rng.random(), rows[i] + rng.random())
                        geom = rectangle(x, y, size, aspect, degrees)
                        left, bottom, right, top = bounds(geom)
                        if left >= edges.left and bottom >= edges.bottom and right <= edges.right and top <= edges.top:
                            break
                    _, fit, data, by_fit, by_area = judge(geom, band, transform)
                    tally[(by_fit == "measured", by_area == "measured")] += 1
                    fits.append(fit)
                    if by_fit != by_area and len(examples) < 50:
                        examples.append({"type": "Feature", "geometry": transform_geom(CRS, "EPSG:4326", geom),
                                         "properties": {"size_ha": size, "aspect": aspect, "rotation": degrees,
                                                        "fit": fit, "with_data": data,
                                                        "fit_rule": by_fit, "area_rule": by_area}})
                print(f"{size:7.1f} {aspect:6d} {degrees:4d}  {tally[(True, True)]:10d} {tally[(False, False)]:9d} "
                      f"{tally[(True, False)]:8d} {tally[(False, True)]:9d}  {min(fits):>9d}-{max(fits):<9d}")
    return examples


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ground", type=Path, default=OUT, help=f"the ground COG (default {OUT})")
    p.add_argument("--per-shape", type=int, default=200, help="rectangles per size, shape and rotation")
    p.add_argument("--seed", type=int, default=0)
    a = p.parse_args()
    if not a.ground.exists():
        sys.exit(f"{a.ground} not found: copy ground.tif from the team Drive or run pipeline/ground.py")
    with rasterio.open(a.ground) as src:
        band, transform = src.read(1), src.transform
        if src.crs != CRS:
            sys.exit(f"{a.ground} is in {src.crs}, expected {CRS} (the EGMS grid)")

    test_plots(band, transform)
    examples = sweep(band, transform, a.per_shape, random.Random(a.seed))
    RUN.mkdir(exist_ok=True)
    out = RUN / "disagreements.geojson"
    out.write_text(json.dumps({"type": "FeatureCollection", "features": examples}))
    print(f"\nfit only = measured under PR #11's rule, unknown under decision #5's; area only = the reverse.")
    print(f"wrote {len(examples)} disagreeing plots to {out}")


if __name__ == "__main__":
    main()
