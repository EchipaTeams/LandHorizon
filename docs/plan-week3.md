# Week 3 plan: Mon 23 – Sun 29 Nov

By Sunday 29 Nov (milestone 5): the flood history runs 2015 to 13 Apr 2025 under research decisions 1a and 1b, the cropland field is in the contract, the gate is written down. The public URL moved to week 4 (G4, 27 Nov).

The work is split into segments. Each team splits its own list; whoever writes a PR, a teammate reviews it.

| Segment | Team | Done by Sunday when |
|---|---|---|
| Flood | Szilly, Sover | 1a and 1b are in the pipeline, every test is re-scored, and the 2015 – 13 Apr 2025 `flood_gfm.tif` is on the Drive |
| Ground | Alex, Miriam | Ground uses a share rule, `POST /evidence` returns the cropland share; the public URL moved to week 4 (G4) |
| Business and law | Miriam | The interview summary is with Matei, the law wording is confirmed, and the BMC, SWOT and PESTEL are drafted |
| Website | Misu, Sara | The website shows the farmland caveat and runs at a public URL |
| Lead and API | Matei | The gate is written down, Tuesday's decisions are made, and `overall` follows the agreed format |

## Flood: Szilly, Sover
F1 was the week's bottleneck. It merged on Wed 25 (PR #15), so F2 and F3 can start.

