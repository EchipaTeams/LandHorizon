"""Time POST /evidence on the 20 test plots, against the flood file FLOOD_PATH points to (default: flood_gfm.tif).

  FLOOD_PATH=data/processed/flood_gfm.tif uv run python checks/api_timing/api_timing.py

In-process (TestClient), two rounds; the second is warm. Used for F3 (docs/flood-validation.md): 2024 file
0.19-0.22 s median per plot, synthetic 1,202-band file 0.59 s median, 1.67 s for the slowest plot.
"""
import json
import os
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "api"))
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402

plots = json.loads((ROOT / "data" / "sample" / "plots.geojson").read_text())["features"]
client = TestClient(main.app)
print("flood file:", main.FLOOD_PATH, os.environ.get("FLOOD_PATH") and "(from FLOOD_PATH)" or "")
for rnd in (1, 2):
    times = []
    for p in plots:
        t = time.perf_counter()
        r = client.post("/evidence", json=p["geometry"])
        times.append(time.perf_counter() - t)
        assert r.status_code == 200, r.text
    print(f"round {rnd}: median {statistics.median(times) * 1000:.0f} ms, max {max(times) * 1000:.0f} ms, "
          f"total {sum(times):.1f} s for {len(plots)} plots")
