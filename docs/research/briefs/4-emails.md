# Decision 4: emails to the GFM helpdesk and to ANAR/INHGA

## Read
- [DECISIONS.md](../DECISIONS.md):
  - "To do after this review", item 1: the helpdesk questions;
  - section 1a: the 224 missing advisory layers and their track pattern.
- [RECOMMENDATIONS.md](../RECOMMENDATIONS.md):
  - F-1, "Ask the GFM helpdesk";
  - "Do now, no build" (ANAR and INHGA).
- [flood/SYNTHESIS.md](../flood/SYNTHESIS.md): the RO-FLOODS and JRC sections, and "Open after this round".

## Background
There are two outward messages. The chat **drafts** them and the lead **sends** them from their own account. The chat never sends anything and never uses mail connectors.

**1. GFM helpdesk** (through the EFAS or GloFAS contact form, which GFM news items point to)
- **Will the Sentinel-1 archive (2015 to April 2025) be reprocessed with GFM v4, and when?** This decides whether a live product could ever have one consistent v4 history (see decision 1b).
- **Why do some scenes have no `advisory_flags` file?**
  - The catalogue lists the file, but the link returns 404 on 224 of 9,102 scenes over our area (2015–2021 and 2025).
  - Over our AOI they follow one track: 16:00 UTC, every 12 days, missing almost every time from September 2018 to January 2020.
  - Scene IDs are in `checks/advisory_layer/run_2015-01-01_2026-01-01/scenes.json`. Include two or three as examples.

**2. ANAR and INHGA** (the RO-FLOODS flood hazard maps)
- **The request:** the licence and the GIS files of the RO-FLOODS maps. Today they are viewer-only, and a viewer is not a licence.
- **What to cite:** the research suggests Implementing Regulation (EU) 2023/138, which lists natural risk zones as high-value datasets to be published under CC BY 4.0 or equivalent, with bulk download.
  - This is **(R): found by a reviewer, and not confirmed** to apply to these maps.
  - Word it as a question, not a demand.
- **Timing:** replies take weeks.
- **Why it matters:** the answer decides the best flood roadmap item, an official LiDAR-based hazard layer like the one the competitor (Imoreview) shows.

## Why it's the lead's call
Both messages go out in the project's name. Who sends them, from which address and in which language is the lead's choice.

## Options
| Option | Cost | What it gets |
|---|---|---|
| Send both by 15 Nov (as planned) | About 1 h to finalise and send | Answers in time for the pitch, if they come |
| Helpdesk only | Less | Nothing on RO-FLOODS; the roadmap item stays "viewer only" |
| Neither | None | Both questions stay open; say so in the limits |

## Coordinator's recommendation
- **Send both.** Neither answer is needed for the build, so nothing blocks on them. But both are cheap, and the replies strengthen the roadmap and the limits section.
- **Write the ANAR/INHGA message in Romanian.** Say it is a student project with a product pilot, because the licence question is about product use, not only research.

## Questions for the lead
1. Send both, one, or neither?
2. Who sends, and from which address (personal or university)?
3. Romanian for ANAR/INHGA and English for the helpdesk?

Next step: ask the chat for the drafts, review them, then send them yourself.

## Drafts (for the lead to review and send)

### 1. GFM helpdesk (English, through the EFAS/GloFAS contact form)
**Subject:** GFM archive: v4 reprocessing and missing advisory_flags files (tile EU020M E060N012T3)

