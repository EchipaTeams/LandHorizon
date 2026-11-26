# Flood: synthesis

Date: 2026-11-12. Written by the research coordinator from the six reviewed findings files in this folder. Nothing here is a decision; decisions live in [architecture.md](../../architecture.md). What to do about it is in [RECOMMENDATIONS.md](../RECOMMENDATIONS.md).

| ID | File | Verdicts |
|---|---|---|
| F1 | [gfm-spring-false-alarms.md](gfm-spring-false-alarms.md) | 21 verified, 4 unsupported, 2 misquoted |
| F2 | [cross-checks-optical-sar-landcover.md](cross-checks-optical-sar-landcover.md) | 15 verified, 1 unsupported |
| F3 | [modelled-hazard-global.md](modelled-hazard-global.md) | 20 verified, 4 unsupported, 1 misquoted, 2 unreachable |
| F4 | [modelled-hazard-europe-romania.md](modelled-hazard-europe-romania.md) | 14 verified, 5 unsupported, 2 misquoted, 3 unreachable |
| F5 | [hydrodynamic-models.md](hydrodynamic-models.md) | 18 verified, 3 unsupported, 5 unreachable |
| F6 | [gnn-surrogates.md](gnn-surrogates.md) | 22 verified, 3 unsupported, 1 misquoted |

## How to read the evidence tags
- **[F1-4]** = claim 4 in file F1, marked `verified` by its reviewer. Only these carry a conclusion.
- **(R)** = something the reviewer found and opened while checking. One person read it and nobody checked the reviewer, so it is weaker than a verified claim. A conclusion that leans on an (R) item says so.
- **(ours)** = a measurement from [flood-validation.md](../../flood-validation.md) or architecture.md.
- **not found** = searched for and not found. That is not proof it doesn't exist.
- **Limit of every verdict:** researchers and reviewers read pages through a fetch tool that summarises and caps quotes at about 125 characters. PDFs were read through a text-extraction proxy or not at all. "Verified" means the exact string was confirmed by that route, not that someone read the page by eye.
- **No follow-up round was run.** The gaps the reviews exposed are listed at the end and are still open.

## Bottom line
1. **The spring false alarm is a documented, unresolved GFM weakness.** The GFM consortium itself calls agricultural over-detection probably its most problematic case [F1-5]. No fix is announced before a new algorithm planned for March/April 2027 [F1-20].
2. **No layer inside GFM is shown to separate tilled soil from water.** The advisory flags are regional [F1-3, F1-4]. No source supports a stricter likelihood cut-off [F1-8, F1-9, F1-10]. The exclusion mask is static [F1-26].
3. **The one untested signal inside GFM is the three per-algorithm layers,** which are published per pass [F1-11]. No source says they help: the consortium says the single-image and the time-series algorithm are both affected by agriculture [F1-15].
4. **No published study was found that tests any fix for tilled-field false alarms against an independent reference** (F2 headline; the two closest papers were read at abstract level only). So whatever we do is our own method and needs our own pre-registered test.
5. **A Sentinel-2 check is the only option with independent-sensor logic,** but no verified claim shows such a rule working, it is a new sensor for the pipeline, and it can flag or reject a detection, never confirm one in cloud.
6. **Modelled hazard:** Google Flood Hub and GloFAS / EFAS discharge are not plot-level layers. The JRC European flood hazard maps (90 m, nine return periods) are the only product that fits the pipeline today, with an unresolved licence, no published validation of the current version, and return-period wording that needs the lead's decision. RO-FLOODS has the better content and no usable access.
7. **Hydrodynamic models and GNN surrogates are roadmap items.** A surrogate needs a hydrodynamic model first, and a hydrodynamic model needs discharge, terrain and defence data we did not find.
8. **The research exposed a new risk for the 2015–2025 batch:** GFM v4.0 (April 2025) is a major version, and GFM's versioning page says layers from different major versions can't be used together (R).

## Part 1. Making the observed history trustworthy

