---
doc_id: SLW-DDR-003
title: SlopeWatch design for construction
project: SlopeWatch
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish, including A1 (sharpened), A2 and A3
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations for A1 to A3 in Table 3, as written for the register on 2026-10-01 (SLW-DEC-001); A1 was sharpened to set conditions for the prototype and for site installations. The changes were made under Amish's 2026-09-30 instruction to make the design physically buildable.

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The SlopeWatch model of SLW-DDR-002 showed what the system does but several of its parts could not be made, fixed or joined as drawn. Checking the concept model with build123d (overlap volumes and gaps between parts) and going through how each part is made and fixed found the eleven problems in Table 1.

The changes keep what SlopeWatch does: the same three grouted tilt stakes 0.8 m deep with the capsule 0.4 m below ground, the same crack gauge span and stroke, the same bus, FieldNode core, siren, beacon, keyed switch post and optional mast, the same alert rules and the same reference site. Every change is in `cad/src/model.py`, which now builds each component separately and runs 79 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must not touch are apart by at least the stated clearance. All 79 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The capsule (34 mm) sat loose in the 41.9 mm pipe bore between two foam plugs, 3.95 mm from the wall, with nothing setting its depth or holding it on the pipe axis. A tilt sensor that can lean in its bore does not read the pipe's tilt. | Two 3D-printed ASA centring collars (41.5 mm outside, 15 mm long) glued flush on the capsule ends, a slip fit in the bore (0.2 mm clearance). A 40 mm PVC stand tube, 335 mm long, stands on the bottom cap inside the pipe; the lower collar rests on its rim, which puts the capsule centre 0.4 m below ground. The foam plug above the capsule stays; the one below is replaced by the stand tube. | The collars make the capsule turn with the pipe; the stand tube sets the depth without measuring down a hole. The closed air column inside the stand tube still stops convection below the capsule, so the thermal case of SLW-CAL-001 section B stands. |
| P2 | The pipe bottom was "plugged" with an unspecified 20 mm internal plug. | The pipe is bought threaded at the bottom and closed with a screwed 1.5 in malleable-iron end cap with thread sealant. The hole is augered 829 mm deep (was 820) so 20 mm of grout runs under the cap. | A stock fitting that keeps grout and ground water out; the merchant who cuts the pipe threads it. |
| P3 | The stake head was a 120 mm PVC cap with a "reducer ring" inside, which is not a stock part, and nothing fixed it to the pipe. | A head from stock 110 mm PVC drainage parts: a 110 x 50 mm concentric reducer whose 50 mm socket slides over the pipe on a self-amalgamating tape wrap, 94 mm of 110 mm pipe and a 110 mm end cap, solvent-cemented. Two M5 stainless self-tapping screws go through the socket into the pipe wall, drilled in place. Head height above ground unchanged (330 mm). | Every part is sold by plumbers' merchants; the tape takes up the 1.9 mm between the 50.2 mm socket and the 48.3 mm pipe and seals it; the screws stop the head being lifted or turned. The bare pipe between ground and head stays 160 mm, so the pipe-heating case is unchanged. |
| P4 | One M20 cable gland on the head, facing downslope, for a bus that must come into every stake and go on to the next. A cable gland also cannot grip corrugated conduit. | Two M20 IP66 conduit fittings for 20 mm corrugated conduit, one upslope (bus in) and one downslope (bus out), with lock nuts inside the head. The bus in, bus out and capsule lead are joined core to core with lever connectors inside the head. | A daisy-chained bus needs an in and an out at each stake; the fittings are the high point of each conduit run, so water in the conduit drains away from the head. |
| P5 | The crack gauge clamps were solid 60 x 60 x 80 mm blocks round the pins with no way to fix the sensor, and the sensor body and rod simply butted against them. | Clamp blocks from 40 x 40 mm aluminium bar, 60 mm tall, bored 20.5 mm for the pin and held by an M8 set screw on their outer face; an M6 rod-end ball joint on a stud on each block's inner face. The sensor body hangs on the upslope ball joint; its plunger joins an 8 mm stainless extension rod through an M6 coupling nut; the rod's far end screws into the downslope ball joint. | Ball joints let the crack open, close or shear without bending the sensor; the set screws let the blocks be re-set on the pins after 100 mm of opening. Both blocks are the same part. The rod is 501 mm (was 580 mm), which lowers the gauge's thermal swing from 0.39 to 0.36 mm a day [C2]. |
| P6 | The guard intersected both anchor pins (12,566 mm³ of overlap) and floated 50 mm above the ground with no fixing. | A channel folded from 1.5 mm galvanized sheet, 1,150 long, 200 wide and 250 high, with 25 mm feet, standing on the ground 48 mm above the pin tops, held by four 8 mm ground pegs through the feet on the upslope half only. | Clears every part of the gauge; pegging only the upslope half lets the ground open under the downslope half without the guard holding the crack together. |
| P7 | The reader box floated 20 mm from the gauge with no fixing. | The box hangs under the guard web at the upslope end, lid down, on two M4 screws with nylon sealing washers, 12 mm clear of the upslope pin; the bus leaves through an M20 conduit fitting on its downslope end and out of the open downslope end of the guard. | Protected by the guard, fixed to the half of the guard that is pegged, and reachable by lifting the guard. |
| P8 | The alert unit (siren box, horn, beacon) stood on the open top of the mast pipe with no fixing, and could not go on an existing pole, which is the reference site (SLW-DDR-002). | The siren driver is in a bought IP65 alert box (120 x 90 x 120 mm) with the horn on its front and the beacon on its top. The box is screwed through its corner holes to a 160 x 360 x 3 mm aluminium back plate, which clamps to the pole or mast with two V-blocks and two band clamps through slots, the same fixing as the FieldNode core. On the mast, the plate's top stands 110 mm above the mast top so the beacon clears it; the siren centre is 3.23 m above ground (was 3.26 m). The mast gets a push-on top cap. | One fixing that works on an existing 40 to 70 mm pole and on the mast; the parts are the FieldNode's (FND-DDR-003), so the maker learns one method. |
| P9 | The keyed switch box floated 5 mm off its post. | A 100 x 160 x 3 mm galvanized back plate bears on the post and is held by two stainless hose clips through slots, above and below the box; the box is screwed to the plate through its corner holes. | Hose clips fit the 26.9 mm post and need no drilling of the galvanized tube. |
| P10 | The FieldNode massing showed the concept V-blocks (50 x 20 x 30 mm boxes 0.9 mm off the pole) and bracket posts floating 13.5 mm off the back plate. | The massing now follows the FieldNode constructable design (FND-DDR-003): V-blocks 60 x 33 x 20 mm with a true 90 degree V touching the pole, two band clamps through slots 51 mm each side of centre, and bracket bars meeting the plate and panel. FieldNode is still built to its own plan (FND-BLD-001). | SlopeWatch shows the node as it will be built, without taking over its design. |
| P11 | The earth bond ran into the mast pipe with no clamp at either end. | A bought earth-rod clamp on the rod, a bonding clamp round the mast 20 to 40 mm above the footing and a 16 mm² green and yellow bond conductor between them. | The usual way to bond a steel mast to an earth rod. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| BOM | Lines 1, 2, 3, 4, 7, 8 and 10 respecified and repriced. Reference site $245.00 to $296.50, $46.50 over the unchanged $250 value-engineering target (`budget_usd`); $324.50 with the optional mast [K2], [K3]. | Parts added to make the design buildable. |
| Calculations | SLW-CAL-001 v0.3: crack gauge thermal swing 0.36 mm a day [C2]; siren height 3.23 m, level at the keyed switch 95.5 dB(A), 42 min NIOSH allowance [E5]; mast in a 35 m/s gust 136 MPa, factor 1.7 on yield (was 113 MPa, 2.1), footing factor 2.2 (was 2.7), because the alert unit's back plate is now counted in the wind area [H1] to [H4]; hole 829 mm, 3.68 L of grout [I1]; installation 44 min (was 43) [I2]. No requirement changes status except R11, now reported against the value-engineering target. | Follows the model. |
| Drawing | SLW-DWG-001 Rev P3 to P4; making sketches SLW-DWG-101 to 116 added. | Follows the model. |
| Documents | SLW-PRC-001 v0.5, SLW-REQ-001 v0.5, SLW-CAL-001 v0.3; build plan SLW-BLD-001 and design decisions register SLW-DEC-001 added. | Follows the model. |
| Appearance model | `cad/src/product_model.py` and the photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` still show the concept head (120 mm cap, single gland, drip loop) and are stale. The appearance session's proposed cap screws (2026-09-26 item 3) are now part of the design as the two head screws; its conduit stub (item 4) is replaced by the two conduit fittings. | Renders are made on Amish's Mac. |

*Table 3. Proposed for Amish; A1 to A3 decided on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The side-mounted alert unit lowers the optional mast's margin in a 35 m/s gust from a factor of 2.1 to 1.7 on yield [H2]. | (a) accept 1.7 for the prototype; (b) narrow the alert back plate below the box to cut its wind area; (c) a 60.3 mm mast where the mast option is used. | (a) for the prototype, with the mast checked against local wind data before a site installation. Decided on 2026-10-02: (a) for the prototype on a fenced test slope with no one under the mast in high wind; any site installation uses (c), the 60.3 mm mast, unless local gust data show winds well below 35 m/s. |
| A2 | The pole fixing (V-blocks and band clamps) fits round poles of 40 to 70 mm. The reference site says "an existing pole or building", and many existing poles are larger timber poles. | (a) state the reference site as a 40 to 70 mm round pole, the mast otherwise; (b) add four wall holes to both back plates so the node and alert unit can be coach-screwed to a timber pole or wall; (c) longer bands and a wider V for large poles. | (b): it keeps the "pole or building" scope with no new part. Accepted by Amish, 2026-10-02; the back plate change is to be agreed with FieldNode. |
| A3 | Which pole the first prototype goes on. | (a) build the optional mast, so the prototype stands alone on a test slope; (b) use an existing 48 mm pole at the test site. | (a). Accepted by Amish, 2026-10-02. |

## Consequences

- With A1 to A3 decided, the first prototype stands on the optional mast on a fenced test slope, both back plates get four wall holes (to be agreed with FieldNode), and site installations use the 60.3 mm mast unless local gust data allow the 48.3 mm one.
- `design_state: constructable` in `project.yaml`. The build plan SLW-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status (SLW-CAL-001 v0.3): 0 not met, 4 at risk (R6, R7, R8, R9), 4 met on paper, 2 met by design, 2 not verifiable at TRL 3, and R11 over the value-engineering target by $46.50.
- The capsule's board size, the stake head's socket fit on the pipe, the sensor's rod ends and the alert and switch boxes' corner holes are checked when parts are bought (SLW-DEC-001).
- TRL 4 stays on hold by Amish's instruction; nothing here authorizes building or testing.
