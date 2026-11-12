"""The 20 test plots of milestone 3 (data/sample/plots.geojson) against the real layers.

Skipped unless data/processed/ holds hand.tif and a flood_gfm.tif that covers all of 2024
(pipeline/hand.py, then pipeline/flood_gfm.py 2024-01-01 2025-01-01).

  uv run pytest api/test_plots.py
  uv run python api/test_plots.py      # the results table, for the data test

Each plot's `expect` says what the answer should be:
  flood_sept_2024     measured, with a flood date inside 12-25 Sept 2024 (storm Boris)
  never_flooded       measured, no flood date
  unknown             GFM can't see it, so "unknown", never "not flooded"
  spring_false_alarm  known problem: GFM flags tilled fields on 30 Apr / 1 May 2024 (docs/flood-validation.md).
                      Marked as an expected failure; it starts passing when the false alarm is fixed.
  probe               no expectation: there to look at (edge of the visible area, wetland, water's edge)
"""
import json
from datetime import date
from pathlib import Path

import pytest
import rasterio
from fastapi.testclient import TestClient

import main

PLOTS = json.loads((Path(__file__).resolve().parents[1] / "data" / "sample" / "plots.geojson").read_text())["features"]
EVENT = (date(2024, 9, 12), date(2024, 9, 25))    # the Sept 2024 flood (EMSR758)
SPRING = (date(2024, 4, 20), date(2024, 5, 5))    # the spring no-flood window that GFM fails
client = TestClient(main.app)


def layers_ready():
    if not (main.HAND_PATH.exists() and main.FLOOD_PATH.exists()):
        return False
    with rasterio.open(main.FLOOD_PATH) as src:
        tags = src.tags()
    return tags.get("period_start", "9") <= "2024-01-01" and tags.get("period_end", "0") >= "2025-01-01"


pytestmark = pytest.mark.skipif(not layers_ready(), reason="needs hand.tif and a flood_gfm.tif covering 2024")


def evidence(plot):
    r = client.post("/evidence", json=plot["geometry"])
    assert r.status_code == 200, r.text
    return r.json()


def dates_in(flood, window):
    return [d for d in flood["flood_dates"] if window[0] <= date.fromisoformat(d) <= window[1]]


def by_name(expect=None):
    return [pytest.param(p, id=p["properties"]["name"]) for p in PLOTS
            if expect is None or p["properties"]["expect"] == expect]


@pytest.mark.parametrize("plot", by_name())
def test_unknown_rule(plot):
    """Whatever the plot: missing data comes out as unknown with no value, never as a low one."""
    e = evidence(plot)
    flood, terrain = e["flood"], e["terrain"]
    if flood["observed_fraction"] < main.MIN_OBSERVED_FRACTION:
        assert (flood["status"], flood["flooded_fraction"], flood["flood_dates"]) == ("unknown", None, [])
    else:
        assert flood["status"] == "measured" and flood["flooded_fraction"] is not None and flood["n_passes"] > 0
    assert (terrain["status"] == "unknown") == (terrain["hand_m"] is None)


@pytest.mark.parametrize("plot", by_name("flood_sept_2024"))
def test_sept_2024_flood_is_found(plot):
    flood = evidence(plot)["flood"]
    assert flood["status"] == "measured" and dates_in(flood, EVENT)


@pytest.mark.parametrize("plot", by_name("never_flooded"))
def test_dry_plot_has_no_flood_date(plot):
    flood = evidence(plot)["flood"]
    assert flood["status"] == "measured" and flood["flood_dates"] == []


@pytest.mark.parametrize("plot", by_name("unknown"))
def test_unseen_plot_is_unknown(plot):
    assert evidence(plot)["flood"]["status"] == "unknown"


@pytest.mark.xfail(strict=True, reason="known GFM false alarm on tilled fields, 30 Apr / 1 May 2024")
@pytest.mark.parametrize("plot", by_name("spring_false_alarm"))
def test_no_flood_date_in_the_spring_no_flood_window(plot):
    assert not dates_in(evidence(plot)["flood"], SPRING)


def table():
    """One line per plot: what the API answers. Run this file as a script to print it."""
    print(f"{'plot':20s} {'ha':>5s}  {'expect':18s} {'flood':8s} {'seen':>5s} {'passes':>6s} {'flooded':>7s} "
          f"{'HAND m':>6s}  flood dates")
    for p in PLOTS:
        props, e = p["properties"], evidence(p)
        f, t = e["flood"], e["terrain"]
        flooded = "-" if f["flooded_fraction"] is None else f"{f['flooded_fraction']:.0%}"
        hand = "-" if t["hand_m"] is None else f"{t['hand_m']:.1f}"
        print(f"{props['name']:20s} {props['area_ha']:5.1f}  {props['expect']:18s} {f['status']:8s} "
              f"{f['observed_fraction']:5.0%} {f['n_passes']:6d} {flooded:>7s} {hand:>6s}  "
              f"{', '.join(d[5:] for d in f['flood_dates'])}")


if __name__ == "__main__":
    table() if layers_ready() else print("needs hand.tif and a flood_gfm.tif covering 2024; see the docstring")
