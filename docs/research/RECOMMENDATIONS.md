# Recommendations

Date: 2026-11-12. Written by the research coordinator for the team lead. Nothing here is a decision: decisions go in [architecture.md](../architecture.md). The evidence is in the three syntheses: [flood](flood/SYNTHESIS.md), [ground](ground/SYNTHESIS.md), [heat and drought](heat-drought/SYNTHESIS.md).

**How to read this**
- **Evidence tags** are the same as in the syntheses: **[F1-4]** is a claim a reviewer marked `verified`; **(R)** is something a reviewer found and opened, which nobody checked; **(ours)** is our own measurement.
- **Person-hours are my estimates.** No source gives them. They include tests and wording, not the pitch.
- **"Hinges on"** names what a recommendation depends on that is not verified.
- **No follow-up round was run,** so every gap the reviews exposed is still open.

## What to try first
1. **Flood: check the GFM batch, then test the per-algorithm layers properly.** Two cheap checks come before any 10-year run: which GFM version made each pass, and whether the three algorithms disagreed on 30 Apr and 1 May 2024. If they disagreed, write a rule down and test it on other springs and another event. No source promises this works, so in parallel the lead decides how the report shows flood dates on farmland (F-3). That decision is needed either way.
2. **Ground: build EGMS Ortho as planned, with three specifics.** Download the tiles by hand now. Report the median of the cells around the plot with the count of cells behind it. Show a signed number without risk classes, because no threshold has a verified source for EGMS.
3. **Heat and drought: build nothing before the freeze.** Nothing cheap changes the default. The pitch gets a concrete first roadmap item instead: a hot-day count from ERA5-Land shown as regional climate context.

**Order against the milestones**
| By | Flood | Ground |
|---|---|---|
| Sun 15 Nov (data test) | F-1 checks; F-2 exploration table; send the two emails | Manual download; fix the plot rule in writing; count cells under the 20 test plots |
| Sun 22 Nov (gate) | F-2 rule and criteria written, then the held-out run; lead decides F-3 | `ground.tif` and the real API section |
| Sun 29 Nov (flood validated) | The batch on a checked period; F-3 in the contract if approved | Wording and tests |

**Budget:** flood 30–45 h (F-1, F-2, F-3 and the two small tasks) and ground 15–22 h, so 45–67 h of the roughly 280–350 h the whole project has.

## Flood

### Build now

#### F-1. Check the batch before running it (6–10 h)
- **Why:** the reviews exposed three things that affect a 2015–2025 count regardless of the spring problem.
- **Data and licence:** GFM from the EODC STAC catalogue, as today. The CEMS terms allow reproduction, distribution and adaptation and ask for an attribution notice [F3-18]. They don't mention commercial use in either direction.
- **What to do:**
  - **Version per pass.** Record which GFM version produced each pass. If the archive crosses the v3/v4 boundary and older items were not reprocessed, keep the history inside one major version and say so in `period_end`.
  - **Passes without an advisory layer.** Count them as not seen. No source explains the gaps (the F1 explanation was `unsupported`), so under the method rules they are "unknown whether there were warnings". The cost is known: at Botoșani it drops a real flood scene (ours). Re-score and report the change.
  - **Algorithms per pass.** Record how many of the three algorithms contributed to each pass. F-2 needs it, and since 27 Nov 2024 a flood pixel can rest on one algorithm (R).
  - **Attribution.** Add "Contains modified Copernicus Emergency Management Service information [Year]" to the report and the README.
  - **Ask the GFM helpdesk** two questions: were items before April 2025 reprocessed with v4.0, and why are advisory layers missing on some passes. This is an outward message, so the lead sends it.
- **Pipeline change:** tags written by `flood_gfm.py`; how `gfm_score.passes()` treats a missing advisory layer. No contract change.
- **Validation:** re-run the existing criteria (September 2023 dry window, September 2024 recall, spring 2024, Botoșani) and log before and after in `flood-validation.md`. No threshold changes.
- **Hinges on:** the version boundary is (R), from the GFM versioning page and consortium slides.

