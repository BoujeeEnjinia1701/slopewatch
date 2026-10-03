---
doc_id: SLW-DEC-001
title: SlopeWatch design decisions register
project: SlopeWatch
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, SLW-DDR-001 to SLW-DDR-003 and the build plan work; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Amish approved the recommendations for open decisions 1 to 12 (SLW-DDR-003 accepted); moved to decisions made
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: Decisions of 2026-10-02 priced in the BOM (stake head marking and four site options); value engineering figures updated (SLW-CAL-001 v0.4)
---

# SlopeWatch design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The 1.5 in end cap thread matches the pipe thread (BSP or NPT) | The cap must seal against grout and water | SLW-DDR-003, P2 |
| 2 | The 110 x 50 mm reducer's 50 mm socket is 50 to 51 mm inside | The tape wrap takes up only about 1 mm a side | SLW-DDR-003, P3 |
| 3 | The capsule board is at most 28 mm wide and fits the 30 mm bore of the tube | Sets the capsule tube size | SLW-DDR-003, P1 |
| 4 | The displacement sensor has an M6 rod-end ball joint at each end and a removable plunger-end joint, and its plunger thread fits the coupling | The rod and the ball joints are sized to it | SLW-DDR-003, P5 |
| 5 | The alert and switch boxes have four corner screw holes outside the lid seal, and their spacing matches the plate holes | The plates are drilled to suit | SLW-DDR-003, P8, P9 |
| 6 | The horn has a sealing flange and the beacon a gasketed base that cover a 10 mm hole | Keeps the alert box sealed | SLW-DDR-003, P8 |
| 7 | The conduit fittings' hole size and lock nut size fit inside the 110 mm head | Sets the 20.5 mm holes and the lock nut clearance | SLW-DDR-003, P4 |
| 8 | The existing pole at the test site, if used, is round, 40 to 70 mm, and sound enough to carry the node and alert unit in wind | The fixing and the wind case depend on it | SLW-CAL-001 [H1] |

## Value engineering

Value-engineering target: USD 250 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 304.00 for the SlopeWatch-specific parts of the reference site, node on an existing pole (USD 54.00 over the target); USD 332.00 where the optional mast is needed. The FieldNode core (USD 126) is costed in its own project. Main cost drivers and savings worth trying:

