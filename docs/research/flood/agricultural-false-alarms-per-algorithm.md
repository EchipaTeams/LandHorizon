# What does published work say about Sentinel-1 flood false alarms over agricultural land (bare, tilled, smooth or dry soil), per algorithm type, and for the three GFM algorithms (DLR, LIST, TU Wien)?
Date: 2026-11-23
Scope: In: Tupas et al. 2024 and Moya et al. 2019; any per-algorithm GFM comparison; tested fixes against an independent reference; the physics in brief. Out: modelled hazard, ML beyond a mention, non-SAR sensors except as reference. Claims already `verified` in `gfm-spring-false-alarms.md` and `cross-checks-optical-sar-landcover.md` are cited by number ("GFM-n", "XC-n"), not redone.

Method note for reviewers: my fetch tool returns a summariser's answer, not raw page text, and it limits quotes to 125 characters. Every quote below is a short string the tool returned as a quotation; a reviewer should re-check each against the page. I had no PDF renderer: the PDFs the tool saved locally (Tupas thesis, DLR review, Roth slides, AM2025 slides) could not be read. A text-extraction proxy request (r.jina.ai) was denied by the permission system, so I did not use it.

Headline: **both blocked papers are still not read in full text.** For both I have the abstract only (via Crossref and the TU Wien repository record), so no agricultural false-alarm numbers from either. **No per-algorithm numbers on cropland false alarms for DLR, LIST or TU Wien were found anywhere.**

## Claims

### A. The two papers that were blocked
1. **Claim:** Moya et al. 2019 (Remote Sensing 11(19), 2320; Western Japan floods 2018, Sentinel-1) found that SAR change detection produced significant misclassifications on farmland. The abstract blames three factors, one of which is using a single before/after image pair.
   - Source: https://api.crossref.org/works/10.3390/rs11192320 (Crossref record of the paper; the MDPI page returned HTTP 403)
   - Quote: "During the 2018 Western Japan Floods, the change detection method generated significant misclassifications for agricultural targets."
   - Source date: 2019-10-05
   - Source type: peer-reviewed (abstract only, read through Crossref metadata)
   - Confidence: medium (abstract; the full text was not opened)
2. **Claim:** Moya et al. name two further causes (backscatter behaviour of farmland over time, and the radar wavelength) and support them with a field survey of 35 paddy fields. The targets are paddy fields in Japan, not tilled dry soil. The abstract gives no accuracy numbers.
   - Source: https://api.crossref.org/works/10.3390/rs11192320
   - Quote: "(iii) The effect of the wavelength on agricultural targets."
   - Source date: 2019-10-05
   - Source type: peer-reviewed (abstract only)
   - Confidence: medium. Related quotes returned by the tool: "Our conclusions are supported by a field survey of 35 paddy fields located within the misclassified area" and "(i) The use of only a single pair of SAR images from before and after the floods." The abstract does not state which wavelength or direction (it mentions neither L- nor C-band).
3. **Claim:** Moya et al. propose "conditional coherence" as a fix and report its use as input to discriminant functions for flooded vs non-flooded agriculture. The abstract gives no precision, recall or commission figure. Needs two or more SAR acquisitions and coherence, so it is not a GFM-layer fix.
   - Source: https://api.crossref.org/works/10.3390/rs11192320
   - Quote: "The performance of the conditional coherence as an input of discriminant functions to identify flooded and non-flooded agricultural targets is reported as well."
   - Source date: 2019-10-05
   - Source type: peer-reviewed (abstract only)
   - Confidence: medium for what was proposed; numbers: not found
