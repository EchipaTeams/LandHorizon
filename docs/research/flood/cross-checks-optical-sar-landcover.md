# Which checks from outside GFM does published work support for separating flood water from smooth/tilled bare soil in Sentinel-1 flood maps, and what would each take for us?
Date: 2026-11-11
Scope: In: Sentinel-2/Landsat optical cross-checks, SAR-only cues (coherence, VH, time-series references), land-cover/crop masks, HAND as a plausibility check, free access routes and licences. Out: GFM's own layers, flags, algorithms and validation; modelled hazard; ML mappers. Quotes were taken from pages I opened; several fetches returned only short or summarised text, so quotes are short. Many sources came back 403 or unreadable (see Open questions): those are not cited.

Headline: I found **no published study that quantifies Sentinel-1 false alarms specifically on freshly tilled fields and tests a fix against an independent reference**. What exists is indirect (items 1, 2, 7, 8). Gaps are marked "not found".

## Claims

### A. Optical cross-check (Sentinel-2 / Landsat)
1. **Claim:** A published S1 flood algorithm (S1-L1, arid regions) uses Sentinel-2 SAVI to identify harvested cropland and excludes smooth, persistently low-backscatter surfaces from its "definitely land" reference. It was checked against Sentinel-2 clear-view maps for 2020 events (Ghana, Congo). Evidence is for arid zones, not tilled temperate fields.
   - Source: https://meetingorganizer.copernicus.org/EGU21/EGU21-6982.html
   - Quote: "known agricultural land-use areas with low values of Sentinel-2 based Soil Adjusted Vegetation Index (SAVI) are used to identify harvested croplands."
   - Source date: 2021 (EGU General Assembly, 19-30 Apr 2021)
   - Source type: preprint (conference abstract, not peer-reviewed)
   - Confidence: low (abstract only; SAVI is used to flag cropland, not to confirm water)
2. **Claim:** The same abstract excludes smooth surfaces from the land reference when backscatter is below the median.
   - Source: https://meetingorganizer.copernicus.org/EGU21/EGU21-6982.html
   - Quote: "Smooth surfaces and radar shadow regions, which exhibit backscatter lower than the median value"
   - Source date: 2021
   - Source type: preprint (conference abstract)
   - Confidence: low
3. **Claim:** Cloud-free optical imagery is often missing at flood time. Across about 2,000 European river sites, Sentinel-1 could potentially observe 58 % of flood events and Sentinel-2 only 28 %. This counts observable events, not the SAR-to-optical time gap; a per-event gap distribution was not found.
   - Source: https://nhess.copernicus.org/articles/22/2473/2022/
   - Quote: "on average 58 % of flood events are potentially observable by Sentinel-1"
   - Source date: 2022-08-02
   - Source type: peer-reviewed
   - Confidence: high (second figure: "only 28 % by Sentinel-2 due to the cloud coverage", same page; synthetic study assuming two satellites per mission)
4. **Claim:** Sentinel-2 nominal revisit with two satellites is 5 days (at the equator; no mid-latitude figure on the page). MNDWI uses green and B11 (SWIR, 20 m). Cloud reliance remains the stated limit of optical methods. No fixed MNDWI threshold is given: Otsu on each scene is used. A literature statement says MNDWI performs well over crops, but this concerns optical water mapping, not rejecting SAR false alarms.
   - Source: https://sentiwiki.copernicus.eu/web/s2-mission ; https://eo.copernicus.org/articles/1/43/2026/
   - Quote: "the nominal constellation operations configuration revisit is 5 days" (SentiWiki); "reliance on cloud-free conditions remains a constraint of optical approaches." and "MNDWI excelled in agricultural (crops), forested, and artificial/urban surface contexts." (Almoadi)
   - Source date: SentiWiki n/d; Almoadi 2026-08-06
   - Source type: official docs (SentiWiki); peer-reviewed (Almoadi, an urban-flood paper)
   - Confidence: medium for revisit and cloud limit; low for the MNDWI-on-crops statement (a review sentence inside an urban study)
