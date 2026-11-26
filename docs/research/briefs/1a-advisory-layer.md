# Decision 1a: GFM passes with no advisory layer

**Status:** the check the lead asked for is done, and the rule fixed before it points to **option B**. The lead has to confirm or overrule.

## Read
- [DECISIONS.md](../DECISIONS.md), section "1a": the options, the rule and the full result.
- [flood-validation.md](../../flood-validation.md):
  - "Advisory flags, and a spring false alarm";
  - "GFM passes without an advisory layer, per year".
- `checks/advisory_layer/advisory_check.py`, with its results in `checks/advisory_layer/run_2015-01-01_2026-01-01/` (`scenes.json`, `flood.csv`).
- `pipeline/gfm_score.py` around lines 144 and 156, where a missing advisory layer is read as "no warnings" today.

## Background
- **The advisory layer:** GFM publishes one per pass. It marks pixels where flood detection is unreliable (frost, snow, dry soil and similar). Since 10 Nov, flagged pixels count as **not seen**.
- **224 of 9,102 scenes** over 2015–2025 have **no advisory file at all**. The catalogue lists the file, but the link returns 404. The first scan said 198, plus 27 it couldn't tell.
- **Today those scenes count as "no warnings".** That breaks the rule that missing data is `unknown`.

## Options
| Option | What happens | Cost |
|---|---|---|
| A. Keep "no warnings" | The 224 scenes count in full | Any frost, snow or dry-soil false alarm in them goes in unchecked |
| B. Whole scene "not seen" | Those scenes are dropped from the history | Real observations are lost (see below) |
| C. Keep the scene, label its detections | Detections stay, marked "no warning information" | More code, probably a contract field |

## The rule (fixed on 13 Nov, before the run)
- A scene is flood-heavy if GFM marks flood on at least 1 % of the land it sees.
- The missing-layer group is flood-heavy if its share is at least double the control's **and** at least 5 points higher.
- **Not flood-heavy → option B.**

## The result
| | Scenes judged | Flood-heavy |
|---|---|---|
| Missing layer | 116 | 3 (2.6 %) |
| Control (same frame, nearest date with the layer) | 63 | 6 (9.5 %) |

- **The verdict doesn't depend on the control.** 2.6 % is under the 5-point margin even against a control of 0 %.
- **The control is weak,** so don't conclude that "missing scenes hold less flood":
  - 53 of its 116 scenes saw 0 % of the AOI;
  - the rest sit a median of 126 days from their missing scene.
- **Where the gaps are:** 116 of the 224 see the AOI.
  - **102 are on one track** (16:00 UTC, every 12 days), and that track's scene is missing almost every time from September 2018 to January 2020.
  - **14 are at 04:12 UTC,** in Nov 2015–May 2016.
  - **The other 108 see none of the AOI.**

## What option B costs
- **That track's view of the AOI is lost** for those stretches.
  - What share of all AOI passes this is was **not measured**: the check didn't count the scenes with the layer that see the AOI.
- **Botoșani loses a validation date.** The 2 July 2018 scene is a real flood scene used in validation, and it is one of the missing ones. Under B, Botoșani recall is measured on 3 July only. This links to decision 2.

## What option A lets in
- **Three flood-heavy missing scenes:** 11 and 23 Mar 2019 (2.4 %, 1.8 %) and 29 Apr 2021 (1.6 %).
- Whether they are real floods or soil false alarms is **unknown**.

## Coordinator's recommendation
- **Confirm B.** It is what the rule says, and its cost is now known.
- Choosing A or C departs from a rule fixed before the run. If the lead does that, the reason must be written down.

## What follows from B (for the lead's to-do list, not for this chat to do)
- **`gfm_score.passes()`:** a scene without the layer counts as not seen.
  - Re-score the existing criteria.
  - Log before and after in `flood-validation.md`.
