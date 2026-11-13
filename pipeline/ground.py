"""Ground motion: EGMS Ortho vertical (U) velocity for the AOI, as a local COG.

EGMS needs a login, so download the Ortho 'U' tiles covering the AOI by hand from
EGMS Explorer and unzip them flat into data/raw/egms/ (the AOI spans two 100 km
tiles, E56N26 and E57N26). This reads their CSVs, not the TIFFs: the E57N26 TIFF
is shifted one cell. It writes data/processed/ground.tif: mean_velocity in mm/yr
on the EGMS 100 m grid, NaN where EGMS has no cell.

  uv run python pipeline/ground.py                                      # build ground.tif
  uv run python pipeline/ground.py --plots data/sample/plots.geojson    # data test (milestone 3)

--plots reads ground.tif and prints, per plot, how many EGMS cells have their centre
inside it and their median velocity; then a summary per size class. It writes nothing.
"""
import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.transform import from_origin
from rasterio.warp import transform_bounds, transform_geom

from flood_common import AOI

# EGMS Ortho grid: ETRS89-LAEA, 100 m cells centred on ...50 m, in 100 km tiles.
CRS, CELL, TILE = "EPSG:3035", 100, 100_000
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "egms"
OUT = ROOT / "data" / "processed" / "ground.tif"
# e.g. EGMS_L3_E57N26_100km_U_2020_2025_1.csv -> tile E57N26, release 2020-2025
NAME = re.compile(r"EGMS_L3_(E\d+N\d+)_100km_U_(\d{4})_(\d{4})_\d+\.csv")


def read_points(path, bounds):
    """(easting, northing, mean_velocity) of the cells in one CSV that fall inside bounds.

    Reads only three columns by index; the ~300 time-series columns are never parsed.
    """
    x0, y0, x1, y1 = bounds
    points = []
    with open(path, newline="") as f:
        rows = csv.reader(f)
        header = next(rows)
        try:
            #find the three columns by name; their positions differ between files (1, 2 and 5 in EGMS's CSVs)
            ie, i_n, iv = (header.index(c) for c in ("easting", "northing", "mean_velocity"))
        except ValueError:
            #this happens in case the csv file has a missing column
            sys.exit(f"{path.name}: missing easting/northing/mean_velocity column")
        for line, row in enumerate(rows, start=2):
            #we start with the second line because the header is the first
            e, n = float(row[ie]), float(row[i_n])
            #the EGMS grid uses 100 m cells whose centers end in 50 meters
            #this checks the condition
            if e % CELL != CELL / 2 or n % CELL != CELL / 2:
                sys.exit(f"{path.name} line {line}: point ({e}, {n}) is not on the {CELL} m EGMS grid "
                         f"(centres end in {CELL // 2}); is this an EGMS Ortho L3 file?")
            #if our point is in bounds and mean_velocity has a value, we store it
            if x0 < e < x1 and y0 < n < y1 and row[iv] != "":
                points.append((e, n, float(row[iv])))
    return points


