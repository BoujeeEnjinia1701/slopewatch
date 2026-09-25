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

1. **Budget.** (A) Raise `budget_usd` to $400 so a full site with its FieldNode fits. (B) Cost the FieldNode core in its own project, as SunSpoke does with SwapCell, and use an existing pole instead of the mast where possible, so SlopeWatch-specific parts fit $250. (C) Two stakes per site (about $339 with FieldNode). Recommendation: B. `project.yaml` budget unchanged.
2. **Tailings dams in the pitch.** Keep them with explicit limits (supplementary layer, owner and engineer of record permission, no claim to detect brittle failure), or narrow the pitch to waste dumps, pit walls and natural slopes. Recommendation: keep, with the limits stated. Pitch unchanged.
3. Surface tilt stakes plus one crack gauge, rather than borehole inclinometers or GNSS.
4. Wired RS-485 bus to one FieldNode for the prototype; wireless stakes as a later variant.
5. Murata SCL3300 inclinometer, with an ADXL355-class accelerometer as fallback.
6. Alert rules: published 0.01 and 0.1 degrees per hour thresholds as defaults; warning on one stake confirmed on two readings; keyed 30 min silence that re-arms.
7. Alert unit on the mast at the toe; a second unit near the work face or in the village as an option.
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
