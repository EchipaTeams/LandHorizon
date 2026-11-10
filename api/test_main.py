import numpy as np
import pytest
import rasterio
from fastapi.testclient import TestClient
from rasterio.transform import from_origin

import main

client = TestClient(main.app)
# Every test raster: 10x10 px of 0.001° over lon 28.00–28.01, lat 45.40–45.41.
GRID = dict(driver="GTiff", width=10, height=10, crs="EPSG:4326", transform=from_origin(28.0, 45.41, 0.001, 0.001))


def square(lon, lat, d=0.001):
    return {"type": "Polygon",
            "coordinates": [[[lon, lat], [lon + d, lat], [lon + d, lat + d], [lon, lat + d], [lon, lat]]]}


LEFT, RIGHT = square(28.001, 45.401), square(28.0065, 45.401)  # left half / right half of the test raster


@pytest.fixture
def layers(tmp_path, monkeypatch):
    """HAND: left half 2 m, right half no data. Flood: left half seen by 3 passes, right half never seen
    (GFM excluded it). One pass (14 Sept) saw water on the whole left half, another (21 Sept) on one pixel."""
    hand = np.full((1, 10, 10), 2.0, dtype="float32")
    hand[:, :, 5:] = np.nan
    with rasterio.open(tmp_path / "hand.tif", "w", count=1, dtype="float32", nodata=float("nan"), **GRID) as dst:
        dst.write(hand)

    n_passes = np.zeros((10, 10), "uint16")
    n_passes[:, :5] = 3
    sept14 = np.zeros((10, 10), "uint16")
    sept14[:, :5] = 1
    sept21 = np.zeros((10, 10), "uint16")
    sept21[5, 4] = 1  # one wet pixel (lon 28.004, lat 45.404): 1 of 25 px = 4 %, under FLOOD_DATE_MIN_SHARE
    n_flooded = sept14 + sept21
    with rasterio.open(tmp_path / "flood.tif", "w", count=4, dtype="uint16", **GRID) as dst:
        dst.write(np.stack([n_flooded, n_passes, sept14, sept21]))
        dst.descriptions = ("n_flooded", "n_passes", "2024-09-14T04", "2024-09-21T04")
        dst.update_tags(period_start="2024-01-01", period_end="2025-01-01")  # as flood_gfm.py writes them

    monkeypatch.setattr(main, "HAND_PATH", tmp_path / "hand.tif")
    monkeypatch.setattr(main, "FLOOD_PATH", tmp_path / "flood.tif")
    return tmp_path


def test_terrain(layers, monkeypatch):
    assert client.post("/evidence", json=LEFT).json()["terrain"] == {"status": "measured", "hand_m": 2.0}
    assert client.post("/evidence", json=RIGHT).json()["terrain"] == {"status": "unknown", "hand_m": None}

    assert client.post("/evidence", json=square(45.401, 28.001)).status_code == 422  # lat/lon swapped

    monkeypatch.setattr(main, "HAND_PATH", layers / "missing.tif")
    assert client.post("/evidence", json=LEFT).status_code == 503


def test_flood(layers, monkeypatch):
    measured = client.post("/evidence", json=LEFT).json()["flood"]
    assert measured == {"status": "measured", "flood_dates": ["2024-09-14"], "n_passes": 3,
                        "flooded_fraction": 1.0, "algorithm_version": "gfm-ensemble",
                        "period_start": "2024-01-01", "period_end": "2024-12-31"}  # end reported inclusive

    # A 5x5 px plot holds the 21 Sept wet pixel, but 1 of 25 px (4 %) is under the 5 % rule...
    big = square(28.0002, 45.4002, d=0.0045)
    assert client.post("/evidence", json=big).json()["flood"]["flood_dates"] == ["2024-09-14"]
    # ...and it's the rule that drops it: with a 1 % rule the date appears.
    monkeypatch.setattr(main, "FLOOD_DATE_MIN_SHARE", 0.01)
    assert client.post("/evidence", json=big).json()["flood"]["flood_dates"] == ["2024-09-14", "2024-09-21"]
    monkeypatch.setattr(main, "FLOOD_DATE_MIN_SHARE", 0.05)

    # The unknown rule: a plot no pass could see is "unknown" with no fraction, never "0 % flooded".
    unseen = client.post("/evidence", json=RIGHT).json()["flood"]
    assert unseen == {"status": "unknown", "flood_dates": [], "n_passes": 0,
                      "flooded_fraction": None, "algorithm_version": "gfm-ensemble",
                      "period_start": "2024-01-01", "period_end": "2024-12-31"}  # the period is known even here

    monkeypatch.setattr(main, "FLOOD_PATH", layers / "missing.tif")
    assert client.post("/evidence", json=LEFT).status_code == 503
