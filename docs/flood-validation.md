# Flood validation log

What was run and what came out. The decisions and pass criteria live in [architecture.md](architecture.md#verification). This file only records measurements.

Reference: Copernicus EMS **EMSR758 AOI03 (Pechea)**, Sept 2024 floods. It has two outlines:
- **PRODUCT v1** (16 Sept): riverine flood, 867 ha
- **MONIT01 v1** (18 Sept): flash flood, 427 ha

The files are in `data/raw/reference/`, which is gitignored. All scores are computed only inside the EMS area of interest.

## Facts about the pilot AOI
- **Sentinel-1 relative orbits** over `AOI`: 36, 58, 109, 131.
- **Passes in the 12–25 Sept 2024 window:**

  | Orbit | Direction | Date |
  |---|---|---|
  | 109 | descending | 14 Sept |
  | 131 | ascending | 15 Sept |
  | 36 | descending | 21 Sept |
  | 58 | ascending | 22 Sept |

  Most pixels see 3 of these passes; a strip where two orbits overlap sees all 4. The flash flood was visible on 14–15 Sept and had mostly drained by 21–22 Sept, so requiring several passes to agree throws away real flooding.
- **Compute per 13-day event export:**
  - v0.1: 898.7 EECU-seconds, about 0.25 EECU-h
  - v0.2: 3,754.2 EECU-seconds, about 1.04 EECU-h, so **4.2× v0.1**. That's mostly the 30 m focal median on every pass, plus VH doubling the bands.
  - Scaled the same way, a v0.2 10-year run could exceed the 150 EECU-h monthly quota. Measure one full year before the batch; a cheaper speckle filter or the 2019–2024 fallback may be needed.

## v0.1 (placeholder thresholds), 9 Nov 2026
Settings: VV < −18 dB, more than 3 dB below baseline, JRC occurrence ≤ 80 %, baseline 1 Jun–1 Sep 2023, no speckle filter.

| Flooded in | Predicted | Precision (PRODUCT) | Recall (PRODUCT) | Precision (MONIT01) | Recall (MONIT01) |
|---|---|---|---|---|---|
| ≥1 pass | 6,814 ha | 7.8 % | 61.0 % | 4.6 % | 72.9 % |
| ≥2 passes | 1,280 ha | 19.0 % | 28.1 % | 14.2 % | 42.5 % |
| ≥3 passes | 106 ha | 63.5 % | 7.8 % | 50.0 % | 12.5 % |

Flag rate at ≥1 pass is 61–73 % inside the EMS outlines and 11 % outside them. The signal is real but buried in false alarms. These cluster on farmland parcels, which fits harvested or bare fields compared with a summer baseline.

## Tuning runs
Dry window: 12–25 Sept 2023. Event window: 12–25 Sept 2024, scored against PRODUCT. All runs use `flood.py --evaluate`.

| Run | Change | Dry flagged ≥1 | Event recall ≥1 | Event precision ≥1 |
|---|---|---|---|---|
| 0 | v0.1 as is (summer-2023 baseline, no filter) | 11.85 % | 61.0 % | 7.8 % |
| A | same-season baseline 15 Aug–31 Oct 2022 | 10.52 % | 56.2 % | 7.6 % |
| B1 | speckle 30 m | 3.45 % | 55.2 % | 12.7 % |
| B2 | speckle 50 m | 2.16 % | 51.4 % | 14.6 % |
| B3 | speckle 30 m + same-season baseline | 2.67 % | 50.0 % | 12.5 % |
| B4 | speckle 50 m + same-season baseline | 1.59 % | 46.0 % | 14.3 % |
| C1 | speckle 30 m, drop −4 dB | 1.95 % | 51.8 % | 12.6 % |
| C2 | speckle 30 m, drop −5 dB | 0.95 % | 46.6 % | 12.6 % |
| C3 | speckle 30 m, water −20 dB | 0.70 % | 37.1 % | 33.8 % |
| C4 | speckle 50 m, drop −4 dB | 1.07 % | 47.8 % | 14.4 % |
| D1 | speckle 30 m, HAND ≤ 15 m | 2.11 % | 54.6 % | 18.9 % |
| D2 | speckle 30 m, HAND ≤ 10 m | 1.91 % | 54.6 % | 22.1 % |
| E1 | speckle 30 m, HAND ≤ 10 m, drop −4 dB | **1.11 %** | **51.2 %** | 21.9 % |
| E2 | speckle 30 m, HAND ≤ 10 m, drop −4.5 dB | **0.80 %** | **48.9 %** | 21.7 % |
| E3 | speckle 30 m, HAND ≤ 15 m, drop −4.5 dB | 0.88 % | 48.9 % | 18.5 % |
| E4 | speckle 30 m, HAND ≤ 10 m, water −19 dB | 0.95 % | 46.3 % | 32.1 % |

| F1 | E1 + VH < −22 dB | 1.08 % | 51.2 % | 21.9 % |
| **F2** | **E1 + VH < −24 dB → v0.2** | **0.92 %** | **50.7 %** | **22.1 %** |
| F3 | E1 + VH < −26 dB | 0.62 % | 48.2 % | 22.8 % |
| F4 | D2 + VH < −24 dB (drop −3 dB) | 1.60 % | 54.0 % | 22.4 % |

Unless stated, runs use the summer-2023 baseline, water −18 dB and drop −3 dB. HAND comes from MERIT Hydro (`hnd`, 90 m). There were 41 runs at about 30 s each. They are interactive computations, not export tasks, so they don't appear in the Tasks list. The quota dashboard read 6.64 % of 150 EECU-h on 10 Nov 2026 and didn't change after the last 9 runs. The cost per evaluate run is therefore not measured yet.

### Result, 10 Nov 2026: no configuration passes both criteria
- **Closest misses:** E1 fails the dry limit by 0.11 points, and E2 misses recall by 1.1 points. The criteria stay as written, so v0.2 is **not** locked in and the constants stay at v0.1.
- **Speckle is the main source of false alarms.** A 30 m focal median cuts the dry rate from 11.9 % to 3.5 % for a small loss of recall. The same-season baseline helps only a little and costs recall, so harvested fields are a smaller factor than first assumed.
- **HAND mostly removes event-window false alarms on high farmland.** It nearly triples precision but barely moves the dry rate, so the remaining dry false alarms lie low in the floodplain.
- **Precision is stuck around 20–30 %, not the ~50 % the 1 % limit implied.** Inside the EMS area, the event window flags far more non-reference land than the dry window does. Either storm-wet fields count as false alarms against EMS's outline, or the EMS outline (1:25,000, 576 m² minimum mapping unit) is incomplete.
- **Overfitting risk:** every choice was tuned on one event and one dry window. Any final setting needs a second event before it's trusted.
- **Possible next steps** (team decision):
  - add VH polarisation (better for water vs. bare soil)
  - a second validation event
  - a second dry window to see how much the 1 % varies year to year

### Result 2, 10 Nov 2026: F2 passes and becomes v0.2
- **Settings:** speckle 30 m, VV < −18 dB, drop −4 dB, VH < −24 dB, HAND ≤ 10 m. Dry rate 0.92 % (limit 1 %), recall 50.7 % (limit 50 %), precision 22 %.
- **Confirmed on the exported v0.2 COG** (local check, same numbers as `--evaluate`):
  - vs PRODUCT: precision 22.1 %, recall 50.7 %
  - vs MONIT01: precision 13.8 %, recall 64.5 %
  - flag rate: 51–65 % inside the outlines, 2.8–3.1 % outside (v0.1: 11 %)
  - The leftover false alarms are compact clusters on the north-western farmland, not scattered speckle.
- **VH helps only a little.** At −24 dB it removes about a sixth of the remaining dry false alarms for 0.5 points of recall.
- **The margin is thin.** It passes by 0.08 and 0.7 points, after 41 configurations tuned on one event and one dry window. Before the 10-year batch, check it on a second dry window and a second flood event. If either fails, report it; don't retune quietly.
