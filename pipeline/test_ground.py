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
    area, fit, cells, median = ground.plot_cells(box(X0 + 20, Y1 - 80, X0 + 80, Y1 - 20), band, transform)
    assert area == pytest.approx(0.36, abs=1e-3)
    assert (fit, cells, median) == (1, 1, -2.0)
    # centres of (0,0), (0,1), (1,0) and the empty (1,1): four cells fit, three have data
    _, fit, cells, median = ground.plot_cells(box(X0 + 20, Y1 - 180, X0 + 180, Y1 - 20), band, transform)
    assert (fit, cells, median) == (4, 3, -2.0)


def test_plot_counts_the_cells_that_fit_and_the_ones_with_data(grid):
    band, transform = grid
    # centres of (0,1) = -4.0 and (0,2) = NaN: two cells fit, one has data, the median is of that one
    _, fit, cells, median = ground.plot_cells(box(X0 + 120, Y1 - 80, X0 + 280, Y1 - 20), band, transform)
    assert (fit, cells, median) == (2, 1, -4.0)
    # the centre of the NaN cell (0, 2) only: a cell fits, none has data, so unknown, never 0
    _, fit, cells, median = ground.plot_cells(box(X0 + 220, Y1 - 80, X0 + 280, Y1 - 20), band, transform)
    assert (fit, cells, median) == (1, 0, None)


def test_plot_on_cell_edge_counts_nothing(grid):
    band, transform = grid
    # straddles the edge between (0,0) and (0,1) without reaching either centre: no cell fits at all
    _, fit, cells, median = ground.plot_cells(box(X0 + 60, Y1 - 80, X0 + 140, Y1 - 20), band, transform)
    assert (fit, cells) == (0, 0)
    assert median is None


def report_rows(tmp_path, capsys, **plots):
    """Run --plots on plots given as name=(size_class, geometry); return the printed lines."""
    features = [{"type": "Feature", "properties": {"name": name, "area_ha": 0.4, "size_class": size_class,
                                                   "land_cover": "grass"}, "geometry": geometry}
                for name, (size_class, geometry) in plots.items()]
    path = tmp_path / "plots.geojson"
    path.write_text(json.dumps({"type": "FeatureCollection", "features": features}))
    ground.report_plots(path)
    return capsys.readouterr().out.splitlines()


def test_plot_without_data_is_unknown(grid, tmp_path, capsys):
    lines = report_rows(tmp_path, capsys, **{
        "no-data": ("under_1_ha", box(X0 + 220, Y1 - 80, X0 + 280, Y1 - 20)),  # covers the centre of the NaN cell (0, 2)
        "no-cell": ("under_1_ha", box(X0 + 60, Y1 - 80, X0 + 140, Y1 - 20))})  # no cell centre at all
    row = lambda name: next(line for line in lines if line.startswith(name)).split()
    assert row("no-data")[-5:] == ["0", "of", "1", "0%", "unknown"]  # a cell fits, it has no data
    # no cell fits: a share of 0 of 0 is not 0 %, it is not defined
    assert row("no-cell")[-5:] == ["0", "of", "0", "-", "unknown"]


def test_report_shows_the_cells_that_fit_and_the_share(grid, tmp_path, capsys):
    lines = report_rows(tmp_path, capsys, **{
        "half": ("under_1_ha", box(X0 + 120, Y1 - 80, X0 + 280, Y1 - 20)),    # (0,1) has data, (0,2) doesn't
        "full": ("1_to_5_ha", box(X0 + 20, Y1 - 80, X0 + 80, Y1 - 20)),       # (0,0) has data
        "none": ("1_to_5_ha", box(X0 + 220, Y1 - 80, X0 + 280, Y1 - 20))})    # (0,2) doesn't
    row = lambda name: next(line for line in lines if line.startswith(name)).split()
    assert row("half")[-5:] == ["1", "of", "2", "50%", "-4.0"]
    assert row("full")[-5:] == ["1", "of", "1", "100%", "-2.0"]
    # per size class: 1 cell of 2 fits with data; 1 of 2 cells in total, one of the two plots has a cell with data
    summary = {line.split()[0]: line for line in lines[lines.index("per size class:") + 1:]}
    assert "cells that fit 2.0 per plot, with data 1.0, share 50%, plots with data 1 of 1" in summary["under_1_ha"]
    assert "cells that fit 1.0 per plot, with data 0.5, share 50%, plots with data 1 of 2" in summary["1_to_5_ha"]


def test_plots_without_ground_tif_stops(paths, tmp_path):
    with pytest.raises(SystemExit, match="run `uv run python pipeline/ground.py` first"):
        ground.report_plots(tmp_path / "plots.geojson")
