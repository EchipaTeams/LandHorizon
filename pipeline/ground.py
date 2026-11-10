"""Ground motion: EGMS Ortho vertical (U) velocity for the AOI, as a local COG.

EGMS needs a login, so the 100 km tiles are downloaded by hand from EGMS Explorer
and unzipped flat into data/raw/egms/. This reads their CSVs (not the TIFFs: the
E57N26 TIFF is shifted one cell) and writes data/processed/ground.tif:
mean_velocity in mm/yr on the EGMS 100 m grid, NaN where EGMS has no cell.

  uv run python pipeline/ground.py
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import transform, transform_bounds

from flood import AOI

RELEASE = "2020-2025"  # EGMS release the tiles come from; stored as a tag in the TIFF
CRS, CELL = "EPSG:3035", 100  # EGMS Ortho grid: ETRS89-LAEA, 100 m cells centred on ...50 m
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "egms"
OUT = ROOT / "data" / "processed" / "ground.tif"


def read_points(path, bounds):
    """(easting, northing, mean_velocity) of the cells in one CSV that fall inside bounds.

    Reads only three columns by index; the ~300 time-series columns are never parsed.
    """
    x0, y0, x1, y1 = bounds
    points = []
    with open(path, newline="", encoding="utf-8-sig") as f:  # -sig: tolerate a BOM before the header
        rows = csv.reader(f)
        header = next(rows, None)
        if header is None:
            sys.exit(f"{path.name}: empty file; re-download or remove it")
        try:
            ie, i_n, iv = (header.index(c) for c in ("easting", "northing", "mean_velocity"))
        except ValueError:
            sys.exit(f"{path.name}: missing easting/northing/mean_velocity column")
        for line, row in enumerate(rows, start=2):
            if not row:  # blank line, e.g. at the end of the file
                continue
            e, n = float(row[ie]), float(row[i_n])
            if e % CELL != CELL / 2 or n % CELL != CELL / 2:
                sys.exit(f"{path.name} line {line}: point ({e}, {n}) is not on the {CELL} m EGMS grid "
                         f"(centres end in {CELL // 2}); is this an EGMS Ortho L3 file?")
            if x0 < e < x1 and y0 < n < y1 and row[iv] != "":
                points.append((e, n, float(row[iv])))
    return points


def main():
    csvs = sorted(RAW.glob("*.csv"))
    if not csvs:
        sys.exit(f"no CSVs in {RAW}: download EGMS Ortho U tiles from EGMS Explorer and unzip them there")

    # Grid: the AOI's bounding box in EPSG:3035, snapped outward to EGMS cell edges (multiples of 100 m).
    bx0, by0, bx1, by1 = transform_bounds("EPSG:4326", CRS, *AOI, densify_pts=21)
    x0, y0 = math.floor(bx0 / CELL) * CELL, math.floor(by0 / CELL) * CELL
    x1, y1 = math.ceil(bx1 / CELL) * CELL, math.ceil(by1 / CELL) * CELL
    width, height = (x1 - x0) // CELL, (y1 - y0) // CELL

    points = [p for path in csvs for p in read_points(path, (x0, y0, x1, y1))]
    e, n, v = np.array(points, dtype="float64").reshape(-1, 3).T
    # The AOI is a lon/lat box, so its 3035 bounding box has extra corners: keep only centres inside the AOI.
    lon, lat = transform(CRS, "EPSG:4326", e, n)
    lon, lat = np.array(lon), np.array(lat)
    inside = (lon >= AOI[0]) & (lon <= AOI[2]) & (lat >= AOI[1]) & (lat <= AOI[3])
    e, n, v = e[inside], n[inside], v[inside]
    if e.size == 0:
        sys.exit(f"no EGMS cells inside AOI {AOI}: do the tiles in {RAW} cover it?")

    cols = ((e - x0) // CELL).astype(int)
    rows = ((y1 - n) // CELL).astype(int)
    if len(set(zip(rows, cols))) != e.size:
        sys.exit(f"some cells appear in more than one CSV: remove duplicate tiles from {RAW}")
    band = np.full((height, width), np.nan, dtype="float32")  # no cell stays NaN (unknown), never 0
    band[rows, cols] = v

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(OUT, "w", driver="COG", dtype="float32", count=1, crs=CRS,
                       width=width, height=height, transform=from_origin(x0, y1, CELL, CELL),
                       nodata=float("nan"), compress="deflate") as dst:
        dst.write(band, 1)
        dst.update_tags(RELEASE=RELEASE, UNITS="mm/yr", SOURCE="EGMS Ortho L3 U mean_velocity")

    print(f"wrote {OUT} ({width}x{height} px, {CELL} m) from {len(csvs)} CSVs, release {RELEASE}; "
          f"{e.size} cells in AOI; velocity mm/yr: min {np.nanmin(band):.1f}, "
          f"median {np.nanmedian(band):.1f}, max {np.nanmax(band):.1f}, NaN {np.isnan(band).mean():.1%}")


if __name__ == "__main__":
    main()