#### F-2. A per-algorithm rule, run as a pre-registered experiment (12–18 h)
- **Why this one:** it is the only signal inside GFM that nobody has tested, it uses the same sensor and the same files, and the three algorithms work differently [F1-11, F1-12]. The honest prior is low: the consortium says the single-image and the time-series algorithm are both affected by agriculture [F1-15].
- **Data and licence:** the `dlr_flood_extent`, `list_flood_extent` and `tuw_flood_extent` assets of the same STAC items [F1-11]. Same terms as F-1. Whether every pass since 2015 carries all three was not checked.
- **Steps:**
  1. **Explore, and call it exploration.** For 30 Apr and 1 May 2024 and the September 2024 flood passes, tabulate per algorithm the flagged area in the polder and inside the EMSR758 outline.
  2. **Stop rule.** If all three flag the polder about equally, stop, log the negative result and go to F-3.
  3. **Write before testing.** Put in `architecture.md`: the rule, how a pass with fewer valid algorithms is treated (`unknown`, never "no flood"), the windows and the pass limits.
  4. **Held-out test.** Suggested, for the lead to fix:
     - The spring window 20 Apr–5 May in two other years: at most 1 % of land flagged in ≥1 pass.
     - The September 2023 dry window: still at most 1 %.
     - Botoșani July 2018 against the COSMO-SkyMed outlines: recall at least 50 %.
  5. **Check the test has power.** Report the plain ensemble's rate in the same spring windows. If the ensemble already passes there, those windows can't show an improvement, and the result says so.
  6. **Confirm the windows are dry.** No flood on record, and a clear Sentinel-2 image checked by eye. Sentinel-2 is used here as an independent reference only, not in the pipeline.
  7. **Report spring 2024 and September 2024 as in-sample.**
- **Pipeline change if it passes:** `flood_gfm.py` reads three more assets per pass, and `algorithm_version` gets a new value. The contract's shape doesn't change.
- **Validation:** as in step 4, with precision and recall against the two independent-sensor references we already hold (PAZ and COSMO-SkyMed).
- **Rejected forms of this idea:** choosing the rule on the failing scenes and calling that a validation; an "all three must agree" vote that turns single-algorithm passes into "no flood".

#### F-3. A cropland caveat on flood dates: flag, never remove (10–14 h, needs the lead's decision)
- **Why:** the false alarm is a documented GFM weakness with no service fix before 2027 [F1-5, F1-20], and no published fix was found. Even if F-2 helps, some of it will remain. The report can't present every pass date as a confirmed flood, which `architecture.md` already says.
- **What:** every detection stays. The report adds, per plot, how much of the flagged area is arable land, with one fixed sentence: on arable land, radar detections include false alarms from bare, smooth soil, as GFM's own documentation says [F1-1].
- **Data and licence:** ESA WorldCover, 10 m, 2021, "free of charge, without restriction of use", CC BY 4.0 [F2-10], from its own data-access page, not Earth Engine. A static map, so not a new sensor; the lead confirms that reading at the gate.
- **Pipeline change:** one static cropland band resampled to the flood grid. A new field in the flood section of the evidence contract, so it needs the lead's review.
- **Validation:** it is a caveat, not a detector. The spring test stays failed, and the report says so. Before computing, write down the two numbers to report: the share of the 30 Apr and 1 May 2024 false alarm that is cropland, and the share of the EMSR758 flood that is cropland (real floods that would carry the caveat).
- **Limits:** the map is from 2021, and it can't tell a tilled field from a planted one.
- **Hinges on:** nothing unverified for the data. The design is our own; no published test of such a flag was found.
- **The alternative** the team already weighed is the verified-event list in `architecture.md`. The research adds nothing for or against it.

#### Do now, no build (2–3 h)
- **Ask ANAR and INHGA** for the licence and GIS files of the RO-FLOODS maps. Cite Implementing Regulation (EU) 2023/138, which lists natural risk zones as high-value data to be published under CC BY 4.0 or equivalent with bulk download (R). Replies take weeks, and the answer decides the best roadmap item. The lead sends it.
- **Read the header of one JRC European flood map file** over Galați: coverage and nodata value. It turns a roadmap item from "probably" into a fact.

### Roadmap
| Item | What it would add | What it needs |
|---|---|---|
| Sentinel-2 check on detections | The only independent-sensor test of a single detection | A new sensor; a computation over the whole area for every pass; an index, a threshold and a maximum time gap fixed in advance; a count of clear images near each pass. It can flag, not confirm. Weak before 2017 (R). No verified claim shows such a rule working |
| Official modelled hazard (RO-FLOODS) | LiDAR-based depth and extent, the layer the competitor shows by address point [F4-13, F4-21] | A licence and files from ANAR. Today: viewer only |
| JRC European flood hazard maps v3.1.1 | A modelled layer that fits the pipeline now: 90 m, nine return periods, GeoTIFF, no login [F4-1] | Which licence governs [F4-6]; the lead's wording for return periods; a way to tell "not modelled" from "dry"; any validation of version 3 (none published) |
| Event coherence (ASF HyP3) | A second radar cue for bare soil against water | A new product type at 40–80 m (R); its terms unread |
| Hydrodynamic model of the confluence | Depth and extent for chosen scenarios | Daily Siret and Prut discharge, defence geometry and better terrain, none of which we found [F5-10, F5-25, F5-26] |
| Surrogate (GNN or CNN) | Fast scenario maps | The hydrodynamic model first [F6-9]; transfer to new terrain is not achieved [F6-15, F6-16, F6-17] |
| GFM's next algorithm (2027) | Possibly fewer farmland false alarms [F1-20] | Re-run our spring test when it ships |

