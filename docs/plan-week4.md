# Week 4 plan: Mon 30 Nov – Sun 6 Dec

By Sunday 6 Dec (feature freeze): the public URL runs the full flow on the 10-year flood history, the deck draft has every "Must fix" item applied, and every pitch claim matches what's built. Thursday 3 Dec is the cloud and deploy workshop.

This first version covers Miriam's work, the two moves agreed on 27 Nov and the Sentinel-2 check (F7, F8). The other segments are added once week 3 closes.

## Moves from week 3 (27 Nov)
- **G4 waits for the full batch (F3).** Matei and Miriam agreed on 27 Nov: the deploy is built once the 10-year `flood_gfm.tif` is on the Drive, so it's sized and tested on the file it will serve. W2 (website deploy) and L10 (plot request end to end) still wait on G4, so G4 comes first this week.
- **L7 (`overall`) stays with Matei**, not handed on.
- **A Sentinel-2 check of the flood dates, labels only** (approved by Matei, 27 Nov, after the #23 review). Each flood date gets "contradicted" (a clear image a few days off shows bare soil, no water), "supported" (it shows water) or no label (no clear image). Nothing is removed from `flood_dates`, `n_flooded` or `flooded_fraction`: a flood can drain before the next clear image, so a dry image doesn't prove there was none. Before anything is built: how many dates have a clear image at all (F7), then the rule on the 12 `floodplain-dry` dates (F8). The pipeline step, the stored layer and the contract field (`optical_check` next to `cropland_share`) are planned only if F8 holds up.

## Deploy, business and law: Miriam

| # | Work to do | Due | Waits on |
|---|---|---|---|
| G4 | Deploy the API: Dockerfile and `docker-compose.yml` (COGs from a volume), a public URL, and a reverse proxy so the website and `/evidence` share one domain ([evidence-request.md](evidence-request.md#deployment-not-decided-yet)). **Before F3 lands:** pick the host and size its disk and memory for the 10-year `flood_gfm.tif`. Update the `docker-compose.yml` line in `architecture.md` (now "planned, W4") | Wed 2 Dec | F3 |
| B4 | Deck draft with every "Must fix" item from the deck review applied (Matei sends the table). Some rows are already settled by decisions since: the score has no number (L6), the EGMS release is 2020-2025 | Sat 5 Dec | — |
| B5 | Check every pitch claim against what's built: the numbers in [flood-validation.md](flood-validation.md), what the cropland share may claim ([DECISIONS.md](research/DECISIONS.md), decision 3), and "unknown, never low". List each claim with its source, or cut it | Sun 6 Dec | B4 |
| B6 | **Stretch**, flood's open F4 question: what grew under 2024's flags outside the polder. WorldCover on the 2024 `flood_gfm.tif` (reuse `checks/cropland_share/cropland_share.py`); log the result in `flood-validation.md`. Agree it with Szilly and Sover first | Thu 3 Dec | — |

## Flood: Szilly, Sover

| # | Work to do | Due | Waits on |
|---|---|---|---|
| F7 | **Count the clear Sentinel-2 images.** For each of the 946 flood dates in the 10-year `flood_gfm.tif` (the `gfm_versions` tag, or the band names), count the Sentinel-2 L2A scenes over the AOI with low cloud cover within ±1, ±3 and ±5 days, from the catalogue's metadata only (no pixels read). Report the share of dates with at least one, per year and for Jan–May, and log it in `flood-validation.md`. If very few dates have one, say so and stop: F8 is dropped and the farmland caveat stays the only signal | Tue 1 Dec | #23 merged |
| F8 | **Agree the rule with Matei, then test it on the 12 `floodplain-dry` dates.** Push the rule before any run, like earlier criteria: the day gap (from F7), the water index (NDWI or MNDWI with SWIR), the thresholds, what counts as a clear image over the plot. Then label the 12 dates on `floodplain-dry-1/2/3` and log the result. No pipeline step, layer or contract field yet | Fri 4 Dec | F7 |

## Lead and API: Matei

| # | Work to do | Due | Waits on |
|---|---|---|---|
| L7 | Implement `overall` in the agreed format (`architecture.md`, *Score format*), if it isn't merged by Sun 29 Nov. Contract change: Misu and Sara regenerate their types | Wed 2 Dec | — |

## Risks
- **G4 has less time.** It starts when F3 lands (due Sat 28 Nov). If F3 slips past Mon 30 Nov, deploy on the 2024 file and swap the file on the volume later: the grid stays the same, so nothing else changes.
- **Spring is cloudy.** F7 may show that most Jan–May dates have no clear image; then the check helps little where the false alarm sits, and that's the result to report, not a reason to widen the day gap until it fits.
- **Miriam carries the deploy and the deck in the same week.** If G4 runs long, B6 is dropped first, then Alex takes the reverse proxy.