| # | Work to do | Due | Waits on |
|---|---|---|---|
| F1 | **Done** (PR #15, 25 Nov): **1a:** a scene with no advisory layer counts as not seen, and its neighbours in the same pass still count. **1b:** `flood_gfm.py` stops the history on the day GFM's major version changes (v3.1.0 ends 13 Apr 2025, so `period_end` follows from the catalogue) and writes each pass's version and contributing algorithms to the `gfm_versions` tag, from the scenes that counted only. Same PR: `architecture.md` period section, 198 → 224 in both docs, tests | Wed 25 | — |
| F2 | Re-score every criterion under 1a: Sept 2023 dry, Sept 2024 event, spring 2024, Botoșani 2018. Log before and after in `flood-validation.md` | Thu 26 | F1 |
| F3 | Time a one-month build first, then run the full batch 2015-01-01 → 2025-04-13 and put `flood_gfm.tif` on the Drive. **Keep the flood grid** (`flood_common.grid()`, same AOI): the API needs `worldcover.tif` (G3, PR #20) on exactly that grid and answers 503 otherwise. If the grid has to change, rerun `pipeline/worldcover.py` (seconds) and put both files on the Drive together | Sat 28 | F1 |
| F4 | **Done** (PR #14, 25 Nov): criterion pushed before the run, then `gfm_score.py 2025-04-20 2025-05-06` logged in `flood-validation.md`. **v4 fails too:** 15.81 % of land flagged in ≥1 pass against the 1 % limit (2024 on v3: 9.06 %). The cause is unknown: 98 % of the flags are outside the polder, on green land, so tilled fields don't explain them. The method isn't changed, and under 1b the history stops before v4 anyway. **Not checked yet:** what grew under 2024's flags outside the polder | Wed 25 | — |
| F5 | **Done** (PR #14): the README credits JRC Global Surface Water v1.4 (Pekel et al., 2016) | Wed 25 | — |
| F6 | With the new `flood_gfm.tif`: run `api/test_plots.py`, check `period_end` reads 2025-04-13, update the 20-plot flood numbers in the docs, the cropland share per date included (2024 per-date numbers in `architecture.md`, 26 Nov; check whether 10 years of spring flags change them) (`api/test_plots.py` now also needs `worldcover.tif` on the same grid) | Sun 29 | F3 |

## Ground: Alex, Miriam
G3 is the hardest item and changes the contract. G4 isn't ground work, but this team has the capacity: G1 and G2 are merged (#11, #16), so G4 comes next.

| # | Work to do | Due | Waits on |
|---|---|---|---|
| G1 | **Done** (PR #11, merged 25 Nov): ground share rule (cells with data ÷ cells whose centre fits in the plot, `GROUND_MIN_SHARE` 0.5), test and `architecture.md`; `api/test_plots.py` asserts unknown ⇔ no velocity and measured ⇒ `n_cells` > 0. L3 kept this denominator and accepted 0.5 (25 Nov) | Fri 27 | — |
| G2 | **Done** (PR #11, PR #16 25 Nov): checked on the real `ground.tif` that `edge-50` (1 of 2 cells) and `edge-65` (4 of 8) stay measured and the other 18 stay unknown. #16: `ground.py --plots` prints the cells that fit and the share with data, and the data-test table (`architecture.md`, "Cells per plot") says so | Fri 27 | — |
| G3 | Cropland share field `flood.cropland_share: float \| None` (agreed in L4): cut WorldCover 2021 to the flood grid (reuse `checks/cropland_share/cropland_share.py`), compute the cropland share of the plot's flagged pixels in the API. `null` when nothing is flagged, flood is unknown or WorldCover has no data. Tests, `architecture.md`, PR marked as a contract change. **Built in PR #20** (26 Nov); in the review the lead changed the type to `list[float \| None]`, one share per flood date | Sat 28 | L4 |
| G4 | Deploy the API: Dockerfile and `docker-compose.yml` (COGs from a volume), a public URL, and a reverse proxy so the website and `/evidence` share one domain ([evidence-request.md](evidence-request.md#deployment-not-decided-yet)). **Moved to week 4** (27 Nov, [plan-week4.md](plan-week4.md)): it waits for the full batch (F3), so it's built on the file it will serve | Wed 2 Dec | F3 |



## Website: Misu, Sara (separate repo)
| # | Work to do | Due | Waits on |
|---|---|---|---|
| W1 | Show the farmland caveat sentence when `flood_dates` is not empty (exact text in `docs/research/DECISIONS.md`, decision 3) | Tue 24 | — |
| W2 | Deploy the website behind the API's domain, with the MOCK label visible whenever mock mode is on | Sun 29 | G4 |
| W3 | Regenerate the types after the cropland PR (#20); show each flood date's cropland share next to that date (`cropland_share[i]` belongs to `flood_dates[i]`), with "can include" wording and `null` as unknown | Sun 29 | G3 |
| W4 | Start the print CSS for the PDF (a W4 item, only if time is left) | Sun 29 | — |

## Lead and API: Matei
Tuesday's decisions unblock Ground (L3, L4) and the scoring (L6), so they come first.

| # | Work to do | Due | Waits on |
|---|---|---|---|
| L1 | **Done** (25 Nov): `pystac-client` dropped from `pyproject.toml` and `uv.lock` (`checks/check_gfm.py` runs it with `uv run --with`), `pipeline/check_gfm.py` moved to `checks/`; the gitignore lines came in with #12 | Mon 23 | — |
| L2 | **Partly done** (25 Nov): Galați locked, milestone 3–4 status filled in, score format written down (L6). **Left:** the segment, after the interview summary (B1), and the law option, after Simonel (Thu 26) | Tue 24 | B1 |
| L3 | **Done** (25 Nov): 0.5, divided by the cells whose centre fits in the plot (as built in PR #11). `checks/ground_share/compare.py` on the real `ground.tif`: same answer as max(1, round(`area_ha`)) on all 20 test plots and 97 % of 9,600 rectangles; the area rule is looser on small plots and depends on the grid | Tue 24 | — |
| L4 | **Done** (25 Nov): `flood.cropland_share: float \| None`, the cropland share of the plot's flagged pixels, `null` (never 0) when nothing is flagged, flood is unknown or WorldCover has no data. Tell Ground (G3) and Website (W3) | Tue 24 | — |
| L5 | Send the GFM helpdesk email (draft in `docs/research/briefs/4-emails.md`) | Tue 24 | — |
| L6 | **Done** (25 Nov): no number; a status for flood, one for terrain and one for both, each with reasons; ground stays out (`architecture.md`, *Score format*) | Wed 25 | — |
| L7 | Implement `overall` in that format: any core layer unknown gives `incomplete`, never low | Sun 29 | L6 |
| L8 | Review the flood PRs, the cropland PR and the deploy; check the website repo. **Started** (25 Nov): F1 reviewed and merged (PR #15), after merging main into it and making `gfm_versions` list only the scenes that counted; #16 merged; `uv run pytest` works on main again (`checks/advisory_layer/timing_test.py` renamed to `timing_check.py`) | Thu 26 – Sat 28 | G3, G4 |
| L9 | Decide #2: held-out windows and limits for the per-algorithm test | Sat 28 | F2 |
| L10 | Wire the plot request end to end as [evidence-request.md](evidence-request.md) describes: the website sends `feature.geometry` to `POST /evidence` by its relative path (Vite proxy locally) and handles 200 / 422 / 503; pick the reverse proxy or CORS with the deploy (G4), never CORS `*` | Sun 29 | G4 |

## Risks
- **The batch runtime (F3) is unknown.** Reading 8,543 scenes at 640 m was already long, and the build reads at 20 m. Fallback: keep 2024 only and move the extension to W4.
- **The flood grid is now shared with `worldcover.tif`.** A rebuilt `flood_gfm.tif` on another grid (another AOI) makes `/evidence` answer 503 until `pipeline/worldcover.py` is rerun. Any flood rebuild, F3 or later, keeps the grid or ships both files together.
- **The gate isn't recorded anywhere.** If no segment had 3 people describe a real decision it would change, keep land buyers and say so in the pitch.
- **The cropland field changes the contract.** W3 can't finish until G3 merges, so agree the field name early (L4).
- **Miriam is in two segments.** If Ground runs short, Alex takes G3's pipeline part (the WorldCover cut) and Miriam the API part.
- **Matei carries the decisions, the reviews and the API.** If L7 slips, `overall` stays the honest mock for another week; that's acceptable, a late deploy isn't.
- **Not this week:** grouping flood dates into events, and orphan flooded passes.
