import numpy as np
import pytest
import rasterio

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
    ground.main()

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
        ground.main()
    assert not out.exists()


def test_off_grid_point_stops(paths):
    raw, out = paths
    write_tiles(raw, [(5701000, 2653950, -3.5)])  # a cell edge, not a centre
    with pytest.raises(SystemExit, match="not on the 100 m EGMS grid"):
        ground.main()
    assert not out.exists()