- The largest lines are the three tilt sensor capsules (USD 82.50, mostly the three inclinometers at about USD 18 each), the crack gauge with its reader (USD 46), the alert unit with its switch post (USD 43), the bus cable in conduit (USD 42) and the three stakes (USD 39).
- Making the design constructable added USD 51.50: end caps and stand tubes (USD 12), collars (USD 1.50), stake heads from drainage fittings with conduit fittings and connectors (USD 18), the gauge's clamp blocks, ball joints, rod coupling, folded guard and pegs (USD 8), the alert and switch mounting plates and clamps (USD 10), and tape and a plug (USD 2).
- Decided on 2026-10-02 and now priced (bom/bom.csv): stake head marking (amber paint, retroreflective band, ID label and arrow, USD 2.50 a stake, USD 7.50 in the reference site); the wall holes in the alert back plate at no change in price; and, as site options outside every total, the 60.3 mm mast for site installations (USD 37.00, USD 9.00 more than line 8), a second alert unit at a machinery site (USD 64.00), armoured bus cable across a rockfall zone (USD 38.00 per 10 m) and an alert unit battery if FieldNode has not rated its 12 V rail (USD 20.00).
- Savings worth trying: bury the bus cable without conduit where the ground is soft and stable (up to about USD 15); buy the inclinometers and boards in a batch for several sites; make the guard from offcut sheet; use plain M20 cable glands on the stake heads where the conduit stops short of the head (about USD 2 a stake); price a second-source crack sensor with ball joints included.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D7: FieldNode core costed in FieldNode; tailings dams kept in the pitch with limits; surface tilt stakes plus a crack gauge; wired RS-485 bus; SCL3300 in mode 1; published tilt-rate thresholds and keyed 30 min silence; alert unit at the toe | Amish: "i accept all your recommendations, go with them across all repos." | SLW-DDR-001, SLW-DDR-002 |
| 2026-09-25 | Reference site on an existing pole, mast a site option; FieldNode asked to rate its 12 V rail; keyed switch on its own post about 5 m from the siren; precaution beacon at 1 % duty or less; own TwinKit gateway at SF12 sites | Amish, same instruction: go with recommendation | SLW-DDR-002, items 8 to 12 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan, keeping what the product does; changes recorded for review and accepted on 2026-10-02 (below) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | SLW-DDR-003 (changes open for his review) |
| 2026-09-30 | Build plan format approved; open decisions kept out of the build plan, in this register | Amish: "this is the correct build plan ... this is a good quality document format. Extend this across all the other repos" | SLW-BLD-001, SLW-DEC-001 |
| 2026-10-01 | `budget_usd` is a hypothetical value-engineering target, not a limit; cost reported against it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register, Value engineering; SLW-CAL-001 v0.3 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P11, as made | Amish: "i approve your recommendations for all 555 open decisions." | SLW-DDR-003, Table 1 |
| 2026-10-02 | Mast factor of 1.7 on yield accepted for the prototype on a fenced test slope with no one under the mast in high wind; any site installation uses the 60.3 mm mast unless local gust data show winds well below 35 m/s | Amish: "i approve your recommendations for all 555 open decisions." | SLW-DDR-003, A1; SLW-CAL-001 [H2] |
| 2026-10-02 | Four wall holes are added to both back plates so the node and the alert unit can be coach-screwed to a timber pole or wall; the change is to be agreed with FieldNode | Amish: "i approve your recommendations for all 555 open decisions." | SLW-DDR-003, A2 |
| 2026-10-02 | The optional mast is built for the first prototype | Amish: "i approve your recommendations for all 555 open decisions." | SLW-DDR-003, A3 |
| 2026-10-02 | The `problem` wording "often give warning" is accepted | Amish: "i approve your recommendations for all 555 open decisions." | SLW-DDR-001 O1, SLW-DDR-002 |
| 2026-10-02 | First co-design partner and site type to approach: an operating aggregate quarry with a geotechnical engineer on staff, testing on a bench away from the work face; a hillside community and its district disaster office only after TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | SLW-DDR-001 O2 |
| 2026-10-02 | A geotechnical partner sets thresholds per site before any alarm goes live; until then the published tilt-rate thresholds and the crack-gauge placeholders are used for logging only, not for public alarms | Amish: "i approve your recommendations for all 555 open decisions." | SLW-DDR-001 O3 |
| 2026-10-02 | At sites with running machinery, a second alert unit at the work face, linked by LoRa; pagers stay a later option | Amish: "i approve your recommendations for all 555 open decisions." | SLW-PRC-001, open questions; SLW-CAL-001 [E3] |
| 2026-10-02 | A fault message whenever a stake stops answering; the bus runs in buried conduit where the ground allows, and armoured cable only across rockfall zones | Amish: "i approve your recommendations for all 555 open decisions." | SLW-PRC-001, open questions |
| 2026-10-02 | Stake heads in signal amber with a retroreflective band, a stake ID label and a downslope arrow on the crown | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26 |
| 2026-10-02 | The request to FieldNode for a 12 V rail rated at least 0.5 A continuous stands; if FieldNode has not rated it before the TRL 4 build, the alert unit gets its own small battery | Amish: "i approve your recommendations for all 555 open decisions." | SLW-DDR-002 item 9 |
| 2026-10-02 | FieldNode's candidate pinout adopted (pin 1 switched rail, pin 2 data A, pin 3 ground, pin 4 data B, pin 5 analog); SlopeWatch uses 12 V on pin 1 with the bus on pins 2 and 4, and the keyed switch input on pin 5 of port B | Amish: "i approve your recommendations for all 555 open decisions." | FND-DDR-001 O2 |
