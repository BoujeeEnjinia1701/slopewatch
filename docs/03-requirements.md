---
doc_id: SLW-REQ-001
title: SlopeWatch requirements
project: SlopeWatch
doc_type: Requirements
version: "0.7"
status: Draft
date: '2026-10-02'
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from SLW-CAL-001; R11 redefined to SlopeWatch-specific parts (SLW-DDR-001 D1); reference-site layout and FieldNode port assumptions stated
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from SLW-CAL-001 v0.3 for the constructable design (SLW-DDR-003); R11 reported against the value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: R7, R8 and threshold notes from the decisions of 2026-10-02 (SLW-DEC-001); no requirement changed status
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R11 figures from SLW-CAL-001 v0.4 (stake head marking, USD 54.00 over the target); no requirement changed status"
---

# SlopeWatch requirements

These are first-pass requirements for one monitored site. Four of the thirteen are met on paper by calculation and two by design; four are at risk, two can only be shown in the field, and R11 (cost) is reported against its value-engineering target (SLW-CAL-001 v0.4, Table 3). None is unmet. The `budget_usd` figure of $250 is a hypothetical value-engineering target, not a spending limit. Value-engineering target: USD 250. Estimated cost of the constructable design (SLW-DDR-003): USD 304.00 for the reference site (USD 54.00 over the target), and $332.00 where a new mast is needed. Amish decided on 2026-09-25 (SLW-DDR-002) that the reference site mounts the node on an existing pole, with a new mast as a site option. R11 was redefined under SLW-DDR-001 D1 (the FieldNode core is costed in the FieldNode project), now also decided by Amish. Targets are still proposals, not yet validated with users, and will be revised after co-design sessions (see SLW-PRB-001). "Met on paper" means shown by calculation, not by test.

The **reference site** is a slope or dump face up to about 50 m wide with three tilt stakes 10 m apart on the fall line, one crack gauge across a tension crack at the crest, and the FieldNode core and alert unit on an existing pole or building 15 m beyond the toe, within 60 m of cable, with the keyed silence switch on its own post about 5 m from the siren. Where no pole exists, the optional mast (BOM line 8) takes its place (SLW-DDR-002).

