import json

import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import transform_geom

import ground

HEADER = "pid,easting,northing,mean_velocity,20201209"


def write_tiles(raw, points, tiles=("E56N26", "E57N26")):
    """The AOI's two EGMS tiles, named as EGMS delivers them; all test points go in E57N26."""
    raw.mkdir()
    for tile in tiles:
        rows = [f"p{i},{e},{n},{v},0.0" for i, (e, n, v) in enumerate(points)] if tile == "E57N26" else []
        (raw / f"EGMS_L3_{tile}_100km_U_2020_2025_1.csv").write_text("\n".join([HEADER, *rows]) + "\n")


@pytest.fixture
def paths(tmp_path, monkeypatch):
    monkeypatch.setattr(ground, "RAW", tmp_path / "egms")
    monkeypatch.setattr(ground, "OUT", tmp_path / "ground.tif")
    return tmp_path / "egms", tmp_path / "ground.tif"


def test_ground(paths):
    raw, out = paths
    # Three neighbouring cells inside the AOI: -3.5 mm/yr, measured 0, and one with no point.
    write_tiles(raw, [(5701050, 2653950, -3.5), (5701150, 2653950, 0)])
    ground.build()

    with rasterio.open(out) as src:
        band = src.read(1)
        assert src.crs.to_epsg() == 3035
        assert src.tags()["RELEASE"] == "2020-2025"  # read from the file names
        moving = band[src.index(5701050, 2653950)]
        still = band[src.index(5701150, 2653950)]
        empty = band[src.index(5701250, 2653950)]

    assert moving == pytest.approx(-3.5)
    assert still == 0  # a measured 0 is real data
    assert np.isnan(empty)  # the unknown rule: no point is NaN, never 0
    assert np.isfinite(band).sum() == 2


def test_missing_tile_stops(paths):
    raw, out = paths
    write_tiles(raw, [(5701050, 2653950, -3.5)], tiles=("E57N26",))  # E56N26 not downloaded
    with pytest.raises(SystemExit, match=r"missing EGMS tiles for the AOI: \['E56N26'\]"):
        ground.build()
    assert not out.exists()


def test_off_grid_point_stops(paths):
    raw, out = paths
    write_tiles(raw, [(5701000, 2653950, -3.5)])  # a cell edge, not a centre
    with pytest.raises(SystemExit, match="not on the 100 m EGMS grid"):
        ground.build()
    assert not out.exists()


# --plots: a 3x2 ground.tif built here, cells 100 m; centres at x 5700050/150/250, y 2653950/850.
#   row 0:  -2.0  -4.0   NaN
#   row 1:   1.0   NaN   NaN
X0, Y1 = 5_700_000, 2_654_000


def box(x0, y0, x1, y1):
    """A WGS84 polygon from an EPSG:3035 box, as a plot drawn on the map would arrive."""
    ring = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    return transform_geom(ground.CRS, "EPSG:4326", {"type": "Polygon", "coordinates": [ring]})


@pytest.fixture
def grid(paths):
    _, out = paths
    band = np.array([[-2.0, -4.0, np.nan], [1.0, np.nan, np.nan]], dtype="float32")
    with rasterio.open(out, "w", driver="GTiff", dtype="float32", count=1, crs=ground.CRS, width=3, height=2,
                       transform=from_origin(X0, Y1, ground.CELL, ground.CELL), nodata=float("nan")) as dst:
        dst.write(band, 1)
    return band, from_origin(X0, Y1, ground.CELL, ground.CELL)


def test_plot_counts_cell_centres(grid):
    band, transform = grid
    # 60 x 60 m around the centre of cell (0, 0)
    area, cells, median = ground.plot_cells(box(X0 + 20, Y1 - 80, X0 + 80, Y1 - 20), band, transform)
    assert area == pytest.approx(0.36, abs=1e-3)
    assert (cells, median) == (1, -2.0)
    # centres of (0,0), (0,1), (1,0) and the empty (1,1): three cells with data
    _, cells, median = ground.plot_cells(box(X0 + 20, Y1 - 180, X0 + 180, Y1 - 20), band, transform)
    assert (cells, median) == (3, -2.0)


def test_plot_on_cell_edge_counts_nothing(grid):
    band, transform = grid
    # straddles the edge between (0,0) and (0,1) without reaching either centre
    _, cells, median = ground.plot_cells(box(X0 + 60, Y1 - 80, X0 + 140, Y1 - 20), band, transform)
    assert cells == 0
    assert median is None


def test_plot_without_cells_is_unknown(grid, tmp_path, capsys):
    plots = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": {"name": "no-data", "area_ha": 0.4, "size_class": "under_1_ha",
                                           "land_cover": "grass"},
         "geometry": box(X0 + 220, Y1 - 80, X0 + 280, Y1 - 20)}]}  # covers the centre of the NaN cell (0, 2)
    path = tmp_path / "plots.geojson"
    path.write_text(json.dumps(plots))
    ground.report_plots(path)

    row = next(line for line in capsys.readouterr().out.splitlines() if line.startswith("no-data"))
    assert row.split()[-2:] == ["0", "unknown"]  # 0 cells, and the median is unknown, never 0


def test_plots_without_ground_tif_stops(paths, tmp_path):
    with pytest.raises(SystemExit, match="run `uv run python pipeline/ground.py` first"):
        ground.report_plots(tmp_path / "plots.geojson")
