# Decision 7: does a dataset used only for validation need an open product licence?

## Read
- [constraints.md](../constraints.md), "Data and money": "Free and openly licensed data only. Check the licence allows use in a product, not only research."
- [RECOMMENDATIONS.md](../RECOMMENDATIONS.md), H-1, "Hinges on".
- [heat-drought/SYNTHESIS.md](../heat-drought/SYNTHESIS.md), "Open after this round".
- [flood-validation.md](../../flood-validation.md): which references the flood tests use.

## Background
- **The constraint was written for data the product ships:** what goes into the COGs and the API answer.
- **Validation references are different:**
  - they are used once, offline, to measure our accuracy;
  - they are never shipped;
  - only the resulting numbers (precision, recall) are published.
- **Where the question comes up:**

  | Use | Reference | Licence situation |
  |---|---|---|
  | Heat (H-1), only if decision 6 opens it | The Galați station series in GHCN-Daily, which comes from ECA&D | ECA&D's data policy is unread, and it may be non-commercial |
  | Flood, today | CEMS rapid-mapping outlines (EMSR758 from PAZ, EMSR293 from COSMO-SkyMed) and Sentinel-2 images checked by eye | Open Copernicus products, so fine under either option |
  | Future | Any national or research dataset offered "for research only" | Depends on the dataset |

## Why it's the lead's call
It interprets a project constraint. The rule should be stated once, so every later choice follows it.

## Options
| Option | Rule | Effect |
|---|---|---|
| A. Validation bar | A validation-only reference needs terms that allow **our use of it**: evaluation and publishing derived accuracy numbers. It is never shipped, never committed to the repo, and always cited | More references become usable; the licence still has to be read |
| B. Product bar | The same as for shipped data: open, with commercial use allowed | Simpler and safer, but some layers may be left without any reference |

## Coordinator's recommendation
- **A, with four conditions:**
  1. The terms are actually read, and they allow evaluation and publishing derived numbers.
  2. The data are never shipped or committed.
  3. The source is cited.
  4. The report says what the reference was.
- **It is only urgent if decision 6 opens H-1.** Otherwise it can be stated now as a general rule and left.
- **This is a reading of licence terms, not legal advice.** If a dataset's terms are unclear, treat it as not usable.

## Questions for the lead
1. A or B?
2. Decide now as a general rule, or wait for decision 6?

## Lead's choice
**Decided 23 Nov 2026: A, the validation bar, stated now as a general rule.** A reference used only for validation can be used if all four conditions hold:
1. Its terms are actually read, and they allow evaluation and publishing derived numbers (precision, recall). Terms that exclude a commercial context fail, even under A.
2. The data are never shipped or committed (they stay in gitignored folders such as `data/raw/reference/`).
3. The source is cited.
4. The report says what the reference was.

- **If a dataset's terms are unclear, treat it as not usable.** This is a reading of licence terms, not legal advice.
- **Today:** the flood references (CEMS EMSR758 and EMSR293 outlines, Sentinel-2 checked by eye) already meet all four. The Galați GHCN-Daily / ECA&D station is not in use, because decision 6 is A (roadmap only). If H-1 is reopened, condition 1 means reading the ECA&D policy first.
- **The lead's reason for citing:** it helps the general presentation and the project.
