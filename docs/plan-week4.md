# Week 4 plan: Mon 30 Nov – Sun 6 Dec

By Sunday 6 Dec (feature freeze): the public URL runs the full flow on the 10-year flood history, the deck draft has every "Must fix" item applied, and every pitch claim matches what's built. Thursday 3 Dec is the cloud and deploy workshop.

This first version covers Miriam's work and the two moves agreed on 27 Nov. The other segments are added once week 3 closes.

## Moves from week 3 (27 Nov)
- **G4 waits for the full batch (F3).** Matei and Miriam agreed on 27 Nov: the deploy is built once the 10-year `flood_gfm.tif` is on the Drive, so it's sized and tested on the file it will serve. W2 (website deploy) and L10 (plot request end to end) still wait on G4, so G4 comes first this week.
- **L7 (`overall`) stays with Matei**, not handed on.

## Deploy, business and law: Miriam

| # | Work to do | Due | Waits on |
|---|---|---|---|
| G4 | Deploy the API: Dockerfile and `docker-compose.yml` (COGs from a volume), a public URL, and a reverse proxy so the website and `/evidence` share one domain ([evidence-request.md](evidence-request.md#deployment-not-decided-yet)). **Before F3 lands:** pick the host and size its disk and memory for the 10-year `flood_gfm.tif`. Update the `docker-compose.yml` line in `architecture.md` (now "planned, W4") | Wed 2 Dec | F3 |
| B4 | Deck draft with every "Must fix" item from the deck review applied (Matei sends the table). Some rows are already settled by decisions since: the score has no number (L6), the EGMS release is 2020-2025 | Sat 5 Dec | — |
| B5 | Check every pitch claim against what's built: the numbers in [flood-validation.md](flood-validation.md), what the cropland share may claim ([DECISIONS.md](research/DECISIONS.md), decision 3), and "unknown, never low". List each claim with its source, or cut it | Sun 6 Dec | B4 |
| B6 | **Stretch**, flood's open F4 question: what grew under 2024's flags outside the polder. WorldCover on the 2024 `flood_gfm.tif` (reuse `checks/cropland_share/cropland_share.py`); log the result in `flood-validation.md`. Agree it with Szilly and Sover first | Thu 3 Dec | — |

## Lead and API: Matei

| # | Work to do | Due | Waits on |
|---|---|---|---|
| L7 | Implement `overall` in the agreed format (`architecture.md`, *Score format*), if it isn't merged by Sun 29 Nov. Contract change: Misu and Sara regenerate their types | Wed 2 Dec | — |

## Risks
- **G4 has less time.** It starts when F3 lands (due Sat 28 Nov). If F3 slips past Mon 30 Nov, deploy on the 2024 file and swap the file on the volume later: the grid stays the same, so nothing else changes.
- **Miriam carries the deploy and the deck in the same week.** If G4 runs long, B6 is dropped first, then Alex takes the reverse proxy.
