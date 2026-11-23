"""Timing test for the share-of-passes count: read GFM layers coarsely (640 m) instead of at 20 m.

Takes 20 scenes advisory_check.py already read at 20 m (10 that saw ~59 % of the AOI, 10 that saw 0 %),
times the coarse read, and checks the coarse seen share against the 20 m one in flood.csv.

  uv run --frozen python -u checks/advisory_layer/timing_test.py
"""
import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
import flood_common  # noqa: E402
import gfm_score  # noqa: E402

flood_common.SCALE = 640
RUN = Path(__file__).parent / "run_2015-01-01_2026-01-01"

rows = list(csv.DictReader((RUN / "flood.csv").open()))
sample = [r for r in rows if float(r["seen_share"]) > 0.5][::10][:10] + [r for r in rows if float(r["seen_share"]) == 0][::10][:10]
scenes = {s["id"]: s for s in json.loads((RUN / "scenes.json").read_text())}

t_all = time.time()
for r in sample:
    s, t = scenes[r["id"]], time.time()
    a = gfm_score.read_asset(s, "ensemble_flood_extent")
    e = gfm_score.read_asset(s, "exclusion_mask")
    seen = (np.isin(a, (0, 1)) & (e != 1)).mean()
    print(f"{r['datetime'][:16]}  20 m seen {float(r['seen_share']):5.1%}  640 m seen {seen:5.1%}  {time.time() - t:4.1f} s",
          flush=True)
per = (time.time() - t_all) / len(sample)
print(f"\n{per:.1f} s per scene -> 8,543 scenes: {per * 8543 / 3600:.1f} h sequential, about {per * 8543 / 3600 / 4:.1f} h with 4 threads")
