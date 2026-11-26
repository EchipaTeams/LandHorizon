# What other free ground-instability data covers Romania, may it be read at plot scale, and what does Imoreview show?
Date: 2026-11-12
Scope: Part A (G3): free landslide / ground-instability data for Romania and the authors' stated scale of use. Part B: the competitor Imoreview, from its public pages only. Out of bounds: EGMS itself, flood data (RO-FLOODS beyond Imoreview naming it), heat and drought. Only claims whose source I opened myself are listed; leads I could not open are under "Open questions". Quotes were returned by the fetch tool's page reader and may be shortened. Re-check before use in a synthesis.

## Claims

### A1. ELSUS v2
1. **Claim:** ELSUS v2 is a 200 m grid with classes 0 (no data) to 5 (very high), distributed as GeoTIFF / ASCII grid.
   - Source: https://esdac.jrc.ec.europa.eu/content/european-landslide-susceptibility-map-elsus-v2
   - Quote: "Cell size: 200 m" ; "0 = no data; 1 = very low; 2 = low; 3 = moderate; 4 = high; 5 = very high" ; "Esri ASCII Grid and GeoTiff file"
   - Source date: 2018-02-12 (release date on page)
   - Source type: official docs
   - Confidence: high
2. **Claim:** The authors state it must not be used for local information. One 200 m cell is 4 ha, so a plot under 1 ha lies inside one cell.
   - Source: https://esdac.jrc.ec.europa.eu/content/european-landslide-susceptibility-map-elsus-v2
   - Quote: "ELSUS v2 is to be viewed at scales up to 1:200,000" ; "should not be used to deduce local information on landslide susceptibility."
   - Source date: 2018-02-12
   - Source type: official docs
   - Confidence: high
3. **Claim:** Access needs ESDAC registration and is free. Commercial use is allowed, but passing the data to third parties is forbidden. The page does not say whether a derived raster or an API output counts as passing data on.
   - Source: https://esdac.jrc.ec.europa.eu/content/european-landslide-susceptibility-map-elsus-v2
   - Quote: "Registration is requested: Yes" ; "They can be used for any purpose, including commercial gain.." ; "under NO CIRCUMSTANCES are these data passed to third parties." ; "Make proper reference to the source of the data when disseminating the results to which this agreement relates."
   - Source date: 2018-02-12
   - Source type: official docs
   - Confidence: medium (derived-product status is unstated)
4. **Claim:** Method is semi-quantitative, using only slope angle, shallow lithology and land cover; the update raised predictive performance by 8 %. No AUC value was found on the page.
   - Source: https://esdac.jrc.ec.europa.eu/node/67026 (Wilde et al., Journal of Maps 2018, abstract)
   - Quote: "combining landslide frequency ratios information with a spatial multi-criteria evaluation model" ; "of three thematic predictors: slope angle, shallow subsurface lithology and land cover." ; "The new version of the map increases the overall predictive performance of ELSUS by 8%."
   - Source date: 2018
   - Source type: peer-reviewed (abstract via ESDAC)
   - Confidence: medium

### A2. Global susceptibility (NASA)
5. **Claim:** The NASA global susceptibility map is a heuristic combination of slope, forest loss, roads, bedrock and faults, built for 2000-2013 conditions. The page gives no resolution.
   - Source: https://science.nasa.gov/earth/earth-observatory/a-global-view-of-landslide-susceptibility-89937
   - Quote: "Steep slopes are the most important factor that make a landscape susceptible to landslides."
   - Source date: 2017-03-30 (page updated 2026-01-31)
   - Source type: official docs
   - Confidence: medium
6. **Claim:** NASA's current LHASA 2.x is a roughly 1 km product, and its repository only encourages users to map susceptibility locally; no data licence is stated on the repository page.
   - Source: https://github.com/nasa/lhasa
   - Quote: "at a 30-arcsecond (~1 km) daily resolution." ; "Users are encouraged to map susceptibility with current information on their own study areas"
   - Source date: not found
   - Source type: official docs
   - Confidence: medium
   - The ~1 km resolution of the older static susceptibility GeoTIFF and its licence: not confirmed from a source I opened.

