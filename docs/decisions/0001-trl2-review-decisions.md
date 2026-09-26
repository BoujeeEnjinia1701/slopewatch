---
doc_id: SLW-DDR-001
title: SlopeWatch TRL 2 review decisions
project: SlopeWatch
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 work, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted in part. Items D1 to D7 are decided by Amish, 2026-09-25: go with recommendation (see SLW-DDR-002); items O1 to O3 had no recommendation and remain "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", and the design precis SLW-PRC-001 v0.2 listed the key design choices, most with options and a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carried a recommendation is therefore adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Items without a recommendation stay open. Update, v0.2: on 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos". D1 to D7 are therefore decided by Amish; SLW-DDR-002 records this and the changes that followed.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in SLW-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted for TRL 3 work, now decided by Amish (2026-09-25).*

| # | Item | Recommendation adopted | Status |
| --- | --- | --- | --- |
| D1 | Budget (TRL 2 item 1) | Option B: the FieldNode core is costed in the FieldNode project, as SunSpoke does with the SwapCell pack, and an existing pole replaces the mast where one exists. The $250 `budget_usd` covers the SlopeWatch-specific parts of one reference site. `budget_usd` is unchanged; no new figure was recommended. R11 is redefined accordingly in SLW-REQ-001 v0.3. | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Tailings dams in the pitch (item 2) | Keep them, with the limits stated in every document: a supplementary layer only, installed with the owner's and engineer of record's permission, and no claim to detect brittle failure. The pitch is unchanged, since no rewording was recommended. | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Sensing method (item 3) | Surface tilt stakes plus one crack gauge, rather than borehole inclinometers or GNSS. | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Bus (item 4) | A wired RS-485 bus to one FieldNode for the prototype; wireless stakes recorded as a later variant. | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Inclinometer (item 5) | Murata SCL3300, with an ADXL355-class accelerometer as the fallback. SLW-CAL-001 adds that the sensor must run in its mode 1 (±90 degrees), because its inclination modes 3 and 4 stop at ±10 degrees. | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Alert rules (item 6) | The published 0.01 and 0.1 degrees per hour tilt-rate thresholds as defaults, site values set by an engineer after a baseline period; warning on one stake confirmed on two consecutive readings; keyed 30 min silence that re-arms. | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Alert unit location (item 7) | On the mast at the toe for the prototype; a second unit near the work face or in the village, linked by LoRa, as an option after co-design. | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | The `problem` wording change in `project.yaml` ("often give warning") made at TRL 2 (item 8). The TRL 2 note offered "accept or revert" without a recommendation, so the wording stays as it is and the choice stays with Amish. | Proposed, awaiting Amish |
| O2 | First co-design partner and site type (item 9): an artisanal mining cooperative, a quarry, or a hillside community with a district disaster office. No preference was stated. | Proposed, awaiting Amish |
| O3 | Crack-gauge thresholds (1 mm per day and 1 mm per hour are placeholders), to be set per site with a geotechnical partner. No recommendation was made. SLW-CAL-001 adds that the precaution rate must be taken over 24 h (see Consequences). | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: `budget_usd` stays $250, and the pitch and problem lines are unchanged. Only the TRL fields and evidence list change.
- SLW-PRB-001, SLW-PRC-001 and SLW-REQ-001 are revised to v0.3. The key design choices in the precis are no longer described as "proposed"; they are adopted for TRL 3 work pending Amish's review. R11 now reads "SlopeWatch-specific parts for one reference site, $250 or less, excluding the FieldNode core and any gateway".
- The calculations in SLW-CAL-001 led to four changes within these choices: the capsule sits 0.4 m deep instead of 0.3 m (R2), with foam plugs above and below it; the crack gauge gets its own RS-485 reader (+$6), since it is about 60 m of cable from the node; the precaution beacon flashes at 1 % duty or less (R8); and the crack-gauge precaution rate is taken over 24 h, so the gauge's own daily thermal swing does not trip it.
- R11 was not met with a new mast ($261 against $250) and met where an existing pole is used ($237). SLW-DDR-002 makes the existing-pole case the reference site; with the switch post added, R11 is met at $245.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
