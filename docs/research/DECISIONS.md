# Lead's decisions

A running log of what the lead chose while going through the eight open questions in [RECOMMENDATIONS.md](RECOMMENDATIONS.md), and what is left to do. Started 2026-11-13.

**Status of this file:** a working log, not the record of decisions. A choice becomes a project decision when it is written into [architecture.md](../architecture.md).

**Open decisions are being worked in separate chats,** one per decision, from the briefs in [briefs/](briefs/README.md). Each chat writes the lead's choice into its own brief, and the coordinator merges those choices here.

## At a glance
| # | Question | Status | Choice |
|---|---|---|---|
| 1a | Flood: passes with no advisory layer | **Decided 17 Nov** | B: no advisory layer = not seen. Recover scenes if GFM regenerates the files; a weather-based stand-in only if B removed ≥ 10 % of AOI passes. It removes 8.15 %, so the stand-in is a roadmap item |
| 1b | Flood: history spans GFM v3 and v4 | **Decided 13 Nov** | End the history at the last v3 scene (13 Apr 2025) |
| 2 | Flood: held-out windows and limits for the per-algorithm test | **Decided 18 Nov; stop rule 23 Nov** (both before any run) | Springs: every 20 Apr–5 May 2018–2023 that passes the dryness check, ≤ 1 % each. Botoșani recall ≤ 10 points below the ensemble on each outline, on passes seen under 1a-B. Sept 2023 stays ≤ 1 %. Any failure = not adopted, no retune. Exploration stop rule: continue only if one algorithm flags < half the ensemble's polder area on both 30 Apr and 1 May 2024 while keeping ≥ 80 % inside EMSR758. Record: [briefs/2-held-out-test.md](briefs/2-held-out-test.md) |
| 3 | Flood: cropland caveat as a contract field | **Decided 18 Nov; check run 20 Nov** | C′ (one fixed sentence when `flood_dates` is not empty) now. The check gave a 50.4-point gap (≥ 20), so **build A (cropland share field) by 29 Nov**. **Built 26 Nov (G3, PR #20)**: see "Built" under section 3 |
| 4 | Flood: send the emails to the GFM helpdesk and ANAR | **Decided 23 Nov; not sent yet** | Send both, from the lead's personal account: English to the GFM helpdesk (3 questions, including regenerating the missing `advisory_flags` files), Romanian to ANAR with INHGA in copy. Drafts: [briefs/4-emails.md](briefs/4-emails.md) |
| 5 | Ground: plot rule, minimum cells, classes or none | **Decided 23 Nov** (after the cell counts were known, so not pre-registered) | Keep the built rule (cells whose centre is inside the plot, median, no classes). Add a share rule: `measured` only when `n_cells` / max(1, round(`area_ha`)) ≥ 0.5, else `unknown`. No contract shape change. Record: [briefs/5-ground-plot-rule.md](briefs/5-ground-plot-rule.md) |
| 6 | Heat and drought: roadmap only | **Decided 23 Nov** | A: roadmap only, nothing built before the freeze. H-1 (ERA5-Land hot-day count as regional climate context) is the first roadmap item. Running the H-1 code later would be a new decision. Record: [briefs/6-heat-drought.md](briefs/6-heat-drought.md) |
| 7 | Does a validation-only dataset need an open licence | **Decided 23 Nov** | A, as a general rule: a validation-only reference is usable if its terms are read and allow evaluation and publishing the numbers, it is never shipped or committed, it is cited, and the report names it. Unclear terms = not usable. Record: [briefs/7-validation-licence.md](briefs/7-validation-licence.md) |
| 8 | Run the research follow-up round | Not discussed yet | |

## To do after this review
1. **Message the GFM helpdesk** (through the EFAS or GloFAS contact form; the GFM news items point there). Two questions:
   - Will the Sentinel-1 archive (2015 to April 2025) be reprocessed with GFM v4, and when?
   - Why do some scenes have no `advisory_flags` file? The catalogue lists the file but the link returns 404, on 224 of 9,102 scenes over our area (2.5 %), all in 2015–2021 and 2025. Over our AOI they follow one track: at 16:00 UTC, every 12 days, nearly without a break from September 2018 to January 2020.
   - Can you regenerate the missing advisory files? (Decision 1a, route 1: under B, a regenerated file brings its scene back on the next build, with no code change.)
2. **Write decision 1b into `architecture.md`** ("Period of the flood history"), in the same commit as the code that applies it.
3. **Flood pipeline, from decision 1b:** record `processing:version` and `flood_members` from the catalogue for each pass, and stop the history at a change of major version instead of at a hard-coded date.
4. **Flood pipeline, from decision 1a:** in `gfm_score.passes()`, a scene without an advisory layer counts as not seen.
5. **Re-score every flood criterion under 1a's option B, Botoșani included, before fixing decision 2's numbers.** Log before and after in `flood-validation.md`.
6. **Change "198" to 224** in `flood-validation.md` and `architecture.md`, in the same commit as item 4.
7. **Roadmap line, from decision 1a:** "Missing GFM warning layers are treated as unknown; a weather-based stand-in is future work."
8. **Frontend, from decision 3 (about 1 h):** when `flood_dates` is not empty, show: "On farmland, radar flood detections can include false alarms. GFM's documentation names 'certain growing conditions and agricultural practices over cropland' as a cause."
9. **Decision 3, build option A by 29 Nov** (the cropland check passed on 20 Nov). **Done in G3 on 26 Nov, PR #20, reviewed by the lead (details under section 3, "Built").**
   - agree the field's name and type with the frontend person: the cropland share of the *flagged* area, `None` (never 0) when nothing is flagged, `status` is unknown, or WorldCover has no data;
   - it changes the evidence contract, so say so explicitly in the PR and write it into `architecture.md` in the same commit.
10. **Gitignore the check results before anyone commits `checks/`.** Neither `checks/advisory_layer/run_*/` nor `checks/cropland_share/run/` is ignored today (checked 20 Nov); `checks/` is untracked as a whole. One line in `.gitignore` covers both, for example `checks/*/run*/`.
11. **Ground, from decision 5 (separate PR):** the share rule in code, a test that a low share gives `unknown` with `velocity_mm_yr` `null`, and the `architecture.md` update in the same commit. It closes the open question "Ground on a single cell". Fixed report sentences: "Based on N EGMS cells (100 m) inside the plot." / "No value means no reliable measurement, not stable ground." / "Not a geotechnical or damage assessment."
12. **Flood, from decision 2:** the lead runs `checks/per_algorithm/explore.py` (results in `checks/per_algorithm/run/`, not to be pushed) and applies the stop rule. If it says continue: write the rule and the held-out criteria into `architecture.md` **before** the held-out run, and do item 5 (re-score under 1a-B) first, because the Botoșani limit is relative to that recall.

## Offered, not decided
- **Run the spring test on v4.** The 20 Apr–5 May 2025 window is entirely v4, and `gfm_score.py` runs it with one command. It would show whether the tillage false alarm repeats in v4. It can't validate v4: no v4 flood with a reference outline is known.
- **Credit JRC Global Surface Water in the README.** The permanent-water mask uses it (`pipeline/flood_common.py`); the README credits Sentinel and GFM only.
- **JRC flood hazard maps licence** (ODbL in the README, CC BY 4.0 in `copyright.txt`). No action: the project doesn't use these maps. It matters only if they are adopted later.

---

## 3. How the report shows flood dates that may be false alarms (decided 18 Nov 2026)

**Choice: C′ now; A later only if the numbers justify it.** Full record: [briefs/3-cropland-caveat.md](briefs/3-cropland-caveat.md), "Lead's choice".

**C′ (now)**
- One fixed sentence on the flood section, shown only when `flood_dates` is not empty. No contract change.
- **The sentence ("Version 1"):** "On farmland, radar flood detections can include false alarms. GFM's documentation names 'certain growing conditions and agricultural practices over cropland' as a cause."
- **Why the brief's draft was replaced:** GFM's documentation never says "bare, smooth soil" [F1-1, F1-5]. Tilled soil is our own finding from the spring test.

**Rule for A, fixed before any run:** build A by 29 Nov only if (a) − (b) ≥ 20 percentage points. Otherwise stay with C′ and log the negative result.
- (a): the share of pixels GFM flagged at least once in 20 Apr–5 May 2024 (the spring-test land) that WorldCover 2021 labels cropland (class 40).
- (b): the share of pixels GFM flagged in 12–25 Sept 2024 inside the EMSR758 AOI03 outline (correct detections) that WorldCover 2021 labels cropland.
- **Why 20 points:** WorldCover 2021's overall accuracy is about 77 %, so a smaller gap could be map error alone. That figure comes from the chat's own knowledge and isn't checked in the research docs. The threshold is a judgment, not a statistical test: one event each, and neighbouring pixels aren't independent.

**Result (run 20 Nov, on the lead's go): (a) 98.9 %, (b) 48.6 %, a gap of 50.4 points, so build A by 29 Nov.** (ours)

| | Flagged area | Cropland | Next class |
|---|---|---|---|
| (a) Spring false alarm, 20 Apr–5 May 2024 | 17,057 ha | 98.9 % | grassland 0.8 % |
| (b) Real flood inside EMSR758 AOI03, 12–25 Sept 2024 | 474 ha | 48.6 % | grassland 50.4 % |

- WorldCover had data under every flagged pixel.
- **What it means, and what it doesn't:**
  - The spring false alarm is almost all cropland; the real flood is about half cropland.
  - So a **low** cropland share is informative: such a detection is unlike the false alarm. A **high** share is ambiguous: a cropland plot inside a real flood scores high too, so about half of real flood detections will carry the caveat.
  - The gap is a contrast across the region, not a per-plot detector. The sentence must keep saying "can include", never "is".
  - (b) rests on one event and 474 ha.
- **Files:** `checks/cropland_share/cropland_share.py`, output in `checks/cropland_share/run/` (not to be pushed). The EMSR758 zip is in `data/raw/reference/` (gitignored).
- **Note:** the result report came through the ground tab's terminal (t1x), signed as the cropland chat. The brief and `output.txt` agree with it.

**Other points settled**
- **WorldCover is not a new sensor** under the 22 Nov gate rule: it is one static map, not a per-pass feed. It is partly derived from Sentinel-1, so it must never be used to validate GFM.
- **If A is built:** the field is the cropland share of the *flagged* area, not of the whole plot. It is `None` (never 0) when nothing is flagged, when `status` is unknown, or when WorldCover has no data under the plot. Name and type to be agreed with the frontend person.
- **The check** goes in `checks/cropland_share/`, reading WorldCover from ESA's public COGs with no new dependency. Its results folder must not be pushed.
- **Unchanged:** the spring test stays failed, and the report says so. A caveat is not a detector.
- **Note:** option B (verified-event list) wasn't contract-free either. `architecture.md` says that under B, `flooded_fraction` counts verified passes only.

**Built (26 Nov 2026, G3, Miriam with Claude; PR #20, reviewed by the lead on 26 Nov).** The lead allowed G3 to edit the flood code (`flood()` and the `Flood` model in `api/main.py`); everything else in the flood lane is untouched.
- **Field:** `flood.cropland_share: list[float | None]`, one value per flood date (name from L4, 25 Nov; L4's `float | None` changed by the lead in the PR #20 review, see below). **This is a contract change**: the website team (W3) must regenerate the types and mock after the merge. It is also in `MOCK` (`[0.6]`, for its one flood date), and the website's mock is generated from it.
- **Meaning:** for each date in `flood_dates`, same order: of the plot's observed pixels seen wet that day (any pass of the day), the share that WorldCover 2021 maps as class 40, with WorldCover no-data pixels left out of both sides. An entry is `null`, never 0, when WorldCover has no data on that day's wet pixels; the list is empty when `flood_dates` is (nothing flagged, or `flood.status` `unknown`). A real `0.0` (wet, all trees or grass) stays 0.0.
- **Changed to per date (26 Nov, PR #20 review, lead's decision):** the first version gave one share over every pixel ever flagged. The check compared single events, and pooled dates would drift, as the spring false alarm recurs each year, towards "how much of the plot is farmland" on a 10-year history. Per date it stays what the check measured. Changed before W3 used the field, so the website builds on the final shape. The real-plot numbers below are from the pooled version and must be re-run (F6).
- **What changes in flood, and what doesn't:** no existing flood field changes, and `status`, `observed_fraction`, `flood_dates`, `n_passes` and `flooded_fraction` come out the same as before. The change in `flood()` is a read of the land cover (`land_cover()`), one `cropland_share()` per flood date and the new field in both returns. **One new failure mode:** the API reads a fourth COG, `worldcover.tif`. If it is missing, `/evidence` answers 503 naming it, for every plot, including plots whose flood is `unknown`. It also answers 503 if `worldcover.tif` is not exactly on the grid of `flood_gfm.tif` (CRS, transform and shape are compared), so a rebuilt flood grid can't give a wrong share. **For the flood lane (F3):** keep the same grid, or tell G3 so `worldcover.tif` is rebuilt.
- **Pipeline:** new `pipeline/worldcover.py` reads the AOI window of the WorldCover 2021 v200 tile N45E027 over HTTP and writes `data/processed/worldcover.tif` (uint8 COG, nearest neighbour, 0 = no data) on `flood_common.grid()`. It uses `flood_common.grid()` and `to_grid()` and changes neither. Real run: 5910 x 5620 px, 0 % no data, 68.2 % cropland of the pixels. The file is not committed; it goes on the team Drive (about 2 MB).
- **Tests:** `pipeline/test_worldcover.py` and, in `api/test_main.py`: all wet on cropland, half, trees only (a real 0.0), WorldCover no data, a second date with its own entry, two dates on different land (each counts only its own pixels; two passes on one day are joined), nothing flagged and flood unknown (empty list), file missing (503), file off the flood grid or smaller than it (503). `api/test_plots.py` checks one share per date and prints each date with its share; it now also needs `worldcover.tif` to run.
- **Real plots, pooled version, superseded (26 Nov, `uv run python api/test_plots.py`, with `flood_gfm.tif` built 10 Nov for 2024; `worldcover.tif` is on exactly its grid; 70 passed, 4 xfailed, the xfails being the known spring false alarm):**

  | Plots | `cropland_share` |
  |---|---|
  | Spring false alarm (`polder-1/2/3`, `spring-west-1`) | 100 % on all four |
  | Real Sept 2024 flood: `flood-pechea-1`, `-2`, `-3`, `flood-north-1` | 18 %, 27 %, 100 %, 100 % |
  | `flood-and-spring-1` (probe) | 100 % |
  | Not flagged (`floodplain-dry-*`, `water-edge-1`, `manta-wetland-1`) and flood `unknown` plots | `null` |
  | `edge-65` (probe; flagged on 25 May and 9 Aug) | 0 %: flagged, all not cropland, a real 0.0 |

  Two Sept 2024 plots are 100 % cropland, so a high share does appear in a real flood: the share doesn't separate the two cases plot by plot, as the check's note says. The two with 18 % and 27 % are the only ones clearly unlike the false alarm. Four plots is not a test of the rule. Pooled, the September plots also carry any spring flags on the same pixels, so the two 100 % values may not be the September flood's own share. The flood file is the 10 Nov build; re-run with the per-date field on the F3 rebuild (F6).
- **Not done:** the frontend sentence of C' (item 8) is the website's, not G3's.
- **Wording the report may use** (from `flood/worldcover-accuracy.md`): "Land cover from ESA WorldCover 2021 (10 m). Its published global overall accuracy is 76.7 %; accuracy for cropland in this area has not been checked. The share is an indicator that the flagged area was farmland, not proof." A low share is informative, a high one is ambiguous (about half of real flood detections carry it); it says "can include", never "is". It is a 2021 map applied to 2024 flood dates.
- **The lead's answers (26 Nov, PR #20 review):** (1) a missing `worldcover.tif` stays a 503 for every plot, `unknown` flood included, like the other layers: a broken server, not missing data; (2) **still open:** the 20-point rule was judged on the two cases it was chosen from, so a held-out event is still to be tested; (3) `worldcover.tif` goes on the Drive (and into the deployed API's data, G4).
- **Review fix (26 Nov):** the grid check now runs before the plot is read, so a `worldcover.tif` smaller than the flood grid answers 503 for every plot, not 422 ("draw it inside the area") for plots outside it.
- **Ground note (not G3):** items 5 and 11 above still write the ground share's denominator as max(1, round(`area_ha`)). L3 on 25 Nov kept the cells whose centre fits in the plot, as built in PR #11, and `architecture.md` says so. The log above is not changed.

---

## 1b. The flood history ends at GFM v3 (decided 13 Nov 2026)

**Choice: option A.** The flood history uses GFM v3 only: 2015 to 13 April 2025. `period_end` says so.

**For a live product:** move to v4. Either rebuild the whole history once GFM reprocesses its archive in v4, or keep a separate v4 history next to the v3 one. Say this in the roadmap.

**Why**
- GFM's own rule: "GFM Layers produced from different MAJOR versions can not be used in unison" (versioning page).
- v4 changed the clean-up after detection, so it keeps small flood patches that v3 removed. A v3 count and a v4 count are not the same measurement.
- Every test we ran is on v3: Botoșani 2018, the September 2023 dry window, spring 2024 and September 2024.

**Cost accepted**
- The history shows nothing after 13 April 2025, and v3 will never produce new data.

**Options not taken**
- Use everything, v3 and v4 mixed.
- Use everything after re-testing on v4.

**Evidence** (read directly on 13 Nov 2026)
- **Catalogue, our AOI:** the last v3 scene is 13 Apr 2025; the first v4 scene is 14 Apr 2025. Each scene records its version (`processing:version`) and which algorithms contributed (`flood_members`).
- **Archive:** every scene up to 7 Apr 2024 was reprocessed in one batch in May 2024 with v3.1.0. Later scenes were processed on the day.
- **The version label is not exact:** v3.2.0 (27 Nov 2024) never appears; scenes up to 13 Apr 2025 say v3.1.0.
- **What v4 changed** (versioning page, CEMS news of 17 June 2025):

  | Part | v3 | v4 |
  |---|---|---|
  | TU Wien | Majority filter | Removes patches under 17 pixels, fills holes under 7 |
  | LIST | No terrain filter listed | Drops flood patches whose height-above-drainage values look wrong |
  | DLR | Fixed fallback threshold | Fallback threshold per scene, wider region growing, less blob removal |
  | Ensemble | Removed small patches after voting | No clean-up |

- **Measured effect, the consortium's own figures on 20 use cases:** critical success index +6.3, omission error −8.87, commission error +2.11.
- **Not fixed in v4:** "Remaining issues in certain land cover types and agriculture overestimation" (consortium slides).
- **Sources:** [versioning page](https://extwiki.eodc.eu/GFM/GFMVersioning), [v4 release news](https://global-flood.emergency.copernicus.eu/news/208-major-update-of-the-cems-global-flood-monitoring-released/), [Roth slides](https://global-flood.emergency.copernicus.eu/media/events/8/8-roth_florian_globalflood25_gfmnewmajorversion.pdf), [Raiger-Stachl slides](https://european-flood.emergency.copernicus.eu/sites/default/files/AM/AM2025/AM2025pdf/Recent%20developments%20of%20GFM.pdf).

**Also looked at: `anomaly_detected`**
- **What it is:** a per-scene flag for "a significant (i.e. unusually high) amount of flooding" compared with that location's history, with a 2 km² minimum ([CEMS news, 28 May 2024](https://global-flood.emergency.copernicus.eu/news/169-minor-gfm-update-for-the-visualization-of-the-anomaly-detection/)). No document names the catalogue field; matching it to that news item is an inference.
- **Not used:** it is set on all 5 scenes of the 30 Apr and 1 May 2024 false alarm and on only 4 of 22 scenes of the real September 2024 flood.

---

## 1a. Passes with no advisory layer (decided 17 Nov 2026)

**Choice: option B, with a way to recover the scenes later.** A scene without an advisory layer counts as not seen. It comes back only once something has checked it, and it is never shown unchecked (that would be option C). Full record: [briefs/1a-advisory-layer.md](briefs/1a-advisory-layer.md), "Lead's choice".

**Why**
- B is what the rule fixed before the run says.
- It is the only option that keeps "missing = `unknown`".
- B is the floor, not the end: the lead wants the lost observations back if that can be done honestly.

**Ways to recover the scenes, cheapest first**
1. **GFM regenerates the missing files.** Asked in the helpdesk message (to-do item 1). No code is needed.
2. **Our own stand-in warning layer** from weather data (frost, snow, soil moisture; for example ERA5-Land), tested against GFM's real warnings. It would be new data with a licence to check, and a new method to validate.
   - **Threshold, fixed 17 Nov before the count:** build it only if B removes at least 10 % of AOI pass coverage over 2015 to 13 Apr 2025.
   - **Measured 18 Nov: 8.15 %.** That is below the threshold, so this route is a roadmap line (to-do item 7).
3. **Rejected:** copying warnings from neighbouring passes. Frost and dry soil change within days.

**The share count** (`checks/advisory_layer/share_of_passes.py`)
- **Scenes read:** all 8,543. 2,067 see at least 5 % of the AOI, and 116 of those have no layer.
- **Per pixel:** a median of 8.5 % of passes removed (out of a median of 1,360 passes), a maximum of 22.5 %.
- **By period:** Sep 2018–Jan 2020, 15.5 %; 2015–2021, 10.2 %; 2022 to 13 Apr 2025, 0 %. The 2015–2021 figure is above 10 %, but it is context: the threshold was fixed on the whole period.
- **Method:** every scene's layers read at 640 m. That matched the 20 m read on 20 scenes (58.9 % vs 58.5 % seen) and agreed on "sees the AOI" for all 335 scenes read earlier.
- **A first attempt is void.** It used catalogue footprints, which are the whole 300 km Equi7 tile, so it failed its own method check.

**Corrections found in the 1a chat** (they also apply to the text below)
- **Botoșani:** 96.7 % and 99.3 % are precision. Ensemble recall is 67.6 % (2 July outline) and 58.5 % (3 July).
- **What B removes at Botoșani** is the 2 July 16:00 Sentinel-1 *pass*, not a reference outline. Both COSMO-SkyMed outlines (2 and 3 July) are still scored, against all passes from 29 Jun to 12 Jul minus the dropped one(s). How much recall falls is unknown until the re-score.
- **Spring windows:** missing scenes fall inside the 20 Apr–5 May windows that decision 2 may use: 28 Apr 2019, 22 Apr and 4 May 2020, and 29 Apr 2021. Under B those springs have fewer passes.

### Before the decision: the options, the check and its result

**The question:** 224 of 9,102 scenes over 2015–2025 have no advisory layer (the first scan found 198 plus 27 it couldn't tell; the check settled all but one of those as missing). Do they count as "no warnings" (today), "not seen", or "seen, but labelled"?

| Option | What happens | Cost |
|---|---|---|
| A. Keep "no warnings" | All 198 scenes count in full | Frost, snow or dry-soil false alarms in them go in unchecked |
| B. Whole scene "not seen" | Those scenes are dropped | Real observations are lost; at Botoșani this drops a real flood scene |
| C. Keep the scene, label its detections | Floods stay, marked "no warning information" | More code, probably a contract field |

**Chosen on 13 Nov:** check first whether the 198 scenes hold more flood than ordinary scenes, then pick.

**The check**
- **Code and results:** `checks/advisory_layer/` (the script, `scenes.json`, `flood.csv`).
- **Control group:** for each missing-layer scene that sees the AOI, the nearest-in-date scene of the same frame that has the layer.
- **Rule, fixed before the run:**
  - A scene is flood-heavy if GFM marks flood on at least 1 % of the land it sees.
  - The missing-layer group is flood-heavy if its share of such scenes is at least double the control's and at least 5 percentage points higher.
  - Not flood-heavy: option B.
  - Flood-heavy: look at the dates before choosing, because frost or snow days would also look flood-heavy.
- **Seen in a one-month test (June 2019):** the gaps sit on the same frame at every repeat of a track, so they follow the satellite track, not flood events. If that holds, option B removes one track's view of the AOI for the affected months.

**Result (run finished 13 Nov): not flood-heavy, so the rule points to option B.**

| | Scenes judged | Flood-heavy | Median flood | 90th percentile |
|---|---|---|---|---|
| Missing layer | 116 | 3 (2.6 %) | 0.008 % | 0.30 % |
| Control | 63 | 6 (9.5 %) | 0.015 % | 0.61 % |

- **The verdict doesn't depend on the control.** 2.6 % is below the 5-point margin even against a control of 0 %.
- **The control is weak; don't read it as "missing scenes hold less flood".** 53 of its 116 scenes saw 0 % of the AOI, the 63 judged see 7–59 % (every missing scene sees 59 %), and they sit a median of 126 days from their pair, so in another season.
- **Coverage:** 223 of the 224 scenes were read; one 2025 scene has no `exclusion_mask`.
- **Which scenes see the AOI:** 116 of the 224, on two tracks, all at 12-day spacing:
  - 16:00 UTC (102 scenes): June 2017 to December 2021, nearly every repeat from September 2018 to January 2020.
  - 04:12 UTC (14 scenes): November 2015 to May 2016.
  - The other 108, including all five 2025 scenes, see none of the AOI. The 2025 ones are all after 13 April 2025, so outside the history under 1b anyway.
- **Cost of option B:** for those stretches, that track's view of the AOI is lost. What share of all AOI passes that is wasn't measured, because the check never counted the scenes with the layer that see the AOI.
- **What option A would let in unchecked:** the three flood-heavy missing scenes are 11 and 23 Mar 2019 (2.4 %, 1.8 %) and 29 Apr 2021 (1.6 %). Whether they are real floods or soil false alarms is unknown.
- **Link to decision 2:** 2 July 2018 16:00 is a missing scene. Under B, that pass drops out of the Botoșani score (corrected above: both outlines are still scored).
- **Choosing other than B** would depart from the rule fixed before the run; say why if you do.