**For the pitch:** "implemented" is observed flood history with stated limits and an explicit `unknown`. "Next" is the Sentinel-2 check and the official maps. Don't promise a surrogate "validated against GFM": no source shows one validated against satellite extent, and GFM is our own flood source.

### Rejected
| Option | Why |
|---|---|
| A stricter likelihood cut-off | No source evaluates one [F1-8, F1-9, F1-10]; our medians are 72 against 73 (ours) |
| Expecting more from the advisory flags | Regional by design, and "typically not raised" for agricultural over-detection [F1-3, F1-4] |
| Masking cropland out | It deletes the floods our users care about (reasoning; no source) |
| Requiring two or more passes | Still 2.17 % in the spring window, and it costs flash-flood recall (ours) |
| A HAND filter for this false alarm | 77 % of the flagged area is under 1 m above the river (ours) |
| Corine Land Cover as the mask | 100 m with a 25 ha minimum unit [F2-12] |
| Google Flood Hub | Forecast-only, waitlist, "primarily limited to non-commercial use", no downloadable hazard raster [F3-22, F3-24] |
| GloFAS or EFAS discharge as a plot layer | River discharge on grids of about 5 km and 1 arcminute, not water on land [F3-11, F4-10] |
| JBA Flood Foresight | Commercial; vendor description only [F5-11, F5-12, F5-13] |
| FFWC "Super Model" | Built for Bangladesh's rivers and gauges [F5-14, F5-15] |
| A pretrained surrogate pointed at Galați | The public weights are for synthetic grids and Swiss cities [F6-21, F6-22] |
| Quoting GFM's own accuracy figures as our validation | Their references come from Sentinel-1 (R); the 43.7 % figure belongs to an old archive version |
| Scraping the RO-FLOODS viewer | A viewer is not a licence |
| Earth Engine as the route for product data | The free tier is for non-commercial use [F2-16] |

## Ground motion

### Build now

#### G-1. EGMS Ortho, vertical, as a neighbourhood value (15–21 h)
- **Data and licence:** EGMS Ortho (L3), the newest release the Explorer offers; write down which one. Copernicus Land Monitoring Service terms: full, open and free; name the source, state that the data were modified, don't imply EU endorsement [G1-23].
- **Access:** a one-off manual download with EU Login [G1-19]. Keep the raw tiles in `data/raw/`, because the Explorer keeps only two releases [G1-17] and the data move to another platform this winter (R). Don't plan on the API: no source says it serves Ortho.
- **Pipeline change:** `pipeline/ground.py` mosaics the per-tile vertical GeoTIFFs [G1-11], reprojects them from EPSG:3035 (R) and clips them to `ground.tif`. The release name goes into the COG tags. If the 15 Nov data test shows the uncertainty field can be read, add `mean_velocity_std` as a band.
- **Plot rule (ours; write it down before the data test):**
  - **Value:** the median of the available cells among the cells the plot touches plus one ring of neighbours.
  - **`n_cells`:** how many of those cells have a value.
  - **`unknown`:** fewer than a fixed minimum of cells. I suggest 3; the lead fixes it.
  - **Why this shape:** no published rule exists [G1-24]. EGMS advises reading clusters, not lone points (R). The competitor uses a 3×3 median [G3-12], which keeps the two products comparable.
- **Output:** a signed mm/year value, with no risk classes. The contract already has `status`, `velocity_mm_yr`, `n_cells` and `release`, so its shape doesn't change. Showing the standard deviation or the east-west layer would change it.
- **Report wording, fixed sentences:**
  - "Describes about N ha around the plot, not the plot itself."
  - "No value means no reliable measurement, not stable ground" [G2-10].
  - "Not a geotechnical or damage assessment."
