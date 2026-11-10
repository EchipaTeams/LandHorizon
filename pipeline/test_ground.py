import numpy as np
import pytest
import rasterio

import ground


def write_csv(raw, points):
    raw.mkdir()
    lines = ["pid,easting,northing,mean_velocity,20201209"]
    lines += [f"p{i},{e},{n},{v},0.0" for i, (e, n, v) in enumerate(points)]
    (raw / "tile.csv").write_text("\n".join(lines) + "\n")


def test_ground(tmp_path, monkeypatch):
    # Three neighbouring cells inside the AOI: -3.5 mm/yr, measured 0, and one with no point.
    write_csv(tmp_path / "egms", [(5701050, 2653950, -3.5), (5701150, 2653950, 0)])
    monkeypatch.setattr(ground, "RAW", tmp_path / "egms")
    monkeypatch.setattr(ground, "OUT", tmp_path / "ground.tif")
    ground.main()

    with rasterio.open(tmp_path / "ground.tif") as src:
        band = src.read(1)
        assert src.crs.to_epsg() == 3035
        assert src.tags()["RELEASE"] == ground.RELEASE
        moving = band[src.index(5701050, 2653950)]
        still = band[src.index(5701150, 2653950)]
        empty = band[src.index(5701250, 2653950)]

    assert moving == pytest.approx(-3.5)
    assert still == 0  # a measured 0 is real data
    assert np.isnan(empty)  # the unknown rule: no point is NaN, never 0
    assert np.isfinite(band).sum() == 2


def test_off_grid_point_stops(tmp_path, monkeypatch):
    write_csv(tmp_path / "egms", [(5701000, 2653950, -3.5)])  # a cell edge, not a centre
    monkeypatch.setattr(ground, "RAW", tmp_path / "egms")
    monkeypatch.setattr(ground, "OUT", tmp_path / "ground.tif")
    with pytest.raises(SystemExit, match="not on the 100 m EGMS grid"):
        ground.main()
    assert not (tmp_path / "ground.tif").exists()


BOUNDS = (5700000, 2650000, 5710000, 2660000)  # an EPSG:3035 box around the test cells


def test_blank_lines_are_skipped(tmp_path):
    path = tmp_path / "tile.csv"
    path.write_text("easting,northing,mean_velocity\n\n5701050,2653950,-3.5\n\n")
    assert ground.read_points(path, BOUNDS) == [(5701050, 2653950, -3.5)]


def test_bom_before_header(tmp_path):
    path = tmp_path / "tile.csv"
    path.write_text("﻿easting,northing,mean_velocity\n5701050,2653950,-3.5\n", encoding="utf-8")
    assert ground.read_points(path, BOUNDS) == [(5701050, 2653950, -3.5)]


def test_empty_file_stops(tmp_path):
    path = tmp_path / "tile.csv"
    path.write_text("")
    with pytest.raises(SystemExit, match="empty file"):
        ground.read_points(path, BOUNDS)