> Hello,
>
> I lead a student team project, LandHorizon, that uses the GFM archive from the EODC STAC catalogue to build a flood history for small plots near Galați, Romania. I have three questions.
>
> **1. Reprocessing with v4.** The versioning page says layers from different major versions can't be used together, so our history stops at the last v3 scene over our area (13 April 2025). Is the Sentinel-1 archive from 2015 to April 2025 going to be reprocessed with v4? If so, roughly when?
>
> **2. Missing advisory_flags files.** On 224 of 9,102 scenes over our area, the STAC item lists an `advisory_flags` asset but the file returns HTTP 404. The scenes are from 2015–2021 and 2025. Over our area they follow one track: around 16:00 UTC, every 12 days, missing at nearly every repeat from September 2018 to January 2020. A few more are at 04:12 UTC between November 2015 and May 2016. Examples:
> - `ENSEMBLE_FLOOD_20180912T160007_VV_EU020M_E060N012T3`
> - `ENSEMBLE_FLOOD_20190603T160007_VV_EU020M_E060N012T3`
> - `ENSEMBLE_FLOOD_20191212T160013_VV_EU020M_E060N012T3`
>
> Is this a known gap, and what causes it?
>
> **3. Regenerating the files.** Could the missing `advisory_flags` files be generated and published? We count a scene without an advisory layer as not observed. Over our area this removes about 8 % of the observations from 2015 to 13 April 2025, and about 15 % from September 2018 to January 2020. A regenerated file would bring its scene back into our history with no change on our side.
>
> I can send the full list of scene IDs if that helps. Thank you for making GFM openly available.
>
> Best regards,
> Matei Tanase
> LandHorizon student project, [university]

Figures: 8.15 % and 15.5 % (decision 1a, Lead's choice). 8 % is the headline because the whole period was fixed before the count. The scene list is in `checks/advisory_layer/run_2015-01-01_2026-01-01/scenes.json` (`has_advisory: false`).

### 2. ANAR, with INHGA in copy (Romanian)
**Subiect:** Cerere de informații: licența și fișierele GIS ale hărților de hazard și risc la inundații (RO-FLOODS)

> Bună ziua,
>
> Mă numesc Matei Tanase și coordonez LandHorizon, un proiect al unei echipe de șapte studenți de la [universitatea]. Construim o platformă web care, pentru un teren desenat de utilizator în zona Galați, arată inundațiile observate din satelit (Copernicus, Sentinel-1), relieful și mișcările terenului. Proiectul are și o componentă de pilot de produs, așa că ne interesează condițiile de utilizare și dincolo de cercetare.
>
> Hărțile de hazard și risc la inundații din proiectul RO-FLOODS, publicate pe inundatii.ro, ar fi cea mai bună sursă oficială pentru zona noastră. Am găsit doar vizualizarea online, fără o licență și fără o opțiune de descărcare. Vă rugăm să ne spuneți, dacă se poate:
>
> 1. Sub ce licență pot fi folosite aceste hărți, inclusiv într-un produs, nu doar în cercetare?
> 2. Putem obține fișierele GIS (de exemplu GeoTIFF sau shapefile) pentru zona Galați (confluența Siretului și a Prutului cu Dunărea)? Dacă da, în ce format, la ce rezoluție și pentru ce scenarii de probabilitate?
> 3. Se aplică acestor hărți Regulamentul de punere în aplicare (UE) 2023/138? Acesta include zonele de risc natural printre seturile de date cu valoare ridicată, care se publică sub licența CC BY 4.0 sau una echivalentă, cu posibilitate de descărcare în masă. Nu suntem siguri că regulamentul acoperă aceste hărți și am aprecia o lămurire.
>
> Dacă cererea trebuie trimisă altui departament sau formulată ca cerere în baza Legii nr. 544/2001, vă rugăm să ne spuneți.
>
> Vă mulțumim,
> Matei Tanase
> Proiectul studențesc LandHorizon, [universitatea]

Notes for the lead:
- **Question 3 is (R):** nobody confirmed that 2023/138 covers RO-FLOODS, so it stays a question.
- **Addresses:** none are recorded in the research. Take them from the official ANAR (rowater.ro) and INHGA (inhga.ro) sites.
- **Law 544/2001:** this is optional leverage. A request under 544/2001 must be answered within 10 days, or 30 for complex requests. Use it if there is no reply by early December.

## Lead's choice
**Choice (23 Nov 2026): send both.**
- **Sender:** the lead (Matei), from their personal account.
- **Languages:** English for the GFM helpdesk; Romanian for ANAR, with INHGA in copy.
- **Helpdesk message:** three questions. The third, added from decision 1a, asks GFM to regenerate the missing `advisory_flags` files.
- **Drafts:** above.
- **Date sent:** not sent yet. The lead fills it in after sending.
- **Open:** the lead asked the coordinator on 23 Nov whether any other outward emails are needed.