- **Validation under the method rules:**
  - **Unknown rule:** a test in `api/test_main.py`, like terrain and flood.
  - **Coverage:** the share of the 20 test plots that reach the minimum, by plot size. This is the honest headline number for the layer.
  - **Accuracy:** we can't validate velocities ourselves; no independent reference for Galați was found. Say so, and say that EGMS's own validation reports cover older releases, not the current one (R).
  - **Consistency check, not validation:** compare our value with Imoreview's at 3–5 addresses. Same source, so agreement only shows we read the data the same way.
- **Hinges on:** the Ortho cell rules come from documents written before the 2020–2024 quality-control change (R). Whether Galați farmland has Ortho cells at all is unknown until the data test.

#### G-2. Fix the label rule before 15 Nov (a decision, under 1 h)
- **Recommended:** no classes. No velocity threshold has a verified source for EGMS, and none links velocity to damage.
- **If the lead wants a two-state label:** "no motion distinguishable from noise" at or below 2 mm/year, marked as our own rule. It is about three times the 0.7 mm/year (1 σ) the product specifies [G2-4]; that is arithmetic, not a source.
- **Don't** present 5 mm/year as an EGMS threshold. The only verified source is a 2013 landslide threshold on older data, measured along the slope [G2-1].

### Roadmap
| Item | What it needs |
|---|---|
| A sourced threshold | Open Palama et al. (JISDM 2025), which may justify 5 mm/year by about 2 mm/year noise (R, unverified) |
| East-west component, acceleration and seasonality | A contract change; the fields exist per cell [G1-10] |
| Calibrated points for larger plots | A point-to-plot rule and per-track handling [G1-8] |
| Scripted download | Confirmation that the API serves Ortho, after the platform move (R) |
| Regional landslide context | ELSUS only with ESDAC's written answer on derived products [G3-3]; county maps under HG 447/2003 if Galați has one (unverified). A new hazard under the constraints |
| Soil and slope context | SoilGrids at 250 m, CC BY 4.0 [G3-10]; no slope threshold was found |

**For the pitch:** we use the same ground data as Imoreview at the same resolution. What differs is the unit (a drawn plot of any size against an address), an explicit `unknown` (they omit the section [G3-15]), and observed flood history next to it. Don't say they are free and we can't compete on price: they sell four per-address products at 19 to 179 lei (R).

### Rejected
| Option | Why |
|---|---|
| EGMS Basic | Not comparable across areas [G1-7] |
| ELSUS as a plot score, or shipped as a COG now | "Should not be used to deduce local information" [G3-2]; terms forbid passing the data to third parties [G3-3] |
| NASA LHASA 2 as a susceptibility layer | It is a daily nowcast at about 1 km (R) |
| Any wording that links a velocity to damage | No verified source |
| Quoting the EGMS building sentence without its qualifier | The source continues "unless they are large enough to cover the ambiguity" (R) |
| The `token.jwt` in the public `copernicus-land/egms-api` repository | Someone else's credential (reported by a researcher, unreviewed). Create our own token |

## Heat and drought

### Build now
**Nothing.** This is the default the constraints set, and the research found nothing that overturns it:
- **It is a new hazard after the gate,** and it needs a new section in the evidence contract.
- **The only cheap candidate is regional.** One ERA5-Land cell is about 8,000 ha [H3-4], so almost every plot in the pilot would show the same number. That is context, not evidence about a plot.
- **Validation would be thin.** One station against one cell, split by years only, and ERA5-Land is not fully independent of station observations [H3-3]. The station's licence for our use is not established.
- **The flood decision is still open,** and flood is the core.

**If the lead opens it at the 22 Nov gate anyway,** this is the one version to build:

#### H-1 (conditional). Hot days per year from ERA5-Land, shown as regional climate context
- **Data and licence:** "ERA5-Land daily statistics" on the Copernicus Climate Data Store: daily maximum 2 m temperature, 0.1°, 1950 to present, CC-BY [H3-1, H3-2, H3-5]. CC BY 4.0 allows commercial use with attribution [H2-30]. Cite the catalogue entry.
- **Effort:** the researcher estimated 15–25 h. With the contract, the frontend and the validation I estimate 20–30 h. Neither figure has a source.
- **Pipeline change:** one `cdsapi` request for a box around the pilot region; count the days above one written threshold per year; write a small COG. Access needs an account, a personal token and one manual licence acceptance (R). New dependencies through `uv add`: wheels look available for 3.14, but nothing was install-tested (R).
- **Contract:** a new evidence section, so the lead's review comes first.
- **Threshold:** ours, written before any run. The WMO says heat thresholds are local [H1-1]; the ETCCDI indices are a standard starting point (R).
- **Validation:** yearly hot-day counts against the Galați station in GHCN-Daily for years held out in advance, with the pass criterion written first. Report it as agreement with a partly dependent reference.
- **Presentation:** "regional climate context from a reanalysis; the same value for every plot within about 9 km". Never "risk", never per-plot.
- **Hinges on:** the station series (R, read through a tool summary; confirm by hand) and its licence (ECA&D origin, policy unread); the lead's ruling on whether a reference used only for validation needs an open product licence; ERA5-Land's bias for hot extremes (search results only).

