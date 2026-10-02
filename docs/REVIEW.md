# Review note: SlopeWatch

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (SLW-PRB-001 v0.2): problem with cited figures, users, operating environment, constraints, out of scope (including failure modes it cannot detect), cited prior work, open questions; co-design checklist kept.
- `docs/03-requirements.md` (SLW-REQ-001 v0.2): 13 measurable requirements (R1 to R13) for a defined reference site, with a status column against the concept estimates.
- `docs/02-concept.md` (SLW-PRC-001 v0.2): how it works, proposed alert states, numbered components, first-order numbers (tilt resolution, temperature drift, crack gauge, airtime, energy, alarm reach, cost), design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of a 25 degree slope with three tilt stakes, crack gauge, bus cable, mast with FieldNode core, siren and beacon, and a 1.75 m person on the toe bench; a separate kit layout for the exploded view and a single-stake section for the cutaway.
- `media/`: `hero.png`, `concept-blueprint.png`/`.pdf`/`.svg`, `model.glb` and `viewer.html`, `exploded.png` (callouts 1 to 8 match the BOM), `cutaway.png` (one stake on its axis), `flow.png` (data and alert flow, latencies marked as estimates). Temporary `media/_views*` folders removed.
- `bom/bom.csv`: 10 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; concept rationale, burning platform, industry and region tables and spark expanded with cited sources; key components and safety updated.
- `project.yaml`: `problem` reworded from "Slope and tailings failures give warning" to "Slope and tailings failures often give warning", because the Brumadinho failure showed only about 30 mm of surface movement in its last year (Zhu, Zhang and Puzrin, 2024). Meaning kept; pitch, budget, TRL and other fields unchanged.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Tilt sensitivity (SCL3300 datasheet) | 0.005 degrees | R1 met |
| Temperature drift, capsule 300 mm deep | about 0.010 to 0.015 degrees per day, peak about 0.002 degrees per hour | R2 met, thin margin |
| Same sensor unburied | about 0.1 degrees per day | Would trip precaution daily |
| Airtime at 6 uplinks per hour | 0.07 % (SF10) to 0.25 % (SF12) of the 1 % EU868 limit | R4 met |
| Average sensor load on FieldNode | under 1 mW | R8 met on energy |
| 30 min alarm | about 3.2 Wh (17 % of the cell), about 2 A from the cell | R8 at risk on 12 V rail current |
| Siren at 100 m | about 65 to 70 dB(A) in open ground | R7 at risk; not met near machinery |
| Parts per site | about $380 with FieldNode, about $254 without | **R11 not met** |

Requirements not met or at risk:

- **R11 (cost) not met:** about $380 per site with the FieldNode core (52 % over $250), about $254 without it (2 % over).
- **R6 (remote alert) not met** at sites without LoRaWAN and mobile coverage; the local siren still works.
- **R7 (alarm reach) at risk** in quiet ground and **not met** near running machinery.
- **R8 at risk:** the FieldNode README does not state the 12 V rail current; the alert unit needs about 0.45 A.
- **R2 thin margin:** heat conducted down a sunlit steel pipe is not included.
- **R9, R10 unverified; R13 cannot be verified at TRL 2.**

### Proposed, awaiting Amish

Status update 2026-09-25: items 1 to 7 are decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002); items 8 and 9 had no recommendation and remain "Proposed, awaiting Amish".

1. **Budget.** (A) Raise `budget_usd` to $400 so a full site with its FieldNode fits. (B) Cost the FieldNode core in its own project, as SunSpoke does with SwapCell, and use an existing pole instead of the mast where possible, so SlopeWatch-specific parts fit $250. (C) Two stakes per site (about $339 with FieldNode). Recommendation: B. `project.yaml` budget unchanged. Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002).
2. **Tailings dams in the pitch.** Keep them with explicit limits (supplementary layer, owner and engineer of record permission, no claim to detect brittle failure), or narrow the pitch to waste dumps, pit walls and natural slopes. Recommendation: keep, with the limits stated. Pitch unchanged. Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002).
3. Surface tilt stakes plus one crack gauge, rather than borehole inclinometers or GNSS. Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002).
4. Wired RS-485 bus to one FieldNode for the prototype; wireless stakes as a later variant. Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002).
5. Murata SCL3300 inclinometer, with an ADXL355-class accelerometer as fallback. Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002).
6. Alert rules: published 0.01 and 0.1 degrees per hour thresholds as defaults; warning on one stake confirmed on two readings; keyed 30 min silence that re-arms. Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002).
7. Alert unit on the mast at the toe; a second unit near the work face or in the village as an option. Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002).
8. Accept the `problem` wording change in `project.yaml` ("often give warning"), or revert it.
9. First partner and site type for co-design (artisanal mining cooperative, quarry, or hillside community with a district disaster office).

