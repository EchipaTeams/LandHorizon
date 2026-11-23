"""One-off check: do GFM scenes with no advisory layer hold more flood than ordinary scenes?

Background: docs/flood-validation.md, "GFM passes without an advisory layer". The answer decides
whether such scenes count as "not seen" in a 10-year flood history.

  uv run --frozen python -u checks/advisory_layer/advisory_check.py [START END]   (default 2015-01-01 2026-01-01)

Results go next to this file in run_<START>_<END>/. Safe to stop and rerun: finished work is kept.
  scenes.json  every GFM scene over the AOI, with has_advisory true / false / null (couldn't tell)
  flood.csv    one row per scene read: how much of the AOI it sees, and the flood share of that

Design:
  - missing: every scene whose advisory_flags link returns 404
  - control: for each missing scene that sees the AOI, the nearest-in-date scene of the same
    frame (same time of day, within seconds) that has the layer

Rule, fixed on 13 Nov 2026 before the run:
  - a scene is "flood-heavy" when GFM marks flood on >= 1 % of the land it sees (and it sees >= 5 % of the AOI)
  - the missing scenes are flood-heavy as a group when their share of such scenes is at least
    double the control's AND at least 5 percentage points higher
"""
import csv
import json
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
import flood_common  # noqa: E402
import gfm_score  # noqa: E402

flood_common.SCALE = 20  # GFM's own pixel size; shares don't need the 10 m product grid
HEAVY, MIN_SEEN = 0.01, 0.05
KEYS = ("ensemble_flood_extent", "exclusion_mask", "advisory_flags")
START, END = (date.fromisoformat(a) for a in (sys.argv[1:3] if len(sys.argv) > 2 else ("2015-01-01", "2026-01-01")))
OUT = Path(__file__).parent / f"run_{START}_{END}"


def slim(assets):
    return {k: {"href": assets[k]["href"]} for k in KEYS if k in assets}