Table 1. SlopeWatch requirements for one site.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (SLW-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Measure surface tilt | Resolution 0.01 degrees or finer; range ±30 degrees or more on two axes | Datasheet and calculation; later bench tilt table | Met on paper: 0.0055 degree step and ±90 degrees in the sensor's mode 1 (modes 3 and 4 stop at ±10 degrees) |
| R2 | Limit false tilt from temperature | Apparent tilt change from the daily soil temperature cycle 0.02 degrees or less per day, and 0.002 degrees per hour or less, without software correction | Thermal calculation; later chamber test (CalRig) | Met on paper with the capsule 0.4 m deep: 0.0092 degrees per day and 0.0012 degrees per hour in wet soil; not met at the TRL 2 depth of 0.3 m in wet soil |
| R3 | Measure crack opening | Range 100 mm or more; resolution 0.1 mm; re-settable in the field without tools beyond a spanner | Datasheet and design review | Met by design (datasheet class); precaution rate taken over 24 h because of the gauge's own thermal swing |
| R4 | Sample and report often enough to see acceleration | Every sensor read every 10 min or faster; uplink every 60 min in the normal state and every 10 min in the precaution or warning state | Firmware sketch review; airtime calculation | Met on paper: 0.30 % of time at SF12 against the 1 % EU868 limit; a site that runs at SF12 uses a TwinKit gateway rather than The Things Network (SLW-DDR-002) |
| R5 | Local alarm without a network | Siren and beacon start within 60 s of a warning condition, driven by the on-site node alone | Design review; later bench test | Met by design: about 13 s |
| R6 | Remote alert | At least two named people notified by SMS or app within 5 min of a warning, where gateway and mobile coverage exist | Latency calculation; later end-to-end test | **At risk:** 1.6 min at the first try, 4.6 min at SF12 with one lost uplink; no remote alert at a site without a gateway |
| R7 | Alarm audible where people work | 65 dB(A) or more at 100 m from the mast in open ground | Spreading-loss calculation; later field measurement | **At risk:** 65.5 to 68.5 dB(A) in open ground; **not met** near running machinery. The keyed switch now sits about 5 m from the mast, at about 95 dB(A) instead of 105 dB(A) (SLW-DDR-002). Sites with running machinery get a second alert unit at the work face, linked by LoRa (decided 2026-10-02) |
| R8 | Energy autonomy | 5 days with no sun, including one 30 min alarm, on the FieldNode cell | Energy calculation | Met on energy (7.3 Wh of 13.1 Wh at -10 °C, with the precaution beacon at 1 % duty or less, decided in SLW-DDR-002); **at risk** on the FieldNode 12 V rail current (0.45 A, no rating stated; FieldNode asked to rate it at 0.5 A or more, SLW-DDR-002); if FieldNode has not rated it before the TRL 4 build, the alert unit gets its own small battery (decided 2026-10-02) |
| R9 | Survive burial and weather | Capsule and stake head IP67 and buried to 0.4 m; node IP65; operate -10 to 50 °C; cable in conduit rated for burial and UV | Datasheets and design review | **At risk:** SlopeWatch parts met by choice of parts; the FieldNode enclosure exceeds 60 °C in 45 °C sun (FND-CAL-001) |
| R10 | Installable by a small team | Each stake installed by two trained people with hand tools (post-hole auger or driven pilot, hand-mixed grout) in 45 min or less; no work below an actively moving face | Method review; later timed trial | **Not verifiable at TRL 3:** 44 min estimated for the constructable design, at the limit |
| R11 | Affordable | Parts specific to SlopeWatch for one reference site (node on an existing pole) within the $250 value-engineering target, excluding the FieldNode core (costed in the FieldNode project), any LoRaWAN gateway and the optional mast, which is a site option (SLW-DDR-002) | Priced BOM (`bom/bom.csv`) | Over the value-engineering target by $54.00: $304.00 for the constructable design; $332.00 at a site that needs the optional mast |
| R12 | Open, local data | 90 days or more of raw readings kept on the node; open CSV export; works with any LoRaWAN server | Storage calculation and design review | Met on paper: 363 kB for 90 days on 16 MB of flash |
| R13 | Trustworthy alarms | No more than one false warning per site per year, and a documented statement of the failure modes the system cannot detect | Field trial with partner | **Not verifiable at TRL 3**; statement in SLW-PRC-001 |

## Assumptions

- Tilt thresholds of 0.01 degrees per hour (precaution) and 0.1 degrees per hour (warning) follow Uchimura et al. (2015); site-specific thresholds must be set with a geotechnical engineer after a baseline period. Until a geotechnical partner has set them for a site, the thresholds drive logging only, not public alarms (decided 2026-10-02).
- The FieldNode core provides about 19 Wh of LiFePO4 storage (3.2 V, 6 Ah), switched 3.3, 5 and 12 V rails on two M12 5-pin ports (one rail per port), SPI flash and a LoRaWAN radio, as described in FND-PRC-001 and FND-REQ-001 v0.3. SlopeWatch uses one port at 5 V for the sensor bus and the other at 12 V for the alert unit.
- Siren sound level 110 dB(A) at 1 m, from typical 12 V piezo sirens; spherical spreading with air absorption and 0 to 3 dB of ground attenuation (SLW-CAL-001, section E).
- Soil temperature ranges and properties as in SLW-CAL-001, Table 1.
- Stake spacing and site layout will change after co-design; R11 is stated for the reference site only.
- Network rule (SLW-DDR-002): a site whose uplinks need SF12 uses its own gateway (TwinKit), because hourly uplinks at SF12 take 43.5 s a day, over The Things Network's 30 s fair-use allowance.