### A3. Romanian national sources
7. **Claim:** The legal county landslide risk map (Law 575/2001 section V, via HG 447/2003) is made "as a rule" at 1:25,000, county by county. The detailed hazard map at 1:5,000 or larger is a later step that needs geotechnical drilling and testing.
   - Source: https://oot.rmdsz.ro/sites/default/files/HG_447-2003_-_Hartile_de_risc_la_inundatii_si_alunercari_de_teren.pdf (copy of HG 447/2003, Monitorul Oficial 305/2003-05-07; read locally)
   - Quote: "Harta de risc natural la alunecări de teren a judeţului, parte componenta a planului de amenajare a teritoriului judeţean şi/sau zonal, se elaborează, de regula, la scara 1:25.000." (gloss: the county landslide risk map is usually made at 1:25,000); flow chart: "HÂRTII DE HAZARD DE DETALIU Scara 1:5.000 sau mai mare" (gloss: detailed hazard map, 1:5,000 or larger)
   - Source date: 2003-04-10
   - Source type: official docs (legislation)
   - Confidence: high
8. **Claim:** The legal hazard classes are potential low / medium / high, mapped to probability classes from "practic zero" to "foarte mare". These are polygons made by experts from lithology, geomorphology, hydrogeology, seismicity, forest cover and human interventions, not a pixel model.
   - Source: same HG 447/2003 copy
   - Quote: "stabilirea gradelor de potenţial (scăzut, mediu, ridicat) cărora le corespunde o anumită probabilitate de producere a alunecarilor (practic zero, redusă, medie, medie-mare, mare şi foarte mare)" (gloss: potential grades low, medium, high correspond to probability classes from practically zero to very high)
   - Source date: 2003-04-10
   - Source type: official docs (legislation)
   - Confidence: high
9. **Claim:** The county map is a planning document approved through the county council and detailed in urban plans. The norm does not say it is published as open data. I found no GIS file, INSPIRE record or data.gov.ro dataset for Galati.
   - Source: same HG 447/2003 copy
   - Quote: "Harta de risc natural la alunecări de teren este documentul pe baza căruia consiliul judeţean poate declara un areal ca zona de risc la alunecări de teren." (gloss: the map is the document on which the county council may declare a landslide risk zone)
   - Source date: 2003-04-10
   - Source type: official docs (legislation)
   - Confidence: medium for the legal role; "no open GIS file" is an absence of evidence (not found)
   - Galati county map, IGR landslide layer, data.gov.ro / INSPIRE dataset: not found.

### A4. Inventories
   - National inventory (Micu et al.), RO-RISK GIS portal, NE Romania database: leads only, not opened, so no claim. Open access terms: not found.

### A5. Other layers
10. **Claim:** SoilGrids is 250 m and CC BY 4.0, so it is usable in a product with attribution. It is far coarser than a plot and describes soil, not instability.
    - Source: https://docs.isric.org/globaldata/soilgrids/
    - Quote: "The SoilGrids maps are publicly available under the CC-BY 4.0 License" ; "at a spatial resolution of 250 meters"
    - Source date: not found
    - Source type: official docs
    - Confidence: high
11. **Claim:** Published landslide models for the Moldavian region use 30 m DEMs and 1:200,000 geological maps (an AI model for the Republic of Moldova, not Romania). Lithology there is mainly Miocene-Pliocene clay, not loess.
    - Source: https://meetingorganizer.copernicus.org/EGU26/EGU26-20026.html
    - Quote: "lithology, and land cover derived from 30m resolution JAXA DEM and 1:200,000 geological maps"
    - Source date: 2026 (EGU26 abstract)
    - Source type: preprint (conference abstract)
    - Confidence: low (other country, abstract only)
    - Slope-angle screening thresholds from the Copernicus 30 m DEM: not found. European Soil Database, 1:200,000 geological map of Romania, loess / collapsible-soil maps, swelling-clay and subsidence-susceptibility maps: not found (not searched to a result).

### A6. Seismic
    - ESHM20 (CC BY 4.0, EFEHR) and the P100-1 ag zonation: my fetch of the EFEHR page failed (certificate error) and the P100-1 search gave no Galati value. No claim made. Resolution and licence: not confirmed.

### B. Imoreview (vendor pages, fetched 2026-11)
12. **Claim:** Imoreview's ground-motion indicator uses the EGMS Ortho vertical product for 2020-2024, as one mm/year value from the median of a 3x3 block of 100 m cells around the address cell.
    - Source: https://imoreview.ro/miscarea-terenului
    - Quote: "ImoReview folosește produsul vertical EGMS Ortho pentru perioada 2020–2024." ; "Indicatorul este mediana valorilor disponibile dintr-o vecinătate de 3 × 3 celule de 100 m, în jurul celulei adresei." (gloss: the median of the available values in a 3x3 neighbourhood of 100 m cells around the address cell)
    - Source date: not found (page current 2026-11)
    - Source type: vendor
    - Confidence: high