def build():
    # Grid: the AOI's bounding box in EPSG:3035, snapped outward to EGMS cell edges (multiples of 100 m).
    bx0, by0, bx1, by1 = transform_bounds("EPSG:4326", CRS, *AOI, densify_pts=21)
    x0, y0 = math.floor(bx0 / CELL) * CELL, math.floor(by0 / CELL) * CELL
    x1, y1 = math.ceil(bx1 / CELL) * CELL, math.ceil(by1 / CELL) * CELL
    #the grid's size in 100 m cells; the bounds above are also passed to read_points
    width, height = (x1 - x0) // CELL, (y1 - y0) // CELL

    # A tile is named by its lower-left corner in 100 km units: E57N26 = x 5,700,000 / y 2,600,000.
    # A tile left out would silently turn into "unknown", so insist on all of them.
    need = {f"E{ix}N{iy}" for ix in range(x0 // TILE, (x1 - 1) // TILE + 1)
            for iy in range(y0 // TILE, (y1 - 1) // TILE + 1)}
    #This creates a Python set containing all the tile names needed to cover your raster.
    tiles = {}
    for path in sorted(RAW.glob("*.csv")):
        if m := NAME.fullmatch(path.name):
            if m[1] in tiles:
                sys.exit(f"two CSVs for tile {m[1]} in {RAW}: keep one")
            tiles[m[1]] = (path, f"{m[2]}-{m[3]}")
    if missing := need - tiles.keys():
        sys.exit(f"missing EGMS tiles for the AOI: {sorted(missing)}. "
                 f"Download the Ortho U tiles from EGMS Explorer and unzip them into {RAW}")
    if len(releases := {tiles[t][1] for t in need}) != 1:
        sys.exit(f"tiles come from different EGMS releases: {sorted(releases)}")
    release = releases.pop()

    points = [p for t in sorted(need) for p in read_points(tiles[t][0], (x0, y0, x1, y1))]
    if not points:
        sys.exit(f"no EGMS cells inside AOI {AOI}: check the tiles in {RAW}")
    e, n, v = np.array(points).T
    band = np.full((height, width), np.nan, dtype="float32")  # no cell stays NaN (unknown), never 0
    band[((y1 - n) // CELL).astype(int), ((e - x0) // CELL).astype(int)] = v

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(OUT, "w", driver="COG", dtype="float32", count=1, crs=CRS,
                       width=width, height=height, transform=from_origin(x0, y1, CELL, CELL),
                       nodata=float("nan"), compress="deflate") as dst:
        dst.write(band, 1)
        dst.update_tags(RELEASE=release, UNITS="mm/yr", SOURCE="EGMS Ortho L3 U mean_velocity")

    print(f"wrote {OUT} ({width}x{height} px, {CELL} m) from tiles {sorted(need)}, release {release}; "
          f"{v.size} cells have data ({v.size / band.size:.1%}); velocity mm/yr: "
          f"min {v.min():.1f}, median {np.median(v):.1f}, max {v.max():.1f}")
    if np.abs(v).max() > 100:
        print("WARNING: |velocity| above 100 mm/yr is rare; check the units of the product.")


def ring_area(ring):
    """Shoelace area of one ring, in the units of its coordinates squared (sign dropped)."""
    x, y = np.array(ring, dtype=float).T
    return abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))) / 2


def plot_cells(geometry, band, transform):
    """(area in ha, EGMS cells whose centre lies inside, median mm/yr or None) for one WGS84 polygon.

    None means unknown: no cell, so no measurement. It is never turned into 0.
    """
    geom = transform_geom("EPSG:4326", CRS, geometry)
    polygons = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    area_m2 = sum(ring_area(p[0]) - sum(ring_area(h) for h in p[1:]) for p in polygons)
    # all_touched=False: a cell counts only if its centre is inside the plot.
    inside = geometry_mask([geom], out_shape=band.shape, transform=transform, all_touched=False, invert=True)
    values = band[inside & np.isfinite(band)]
    return area_m2 / 10_000, values.size, float(np.median(values)) if values.size else None


def report_plots(plots_path):
    """Print the EGMS cells per plot and a summary per size class. Writes nothing."""
    if not OUT.exists():
        sys.exit(f"{OUT} not found: run `uv run python pipeline/ground.py` first to build it")
    with rasterio.open(OUT) as src:
        band, transform = src.read(1), src.transform
        release = src.tags().get("RELEASE", "?")
    features = json.loads(Path(plots_path).read_text())["features"]

    print(f"EGMS cells per plot (centre inside), {OUT.name} release {release}")
    print(f"{'name':<24} {'size_class':<11} {'area_ha':>8}  {'land_cover':<18} {'cells':>5}  median mm/yr")
    by_class = {}
    for f in features:
        props = f["properties"]
        area, cells, median = plot_cells(f["geometry"], band, transform)
        by_class.setdefault(props["size_class"], []).append(cells)
        shown = "unknown" if median is None else f"{median:.1f}"
        print(f"{props['name']:<24} {props['size_class']:<11} {area:8.2f}  {props['land_cover']:<18} "
              f"{cells:5d}  {shown}")

    print("per size class:")
    order = ["under_1_ha", "1_to_5_ha", "over_5_ha"]  # any other class the file uses goes last
    for size_class in sorted(by_class, key=lambda c: order.index(c) if c in order else len(order)):
        counts = by_class[size_class]
        print(f"  {size_class:<11} plots {len(counts):2d}, with >=1 cell {sum(c > 0 for c in counts):2d}, "
              f"cells per plot {sum(counts) / len(counts):.1f}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--plots", metavar="PATH",
                   help="GeoJSON of WGS84 plots: print EGMS cells per plot from ground.tif (writes nothing)")
    a = p.parse_args()
    if a.plots:
        report_plots(a.plots)
    else:
        build()


if __name__ == "__main__":
    main()