### Roadmap
| Order | Item | What it needs |
|---|---|---|
| 1 | H-1 above | The conditions listed there |
| 2 | Regional drought context | SPEIbase is 0.5°, to December 2024, under the Open Database License [H2-13]. The European Drought Observatory would be finer, but its resolution and licence were not found |
| 3 | An observation-based heat layer (E-OBS) | Its open licence text and grid spacing, both unread [H2-7] |
| 4 | Scenario statements from EURO-CORDEX | 0.11°, three scenarios, commercial use allowed [H2-42, H3-22]. Worded as "under scenario X the region shows Y", outside the "past observations" rule until the lead widens it |
| 5 | Plot-scale surface temperature or vegetation stress | Landsat, ECOSTRESS or HR-VPP [H2-17, H2-18, H2-35]. A way to handle clouds, crop rotation and irrigation, and an independent field-scale reference. None was found |
| 6 | From hazard to risk | Exposure and vulnerability data per plot (crop, irrigation, soil, buildings). Not found |

**For the pitch:** say "hazard indicator" or "regional climate context", not "risk" [H1-7]. Don't claim the pilot region is drying: the trends we verified are for Sulina, Dobrogea and Romania as a whole, not Galați [H1-15, H1-16, H1-17].

### Rejected
| Option | Why |
|---|---|
| A per-plot heat or drought "risk score" | Risk needs exposure and vulnerability [H1-7]; vendor scores diverge at property level in the one comparison found, which was on fire and flood [H1-13] |
| Seasonal forecasts | They describe the coming months [H1-8], on a 1° grid, with an extra licence nobody read [H2-44] |
| The CDS "heat waves and cold spells" dataset as history | It is climate-model output, not observations [H2-10, H3-5b] |
| ROCADA | On request, "licensing unknown", ends in 2013 [H2-8] |
| NOAA VHI | "Provided for experimental use only", 4 km [H2-22] |
| Suomi NPP VIIRS surface temperature going forward | Delivery ceased on 2 November 2026 [H2-37] |
| MODIS as a continuing series | Terra and Aqua start shutting down in late 2026 or early 2027 (R) |
| Landsat surface temperature as "how hot the plot gets" | Surface, not air, temperature; a 100 m sensor; morning overpass; a known cloud error [H2-19, H3-10, H3-11] |

## Decisions the lead needs to make
The lead's choices so far, and the to-do list that follows from them, are in [DECISIONS.md](DECISIONS.md).

1. **Flood, F-1:** count passes without an advisory layer as not seen? What to do if the batch spans two GFM major versions?
2. **Flood, F-2:** the held-out windows and limits, before anyone runs them.
3. **Flood, F-3:** the cropland caveat as a new contract field, or another way to show unconfirmed dates.
4. **Flood:** send the emails to the GFM helpdesk and to ANAR?
5. **Ground:** the plot rule and minimum cell count, and classes or no classes, before the 15 Nov data test.
6. **Heat and drought:** confirm "roadmap only".
7. **General:** does a dataset used only to validate, and never shipped, need an open product licence?
8. **Research:** run the follow-up round on the open gaps, or stop here?

## What each recommendation hinges on
| Recommendation | Unverified point it depends on |
|---|---|
| F-1 version check | The v3/v4 boundary and "can not be used in unison" are (R) |
| F-1 single-algorithm passes | Claim F1-14 was `misquoted`; the fact rests on the reviewer's reading |
| F-2 | No source says the algorithms differ on tilled soil. Whether old passes carry all three assets is unchecked |
| F-3 | Our own design; no published test of a cropland caveat |
| RO-FLOODS request | Regulation (EU) 2023/138 applying to these maps is (R) and unconfirmed |
| JRC maps as fallback | Coverage of Galați (header unread), the licence, and the absence of any version 3 validation |
| G-1 | Ortho cell rules documented for older releases; uncertainty field readable from the delivery; Ortho coverage of Galați farmland |
| G-1 manual download | That the API doesn't serve Ortho is unknown, not established |
| G-2 fallback label | 2 mm/year has no source |
| H-1 | The Galați station and its licence; 3.14 installs; ERA5-Land hot-extreme bias |
