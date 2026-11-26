# How accurate is ESA WorldCover 2021, overall and for cropland, in Europe and near Romania / the lower Danube?
Date: 2026-11-23
Scope: overall and cropland (class 40) accuracy of WorldCover 2020/2021, independent European checks, 2020 vs 2021, and the LCFM successor (accuracy, licence). Out of bounds: WorldCover licence (done), GFM and flood methods, other land-cover products.

**Access limit (read first):** the official Product Validation Report (PVR V2.0) and Product User Manual (PUM V2.0) are PDFs. The fetch tool returned only compressed binary for them (S3, IIASA, and LCFM PVR), and worldcover2021.esa.int refused the connection. So the 2021 confusion matrix, the confidence interval method, continental values and the cropland user's/producer's accuracy (UA/PA) were **not read by me and are "not found" below**. Search-engine summaries mentioned some PVR/PUM numbers (continental range 72.5–82.1 %, "Eurasia" lowest, accuracy up on every continent vs 2020); I did not open them, so they are not cited. A person with a PDF viewer should read PVR V2.0 Tables 2 and 3 and the sample-design section.

## Claims
1. **Claim:** The official headline overall accuracy is 76.7 % for WorldCover 2021 v200 and 74.4 % for 2020 v100, independently validated (Wageningen for statistical accuracy, IIASA for spatial accuracy). So "about 77 %" is a correct citation of the global figure.
   - Source: https://esa-worldcover.org/en/data-access
   - Quote: "The WorldCover 2021 v200 reaches an overall accuracy of 76.7%."
   - Source date: undated page, accessed 2026-11-23
   - Source type: official docs
   - Confidence: high
   - Supporting quote (same page): "The WorldCover 2020 v100 product reaches an overall accuracy of 74.4%."

2. **Claim:** The 2020 and 2021 maps used different algorithm versions (v100 vs v200), and the data record warns that changes between the two maps should be treated with caution. 2021 scores higher overall (76.7 vs 74.4 %). The reason for the gain (algorithm changes) is in the PUM, which I could not read.
   - Source: https://zenodo.org/records/7254221
   - Quote: "changes between the maps should be treated with caution"
   - Source date: 2022-10-28
   - Source type: official docs
   - Confidence: medium (the quote supports "different versions, be careful"; the cause of the accuracy gain is not sourced)

3. **Claim:** Global overall accuracy is also reported as about 75 % (2020) and 76.7 % (2021) by a data-hosting mirror that cites the same validation.
   - Source: https://docs.terrabyte.lrz.de/datasets/esaworldcover/
   - Quote: "independently validated with a global overall accuracy of about 75% and 76.7%, respectively for the 2020 and 2021 dataset."
   - Source date: undated
   - Source type: vendor (data host, secondary)
   - Confidence: medium