def probe(href):
    """HTTP status of a 1-byte read; None when the server doesn't give a clear answer."""
    req = urllib.request.Request(href, headers={"Range": "bytes=0-0"})
    for attempt in range(1, 5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 404
        except OSError:
            pass
        time.sleep(5 * attempt)
    return None


def has_advisory(scene):
    """True, False (404, also after asking the catalogue whether the file moved) or None (couldn't tell)."""
    href = scene["assets"].get("advisory_flags", {}).get("href")
    status = probe(href) if href else 404
    if status == 404:
        try:
            fresh = slim(gfm_score.get_json(f"{gfm_score.STAC}/{scene['id']}")["assets"])
        except OSError:
            return None
        new = fresh.get("advisory_flags", {}).get("href")
        if new and new != href:
            scene["assets"] = fresh
            status = probe(new)
    return None if status is None else status != 404


def list_scenes():
    scenes = []
    for year in range(START.year, END.year + 1):
        a, b = max(START, date(year, 1, 1)), min(END, date(year + 1, 1, 1))
        if a >= b:
            continue
        feats = gfm_score.items(a, b)
        scenes += [{"id": f["id"], "datetime": f["properties"]["datetime"], "assets": slim(f["assets"])} for f in feats]
        print(f"{year}: {len(feats)} scenes listed", flush=True)
    with ThreadPoolExecutor(4) as pool:
        for i, (s, has) in enumerate(zip(scenes, pool.map(has_advisory, scenes)), 1):
            s["has_advisory"] = has
            if i % 500 == 0:
                print(f"  advisory link checked for {i}/{len(scenes)}", flush=True)
    return scenes


def time_of_day(scene):
    t = scene["datetime"]
    return int(t[11:13]) * 3600 + int(t[14:16]) * 60 + int(t[17:19])


def day(scene):
    return date.fromisoformat(scene["datetime"][:10]).toordinal()


def pick_control(missing, with_layer):
    """Per missing scene: the nearest-in-date scene with the layer from the same frame.
    Frames are 25 s long and a track repeats to the second, so within 13 s means the same frame.
    (A neighbouring frame is no use: in June 2019 it saw none of the AOI.)"""
    used, control, gaps = set(), [], []
    for s in missing:
        cands = [c for c in with_layer if abs(time_of_day(c) - time_of_day(s)) <= 13 and c["id"] not in used]
        if cands:
            c = min(cands, key=lambda c: abs(day(c) - day(s)))
            used.add(c["id"])
            control.append(c)
            gaps.append(abs(day(c) - day(s)))
    if gaps:
        print(f"control: {len(control)} same-frame scenes, median {int(np.median(gaps))} days from their "
              f"missing-layer scene, at most {max(gaps)}", flush=True)
    return control


def rows(path):
    return list(csv.DictReader(path.open())) if path.exists() else []


def measure(group, scenes, path):
    done = {r["id"] for r in rows(path)}
    with path.open("a", newline="") as f:
        w = csv.writer(f)
        if not path.stat().st_size:
            w.writerow(["id", "datetime", "group", "seen_share", "flood_share"])
        for i, s in enumerate(scenes, 1):
            if s["id"] in done:
                continue
            try:
                a = gfm_score.read_asset(s, "ensemble_flood_extent")
                e = gfm_score.read_asset(s, "exclusion_mask")
            except Exception as err:  # one unreadable scene shouldn't stop a run of an hour
                print(f"  {s['id']}: unreadable ({str(err)[:70]})", flush=True)
                continue
            seen = np.isin(a, (0, 1)) & (e != 1)
            flood = (seen & (a == 1)).sum() / max(seen.sum(), 1)
            w.writerow([s["id"], s["datetime"], group, f"{seen.mean():.4f}", f"{flood:.6f}"])
            f.flush()
            print(f"{group} {i}/{len(scenes)} {s['datetime'][:16]}: sees {seen.mean():.0%}, flood {flood:.2%}", flush=True)


def judged(path, group):
    return [r for r in rows(path) if r["group"] == group and float(r["seen_share"]) >= MIN_SEEN]


def summary(path):
    share = {}
    for group in ("missing", "control"):
        x = np.array([float(r["flood_share"]) for r in judged(path, group)])
        if not len(x):
            print(f"{group}: no scene sees enough of the AOI to judge")
            return
        share[group] = (x >= HEAVY).mean()
        print(f"{group}: {len(x)} scenes judged, {int((x >= HEAVY).sum())} flood-heavy ({share[group]:.1%}), "
              f"median flood {np.median(x):.3%}, 90th percentile {np.percentile(x, 90):.3%}")
    heavy = share["missing"] >= 2 * share["control"] and share["missing"] - share["control"] >= 0.05
    print("RULE:", "missing-layer scenes ARE flood-heavy: look at the dates before choosing" if heavy
          else "missing-layer scenes are NOT flood-heavy")
    seeing = judged(path, "missing")
    print("\nmissing-layer scenes with the most flood:")
    for r in sorted(seeing, key=lambda r: -float(r["flood_share"]))[:15]:
        print(f"  {r['datetime'][:16]}  sees {float(r['seen_share']):.0%}  flood {float(r['flood_share']):.2%}")
    print("\nmissing-layer scenes that see the AOI, per year:", sorted(Counter(r["datetime"][:4] for r in seeing).items()))
    print("per month of the year:", sorted(Counter(r["datetime"][5:7] for r in seeing).items()))
    print("per time of day (the track):", sorted(Counter(r["datetime"][11:16] for r in seeing).items()))


def main():
    OUT.mkdir(exist_ok=True)
    scenes_file, flood_file = OUT / "scenes.json", OUT / "flood.csv"
    if scenes_file.exists():
        scenes = json.loads(scenes_file.read_text())
    else:
        scenes = list_scenes()
        scenes_file.write_text(json.dumps(scenes))
    missing = [s for s in scenes if s["has_advisory"] is False]
    unknown = sum(s["has_advisory"] is None for s in scenes)
    print(f"{len(scenes)} scenes: {len(missing)} without an advisory layer, {unknown} couldn't tell", flush=True)
    print("per year:", sorted(Counter(s["datetime"][:4] for s in missing).items()), flush=True)

    measure("missing", missing, flood_file)
    seeing = {r["id"] for r in judged(flood_file, "missing")}
    print(f"{len(seeing)} of the {len(missing)} missing-layer scenes see at least {MIN_SEEN:.0%} of the AOI", flush=True)
    control = pick_control([s for s in missing if s["id"] in seeing], [s for s in scenes if s["has_advisory"]])
    measure("control", control, flood_file)
    summary(flood_file)


if __name__ == "__main__":
    main()