13. **Claim:** It shows a signed number with no classes, thresholds or colours, and warns that a near-zero value is not proof of safety. The page does not describe missing-data handling beyond "available values".
    - Source: https://imoreview.ro/miscarea-terenului
    - Quote: "O valoare negativă indică o coborâre, una pozitivă o ridicare." ; "Nu este o expertiză geotehnică și nu poate confirma sau exclude singură o alunecare de teren." (gloss: it is not a geotechnical survey and cannot alone confirm or rule out a landslide)
    - Source date: not found
    - Source type: vendor
    - Confidence: high (classes/colours "not described on this page" is the reader's report)
14. **Claim:** Imoreview names RO-FLOODS for flood zones, by address. It states a point check does not describe every corner of the parcel.
    - Source: https://imoreview.ro/inundatii
    - Quote: "hărțile oficiale RO-FLOODS" ; "nu descrie fiecare colț al parcelei"
    - Source date: not found
    - Source type: vendor
    - Confidence: medium
15. **Claim:** Missing data is shown by omitting the section and saying so; gaps are not filled.
    - Source: https://imoreview.ro/date-si-surse
    - Quote: "Dacă o secțiune lipsește de pe o pagină, înseamnă că nu avem date verificate pentru acea adresă." ; "Nu completăm spațiile goale cu presupuneri." (gloss: if a section is missing, we have no verified data for that address; we do not fill gaps with assumptions)
    - Source date: not found
    - Source type: vendor
    - Confidence: high
16. **Claim:** The unit is the building or address (building register, cadastre), not a drawn land plot. Reports are free without an account. Only a "negotiation file" is paid; the terms call all content indicative and not a safety certification.
    - Source: https://imoreview.ro/termeni and https://imoreview.ro
    - Quote: "Dosarul de negociere este singurul serviciu cu plată, cu prețul afișat înainte de cumpărare." ; "Fișa blocului tău 19 lei, Dosarul de chirie 29 lei, Dosarul de negociere 79 lei" ; "Informațiile de pe platformă sunt orientative." ; "Gratuit, fără cont."
    - Source date: not found
    - Source type: vendor
    - Confidence: medium (the building-versus-plot reading is from page wording such as "Identitatea clădirii", not a stated rule)
    - Other hazards listed on the homepage: seismic ("Clasa din expertiză și consolidările consemnate") and flood zones. No landslide hazard or other EGMS product level was found.

## Relevance to LandHorizon
- **ELSUS v2:** free, 200 m, commercial use allowed. But the authors say not to deduce local information, and plots of 1 ha or less fall inside a single 4 ha cell. It could only be shown as a regional context line ("region, not plot"), never as a plot score. Registration is manual, and the third-party clause makes shipping a derived COG a legal question for the lead. Cost and compute are minimal if it is used (one 200 m GeoTIFF).
- **NASA global map / LHASA:** about 1 km (LHASA) and licence unconfirmed. Coarser than ELSUS, so no added value in Galati; treat as not worth adding.
- **Romanian legal maps (HG 447/2003):** county maps at 1:25,000 are the only official scale that is close to plot level. No open GIS file or reuse terms were found, so it cannot go into the batch pipeline. A "check the county (PATJ) landslide map with the county council" note is a cheap honest roadmap line.
- **Terrain proxy:** the existing 30 m Copernicus DEM already feeds HAND. A slope layer costs almost nothing, but I found no published slope threshold for a loess lowland, so any threshold would be our own and must be labelled so. Slope is a hint of instability, not ground motion.
- **SoilGrids:** CC BY, 250 m: regional soil context only.
- **Imoreview:** uses the same EGMS Ortho vertical product at the same 100 m grid, but reports per address using a 3x3 median. For a plot it gives no classes, so there is no threshold for us to copy. The differences we can claim: our unit is a drawn plot of any size, and our `unknown` is explicit. It hides missing sections instead of marking them. Imoreview is free, so we cannot compete on price. We cannot say it ignores farmland, since its pages are building-centred.
- **Seismic (item 6):** not established from sources I opened; leave as a roadmap idea only, with licence and resolution still to be confirmed.

## Open questions
- Leads I could not open: the Micu et al. national landslide inventory (about 27,900 to 30,000 records per search summaries, availability said to be limited), the Grozavu & Patriche 2021 national susceptibility map (data availability unknown), Bălteanu et al. 2010 and 2020 (scale statements, downloads), the NASA susceptibility GeoTIFF licence, ESHM20 licence/resolution, P100-1 ag for Galati.
- Is a derived COG from ELSUS "passing data to third parties"? Ask ESDAC.
- Whether a Galati PATJ landslide hazard map exists in digital form: ask Consiliul Județean Galați.
- Out of scope, one line: EGMS levels, accuracy and thresholds are for the EGMS researcher; Imoreview's flood use of RO-FLOODS is for the flood researcher.
- Tool note: some fetched PDFs came back as unreadable binary, and I did not follow any instructions found in fetched content (none seen).

## Review
Reviewer: independent verifier, 2026-11-12. I opened every cited URL with a fetch tool whose page reader returns quotes. For Romanian pages I asked for verbatim text and checked each quoted phrase separately.

### Verdicts
1. **verified.** The ESDAC page has "Cell size: 200 m", the 0–5 coding and "Esri ASCII Grid and GeoTiff file". Release date 12 February 2018 confirmed. The page also gives ETRS89 LAEA and coverage that includes Romania.
2. **verified.** Both quotes are on the page. Geometry nit: 200 m × 200 m = 4 ha is right, but a plot under 1 ha can straddle 2–4 cells, so "lies inside one cell" is not always true. The conclusion (region, not plot) still holds.
3. **verified.** All four quotes are on the page. The page shows "Last updated 12/11/2026", so re-read the terms before relying on them.
4. **verified.** The method, the three predictors and "by 8%" are on the ESDAC node page, and no AUC is given. The node page names neither authors nor journal (it only links to tandfonline). "Wilde et al., Journal of Maps" was not confirmed from the cited page.
5. **unsupported.** The quote is on the page but supports only the steep-slopes point. The rest of the claim is on the same page but not in the quote: forest loss, roads, bedrock/soil strength, faults, the 2000–2013 captions, and the cited "A heuristic approach…" reference. Re-quote those parts and the claim should pass. No resolution is given. Dates confirmed: 2017-03-30, updated 2026-01-31.
6. **unsupported.** "~1 km daily resolution" for LHASA 2 is on the page, but LHASA 2 is an ML daily *probability nowcast*, not a susceptibility map. The "Users are encouraged to map susceptibility…" sentence sits in the legacy **LHASA 1.1** "Data files" section and is advice for replacing that version's global susceptibility input. It is not a statement about LHASA 2. The repo also links a `LICENSE.pdf` that the researcher did not read, so "no data licence is stated" is incomplete rather than established.
7. **unreachable.** The cited oot.rmdsz.ro PDF failed with a TLS certificate error ("unable to verify the first certificate"). The FAOLEX copy (https://faolex.fao.org/docs/pdf/rom197065.pdf) came back as compressed binary that I could not read. A search summary corroborates "de regula, la scara 1:25.000" and the date (10 Apr 2003, MO 305/2003-05-07), but I did not read the text myself. The 1:5,000 flow-chart quote and the drilling requirement are unchecked.
8. **unreachable.** Same source. The quote, the class list and the list of expert factors are unchecked.
9. **unreachable.** Same source. "No GIS file / INSPIRE / data.gov.ro for Galați" is an absence-of-evidence statement and cannot be verified.
10. **verified.** Both quotes are on docs.isric.org. The page gives no data version or date. Its footer reads "Last updated on 2025-12-18" (docs only).
11. **unsupported.** The quote is verbatim (EGU26-20026, Ilinca et al., MaxEnt, Republic of Moldova). However, "Lithology there is mainly Miocene-Pliocene clay, not loess" is not in the abstract. It says only that landslides reflect "structural control by cuesta landforms and Miocene clay-rich lithologies". It mentions no Pliocene and no loess. "Published landslide models" (plural) rests on a single abstract.
12. **verified.** Both Romanian sentences are verbatim on imoreview.ro/miscarea-terenului.
13. **verified.** Both quotes are verbatim, and the page has no classes, thresholds or colours. "Near-zero value is not proof of safety" is the researcher's paraphrase: the page warns in general ("nu poate confirma sau exclude singură o alunecare"; also "Nu certifică stabilitatea versantului…"), not about near-zero values specifically.
14. **verified.** "comparată cu hărțile oficiale RO-FLOODS" and "Verificarea unui punct nu descrie fiecare colț al parcelei…" are on imoreview.ro/inundatii, and the check is by address position.
15. **verified.** Both sentences are verbatim on imoreview.ro/date-si-surse. Side note: that sources page lists neither EGMS nor RO-FLOODS.
16. **misquoted.** The following quotes are not on the cited pages:
    - "Dosarul de negociere este singurul serviciu cu plată…" is not on /termeni. The page instead says "Serviciile cu plată sunt fișele și dosarele pentru o adresă".
    - "Identitatea clădirii" is not on the homepage.
    - The prices are on /termeni, not the homepage. The list has a fourth product, **"Dosarul Plus 179 lei"**.

    The claim "Only a negotiation file is paid" is therefore contradicted. Four paid products exist (19, 29, 79 and 179 lei), plus a free dossier unlocked by three reviews ("Trei recenzii îți deblochează gratuit un dosar"). Some parts are correct: "Gratuit, fără cont." and "Informațiile de pe platformă sunt orientative." are present, and the terms also say "Nu certifică siguranța… unei proprietăți". The building-level reading is supported by other homepage text ("fișa clădirii", "728.500 de clădiri cu fișă"). Source date: /termeni shows "Ultima actualizare: 1 noiembrie 2026" (the researcher wrote "not found").

**Counts:** verified 9 (1, 2, 3, 4, 10, 12, 13, 14, 15). Unsupported 3 (5, 6, 11). Misquoted 1 (16). Unreachable 3 (7, 8, 9).

### What the researcher missed
- **ELSUS confidence map.** ESDAC publishes an ELSUS v2 Confidence Level Map whose coverage names Romania. Any regional ELSUS line should carry it. https://esdac.jrc.ec.europa.eu/content/european-landslide-susceptibility-map-elsus-v2
- **NASA susceptibility GeoTIFF is downloadable.** The LHASA README (1.1 section) links it directly: https://gpm.nasa.gov/sites/default/files/downloads/global-landslide-susceptibility-map-2-27-23.tif. Its resolution and licence are still unchecked, but "no source opened" was avoidable. The repo's LICENSE.pdf is unread. https://github.com/nasa/lhasa
- **New and updated county landslide maps are state-funded.** HG 6/2024 (4 Jan 2024, MO 22/2024-01-11) runs a multi-year national programme funding counties to prepare or update earthquake and landslide risk maps under Law 575/2001 and HG 447/2003. This confirms HG 447/2003 is still the operative norm and that county maps may be in production. Galați is not named. https://legeaz.net/monitorul-oficial-22-2024/hg-6-2024
- **Possible title and amendment drift in HG 447/2003 (unconfirmed: a search-result summary only, I did not open a readable copy).** Copies seem to differ between a landslide-only title and a later one amended to cover flood maps (HG 663/2013 mentioned). Read the consolidated text on legislatie.just.ro before citing.
- **Imoreview paid products and date.** See claim 16: there are four paid products, and /termeni was last updated 1 Nov 2026. https://imoreview.ro/termeni

### Problems in "Relevance to LandHorizon"
- **"Imoreview is free, so we cannot compete on price"** rests on misquoted claim 16. Reading is free, but Imoreview sells per-address files at 19–179 lei. https://imoreview.ro/termeni
- **"It hides missing sections instead of marking them"** is a framing. The page states a convention (a missing section means no verified data). That is a weaker form of explicit `unknown`, but it is not concealment. Phrase it as a UX difference. https://imoreview.ro/date-si-surse
- **NASA "coarser than ELSUS, so no added value"** compares LHASA 2, a daily probability nowcast, with a static susceptibility map (claim 6 unsupported). The conclusion may still hold, but the reason is wrong.
- **Romanian legal maps bullet** rests only on unreachable claims 7–9. It must not reach a synthesis until the HG 447/2003 text is read.
- **Scope gap.** ELSUS, slope and the county landslide maps are landslide susceptibility, not ground motion. Under the constraints, a new hazard is "expensive, out of scope after the 22 Nov gate", and the ground area means ground motion. The section should say plainly that all of these are roadmap or regional-context items, not plot indicators for the 22 Nov–6 Dec window. It also does not mention ELSUS's manual ESDAC registration as a team-time cost under the constraints.
- **ELSUS versus "free and openly licensed data only".** The ELSUS terms need registration and say "under NO CIRCUMSTANCES are these data passed to third parties". That is not an open licence. A COG we derive and serve through the API is plausibly passing data on. Calling it "a legal question for the lead" understates this: under the constraint it is likely disqualifying for product use. Until ESDAC answers in writing, ELSUS is at most a cited regional reference or a roadmap item. Sources: https://esdac.jrc.ec.europa.eu/content/european-landslide-susceptibility-map-elsus-v2 and `docs/research/constraints.md` (Data and money).
- **Labelling slip.** "Seismic (item 6)" points at claim 6 (LHASA). The seismic material is section A6 and has no numbered claim.

### Untrusted content
None of the fetched pages or the findings file contained instructions aimed at the reviewer.
