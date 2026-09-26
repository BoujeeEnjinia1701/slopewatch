---
doc_id: SLW-DDR-002
title: SlopeWatch recommendations accepted
project: SlopeWatch
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the recommendations accepted by Amish on 2026-09-25, what changed in the repo, and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below with a recommendation is decided by Amish, 2026-09-25: go with recommendation. Items without a recommendation remain "Proposed, awaiting Amish".

## Context

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." This record lists every SlopeWatch item that carried a recommendation in `docs/REVIEW.md` (TRL 2 and TRL 3 sessions) or in SLW-DDR-001, and what changed in the repo because of it. Where a recommendation offered several options, the recommended option is the decision. Work that would need TRL 4 (build, test, trial, firmware beyond a sketch, purchasing) is decided but on hold, because TRL 4 is on hold by Amish's instruction. Changes that belong in another repo are listed as cross-repo actions and were not made here.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in this repo |
| --- | --- | --- | --- |
| 1 | SLW-DDR-001 D1, budget (TRL 2 item 1) | Option B: FieldNode core costed in the FieldNode project; $250 covers SlopeWatch-specific parts | Status wording in SLW-DDR-001 v0.2, SLW-PRB-001 v0.4, SLW-PRC-001 v0.4 and `bom/bom-notes.md`. `budget_usd` stays $250 (no new figure was recommended) |
| 2 | SLW-DDR-001 D2, tailings dams in the pitch (item 2) | Keep them, with the limits stated | Status wording only; pitch unchanged |
| 3 | SLW-DDR-001 D3, sensing method (item 3) | Surface tilt stakes plus one crack gauge | Status wording only |
| 4 | SLW-DDR-001 D4, bus (item 4) | Wired RS-485 bus to one FieldNode; wireless stakes later | Status wording only |
| 5 | SLW-DDR-001 D5, inclinometer (item 5) | Murata SCL3300 in mode 1, ADXL355-class fallback | Status wording only |
| 6 | SLW-DDR-001 D6, alert rules (item 6) | Published 0.01 and 0.1 degrees per hour thresholds as defaults; two-reading confirmation; keyed 30 min silence that re-arms | Status wording only |
| 7 | SLW-DDR-001 D7, alert unit location (item 7) | On the pole or mast at the toe; second unit optional after co-design | Status wording only |
| 8 | TRL 3 review item 4, R11 gap with a new mast | Option (a): the existing-pole case is the reference site; the mast is a site option | R11 in SLW-REQ-001 v0.4 restated for the reference site on an existing pole; BOM line 8 marked as a site option; SLW-CAL-001 v0.2 section K recomputed. R11 moves from **not met** ($261) to **met on paper** ($245, with item 10 below). `budget_usd` unchanged |
| 9 | TRL 3 review item 5, FieldNode 12 V rail (R8) | Option (a): ask FieldNode to specify at least 0.5 A continuous on its 12 V rail | Recorded as a cross-repo action in `docs/REVIEW.md`; R8 text updated. FieldNode not edited; R8 stays at risk until FieldNode rates the rail |
| 10 | TRL 3 review item 6, keyed switch location (safety, R7) | Move the switch about 5 m from the mast on its own lead | Design change: `cad/src/model.py` adds `switch_post()` (26.9 mm post, 1.4 m above ground, 0.5 m driven, switch box at 1.3 m, 7 m lead) and removes the box from the mast; new `cad/step/slopewatch-switch-post.step` and `.stl`; SLW-DWG-001 Rev P1 to P2; BOM line 7 $25 to $33; media re-rendered; SLW-CAL-001 v0.2 adds [E5]: level at the switch 105.4 to 95.5 dB(A), NIOSH allowance 4.3 to 43 min; mast base moment 550 to 541 N·m, factor 2.0 to 2.1 |
| 11 | TRL 3 review item 7, precaution beacon duty | Keep the slow flash at 1 % duty or less (as set by SLW-CAL-001) | Status wording in SLW-PRC-001 v0.4 and SLW-REQ-001 v0.4; no number changed |
| 12 | TRL 3 review item 8, networks at SF12 | A site that needs SF12 uses its own TwinKit gateway rather than The Things Network | Network rule added to SLW-REQ-001 v0.4 (R4 and assumptions), SLW-PRC-001 v0.4 and SLW-CAL-001 v0.2 section D. The gateway stays outside the site cost |

## Items still open

*Table 2. Items with no recommendation, still "Proposed, awaiting Amish".*

| # | Item | Status |
| --- | --- | --- |
| O1 | The `problem` wording in `project.yaml` ("often give warning"), changed at TRL 2 with "accept or revert" and no recommendation. The wording stays in place | Proposed, awaiting Amish |
| O2 | First co-design partner and site type; no preference stated | Proposed, awaiting Amish |
| O3 | Crack-gauge thresholds (placeholders 1 mm per day over 24 h and 1 mm per hour), to be set with a geotechnical partner; no recommendation | Proposed, awaiting Amish |

## Consequences

- Requirement status (SLW-CAL-001 v0.2): 0 not met (was 1), 4 at risk (R6, R7, R8, R9), 5 met on paper (was 4), 2 met by design, 2 not verifiable at TRL 3.
- Cost: $245 SlopeWatch-specific parts for the reference site against $250 (was $261 with a new mast, $237 on a pole without the switch post); $269 at a site that needs the mast; $371 for the reference site with the FieldNode core.
- Cross-repo actions, not made here: FieldNode to rate its 12 V rail at 0.5 A or more continuous (item 9); FieldNode's proposed airtime rule (longer intervals at SF10 and slower on The Things Network) needs an exception for SlopeWatch alert states, or such sites use a private gateway, which item 12 now requires at SF12.
- On hold (TRL 4): the suggested cut-cable and flat-battery fault message as a firmware rule, the capsule chamber test in CalRig and every build, test or field trial. TRL 4 is on hold by Amish's instruction.
- `trl` and `trl_target` stay at 3.