### 1.1 What GFM says about the failure
- **Cause, in the user manual:** "Certain growing conditions and agricultural practices over cropland" give very low backscatter and look like water [F1-1].
- **Severity, in the consortium's own review:** over-detection in agricultural and grassland areas is "probably the most problematic case from a service point of view". False positive rates "can be quite high in some agricultural regions", depend on crop type and weather, and are worse on dry soils. The review gives no rate. It names rapid changes in surface roughness and crop cover from farming, but never tillage or bare soil by name [F1-5].
- **No fix in the operational version:** version 3 updated its harmonic parameters "to improve accuracy over agriculture" [F1-23]. The next step is a deep-learning algorithm (SWIM) with an implementation target of March/April 2027. Its improvement is the consortium's own claim with no independent check [F1-20].
- **Version 4.0 did not solve it (R):** the consortium's slides list "Remaining issues in certain land cover types and agriculture overestimation" and an average commission-error change of +2.11 (no units, baseline version not named).
- **Not found:** any GFM validation over Romania, and any published false-alarm rate on cropland.

### 1.2 What each GFM layer can and cannot do
| Layer | What the sources say | Effect on our problem |
|---|---|---|
| Advisory flags | Two flags (low regional backscatter, rough water). They are not removed from the maps [F1-2]. The low-backscatter flag compares against a regional monthly median after resampling to 20 km, with a 14 km buffer [F1-3]. The consortium says flags "are typically not raised for overdetection in agricultural areas", because the effect is confined to smaller areas than frost or drought [F1-4]. | Explains why the flags removed only part of the 30 Apr 2024 false alarm (40 % of flagged pixels carried a flag) (ours). Already used; no more to gain. |
| Likelihood | The mean of the per-algorithm likelihoods, with 50 as the class boundary [F1-7, F1-25]. No cut-off other than 50 is evaluated anywhere [F1-8]. Thresholding is "not carried out by the GFM service itself"; the one external study used 0.3, which is below the boundary and adds flood pixels [F1-9]. The 2023 quality report left likelihood out of validation [F1-10]. | No sourced cut-off. Our own medians are 72 (false) against 73 (real) (ours). Dead end. |
| Exclusion mask | Five static sub-layers. "Water look-alikes" is built from 2020–2022 backscatter statistics [F1-26]. | It does not change with field state. No layer with crop or tillage information was found. |
| Per-algorithm extents | `dlr_flood_extent`, `list_flood_extent`, `tuw_flood_extent` and their likelihoods are assets in the STAC collection, labelled "Intermediate output" [F1-11]. The three algorithms work differently: single-image thresholding (DLR), change detection against a recent scene of the same orbit (LIST), and a time-series model (TU Wien) [F1-12]. The ensemble is a majority vote [F1-13]. | The only untested signal. See 1.3. |

### 1.3 The per-algorithm layers: what is known
- **No source ranks the three algorithms by cropland false alarms** (not found).
- **Two of the three are said to be affected.** The consortium writes that "not only the single-image algorithm is impacted, but also time-series algorithm", whose harmonic model "cannot account for crop rotation practices". The change-detection algorithm (LIST) is not discussed in that section, which is silence, not evidence that it is cleaner [F1-15].
- **Leads, not evidence:**
  - Tupas et al. 2024 (abstract only, R) reports agricultural overestimation for the TU Wien algorithm.
  - Garg et al. (EGU 2026 abstract) say they evaluate the three algorithms for false alarms; no results are published [F1-18].
- **So the gain is unproven.** Whether the algorithms disagreed on 30 Apr 2024 is an empirical question we can answer from the STAC assets.
- **Three constraints on any per-algorithm rule** (from the F1 review):
  - **Criteria first.** Looking at 30 Apr and 1 May 2024 is exploration. A rule chosen there has to be written down and then tested on other windows and another event.
  - **Missing algorithms mean unknown.** Since 27 Nov 2024 the ensemble also produces a result when only one algorithm has valid input. Claim F1-14 was marked `misquoted`, but the reviewer confirmed the fact from the versioning page and the product definition document, so treat it as (R). A rule that needs two or three algorithms must mark such scenes `unknown`, not "no flood".
  - **One major version.** The rule must not run across the v3/v4 boundary (see 1.5).

