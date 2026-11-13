import numpy as np

import flood_common
from flood_common import scores, water_masks


def px(*values):
    """A 1x4 test image."""
    return np.array([values], dtype="float32")


def test_scores():
    n_flooded = np.array([[2, 1, 0, 0, 0]], dtype="uint16")
    n_passes = np.array([[3, 3, 3, 3, 0]], dtype="uint16")
    permanent = np.array([[False, False, False, True, False]])
    ref = np.array([[True, False, True, False, True]])
    ref_aoi = np.ones((1, 5), bool)

    s = scores(n_flooded, n_passes, permanent, ref, ref_aoi)
    assert s["share"][1] == 2 / 3  # land = 3 pixels with passes, not permanent water
    assert s["ref_px"] == 2        # the no-data pixel doesn't count as missed flood
    assert s[1]["precision"] == 0.5 and s[1]["recall"] == 0.5
    assert s[2]["precision"] == 1.0 and s[2]["recall"] == 0.5


def test_water_masks():
    occurrence = px(0, 60, 90, 0)  # field, seasonal lake (like Lacul Manta), river, field
    hand = px(2, 0, 0, 30)          # the last field sits 30 m above drainage

    permanent, can_flood = water_masks(occurrence, hand, permanent_water=80, hand_max_m=10)
    assert permanent.tolist() == [[False, False, True, False]]   # at 80 the seasonal lake is land
    assert can_flood.tolist() == [[True, True, False, False]]

    permanent, can_flood = water_masks(occurrence, hand, permanent_water=50, hand_max_m=10)
    assert permanent.tolist() == [[False, True, True, False]]    # at 50 it is water
    assert can_flood.tolist() == [[True, False, False, False]]

    _, can_flood = water_masks(occurrence, None, permanent_water=80, hand_max_m=None)  # no HAND mask
    assert can_flood.tolist() == [[True, True, False, True]]


def test_set_area_moves_the_grid(monkeypatch):
    # gfm_score.py --area-from-reference relies on this: grid() must follow set_area().
    monkeypatch.setattr(flood_common, "AOI", flood_common.AOI)  # restored after the test
    galati = flood_common.grid()
    flood_common.set_area([26.5, 47.5, 27.0, 47.8])  # Botoșani
    assert flood_common.grid() != galati
    assert flood_common.aoi_wkt().startswith("POLYGON((26.5 47.5,27.0 47.5,")
