# Decision 3: how the report shows flood dates that may be false alarms (F-3)

## Read
- [RECOMMENDATIONS.md](../RECOMMENDATIONS.md):
  - "F-3. A cropland caveat on flood dates";
  - the "Rejected" table under Flood.
- [architecture.md](../../architecture.md), "Open questions", "False flood dates outside real floods": the verified-event list and why it wasn't adopted.
- `api/main.py`, class `Flood`: the current flood section of the evidence contract.
- [flood/SYNTHESIS.md](../flood/SYNTHESIS.md): what the research found on cropland false alarms.

## Background
- **The weakness:** GFM flags freshly tilled, bare, smooth soil as water, and our spring test fails because of it (9.06 % against 1 %).
  - GFM's own documentation lists this weakness [F1-5, F1-20].
  - No service fix is expected before 2027 [F1-5, F1-20].
- **The consequence:** on floodplain farmland, `flood_dates` and `flooded_fraction` can include false alarms. The report can't present every date as a confirmed flood, and `architecture.md` already says so.
- **This decision is needed whatever happens with F-2 (decision 2).** Even if a per-algorithm rule helps, some false alarms will remain.

## Why it's the lead's call
- Option A adds a field to the evidence contract, which the frontend depends on, so it needs the lead's review.
- The wording users see is also a product decision.

## Options
| Option | What the report does | Cost | Weakness |
|---|---|---|---|
| A. Cropland caveat (recommended in RECOMMENDATIONS) | Every detection stays. The report adds, per plot, how much of the flagged area is arable land, plus one fixed sentence about false alarms on bare soil | 10–14 h. One static map (ESA WorldCover 2021, 10 m, CC BY 4.0). **New contract field** | The map is from 2021, and it can't tell a tilled field from a planted one. Our own design, never tested anywhere |
| B. Verified-event list | Only dates inside a list of confirmed floods (for 2024: 12–25 Sept, EMSR758) count as flood. The rest are shown as "unverified" | No new data | Already considered and **not adopted**: the list is kept by hand, it is region-wide rather than per plot, and a real flood without an EMS activation lands in "unverified" |
| C. Sentence only | The same fixed sentence on every flood section, with no number | Smallest; no contract change | Says the same thing to a plot on a hill and a plot in the polder |
| D. Remove cropland detections | n/a | n/a | **Rejected:** it deletes the floods users care about |

## What the research added
- **Nothing tested exists:** no published fix for tilled-field false alarms was found, and no published test of a cropland flag.
- **Also rejected:**

  | Option | Why |
  |---|---|
  | A stricter likelihood cut-off | No source evaluates one; our medians are 72 against 73 |
  | Requiring two or more passes | Still 2.17 %, and it costs flash-flood recall |
  | A HAND filter | 77 % of the false alarm is under 1 m above the river |
  | Corine Land Cover | 100 m, with a 25 ha minimum unit |

- **An optical check (Sentinel-2)** is the only independent test of a single detection. It is a new sensor, so it goes on the roadmap after the 22 Nov gate.

## Coordinator's recommendation
- **Option A**, decided by the 22 Nov gate.
- **Before computing, write down the two numbers to report:**
  - the share of the 30 Apr and 1 May 2024 false alarm that is cropland;
  - the share of the real EMSR758 flood that is cropland, i.e. real floods that would carry the caveat.
- **The spring test stays failed,** and the report says so. A caveat is not a detector.
- **The lead must also confirm** that a static land-cover map doesn't count as a "new sensor" under the gate rule.

## Questions for the lead
1. A, B, C, or another way?
2. If A: are you fine with a new field in the flood section of the contract? Its name and type can be fixed with the frontend person.
3. If A: does WorldCover count as a new sensor under the 22 Nov rule?
4. The fixed sentence: approve this draft, or write your own: "On arable land, radar flood detections include false alarms from bare, smooth soil, as GFM's own documentation says."

## Lead's choice
**Decided 18 Nov 2026: C′ now; A later only if the numbers justify it.**

- **C′ (now):** the fixed sentence is shown on the flood section only when `flood_dates` is not empty. No contract change; about 1 h of frontend work.
- **The sentence (lead's pick, "Version 1"):** "On farmland, radar flood detections can include false alarms. GFM's documentation names 'certain growing conditions and agricultural practices over cropland' as a cause."
  - Why the brief's draft was replaced: GFM's documentation never says "bare, smooth soil" [F1-1, F1-5]. Tilled soil is our own finding from the spring test.
- **Rule for A, fixed before any run:** build A by 29 Nov only if (a) − (b) ≥ 20 percentage points. Otherwise stay with C′ and log the negative result.
  - (a) = share of pixels flagged by GFM at least once in 20 Apr–5 May 2024 (same land as the spring test) that WorldCover 2021 labels cropland (class 40).
  - (b) = share of pixels flagged by GFM in 12–25 Sept 2024 inside the EMSR758 AOI03 PRODUCT v1 outline (correct detections) that WorldCover 2021 labels cropland.
  - Why 20: WorldCover 2021 reports about 77 % overall accuracy (the chat's own knowledge, not checked in the research docs), so a smaller gap could come from map error alone. A higher X would reject a number that already means something to users. This is a judgment, not a statistical test: one event each, and neighbouring pixels aren't independent.
- **WorldCover counts as "not a new sensor"** under the 22 Nov gate rule (lead confirmed). It is one static map, not a per-pass feed. Because it is partly derived from Sentinel-1, it must never be used to validate GFM.
- **Result (run 20 Nov 2026, lead's go): (a) 98.9 %, (b) 48.6 %, gap 50.4 pp ≥ 20 → build A by 29 Nov.** (ours)
  - (a): 17 057 ha flagged in 20 Apr–5 May 2024; 16 878 ha cropland, then grassland 0.8 %.
  - (b): 474 ha flagged inside the EMSR758 AOI03 outline; grassland 50.4 %, cropland 48.6 %.
  - WorldCover had data under every flagged pixel.
  - **What it means:** the spring false alarm is almost all cropland, and the real flood is about half cropland. The gap is a contrast across the region, not a per-plot detector. A cropland plot in a real flood still gets a high cropland share, so the caveat will also show on about half of real flood detections. The fixed sentence must keep saying "can include", never "is".
  - Script: `checks/cropland_share/cropland_share.py`. Output and cached GFM counts are in `checks/cropland_share/run/` (not to be pushed). The EMSR758 zip was downloaded from the Copernicus EMS rapid-mapping site to `data/raw/reference/` (gitignored).
- **The check was first deferred; the lead gave the go on 20 Nov.** Original plan: `checks/cropland_share/`, about 2–3 h of work plus machine time for two `gfm_score.py --write` runs (not measured). WorldCover is read as an AOI window from ESA's public COGs; no new dependency. Needs `EMSR758_AOI03_DEL_PRODUCT_v1.zip` in `data/raw/reference/` (not on the lead's machine as of 18 Nov). The results folder must not be pushed.
- **If A is built later:** the new field is the cropland share of the **flagged** area, not of the whole plot. It is `None` (never 0) when there are no flagged pixels, when `status` is unknown, or when WorldCover has no data under the plot. Name and type to be agreed with the frontend person.
- **Unchanged:** the spring test stays failed, and the report says so. A caveat is not a detector.
- **Note for the coordinator:** option B is not contract-free either. `architecture.md` says that under B, `flooded_fraction` counts verified passes only.
