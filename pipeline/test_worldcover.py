import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

import flood_common
import worldcover


@pytest.fixture
def source(tmp_path, monkeypatch):
    """A 3x3 km WorldCover-like raster (10 m, WGS84 like the real tile) over a small AOI; one pixel has no data."""
    monkeypatch.setattr(flood_common, "AOI", [28.0, 45.4, 28.01, 45.41])
    monkeypatch.setattr(worldcover, "OUT", tmp_path / "worldcover.tif")
    codes = np.tile(np.array([10, 30, 40, 50, 80], dtype="uint8"), (200, 40))[:200, :200]
    codes[0, 0] = 0
    path = tmp_path / "wc.tif"
    with rasterio.open(path, "w", driver="GTiff", dtype="uint8", count=1, width=200, height=200, crs="EPSG:4326",
                       transform=from_origin(27.99, 45.42, 0.0001, 0.0001), nodata=0) as dst:
        dst.write(codes, 1)
    monkeypatch.setattr(worldcover, "URL", str(path))
    return path


def test_class_codes_survive_and_no_data_stays_zero(source):
    with rasterio.open(source) as src:
        cover = worldcover.cut(src)
    assert cover.dtype == "uint8"
    assert set(np.unique(cover)) <= {0, 10, 30, 40, 50, 80}  # nothing averaged in between
    assert (cover == 40).any()


def test_outside_the_tile_is_no_data(source, monkeypatch):
    monkeypatch.setattr(flood_common, "AOI", [28.05, 45.4, 28.06, 45.41])  # east of the source raster
    with rasterio.open(source) as src:
        assert (worldcover.cut(src) == 0).all()  # no data, never a class


def test_output_is_on_the_flood_grid(source):
    worldcover.main()
    transform, width, height = flood_common.grid()
    with rasterio.open(worldcover.OUT) as dst, rasterio.open(source) as src:
        assert (dst.transform, dst.width, dst.height) == (transform, width, height)
        assert dst.crs.to_epsg() == 32635 and dst.nodata == 0 and dst.dtypes == ("uint8",)
        assert (dst.read(1) == worldcover.cut(src)).all()
