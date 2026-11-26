# Which InSAR velocity thresholds have a citable source, how precise is EGMS, and how should uncertainty and "unknown" be expressed for a plot? (G2)
Date: 2026-11-12
Scope: published stability/activity thresholds and classes, the 2 and 5 mm/year question, damage link, EGMS precision and quality attributes, how absence and uncertainty are worded, interpretation traps. Out of bounds: EGMS product choice, format, access and licence, spatial pick of points or cell, non-EGMS data, own InSAR processing.

Method note: the fetch tool returns summaries, and quotes are capped near 125 characters. Only quotes seen in an opened page or a search snippet are used. Many PDFs (EGMS validation reports, ISPRS ADAtools paper, Cigna full text) could not be read, so numbers from them are "not found" here, not guessed. Every claim marked "snippet" was seen in a search result and should be re-checked by the reviewer.

## Claims
1. **Claim:** Cigna, Bianchini and Casagli (2013) set an activity threshold of ±5 mm/year for PSI landslide mapping. It is a detection threshold (data precision projected onto the slope), applied to velocity projected along the steepest slope, on ERS-1/2 and RADARSAT-1/2 data, not EGMS. This is the only citable 5 mm/year found.
   - Source: https://nora.nerc.ac.uk/id/eprint/19874/
   - Quote: "An activity threshold of ±5mm/year is determined by applying the average projection factor of local slopes to the PSI data precision."
   - Source date: 2013
   - Source type: peer-reviewed (Landslides 10, 267-283)
   - Confidence: medium (quote from search snippet of this page; page summary agreed)

2. **Claim:** The same method uses the Cruden and Varnes classes for an intensity scale, with 16 mm/year between extremely slow and very slow, lowered by about 20% for averaging. This is an engineering/hazard-style intensity class, applied to landslide polygons, not a statistical noise floor.
   - Source: https://nora.nerc.ac.uk/id/eprint/19874/
   - Quote: "The intensity threshold between extremely and very slow phenomena (16mm/year) is reduced by ~20%"
   - Source date: 2013
   - Source type: peer-reviewed
   - Confidence: medium (snippet)

3. **Claim:** The ADAtools suite (Navarro, Tomas, Barra and colleagues; applied to EGMS) uses a user-set absolute velocity threshold to mark a measurement point (MP) active, and says points below it are not proven stable. This is a detection threshold, tied to the map's noise (earlier Barra-group work sets it as a multiple of the standard deviation of PS velocities; exact multiple not confirmed here).
   - Source: https://isprs-archives.copernicus.org/articles/XLVIII-3-2024/351/2024/isprs-archives-XLVIII-3-2024-351-2024.pdf
   - Quote: "MPs falling below this threshold may not inherently be stable but are excluded from active categorization."
   - Source date: 2024 (ISPRS Archives XLVIII-3-2024; the snippet may come from a sibling ADAtools paper, check)
   - Source type: peer-reviewed (conference archive)
   - Confidence: low (snippet only, PDF unreadable)

4. **Claim:** EGMS specification: Basic and Calibrated mean-velocity standard deviation is 0.7 mm/year (1 sigma) for MPs with coherence above 0.7; Ortho is listed at 0.7 mm/year (1 sigma) with no coherence condition; displacement standard deviation 8 mm (1 sigma). This is a stated product requirement, not a measured result.
   - Source: https://library.land.copernicus.eu/products/European_Ground_Motion_Service_Product_Description_v3.html
   - Quote: "0.7 mm/year (1 σ) for MP with coherence greater than 0.7."
   - Source date: 2025-08-07
   - Source type: official docs
   - Confidence: high

5. **Claim:** Independent validation (GNSS and corner reflectors, statistical tests, 2015 and 2021 EGMS releases, sites with significant deformation) found most velocity differences under 2 mm/year. This is the nearest citable support for a ~2 mm/year figure, but it describes differences to GNSS at test sites, not a noise floor for a rural plot. Romania: not found.
   - Source: https://orbit.dtu.dk/en/publications/validation-of-the-european-ground-motion-service-with-global-navi/
   - Quote: "most of the differences between velocities being below 2 mm/year"
   - Source date: 2024 (IGARSS 2024)
   - Source type: peer-reviewed (conference paper)
   - Confidence: medium (snippet wording; page summary agreed)

