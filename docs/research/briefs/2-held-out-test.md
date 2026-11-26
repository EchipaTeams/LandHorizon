# Decision 2: windows and limits for the per-algorithm test (F-2)

## Read
- [RECOMMENDATIONS.md](../RECOMMENDATIONS.md), "F-2. A per-algorithm rule, run as a pre-registered experiment".
- [flood/SYNTHESIS.md](../flood/SYNTHESIS.md), section 1.3, "The per-algorithm layers: what is known".
- [flood-validation.md](../../flood-validation.md):
  - the Botoșani section;
  - "Review of PR #1" (the spring window);
  - the September 2023 dry window.
- [architecture.md](../../architecture.md), "Verification": the pass criteria in force.

## Background
- **The problem:** on 30 Apr and 1 May 2024 GFM flagged about 15,000 ha of freshly tilled fields as flood. The spring window scored 9.06 % against a limit of 1 %.
- **The idea:** GFM publishes each of its three algorithms' flood maps separately (`dlr_flood_extent`, `list_flood_extent`, `tuw_flood_extent`).
  - Nobody has tested whether the three disagreed on those days.
  - If they did, a rule like "count a pixel only if algorithm X agrees" might remove the false alarm.
- **The trap:** a rule picked by looking at 30 Apr and 1 May fits those days by construction. It has to be tested on windows it has never seen, with limits written **before** the run.
- **Order of work:**
  1. Run an exploration table on the 2024 scenes, and call it exploration.
  2. Stop if all three algorithms flag the polder about equally.
  3. Otherwise, write the rule and the test into `architecture.md`.
  4. Run the held-out test.
- **This decision is step 3's content.** It is used only if step 2 doesn't stop the work.

## Why it's the lead's call
Pass criteria are project decisions in `architecture.md`. The person who runs the test must not pick the windows after seeing the data.

## Constraint from decision 1b
The test must stay in GFM v3. Spring 2025 is v4, so the spring years come from 2024 or earlier.

## What to fix

**1. No-flood spring windows** (20 Apr–5 May, at most 1 % of land flagged in at least one pass)