### 1.4 Checks from outside GFM
**Optical (Sentinel-2)**
- **Coverage:** two Sentinel-2 satellites give a nominal 5-day revisit [F2-4]. In a synthetic study of about 2,000 European river sites, Sentinel-2 could observe 28 % of flood events against 58 % for Sentinel-1, because of cloud [F2-3]. That number is about cloud *during floods*. The share of dry spring passes with a clear image nearby is unmeasured.
- **Early years are weaker (R):** one Sentinel-2 satellite has a 10-day revisit, and Sentinel-2B was not flying in 2015–2016.
- **Method evidence is thin:**
  - One conference abstract from a flood-mapping vendor uses Sentinel-2 SAVI to identify harvested cropland in arid regions, with a partly independent reference [F2-1, F2-2].
  - Optical water mapping commonly sets an MNDWI threshold per scene with Otsu; no fixed threshold is published [F2-4].
- **No verified claim shows an optical rule rejecting SAR false alarms on tilled fields.** The only evidence that Sentinel-2 separates the two is our own 29 Apr 2024 image, which is the tuning case (ours).
- **What it can claim:** a clear image shortly before or after a pass can flag a detection as doubtful. It can't confirm a flood in cloud, and a real flash flood can drain before the next clear image, so the allowed time gap has to be fixed beforehand.
- **Fit:** Sentinel-2 is a new sensor, which the constraints rate out of scope after the 22 Nov gate. It also has to be computed over the whole area for every pass and written to a COG, because the API reads only precomputed pixels.

**Other radar cues**
- **Coherence:** the free global Sentinel-1 coherence product is a 2019–2020 seasonal climatology at about 90 m, not event data [F2-8]. Coherence-based flood mapping is published for a city (Houston) [F2-9]; nothing was found for bare farmland. ASF HyP3 computes coherence for chosen pairs on request, free within 8,000 credits a month, at 80 m or 40 m (R). That is a new product type for the pipeline: roadmap.
- **Terrain:** one TU Wien study replaces a HAND mask with a HAND prior and trades fewer missed floods for slightly more false alarms [F2-7, F2-14]. HAND can't remove our false alarm: 77 % of the flagged spring area is less than 1 m above the river (ours).

**Land-cover masks**
| Product | Facts | Tag |
|---|---|---|
| ESA WorldCover | 10 m, 2020 and 2021, free "without restriction of use", CC BY 4.0 | [F2-10] |
| EU crop map | 10 m, 2018 (Sentinel-1 based) and 2022 (Sentinel-1 and 2), CC BY 4.0 | [F2-11] |
| Corine Land Cover 2018 | 100 m, 25 ha minimum unit: too coarse for small plots | [F2-12] |
| Dynamic World | 10 m, crops, water and bare bands, CC BY 4.0, read through Earth Engine | [F2-5] |
| JRC Global Surface Water | 30 m monthly recurrence, 1984–2021 | [F2-13] |
| CLCplus Backbone 2023 | 10 m, Europe; licence text not read | (R) |

- **A cropland mask can only flag, not remove.** Our users buy farmland, so masking cropland would delete the floods they care about. A static mask also doesn't know whether a field was tilled that week. Both points are reasoning, not sourced findings; no published test of such a flag was found.
- **Access:** Copernicus Data Space data are "free, full and open"; the 10,000 openEO credits a month are a temporary boost [F2-15]. Earth Engine's free tier is for non-commercial use [F2-16].

### 1.5 What the research adds for the 2015–2025 batch
- **Major version boundary (R).** GFM v4.0 was released in mid-April 2025. The versioning page says "GFM Layers produced from different MAJOR versions can not be used in unison". Not found: whether older STAC items were reprocessed with v4; the collection states no version. Until this is checked, a 2015–2025 count may mix versions.
- **Passes without an advisory layer.** No source explains them. The explanation in F1 (claim 21) was marked `unsupported`. The archive is reprocessed regularly, and no source says flags were back-filled [F1-22]. Under the method rules a pass without the layer is "unknown whether there were warnings", whatever the cause.
- **Tie rule.** The definition document, its own worked example and the consortium's review contradict each other on what a 1-against-1 vote gives [F1-13].
- **Likelihood 49** can mean "detected, then masked by the exclusion mask" [F1-25].
- **Do not quote the consortium's accuracy figures as our validation.**
  - The CSI target is 70 % [F1-6].
  - The often-quoted 43.7 % belongs to archive version 2.1.0 (claim F1-16 was `unsupported` for that reason).
  - The consortium's reference maps are derived from Sentinel-1 with manual Sentinel-2 enhancement (R), so they are not an independent-sensor reference in our sense.
