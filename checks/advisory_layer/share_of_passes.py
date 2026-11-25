"""One-off check: what share of the AOI's GFM passes does decision 1a option B remove?

Option B: a scene with no advisory layer counts as not seen. advisory_check.py found which scenes those
are (run_.../scenes.json) but never counted the scenes WITH the layer that see the AOI, so B's cost had
no denominator. Catalogue footprints can't give it (they are the whole 300 km Equi7 tile), so every
scene's layers are read, coarsely: 640 m cells. timing_check.py showed 640 m agrees with 20 m on 20
scenes (58.9 % vs 58.5 % seen, 0 % vs 0 %).

  uv run --frozen python -u checks/advisory_layer/share_of_passes.py

Safe to stop and rerun: finished scenes are kept in run_.../seen.csv.
Period: 2015 to 13 Apr 2025 (the last GFM v3 scene, decision 1b).
Headline, fixed on 17 Nov 2026 before the run: the share of AOI pass coverage (sum of each scene's seen
share of the AOI) that belongs to missing-layer scenes, over the whole period. If it is >= 10 %, the lead
builds a stand-in warning layer (route 2); below, that stays a roadmap item. Per-pixel and per-period
numbers are context.
"""
import csv
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
import flood_common  # noqa: E402
import gfm_score  # noqa: E402

flood_common.SCALE = 640
RUN = Path(__file__).parent / "run_2015-01-01_2026-01-01"
OUT = RUN / "seen.csv"
END = date(2025, 4, 14)  # exclusive: last v3 scene is 13 Apr 2025
THRESHOLD = 0.10


def seen_mask(s):
    try:
        a = gfm_score.read_asset(s, "ensemble_flood_extent")
        e = gfm_score.read_asset(s, "exclusion_mask")
    except Exception as err:  # one unreadable scene shouldn't stop the run
        print(f"  {s['id']}: unreadable ({str(err)[:70]})", flush=True)
        return None
    return np.isin(a, (0, 1)) & (e != 1)


def main():
    scenes = [s for s in json.loads((RUN / "scenes.json").read_text()) if s["datetime"] < END.isoformat()]
    done = {r["id"] for r in csv.DictReader(OUT.open())} if OUT.exists() else set()
    todo = [s for s in scenes if s["id"] not in done]
    print(f"{len(scenes)} scenes to {END}: {len(done)} done, {len(todo)} to read", flush=True)
    with OUT.open("a", newline="") as f, ThreadPoolExecutor(4) as pool:
        w = csv.writer(f)
        if not done:
            w.writerow(["id", "datetime", "missing", "seen_share", "mask"])
        for i, (s, m) in enumerate(zip(todo, pool.map(seen_mask, todo)), 1):
            if m is not None:
                w.writerow([s["id"], s["datetime"], int(s["has_advisory"] is False), f"{m.mean():.4f}",
                            np.packbits(m).tobytes().hex()])
                f.flush()
            if i % 250 == 0:
                print(f"  {i}/{len(todo)} read", flush=True)

    rows = list(csv.DictReader(OUT.open()))
    shape = (flood_common.grid()[2], flood_common.grid()[1])
    total, lost = np.zeros(shape, "uint32"), np.zeros(shape, "uint32")
    for r in rows:
        m = np.unpackbits(np.frombuffer(bytes.fromhex(r["mask"]), "uint8"))[:shape[0] * shape[1]].reshape(shape)
        total += m
        if r["missing"] == "1":
            lost += m
    print(f"\n{len(rows)} of {len(scenes)} scenes read; "
          f"{sum(r['missing'] == '1' for r in rows)} of them missing the layer, "
          f"{sum(float(r['seen_share']) >= 0.05 for r in rows)} see >= 5 % of the AOI")

    def share(part):
        w = sum(float(r["seen_share"]) for r in part)
        return sum(float(r["seen_share"]) for r in part if r["missing"] == "1") / w if w else float("nan")

    h = share(rows)
    print(f"HEADLINE: share of AOI pass coverage removed by option B: {h:.2%} "
          f"-> {'AT OR ABOVE' if h >= THRESHOLD else 'below'} the {THRESHOLD:.0%} threshold")

    px = lost[total > 0] / total[total > 0]
    hit = lost > 0
    print(f"\nper pixel (cells seen at least once): median {np.median(px):.1%}, 90th pct {np.percentile(px, 90):.1%}, "
          f"max {px.max():.1%} of passes removed")
    print(f"  cells hit at all ({hit.sum()} of {(total > 0).sum()}): median {np.median(lost[hit] / total[hit]):.1%}, "
          f"passes per cell there: median {int(np.median(total[hit]))}")
    for label, a, b in (("Sep 2018 - Jan 2020 (worst stretch)", "2018-09", "2020-02"),
                        ("2015-2021", "2015", "2022"), ("2022 - 13 Apr 2025", "2022", "2025-04-14")):
        print(f"  {label}: share removed {share([r for r in rows if a <= r['datetime'] < b]):.1%}")


if __name__ == "__main__":
    main()