4. **Claim:** In a multi-product comparison, WorldCover 2021's cropland class scored a user's accuracy of 80.6 % (±1.5). The excerpt I opened gives no region, reference data or year for this number, and it is not a Europe-only figure. The paper says binary cropland maps tend to score higher than multi-class land-cover maps. (A producer's accuracy of 79.3 % was reported in the same table per my reading of the page, but I did not get a verbatim quote for it, so treat it as unconfirmed.)
   - Source: https://essd.copernicus.org/articles/15/5491/2023/essd-15-5491-2023.html
   - Quote: "the cropland class of WorldCover has a user's accuracy of 80.6 (±1.5)."
   - Source date: 2023
   - Source type: peer-reviewed (WorldCereal paper, ESSD)
   - Confidence: medium (exact quote, but scope of the sample unknown)

5. **Claim:** Independent Europe check (Ireland, LUCAS 2022 points): WorldCover 2021 area-weighted overall accuracy is 0.664 ± 0.012, well below the 76.7 % global figure. Cropland UA 0.808 ± 0.036 and PA 0.739 ± 0.043 (the tutorial's accuracy table; only the overall quote is verbatim). Ireland is mostly grassland, so it says little about the Galați plain.
   - Source: https://www.technicalgis.com/tutorials/land-cover-accuracy-assessment-python/
   - Quote: "ESA WorldCover 2021 has an area-weighted overall accuracy of 0.664 ± 0.012 in Ireland"
   - Source date: 2026-10-27
   - Source type: blog (tutorial, not peer-reviewed)
   - Confidence: low

6. **Claim:** LCFM Global Land Cover Map (LCM-10) 2020 V1 has a global overall accuracy of 80.10 % ± 0.20 % (vs 74.4 % for WorldCover 2020 on the official figures above), but this is a different validation sample, so it is not a like-for-like comparison. Cropland UA/PA: not found (PVR not readable).
   - Source: https://sdi.eea.europa.eu/catalogue/srv/api/records/602507b2-96c7-47bb-b79d-7ba25e97d0a9?language=eng
   - Quote: "Global overall accuracy of 80.10% ± 0.20%."
   - Source date: metadata published 2025-06-26; validation report published 2026-01-27
   - Source type: official docs (Copernicus metadata record)
   - Confidence: high for the number; low for any comparison with WorldCover

7. **Claim:** LCFM licence is Copernicus full, open and free access, with attribution; use in a product looks allowed.
   - Source: https://sdi.eea.europa.eu/catalogue/srv/api/records/602507b2-96c7-47bb-b79d-7ba25e97d0a9?language=eng
   - Quote: "The Copernicus land monitoring products and services are made available on a principle of full, open and free access"
   - Source date: 2026-01-27 (record revised 2026-08-26)
   - Source type: official docs
   - Confidence: medium (metadata summary, not the full licence text)

8. **Claim:** LCFM launched 26 Jun 2025 with the 2020 map, with yearly updates planned from 2020 to 2026. Whether a 2024 map is already published: not found.
   - Source: https://land.copernicus.eu/en/news/lcfm-a-new-chapter-in-global-land-cover-monitoring
   - Quote: "new yearly updates from 2020 through 2026"
   - Source date: 2025-06-26
   - Source type: official docs
   - Confidence: low (my fetch tool paraphrased this page; the quoted phrase is from the tool's summary, so the reviewer must check it verbatim)

Not found: WorldCover 2021 cropland UA/PA global or for Europe; the main cropland confusions (cropland vs grassland); validation sample design and reference data; any Romania or lower-Danube validation of WorldCover; LCFM cropland accuracy; any study comparing LCFM with WorldCover on cropland.

## Relevance to LandHorizon
- **The "about 77 %" justification:** sourced as a correct citation of the global overall accuracy (claim 1). But it is a weak basis for a 20-point gap rule. It is an all-class, global average. It says nothing about how often cropland is mislabelled, or mislabelled as grassland, in the Galați plain. The one European check I could open (Ireland, low-quality source) shows 66 %, below 77 %. So the figure neither supports nor weakens the 20-point rule directly; it does not bear on it. (Inference.)
- **Wording the report can honestly use:** "Land cover from ESA WorldCover 2021 (10 m). Its published global overall accuracy is 76.7 %; accuracy for cropland in this area has not been checked. The share is an indicator that the flagged area was farmland, not proof." Do not write "77 % accurate" next to a per-plot number. (Inference, from claims 1 and 5.)
- **Better justification for the 20-point rule (inference):** state it as a threshold chosen from our two test cases (98.9 % vs 48.6 %), not derived from map accuracy. Add that an independent cropland reference (LUCAS points near Galați, or the Copernicus HRL Croplands validation) was not used.
- **LCFM replacement:** not supported yet. It has a higher headline accuracy and an open licence, but I found no cropland-specific accuracy and could not confirm a 2024 layer. Keep WorldCover 2021 for the 29 Nov ship date and list LCFM as a roadmap item once a 2024 layer and its cropland UA/PA are confirmed. Note that WorldCover 2021 is a 2021 map applied to a 2024 flood, so crop-to-grass changes after 2021 are not seen. (Inference.)
- **Pipeline, cost, compute:** no change; WorldCover is already open (CC BY 4.0) and LCFM would be a drop-in raster swap. Coverage of Galați is global in both.

## Open questions
- Read PVR V2.0 Tables 2 and 3 by hand: global cropland UA/PA, Europe/Eurasia row, cropland-grassland confusion, sample design.
- Is a 2024 LCFM land cover layer published, and what is its cropland UA/PA? (LCM-10 PVR, land.copernicus.eu, PDF I could not read.)
- A Romanian or lower-Danube check using LUCAS points (EU Eurostat) would answer the local accuracy question directly.
- Fetch-tool note: no instruction-like content was found in any fetched page.

## Review
Reviewer: independent verifier, 2026-11-23. I opened all 7 cited URLs myself. My fetch tool caps verbatim quotes at about 125 characters, so long passages were checked in pieces.

### Verdicts
1. **verified.** Both quotes ("The WorldCover 2021 v200 reaches an overall accuracy of 76.7%." and the 2020 v100 74.4 % sentence) are on the page word for word. The page also says "independently validated by Wageningen University (statistical accuracy)" and "IIASA (spatial accuracy)". The page is undated; official docs is the right type.
2. **verified.** The record says the maps "were generated with different algorithm versions (v100 and v200, respectively)" and contains "changes between the maps should be treated with caution". It also calls v200 "an improved algorithm version", which partly sources the gain. The record has no accuracy figures, so the 76.7 vs 74.4 comparison comes from claim 1. Published 2022-10-28, CC BY 4.0.
3. **verified.** The quote is on the page. Source type: DLR terrabyte is a research data host, not a vendor. It is a secondary source that adds nothing to claim 1, and the page is undated.
4. **verified.** The quote is in Sect. 5.1 of Van Tricht et al., ESSD 15, 5491–5515, published 2023-12-06. The **producer's accuracy of 79.3 (±1.5) is confirmed verbatim**: "a user's accuracy of 80.6 (±1.5) and a producer's accuracy of 79.3 (±1.5)". The comparison is global. The page doesn't say which reference set was used for the WorldCover figure; the WorldCereal figures match the global row of Table 5 (Lesiv et al. 2023b temporary-crop validation set). The binary-vs-multi-class statement is also there: "global cropland maps reach higher accuracies when being the result of a binary classification procedure". Note that WorldCereal is a competing ESA/VITO product, so this is not a neutral check.
5. **verified, low weight.** The quote is there word for word, and the table values match (cropland UA 0.808 ±0.036, PA 0.739 ±0.043, LUCAS 2022, published 27 Oct 2026, author Sean Blaney). It is a one-author tutorial, less than a month old and not reviewed. The LUCAS 2022 points (May 2022 – Feb 2023) are scored against the 2021 map. Use it as an illustration only.
6. **verified.** The record title is "Land Cover 2020 (raster 10 m), global, annual - version 1". The quote is there word for word. Publication date 2025-06-26, validation results published 2026-01-27. The researcher's warning against comparing it with WorldCover is right.
7. **verified.** The quote is there. The licence text also requires attribution when distributing and says users must not "convey the impression to the public that the user's activities are officially ... endorsed by the European Union". The access constraint is "no limitations to public access". "Looks allowed" for a product is a fair reading at medium confidence.
8. **verified.** The article is dated 26.06.2025 and the exact sentence is "...resumes the global Copernicus Land Cover time series—paused in 2019—with new yearly updates from 2020 through 2026." The service "has just launched the first two products", available "for 2020". So the quoted phrase is verbatim, not a tool paraphrase.

Counts: 8 verified, 0 unsupported, 0 misquoted, 0 unreachable.

### What the researcher missed
- **A peer-reviewed European LUCAS check exists (the file lists it as "not found").** Venter et al. 2022, *Remote Sensing* 14(16) 4101, compared WorldCover **2020 (v100)** with LUCAS: "WC had the highest accuracy (71%) compared to DW (66%) and Esri (63%)". Against global ground truth it scored lowest: "Esri had the highest overall accuracy (75%) compared to DW (72%) and WC (65%)". It also found "WC is biased towards over-estimating grass cover". That bias bears directly on the cropland-vs-grassland confusion the file couldn't find. The figures are for v100, not v200. Source: https://www.osti.gov/biblio/1888312 (abstract opened; MDPI full text returned 403: https://doi.org/10.3390/rs14164101).
- **PVR V2.0 has a direct link**: https://pure.iiasa.ac.at/18981/1/WorldCover_PVR_V2.0.pdf (V1.1 for 2020: https://pure.iiasa.ac.at/18980/1/WorldCover_PVR_V1.1.pdf). My tool was blocked too (bot protection), so a person still needs to read Tables 2 and 3. A search summary says the 2020 validation used the CGLS-LC validation dataset, not LUCAS. I haven't verified that.
- **LCFM 2021+ availability:** a search found no released 2021–2024 annual LCM-10 maps. An Oct 2025 webinar FAQ reportedly places the 2020–2021 change product (LCCM-10) in Q2 2026. Not opened by me, treat as a lead: https://land.copernicus.eu/en/events/a-new-era-in-forest-and-land-cover-monitoring/webinar-questions-def.pdf/@@download/file
- **Regional variation:** an EGU25 abstract (Poland, LUCAS) ranks the products differently for forest. It is a lead only, not opened: https://meetingorganizer.copernicus.org/EGU25/EGU25-2557.html

### Problems in "Relevance to LandHorizon"
- **The 20-point rule "chosen from our two test cases" conflicts with the method rules** in `constraints.md`: thresholds and pass criteria are written down before a test is run, and validation is split by event, time or region. A threshold tuned on the same two cases it is then judged on is fitted to them. Present it as provisional, and test it on a held-out event or area, before calling it justified.
- **"LCFM would be a drop-in raster swap" is not backed by any verified claim.** The file has nothing on the LCM-10 legend or class codes, the file format, or how it is distributed (GEE asset, CDSE or Terrascope). Mark it as unverified.
- **The Ireland 66 % figure** (claim 5, blog) is the only European number in the relevance section. Venter et al. (71 % vs LUCAS, Europe, v100) is the stronger independent source and should replace or sit next to it. Neither figure covers Romania.
- The rest is consistent with the constraints: the honest wording, roadmap-only for LCFM, the 2021-map vs 2024-flood caveat, and the 10 m resolution being adequate for the plot sizes.

No instruction-like content was found in the findings file or in any page I fetched.