6. **Claim:** The official EGMS validation (2015-2021 and 2019-2023 datasets) covers 38 areas in ten countries, by comparison with field measurements. The mm/year results in the reports could not be opened (files exceed fetch limit): not found.
   - Source: https://land.copernicus.eu/en/feature-articles/when-the-ground-validates-the-sky-how-field-data-enable-satellite-monitoring-of-ground-motion
   - Quote: "These activities are being performed in 38 areas in ten European countries."
   - Source date: not found (probably 2024)
   - Source type: official docs
   - Confidence: medium

7. **Claim:** Calibrated and Ortho accuracy depends on the GNSS model used for calibration; Basic is relative to a virtual reference point and cannot be compared across adjacent Basic areas. So absolute velocities carry the GNSS model's regional signal.
   - Source: https://land.copernicus.eu/en/faq/products/european-ground-motion-service
   - Quote: "CALIBRATED and ORTHO data accuracy depends on the Global Navigation Satellite System (GNSS) model used for calibration"
   - Source date: not found
   - Source type: official docs
   - Confidence: high

8. **Claim:** Basic products from different areas cannot be compared with each other (reference-frame trap).
   - Source: https://library.land.copernicus.eu/products/European_Ground_Motion_Service_Product_Description_v3.html
   - Quote: "It is not possible to compare deformations from adjacent areas belonging to different products of the same level."
   - Source date: 2025-08-07
   - Source type: official docs
   - Confidence: high