| Option | Cost | Weakness |
|---|---|---|
| A. Two other years, picked now (e.g. 2022, 2023) | Least work | If the plain ensemble already passes there, the test can't show an improvement |
| B. Every spring 2018–2023 that passes the dryness check | About 2–3 h more for dryness checks (coordinator's estimate), and more compute | Mixes one-satellite years (2022–23) with two-satellite years (2018–21), which have twice the passes |
| C. Decide after the exploration table | Nothing now | The windows are chosen by someone who has seen per-algorithm data |

**2. The September 2023 dry window:** keep the limit at 1 % (the ensemble scores 0.09 %). There is no real choice here.

**3. The flood event and its recall limit:** Botoșani, July 2018, against the COSMO-SkyMed outlines. The ensemble gets 96.7 % and 99.3 % there.

| Option | What it accepts |
|---|---|
| A. Recall ≥ 50 % (as first suggested) | A rule that loses almost half of a flood the ensemble catches nearly whole |
| B. At most 10 points below the ensemble on the same outline | Only a rule that keeps nearly everything the ensemble finds |

## What the research added
- **Low odds:** the consortium says two of the three algorithms are affected by agriculture; the third (LIST) isn't discussed. No source says a per-algorithm rule works [F1-15].
- **Power check:** run the plain ensemble on the same spring windows. If it already passes there, those windows prove nothing, and the result must say so.
- **Dryness:** each window needs no flood on record and a clear Sentinel-2 image checked by eye. Sentinel-2B wasn't flying before 2017, so this check is weaker in the early years (R).
- **Missing algorithms:** a pass with fewer than three valid algorithms counts as `unknown`, never "no flood". Whether old passes carry all three assets is unchecked.
- **Rejected forms:**
  - choosing the rule on the failing scenes and calling that validation;
  - an "all three must agree" vote, which turns single-algorithm passes into "no flood".

## Coordinator's recommendation
- **Springs: option B.**
  - It removes the choice of years, so nobody can pick favourable ones.
  - It also measures how often the ensemble fails in spring across the history, which decision 3 needs anyway.
- **Recall: option B.**
  - The 10 points are the coordinator's number, not a sourced one.
  - The 50 % limit came from the Galați flash flood, where the ensemble itself gets 58 %. At Botoșani it is far too loose.
- **Passing:** every criterion holds in every dry spring. Any failure means the rule is not adopted, the result is logged and nothing is retuned.
- **Limit to state:** Botoșani is a river flood that GFM maps almost completely. Passing there says little about flash floods like Pechea.
- **Link to 1a:** the 2 July 2018 Botoșani scene has no advisory layer. If 1a ends as B, write the criterion as "on each Botoșani date that counts as seen" (3 July only).

## Questions for the lead
1. Springs: A, B or C?
2. Recall limit: 50 %, or tied to the ensemble (and is 10 points right)?
3. Should the exploration table (step 1) be run now as a one-off check in `checks/`? It decides whether this test happens at all. Run it only on the lead's go.

## Lead's choice
**Fixed on 18 Nov 2026, before the exploration table was run and before anyone saw per-algorithm data.**

**1. Spring windows: option B.**
- Every 20 Apr–5 May window from 2018 to 2023 that passes the dryness check.
- 2024 is in-sample, and 2025 is v4 (decision 1b).
- **The dryness check, done before the held-out run:** no flood on record in Galați County, and a clear Sentinel-2 image checked by eye.
- **Limit in each dry spring:** at most 1 % of land flagged in at least one pass.
- **Why:** nobody picks the years, and the run also shows how often the plain ensemble fails in spring, which decision 3 needs anyway.
- **Known weakness:** under decision 1a (B), the missing-layer scenes in these windows are not seen: 28 Apr 2019, 22 Apr and 4 May 2020, 29 Apr 2021. Those springs have fewer passes.

**2. Botoșani recall: option B.**
- On each COSMO-SkyMed outline (2 July and 3 July 2018), the rule's recall at ≥1 pass is **at most 10 points below the plain ensemble's**.
- Both are computed on the passes of 29 Jun–12 Jul 2018 that count as seen under 1a (B), so without the 2 July 16:00 pass.
- **The 10 points are the coordinator's number,** not a sourced one.
- **Correction to this brief:** the ensemble's recall is 67.6 % (2 July outline) and 58.5 % (3 July) with all passes. 96.7 % and 99.3 % are precision. The recall under 1a (B) is not measured yet; the relative limit follows it automatically.

**Unchanged:** the September 2023 dry window stays at most 1 %.

**Applies to the whole test**
- **Pass rule:** every criterion holds in every dry spring. Any failure means the rule is not adopted; the result is logged and nothing is retuned.
- **Power check:** report the plain ensemble on the same spring windows. Where it already passes, that window can't show an improvement, and the result says so.
- **Missing algorithms:** a pass with fewer than three valid algorithms counts as `unknown`, never "no flood".
- **Limit to state:** Botoșani is a river flood that GFM maps well. Passing there says little about flash floods like Pechea.
- **To do before the held-out run, not for this chat:** write the rule and these criteria into `architecture.md`.

**3. Exploration table: yes.** The lead runs it overnight.
- **Script:** `checks/per_algorithm/explore.py`, with `--reference` pointing to the EMSR758 AOI03 PRODUCT zip. Results go to `checks/per_algorithm/run/` and must not be pushed.
- **Part 2 of the script:** a catalogue-only count of how many 2018–2023 spring scenes carry all three algorithms.
- **Stop rule, fixed on 23 Nov 2026 before the run** (the chat's proposal, accepted by the lead; the numbers are ours, not sourced). The exploration had not been run on the lead's machine: `checks/per_algorithm/run/` did not exist.
  - **Continue to the held-out test** only if at least one algorithm meets both conditions:
    - on **both** 30 Apr and 1 May 2024, it flags **less than half** of the polder area the ensemble flags;
    - it still flags **at least 80 %** of what the ensemble flags inside the EMSR758 outline (Sept 2024).
  - **Otherwise stop:** log the negative result in `flood-validation.md` and go on to decision 3 (cropland caveat).
  - **Areas:** compared on seen pixels only, as `explore.py` prints them (hectares per scene; a day with several scenes is their sum).
