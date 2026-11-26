# Decision 5: ground motion plot rule, minimum cells, classes or none

**Deadline: before the 15 Nov data test, two days away.** The rule has to be written before anyone sees how many cells Galați plots get; otherwise it gets chosen to fit the data.

## Read
- [RECOMMENDATIONS.md](../RECOMMENDATIONS.md):
  - "G-1. EGMS Ortho, vertical, as a neighbourhood value";
  - "G-2. Fix the label rule before 15 Nov".
- [ground/SYNTHESIS.md](../ground/SYNTHESIS.md): "Bottom line", sections 1–4, and "Open after this round".
- `api/main.py`, class `Ground`: `status`, `velocity_mm_yr`, `n_cells` and `release` already exist.
- [architecture.md](../../architecture.md):
  - the ground row;
  - "Plots of 1 ha or less get 0–1 EGMS cells".

## Background
- **The data:** EGMS Ortho is a 100 m grid of vertical ground velocity in mm/year, from Sentinel-1 radar; one cell is 1 ha. It is the only EGMS level that is absolute and comparable across areas.
- **Farmland has few or no cells,** because ploughing and changing vegetation break the radar signal. Many Galați plots will have empty cells, and empty must be `unknown`, never "stable".
- **No published rule exists for summarising a small plot** [G1-24]. Whatever we pick is our own rule.
- **No velocity threshold has a verified source for EGMS:**
  - not 2 mm/year and not 5 mm/year;
  - the only citable 5 mm/year is a 2013 landslide threshold on older data, measured along the slope [G2-1];
  - no source links velocity to damage.
- **The competitor (Imoreview)** shows the median of the 3×3 cells around an address as a signed number, without classes [G3-12, G3-13].

## Three things to fix

**1. Which cells describe a plot**

| Option | Cells used | Trade-off |
|---|---|---|
| A. Cells the plot touches plus one ring of neighbours (recommended) | About 9–16 for a plot under 1 ha | More plots get a value. It describes the neighbourhood, so the report must say "about N ha around the plot" |
| B. Only the cells the plot touches | 1–4 for a small plot | Closest to the plot, but most small farmland plots end up `unknown` |
| C. A fixed 3×3 around the plot centre (the competitor's rule) | 9 | Comparable with Imoreview, but ignores the plot's size and shape |

Under every option, the value is the **median** of the cells that have data, and `n_cells` reports how many did.

**2. Minimum cells for a value** (below it, the answer is `unknown`)
- **The suggested value is 3.** EGMS advises reading clusters, not lone points (R). There is no source for any exact number.
- **1** means a lone cell can drive the answer.
- **5 or more** means even more `unknown` on farmland.

**3. Classes or none**

| Option | What users see |
|---|---|
| A. No classes (recommended) | A signed mm/year value, `n_cells`, and fixed sentences |
| B. Two-state label | "No motion distinguishable from noise" at or below 2 mm/year, **marked as our own rule**. 2 mm/year is about three times the 0.7 mm/year (1 σ) the product specifies [G2-4]; that is arithmetic, not a source |

Don't present 5 mm/year as an EGMS threshold under any option.

## Fixed report sentences (proposed)
- "Describes about N ha around the plot, not the plot itself."
- "No value means no reliable measurement, not stable ground."
- "Not a geotechnical or damage assessment."

## Validation that follows
- **A test** that too few cells give `unknown`.
- **Coverage:** the share of the 20 test plots that reach the minimum, by plot size. This is the honest headline number for the layer.
- **The velocities themselves can't be validated:** no independent reference for Galați was found.

## Coordinator's recommendation
Rule A, a minimum of 3 cells, and no classes. The contract's shape doesn't change.

## Questions for the lead
1. Cells: A, B or C?
2. Minimum: 3, or another number?
3. Classes: none, or the two-state label at 2 mm/year, marked as ours?
4. Approve the three fixed sentences, or reword them.
5. Who on the ground team writes the rule into `architecture.md` before the 15 Nov data test?

## Lead's choice
**Decided 23 Nov 2026, after the 15 Nov deadline and after the cell counts were known** (`architecture.md`: 18 of 20 test plots get no cell). This rule was chosen with the coverage in view, so it is not pre-registered.

- **Cells: keep what is built since 16 Nov.** EGMS cells whose centre is inside the plot (about option B), median of their velocities. Option A was rejected: EGMS cells sit on buildings, roads and villages, so a neighbour ring would mostly report the village next to a field.
- **Minimum: a share rule instead of a fixed count.** Ground is `measured` only when `n_cells` / max(1, round(`area_ha`)) ≥ 0.5 (one EGMS cell = 1 ha); below that it is `unknown`, `velocity_mm_yr` `null`. This is the half-share idea terrain uses.
  - It closes the open question "Ground on a single cell" in `architecture.md` (postponed from PR #9).
  - Test plots: `edge-50` (1 of 2) and `edge-65` (4 of 8) stay `measured`. No contract shape change.
  - Still to do (separate PR): the code change, a test that a low share gives `unknown`, and the `architecture.md` update in the same commit.
- **Classes: none.** A signed mm/yr value and `n_cells`. Never present 5 mm/year as an EGMS threshold.
- **Fixed report sentences (approved):**
  1. "Based on N EGMS cells (100 m) inside the plot." (replaces the "about N ha around the plot" draft, which fit option A only)
  2. "No value means no reliable measurement, not stable ground."
  3. "Not a geotechnical or damage assessment."
- **Who writes it:** whoever opens the share-rule PR updates `architecture.md` in the same commit.