### Safety concerns

- Installers working on moving ground; never below an active face or on a tailings dam without permits.
- False confidence: some failures give no surface warning; faults (flat battery, cut cable, silenced siren) must be reported.
- False alarms eroding trust in the siren; thresholds set with the community and an engineer.
- LiFePO4 cell in the FieldNode core; wet cement grout; mast erection near power lines; lightning on exposed masts; siren loudness at close range.

### Problems and notes

- The kit's cutaway cuts at the mean part center, which missed the stakes, and the 10 m site made the exploded view unreadable. `concept_media.py` therefore renders the exploded view from a kit layout (one of each item) and the cutaway from a single stake, both with the kit's `_render`. Scene parts in `render_all` have no explode offsets, so `render_all` does not overwrite these files.
- The 1.75 m person is passed as a context part so it stands on the toe bench; the kit helper would place it at the bottom of the ground block.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- Sibling dependencies: FieldNode (power, radio, flash; figures from its README), TwinKit (optional gateway), CalRig (proposed for capsule temperature characterization). SwapCell is not used.

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to check the temperature drift (including pipe conduction), alarm energy and rail current, siren reach and cost by calculation, and to produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to go through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (SLW-DDR-001 v0.1, status proposed): seven items adopted as recommended for TRL 3, open for Amish's review (D1 to D7), and three left open (O1 to O3).
- `docs/04-calcs/01-sizing.md` (SLW-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: tilt resolution and rate noise, temperature drift with soil damping and pipe conduction, crack gauge, airtime and alert latency, siren reach, energy and rail current, bus cable, mast wind load and footing, installation time, data and cost, with a status for every requirement. The script imports the model, reads the BOM and `project.yaml`, prints every number the note quotes and writes `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model of the tilt stake (pipe, grout column, capsule, foam plugs, head, gland, lead), the crack gauge (pins, clamps, sensor body, rod, guard, reader box) and the mast (pole, footing, earth rod, FieldNode massing from the FieldNode model's dimensions, siren, horn, beacon, switch box). Exports `cad/step/` and `cad/stl/` for `slopewatch-stake`, `slopewatch-crack-gauge`, `slopewatch-mast` and `slopewatch-arrangement`.
- `cad/src/sheets.py` and `cad/drawings/SLW-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:50, with a 1:10 stake section (Detail A), marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". SLW-DWG-001 was free because the concept blueprint is SLW-DWG-010.
- `bom/bom.csv` (10 lines, all priced with a supplier or supplier type) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now takes the stake, gauge and mast from the model; all of `media/` was re-rendered and every image checked; temporary `_views` folders deleted.
- SLW-PRB-001, SLW-PRC-001 and SLW-REQ-001 revised to v0.3; `README.md` (TRL badge and line, links, key components and checked numbers) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

Design changes found necessary by the calculations, within the adopted choices: the capsule moves from 0.3 m to 0.4 m deep with foam plugs above and below (R2 fails at 0.3 m in wet soil); the crack gauge gets its own RS-485 reader (+$6); the precaution beacon is held to 1 % duty (at 5 % a long precaution spell drains the cell, R8); the crack-gauge precaution rate is taken over 24 h (its own thermal swing reads as 1.22 mm per day over 3 h).

### Requirement status (SLW-CAL-001, Table 3)

1 not met, 4 at risk, 4 met on paper, 2 met by design, 2 not verifiable at TRL 3.

| ID | Status | Key number |
| --- | --- | --- |
| R11 Affordable | **Not met** | $261 SlopeWatch-specific parts with a new mast against $250; $237 on an existing pole; $387 with the FieldNode core |
| R6 Remote alert | At risk | 1.6 min at the first try; 4.6 min at SF12 with one lost uplink (limit 5 min); needs coverage |
| R7 Alarm audible | At risk | 65.5 to 68.5 dB(A) at 100 m in open ground; about 5 m of useful reach over 80 dB(A) plant |
| R8 Energy autonomy | At risk | 7.3 Wh of 13.1 Wh for five sunless days in precaution with an alarm; 0.45 A on a FieldNode 12 V rail with no stated rating |
| R9 Survive burial and weather | At risk | SlopeWatch parts IP67 by choice; FieldNode enclosure above 60 °C in 45 °C sun (FND-CAL-001) |
| R1, R2, R4, R12 | Met on paper | 0.0055 degree step, ±90 degrees in mode 1; 0.0012 degrees per hour drift at 0.4 m in wet soil; 0.30 % airtime at SF12; 363 kB for 90 days |
| R3, R5 | Met by design | 0.024 mm gauge step; 13 s to siren |
| R10, R13 | Not verifiable at TRL 3 | 43 min per stake estimated (limit 45 min); false-alarm rate needs a field record |

Key numbers: tilt-rate noise 164 times below the warning rate; SF10 and SF12 airtime 0.453 s and 1.810 s (TRL 2 said 0.4 s and 1.5 s); sensor load 2.67 mW (TRL 2 said under 1 mW); 30 min alarm 3.00 Wh; bus cable 59.2 m with a 0.096 V drop; mast 115 MPa in a 35 m/s gust (factor 2.0), footing factor 2.6.

### Decisions recorded (SLW-DDR-001)

Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002; previously adopted as recommended for TRL 3, open for his review): D1 budget option B (FieldNode core costed in FieldNode, existing pole where possible; R11 redefined to SlopeWatch-specific parts; `budget_usd` unchanged at $250, no new figure recommended); D2 tailings dams kept in the pitch with limits (pitch unchanged); D3 surface tilt stakes plus a crack gauge; D4 wired RS-485 bus; D5 SCL3300 (mode 1) with ADXL355-class fallback; D6 alert rules and thresholds; D7 alert unit on the mast at the toe, second unit optional.

