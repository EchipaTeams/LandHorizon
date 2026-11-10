import numpy as np

from flood_local import flood_counts, scores

NAN = np.nan


def px(*values):
    """A 1x4 test image."""
    return np.array([values], dtype="float32")


def test_flood_counts():
    # Pixels: 0 = flood (dark, dropped), 1 = permanent water, 2 = dry field, 3 = no data in this pass.
    base = px(-8, -25, -8, -8)
    vv = px(-22, -25, -9, NAN)
    vh = px(-28, -30, -15, NAN)
    can_flood = np.array([[True, False, True, True]])
    event = {109: [("2024-09-14", vv, vh)], 58: [("2024-09-22", vv, vh)]}

    n_flooded, n_passes = flood_counts(event, {109: base}, can_flood,
                                       water_db=-18, drop_db=-4, speckle_m=0, vh_db=-24)
    # Orbit 58 has no baseline, so only orbit 109 counts.
    assert n_flooded.tolist() == [[1, 0, 0, 0]]
    assert n_passes.tolist() == [[1, 1, 1, 0]]  # no data -> 0 passes -> "unknown" downstream, never "dry"

    # VH condition: a VV-dark pixel that is bright in VH (wet bare soil) is not flood.
    n_flooded, _ = flood_counts({109: [("d", vv, px(-15, -30, -15, NAN))]}, {109: base}, can_flood,
                                water_db=-18, drop_db=-4, speckle_m=0, vh_db=-24)
    assert n_flooded[0, 0] == 0


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


def test_prefetched_keeps_order_and_bounds_downloads(monkeypatch):
    import random
    import threading
    import time

    import flood_local

    active, peak, lock = 0, 0, threading.Lock()

    def fake_download(scene):
        nonlocal active, peak
        with lock:
            active += 1
            peak = max(peak, active)
        time.sleep(random.uniform(0, 0.02))  # downloads finish out of order
        with lock:
            active -= 1
        return f"{scene}.zip"

    monkeypatch.setattr(flood_local, "download", fake_download)
    scenes = list(range(20))
    got = []
    for scene, path in flood_local.prefetched(scenes, workers=2, ahead=3):
        time.sleep(random.uniform(0, 0.01))  # "SNAP"
        got.append((scene, path))
    assert got == [(s, f"{s}.zip") for s in scenes]  # in order, none lost, no deadlock
    assert peak <= 2                                  # never more than `workers` at once


def test_water_masks():
    from flood_local import water_masks

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
