import math

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
    (GFM excluded it). One pass (14 Sept) saw water on the whole left half, another (21 Sept) on one pixel.
    Ground: four cells with data in the lower left (a 2x2 block), no cell anywhere else.
    WorldCover (on the flood grid): cols 0-3 are trees in rows 0-4 and cropland in rows 5-9; col 4 and the right
    half have no data."""
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

    ground = np.full((10, 10), np.nan, dtype="float32")  # mm/yr; NaN = EGMS has no cell there
    ground[8, 1], ground[7, 1], ground[8, 2], ground[7, 2] = -3.2, -1.0, 1.4, -2.0  # [8, 1] is the cell under LEFT
    with rasterio.open(tmp_path / "ground.tif", "w", count=1, dtype="float32", nodata=float("nan"), **GRID) as dst:
        dst.write(ground, 1)
        dst.update_tags(RELEASE="2020-2025")  # as ground.py writes it

    cover = np.zeros((10, 10), "uint8")  # 0 = no data
    cover[:5, :4], cover[5:, :4] = 10, main.CROPLAND
    with rasterio.open(tmp_path / "worldcover.tif", "w", count=1, dtype="uint8", nodata=0, **GRID) as dst:
        dst.write(cover, 1)

    monkeypatch.setattr(main, "GROUND_PATH", tmp_path / "ground.tif")
    monkeypatch.setattr(main, "WORLDCOVER_PATH", tmp_path / "worldcover.tif")
    monkeypatch.setattr(main, "HAND_PATH", tmp_path / "hand.tif")
    monkeypatch.setattr(main, "FLOOD_PATH", tmp_path / "flood.tif")
    return tmp_path


def test_terrain(layers, monkeypatch):
    assert client.post("/evidence", json=LEFT).json()["terrain"] == {"status": "measured", "hand_m": 2.0}
    assert client.post("/evidence", json=RIGHT).json()["terrain"] == {"status": "unknown", "hand_m": None}

    # The share rule: 3x3 px plots across the data/no-data edge (HAND has data in columns 0-4).
    mostly = client.post("/evidence", json=square(28.0032, 45.4012, d=0.0026)).json()["terrain"]  # 2 of 3 columns
    assert mostly == {"status": "measured", "hand_m": 2.0}
    barely = client.post("/evidence", json=square(28.0042, 45.4012, d=0.0026)).json()["terrain"]  # 1 of 3 columns
    assert barely == {"status": "unknown", "hand_m": None}  # a median from one corner doesn't describe the plot

    assert client.post("/evidence", json=square(45.401, 28.001)).status_code == 422  # lat/lon swapped

    monkeypatch.setattr(main, "HAND_PATH", layers / "missing.tif")
    assert client.post("/evidence", json=LEFT).status_code == 503


def test_plot_across_the_edge_is_refused(layers):
    # Half of this plot is east of the test raster (it ends at lon 28.01). Answering from the half inside
    # would describe a different plot, so it is refused, as a plot wholly outside is.
    across = client.post("/evidence", json=square(28.0095, 45.401))
    assert across.status_code == 422
    assert "partly or fully outside the covered area (hand.tif)" in across.json()["detail"]
    # Just inside the north-east corner (0.0001°, about 8 m, from both edges): answered.
    assert client.post("/evidence", json=square(28.0089, 45.4089)).status_code == 200


def test_flood(layers, monkeypatch):
    measured = client.post("/evidence", json=LEFT).json()["flood"]
    assert measured == {"status": "measured", "observed_fraction": 1.0, "flood_dates": ["2024-09-14"], "n_passes": 3,
                        "flooded_fraction": 1.0, "cropland_share": [1.0],
                        "algorithm_version": "gfm-ensemble", "period_start": "2024-01-01", "period_end": "2024-12-31"}  # end reported inclusive

    # A 5x5 px plot holds the 21 Sept wet pixel, but 1 of 25 px (4 %) is under the 5 % rule...
    big = square(28.0002, 45.4002, d=0.0045)
    assert client.post("/evidence", json=big).json()["flood"]["flood_dates"] == ["2024-09-14"]
    # ...and it's the rule that drops it: with a 1 % rule the date appears.
    monkeypatch.setattr(main, "FLOOD_DATE_MIN_SHARE", 0.01)
    assert client.post("/evidence", json=big).json()["flood"]["flood_dates"] == ["2024-09-14", "2024-09-21"]
    monkeypatch.setattr(main, "FLOOD_DATE_MIN_SHARE", 0.05)

    # The unknown rule: a plot no pass could see is "unknown" with no fraction, never "0 % flooded".
    unseen = client.post("/evidence", json=RIGHT).json()["flood"]
    assert unseen == {"status": "unknown", "observed_fraction": 0.0, "flood_dates": [], "n_passes": 0,
                      "flooded_fraction": None, "cropland_share": [], "algorithm_version": "gfm-ensemble",
                      "period_start": "2024-01-01", "period_end": "2024-12-31"}  # the period is known even here

    # A barely observed plot is unknown too. 3x3 px plots across the seen/unseen edge (columns 0-4 are seen):
    mostly = client.post("/evidence", json=square(28.0032, 45.4012, d=0.0026)).json()["flood"]  # 2 of 3 columns seen
    assert (mostly["status"], mostly["observed_fraction"], mostly["flooded_fraction"]) == ("measured", 0.667, 1.0)
    barely = client.post("/evidence", json=square(28.0042, 45.4012, d=0.0026)).json()["flood"]  # 1 of 3 columns seen
    assert barely == {"status": "unknown", "observed_fraction": 0.333, "flood_dates": [], "n_passes": 3,
                      "flooded_fraction": None, "cropland_share": [], "algorithm_version": "gfm-ensemble",  # still unknown
                      "period_start": "2024-01-01", "period_end": "2024-12-31"}

    monkeypatch.setattr(main, "FLOOD_PATH", layers / "missing.tif")
    assert client.post("/evidence", json=LEFT).status_code == 503


def cropland(plot):
    return client.post("/evidence", json=plot).json()["flood"]["cropland_share"]


def flood_file(path, passes):
    """A flood layer on GRID, the left half seen by every pass; passes maps a band name to its wet pixels."""
    bands = np.stack(list(passes.values())).astype("uint16")
    n_passes = np.zeros((10, 10), "uint16")
    n_passes[:, :5] = len(passes)
    with rasterio.open(path, "w", count=2 + len(passes), dtype="uint16", **GRID) as dst:
        dst.write(np.concatenate([[bands.sum(0), n_passes], bands]))
        dst.descriptions = ("n_flooded", "n_passes", *passes)
        dst.update_tags(period_start="2024-01-01", period_end="2025-01-01")
    return path


def test_cropland_share(layers, monkeypatch):
    # One share per flood date, in the order of flood_dates. 14 Sept saw water on the whole left half (cols 0-4).
    # WorldCover no-data pixels (col 4) are left out of the share, not counted as "not cropland".
    assert cropland(square(28.0002, 45.4002, d=0.0045)) == [1.0]  # cols 0-4, rows 5-9: 20 px cropland, 5 no data
    assert cropland(square(28.0002, 45.4042, d=0.0016)) == [0.5]  # cols 0-1, rows 4-5: 2 px trees, 2 px cropland
    assert cropland(square(28.0002, 45.4082, d=0.0016)) == [0.0]  # cols 0-1, rows 0-1: wet, all trees: a real 0
    # WorldCover has no data on the date's wet pixels (col 4): null, not 0 and not 1.
    assert cropland(square(28.0042, 45.4012, d=0.0004)) == [None]
    # A second date (21 Sept, its one wet pixel in col 4, no WorldCover data) gets its own entry.
    monkeypatch.setattr(main, "FLOOD_DATE_MIN_SHARE", 0.01)
    assert cropland(square(28.0002, 45.4002, d=0.0045)) == [1.0, None]
    monkeypatch.setattr(main, "FLOOD_DATE_MIN_SHARE", 0.05)
    # No flood date: an empty list, like flood_dates. Flood unknown (nothing observed): empty too.
    assert cropland(RIGHT) == []

    # Each date counts only its own pixels. Plot: cols 0-1, rows 4-5 (row 4 trees, row 5 cropland). A spring pass
    # wets the cropland row; on 14 Sept one pass wets the trees row and a second the cropland pixel of col 0.
    # Pooled over the history the answer would be 0.5 for both dates.
    wet = {name: np.zeros((10, 10), bool) for name in ("2024-04-30T04", "2024-09-14T04", "2024-09-14T16")}
    wet["2024-04-30T04"][5, :4] = wet["2024-09-14T04"][4, :4] = wet["2024-09-14T16"][5, 0] = True
    monkeypatch.setattr(main, "FLOOD_PATH", flood_file(layers / "two_dates.tif", wet))
    flood = client.post("/evidence", json=square(28.0002, 45.4042, d=0.0016)).json()["flood"]
    assert (flood["flood_dates"], flood["cropland_share"]) == (["2024-04-30", "2024-09-14"], [1.0, 0.333])

    # Seen by passes, but no pass saw water: no date, no share (never a 0).
    dry = {name: np.zeros((10, 10), bool) for name in wet}
    monkeypatch.setattr(main, "FLOOD_PATH", flood_file(layers / "dry.tif", dry))
    dry = client.post("/evidence", json=LEFT).json()["flood"]
    assert (dry["status"], dry["flooded_fraction"], dry["cropland_share"]) == ("measured", 0.0, [])


def test_cropland_layer_missing_is_503(layers, monkeypatch):
    monkeypatch.setattr(main, "WORLDCOVER_PATH", layers / "missing.tif")
    r = client.post("/evidence", json=LEFT)
    assert r.status_code == 503 and "missing.tif" in r.text


def test_cropland_layer_off_the_flood_grid_is_503(layers, monkeypatch):
    with rasterio.open(layers / "worldcover.tif", "w", count=1, dtype="uint8", nodata=0,
                       **{**GRID, "width": 5, "height": 5, "transform": from_origin(28.0, 45.41, 0.002, 0.002)}) as dst:
        dst.write(np.full((5, 5), main.CROPLAND, "uint8"), 1)
    assert client.post("/evidence", json=LEFT).status_code == 503
    # Smaller than the flood grid (e.g. flood_gfm.tif rebuilt on a bigger AOI): a plot outside it is still the
    # server's fault (503), not the user's (422).
    with rasterio.open(layers / "worldcover.tif", "w", count=1, dtype="uint8", nodata=0,
                       **{**GRID, "width": 5, "height": 5}) as dst:  # the left half only
        dst.write(np.full((5, 5), main.CROPLAND, "uint8"), 1)
    assert client.post("/evidence", json=RIGHT).status_code == 503


def test_ground(layers, monkeypatch):
    one = client.post("/evidence", json=LEFT).json()["ground"]
    assert one == {"status": "measured", "velocity_mm_yr": -3.2, "n_cells": 1, "release": "2020-2025"}
    # 2x2 cells: the median of -3.2, -2.0, -1.0 and 1.4.
    four = client.post("/evidence", json=square(28.001, 45.401, d=0.002)).json()["ground"]
    assert four == {"status": "measured", "velocity_mm_yr": -1.5, "n_cells": 4, "release": "2020-2025"}

    # The unknown rule: no EGMS cell under the plot is "unknown" with no velocity, never "0 mm/yr".
    none = client.post("/evidence", json=RIGHT).json()["ground"]
    assert none == {"status": "unknown", "velocity_mm_yr": None, "n_cells": 0, "release": "2020-2025"}

    # The centre rule: a small plot inside the -3.2 cell that doesn't contain its centre gets no cell.
    # (Flood and terrain do count this pixel: they take every pixel a plot touches.)
    corner = client.post("/evidence", json=square(28.0011, 45.4011, d=0.0003)).json()
    assert corner["ground"] == none and corner["plot"]["n_pixels"] == 1

    monkeypatch.setattr(main, "GROUND_PATH", layers / "missing.tif")
    assert client.post("/evidence", json=LEFT).status_code == 503


def test_ground_share(layers, monkeypatch):
    """Ground needs GROUND_MIN_SHARE of the cells whose centre is inside the plot to have data, like terrain and flood."""
    def rectangle(west, south, east, north):
        return {"type": "Polygon", "coordinates": [[[west, south], [east, south], [east, north], [west, north], [west, south]]]}

    # Row 8, cols 2-4: three cells fit and only the first has data (1.4). 1 of 3 is under the share: unknown, yet
    # n_cells says how much data sits behind it, as flood's n_passes does.
    one_of_three = rectangle(28.0021, 45.4011, 28.0049, 45.4019)
    under = client.post("/evidence", json=one_of_three).json()["ground"]
    assert under == {"status": "unknown", "velocity_mm_yr": None, "n_cells": 1, "release": "2020-2025"}

    # Rows 8-9, cols 1-2: four cells fit and two have data (-3.2 and 1.4). 2 of 4 is exactly the share: measured.
    two_of_four = rectangle(28.0011, 45.4001, 28.0029, 45.4019)
    at = client.post("/evidence", json=two_of_four).json()["ground"]
    assert at == {"status": "measured", "velocity_mm_yr": -0.9, "n_cells": 2, "release": "2020-2025"}

    # The constant decides, in both directions.
    monkeypatch.setattr(main, "GROUND_MIN_SHARE", 0.6)
    assert client.post("/evidence", json=two_of_four).json()["ground"]["status"] == "unknown"
    monkeypatch.setattr(main, "GROUND_MIN_SHARE", 0.3)
    assert client.post("/evidence", json=one_of_three).json()["ground"] == {
        "status": "measured", "velocity_mm_yr": 1.4, "n_cells": 1, "release": "2020-2025"}


def test_plot(layers):
    def expected_ha(lat, d):
        """A d x d degree square's area from the length of a degree on the WGS84 ellipsoid at its mid latitude."""
        f = math.radians(lat + d / 2)
        m_per_deg_lat = 111132.92 - 559.82 * math.cos(2 * f) + 1.175 * math.cos(4 * f)
        m_per_deg_lon = 111412.84 * math.cos(f) - 93.5 * math.cos(3 * f)
        return m_per_deg_lat * d * m_per_deg_lon * d / 10_000

    big = client.post("/evidence", json=square(28.0002, 45.4002, d=0.0045)).json()["plot"]  # 5x5 px of the flood grid
    assert big["n_pixels"] == 25 and big["area_ha"] == pytest.approx(expected_ha(45.4002, 0.0045), abs=0.01)
    small = client.post("/evidence", json=square(28.0032, 45.4012, d=0.0026)).json()["plot"]  # 3x3 px
    assert small["n_pixels"] == 9 and small["area_ha"] == pytest.approx(expected_ha(45.4012, 0.0026), abs=0.01)

    # A hole is not part of the plot: the area drops by the hole's area.
    ring = square(28.0002, 45.4002, d=0.0045)["coordinates"][0]
    hole = square(28.002, 45.402, d=0.001)["coordinates"][0]
    holed = client.post("/evidence", json={"type": "Polygon", "coordinates": [ring, hole]}).json()["plot"]
    assert holed["area_ha"] == pytest.approx(big["area_ha"] - expected_ha(45.402, 0.001), abs=0.01)