- **Licence:** the STAC collection points to the CEMS terms. They grant free access for reproduction, distribution and adaptation, and ask for the notice "Generated using Copernicus Emergency Management Service information [Year]", or "Contains modified ..." for adapted data [F3-18]. The word "commercial" does not appear in either direction.

## Part 2. A modelled hazard next to the observed history

### 2.1 What each candidate really is
| Candidate | What it provides | Resolution | Licence and access | Verdict |
|---|---|---|---|---|
| Google Flood Hub / Flood Forecasting API | Real-time forecasts for gauged rivers. Access by API key and waitlist [F3-22]. The "inundation history" view is for expert users, with no download described [F3-24]. Romania is on the country list; gauges at Galați were not found [F3-27]. | Forecast points | Data CC BY 4.0, but use is "primarily limited to non-commercial use" [F3-22] | Dead end for a precomputed layer |
| Google Inundation History | How often each pixel was wet, 1999–2020, from unnamed satellite imagery [F3-23] | 128 m | CC BY 4.0, Cloud Storage | Observed, not modelled; ends 2020. Possible cross-check later |
| GloFAS (v4, v5) | Daily river discharge: reanalysis, forecasts, return-period thresholds [F3-1, F3-3, F3-6] | 0.05°, about 5 km | CEMS-FLOODS licence | A river-reach quantity, not a plot layer [F3-11] |
| EFAS | Forecasts: real time for partners only, public after 30 days [F4-9, F4-10] | 1 arcmin (v5) | CEMS-FLOODS licence | Not a plot layer |
| JRC global flood hazard maps v2.1 | Depth for 7 return periods, from LISFLOOD-FP on GloFAS v4.0 flows [F3-4, F3-5, F3-10] | 3 arc-seconds, about 90 m | README: ODbL. Earth Engine: "without restriction" [F3-19] | Same family as the European maps; use those for Galați |
| **JRC European flood hazard maps v3.1.1** | Depth for 9 return periods (10 to 500 years), plus permanent water and "spurious depth" layers; released 5 Mar 2026 [F4-1, F4-2, F4-3] | About 90 m | README: ODbL. `copyright.txt`: CC BY 4.0 [F4-6]. GeoTIFF over HTTP, no login, 260–334 MB per file | The only one that fits the pipeline. See 2.2 |
| RO-FLOODS (inundatii.ro) | Official hazard and risk maps for 526 areas: extent, depth, sometimes velocity, several probabilities, LiDAR terrain [F4-13, F4-18] | Not stated | Viewer only. No licence, no download found | Best content, no usable access. See 2.3 |

### 2.2 JRC European maps: what is and isn't established
- **Established:**
  - Version, resolution, return periods and file layout [F4-1, F4-2].
  - A layer marks places where the 10-year depth exceeds 10 m in small channels (under 3,000 km²), with a warning to use depths there with caution [F4-3].
- **Validation exists only for the older version 2.** Against official maps in five countries (not Romania), it identified on average two-thirds of the reference flood extent at the 1-in-100-year level, with high false alarms in some regions [F4-5, F5-7]. Version 2 modelled only rivers above 500 km² and had no flood defences [F4-4].
- **For version 3 none of that is known.** Its description is "Manuscript under preparation" [F4-2], and its README states no minimum river size and nothing on defences. Version 2's skill and limits can't be carried over (R).
- **Indirect evidence (R):** an independent 2026 paper forced a different inundation model with GloFAS v4 flows and got a mean CSI of 0.39, and notes that global terrain data are too coarse for flood defences.
- **Coverage of Galați:** probably inside the raster. The F4 worry that it stops at 27.81° E was marked `unsupported`: that reading of the README would put the map's latitude range in the far north of Scandinavia. Only the GeoTIFF header settles it.
- **Three decisions it would need from the lead:**
  - **Licence:** ODbL or CC BY 4.0. The JRC Data Catalogue entry, which might settle it, blocked every fetch.
  - **Wording:** "1-in-100-year depth" is probability language from a third-party model. The constraints call the product a screening indicator, not a probability.
  - **Empty pixels:** the README doesn't say whether an empty pixel is "modelled dry" or "river not modelled" (R, checked for the global README; the European one is equally silent on minimum river size). Under the `unknown` rule it can't be shown as "no hazard".
