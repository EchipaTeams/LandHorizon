# Decision 6: heat and drought, roadmap only?

## Read
- [RECOMMENDATIONS.md](../RECOMMENDATIONS.md), "Heat and drought": build now, H-1 (conditional), the roadmap and the rejected options.
- [heat-drought/SYNTHESIS.md](../heat-drought/SYNTHESIS.md).
- [constraints.md](../constraints.md): "A new hazard or a new sensor is rated expensive, out of scope after the 22 Nov gate".

## Background
- **Nothing exists yet** for heat or drought in the project.
- **The default is a roadmap item.** The plan rates a new hazard as out of scope after the 22 Nov gate, unless something very cheap and honest exists.
- **The research found nothing that overturns that default:**
  - **It needs a new section in the evidence contract.**
  - **The only cheap candidate is regional.** One ERA5-Land cell is about 8,000 ha [H3-4], so nearly every pilot plot would show the same number. That is context, not evidence about a plot.
  - **Validation would be thin:**
    - one station against one cell;
    - the station's licence is unread;
    - ERA5-Land isn't fully independent of stations [H3-3].
  - **Flood, the core, is still open.**

## Options
| Option | Cost | What it gives |
|---|---|---|
| A. Roadmap only (recommended) | Nothing now | A concrete roadmap item for the pitch |
| B. Build H-1 if the 22 Nov gate allows | 20–30 h (coordinator's estimate, unsourced), a new contract section, a new dependency through `uv add`, and an account and token for the Copernicus Climate Data Store | "Hot days per year" from ERA5-Land, shown as **regional climate context**: the same value for every plot within about 9 km |
| C. Something else | Depends on the proposal | A per-plot heat or drought "risk score" is rejected: risk needs exposure and vulnerability [H1-7] |

## If B: what H-1 needs
- **Data:** ERA5-Land daily maximum temperature, 0.1°, CC BY.
- **Threshold:** our own, written before any run. The WMO says heat thresholds are local.
- **Validation:** against the Galați station in GHCN-Daily, on years held out in advance. Whether that station can be used depends on **decision 7**.
- **Wording:** "regional climate context from a reanalysis". Never "risk", never per plot.

## For the pitch, either way
- **First roadmap item:** H-1, a hot-day count from ERA5-Land shown as regional context.
- **After that, in order:**
  1. regional drought context;
  2. observation-based heat (E-OBS);
  3. scenario statements (EURO-CORDEX);
  4. plot-scale surface temperature.
- **Wording:** say "hazard indicator" or "regional climate context", not "risk".
- **Don't claim the pilot region is drying.** The verified trends are for Sulina, Dobrogea and Romania as a whole, not for Galați.

## Coordinator's recommendation
**A, roadmap only.** Revisit it at the 22 Nov gate only if flood and ground are on track.

## Questions for the lead
1. A, B or C?
2. If B: who would own it, and does it come out of the flood or the ground hours?

## Lead's choice
**Decided 23 Nov 2026: A, roadmap only.** Nothing is built for heat or drought before the freeze. The pitch gets H-1 (an ERA5-Land hot-day count shown as regional climate context) as the first roadmap item, with the order and wording above.

- **Left open by the lead:** they may come back later to see whether the H-1 code can be run. That would be a new decision, with its own owner, hours, contract review and validation plan. Choice A does not approve it.
- **Question 2 (owner, hours):** doesn't apply under A.
- **Effect on decision 7:** no longer urgent, because H-1 isn't opened.
