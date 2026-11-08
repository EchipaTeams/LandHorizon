import numpy as np
import rasterio
from fastapi.testclient import TestClient
from rasterio.transform import from_origin

import main

client = TestClient(main.app)


def square(lon, lat, d=0.001):
    return {"type": "Polygon",
            "coordinates": [[[lon, lat], [lon + d, lat], [lon + d, lat + d], [lon, lat + d], [lon, lat]]]}


def test_terrain(tmp_path, monkeypatch):
    # 10x10 px of 0.001° over lon 28.00–28.01, lat 45.40–45.41: left half HAND 2 m, right half no data.
    data = np.full((1, 10, 10), 2.0, dtype="float32")
    data[:, :, 5:] = np.nan
    path = tmp_path / "hand.tif"
    with rasterio.open(path, "w", driver="GTiff", width=10, height=10, count=1, dtype="float32",
                       crs="EPSG:4326", transform=from_origin(28.0, 45.41, 0.001, 0.001),
                       nodata=float("nan")) as dst:
        dst.write(data)
    monkeypatch.setattr(main, "HAND_PATH", path)

    measured = client.post("/evidence", json=square(28.001, 45.401)).json()["terrain"]
    assert measured == {"status": "measured", "hand_m": 2.0}

    no_data = client.post("/evidence", json=square(28.0065, 45.401)).json()["terrain"]
    assert no_data == {"status": "unknown", "hand_m": None}  # the unknown rule

    assert client.post("/evidence", json=square(45.401, 28.001)).status_code == 422  # lat/lon swapped

    monkeypatch.setattr(main, "HAND_PATH", tmp_path / "missing.tif")
    assert client.post("/evidence", json=square(28.001, 45.401)).status_code == 503
