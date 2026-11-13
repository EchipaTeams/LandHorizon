# Flood validation log

What was run and what came out. The decisions and pass criteria live in [architecture.md](architecture.md#verification). This file only records measurements.

Reference: Copernicus EMS **EMSR758 AOI03 (Pechea)**, Sept 2024 floods. It has two outlines:
- **PRODUCT v1** (16 Sept): riverine flood, 867 ha. Mapped from **PAZ** (X-band radar, 15 Sept 2024 15:59 UTC, 3 m).
- **MONIT01 v1** (18 Sept): flash flood, 427 ha. Mapped from **COSMO-SkyMed Second Generation** (X-band radar, 17 Sept 2024 16:13 UTC, 3 m).

Neither is Sentinel-1 (the pre-event image is Sentinel-2, 24 Aug 2024), so the Galați scores are against independent references and aren't flattered. Sensors as printed on the EMS map PDFs inside the zips.

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
- **Precision is stuck around 20–30 %, not the ~50 % the 1 % limit implied.** Inside the EMS area, the event window flags far more non-reference land than the dry window does. Either storm-wet fields count as false alarms against EMS's outline, or the EMS outline (1:25,000, 576 m² minimum mapping unit) is incomplete. **Untested hypothesis:** neither explanation has been checked.
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

## Local pipeline (flood_local.py), 10 Nov 2026: not finished
The local prototype downloads scenes from the Copernicus Data Space and processes them with ESA SNAP.
- **What works:** SNAP processing of real scenes (2 of 34 cached), on the same 10 m grid as the Earth Engine export, with plausible values (VV median −9.4 dB, VH −17.5 dB on the first scene).
- **Why it stopped:** at about 2 MB/s a full event plus baseline is 6–10 hours of downloading. The run was paused when GFM (below) turned out to be the better option.
- **Status:** kept as a fallback; no scores yet.

## Copernicus GFM, 10 Nov 2026
GFM (CEMS Global Flood Monitoring) publishes a flood map for every Sentinel-1 pass, made by an ensemble of three algorithms, plus an exclusion mask and a reference water mask. `pipeline/gfm_score.py` reads it from the EODC STAC catalogue and scores it exactly like our own method:
- **Same grid:** UTM 35N, 10 m.
- **Same land definition:** not JRC permanent water above 80 %.
- **Same windows and references.**
- **Unknown pixels:** where GFM excludes a pixel or has no data, it doesn't count as a pass, so the pixel stays unknown.

GFM was **not tuned** on any of this data, so unlike v0.2, these are out-of-sample results.

### Galați: the pre-registered criteria
| | v0.2 (EE) | GFM | Criterion |
|---|---|---|---|
| Dry window 12–25 Sept 2023, land flagged ≥1 pass | 0.92 % | **0.09 %** | ≤ 1 % |
| Sept 2024 vs EMSR758 PRODUCT, recall ≥1 pass | 50.7 % | **58.0 %**, or **54.7 %** counting flood GFM can't see as missed | ≥ 50 % |
| … precision ≥1 pass | 22.1 % | **27.1 %** | |
| … precision ≥2 passes | 37.3 % | **72.4 %** | |

- **v0.2's 0.92 % is flattering:** it includes high ground that v0.2's HAND mask could never flag. GFM's 0.09 % counts only land GFM can see, so its real advantage is larger.
- **GFM's 58.0 % recall is measured on the 817 of 867 ha of EMS flood it can see.**

### What GFM can't see (exclusion mask, 14 Sept 2024 pass)
42 % of the AOI is excluded, almost all of it high ground:

| HAND | Share of AOI | Excluded |
|---|---|---|
| 0–2 m | 56 % | 13 % |
| 2–5 m | 11 % | 42 % |
| 5–10 m | 9 % | 62 % |
| 10–30 m | 16 % | 95 % |
| 30+ m | 9 % | 99.8 % |

- **The real flood is barely affected:** only 5.8 % of the EMS flood outline is excluded.
- **The eastern edge** (the Prut wetland around Lacul Manta, plus the Moldovan hills) is about 80 % excluded. That's how GFM avoids the seasonal-lake false alarms v0.2 had there.

### Second event: Botoșani, July 2018 (EMSR293 AOI01)
- **Reference:** a river flood in the Jijia/Prut basin. The outlines come from **COSMO-SkyMed** images of 2 and 3 July 2018, an independent radar satellite rather than Sentinel-1, so they don't flatter GFM.
- **Window:** 29 June–12 July 2018, chosen before looking at any result.
- **Area:** the EMS area of interest.
- **Passes:** 9 Sentinel-1 passes saw the area; in 2018 there were two Sentinel-1 satellites.

| Reference | EMS flood | Seen by GFM | Precision ≥1 | Recall ≥1 | Recall, unseen = missed |
|---|---|---|---|---|---|
| 2 July (PRODUCT) | 314 ha | 98 % | **96.7 %** | 67.6 % | **66.0 %** |
| 3 July (MONIT01) | 373 ha | 97 % | **99.3 %** | 58.5 % | **56.9 %** |

- **75 % of this area is excluded** (hilly plateau), yet 97–98 % of the flood lies in the part GFM sees.
- **Precision is far higher than at Galați.** A slow river flood stays in place and is seen by many passes. Why Galați's precision is only 27 % is **an untested hypothesis**: possibly storm-soaked fields around a short flash flood, or EMS mapping only part of the water. Neither has been checked.

### Result
GFM passes both pre-registered criteria with a wide margin and holds on a second, independent event. It beats v0.2 on every number. **Proposed as the flood source; needs the lead's review** (see architecture.md, *Flood method*).

*Added 11 Nov 2026:* the lead accepted it as the flood source for now. A third criterion added later, the spring window, fails: see *Review of PR #1* below.

### Advisory flags, and a spring false alarm (10 Nov 2026)
Building the 2024 history (`flood_gfm.py`) showed 17 % of the seen AOI flagged as flood at least once.
- **Where it came from:** most of it was **30 Apr and 1 May 2024**, seen by two different orbits. About 15,000 ha were flagged, 77 % of it less than 1 m above the river, mostly in the agricultural polder north of Lake Brateș (lat 45.51–45.62, lon 28.07–28.15).
- **No flood on record:** there's no recorded flood in Galați County then; the only 2024 events are September's (storm Boris).
- **Checked with Sentinel-2:** the NDWI image of 29 Apr 2024 (Copernicus Browser) shows **no water** in the polder, only large bare, freshly worked fields. Lake Brateș, the Danube and Lacul Manta all show water as expected. So this was a **false alarm on tilled soil**, a case GFM's user manual lists itself.
- **What separates it from a real flood:**

| Flagged as flood | 30 Apr 2024 (false) | 21 Sept 2024 (real) |
|---|---|---|
| Pixels | 1.49 M | 0.43 M |
| …with a GFM advisory flag | **40 %** | **0.7 %** |
| Likelihood (median) | 72 | 73 |

- **Fix:** pixels under an advisory flag now count as **not seen** for that pass, as GFM's manual advises ("use with caution").
- **Effect on validation:**
  - dry window 0.09 %, Galați recall 58.0 % / precision 27.1 %, Botoșani 96.7 % / 67.6 % (2 July) and 99.3 % / 58.5 % (3 July)
  - the advisory layer is missing for 2 of the 31 passes from 2018; those count as having no warnings
- **What's left:** most of the false alarm carried no advisory flag, so it remains. Removing it would need an optical cross-check (e.g. Sentinel-2 NDWI), which isn't built.
- **2024 history after the fix:**

| | Before | After |
|---|---|---|
| Seen area flagged at least once | 17.05 % | 13.34 % |
| 30 Apr | 7.63 % | 4.61 % |
| 1 May | 6.12 % | 5.79 % |
| 21 Sept (real flood) | 2.20 % | 2.19 % |
| Median passes per pixel | 92 | 69 |

  The pass count drops because passes under a warning (frost, snow, dry soil) no longer count.
- **API check on real plots** (`POST /evidence`, ~1 ha squares):
  - **Inside the Pechea EMS outline:** measured, 99 % flooded, date 21 Sept 2024.
  - **Polder plot (45.644 N, 28.131 E):** dates went from 11 Apr, 30 Apr, 1 May, 5 May to **11 Apr, 5 May**. Both remaining dates are unverified and probably the same tilled-soil effect.
  - **Plateau near the Tecuci road:** unknown, `flooded_fraction` null, HAND 13.7 m.
  - **Danube floodplain south of Galați:** measured, never flooded, 49 passes.

## Review of PR #1, 10 Nov 2026

### Spring no-flood window: fails
The lead asked for a spring window, because the September one can't catch false alarms on tilled fields. The criterion was committed before the run (`0a80f0c`): **20 Apr–5 May 2024, at most 1 % of land flagged in ≥1 pass.**

| | Land flagged ≥1 pass | ≥2 passes | ≥3 passes |
|---|---|---|---|
| Spring window (`gfm_score.py 2024-04-20 2024-05-06`) | **9.06 %** | 2.17 % | 0.32 % |
| Limit | 1 % | | |

- **Result: it fails.** Almost all of it comes from 30 Apr (7.55 % of what that pass saw) and 1 May (6.36 %).
- **Other passes in the window:** 23 Apr 0.33 %, 5 May 0.50 %.
- **Not adjusted:** the method stays as it is. How the report shows flood dates outside a verified event is to be decided with the lead.

### GFM passes without an advisory layer, per year (asked before any 10-year run)
The fix above treats pixels under a GFM advisory flag as not seen. The lead asked how many older passes don't have the advisory layer at all, because the fix can't apply there.

**Method:**
- **Scenes:** every GFM scene over the AOI per year, 2015–2025, from the EODC catalogue.
- **The check:** a request for each scene's `advisory_flags` file.
- **Moved files:** a missing file was looked up again in the catalogue, in case EODC had moved it.
- **"Couldn't tell":** the server didn't answer after retries.
- **Run on:** 10–11 Nov 2026 (one-off script, not in the repo).

| Year | Passes | No advisory layer | Share | Couldn't tell |
|---|---|---|---|---|
| 2015 | 388 | 6 | 1.5 % | 0 |
| 2016 | 683 | 9 | 1.3 % | 2 |
| 2017 | 1,081 | 13 | 1.2 % | 1 |
| 2018 | 1,086 | 45 | 4.1 % | 9 |
| 2019 | 1,094 | 62 | 5.7 % | 6 |
| 2020 | 1,136 | 34 | 3.0 % | 9 |
| 2021 | 1,131 | 24 | 2.1 % | 0 |
| 2022 | 616 | 0 | 0 % | 0 |
| 2023 | 516 | 0 | 0 % | 0 |
| 2024 | 630 | 0 | 0 % | 0 |
| 2025 | 741 | 5 | 0.7 % | 0 |
| **Total** | **9,102** | **198** | **2.2 %** | **27** |

**Missing doesn't mean empty:**
- **GFM publishes empty layers:** an advisory file where every pixel is 0 when nothing is flagged (2 of 8 July 2024 scenes checked).
- **So a missing file was never produced.** The catalogue still lists `advisory_flags` for these scenes; the link just returns 404.
- **The code is wrong here:** `gfm_score.passes()` treats a missing layer as "no warnings", but the honest reading is "**unknown** whether there were warnings".

**Pattern:**
- **The older archive (2015–2021):** 1–6 % of passes are missing the layer.
- **2022–2024:** none are missing.
- **2025:** a few.
- **Hint, not proven:** the gaps may come from GFM's reprocessing of its archive. The one scene compared in detail (2 July 2018, Botoșani) was processed separately from its sibling scene. It was also a real flood scene: 14,085 flooded pixels vs 112 on the sibling.

**Consequences:**
- **The 2024 history isn't affected,** since no 2024 pass lacks the layer.
- **A 10-year build would hit this in roughly 1 in 20–50 older passes.**
- **Treating them as "no warnings"** (current) lets any false alarms in them through.
- **Treating them as "not seen"** is safer, but also drops real observations. At Botoșani it would remove a real flood scene and lower the recall.
- **Which to use is a method decision for the lead.**
