# Decision 8: run the research follow-up round, or stop here?

## Read
- [plan.md](../plan.md): every "follow-up candidate" in the log.
- "Open after this round" at the end of each synthesis:
  - [flood/SYNTHESIS.md](../flood/SYNTHESIS.md)
  - [ground/SYNTHESIS.md](../ground/SYNTHESIS.md)
  - [heat-drought/SYNTHESIS.md](../heat-drought/SYNTHESIS.md)
- [RECOMMENDATIONS.md](../RECOMMENDATIONS.md), "What each recommendation hinges on".

## Background
- **The round was planned but not run.** The plan had one follow-up round after the reviews, for gaps they exposed. On 12 Nov the lead said to go straight to the syntheses, so every gap from the reviews is still open.
- **A round means researcher and reviewer subagents.** They cost usage and run only when the lead names them.
- **It competes with build time:** the data test is on 15 Nov and the gate on 22 Nov.
- **Two gaps have since been answered directly:**
  - the GFM v3/v4 boundary and the reprocessing question, read from the catalogue on 13 Nov (decision 1b);
  - the missing advisory layers (the decision 1a check).

## The open gaps that could change a decision (coordinator's selection)
| Gap | Decision it could change | Size |
|---|---|---|
| Palama et al. (JISDM 2025): is there a sourced 5 mm/year EGMS threshold, justified by about 2 mm/year noise? | 5 (classes) | One paper. **Only useful before 15 Nov** |
| What the 2020–2024 Ortho quality control changed, and the minimum point count per cell | 5 (how many empty cells to expect) | Small; the data test may answer it in practice |
| Tupas 2024 and Moya 2019 in full: agricultural false alarms per algorithm | 2 (the odds that F-2 works) | Two papers, previously blocked (403) |
| The JRC European flood map header over Galați: coverage and nodata | Roadmap wording | A few minutes, not a research round |
| The Galați station's licence (ECA&D policy) | 6 and 7, only if H-1 opens | Small |
| EDO drought indicators: resolution and licence | Heat roadmap order | Small |

**Gaps that can't change a decision:**
- HG 447/2003;
- ESDAC's answer on ELSUS;
- the CEMS commercial-use wording;
- HyP3 coherence terms.

## Options
| Option | Cost | What it gives |
|---|---|---|
| A. Stop here | Nothing | Every gap stays listed as a limit |
| B. A narrow round: only gaps that can change a decision | 2–4 subagents, about a day | Palama before 15 Nov; Tupas and Moya before the F-2 test |
| C. The full round | Many subagents, several days | Every gap closed or confirmed unfindable |

## Coordinator's recommendation
- **B, narrow,** and only for items whose decision will still be open when the result arrives.
  - Palama only if the lead is considering classes in decision 5.
  - The JRC header is a few minutes' check, not a research task.
- **If usage is tight, A is defensible.** The recommendations already state each gap as a limit.

## Questions for the lead
1. A, B or C?
2. If B: which rows? Name the agents to launch; the coordinator only launches agents the lead names.

## Lead's choice
**Decided 23 Nov 2026 in the coordinator chat: B, a narrow round of four researchers, each followed by a fresh reviewer.** The gap list was re-checked against decisions 1–7 first: Palama, the station licence and the JRC header could no longer change a decision on their own.
1. **WorldCover accuracy** (`flood/worldcover-accuracy.md`): backs the 20-point threshold of decision 3 and field A, due 29 Nov.
2. **CEMS/GFM commercial use** (`flood/cems-commercial-use.md`): the core layer's licence for a product.
3. **Tupas 2024 + Moya 2019** (`flood/agricultural-false-alarms-per-algorithm.md`): context for reading the per-algorithm exploration run. The stop rule is already fixed.
4. **EGMS Ortho 2020–2024 + Palama** (`ground/egms-ortho-2020-2024.md`): limits wording and the ground roadmap.

- **No Fable agents** (the lead's instruction: no subscription for it). Researchers run on Sonnet and reviewers on Opus, with the model set on every launch.