5. **Claim:** Dynamic World (Sentinel-2 based, 10 m, 2015-06 to present, CC BY 4.0) has a per-pixel "crops" probability and a stated 2-5 day revisit. It also has a water class, so it could serve as a cheap optical land-cover cross-check; no flood-mapping study using it to reject SAR false alarms on cropland was found.
   - Source: https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1
   - Quote: "The revisit frequency of Sentinel-2 is between 2-5 days depending on latitude."
   - Source date: catalog page fetched 2026-11-11
   - Source type: official docs
   - Confidence: medium (revisit and crops class quoted from page; water-class point is from my knowledge, not quoted)

### B. SAR-only cues
6. **Claim:** Time-series change-detection with a one-year Bayesian baseline still misclassified agricultural change as flood (Nova Kakhovka 2023 dam flood: precision 0.52, recall 0.46, F1 0.49 overall). Independent reference: UrbanSARFloods benchmark. Bare soil is not discussed.
   - Source: https://arxiv.org/html/2504.19526v4
   - Quote: "vegetation growth and harvest activities that can create backscatter changes similar to flooding"
   - Source date: 2025-10-11
   - Source type: preprint
   - Confidence: medium (the quote is cited from the paper's section 6.4 via the fetch tool; numbers from Table 3)
7. **Claim:** A TU Wien study of the Bayesian algorithm used in GFM proposes a HAND prior instead of a HAND mask, reducing false negatives at the cost of slightly more false positives. This is evidence that terrain cues trade off against false alarms and do not remove agricultural ones.
   - Source: https://repositum.tuwien.at/bitstream/20.500.12708/190681/1/Tupas-2023-Water-vor.pdf
   - Quote: "Our results show enhanced performance by decreasing false negatives at the cost of slightly increasing false positives."
   - Source date: 2023
   - Source type: peer-reviewed (Tupas et al., "Improving Sentinel-1 Flood Maps Using a Topographic Index as Prior in Bayesian Inference")
   - Confidence: medium (abstract only; body text was unreadable)
8. **Claim:** Precomputed Sentinel-1 coherence exists, free and global, but only as a Dec 2019 - Nov 2020 seasonal-median climatology with no updates. It covers Romania (latitude range 79S-82N) but cannot give coherence for a 2024 flood pass. Coherence for specific event pairs needs SLC pairs processed ourselves. CC BY 4.0, tiled COGs on AWS Open Data.
   - Source: https://registry.opendata.aws/ebd-sentinel-1-global-coherence-backscatter/
   - Quote: "Global coverage comprises all land masses and ice sheets from 82 degrees northern to 79 degrees southern latitude."
   - Source date: n/d (data Dec 2019 - Nov 2020)
   - Source type: official docs
   - Confidence: high for existence, licence and period ("No updates are currently produced."); not found for any test of this product against bare-soil flood false alarms
9. **Claim:** Coherence-based flood mapping is published (Chini et al., Houston/Harvey, urban, validated against very-high-resolution optical images and FEMA model). Evidence for bare agricultural soil: not found in sources I could open.
   - Source: https://api.crossref.org/works/10.3390/rs11020107
   - Quote: "This paper presents an automatic algorithm for mapping floods."
   - Source date: 2019-01-09
   - Source type: peer-reviewed (metadata record only)
   - Confidence: low (quote supports only existence of the method; the urban scope is from the record's summary)

### C. Land cover / crop masks
10. **Claim:** ESA WorldCover is 10 m, years 2020 and 2021, free with no restriction of use (CC BY 4.0). The page does not list the classes.
    - Source: https://esa-worldcover.org/en/data-access
    - Quote: "The ESA WorldCover product is provided free of charge, without restriction of use."
    - Source date: n/d (versions v100 2020, v200 2021)
    - Source type: official docs
    - Confidence: high for licence and resolution
11. **Claim:** EU crop type map (EUCROPMAP) is 10 m, 2018 (also 2022), CC-BY-4.0, built from Sentinel-1 and LUCAS in situ data. It is built from the same sensor, so errors may correlate; no flood-use study found.
    - Source: https://developers.google.com/earth-engine/datasets/catalog/JRC_D5_EUCROPMAP_V1
    - Quote: "European crop type maps based on Sentinel-1 and LUCAS Copernicus 2018 in-situ observations for 2018"
    - Source date: catalog fetched 2026-11-11
    - Source type: official docs
    - Confidence: medium
12. **Claim:** Corine Land Cover 2018 is 25 ha / 100 m, 6-yearly: far coarser than a 1 ha plot. The page fetched states no licence.
    - Source: https://land.copernicus.eu/en/products/corine-land-cover/clc2018
    - Quote: "25 ha/100 m"
    - Source date: n/d (2017-2018)
    - Source type: official docs
    - Confidence: medium (licence not found on that page)
13. **Claim:** JRC Global Surface Water monthly recurrence gives per-month water seasonality at 30 m, 1984-2022, free without restriction. It can say whether a pixel has ever been water in a given month, which is a flag-not-remove prior.
    - Source: https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_MonthlyRecurrence
    - Quote: "monthly measures of the seasonality of water based on the occurrence values detected in that month over all years."
    - Source date: catalog fetched 2026-11-11
    - Source type: official docs
    - Confidence: medium (permanent-water use is conventional; its use as an agricultural-false-alarm flag is my inference, not a published result)

### D. Terrain
14. **Claim:** Exclusion masks (including HAND) are common practice in global SAR flood products, and the literature I could open moves from hard masks to HAND priors because masks cost recall. No source I opened treats a case where the false alarm sits below 1 m HAND; none says a HAND filter helps there.
    - Source: https://repositum.tuwien.at/bitstream/20.500.12708/190681/1/Tupas-2023-Water-vor.pdf
    - Quote: "Applying exclusion masks to improve the results is common practice in unsupervised and global applications."
    - Source date: 2023
    - Source type: peer-reviewed
    - Confidence: medium for the first half; "not found" for the sub-1 m case

### E. Free access routes and terms
15. **Claim:** CDSE: Sentinel data free, full and open. General-user limits: 2000 requests/min (S3), 4 concurrent connections, 12 TB/month transfer; openEO 10,000 credits/month (footnoted as a temporary boost announced 3 Sep 2024).
    - Source: https://documentation.dataspace.copernicus.eu/Quotas.html ; https://dataspace.copernicus.eu/terms-and-conditions
    - Quote: "The access and use of Copernicus Sentinel data is available on a free, full and open basis"
    - Source date: n/d (quota page fetched 2026-11-11)
    - Source type: official docs
    - Confidence: high for licence; medium for credits (may revert)
16. **Claim:** Google Earth Engine is free only for noncommercial use.
    - Source: https://earthengine.google.com/noncommercial/
    - Quote: "You are an individual developer using Earth Engine for noncommercial purposes."
    - Source date: n/d
    - Source type: official docs
    - Confidence: medium (eligibility list; a commercial product would need a paid plan)
17. Microsoft Planetary Computer and Earth Search (AWS) terms and quotas: not found (the Planetary Computer page returned no usable text; Earth Search not fetched). Landsat as a cross-check: not found. Cloud-free Sentinel-2 statistics for south-east Europe: not found.

## Relevance to LandHorizon
- **Optical cross-check is the only option with a direct independent-sensor logic, but with a hard cap.** Claim 3 says Sentinel-2 sees about 28 % of floods EU-wide because of cloud. For our spring case, the 29 Apr image already existed, so it works as a *rejection* test: "clear Sentinel-2 within N days shows no water, SAR says flooded -> flag as doubtful". It cannot *confirm* floods in cloud, so the rule must produce `unknown`/"low confidence", never "no flood". Whether a clear image exists within N days for most Galati passes: not found; we would have to count it ourselves in the batch (STAC query over about 9,000 passes, cheap metadata only).
- **Thresholds:** no published fixed MNDWI threshold for confirming SAR detections (Otsu per scene is common). Any threshold we pick (e.g. an MNDWI cut) must be pre-registered and tested on events outside the polder case; the 30 Apr case alone is tuning, not validation. Timing: a flash flood may drain in days, so a clear image with a gap of several days can falsely "reject" a real flood; the gap limit has to be fixed in advance.
- **Cost:** Sentinel-2 L2A on CDSE (free, full and open; quotas generous for a one-off batch) or via GEE (noncommercial only; the product's commercial status conflicts with GEE terms, see `constraints.md`). Compute: a per-pass flag for about 9,000 passes is metadata-scale plus one B3/B11 pixel read per clear scene; fits free tiers. Code size is small and explainable.
- **SAR-only cues:** no free precomputed coherence for 2015-2025 (claim 8; the 2019-20 climatology is not event-specific). Event coherence needs SLC pairs (large downloads, SNAP/ISCE-style processing): likely a roadmap item, not before 6 Dec. A seasonal baseline helps in principle but published agricultural cases still fail (claim 6) and GFM's no-flood reference problem is the same; I found no result showing it fixes tilled soil.
- **Masks:** a cropland mask is available free (WorldCover 10 m, EUCROPMAP 10 m, Dynamic World), but removing cropland removes the users' real floods. The defensible form is to *flag* "arable land, spring tillage window, single-season detection" as low confidence and keep the pixel count separate; no published tests of such a flag were found. CLC at 100 m is too coarse for sub-hectare plots. Cropland masks do not tell tilled from not tilled in a given week; Sentinel-2 bare-soil/vegetation index (SAVI in claim 1) would.
- **Terrain:** HAND cannot help for the polder (sub-1 m above river): it passes every true and false pixel. Literature only supports it for removing hill/urban false alarms.
- **Independence of validation:** claims 1 and 6 have independent references only for their own cases; for tilled soil specifically, none found. Our own spring test (1 % limit) remains the only pre-registered check and any cross-check should be judged on it plus an event-split test.
- **Coverage:** Romania is covered by all datasets above; CLC, WorldCover and crop maps are static yearly (2018-2021) so they do not describe a 2024 field's state.

## Open questions
- Sources I could not open (403/unreadable) but which search results suggest are relevant: Moya et al. 2019 (Japan, agricultural false detections in change detection and "conditional coherence"), Alonso-Sarria et al. (SE Spain S1 vs S2 validation), a South Africa HAND 10 m threshold paper, Cerbelaud et al. 2021, Chini 2019 full text, Tupas 2024 (GISScience & Remote Sensing; exponential filter against agricultural overestimation), Mekong Otsu paper (Sentinel-2 agreement is weaker over paddy fields according to its record). A reviewer with access should open these.
- Empirical question we can answer ourselves: share of Galati S1 passes with a clear Sentinel-2 image within 1, 3, 5 days (not published).
- Does Sentinel-2 B11/B12 bare-soil moisture reject tilled soil as well as MNDWI? Not found.
- (Out of scope) GFM likelihood/advisory layers were left to other researchers.

## Review
Reviewed: 2026-11-11, by a reviewer who did not write this file.

How it was checked: every cited URL was opened on 2026-11-11. The fetch tool returns page text in short excerpts, so each quote was confirmed by an exact-string check, not by reading the full page. The Tupas 2023 PDF body came back as binary; its abstract was confirmed from the PDF metadata and from the TU Wien repository record (https://repositum.tuwien.at/handle/20.500.12708/190681). No fetched page and nothing in this file contained instructions addressed to the reviewer.

### Verdicts
1. `verified`. Both halves of the quote are in the abstract. Smooth surfaces are excluded from the "definitely land" pixels; test events are Ghana (Sept 2020) and Republic of the Congo (Nov 2020). Two limits to carry along: the reference was "Sentinel-2 clear view coincident optical maps" **and** expert-classified Sentinel-1 maps, so it is only partly independent; the authors are from Cloud to Street PBC (a flood-mapping vendor) and the abstract was never peer-reviewed, so the "50 % fewer false positives" it reports has no independent validation.
2. `verified`. Quote is exact; the sentence continues "are excluded from the DL pixels".
3. `verified`. Quote exact, including "due to the cloud coverage". 1,957 gauge stations; the paper calls itself "a synthetic study" and assumes two satellites per mission. Missed in the claim: the same paper gives single-satellite figures of about 20 % (Sentinel-1) and 9-10 % (Sentinel-2).
4. `verified`. SentiWiki quote exact; B11 is listed among the 20 m bands on the same page. Almoadi quotes exact; date 06 Aug 2026 and peer-reviewed status confirmed; Otsu per scene confirmed ("the Otsu threshold was calculated independently from the full-scene histogram"). The "MNDWI excelled" sentence is in the Introduction and reports Albertini et al. (2022), not Almoadi's own result, and the paper itself is one urban flash flood in arid Saudi Arabia. The researcher's "low" confidence for that part is right.
5. `verified`. Quote exact; 10 m, start 2015-06-27, CC-BY 4.0 confirmed. The `water` band ("Estimated probability of complete coverage by water") is on the page, so the water-class point is now sourced. The page also lists a `bare` band, which the claim does not mention.
6. `unsupported`. The quote is in section 6.4 word for word and the numbers match Table 3 (BCP 0.52 / 0.46 / 0.49). Two parts of the claim go beyond the source:
   - "still misclassified agricultural change as flood" is stronger than the paper. The full sentence is hedged: "This limitation **appears related to** the complex temporal patterns of vegetation growth and harvest activities that can create backscatter changes similar to flooding." The paper reports "challenges in distinguishing flood inundation from other changes in agricultural regions"; it does not show that the false positives sat on farmland.
   - "Independent reference" is not supported. The paper describes UrbanSARFloods as a Sentinel-1 benchmark whose labels combine "semi-automatic labeling through conventional remote sensing techniques" with manual verification using PlanetScope and UAV imagery. That is not an independent-sensor reference in the sense of `constraints.md`.
   - Usable restatement: "BCP on a one-year Sentinel-1 series scored P 0.52 / R 0.46 / F1 0.49 at Nova Kakhovka against UrbanSARFloods labels; the authors suspect crop growth and harvest." Also: arXiv now lists a related DOI, https://doi.org/10.1109/TGRS.2025.3620907 (IEEE TGRS), so a published version probably supersedes the preprint. Not opened.
7. `verified`, first sentence only. Quote exact; Water 15(23), 4034, DOI 10.3390/w15234034, peer-reviewed. The link to GFM is not in the abstract; it comes from the repository record, which lists the GFM project (contract 939866-IPR-2020) as funding. The second sentence ("do not remove agricultural ones") is the researcher's inference: the readable text is about rugged terrain and does not mention agriculture. Do not cite it as a finding of the paper.
8. `verified`. Coverage quote exact; "1-Dec-2019 to 30-Nov-2020", "No updates are currently produced.", CC BY 4.0 and COG tiles all confirmed. Not stated in the claim: pixel spacing is 3 arcsec (about 90 m) in the 1x1 degree tiles and 0.01 degree in the mosaics, far coarser than a plot. The sentence "needs SLC pairs processed ourselves" is not from this source and is too strong (see Missed, ASF HyP3).
9. `verified`. Quote exact. Validation data named in the abstract: very-high-resolution optical images, DigitalGlobe crowdsourced points and the FEMA inundation model. The abstract's next sentence mentions bare soil only as what backscatter already detects ("not only inundated bare soils, but also floodwater in urban areas"); it is not evidence about tilled-soil false alarms.
10. `verified`. Quote exact; v100 (2020) and v200 (2021); the page links the Creative Commons Attribution 4.0 licence; "11 classes" are mentioned but not listed.
11. `verified`. Quote exact; 10 m; CC-BY-4.0. Correction to the caveat: the page says the **2022** map combines Sentinel-1 **and Sentinel-2**, so "same sensor" holds fully for 2018 only. The page does not name Romania; coverage is inferred from the bounding box.
12. `verified`. "25 ha/100 m", "6-yearly", 2017-2018 confirmed; no licence text on the page (it points to the CLMS data policy).
13. `verified`, with a correction: the page says surface water "from 1984 to 2021" (availability ends 2022-01-01, exclusive), so the period is 1984-**2021**, not 1984-2022. Quote, 30 m and "free of charge, without restriction of use" confirmed. The use as a false-alarm flag is the researcher's inference, as stated.
14. `verified` for the quoted sentence. "The literature ... moves from hard masks to HAND priors" rests on this one paper; read it as "one TU Wien study". The "not found" for the sub-1 m case stands.
15. `verified`. 2000 requests/min ("Only applies to S3"), 4 concurrent connections, 12 TB/month (then 1 MB/s), and "10 000" openEO credits with the footnote "Temporary Boost of monthly openEO Credits to 10 000", published 3 Sep 2024. Terms quote exact. This also confirms the *(course notes)* openEO figure in `constraints.md`, with the caveat that it is called temporary.
16. `verified`. Quote exact. The page lists eligibility categories only; it gives no quota figure.
17. No verdict: "not found" statements, no source cited.

Count: 15 verified (7 and 13 with corrections), 1 unsupported (6), 0 misquoted, 0 unreachable.

### What the researcher missed
- **Free on-demand coherence exists.** ASF HyP3 processes Sentinel-1 InSAR pairs on request: a "free allotment of 8,000 credits per month", 10-15 credits per full-scene pair, less for burst pairs, and "GeoTIFFs are created for amplitude, coherence, and unwrapped phase by default". So event coherence does not need large SLC downloads or our own SNAP/ISCE chain. Limits: pixel spacing is 80 m by default, 40 m optional (20 m for burst jobs), and it is still a new product type for the pipeline. https://hyp3-docs.asf.alaska.edu/using/credits/ ; https://hyp3-docs.asf.alaska.edu/guides/insar_product_guide/
- **Closest published evidence on agricultural false alarms, openable at abstract level.** Both are listed under Open questions as unopened:
  - Tupas et al. 2024, GIScience & Remote Sensing 61(1), DOI 10.1080/15481603.2024.2427304: the time-series analysis "confirms increased false positive rates due to well-known environmental drivers" and "highlights issues with agricultural overestimation"; an exponential-filter no-flood reference is reported as "effectively reducing false positive rates on non-flooded scenes in most study sites", with "difficulties with sites with prolonged floods". Reference: CEMS and Sentinel Asia semi-automatic maps. It concerns the TU Wien algorithm (inside GFM, so partly outside this file's scope) and is not a fix we can apply to GFM output. Abstract only; full text not read. https://repositum.tuwien.at/handle/20.500.12708/206671
  - Moya et al. 2019, Remote Sensing 11(19), 2320: "the change detection method generated significant misclassifications for agricultural targets"; proposes "conditional coherence"; uses "a field survey of 35 paddy fields located within the misclassified area". Paddy fields in Japan, not tilled dry soil. Abstract only. https://api.crossref.org/works/10.3390/rs11192320
  - Neither overturns the headline ("no study on freshly tilled fields with a tested fix"), but they are nearer to it than claims 1, 2, 7 and 8.
- **Newer land-cover products.** WorldCover (2020, 2021) has a Copernicus successor: LCFM's 10 m Global Land Cover Map, first released 26 Jun 2025 for 2020, with "new yearly updates from 2020 through 2026" announced. Which years are out today was not checked. https://land.copernicus.eu/en/news/lcfm-a-new-chapter-in-global-land-cover-monitoring
- **CLC is not the only Copernicus land cover for Europe.** CLCplus Backbone 2023 is a 10 m raster for Europe (temporal extent 2022-2024). It removes the "100 m is too coarse" objection and is closer to 2024 than any mask cited. Class list and licence text were not on the page fetched. https://land.copernicus.eu/en/products/clc-backbone/clcplus-backbone-2023-raster-10-m-europe-2-yearly
- **Sentinel-2 revisit is not 5 days for the whole 2015-2025 batch.** SentiWiki: "The revisit frequency of each single Sentinel-2 satellite is 10 days", and Sentinel-2B was not yet flying in 2015-2016. Tarpanelli et al. put single-satellite Sentinel-2 observability at about 9-10 %. An optical cross-check will be much weaker for the first years. https://sentiwiki.copernicus.eu/web/s2-mission ; https://nhess.copernicus.org/articles/22/2473/2022/
- **Access route.** Dynamic World, EUCROPMAP and JRC GSW are cited only through the Earth Engine catalogue. Using them that way falls under the Earth Engine noncommercial terms and the 150 EECU-h quota; download routes outside Earth Engine were not checked. https://earthengine.google.com/noncommercial/

### Problems in "Relevance to LandHorizon"
- **Ignores the new-sensor gate.** `constraints.md` rates "a new sensor" as "expensive, out of scope after the 22 Nov gate". Sentinel-2 is a new sensor for this pipeline, and the section presents the optical cross-check as small and cheap without saying whether it lands before 22 Nov or is a roadmap item.
- **The cost estimate does not match the architecture and has no verified claim behind it.** "one B3/B11 pixel read per clear scene; fits free tiers" assumes a per-plot read. Plots are drawn at request time and the API only reads precomputed COGs, so the cross-check has to be computed over the whole AOI for every pass with a clear image and written to a COG. No credit or time estimate for that is given.
- **The 28 % "hard cap" is the wrong statistic for a rejection test.** Claim 3 measures cloud during floods. The false alarms to reject fall on dry spring days, when cloud is probably lower. The share of passes with a clear image is unmeasured either way, as the Open questions admit, so "about 28 %" should not be quoted as the coverage of the rule.
- **No verified claim shows an optical rejection rule working.** Claim 1 uses SAVI to find harvested cropland in arid regions (low confidence, vendor abstract); claim 4 is about optical water mapping. "Sentinel-2 bare-soil/vegetation index ... would" tell tilled from untilled is a hypothesis, not a finding. The only evidence that Sentinel-2 separates the two is our own 29 Apr 2024 image (`docs/architecture.md`), which is the tuning case.
- **SAR-only cost is overstated.** "Event coherence needs SLC pairs (large downloads, SNAP/ISCE-style processing)" is contradicted by ASF HyP3 (above). Roadmap is still the likely answer, for resolution and time reasons, not for compute.
- **"HAND cannot help for the polder (sub-1 m above river): it passes every true and false pixel"** is not backed by a claim or a measurement. `architecture.md` records "Danube bank about 1 m" at one spot, not HAND under the flagged pixels. It is cheap to check against `hand.tif` and should be checked before it is used as an argument.
- **"Literature only supports it for removing hill/urban false alarms"**: claims 7 and 14 concern rugged terrain only; nothing verified here covers urban.
- **"claims 1 and 6 have independent references"**: not for claim 6 (labels are derived from Sentinel-1 with optical verification), and only partly for claim 1 (reference includes expert-classified Sentinel-1 maps).
- **"the product's commercial status conflicts with GEE terms, see `constraints.md`"**: `constraints.md` says the free tier is non-commercial and commercial use is paid. It does not say the product is commercial. The caution is reasonable; the citation is wrong.
- **Masks paragraph** relies on the "same sensor" caveat for EUCROPMAP, which is wrong for the 2022 map (Sentinel-1 + Sentinel-2), and on CLC being the only Copernicus option (see CLCplus Backbone above). "Static yearly (2018-2021)" should be revisited with the newer products.
