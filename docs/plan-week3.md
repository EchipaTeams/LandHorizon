# Week 3 plan: Mon 23 – Sun 29 Nov

By Sunday 29 Nov (milestone 5): the flood history runs 2015 to 13 Apr 2025 under research decisions 1a and 1b, the cropland field is in the contract, the gate is written down, and the API runs at a public URL.

The work is split into segments. Each team splits its own list; whoever writes a PR, a teammate reviews it.

| Segment | Team | Done by Sunday when |
|---|---|---|
| Flood | Szilly, Sover | 1a and 1b are in the pipeline, every test is re-scored, and the 2015 – 13 Apr 2025 `flood_gfm.tif` is on the Drive |
| Ground | Alex, Miriam | Ground uses a share rule, `POST /evidence` returns the cropland share, and the API runs at a public URL |
| Business and law | Miriam | The interview summary is with Matei, the law wording is confirmed, and the BMC, SWOT and PESTEL are drafted |
| Website | Misu, Sara | The website shows the farmland caveat and runs at a public URL |
| Lead and API | Matei | The gate is written down, Tuesday's decisions are made, and `overall` follows the agreed format |

## Flood: Szilly, Sover
F1 is the week's bottleneck: everything else on flood waits for it, so it should merge by Wednesday.

| # | Work to do | Due | Waits on |
|---|---|---|---|
| F1 | Decision 1a: in `gfm_score.passes()` a pass with no advisory layer counts as not seen (today `gfm_score.py:144` fills in zeros). Decision 1b: record `processing:version` per pass and stop the history at a major version change, not a fixed date. Same commit: `architecture.md` period section, 198 → 224 in both docs, tests | Wed 25 | — |
| F2 | Re-score every criterion under 1a: Sept 2023 dry, Sept 2024 event, spring 2024, Botoșani 2018. Log before and after in `flood-validation.md` | Thu 26 | F1 |
| F3 | Time a one-month build first, then run the full batch 2015-01-01 → 2025-04-13 and put `flood_gfm.tif` on the Drive | Sat 28 | F1 |
| F4 | **Done** (PR #14, 25 Nov): criterion pushed before the run, then `gfm_score.py 2025-04-20 2025-05-06` logged in `flood-validation.md`. **v4 fails too:** 15.81 % of land flagged in ≥1 pass against the 1 % limit (2024 on v3: 9.06 %). The cause is unknown: 98 % of the flags are outside the polder, on green land, so tilled fields don't explain them. The method isn't changed, and under 1b the history stops before v4 anyway. **Not checked yet:** what grew under 2024's flags outside the polder | Wed 25 | — |
| F5 | **Done** (PR #14): the README credits JRC Global Surface Water v1.4 (Pekel et al., 2016) | Wed 25 | — |
| F6 | With the new `flood_gfm.tif`: run `api/test_plots.py`, check `period_end` reads 2025-04-13, update the 20-plot flood numbers in the docs | Sun 29 | F3 |

## Ground: Alex, Miriam
G3 is the hardest item and changes the contract. G4 isn't ground work, but this team has the capacity: G1 is in review (PR #11), so G4 comes next.

| # | Work to do | Due | Waits on |
|---|---|---|---|
| G1 | **Done** (PR #11, 23 Nov): ground share rule (cells with data ÷ cells whose centre fits in the plot, `GROUND_MIN_SHARE` 0.5), test and `architecture.md`. **Left:** `api/test_plots.py:69` still asserts unknown ⇔ 0 cells, so make it unknown ⇔ no velocity, and measured ⇒ `n_cells` > 0; then follow L3 (switch the denominator if the area rule wins, mark 0.5 accepted) | Fri 27 | L3 |
| G2 | **Done** (PR #11): checked on the real `ground.tif` that `edge-50` (1 of 2 cells) and `edge-65` (4 of 8) stay measured and the other 18 stay unknown. **Left:** say so in the data-test table (`architecture.md`, "Cells per plot") | Fri 27 | G1 |
| G3 | Cropland share field: cut WorldCover 2021 to the flood grid (reuse `checks/cropland_share/cropland_share.py`), compute the cropland share of the plot's flagged pixels in the API. `null` when nothing is flagged, flood is unknown or WorldCover has no data. Tests, `architecture.md`, PR marked as a contract change | Sat 28 | L4 |
| G4 | Deploy the API: Dockerfile and `docker-compose.yml` (COGs from a volume), a public URL, and a reverse proxy so the website and `/evidence` share one domain ([evidence-request.md](evidence-request.md#deployment-not-decided-yet)). Move docker-compose from W4 to now in `architecture.md` | Fri 27 | — |



## Website: Misu, Sara (separate repo)
| # | Work to do | Due | Waits on |
|---|---|---|---|
| W1 | Show the farmland caveat sentence when `flood_dates` is not empty (exact text in `docs/research/DECISIONS.md`, decision 3) | Tue 24 | — |
| W2 | Deploy the website behind the API's domain, with the MOCK label visible whenever mock mode is on | Sun 29 | G4 |
| W3 | Regenerate the types after the cropland PR; show the cropland share with "can include" wording and `null` as unknown | Sun 29 | G3 |
| W4 | Start the print CSS for the PDF (a W4 item, only if time is left) | Sun 29 | — |

## Lead and API: Matei
Tuesday's decisions unblock Ground (L3, L4) and the scoring (L6), so they come first.

| # | Work to do | Due | Waits on |
|---|---|---|---|
| L1 | **Done** (25 Nov): `pystac-client` dropped from `pyproject.toml` and `uv.lock` (`checks/check_gfm.py` runs it with `uv run --with`), `pipeline/check_gfm.py` moved to `checks/`; the gitignore lines came in with #12 | Mon 23 | — |
| L2 | Write the gate outcomes (segment, score format, provisional law option), lock Galați, fill in milestone 3–4 status in `architecture.md` | Tue 24 | B1 |
| L3 | Set the ground share threshold (0.5 proposed in PR #9) and its denominator: PR #11 divides by the cells whose centre fits in the plot, `DECISIONS.md` #5 by max(1, round(`area_ha`)) | Tue 24 | — |
| L4 | Agree the cropland field's name and type with Ground and Website | Tue 24 | — |
| L5 | Send the GFM helpdesk email (draft in `docs/research/briefs/4-emails.md`) | Tue 24 | — |
| L6 | Decide the `overall` score format from the gate | Wed 25 | L2 |
| L7 | Implement `overall` in that format: any core layer unknown gives `incomplete`, never low | Sun 29 | L6 |
| L8 | Review the flood PRs, the cropland PR and the deploy; check the website repo | Thu 26 – Sat 28 | F1, G3, G4 |
| L9 | Decide #2: held-out windows and limits for the per-algorithm test | Sat 28 | F2 |

## Risks
- **The batch runtime (F3) is unknown.** Reading 8,543 scenes at 640 m was already long, and the build reads at 20 m. Fallback: keep 2024 only and move the extension to W4.
- **The gate isn't recorded anywhere.** If no segment had 3 people describe a real decision it would change, keep land buyers and say so in the pitch.
- **The cropland field changes the contract.** W3 can't finish until G3 merges, so agree the field name early (L4).
- **Miriam is in two segments.** If Ground runs short, Alex takes G3's pipeline part (the WorldCover cut) and Miriam the API part.
- **Matei carries the decisions, the reviews and the API.** If L7 slips, `overall` stays the honest mock for another week; that's acceptable, a late deploy isn't.
- **Not this week:** grouping flood dates into events, and orphan flooded passes.