### Still awaiting Amish

Status update 2026-09-25: O1 to O3 remain "Proposed, awaiting Amish"; items 4 to 8 are decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002).

1. **O1, `problem` wording** ("often give warning"), changed at TRL 2 with no recommendation. The wording stays in place; accept or revert.
2. **O2, first co-design partner and site type.** No preference stated.
3. **O3, crack-gauge thresholds** (placeholders 1 mm per day over 24 h and 1 mm per hour), to be set with a geotechnical partner.
4. **New, R11 gap with a new mast ($11).** Options: (a) treat the existing-pole case ($237) as the reference and list the mast as a site option; (b) a cheaper local mast (for example a treated timber post), which would need its own wind check; (c) raise `budget_usd` to $270. Recommendation: (a). Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002). Applied: the existing-pole case is the reference site; `budget_usd` stays $250.
5. **New, FieldNode 12 V rail (R8).** Options: (a) ask FieldNode to specify at least 0.5 A continuous on its 12 V rail; (b) give the alert unit its own small battery and charger (roughly $15, estimate). Recommendation: (a). Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002). Listed as a cross-repo action; FieldNode was not edited.
6. **New, keyed switch location (safety, R7).** The switch sits under a siren giving about 105 dB(A) there. Recommendation: move it about 5 m from the mast on its own lead. Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002). Applied (switch post).
7. **New, precaution beacon duty.** Set at 1 % or less by SLW-CAL-001 (R8); flagged here because it changes how visible the precaution state is. Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002). (1 % or less kept.)
8. **New, networks at SF12.** A site that lives at SF12 on The Things Network exceeds its 30 s per day fair use even when hourly (43.5 s). Recommendation: such sites use a TwinKit gateway. Decided by Amish, 2026-09-25: go with recommendation (SLW-DDR-002). Applied as a network rule.

Suggestion only, not in the repo: a cut-cable and flat-battery fault message as a firmware rule at TRL 4.

### Cross-repo consistency

- FieldNode (FND REVIEW, TRL 3): the FieldNode core stays $126.00, the figure used here. SlopeWatch uses one M12 port at 5 V for the bus and one at 12 V for the alert unit, consistent with FND-DDR-001's one switched rail per port; the pinout is still open there (FND O2). SlopeWatch's precaution load (29.8 mW) fits both the 115 mW and the proposed 100 mW allowance. **Conflict noted:** FieldNode's proposed firmware airtime rule (lengthen the interval at SF10 and slower on The Things Network) would stretch SlopeWatch's 10 min alert-state uplinks; SlopeWatch needs an exception for alert states or a private gateway. **Gap noted:** FieldNode does not rate its 12 V rail current (item 5 above). FieldNode's own R3 (interior temperature) is not met, which is why R9 here is at risk.
- TwinKit (TWK REVIEW, TRL 3): gateway about $290 in parts; figures here updated from $285. TwinKit's airtime figures (72 ms at SF7, 247 ms at SF9, 1.8 s at SF12) match SLW-CAL-001.
- CalRig (CLR REVIEW, TRL 2): proposed for capsule drift characterization; its 36 L chamber takes the 34 x 130 mm capsule, and its 10 to 40 °C range covers the capsule's daily swing. No conflict.
- CellGuard, MotionCore and ThermaCart are not used. SwapCell is not used.
- No other repo was edited.