- **Update the count:** change "198" to 224 in `flood-validation.md` and `architecture.md`, in the same commit.
- **Optional:** count all scenes that see the AOI, so B's cost can be given as a share.

## Questions for the lead
1. Confirm B, or choose A or C and say why?
2. Do you want the share measured (how many AOI passes B removes in total)? It is a small extension of the same check.

## Lead's choice
**Choice (17 Nov 2026): B now, with a way to recover the scenes later.** A scene without an advisory layer counts as not seen. It comes back only once something has checked it; it is never shown unchecked (that would be C).

**Why**
- B is what the rule fixed before the run says.
- It is the only option that keeps "missing = `unknown`".
- The lead wants the lost observations back if that can be done honestly, so B is the floor, not the end.

**Ways to recover them, cheapest first**
1. **GFM produces the missing files.** Ask in the helpdesk message, which is already on the to-do list. This needs no code: under B, only scenes whose file is missing are dropped, so a regenerated file brings its scene back on the next build.
2. **Build our own stand-in warning layer** from weather data (frost, snow, soil moisture, e.g. ERA5-Land). Test it against GFM's real warnings on the scenes that have the layer. This is new data (licence to check) and a new method to validate.
   - **Build it only if B removes at least 10 % of AOI pass coverage** (2015 to 13 Apr 2025). The lead fixed this threshold on 17 Nov, before the count was run.
   - **Below 10 %:** a roadmap line ("missing GFM warning layers are treated as unknown; a weather-based stand-in is future work").
3. **Rejected:** copying warnings from neighbouring passes. Frost and dry soil change within days.

**Share count (question 2): yes.**
- Run on 17 Nov with `checks/advisory_layer/share_of_passes.py`.
- **Result (18 Nov): B removes 8.15 % of AOI pass coverage over 2015 to 13 Apr 2025.** This is below the 10 % threshold, so route 2 is a roadmap item.
  - **Scenes read:** all 8,543. 2,067 see at least 5 % of the AOI, and 116 of those are missing the layer.
  - **Per pixel:** median 8.5 % of passes removed (median 1,360 passes per pixel), maximum 22.5 %.
  - **By period:**
    - Sep 2018–Jan 2020: 15.5 %.
    - 2015–2021: 10.2 %.
    - 2022 to 13 Apr 2025: 0 %.
  - **The 2015–2021 figure is above 10 %, but it is context, not the headline.** The headline (whole period) was fixed before the run.
  - **Checks:** the 640 m read agrees with the 20 m read on "sees the AOI" for all 335 scenes read earlier (0 disagree). A georeferencing warning appeared 3 times, at startup only.
- **The first attempt failed its own method check and its number is void:** catalogue footprints are the whole 300 km Equi7 tile.
- **The method used instead:** read every scene's layers at 640 m. On 20 scenes this matched the 20 m read (58.9 % vs 58.5 % seen; 0 % vs 0 %; `timing_test.py`).

**Corrections to this brief found in the chat**
- **Botoșani numbers:** 96.7 % and 99.3 % are **precision**. Ensemble recall is 67.6 % (2 July outline) and 58.5 % (3 July) (`flood-validation.md` table; `architecture.md`, Verification).
- **What B removes at Botoșani:** the 2 July 16:00 Sentinel-1 **pass**, not a reference outline. Both COSMO-SkyMed outlines (2 and 3 July) are still scored, against all passes 29 Jun–12 Jul minus the dropped one(s). How much recall falls is unknown until re-scored.
- **Spring windows:** some missing scenes fall inside the 20 Apr–5 May spring windows that decision 2 may use. They are 28 Apr 2019, 22 Apr and 4 May 2020, and 29 Apr 2021 (1.58 % flood). Under B those springs have fewer passes.

**Add to the to-do list**
- In the GFM helpdesk message, also ask them to regenerate the missing advisory files (route 1).
- Re-score all criteria under B, including Botoșani, **before** fixing decision 2's numbers.