- **It does nothing for the open GFM decision,** and it changes the evidence contract.

### 2.3 RO-FLOODS and the competitor
- **What Imoreview does:** it compares an address point with the RO-FLOODS maps, reports the scenario and the estimated depth, and says itself that a point check "does not describe every corner of the plot" [F4-21, G3-14].
- **Scenarios:** "about 10 %, 1 % and 0.1 %" annual probability is stated only by Imoreview [F4-15]. Official pages say "different annual exceedance probabilities" [F4-13].
- **Flash and pluvial floods:** sources conflict on whether the maps cover them [F4-16].
- **Access:** the maps are on inundatii.ro for anyone to view [F4-14 was `misquoted` by one letter; the fact stands (R)]. An EEA registry record lists the dataset as "Freely accessible" with a "View and Download Service", no licence and no URL (R, from the part of claim F4-17 the reviewer confirmed). The ANAR web map service address returned 404 (R).
- **Leverage (R):** Implementing Regulation (EU) 2023/138 lists natural risk zones among high-value datasets, to be published under CC BY 4.0 or an equivalent licence, with bulk download. Whether RO-FLOODS falls under it and whether ANAR complies was not found. It is the argument to use when asking ANAR.
- **The September 2024 event:** documented as EMSR758, "major floods ... in Galati and Vaslui counties" [F4-23]. No verified claim says it was a small-stream flood, so don't argue that a river model "would have missed it".

