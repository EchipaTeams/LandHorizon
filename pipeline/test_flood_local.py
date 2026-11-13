import numpy as np

from flood_local import flood_counts

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