### Safety concerns

- Installers working on moving ground; never below an active face or on a tailings dam without permits.
- False confidence: some failures give no surface warning; faults (flat battery, cut cable, silenced siren) must be reported.
- Siren at close range: about 105 dB(A) at the keyed switch, 4 min allowed by NIOSH; keep people away from the mast during an alarm (item 6).
- False alarms eroding trust in the siren; the crack-gauge rule must average over 24 h or its own thermal swing trips it.
- LiFePO4 cell in the FieldNode core supplying about 2 A in an alarm; wet cement grout; mast erection near power lines; lightning on exposed masts (earth rod now in the model and BOM).

### Gaps and notes

- Citations: the TRL 2 note listed no unchecked citations. The SCL3300 figures used in SLW-CAL-001 (mode ranges, noise density, 0.0055 degree output step, ±0.005 degrees per K offset drift) were checked on 2026-09-25 by WebFetch against Murata's product page and datasheet. Other citations were not re-checked this session.
- Assumptions only tests can settle: soil thermal properties, the pipe-heating model (steady state, an upper bound), siren output against its rating, auger rate and the FieldNode rail rating.
- Media: the site scene compresses the 10 m stake spacing so the parts stay visible; the calculations use the reference layout in `cad/src/model.py` (`SITE`). The kit's cutaway cuts near the mean part center, which misses the stakes, so `concept_media.py` renders the cutaway from a single stake with the kit's `_render`, as at TRL 2. In the exploded view the small capsule (item 2) sits under its callout at the scale set by the 3.8 m mast; the cutaway and Detail A on SLW-DWG-001 show it.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. `electronics/` and `firmware/` hold only placeholders. No test, build or firmware material exists.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on SLW-DDR-001 (D1 to D7), on O1 to O3 and on items 4 to 8 above. For the record only, TRL 4 would need: a bench build of one capsule and the crack-gauge reader on a FieldNode; a lab test report (TST, `environment: lab`) covering capsule offset drift over temperature in CalRig, tilt resolution on a tilt table, bus operation over 60 m of cable, siren output and 12 V rail current during a 30 min alarm; and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation", recorded in `docs/decisions/0002-recommendations-accepted.md` (SLW-DDR-002 v0.1). This session also regenerated every PDF, drawing and media file so that the footers show designmolecule.com, and rewrote the README's "What sparked the idea".

### Decisions applied and what changed