4. **Claim:** Tupas et al. 2024 (GIScience & Remote Sensing 61(1), doi 10.1080/15481603.2024.2427304) analyse false positive rates of the TU Wien Bayesian algorithm (the algorithm inside GFM) on non-flooded scenes, and say their analysis "highlights issues with agricultural overestimation". Abstract gives no figure for agriculture.
   - Source: https://repositum.tuwien.at/handle/20.500.12708/206671?mode=full (repository record; open-access full-text PDF at https://repositum.tuwien.at/bitstream/20.500.12708/206671/1/Tupas-2024-GISCIENCE%20%20REMOTE%20SENSING-vor.pdf was too large for my fetch tool, over 10 MB)
   - Quote: "highlights issues with agricultural overestimation"
   - Source date: 2024-12-01 (published online)
   - Source type: peer-reviewed (TU Wien authors, the algorithm's own group; abstract only)
   - Confidence: medium (abstract only). Related returned quotes: "Our time-series analysis confirms increased false positive rates due to well-known environmental drivers" and "we analyze the false positive rate of the corresponding flood maps generated".
5. **Claim:** The tested fix is a different no-flood reference for the TU Wien algorithm (an exponential filter replacing the harmonic model). It lowers false positives on non-flooded scenes at most sites, struggles on sites with prolonged floods, and is scored against CEMS and Sentinel Asia semi-automatic maps. So it is a change inside one algorithm, not something a GFM user can apply; the abstract does not say it removes the agricultural cases specifically.
   - Source: https://repositum.tuwien.at/handle/20.500.12708/206671?mode=full
   - Quote: "effectively reducing false positive rates on non-flooded scenes in most study sites"
   - Source date: 2024-12-01
   - Source type: peer-reviewed (abstract only)
   - Confidence: medium. Reference: "semi-automatic results from Copernicus Emergency Management Services and Sentinel Asia as a reference" (these are SAR-derived with manual edits, so not an independent sensor, see XC "missed" and GFM review item 6).
6. **Claim:** The sites of the Tupas 2024 analysis (companion dataset): Scotland, Vietnam, Greece, Slovenia, India, Philippines, Latvia. Romania is not among them; the Danube lowland near Galați is not represented.
   - Source: https://researchdata.tuwien.ac.at/records/3dd60-ydz51
   - Quote: "False Positive Rate_ time-series analysis in CSV format"
   - Source date: 2024-04-23 (record shows "Published April 23, 2024 | Version 1.0.0" in search result)
   - Source type: official docs (data repository record, CC BY 4.0)
   - Confidence: low-medium (the site list comes from the tool's summary of the page; the quote only shows the FPR analysis is published as CSV, so the per-site FPR numbers exist but I did not open them: not found)
7. The PhD thesis version (Tupas 2024, https://repositum.tuwien.at/bitstream/20.500.12708/209576/1/Tupas%20Mark%20Edwin%20-%202024%20-%20Improving%20flood%20monitoring%20capabilities%20using...pdf) has chapter 4 with the same title as the paper. My fetch returned only the outline and saved the 5.2 MB PDF; I could not read the body. Not cited.

### B. Per-algorithm and GFM-specific evidence
8. **Claim (already verified, see GFM-4, GFM-5):** The GFM consortium review calls agricultural/grassland over-detection the most problematic service case, says advisory flags are typically not raised for it, and gives no false-positive rate. Cite as GFM-4 and GFM-5.
   - Source: https://elib.dlr.de/218412/1/1-s2.0-S0034425725005127-main.pdf (Wagner et al., Remote Sensing of Environment, doi 10.1016/j.rse.2025.115108)
   - Quote: "Probably the most problematic case from a service point of view is overdetection in agricultural and grassland areas" (as recorded and verified in GFM-5; I could not reopen the PDF this time)
   - Source date: 2025
   - Source type: peer-reviewed (consortium authors, not independent)
   - Confidence: high (verified by the earlier review)
9. **Claim (already verified, see GFM-15):** The same review says the time-series algorithm is also affected by agriculture, because its harmonic model cannot represent crop rotation, and the single-image algorithm is too. It says nothing on a residual LIST weakness. Cite as GFM-15. Tupas 2024 (claim 4) is the TU Wien group's own confirmation for that algorithm.
   - Source: https://elib.dlr.de/218412/1/1-s2.0-S0034425725005127-main.pdf
   - Quote: "Not only the single-image algorithm is impacted, but also time-series algorithm" (as recorded in GFM-15)
   - Source date: 2025
   - Source type: peer-reviewed (consortium)
   - Confidence: medium
10. **Claim:** The only study found that says it evaluates the three GFM algorithms individually for misdetections and false alarms is an EGU 2026 abstract (Garg et al., Cambridge). It publishes no per-algorithm result, does not name DLR, LIST or TU Wien, and says nothing about agriculture.
    - Source: https://meetingorganizer.copernicus.org/EGU26/EGU26-21734.html
    - Quote: "We evaluate the three-underlying flood-mapping algorithms individually for consistent patterns of misdetection"
    - Source date: 2026-03-14 (abstract update date; EGU General Assembly 3-8 May 2026)
    - Source type: preprint (conference abstract)
    - Confidence: medium that the study exists and what it promises; results: not found
11. **Claim:** The v4.0 release (mid-April 2025) changed the post-processing of all three algorithms, but the consortium's own average change was a slightly higher commission error, and the list of remaining issues includes agriculture. Per-algorithm detail (LIST HAND-based filtering of flood objects, TU Wien larger minimum mapping unit, DLR region growing and fall-back thresholds) reached me only through a search summary of the Roth et al. slides and the news item, which I could not open (the slide PDF returned binary, the news page returned only its title). The GFM review in GFM "missed" item 1 already records, from the reviewer's own reading of these slides, "Commission error: + 2.11" and "Remaining issues in certain land cover types and agriculture overestimation". I do not cite per-algorithm v4 changes; a per-scene DLR threshold: not found in anything I opened.
    - Source: https://global-flood.emergency.copernicus.eu/media/events/8/8-roth_florian_globalflood25_gfmnewmajorversion.pdf (reviewed in `gfm-spring-false-alarms.md` Review, "missed" item 1)
    - Quote: "Remaining issues in certain land cover types and agriculture overestimation" (as quoted by the earlier reviewer; not reopened by me)
    - Source date: 2025-04
    - Source type: official docs (consortium slides)
    - Confidence: low-medium (second-hand for me)
12. **Claim (already verified, see GFM-12, GFM-13):** DLR is single-image, LIST dual-image change detection against a recent same-orbit scene, TU Wien a harmonic time-series model with Bayesian inference; the ensemble is a majority of the contributing algorithms. Cite as GFM-12 and GFM-13. The tie rule is contradictory in the sources (GFM-13).

### C. Fixes tested against a reference
13. **Claim:** I found no study that tests a fix for tilled-field or bare-soil false alarms against an independent reference and reports precision and recall or commission error for cropland. The nearest are: (a) Dasgupta et al. (EGU21, arid Ghana and Congo), reporting "50% false positive reductions over traditional Otsu approaches" and ">20%" CSI gains, from Sentinel-2 SAVI-based harvested-cropland screening; (b) Tupas 2024 (claim 5), an exponential filter in the TU Wien algorithm; (c) Moya 2019 (claim 3), conditional coherence. Each is partly or not independent, abstract-level, or on paddy/arid land.
    - Source: https://meetingorganizer.copernicus.org/EGU21/EGU21-6982.html
    - Quote: "First results demonstrated 50% false positive reductions over traditional Otsu approaches"
    - Source date: 2021-04 (vEGU21, 19-30 April 2021)
    - Source type: preprint (conference abstract; authors from Cloud to Street, a flood-mapping vendor; reference includes "expert classified Sentinel-1 SAR-based flood maps" as well as "Sentinel-2 clear view coincident optical maps")
    - Confidence: low (see XC-1 and its review: partly independent reference, not peer-reviewed)
14. **Claim:** A one-year Bayesian time-series baseline scored precision 0.52, recall 0.46 at Nova Kakhovka, with the authors suspecting crop growth and harvest. Cited by restatement in the earlier file; see XC-6 (`unsupported` as originally worded; use the reviewer's restatement). Not a fix test.

### D. The physics, in brief
15. **Claim:** Calm water and dry smooth bare ground both give very low C-band backscatter, so one absolute threshold cannot separate "dark because wet" from "dark because smooth and dry". Support from two sources: the Copernicus Data Space support team and the EGU21 abstract.
    - Source: https://forum.dataspace.copernicus.eu/t/s1-flood-mapping-arid-land-false-positives/5460
    - Quote: "Calm water and dry, smooth arid ground (bare soil, sand, sparse shrubland) both return very low C-band backscatter"
    - Source date: 2026-08-31
    - Source type: official docs (CDSE support-team forum reply; not peer-reviewed)
    - Confidence: medium. Second source: https://meetingorganizer.copernicus.org/EGU21/EGU21-6982.html, quote "since dry and smooth desert sand appears as dark as water in SAR images." (2021, conference abstract, low-medium). Both speak of arid ground; neither mentions freshly tilled temperate fields. The link from "tilled" to "smooth" is an inference (a harrowed, fine-seedbed field is smooth at C-band wavelength scale), not a quote I opened.
16. **Claim:** Cues the opened sources name for separating the two: a same-orbit pre-event vs during-event comparison instead of one absolute threshold, and a static exclusion mask built from a short pre-event time series for pixels that stay dark; Moya's abstract points to farmland's backscatter behaviour over time and to coherence.
    - Source: https://forum.dataspace.copernicus.eu/t/s1-flood-mapping-arid-land-false-positives/5460
    - Quote: "change-detection approach (pre- vs. during-event, same orbit)"
    - Source date: 2026-08-31
    - Source type: official docs (support reply)
    - Confidence: low-medium. A change-detection baseline is exactly what Moya's 2019 abstract says failed on farmland when only one image pair was used (claim 1), and what TU Wien says fails on crop rotation (claim 9): both predate/follow different tillage states. VH, incidence angle: not found in any source I could open as a tested cue for tilled fields (a search summary mentioned VH-vs-VV disagreement between sources; I did not open them, so I do not cite it).

## Relevance to LandHorizon
The stop rule is fixed (continue only if one algorithm flags less than half the ensemble's area on both dates while keeping at least 80 % of the ensemble's detections inside a real-flood outline). **Nothing here changes it.** This section only sets expectations. "Sourced" means a claim number above; "inference" is mine.

- **What the literature predicts (sourced):** all three algorithm types are documented to over-detect on agriculture: single-image (GFM-9), time-series harmonic (GFM-9, claim 4), and change-detection with one reference pair (Moya, claim 1; LIST is a recent-same-orbit change detector, GFM-12). No source ranks them, none gives per-algorithm cropland false-alarm numbers (claims 10, 13), and the consortium's own list of remaining v4 issues still includes agriculture (claim 11).
- **Is any algorithm likely to meet the stop rule? (inference):** the literature gives no reason to expect one to. Reasons: (a) the shared error source (smooth tilled soil, claim 15) affects all three designs; (b) a change-detection algorithm such as LIST compares with an earlier scene, and a field tilled between the reference scene and 30 Apr should look like a backscatter drop, which is Moya's failure mode; (c) a harmonic model (TU Wien) cannot know about tillage timing (GFM-9). Weak counter-possibility: the three designs differ in reference and thresholds, so their errors need not coincide pixel by pixel, and nobody has published the comparison. That is what the run measures.
- **A logic check on the rule (inference, assumes plain 2-of-3 voting for April 2024 scenes, with the tie rule uncertain, GFM-13):** every ensemble flood pixel was flagged by at least two algorithms. If algorithm A flags under half of the ensemble area, then B and C must both flag everything A did not, i.e. more than half. So the first half of the rule can pass only if the other two algorithms agree with each other over most of the false area. Whether the fields are flagged by the "pair" in common is therefore the real question; one algorithm being clean would still leave the remaining two agreeing on the error. Then the second half (80 % of detections inside a real-flood outline) is a different test, on an event where a real flood exists.
- **Pipeline (not a decision):** if the run did pass, using a single algorithm's layer (`dlr_flood_extent`, `list_flood_extent` or `tuw_flood_extent` in STAC, GFM-11) would be our own method on top of GFM and would bump `ALGORITHM_VERSION`; it would also lose the majority vote's protection against other error types. A Tupas-style exponential-filter reference is a change inside TU Wien's code, not available to us; running it ourselves means our own pipeline on Sentinel-1 time series (new compute, not free of cost in team time).
- **Data access, licence, cost, compute:** all sources cited are open (Crossref, TU Wien repository CC BY 4.0 for Tupas 2024 PDF, EGU abstracts). No new data is implied by this file. GFM per-algorithm layers: already free in STAC (GFM-11); licence "other" / CEMS terms (GFM review "missed" item 7).
- **Coverage of our area:** Tupas 2024 sites do not include Romania (claim 6); Moya is Japanese paddy fields; Dasgupta is arid Africa. Nothing found tests the Danube lowland near Galați. Treat all as indirect.
- **Wording for the report:** "Over-detection on agricultural land is a documented, unresolved limit of GFM's own algorithms (consortium review, GFM-5), with no published per-algorithm cropland false-alarm rate" is supported. Do not write that any algorithm is cleaner.

## Open questions
- Full text of Tupas 2024 (PDF over 10 MB for my fetch tool; open access at the repositum URL in claim 4) and its per-site FPR CSV in https://researchdata.tuwien.ac.at/records/3dd60-ydz51: do they give agricultural FPR numbers, and for which sites? A reviewer with a PDF reader should open them.
- Full text of Moya 2019 (MDPI 403, DOAJ 403, proxy denied): did the field survey give a misclassification rate, and which band/wavelength reasoning does it use? Not found.
- Alonso-Sarria et al. (SE Spain, Sentinel-1 vs Sentinel-2, https://digitum.um.es/digitum/bitstream/10201/155820/1/AlonsoSarria_etal.pdf) returned 403; may hold commission figures on cropland. Unopened.
- The 2026 Garg et al. results (per-algorithm misdetections) when published.
- Per-algorithm v4 changes (LIST HAND filter, TU Wien patch filter, DLR threshold): slide PDFs and the EODC versioning page were unreadable to me; the PDD v4.0 (https://extwiki.eodc.eu/gfm_assets/gfm_pdd_v4_0.pdf) section 3 should be read directly.
- Tested VH and incidence-angle cues for tilled soil: not found in opened sources.
- Out of scope, one line: the SWIM deep-learning replacement planned for 2027 (GFM-20).

## Untrusted content
No fetched page contained instructions addressed to me. One tool call (a text-extraction proxy request for the MDPI page) was denied by the permission system and was not retried.

## Review
Reviewer date: 2026-11-23. Reviewer did not write this file.

Method limit: my fetch tool also returns a summariser's answer, so each quote was checked by an exact-string question ("does this string appear word for word"), not by reading the page by eye. PDFs could not be read: the DLR review PDF and the Roth slide PDF came back as binary, and the local PDF reader failed (no renderer installed). The EODC ensemble wiki page returned only its title. Claims that rest only on those sources are `unreachable` for me, even where the earlier review (`gfm-spring-false-alarms.md`) verified them by another route.

Count: 10 `verified`, 1 `unsupported`, 0 `misquoted`, 4 `unreachable`. Item 7 is not a claim (nothing cited) and gets no verdict.

### Verdicts
1. `verified`. Crossref abstract has the sentence word for word. The abstract lists three causes, (i) to (iii); "single pair" is (i). Title: "Drawback in the Change Detection Approach: False Detection during the 2018 Western Japan Floods"; published online 2019-10-05.
2. `verified`. "(iii) The effect of the wavelength on agricultural targets." and the 35-paddy-field sentence and (i) are all exact. No band named, no accuracy figure: confirmed.
3. `verified`. Sentence exact. No precision, recall or commission figure in the abstract.
4. `verified`. All three quotes are in the reposiTUm abstract word for word. GIScience & Remote Sensing 61(1), doi 10.1080/15481603.2024.2427304, online 2024-12-01, CC BY 4.0. The abstract says the analysis uses 2023 time-series data (see "missed" item 1).
5. `verified`. Both quotes exact. The abstract also reports better CSI and user's accuracy in most flooded scenes and says the filter struggles with prolonged flooding. Nothing in the abstract ties the reduction to agricultural pixels.
6. `verified`. The quote is on the page (as "_False Positive Rate_ time-series analysis in CSV format", listed under validation results). The seven sites are on the page; no Romania. Published 23 Apr 2024, v1.0.0, CC BY 4.0. Two notes: `fp_counts.tar.gz` (1.4 GiB) is "false positive count maps", not per-site rates; that the FPR CSV is split per site is likely but not stated. The page names no land-cover classes, so agricultural FPR is not given there either.
7. No verdict (not cited).
8. `unreachable`. The DLR PDF came back as binary. The earlier review recorded the quote as present in section 4.5; I could not re-check it.
9. `unreachable`. Same PDF. The earlier review verified the quote and "cannot account for crop rotation practices" (GFM-15).
10. `verified`. String exact; the sentence continues "or false alarms". Authors Garg, He, Selvakumaran, Borgomeo (Cambridge, NTU Singapore); page updated 14 Mar 2026; session HS6.5. No DLR, LIST, TU Wien or agriculture on the page.
11. `unreachable`. Slide PDF came back as binary for me too. The quote matches what the earlier reviewer recorded ("missed" item 1 of `gfm-spring-false-alarms.md`), but the claim's other parts ("changed the post-processing of all three algorithms") rest on search summaries.
12. `unreachable`. No source of its own; it restates GFM-12 and GFM-13, whose sources (DLR PDF, EODC ensemble wiki page) I could not read. The earlier review verified both, with the tie-rule contradiction.
13. `unsupported` as worded. The quote is exact, and so are ">20%" CSI and the two reference types. But the abstract credits the 50 % reduction to the whole S1-L1 algorithm (Landsat water history, backscatter land classification, a "flood plausibility" post-processing layer, plus the SAVI harvested-cropland step), compared with Otsu and a deterministic sand exclusion layer. It does not credit the reduction to "SAVI-based harvested-cropland screening". It also does not say which reference (expert Sentinel-1 maps or Sentinel-2 maps) produced the figures. Usable restatement: "S1-L1 (arid Ghana and Congo, vendor authors) reports about 50 % fewer false positives than Otsu and >20 % higher CSI. One of its steps flags harvested cropland with low Sentinel-2 SAVI. Which reference produced the figures is not stated." The "no study found" part is a search result, not a sourced statement.
14. `verified`. arXiv 2504.19526v4 Table 3: BCP at Nova Kakhovka P 0.52 / R 0.46 / F1 0.49 (IoU 0.36). The baseline is "one year before the event" (3.1.2). The harvest sentence is hedged ("appears related to"). The restatement follows XC-6's review. Keep the note that the labels (UrbanSARFloods) are not from an independent sensor.
15. `verified`. CDSE quote exact, in the support team's reply of 31 Aug 2026. The thread is about VH auto-thresholding over arid western US shrubland. EGU21 quote exact. "Official docs" is generous: it is a support-forum reply, not documentation. The researcher flags the tilled-to-smooth step as an inference, and that is right; see "missed" item 3.
16. `verified`. Quote exact. The static exclusion mask from a short pre-event series of persistently low pixels is in the same reply. The reply also recommends terrain-corrected gamma0 for slopes, which is not relevant to the flat polder.

### What the researcher missed
1. **Tupas 2024 may describe a superseded TU Wien setup.** Its abstract says the comparison uses 2023 time series. The PDD says that for v3.x "the harmonic parameters were updated, to improve accuracy over agriculture" (the earlier review's item 23 verified this; v3.0.0 went live 24 Jan 2024). Our 30 Apr 2024 scenes are v3. Not found: which harmonic parameters Tupas used. Until the full text is read, its FPR results may not describe the TU Wien layer we would test.
   - https://repositum.tuwien.at/handle/20.500.12708/206671?mode=full
   - https://extwiki.eodc.eu/gfm_assets/gfm_pdd_v4_0.pdf (via the earlier review, not opened by me)
2. **Moya's farmland is rice paddy during a July flood season.** The misclassified targets were paddy fields (claim 2), which are often irrigated or under crop in July. That mechanism is not dry, freshly tilled soil. The Relevance section uses Moya as support for LIST's likely failure on tilled fields (reason b). That stretches an abstract-only, paddy-field result.
   - https://api.crossref.org/works/10.3390/rs11192320
3. **Roughness cuts both ways.** "The rougher the surface, the higher the copolarized backscatter" (Esri SAR flood-mapping guide). A freshly ploughed field is rough and should be bright; only a harrowed or rolled fine seedbed is smooth. So "tilled, therefore dark" depends on the tillage stage on 30 Apr, and no opened source links the two. This weakens reason (a) in Relevance, which treats smooth tilled soil as a shared error source on the strength of claim 15 (arid ground only).
   - https://doc.esri.com/en/arcgis-pro/latest/help/analysis/image-analyst/interpret-sar-data-for-flood-mapping.html
4. **Dasgupta et al. is vendor work with no independent validation.** The authors are from Cloud to Street PBC, it is a conference abstract, and part of the reference is "expert classified Sentinel-1 SAR-based flood maps" (same sensor).
   - https://meetingorganizer.copernicus.org/EGU21/EGU21-6982.html

### Problems in "Relevance to LandHorizon"
- **Wrong cross-reference.** The section cites GFM-9 for "single-image" and "time-series harmonic" over-detection, and for "cannot know about tillage timing". GFM-9 is the likelihood-threshold claim (0.3). The right reference is GFM-15, and it says "crop rotation", not tillage timing; tillage timing is the researcher's inference. Source: https://elib.dlr.de/218412/1/1-s2.0-S0034425725005127-main.pdf (via GFM-15)
- **"Sourced" labels on inferences.** The first bullet links Moya (claim 1) to LIST (GFM-12) as sourced. That link is an inference: Moya did not test LIST, and its targets were paddies ("missed" item 2). Reason (a) rests on claim 15, which is about arid ground ("missed" item 3).
- **The logic check leaves out missing inputs.** The 2-of-3 argument assumes all three algorithms are valid on every pixel. Before Nov 2024, when only two algorithms report, the ensemble uses consensus (wiki entry of 2 Jan 2023, per the earlier review), so an algorithm with no valid input on the polder (for example LIST without a recent same-orbit reference scene) would meet the "less than half" condition by absence, not by being cleaner. The brief's "seen pixels only" rule should be confirmed to mean pixels where all three algorithms are valid. This links to the held-out brief's rule that fewer than three valid algorithms counts as `unknown`. Sources: https://extwiki.eodc.eu/GFM/GFMVersioning ; `docs/research/briefs/2-held-out-test.md` lines 97 and 109.
- **Version boundary not carried into the pipeline bullet.** Claim 11 says v4.0 changed the post-processing (and that claim is itself `unreachable`). The earlier review records "GFM Layers produced from different MAJOR versions can not be used in unison". A single-algorithm rule passed on 2024 (v3) scenes would not carry over to v4 scenes in a 2015-2025 batch without a re-check. Source: https://extwiki.eodc.eu/GFM/GFMVersioning
- **Licence and product status.** Per-algorithm layers are labelled "Intermediate output" in STAC (GFM-11). The CEMS terms do not address commercial use (earlier review, "missed" item 7). `constraints.md` requires a product-use licence check, so this is still open, not "already free". Sources: https://stac.eodc.eu/api/v1/collections/GFM ; https://global-flood.emergency.copernicus.eu/terms-of-service/
- The stop rule as stated matches `docs/research/briefs/2-held-out-test.md` (lines 104-108). The section rightly says it does not change it. The report wording in the last bullet rests on GFM-5 (verified in the earlier review, `unreachable` for me) and on negative search results. That is acceptable as "none found", not as "none exists".

### Untrusted content
No fetched page or text in this file read as instructions to the reviewer. None were followed.
