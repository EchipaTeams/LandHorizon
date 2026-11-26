# What do GFM and independent studies say about false flood detections on tilled, bare or dry cropland, and can anything inside the GFM product remove them? (F1)
Date: 2026-11-11
Scope: GFM documentation (PDD v4.0, PUM 2025, EODC wiki, STAC), the three algorithms, the ensemble likelihood, validation studies, versions, per-scene layers. Out of bounds: optical cross-checks, SAR cues computed outside GFM, external land-cover masks, modelled hazard, ML.

Method note for reviewers: the EODC wiki is JavaScript-rendered and the PDFs would not open directly. Most PDF text was read through a text-extraction proxy (r.jina.ai) and a small summariser model, which returned the short quotes below. Quotes are as returned; a reviewer should re-check them against the PDFs. The two QA/validation papers marked "consortium" are not independent. I never reached the full text of the 2024 and 2025 JRC QA reports (the JRC site rejected the request) or of Garg et al.

## Claims

### 1. GFM's own documentation: false alarms, advisory flags, accuracy target
1. **Claim:** The User Manual names cropland growing conditions and agricultural practices as a cause of false alarms, because such surfaces have very low backscatter and look like water.
   - Source: https://extwiki.eodc.eu/gfm_assets/gfm4.0_pum_2025.pdf (PUM 2025, section 4.1)
   - Quote: "Certain growing conditions and agricultural practices over cropland."
   - Source date: 2025-12 (cover says V20251201)
   - Source type: official docs (service's own documentation)
   - Confidence: medium (short quote; context sentence "These surfaces and artifacts usually feature very low backscatter signatures and thus appear as water in SAR imagery" was also returned)
2. **Claim:** The advisory flags have only two parts, low regional backscatter (dry soil, frost, snow) and rough water (wind). They are not removed from the maps and only warn users.
   - Source: https://extwiki.eodc.eu/gfm_assets/gfm4.0_pum_2025.pdf (section 3.6)
   - Quote: "Pixels marked by the Advisory Flags are not excluded by the Exclusion Mask."
   - Source date: 2025-12
   - Source type: official docs
   - Confidence: medium
3. **Claim:** The low-backscatter flag is set from a regional comparison (more than 1 dB below the regional monthly median), not per field. The PUM says the flag is buffered by 14 km (rough-water flag 5 km). This is why a locally tilled polder can go unflagged.
   - Source: https://extwiki.eodc.eu/gfm_assets/gfm_pdd_v4_0.pdf (PDD v4.0, section 4.6.1) and PUM 2025 section 3.6
   - Quote: "If this difference exceeds 1 dB, the low backscatter flag is set to value 1"
   - Source date: 2025-10-14 (PDD v4.0)
   - Source type: official docs
   - Confidence: medium (the 14 km buffer figure came from the summariser's paraphrase of the PUM, not a quote)
4. **Claim:** The consortium's own review says advisory flags are typically not raised for over-detection in agricultural areas. This matches our observation (about 40 % flagged).
   - Source: https://elib.dlr.de/218412/1/1-s2.0-S0034425725005127-main.pdf (Wagner et al., Remote Sensing of Environment, doi 10.1016/j.rse.2025.115108; the authors are the GFM consortium)
   - Quote: "Additionally, advisory flags are typically not raised for overdetection in agricultural areas"
   - Source date: 2025
   - Source type: peer-reviewed (consortium authors, not independent)
   - Confidence: high
5. **Claim:** The same review calls agricultural and grassland over-detection the most problematic service case. It says false positives depend on crop type and weather and are worse on dry soils. It gives no false-positive rate figure.
   - Source: https://elib.dlr.de/218412/1/1-s2.0-S0034425725005127-main.pdf (section 4)
   - Quote: "Probably the most problematic case from a service point of view is overdetection in agricultural and grassland areas"
   - Source date: 2025
   - Source type: peer-reviewed (consortium)
   - Confidence: high
6. **Claim:** Stated accuracy target is a Critical Success Index (CSI) of at least 70 %, assessed against independent reference datasets in annual QA reports. A commission-error target of under 5 % (KPI-3d) is listed in a 2025 consortium slide deck.
   - Source: https://extwiki.eodc.eu/GFM/PDD/GFM_quality_assessment and https://global-flood.emergency.copernicus.eu/media/events/8/seewald_michaela_globalflood25_the-global-flood-monitoring.pdf
   - Quote: "Commission Error (KPI-3d, target < 5%)"
   - Source date: 2025
   - Source type: official docs
   - Confidence: medium

### 2. Likelihood and uncertainty layers
7. **Claim:** The ensemble likelihood is the mean of the per-algorithm likelihoods (each rescaled to 0-100), with 50 as the class boundary. Low values in [50, 60] mark classifications without full agreement.
   - Source: https://arxiv.org/pdf/2304.12488 (Krullikowski et al., IEEE JSTARS 2023, doi 10.1109/JSTARS.2023.3292350; GFM consortium authors)
   - Quote: "The ensemble likelihood is computed as the mean of the individual likelihood layers"
   - Source date: 2023
   - Source type: peer-reviewed (consortium)
   - Confidence: high
8. **Claim:** The same paper says dry soil and agriculture on dry soil are known false-flood cases, and its Somalia test claims the consensus rule reduces such over-detection. It offers no tuned likelihood cut-off for removing false alarms.
   - Source: https://arxiv.org/pdf/2304.12488
   - Quote: "Herbaceous vegetation, shrubs and agriculture on dry soil are well-known challenges"
   - Source date: 2023
   - Source type: peer-reviewed (consortium)
   - Confidence: medium
9. **Claim:** Thresholding the likelihood is allowed but not applied by the service, and no study shows it reducing cropland false alarms. The consortium review says only that it "can be easily converted into a binary flood map adapted to local conditions" and gives no values or accuracy effect. One external study (Misra et al. 2025, cited in the review) used a global threshold of 0.3, which scored below a neural network. Our own finding (median likelihood 72 on false flood vs 73 on real flood) says a likelihood cut-off would not separate them. That finding is not in these sources.
   - Source: https://elib.dlr.de/218412/1/1-s2.0-S0034425725005127-main.pdf (section 2.2.4; section 4)
   - Quote: "a tuned global threshold of 0.3 to turn the GFM flood likelihood layer into binary flood maps"
   - Source date: 2025
   - Source type: peer-reviewed (consortium review quoting a third-party study)
   - Confidence: medium
10. **Claim:** No quantitative evaluation of the likelihood layer exists in the review, and the 2023 QA report excluded it from validation.
    - Source: https://civil-protection-knowledge-network.europa.eu/system/files/2024-12/global-flood-monitoring-annual-product-and-service-quality-assessment-report-2023.pdf
    - Quote: "The Likelihood Values of pixels (see Table 1) were not considered."
    - Source date: 2024-12-06
    - Source type: official docs (JRC technical report, GFM consortium)
    - Confidence: medium

### 3. The three algorithms and the ensemble
11. **Claim:** Each algorithm's own flood extent and likelihood is published per scene in the STAC catalogue (asset keys `dlr_flood_extent`, `dlr_likelihood`, `list_flood_extent`, `list_likelihood`, `tuw_flood_extent`, `tuw_likelihood`). The TU Wien one is titled "Uncertainties". They are labelled "Intermediate output".
    - Source: https://stac.eodc.eu/api/v1/collections/GFM
    - Quote: "GFM Observed Flood Extent (Intermediate output - DLR algorithm)"
    - Source date: read 2026-11-11 (no date on the page)
    - Source type: official docs (live catalogue)
    - Confidence: high (asset presence on the collection; whether every scene carries all of them was not checked)
12. **Claim:** Each algorithm works differently: DLR is single-image (tile thresholding plus fuzzy logic), LIST is dual-image change detection against a recent scene of the same orbit, TU Wien is a time-series harmonic model with Bayesian inference.
    - Source: https://elib.dlr.de/218412/1/1-s2.0-S0034425725005127-main.pdf (section 2.2)
    - Quote: "The classification is initialised by an unsupervised hierarchical tile-based thresholding procedure."
    - Source date: 2025
    - Source type: peer-reviewed (consortium)
    - Confidence: medium
13. **Claim:** The voting rule is a majority of the contributing algorithms (at least two of three). Sources disagree on a 1-vs-1 tie: the PDD/wiki say a ratio of 0.5 gives Unflooded; the review says an equal-likelihood tie defaults to flooded. The versioning page records a Jan 2023 change ("ENSEMBLE uses consensus when two algorithms report"), so the rule may have changed over time.
    - Source: https://extwiki.eodc.eu/GFM/PDD/GFM_algorithms/Ensemble_algorithm
    - Quote: "a majority-based consensus rule"
    - Source date: read 2026-11-11 (PDD v4.0 is 2025-10-14)
    - Source type: official docs
    - Confidence: medium (tie handling is contradictory)
14. **Claim:** Since 27 Nov 2024 the ensemble also gives a result when only one algorithm returns valid input. A flood pixel may then rest on one algorithm alone, with no vote.
    - Source: https://extwiki.eodc.eu/GFM/GFMVersioning
    - Quote: "ENSEMBLE produces results when only one algorithm gives valid input."
    - Source date: 2024-11-27 (entry date)
    - Source type: official docs (the quote is the summariser's wording of the entry)
    - Confidence: low-medium
15. **Claim:** No published work found that ranks the three algorithms by bare-soil or cropland false alarms. The review says the time-series (TU Wien) algorithm is also affected by agriculture because its harmonic model cannot represent crop rotation. It says the single-image algorithm is affected too. For LIST it claims improved detection of backscatter reduction from vegetation and dry soils but gives no residual weakness. The review says the three algorithms "agree very well" outside flood edges.
    - Source: https://elib.dlr.de/218412/1/1-s2.0-S0034425725005127-main.pdf (sections 2.2, 3.1, 4)
    - Quote: "Not only the single-image algorithm is impacted, but also time-series algorithm"
    - Source date: 2025
    - Source type: peer-reviewed (consortium)
    - Confidence: medium. Implication, not a source finding: if all three share the error, their individual layers cannot outvote it. Whether they differ on our 30 Apr 2024 scenes can be checked directly, since the layers are in STAC.

### 4. Validation studies
16. **Claim:** Consortium global validation (v3.2.0 archive): flood overall accuracy 72.0 %, flood CSI 43.7 %, below the 70 % target. By environmental zone CSI runs from 36.2 % (hot and arid) to 74.2 % (extremely hot and moist). The review reports only OA and CSI (no precision, no land-cover split) and its own text says the target "had not yet been reached".
    - Source: https://elib.dlr.de/218412/1/1-s2.0-S0034425725005127-main.pdf (Table 6, Table 7, section 3.6)
    - Quote: "the accuracy target had not yet been reached for the investigated archive version"
    - Source date: 2025
    - Source type: peer-reviewed (consortium, not independent)
    - Confidence: high for the sentence; medium for the figures (summariser-read tables)
17. **Claim:** The JRC 2023 QA report (12 use cases, v2.1.0) found CSI from 11.0 % to 81.1 %. Its agricultural findings are mostly omissions (Greece, Italy, India rice, topographic-distortion mask over farmland), not false alarms. It names no tillage or bare-soil false alarms.
    - Source: https://civil-protection-knowledge-network.europa.eu/system/files/2024-12/global-flood-monitoring-annual-product-and-service-quality-assessment-report-2023.pdf
    - Quote: "The vast majority of the omitted flood extent occurred in agricultural fields."
    - Source date: 2024-12-06
    - Source type: official docs (JRC technical report; GFM consortium; references were made by the consortium's own interpretation)
    - Confidence: medium
18. **Claim:** Independent, event-based study (Cambridge) of 20 events: GFM does well on large floods and worse on small, local ones; many errors come from the reference water layer, which causes false alarms and missed floods. No cropland statement in the abstract.
    - Source: https://meetingorganizer.copernicus.org/EGU26/EGU26-21734.html (Garg et al., EGU26 abstract)
    - Quote: "misclassification of permanent or seasonal water bodies leads to false alarms and missed floods"
    - Source date: 2026
    - Source type: preprint (conference abstract; the summariser rendered this line; wording needs reviewer check)
    - Confidence: low-medium
19. **Claim:** A 2026 arXiv comparison (Kolluru et al.) of a foundation model against GFM and DSWx reports cropland false positives in GFM. This was only via a search summary; the abstract page I opened says nothing about GFM false positives in cropland, so this claim is not supported by a quote I opened.
    - Source: https://arxiv.org/abs/2606.07780
    - Quote: "Cropland had the highest agreement"
    - Source date: 2026-06-05
    - Source type: preprint
    - Confidence: low (the quote supports only that cropland had the highest agreement for their model)
20. **Claim:** The April 2026 consortium roadmap presentation lists over-detection of water look-alikes as a core challenge, shows "strong overestimation in agricultural fields" for a 2025 US case, and shows it reduced by a SWIM deep-learning approach planned for the next GFM (implementation target March/April 2027).
    - Source: https://global-flood.emergency.copernicus.eu/media/events/9/salamon_evolution_gfm_april2026.pdf
    - Quote: "Strong overestimation in agricultural fields"
    - Source date: 2026-04
    - Source type: official docs (consortium slides)
    - Confidence: medium

### 5. Versions and reprocessing
21. **Claim:** Advisory-flag calculation was added to production only on 19 Jan 2022. This explains missing `advisory_flags` on pre-2022 scenes (inference: the archive for 2015-01 to 2021-06 predates it). Production versions: v1.x from July 2021, v2.x from Jan 2023, v3.0.0 on 23 Jan 2024, v3.2.0 and later in 2025.
    - Source: https://extwiki.eodc.eu/GFM/GFMVersioning and https://global-flood.emergency.copernicus.eu/media/events/4/the_new_gfm_archive.pdf
    - Quote: "used for producing archive spanning 2015 -01 to 2021 -06"
    - Source date: 2023 (archive slides); wiki read 2026-11-11
    - Source type: official docs
    - Confidence: medium (the flag-introduction entry is the summariser's paraphrase "Adds advisory flag calculation"; the link to missing files is inference)
22. **Claim:** The archive was planned to be reprocessed with updated algorithms (early 2024). The review says reprocessing is regular and the archive is "continuously updated with NRT data". No explicit statement that advisory flags were back-filled. Not found: any reason for missing flags on 2025 scenes. Candidate changes that coincide with 2025 (Apr 15 2025 post-processing overhaul; Oct 29 2025 Sentinel-1C support) are listed on the versioning page, but no source ties them to flags.
    - Source: https://global-flood.emergency.copernicus.eu/media/events/4/the_new_gfm_archive.pdf
    - Quote: "early 2024: release of reprocessed Sentinel -1 archive period usign updated algorithms"
    - Source date: 2023
    - Source type: official docs
    - Confidence: medium
23. **Claim:** Algorithm changes relevant to false alarms: v3.0.0 (Jan 2024) updated harmonic parameters and exclusion mask; 15 Apr 2025 post-processing overhaul (HAND filtering, extended minimum mapping unit); PDD cites updated harmonic parameters "to improve accuracy over agriculture". Review lists VH use and replacing the harmonic model with an exponential filter as future steps. Nothing announced for the current operational version that removes tilled-field false alarms; SWIM is the next evolution.
    - Source: https://extwiki.eodc.eu/gfm_assets/gfm_pdd_v4_0.pdf (section 3.3.2)
    - Quote: "to improve accuracy over agriculture, for example"
    - Source date: 2025-10-14
    - Source type: official docs
    - Confidence: medium

### 6. Layers in the product
24. **Claim:** The service has ten output layers: Observed Flood Extent, Observed Water Extent, Reference Water Mask, Exclusion Mask, Likelihood Values, Advisory Flags, Sentinel-1 Footprint and Metadata, Sentinel-1 Schedule, Affected Population, Affected Landcover.
    - Source: https://extwiki.eodc.eu/gfm_assets/gfm4.0_pum_2025.pdf (Table 1)
    - Quote: "Affected Landcover"
    - Source date: 2025-12
    - Source type: official docs
    - Confidence: medium (list read from the summariser's table)
25. **Claim:** Encodings as documented. Flood extent: 1 flood, 0 non-flood, 255 no data (when all algorithms return no data). Likelihood: 0-100, 50 is the class boundary; non-flood [0,49], flood [50,100]; excluded non-flood pixels are set to 49. Advisory flags: values 0 to 3 (none, low regional backscatter, rough water, both) per the PDD; the PUM gives no numeric table. Reference water mask: 12 monthly masks, values 0 to 2 (no water, permanent, seasonal for the month). Exclusion mask: 1 means excluded. Observed water extent: 1 means water detected.
    - Source: https://extwiki.eodc.eu/gfm_assets/gfm4.0_pum_2025.pdf (3.1, 3.3-3.5) and https://extwiki.eodc.eu/gfm_assets/gfm_pdd_v4_0.pdf (4.2-4.6)
    - Quote: "A likelihood value of 50 separates both classes."
    - Source date: 2025
    - Source type: official docs
    - Confidence: medium
26. **Claim:** The exclusion mask has five sub-layers: no-sensitivity areas (dense vegetation, urban), water look-alikes, topographic distortions, radar shadow, low Sentinel-1 coverage. "Water look-alikes" covers very dry or sandy soils, frozen ground, wet snow and flat impervious areas. It is static (built from backscatter and land-cover parameters) and does not know about tillage, so tilled fields are not in it.
    - Source: https://extwiki.eodc.eu/gfm_assets/gfm_pdd_v4_0.pdf (section 4.4)
    - Quote: "Water look-alikes"
    - Source date: 2025-10-14
    - Source type: official docs
    - Confidence: medium (the claim that tilled fields are not covered is an inference: no source mentions tillage)
27. **Claim:** Nothing inside the product separates tilled soil from water beyond what we already read. The reference water mask is built from five years of Sentinel-1 median backscatter and only marks permanent and seasonal water. The advisory-flag quality depends on that mask. Per-algorithm layers are the only other published signals. No layer carries crop or tillage information; "Affected Landcover" is an impact statistic.
    - Source: https://extwiki.eodc.eu/gfm_assets/gfm_pdd_v4_0.pdf (4.3, 4.6)
    - Quote: "Generally, the quality of this flag is strongly dependent on the quality and timeliness of the Reference Water Mask."
    - Source date: 2025-10-14
    - Source type: official docs
    - Confidence: medium

## Relevance to LandHorizon
- **Why the spring test fails, in the sources' words:** tilled or dry cropland is a documented, unresolved GFM failure mode (claims 1, 4, 5, 20). The consortium says advisory flags are typically not raised for it (claim 4) and the flags are regional (claim 3). So "advisory flag = not seen" will remove only part of it, which matches our 40 %. Do not count on a service fix before 11 Dec: the next evolution is a deep-learning algorithm planned for 2027 (claim 20).
- **Likelihood cut-off:** no source supports it, and our own medians (72 vs 73) argue against it (claims 8-10). Cost to test is small (the layer is already in STAC), but under the rule that thresholds are fixed before a test, any cut-off needs to be written down first and checked on a separate event.
- **Per-algorithm layers:** `dlr_flood_extent`, `list_flood_extent`, `tuw_flood_extent` and their likelihoods are in STAC (claim 11), so a stricter rule (for example, require all three, or require LIST plus one) is a cheap batch change. No source says which algorithm is cleaner on tilled soil, and the review says single-image and time-series both suffer (claim 15), so the gain is unproven. Test it on 30 Apr and 1 May 2024 and on the September 2024 flood. Extra assets mean more downloads per scene (more I/O; storage in the batch is a COG write only). Any such rule would be our own method on top of GFM and would change `ALGORITHM_VERSION`.
- **Pitch/report wording:** GFM's own consortium reports CSI 43.7 % globally against a 70 % target (claim 16). That supports calling flood history a screening indicator with stated limits, and agricultural over-detection a known limit.
- **Licence and access:** STAC collection licence is "other" (CEMS terms of service), and the PUM says data are "freely available" (not checked: whether product use is allowed). Free; no extra compute.
- **Missing flags:** pre-2022 scenes lack flags because the flag calculation started in Jan 2022 (claim 21, partly inference). Those scenes should be "unknown" for the advisory dimension, not "no advisory". For 2025 gaps, not found.
- **Coverage:** the dry-soil and arid sensitivity (claim 16) applies to the Galați region in spring and summer; none of the sources is specific to Romania. Not found: any GFM validation over Romania.

## Open questions
- Optical cross-check of tilled fields (other researcher).
- Does the full text of the JRC 2024/2025 QA reports (JRC142154, JRC146857) report commission error over cropland? Not opened.
- Does the wiki PDD section 4.6 describe any other flag logic for agricultural conditions? The text was cut off in my read.
- Which of the three algorithms flagged the 30 Apr 2024 polder? Check the per-algorithm STAC assets (empirical, not a source question).
- Why are `advisory_flags` missing on some 2025 scenes? Not found; ask gfm-support@eodc.eu (address from the GFM pages).
- Tupas (TU Wien, 2024 thesis) proposes a time-series false-positive assessment for agriculture; not opened.
- Tie-break rule contradiction (claim 13): confirm with the service which rule applies to v3.x scenes.

## Review
Reviewer date: 2026-11-11. Reviewer did not write this file.

Method limit: no PDF opened directly (the fetch tool returned raw binary and there was no PDF renderer). Every PDF and every EODC wiki page was read through the same kind of route the researcher used (r.jina.ai text extraction plus a small summariser model), run independently with exact-string checks and in several passes to cover the full text. The STAC collection, the EGU abstract and the arXiv abstract/HTML pages were opened directly. `verified` below means "the exact string was confirmed present and the surrounding text supports the claim" by that route. Nobody has yet compared the quotes against the PDFs by eye.

Count: 21 `verified`, 4 `unsupported`, 2 `misquoted`, 0 `unreachable`.

### Verdicts
1. `verified`. Quote and the "very low backscatter signatures" sentence are in PUM section 4.1. Date detail: page 1 carries "V20251021", the running headers "V20251201"; page metadata says published 15 Dec 2025.
2. `verified`. PUM 3.6 has two flags (low regional backscatter: dry soil, frost, snow; rough water: wind) plus their overlap, and the quoted sentence.
3. `verified`. Quote is in PDD 4.6.1. The comparison is against a "regional monthly grouped median value" after resampling to 20 km. The 14 km buffer is in both the PUM and the PDD ("a simple radial buffer of 14 km radius"); 5 km is in the PUM. The last sentence (tilled polder goes unflagged) is the researcher's inference, not in a source.
4. `verified`. Quote is in section 4.5 of the review. The source also gives the reason: the impact "is usually confined to smaller areas than in the case of frost or drought". "About 40 %" is the project's own figure, not checked here.
5. `verified`. Quote is in section 4.5. The text says false positive rates "can be quite high in some agricultural regions" depending on crop type and weather, worse "when the soils are dry", and gives no figure. It names "rapid changes in surface roughness and crop cover due to farming activities" but never tillage, ploughing or bare soil.
6. `verified`. Wiki QA page: target ">=70% (CSI)" against "independent reference datasets". Slide quote is exact. The same slide gives the CSI target as "70-80%" (KPI-3a). Slide deck page was published 21 May 2025.
7. `verified`. The string is in section III mid-sentence (lower-case "the", and it continues ", irrespective of nodata values"). I read arXiv v1, not the JSTARS version of record. Harmonisation to 0-100 and the [50, 60] statement are in the abstract and conclusion. See "missed" item 5: since Nov 2024 the likelihood can come from one algorithm alone.
8. `verified`. Quote is in section VI-B. The paper says setting split situations to non-flood "reduces these over-detections significantly" and that no flood was classified in the Somalia case. No cut-off other than 50 is evaluated.
9. `verified`, with a wrong section reference. The 0.3 quote is in section 4.7, not 2.2.4. "can be easily converted into a binary flood map adapted to local conditions" is in 2.2.4, with "While not carried out by the GFM service itself". Misra et al.: GFM IoU 56 % against 63 % for their own dataset, on the Kuro Siwo reference (43 events). Reviewer's reading, not in the source: 0.3 on a 0-1 scale is below the service's boundary of 50, so that threshold adds flood pixels and says nothing about a stricter cut-off. The 72 vs 73 medians are project data, not checked.
10. `verified`. Quote is in the 2023 QA report. The review evaluates only binary maps (OA, CSI) in section 3.6.
11. `verified`. All six keys and both titles are in `item_assets` on the live collection. Licence field is "other" with a link to the CEMS terms of service. The collection states no product version.
12. `verified`. Quote is in 2.2.1; "fuzzy logic-based post-classification" (2.2.1), "a recent SAR scene acquired from the same orbit" (2.2.2), harmonic model and "Bayesian inference model" (2.2.3) are all present.
13. `verified`. The wiki sentence starts "A majority-based consensus rule" (capital A); ratio <= 0.5 is Unflooded, and Table 18 case 5 (2 providers, 1 flooded) is Unflooded. The review (2.2.4) says "the ensemble defaults to classifying the pixel as flooded". Two corrections: the inline quote "ENSEMBLE uses consensus when two algorithms report" is not the wiki's wording (the 2 Jan 2023 entry reads "Update ENSEMBLE to use a consensus (instead of split decision) approach, when only two algorithms produce a result"); and the PDD contradicts itself, since Example 4 in section 3.4 says "Ensemble result: Flooded" for a 1-vs-1 case while Table 18 and the Figure 24 caption say Unflooded.
14. `misquoted`. The quote is not on the page. The 27 Nov 2024 entry reads: "The ENSEMBLE algorithm is now producing also results if only one individual flood mapping algorithm provides valid input". The substance of the claim holds (PDD 3.4 also gives "Likelihood from the individual algorithm" for that case). Replace the quote before using it.
15. `verified`. Quote is in section 4.5 (time-series algorithm "as described by Bauer-Marschallinger et al. (2022)"; the harmonic model "cannot account for crop rotation practices"). The LIST sentence is in 2.2.2 and "agree very well" in 3.1. Section 4.5 does not mention the dual-image algorithm at all, which is silence, not evidence that LIST is cleaner. "No published work found" is a search result, not a source statement; see "missed" items 3 and 4.
16. `unsupported`. The quote and the figures (OA 72.0 %, CSI 43.7 %, 36.2 % to 74.2 % by zone) are in the source, but they are not for v3.2.0. Section 3.6 says: "As results for the current GFM version v3.2.0 are not yet available" and "we report here results from version v2.1.0 that was used for generating the first version of the GFM data archive". The claim's version is wrong.
17. `unsupported`. The quote is present (Use Case 9, Greece), and the report has 12 use cases, agricultural omissions in Italy and India (rice) and a topographic distortion mask "covering agricultural fields" (Texas), and no tillage or bare-soil false alarms. Two figures do not match: the maximum CSI is 82.1 % (Greece), and "81.1" appears nowhere; "v2.1.0" appears nowhere either (the report names only V2.0.0, 2 Jan 2023, and V3.0.0, 24 Jan 2024, and does not say which produced the evaluated data).
18. `verified`. The string is in the abstract; twenty events; authors from Cambridge and NTU Singapore. It is a conference abstract with no results published. The abstract also says the three underlying algorithms are evaluated for systematic misdetections and false alarms.
19. `misquoted`. The abstract says "with cropland yielding the highest agreement (IoU=52%)", not the quoted words. The researcher already says the claim is unsupported, and that is right: the paper scores a foundation model against GFM and DSWx as references. The full text has one line, "These false positives in GFM occur in cropland and wetland areas," which reads as model false positives measured against GFM. Do not use this as evidence of GFM cropland false alarms.
20. `verified`. "Strong overestimation in agricultural fields" is on slide 9 (USA 2025); "Over-detection (water look-alikes)" on slide 3; SWIM as a "deep learning-based algorithm" on slide 6; "March/April 2027!" on slide 13. Presentation dated 21 April 2026. The SWIM improvement is the consortium's own claim with no independent check.
21. `unsupported`. Present in the sources: wiki entry of 19 Jan 2022 "added Advisory Flag calculation"; slide lines "used for producing archive spanning 2015 -01 to 2021 -06", "NRT production ramped up 2021 -07 with GFM versions v1.x", "NRT production update at 2023 -01 to GFM versions v2.x". The quote is about the archive's time span and says nothing on flags. The inference that the archive "predates" the flag calculation does not follow and is probably wrong: the archive was produced after Jan 2022 (the slides are from 2023, the review names v2.1.0 as the first archive version), and the same deck lists advisory flags among the archive's output layers. Also: V3.0.0 was released 24 Jan 2024 per the wiki and the 2023 QA report, not 23 Jan, and the list omits the v4.0 major release of April 2025 ("missed" item 1).
22. `verified`. The slide quote is present, typos included. The review's conclusions say "The GFM flood archive is continuously updated with NRT data" and "regular reprocessing efforts are conducted to ensure compatibility between the NRT and archive data". The 15 Apr 2025 and 29 Oct 2025 wiki entries exist. No source read says flags were back-filled.
23. `verified`, with corrections. PDD 3.3.2: "for Version 3.x of the GFM product, the harmonic parameters were updated, to improve accuracy over agriculture, for example." Wiki 24 Jan 2024 (not 23): harmonic parameters and "Improved exclusion masks". Wiki 15 Apr 2025: "Replaced the majority filter with the extended minimum mapping unit (MMU)" plus HAND-based filtering. In the review, VH is proposed against under-detection of flooded vegetation (4.6), not against false alarms; the exponential filter is Tupas et al. (2024)'s suggestion (4.5). No wiki entry from 2024 to 11 June 2026 mentions agriculture.
24. `verified`. The ten layers are in PUM Table 1.
25. `verified`, with notes. Flood extent 1 / 0 / 255 and the likelihood ranges are in PUM 3.1 and 3.5; flag values 0 to 3 in PDD 4.6; reference water mask 0 to 2 with 12 monthly masks in PDD 4.3; water extent 0 / 1 in PDD Table 19 (no-data there is NaN). The exclusion mask encoding is given only as "TRUE (1)" in the PUM table; the PDD calls it binary without values. On 49: the PUM says a flooded pixel inside the Exclusion Mask gets the adjusted likelihood "49 (i.e. lowest for No flood)", so 49 can mean "detected, then masked". The PUM gives the reference period as 2018-2022 in 3.3 and 2017-2021 elsewhere.
26. `verified` for the documented part. Five sub-layers in PDD 4.4. Water look-alikes (4.4.2): flat impervious areas, sand, dry soils, frozen ground, wet snow, tarmac; cells masked where backscatter is below -15 dB in more than 70 % of observations over a 2020-2022 baseline for v3.x. That tilled fields are not covered is the researcher's inference, as stated.
27. `unsupported`. The quoted sentence is in PDD 4.6.2 "Rough water surface" and refers to that flag only (the sentence before it is about a changed water-body shape "misinterpreted as roughened water surface"). It does not support "the advisory-flag quality depends on that mask" in general, and it says nothing on the low-backscatter flag, which is the one that matters for tilled soil. The other parts hold: reference water mask from five years (2017-2021) of Sentinel-1 median backscatter, values 0 to 2; Affected Land Cover is an impact layer (PDD 4.10); no layer or flag logic for crops or tillage was found.

### What the researcher missed
1. **GFM v4.0 is a major version, released mid-April 2025, and it raised commission error.** The consortium's own slides give "Commission error: + 2.11", "Omission error: - 8.87", "CSI: + 6.30" as average changes ("improvements in 17 of 20 use cases") and list "Remaining issues in certain land cover types and agriculture overestimation". The slides give no units and do not name the baseline version. The versioning page says "GFM Layers produced from different MAJOR versions can not be used in unison." So scenes produced since 15 Apr 2025 may over-detect more than the 2024 scenes the spring test used, and a 2015-2025 per-pixel count may mix v3.x and v4.x. Not found: whether older STAC items were reprocessed with v4 (the collection states no version). The exact release date (15 Apr 2025) comes from a search snippet of the news item, whose body I could not open, and matches the wiki entry date.
   - https://global-flood.emergency.copernicus.eu/media/events/8/8-roth_florian_globalflood25_gfmnewmajorversion.pdf
   - https://extwiki.eodc.eu/GFM/GFMVersioning
   - https://global-flood.emergency.copernicus.eu/news/208-major-update-of-the-cems-global-flood-monitoring-released/
2. **Newer accuracy evidence than the v2.1.0 figures in claim 16 exists, all from the consortium and all on use cases it selected.** A news item of 1 Aug 2025 reports CSI 71.4 % (v3) against 82.4 % (v4) for one Arkansas event. The 2025 annual QA report (news of 27 Jul 2026) has ten of 12 use cases above 70 % CSI for flood extent, two just below (63.4 %, 67.0 %). Neither news item mentions agriculture or commission error. The 2024 report (JRC142154) and the 2025 report full texts were not opened by me either.
   - https://global-flood.emergency.copernicus.eu/news/212-improved-performance-of-the-new-version-of-the-global-flood-monitoring-of-cems/
   - https://global-flood.emergency.copernicus.eu/news/255-publication-of-the-global-flood-monitoring-annual-product-and-service-quality-assessment-report-2025/
   - https://publications.jrc.ec.europa.eu/repository/handle/JRC142154
3. **Tupas et al. (2024) is a peer-reviewed paper, not only a thesis** ("Assessment of time-series-derived no-flood references for SAR-based Bayesian flood mapping", GIScience & Remote Sensing). A search summary says it reports higher false positive rates and agricultural overestimation for the TU Wien algorithm and that an exponential filter lowers them at most sites. I could not open the full text, so this is unverified, but it is the most likely place for per-algorithm false-positive numbers on cropland.
   - https://repositum.tuwien.at/handle/20.500.12708/206671
4. **Garg et al. say they evaluate the three underlying algorithms for systematic misdetections and false alarms.** That is the per-algorithm comparison claim 15 says was not found. Only the abstract is public.
   - https://meetingorganizer.copernicus.org/EGU26/EGU26-21734.html
5. **The likelihood no longer always encodes agreement.** With the Nov 2024 single-algorithm fallback, the ensemble likelihood is the "Likelihood from the individual algorithm" (PDD 3.4), so a high value can rest on one algorithm. The [50, 60] reading in claim 7 comes from the 2023 design.
   - https://extwiki.eodc.eu/gfm_assets/gfm_pdd_v4_0.pdf
6. **The consortium's reference data is not from an independent sensor.** In the 2023 QA report the flood references come from thresholding "applied to Sentinel-1 data", with "Manual enhancement is performed using Sentinel-2 imagery", masked with the same layers as the product. Under the project rule on independent-sensor references, these CSI figures cannot stand in for our own validation.
   - https://civil-protection-knowledge-network.europa.eu/system/files/2024-12/global-flood-monitoring-annual-product-and-service-quality-assessment-report-2023.pdf
7. **The licence can be partly closed.** The CEMS terms grant "free access", allow users to reproduce, distribute, adapt, modify and combine the data, and ask for the notice "Generated using Copernicus Emergency Management Service information [Year]" (or "Contains modified ..." for adapted data). Data is provided "as is" and is not an official warning. The page does not mention commercial use in either direction and carries no date.
   - https://global-flood.emergency.copernicus.eu/terms-of-service/

### Problems in "Relevance to LandHorizon"
- **Pitch/report wording** rests on claim 16 (`unsupported`). CSI 43.7 % is for archive version v2.1.0, not for the v3.x or v4.x data the pipeline reads. It can be cited only as "the first archive version, consortium's own validation". Source: https://elib.dlr.de/218412/1/1-s2.0-S0034425725005127-main.pdf
- **Missing flags** rests on claim 21 (`unsupported`). Treating scenes without flags as `unknown` is right under the project rules whatever the cause, but the stated cause (flag calculation started Jan 2022) should be dropped. Source: https://global-flood.emergency.copernicus.eu/media/events/4/the_new_gfm_archive.pdf
- **Coverage** says the "hot and arid" sensitivity "applies to the Galați region". No source places Galați in any of the review's environmental zones, the zone figures range widely (for example 58.3 % for "cool temperate and dry", 63.8 % for "warm temperate and mesic"), and they are v2.1.0 figures. Not backed by a verified claim. Same source as above.
- **Per-algorithm layers:**
  - "Require LIST plus one" has no verified backing. The only LIST statement is the authors' own design description (2.2.2), and section 4.5 does not discuss LIST.
  - The proposed test uses 30 Apr-1 May 2024 and September 2024, the scenes on which the failure was found. Under the project rules the rule and pass criteria must be written down first and checked on a separate event against an independent-sensor reference. The bullet says this for the likelihood cut-off but not here.
  - Since Nov 2024 some scenes carry one algorithm only (claim 14). An "all three" rule would turn those into "no flood"; under the project rules they must be `unknown`.
  - The rule would also run across the v3/v4 major-version boundary ("missed" item 1).
- **Licence and access:** "not checked" is now partly answered ("missed" item 7); the product needs the attribution notice, and commercial use is not addressed on the terms page.
- The other bullets (advisory flags remove only part; no service fix before 11 Dec; likelihood cut-off unsupported) are backed by verified claims 3, 4, 5, 8, 9, 10 and 20.

### Untrusted content
Nothing in the fetched pages or in this file read as instructions to the reviewer; none were followed.
