---
doc_id: SLW-REQ-001
title: SlopeWatch requirements
project: SlopeWatch
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
---

# SlopeWatch requirements

These are first-pass requirements for one monitored site. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design sessions (see SLW-PRB-001). The status column gives the position against the first-order estimates in SLW-PRC-001; "met" means met on paper only.

The **reference site** is a slope or dump face up to about 50 m wide with three tilt stakes on the fall line, one crack gauge across a tension crack at the crest, and a mast with the FieldNode core and alert unit at the toe, within 60 m of cable.

Table 1. SlopeWatch requirements for one site.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Measure surface tilt | Resolution 0.01 degrees or finer; range ±30 degrees or more on two axes | Sensor datasheet; later bench tilt table | Met (datasheet) |
| R2 | Limit false tilt from temperature | Apparent tilt change from the daily soil temperature cycle 0.02 degrees or less per day, and 0.002 degrees per hour or less, without software correction | Thermal estimate; later chamber test (CalRig) | Met, thin margin (estimate) |
| R3 | Measure crack opening | Range 100 mm or more; resolution 0.1 mm; re-settable in the field without tools beyond a spanner | Datasheet and design review | Met (datasheet class) |
| R4 | Sample and report often enough to see acceleration | Every sensor read every 10 min or faster; uplink every 60 min in the normal state and every 10 min in the precaution or warning state | Firmware sketch review; airtime estimate | Met |
| R5 | Local alarm without a network | Siren and beacon start within 60 s of a warning condition, driven by the on-site node alone | Design review; later bench test | Met by design |
| R6 | Remote alert | At least two named people notified by SMS or app within 5 min of a warning, where gateway and mobile coverage exist | Design review; later end-to-end test | Met only where coverage exists; **not met** at sites without a gateway |
| R7 | Alarm audible where people work | 65 dB(A) or more at 100 m from the mast in open ground | Spreading-loss estimate; later field measurement | **At risk:** about 65 to 70 dB(A) estimated in quiet ground; **not met** near running machinery |
| R8 | Energy autonomy | 5 days with no sun, including one 30 min alarm, on the FieldNode cell | Energy estimate | Met on energy; **at risk** on FieldNode 12 V rail current (open question) |
| R9 | Survive burial and weather | Capsule and stake head IP67 and buried to 0.4 m; node IP65; operate -10 to 50 °C; cable in conduit rated for burial and UV | Datasheets and design review | Unverified |
| R10 | Installable by a small team | Each stake installed by two trained people with hand tools (post-hole auger or driven pilot, hand-mixed grout) in 45 min or less; no work below an actively moving face | Method review; later timed trial | Unverified |
| R11 | Affordable | Parts for one reference site $250 or less | Priced BOM (`bom/bom.csv`) | **Not met:** about $380 with the FieldNode core; about $254 without it |
| R12 | Open, local data | 90 days or more of raw readings kept on the node; open CSV export; works with any LoRaWAN server | Design review | Met (FieldNode flash) |
| R13 | Trustworthy alarms | No more than one false warning per site per year, and a documented statement of the failure modes the system cannot detect | Field trial with partner | **Not verifiable at TRL 2**; statement drafted in SLW-PRC-001 |

## Assumptions

- Tilt thresholds of 0.01 degrees per hour (precaution) and 0.1 degrees per hour (warning) follow Uchimura et al. (2015); site-specific thresholds must be set with a geotechnical engineer after a baseline period.
- The FieldNode core provides about 19 Wh of LiFePO4 storage (3.2 V, 6 Ah), a switched 5 V and 12 V sensor rail, SPI flash and a LoRaWAN radio, as described in the FieldNode README.
- Siren sound level 110 dB(A) at 1 m, from typical 12 V piezo sirens; free-field spreading of 6 dB per doubling of distance.
- Daily temperature range at the soil surface about 20 °C, damped to about 10 to 15 % of that at 0.3 m depth in moist soil (estimate).
- Stake spacing and site layout will change after co-design; R11 is stated for the reference site only.
