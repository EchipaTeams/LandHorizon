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
- **Compute:** one 13-day event export cost 898.7 EECU-seconds, about 0.25 EECU-h.

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