9. **Claim:** EGMS's own guidance says the data are for wider-scale analysis and not for individual buildings, and lone points are unreliable (a point may sit on a roof or shed, subject to thermal dilation). Safest reading is from clusters of points. This is the closest to an EGMS disclaimer found; no separate legal disclaimer text was found.
   - Source: https://land.copernicus.eu/en/faq/products/european-ground-motion-service/there-is-a-moving-egms-point-on-my-house-2013-what-should-i-do
   - Quote: "is not appropriate to the analysis of individual buildings."
   - Source date: not found
   - Source type: official docs
   - Confidence: high (the page summary also used "may be subject to thermal dilation or seasonal change", via https://land.copernicus.eu/en/faq/products/european-ground-motion-service)

10. **Claim:** Coverage is not continuous; vegetation causes decorrelation, so rural and farmland plots often have no points. Absence means no reliable measurement, not stability.
    - Source: https://land.copernicus.eu/api/en/faq/products/european-ground-motion-service/where-are-the-main-limitations-of-egms-data
    - Quote: "typically vegetation causes decorrelation from one image to the next,"
    - Source date: not found
    - Source type: official docs
    - Confidence: high

11. **Claim:** Ortho has gaps by design: no measurements where geometry prevents coverage, cells rejected when they hold too few points, and a minimum in both ascending and descending orbits. The minimum count itself: not found.
    - Source: https://library.land.copernicus.eu/products/European_Ground_Motion_Service_Product_Description_v3.html (gaps); https://library.land.copernicus.eu/products/European_Ground_Motion_Service_Algorithm_Theoretical_Basis_Document_v4.html (rejection)
    - Quote: "In such areas, there are no EGMS Ortho measurements." and "Rejecting grid-cells with less than a predefined number of points."
    - Source date: 2025-08-07
    - Source type: official docs
    - Confidence: high

12. **Claim:** Ortho has no north-south component and cannot measure motion in that direction, so vertical and east-west values assume it is absent or negligible.
    - Source: https://library.land.copernicus.eu/products/European_Ground_Motion_Service_Product_Description_v3.html
    - Quote: "north-south displacement components are not available for any MP"
    - Source date: 2025-08-07
    - Source type: official docs
    - Confidence: high

13. **Claim:** Per-point quality attributes available for an honest label: temporal coherence, RMSE of the time-series regression (third-order polynomial plus seasonal term), amplitude dispersion, and standard deviation fields. Ortho per-cell attributes: velocity std from error propagation; the number of points per cell is not listed as an attribute (not found).
    - Source: https://library.land.copernicus.eu/products/European_Ground_Motion_Service_Product_Description_v3.html
    - Quote: "temporal_coherence, rmse, amplitude_dispersion, all the standard deviation fields."
    - Source date: 2025-08-07
    - Source type: official docs
    - Confidence: medium (the Ortho remark is an absence in the summary I read)

14. **Claim:** Phase and seasonal limits: with snow cover, non-linear motion is ambiguous, and the ambiguity rate is half a wavelength per year (about 28 mm/year). Fast-motion phase-unwrapping limits for EGMS in mm/year: not found beyond this.
    - Source: https://land.copernicus.eu/en/faq/products/european-ground-motion-service
    - Quote: "measuring nonlinear motion is sometimes ambiguous when half of the year or more is unobservable"
    - Source date: not found
    - Source type: official docs
    - Confidence: medium

15. **Claim:** Damage link: not found in sources I could open. The candidate sources seen only in search results, not opened, are Burland/Boscardin and Cording angular-distortion work, Cigna and Tapete 2021, Bianchini 2015 (Remote Sensing 7, 4678) and an ESA Fringe 2026 poster (ID_370). They are reported as saying damage tracks differential settlement more than absolute settlement. That is not citable until a reviewer opens them.
    - Source: not found
    - Quote: not found
    - Source date: not found
    - Source type: not found
    - Confidence: low

16. **Claim:** National services: the Norwegian service (NGU) shows 1D line-of-sight velocity with a legend the user can change. Class schemes for Italy, Germany BBD, Netherlands, Denmark, UK: not found in opened sources.
    - Source: https://www.ngu.no/en/geological-mapping/how-does-insar-map-service-work
    - Quote: "The colour of the point represents its average velocity, which is defined in the legend."
    - Source date: not found
    - Source type: official docs
    - Confidence: medium

## Not found (explicit)
- A source for 2 mm/year as an EGMS noise floor: not found. Nearest: claim 5 (differences mostly under 2 mm/year) and claim 4 (0.7 mm/year 1 sigma spec).
- A 5 mm/year source for EGMS: not found. Nearest: claim 1 (landslide activity threshold on older PSI, along-slope).
- 2 / 10 / 16 mm/year state-of-activity classes, Cruden and Varnes mm/year values: only the 16 mm/year boundary seen via claim 2; Cruden and Varnes primary text not opened.
- EGMS validation-report velocity precision per product level and any Romania or low-density result: not found.
- Published minimum point count or distance before describing an area: not found.
- Quantified seasonal soil shrink-swell effect on EGMS: not found (te Brake 2017 and Westerhoff and Steyn-Ross 2020 seen in search only, unopened).

## Relevance to LandHorizon
- **Threshold wording:** keep 2 mm/year only as a placeholder labelled "no source for EGMS; test-site differences mostly under 2 mm/year; spec is 0.7 mm/year 1 sigma". Do not present 5 mm/year as sourced for EGMS; if used, cite Cigna 2013 and say it is a landslide along-slope detection threshold. Neither is a damage threshold. Writing them down before testing is possible now, with that status.
- **Label design (no new data, no compute):** three states fit the method rules: "unknown" when no point or cell, or the cell is gap/too few points; "no significant motion detected" when |v| is below k times the velocity std (k to be fixed in advance; ADAtools-style, value not confirmed); "moving" otherwise. Say that absence of points (common on farmland) is not stability. Needs coherence, RMSE and velocity std attributes carried into the raster step; whether the Ortho product has them is for the product-level researcher.
- **Plot size:** 100 m cells say little about a plot under 1 ha; EGMS itself says lone points are not for individual buildings, so describe the area, not the plot.
- **Disclaimer text:** reuse the EGMS wording in claim 9 and say the output is a screening indicator, not a geotechnical or damage assessment; mean velocity does not show differential motion (claim 15 unverified).
- **Cost/licence/coverage:** nothing in these sources changes EGMS access or licence. Galati/Romania-specific precision: not found.

## Open questions
- Open the EGMS validation reports (2015-2021, 2019-2023; too large for the fetch tool) for per-product mm/year results and any Romanian test area.
- Confirm the sigma multiple (1.5, 2) in Barra 2017 and Navarro 2020 from the papers.
- Verify damage sources (Cigna and Tapete 2021, Bianchini 2015, Boscardin and Cording 1989) and Cruden and Varnes 1996 primary text.
- Product-level question for another researcher: does the Ortho layer expose velocity std and a point count per cell?

## Review
Reviewer: independent verifier, 2026-11-12. Every cited URL was opened with the same summarising fetch tool, so exact wording was checked through the tool's quotes. My rule on small differences: a difference only in whitespace or in where the quote stops is `verified` with a note, if the meaning is unchanged. A cut that drops a qualifier is `misquoted`.

### Verdicts
1. **verified.** The NORA record (Cigna, Bianchini, Casagli, Landslides 10(3):267-283, 2013, ERS1/2 and RADARSAT1/2, 1992-2011) has the sentence. The source writes "±5 mm/year" with a space; fix the spacing. "Projected along the steepest slope" is not in the quote. The quote only says "average projection factor of local slopes". "Only citable 5 mm/year found" is weakened by the Palama lead under "Missed" below.
2. **verified.** Same record. The source writes "(16 mm/year)" with a space. "For averaging" is the researcher's reading; the quote only says "reduced by ~20%".
3. **unreachable.** The PDF downloads, but its text could not be extracted. The HTML abstract page (https://isprs-archives.copernicus.org/articles/XLVIII-3-2024/351/2024/) has neither the quote nor any threshold or standard-deviation detail. A search snippet attributes the sentence to this paper, but I could not see it in the text. The author list is Monserrat, Barra, Béjar-Pizarro, Rivera, Galve, Guardiola, Cuevas-González, Mateos, Ezquerro, Azañon, Shahbazi, Navarro, Crosetto, Luzi. "Tomas" is not an author. The abstract does confirm that ADATools is applied to EGMS (SARAI project). The standard-deviation link is unconfirmed.
4. **verified.** Tables 1-3 have "0.7 mm/year (1 σ) for MP with coherence greater than 0.7." for Basic and Calibrated, and "0.7 mm/year (1 σ)" for Ortho, in the Specification column. Corrections:
   - Displacement std is **4 mm** for Basic and 8 mm only for Calibrated and Ortho.
   - The source date is inconsistent. The page says "Published August 7, 2025", the Document Control table says v3.0 06/08/2025, and the Change Log has 3.0.0 on 2025-12-03 and 3.0.2 on 2026-10-29.
5. **verified.** The DTU Orbit abstract (Martins, Caro Cuenca, et al., IGARSS 2024, pp. 7537-7541) has the quote. "2015 and 2021 EGMS releases" misreads the abstract's "first EGMS product from 2015 and 2021". That is the single baseline product, which has since been archived (see "Missed"). No sites or countries are named, so "Romania: not found" stands.
6. **unsupported.** The quote is there and supports "38 areas in ten countries". But the article says the team finished validating "EGMS data from 2015 to 2022", while the 2019-2023 dataset was still to be validated, with a report planned for April 2025. The claim's "2015-2021 and 2019-2023 datasets" is wrong. The page has no date (about 2024, inferred).
7. **verified** for the GNSS-model sentence. The FAQ says Basic is "relative to a virtual reference point". It does **not** say that Basic areas cannot be compared; that part comes from the Product Description (claim 8). "Absolute velocities carry the GNSS model's regional signal" is an inference. The FAQ adds that the model depends strongly on GNSS station density.
8. **verified.** The quote is in Section 2.1 and applies to **Basic (L2a) only**. Calibrated and Ortho are GNSS-referenced and overcome the limit.
9. **misquoted.** In the source the sentence goes on: "is not appropriate to the analysis of individual buildings, unless they are large enough to cover the ambiguity", or unless the building sits within a broader cluster of points. Ending the quote with a period removes the qualifier. The cluster advice ("are clustered and show some collective result") and the thermal-dilation shed-roof example are both on the page. The FAQ also gives geolocation tolerances of about N ±8 m, E ±12 m, V ±8 m.
10. **verified.** The page has the quote, then "and so no reliable data can be extracted". It also says coverage "is not continuous" and is densest in built areas. "Rural and farmland plots often have no points" is an inference: the page does not name farmland. "Absence means no reliable measurement, not stability" follows from the text.
11. **verified.** Both quotes were found: the Product Description, and ATBD §9.3. The ATBD §9.3 also requires at least one ascending and one descending MP per cell, and does not state the predefined number. Note that "such areas" means high-relief terrain with layover, foreshortening and shadow. That is unlikely to matter in flat Galați, so the geometry gap is not the main source of gaps for us. Vegetation is (claim 10).
12. **verified.** The source continues "...since they are estimated from GNSS data". "Assume it is absent or negligible" is the researcher's inference.
13. **verified.** Section 8 lists these as "some of the quality checks", so the list is not exhaustive. Ortho attributes (Table 6) are pid, easting, northing, height, rmse, mean_velocity, mean_velocity_std, acceleration(_std), seasonality(_std) and the time series. It has **no temporal_coherence** and no point count. "From error propagation" was not confirmed.
14. **verified.** The FAQ has the quote and "half a wavelength per year (about +/- 28 mm/yr)" for isolated points relative to their surroundings, in snow-affected areas.
15. **unsupported.** No source or quote is given, so there is nothing to verify. It is correctly marked "not citable".
16. **verified.** The source sentence continues "...defined in the legend (B in the figure below)." The meaning is unchanged. The user changes the colour-table limit values per layer, and the page gives no class breaks in mm/year.

Counts: 12 verified, 2 unsupported, 1 misquoted, 1 unreachable.

### What the researcher missed
- **A possible EGMS-specific 5 mm/year threshold, with ~2 mm/year given as the EGMS Basic noise.** I saw this only in a search snippet: Palama et al., JISDM 2025, https://jisdm2025.gik.kit.edu/downloads/JISDM2025_Palama_et_al.pdf. The PDF text could not be extracted, so it is **unverified**. If it holds, it contradicts two items under "Not found": "A source for 2 mm/year as an EGMS noise floor" and "A 5 mm/year source for EGMS". Open it before any threshold decision. The same search snippet attributed a 5 mm/year ADAFinder threshold to an ESA Fringe presentation (https://fringe.esa.int/iframe-agenda/files/presentation-373.pdf). It redirects to fringe2026.esa.int, which returns 404, so it is unverified.
- **Superseded product.** The EGMS 2020-2024 release (29 Apr 2026, https://land.copernicus.eu/en/news/egms-annual-update-brings-new-data-improvements-to-egms-explorer) adds an "enhanced quality-control strategy", mainly for **Ortho**. It also moves the Baseline (2015-2021) and 2018-2022 datasets to the archive. Claim 5's validation therefore describes a superseded product, and the precision of the current Ortho release is unvalidated in this file. The FAQ (https://land.copernicus.eu/en/faq/products/european-ground-motion-service) says the current products cover 2020-2024, with the next update due in Q4 2026.
- **Validation report for the 2019-2023 dataset.** It answers the first open question and is linked from the technical library: https://land.copernicus.eu/en/technical-library/validation-report-2019-2023-dataset/@@download/file (not opened here).
- **The 5 mm/yr reliability limit in vegetated areas is contested.** Li et al. (2026) conclude that "InSAR is unreliable in vegetated coastal settings for rates below 5 mm/yr". This is US Gulf Coast work, not EGMS. Shirzaei et al. dispute it in a peer-reviewed comment (Earth Observation 1:145-154, 30 Sep 2026): https://egusphere.copernicus.org/preprints/2026/egusphere-2026-3372/. It is relevant because our plots are vegetated farmland.
- **Pointer outside this file's scope.** The same 29 Apr 2026 news item announces a machine-to-machine API in EGMS Explorer. That may change the constraint that EGMS "can't be scripted"; the access researcher should check it.

### Problems in "Relevance to LandHorizon"
- **The label design needs coherence that Ortho does not have.** It requires "coherence, RMSE and velocity std attributes carried into the raster step". The planned product is Ortho, and Table 6 has rmse and mean_velocity_std but **no temporal_coherence and no point count**. This also answers the last open question: velocity std yes, point count no (Product Description v3, link above).
- **The k-times-std rule is not backed by a verified claim.** "ADAtools-style" rests on claim 3, which is unreachable, and the multiple k is unconfirmed. Keep it as our own rule, and write it down before testing.
- **The disclaimer reuses claim 9 without its qualifier.** Quote the full sentence, including "unless they are large enough to cover the ambiguity", or paraphrase it faithfully.
- **"Mean velocity does not show differential motion"** rests on claim 15, which is unsupported. The bullet already says so; keep it out of any product text until a source is opened.
- **The 2 mm/year placeholder wording** cites "test-site differences mostly under 2 mm/year". That comes from validation on the archived baseline product at deforming sites (claim 5), and should say so.
- The rest respects the constraints (no new data, no compute, missing data = `unknown`, area-not-plot wording for 100 m cells).

No fetched page, and nothing in this file, contained instructions to the reviewer.