### 2.4 Hydrodynamic models (F5)
- **LISFLOOD-FP:** a 2D floodplain model from Bristol [F5-1] with GPU solvers; the published speed-ups are ratios, not runtimes [F5-3, F5-4]. Version 8.3 is current (R). Its licence is stated two ways (see *Where sources disagree*).
- **Alternatives:**
  - SFINCS: source under GPL-3.0, prebuilt binaries under a no-redistribution freeware licence [F5-19].
  - ANUGA [F5-21] and Itzï (GPL, needs GRASS GIS) [F5-22].
  - HEC-RAS is free to use (R; the claim's own source was unreachable).
- **What a model of the Galați confluence would need, and what we found:**
  - **Discharge:** GRDC needs identified access and has no API [F5-10]. Daily Siret and Prut series: not found.
  - **Terrain:** the national 5 m model is derived from 1:50,000 contours, with 1.5 m stated vertical accuracy in flat areas, under OGL-ROU-1.0 (licence text not read) [F5-25]. The 0.5 m LiDAR programme lists other counties, not Galați [F5-26]. FABDEM, the better global terrain in one study [F5-8], is free for non-commercial use only (R).
  - **Flood defences:** no source found. The argument that 30 m terrain can't resolve levees has no verified source either (claim F5-9 `unsupported`).
- **Flood Foresight (JBA):** a commercial system; everything known is the vendor's own description [F5-11, F5-12, F5-13]. Not usable.
- **FFWC "Super Model":** Bangladesh's national forecasting system, built on MIKE 11 and Bangladeshi catchments [F5-14, F5-15]. Not transferable.
- **HAND against hydraulic models:** the two published comparisons use LiDAR terrain plus a discharge and rating curve [F5-17, F5-18]. They say nothing about our 30 m HAND index, which should stay labelled as terrain context.
- **Verdict:** roadmap. The effort figures in F5 are the researcher's own and are not used here.

### 2.5 GNN and other surrogates (F6)
- **They emulate a simulator.** Every surrogate reviewed is trained on hydrodynamic model output, and its accuracy depends on those simulations [F6-9]. Examples: synthetic dike-breach grids [F6-1], one French river on a 400,000-node mesh [F6-2], Berlin [F6-3], Zurich [F6-4], Houston [F6-5].
- **Transfer to new terrain is not achieved.**
  - Within one synthetic family only [F6-15].
  - Poor outside the training area, improved by fine-tuning [F6-16].
  - "Generalizability to terrain is not yet fully achieved" [F6-17].
  - One holdout domain [F6-18].
  - The newest GNN tested on a real Dutch area needed fine-tuning on a local simulation (R).
- **Authors' own limits:** the SWE-GNN "cannot yet completely replace numerical models" [F6-24]; the French study leaves map validation as future work [F6-25].
- **Compute:** from one GPU for small models to 8 A100 GPUs for the mesh model [F6-11, F6-12, F6-14].
- **Pretrained models:** two sets of public weights exist, for synthetic 100 m grids [F6-21] and for 1 m urban rain flooding in Swiss cities [F6-22]. A pretrained river-flood model that could be pointed at Galați was not found (an absence, claims F6-20 and F6-23 were `unsupported`).
- **Verdict:** roadmap, after a hydrodynamic model exists. ML is also outside the plan.

## What could not be used
- **F1:** claims 16 (wrong version), 17 (wrong figures), 19 (misread paper), 21 (advisory-flag history), 27 (quote about the wrong flag). Claim 14 misquoted, fact confirmed by the reviewer.
- **F2:** claim 6 (the reference is not independent, and the wording is stronger than the paper).
- **F3:** claims 7, 8, 9, 14 (`unsupported`), 21 (`misquoted`, facts stand), 2 and 12 (`unreachable`: GloFAS minimum catchment sizes).
- **F4:** claims 7, 11, 12, 17, 24 (`unsupported`), 8 and 14 (`misquoted`), 19, 20, 22 (`unreachable`: Law 179/2022, the RO-FLOODS III tender, ICPDR maps).
- **F5:** claims 2, 6, 9 (`unsupported`), 5, 16, 20, 23, 24 (`unreachable`: input list, the "Super Model" paper, HEC-RAS licence, TELEMAC, the lower Siret and Prut studies).
- **F6:** claims 6, 20, 23 (`unsupported`), 13 (`misquoted`, numbers right).

## Where sources disagree
- **JRC flood maps licence:** README says ODbL v1.0; `copyright.txt` (European) says CC BY 4.0 [F4-6]; Earth Engine (global) says "without restriction on use or distribution" [F3-19].
- **GloFAS v5:** the data store page says "Operational version - GloFAS v5.0 released 2026-07-15" [F3-1]; the wiki, edited 22 Oct 2026, still gives the release as "2026 (TBD)" (R). Most likely only the reanalysis is out.
- **GFM tie rule:** unflooded per the definition document's table, flooded per its worked example and per the consortium's review [F1-13].
- **RO-FLOODS scope:** the World Bank says the methods covered fluvial, flash, pluvial and coastal flooding; ANAR said in 2014 that the maps show river overflow only [F4-16].
- **LISFLOOD-FP licence:** GPL v3 in the papers, "GPL v2.0 only" in the Zenodo record, and "non-commercial, research code" on the Bristol page [F5-1, and (R)].

## Open after this round (no follow-up was run)
- Were pre-April-2025 GFM STAC items reprocessed with v4.0? Why are advisory layers missing on some passes? (ask the GFM helpdesk)
- Tupas et al. 2024 and Moya et al. 2019 in full; the JRC quality reports for 2024 and 2025.
- JRC European maps: GeoTIFF header over Galați, nodata value, minimum river size in v3, and which licence governs.
- RO-FLOODS: licence, download, grid, scenarios and flood types (ask ANAR; read the World Bank 2024 report).
- Terms of ASF HyP3 products and of CLCplus Backbone.
- Daily Siret and Prut discharge and defence geometry from ANAR / INHGA.

## Follow-up round, 23 Nov 2026
Three flood files, each reviewed by a fresh reviewer: FU1 [worldcover-accuracy.md](worldcover-accuracy.md), FU2 [cems-commercial-use.md](cems-commercial-use.md), FU3 [agricultural-false-alarms-per-algorithm.md](agricultural-false-alarms-per-algorithm.md). Same tags as above: `[FU1-1]` is claim 1 of FU1, marked verified.

### WorldCover accuracy (decision 3, field A)
- **"About 77 %" is a correct citation, of the wrong number for our use.** WorldCover 2021 v200 reports 76.7 % global overall accuracy (2020 v100: 74.4 %) [FU1-1]. It is averaged over all classes worldwide and says nothing about cropland near Galați.
- **Cropland and Europe figures are weak.** One multi-product comparison gives WorldCover 2021 cropland a user's accuracy of 80.6 %, with no region given [FU1-4]. A one-author tutorial for Ireland finds 66.4 % overall against LUCAS points [FU1-5] (verified, but little weight). (R): Venter et al. 2022 (peer-reviewed) found 71 % in Europe for WorldCover 2020, with grassland over-mapped. That bears on the cropland-vs-grassland split of the real flood (48.6 % / 50.4 %, ours).
- **The 20-point rule stands as fixed on 18 Nov,** before the 20 Nov run. FU1's suggestion to re-justify it "from the two test cases" would pick a threshold from its own test data, and the reviewer rejected it. Keep the rule as it is, and write "global overall accuracy 76.7 %; cropland accuracy in this area not checked" wherever map accuracy is mentioned.
- **LCFM** (the 10 m successor) reports 80.1 % overall for 2020, on a different validation sample [FU1-6]. It has an open Copernicus licence [FU1-7], and no 2024 map was found [FU1-8]. **Roadmap, not a swap before 29 Nov:** "drop-in replacement" has no source.
- **Still needs a person:** the cropland and Europe rows of the WorldCover validation report (PVR V2.0) blocked both the researcher and the reviewer.

### GFM in a commercial product (licence)
- **The texts allow reuse and adaptation, and say nothing about "commercial".** Regulation 2021/696 Art. 53(1)(a) and Delegated Regulation 1159/2013 Arts. 3, 4, 7 grant free, worldwide reproduction, distribution, adaptation and combination, "in so far as it is lawful" [FU2-1 – FU2-4, FU2-6]. The CEMS terms name GFM [FU2-9], grant the same uses free of charge and never use the word "commercial" [FU2-10]. IP in adaptations belongs to their creators [FU2-12].
- **Conditions:** name the source, imply no EU endorsement, say when data was modified [FU2-5, FU2-11]; information only, not an early warning, "as is", damage claims waived [FU2-13]. For our per-pixel count: "Contains modified Copernicus Emergency Management Service information [year]" [FU2-11].
- **Wording for the pitch:** "free to reuse, adapt and combine under the CEMS terms". Not "commercial use explicitly allowed": no CEMS sentence says so [FU2-18 is `unsupported`; the Land Monitoring Service's explicit "including commercial" applies only to its own data (R)].
- **Cite** the readable copy of the terms, https://ewds.climate.copernicus.eu/licences/terms-of-use-cems (rev. 11, names GFM) (R), rather than the PDF.
- **Applies to GFM only.** The fallback pipeline runs on Earth Engine, whose free tier is non-commercial (constraints.md).
- **Still worth asking the helpdesk:** one explicit sentence on commercial use, and which year goes in the notice. This is a reading of the texts, not legal advice.

### Farmland false alarms per algorithm (decision 2)
- **No per-algorithm cropland numbers exist** in anything opened. The only study that promises a per-algorithm evaluation is an EGU 2026 abstract with no results [FU3-10].
- **Tupas 2024:** the TU Wien algorithm only, on 2023 data at seven sites, none in Romania [FU3-4, FU3-6]. A different no-flood reference lowered false positives at most sites [FU3-5]. Reviewer: it may describe TU Wien settings that later changed, and its references are SAR-derived.
- **Moya 2019:** change-detection misclassifications on farmland [FU3-1, FU3-2], but on rice paddies in July, not dry tilled soil; no accuracy figures [FU3-3].
- **Physics:** calm water and dry, smooth bare ground both give very low C-band backscatter, so one absolute threshold can't separate them [FU3-15]. A same-orbit before/after comparison and a static exclusion mask are the named remedies [FU3-16]. "Tilled, therefore dark" has no source: rougher ground scatters more (reviewer).
- **What it predicts for the exploration run (FU3's inference, not a source):** all three algorithm designs are documented to over-detect on farmland, so no algorithm is likely to meet the stop rule. The stop rule is fixed; this changes nothing about it.
- **A flaw in how the stop rule is measured (reviewer, confirmed in the code):** `checks/per_algorithm/explore.py` counts "seen" from the **ensemble** layer only (line 66). An algorithm with no data on part of the polder flags less area there just by being absent, so it can meet "less than half" without detecting anything better. The lead's call before the run: restrict the comparison to pixels where all three algorithms have valid data, or read the `flood_members` column and treat partial coverage as `unknown`.
- **Also:** a rule passed on v3 scenes doesn't carry over to v4 (decision 1b), and the per-algorithm layers are intermediate outputs whose licence for product use nobody has checked.