- **D1 to D7 (SLW-DDR-001):** status changed to decided in SLW-DDR-001 v0.2 and in the documents; no numbers changed. `budget_usd` stays $250 (no new figure was recommended).
- **R11 reference site (TRL 3 item 4, option a):** the node goes on an existing pole; the mast (BOM line 8, $24) is a site option. R11 restated in SLW-REQ-001 v0.4. SlopeWatch-specific cost $261 with a new mast (not met) to **$245** for the reference site (met on paper, $5 within $250); $269 where the mast is needed.
- **Keyed switch (TRL 3 item 6):** moved from the mast to its own 26.9 mm post about 5 m away on a 7 m lead. `cad/src/model.py` gains `switch_post()`; new `cad/step/slopewatch-switch-post.step` and `.stl`; SLW-DWG-001 Rev P1 to **P2**; BOM line 7 $25 to $33. Siren level at the switch 105.4 to 95.5 dB(A); NIOSH allowance 4.3 to 43 min. With the box off the mast, the mast base moment falls from 550 to 541 N·m, stress 115 to 113 MPa (factor 2.0 to 2.1), footing factor 2.6 to 2.7.
- **Precaution beacon (item 7):** 1 % duty or less kept; wording only.
- **SF12 sites (item 8):** network rule added: a site that needs SF12 uses a TwinKit gateway (hourly SF12 uplinks take 43.5 s a day against The Things Network's 30 s).
- **FieldNode 12 V rail (item 5, option a):** a request to FieldNode; see cross-repo actions.
- Documents bumped: SLW-PRB-001 0.3 to 0.4, SLW-PRC-001 0.3 to 0.4, SLW-REQ-001 0.3 to 0.4, SLW-CAL-001 0.1 to 0.2, SLW-DDR-001 0.1 to 0.2; SLW-DDR-002 v0.1 new. `sizing.py` re-run and `results.csv` rewritten; `model.py`, `sheets.py` and `concept_media.py` re-run; hero, exploded view and blueprint checked; `media/_views*` removed. `project.yaml` evidence list gains DDR-002 and the switch-post STEP.
- **README:** "What sparked the idea" now traces the idea to the 1966 Aberfan colliery tip disaster (Tip 7 had sunk by about 20 ft before it slid), with ICE and Northern Mine Research Society sources; key numbers and components updated.

### Requirement status (SLW-CAL-001 v0.2)

0 not met, 4 at risk, 5 met on paper, 2 met by design, 2 not verifiable at TRL 3.

| ID | Status | Key number |
| --- | --- | --- |
| R6 Remote alert | At risk | 4.6 min at SF12 with one lost uplink (limit 5 min); needs coverage |
| R7 Alarm audible | At risk | 65.5 to 68.5 dB(A) at 100 m; about 5 m of reach over 80 dB(A) plant |
| R8 Energy autonomy | At risk | 7.3 Wh of 13.1 Wh; 0.45 A on an unrated FieldNode 12 V rail |
| R9 Survive burial and weather | At risk | FieldNode enclosure above 60 °C in 45 °C sun (FND-CAL-001) |
| R1, R2, R4, R11, R12 | Met on paper | R11 $245 against $250 (was not met at $261) |
| R3, R5 | Met by design | 0.024 mm gauge step; 13 s to siren |
| R10, R13 | Not verifiable at TRL 3 | 43 min per stake; false-alarm rate needs a field record |

### Still awaiting Amish

1. **O1, `problem` wording** ("often give warning"): no recommendation was made; wording stays.
2. **O2, first co-design partner and site type:** no preference stated.
3. **O3, crack-gauge thresholds:** placeholders; no recommendation.

### Cross-repo actions

- **FieldNode:** rate the 12 V rail at 0.5 A or more continuous for 30 min (SlopeWatch R8).
- **FieldNode:** its proposed airtime rule (longer intervals at SF10 and slower on The Things Network) needs an exception for SlopeWatch alert states; SlopeWatch sites that need SF12 now use a TwinKit gateway.
- **TwinKit:** note that SlopeWatch sites at SF12 rely on a TwinKit gateway (about $290 in parts, outside the SlopeWatch site cost).
- No other repo was edited.

### Safety

- The keyed switch now stands about 5 m from the siren (about 95 dB(A)); people should still keep away from the mast during an alarm.
- An existing pole must carry the node, siren and beacon in wind; the installer checks it with the site owner, since SLW-CAL-001 checks only the optional mast.
- All TRL 2 and TRL 3 safety concerns above still apply.

### TRL 4

TRL 4 remains on hold by Amish's instruction. `trl: 3` and `trl_target: 3` are unchanged. Decided but on hold: the cut-cable and flat-battery fault message (firmware), the CalRig capsule drift test, bench builds and any field trial. None was started.

## Session 2026-09-26: sources strengthened

README.md only; no controlled document changed and no budget change.

| Where | Old source | New source |
| --- | --- | --- |
| Country row: Ghana | Ghana News Agency (seven deaths, early report) | Ghana Broadcasting Corporation, the national public broadcaster (eight of twelve miners killed, confirmed by police, NADMO and the ambulance service), plus Froude and Petley (2018) on landslides from illegal mining; the unsourced "collapse regularly" claim removed |
| Country row: Brazil | House of Commons Library and Zhu, Zhang and Puzrin (2024) | Same sources; the unsourced claim that the failures "drove new rules for large dams" and that small mines "remain largely unmonitored" removed |
| Country row: Myanmar | Hpakant multi-sensor study | Same source; the unsourced claim that informal mining continues on waste slopes removed |
| Burning platform, Brumadinho 30 mm | None | Zhu, Zhang and Puzrin (2024) |
| What sparked the idea | Institution of Civil Engineers and Northern Mine Research Society | Glamorgan Archives and Hansard (House of Commons, 26 October 1967) added as primary sources; ICE kept; NMRS kept only for the Tribunal's record of the tip sinking on the morning, now attributed to the Tribunal. Corrected: the 1944 slip was on Tip 4, not ground under Tip 7. Tips Act 1969 now cited. Inspiration event unchanged |

Not verified this session: the full text of the 1967 Tribunal report (the Durham Mining Museum copy could not be fetched), so the 9 to 10 ft and 20 ft figures rest on the NMRS quotation of it.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session added `cad/src/product_model.py` (an appearance model for one tilt stake, items 1 to 3 with its bus lead) and pointed the README hero image at `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced separately by the orchestrator. No controlled document, BOM line, budget or `model.py` dimension changed.

### What `product_model.py` adds

- `product_parts()`: 26 parts (13 shell, 9 internal, 4 context) with colour, material, BOM line, group and explode offset, all built from `PARAMS`, `SITE` and `derived()` in `model.py`.
- Stake head: 10 mm filleted crown, a molding line above the skirt, a white retroreflective band, a curved stake ID label with print and a teal tag, a raised teal arrow on the crown pointing downslope, two stainless cap screws, the reducer ring, and the M20 gland as a locknut, body and domed seal nut.
- Bus cable leaving the gland in a smooth drip loop into a short ribbed stub of the 20 mm corrugated conduit (item 5), which runs buried downslope.
- Below ground: the galvanized pipe, bottom plug and grout column; the potted sensor capsule with dark end caps, a teal band and a label with an up arrow; the two closed-cell foam plugs; and the capsule lead up to the gland.
- Context: a compact patch of 25 degree slope (subsoil, a 45 mm topsoil layer and a few surface stones). The front downslope quarter of the ground, grout, buried pipe and foam plugs is cut away so the capsule 0.4 m below ground shows.
- `TITLE` and three `RENDER_VIEWS`: hero (stake in the cut-away slope patch), exploded (head, pipe and grout, with the plugs, capsule and lead drawn out to the side) and detail (the stake head above ground, without the slope, so the head fills the frame).

### Where the appearance model differs from `model.py`

Each item is **Proposed, awaiting Amish**.

1. **Head colour.** The BOM says the head is "painted for visibility" without a colour. The model uses a signal amber with a white retroreflective band. Recommendation: adopt amber plus a retroreflective band, which reads at a distance and in headlamps on a working slope.
2. **Stake ID label and downslope arrow.** Neither is in the BOM. The label identifies each of the three stakes; the arrow on the crown shows that the gland must face downslope at installation. Recommendation: adopt both as item 10 consumables (printed outdoor label and a painted or molded arrow).
3. **Two cap screws.** `model.py` shows the head resting on its reducer ring with no fixing. The model adds two stainless screws through the head into the pipe, in the 40 mm overlap. Recommendation: adopt, so the head cannot be lifted or turned by animals or wind-blown debris; add them to item 10.
4. **Conduit stub at the stake.** `model.py` stops the bus lead 60 mm outside the head. The model adds a drip loop and a 20 mm conduit stub about 70 mm out of the ground, 175 mm downslope of the stake. Recommendation: adopt as the reference arrangement; the conduit is already in item 5.
5. **Lead routing inside the head.** In `model.py` the lead turns horizontal at 230 mm above ground; here it bends to the gland axis at 220 mm. The gland position and size are unchanged. No action needed beyond noting it.
6. **Pipe split at ground level.** The pipe is two render parts (above and below ground) so the detail view can omit the buried parts. Size and length are unchanged. No action needed.

The cable gland hex (30 mm across flats) is slightly larger than the 28 mm gland envelope in `model.py`; this is a cosmetic difference, not a change of gland size.

### Status

This is an appearance model only: no tolerances and no fabrication detail. `trl: 3` and `trl_target: 3` in `project.yaml` are unchanged, and TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: build plan and design for construction (kit 1.7.0)

Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with open decisions kept in a separate design decisions register. This session installed kit 1.7.0 (`CLAUDE.md` now matches `.kit/CLAUDE.md`), made the design constructable and wrote the build plan and the register. Nothing was built; TRL stays 3.

### What was done

- `cad/src/model.py`: rebuilt as separate components (`build_components()`), with 79 constructability checks (`python cad/src/model.py --check`), all passing. STEP and STL regenerated.
- `docs/decisions/0003-design-for-construction.md` (SLW-DDR-003 v0.1, Draft): every change below, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `cad/src/build_plan_media.py`: overview, 16 making sketches (`cad/drawings/SLW-DWG-101` to `116`), 12 joint close-ups, 18 assembly step pictures, a bus wiring diagram and a site layout (`docs/05-build-plan/`).
- `docs/05-build-plan.md` (SLW-BLD-001 v0.1) and `docs/06-design-decisions.md` (SLW-DEC-001 v0.1).
- SLW-DWG-001 Rev P3 to P4; SLW-CAL-001 v0.3, SLW-REQ-001 v0.5, SLW-PRC-001 v0.5; `bom/bom.csv` and `bom/bom-notes.md`; concept media re-rendered; README links line and "Building the prototype" section; `project.yaml` gains `design_state: constructable` and the new documents in `trl_evidence`.

### Design changes made for construction (SLW-DDR-003)

1. Capsule held on the pipe axis by two printed centring collars and set at 0.4 m by a 40 mm PVC stand tube on the pipe's bottom cap (the lower foam plug is replaced by the stand tube).
2. Pipe bottom closed by a screwed 1.5 in malleable-iron end cap; hole augered 829 mm so grout runs under it.
3. Stake head made from stock 110 mm drainage fittings (110 x 50 mm reducer, 94 mm of pipe, end cap), sealed on a tape wrap and held by two M5 screws drilled through the socket into the pipe.
4. Two M20 conduit fittings on each head (bus in upslope, bus out downslope) with lever connectors inside, replacing the single cable gland.
5. Crack gauge: 40 x 40 x 60 mm aluminium clamp blocks with M8 set screws, M6 rod-end ball joints, a coupling and a 501 mm stainless extension rod.
6. Guard: folded 1.5 mm galvanized channel on feet, 48 mm above the pin tops, pegged on its upslope half only (it used to pass through both pins and float).
7. Reader box hung under the guard web on two M4 screws, with a conduit fitting on its downslope end.
8. Alert unit: alert box on a 160 x 360 mm aluminium back plate clamped to the pole or mast with two V-blocks and two band clamps (the FieldNode fixing); siren centre 3.23 m on the mast; push-on mast cap.
9. Keyed switch box on a galvanized back plate held to its post by two hose clips.
10. FieldNode massing updated to its constructable design (FND-DDR-003).
11. Earth bond with a rod clamp, a mast bonding clamp and a 16 mm² conductor.

### Key results

- Requirement status (SLW-CAL-001 v0.3): 0 not met, 4 at risk (R6, R7, R8, R9), 4 met on paper, 2 met by design, 2 not verifiable at TRL 3, and R11 over the value-engineering target.
- Value-engineering target: USD 250. Estimated cost of the constructable design: USD 296.50 for the reference site (USD 46.50 over the target); $324.50 with the optional mast.
- Optional mast in a 35 m/s gust: 136 MPa, factor 1.7 on yield (was 2.1), footing factor 2.2 (was 2.7), because the alert unit's back plate is now in the wind area.
- Crack gauge thermal swing 0.36 mm a day (was 0.39); installation estimate 44 min (was 43), at the R10 limit; level at the keyed switch 95.5 dB(A).

### Proposed, awaiting Amish

See the register (SLW-DEC-001). New from this session: accept SLW-DDR-003; the mast margin (A1, recommend accept 1.7 for the prototype); mounting on larger poles or walls (A2, recommend wall holes in both back plates); the pole for the first prototype (A3, recommend the mast). Still open from earlier sessions: O1 to O3, second alert unit near machinery, cable protection and cut-cable detection, head colour and marking, and the FieldNode 12 V rail rating and port pinout.

### Stale, to regenerate on Amish's Mac

`cad/src/product_model.py`, the photoreal renders `media/render-*.png`, `media/card.png` and `media/social-preview.png` show the concept stake head (120 mm cap, one gland, drip loop into a conduit stub); the head is now a 110 mm drainage-fitting head with two conduit fittings. They were not regenerated here. `media/render-hero.png` is not in this cloud copy.

### Safety

- The build plan carries safety stops S1 to S7 (slope work, augering, grout, the FieldNode cell, raising the mast, the first siren test, leaving the site).
- The optional mast's wind margin falls to 1.7 on yield; check it against local wind data before a site installation.
- All earlier safety concerns still apply.

### Recommended next step

Amish to review SLW-DDR-003 and decide items 1 to 4 of the register. TRL 4 (building to this plan) remains on hold.

## Session 2026-10-02: open decisions decided

On 2026-10-02 Amish approved every recommendation written for the open decisions: "i approve your recommendations for all 555 open decisions." Nothing was built or tested; TRL 4 remains on hold.

### Decisions recorded

12 decisions moved from "Open decisions" to "Decisions made" in the design decisions register, dated 2026-10-02. Design for construction (SLW-DDR-003) accepted with A1 (sharpened), A2 and A3; the problem wording kept; an operating aggregate quarry named as the first partner to approach; thresholds for logging only until set per site; a second alert unit at machinery sites; cable protection and a fault message; stake marking; a battery fallback for the alert unit; FieldNode's candidate M12 pinout adopted.

### Documents changed

- `docs/01-problem.md` (SLW-PRB-001 v0.5)
- `docs/02-concept.md` (SLW-PRC-001 v0.6)
- `docs/03-requirements.md` (SLW-REQ-001 v0.6)
- `docs/05-build-plan.md` (SLW-BLD-001 v0.2)
- `docs/06-design-decisions.md` (SLW-DEC-001 v0.2)
- `docs/decisions/0001-trl2-review-decisions.md` (SLW-DDR-001 v0.3)
- `docs/decisions/0002-recommendations-accepted.md` (SLW-DDR-002 v0.2)
- `docs/decisions/0003-design-for-construction.md` (SLW-DDR-003 v0.2)
- `bom/bom-notes.md` (not a controlled document)
- `README.md` (not a controlled document)
- `docs/pdf/`: every controlled document re-rendered.

### Follow-up actions to carry approved decisions into the design

The model, drawings, build plan pictures, BOM quantities and prices, and calculations were not changed in this session. These actions carry the approved decisions into them:

1. Decision 3 (model): Add four wall holes to the alert unit back plate in cad/src/model.py; agree the same change for the FieldNode back plate with FieldNode (cross-repo).
2. Decision 3 (drawings): Alert unit back plate making sketch: add the four wall holes and a coach-screw fixing note; build plan picture of the back plate.
3. Decision 2 (calcs): SLW-CAL-001 [H2]: add the 60.3 mm mast case for site installations and state the local gust condition.
4. Decision 2 (bom): BOM line 8: add the 60.3 mm mast as the site-installation option and price it.
5. Decision 7 (docs): Firmware notes (TRL 4): run in logging-only mode until site thresholds are set by a geotechnical partner.
6. Decision 8 (bom): Price a second alert unit as an option for sites with running machinery.
7. Decision 9 (docs): Firmware notes (TRL 4): a fault message whenever a stake stops answering.
8. Decision 9 (bom): Add armoured bus cable as a priced option for rockfall zones.
9. Decision 10 (pictures): Build plan: recolour the stake head in the step and making pictures to signal amber with a retroreflective band, ID label and downslope arrow; same in the appearance model and renders.
10. Decision 10 (bom): BOM line 3: add the amber paint, retroreflective band and labels.
11. Decision 11 (bom): If FieldNode has not rated its 12 V rail before the TRL 4 build, add a small battery for the alert unit and price it.
12. Decision 12 (drawings): Build plan section 3.17 and the wiring diagram: show the M12 pin assignment (12 V on pin 1, bus on pins 2 and 4, keyed switch input on pin 5 of port B) and label the port with its rail voltage.
13. Decision 12 (docs): Cross-repo: ask FieldNode to adopt its candidate M12 pinout and to label each port with its rail voltage.
14. Decision 1 (pictures): At the next render session on Amish's Mac, redraw the photoreal renders, card and social preview to the constructable design (stake head, conduit fittings, cap screws).

### Points found in the review

Raised when the recommendations were written (2026-10-01) and not yet acted on:

- The value-engineering section prices the FieldNode core at USD 126; FieldNode's constructable design is now USD 139.
- Open decision 11 is already decided as a request to FieldNode (SLW-DDR-002, 2026-09-25); only the fallback is open.
- FieldNode publishes a 100 mW sensor allowance, while the SlopeWatch alarm draws 0.45 A at 12 V (about 5.4 W) while sounding; FieldNode's rating needs to cover alarm peaks as well as averages.
- Cross-repo with NoiseMap: ports set to different rail voltages (3.3 V and 12 V) need clear labels.
