---
doc_id: SLW-PRC-001
title: SlopeWatch design precis
project: SlopeWatch
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, alert logic, first-order numbers, safety, media)
---

# SlopeWatch design precis

SlopeWatch watches a slope for accelerating movement with three grouted tilt stakes and a crack gauge, cabled to one FieldNode core on a mast at the toe, and sounds a siren and beacon on site when the tilt rate passes a warning threshold, while sending an SMS through LoRaWAN. First-order numbers suggest the sensors resolve far finer than the 0.01 degrees per hour precaution threshold, that burying the sensor capsule keeps temperature drift about 5 times below that threshold, and that the sensors add under 1 mW to the FieldNode's load. A site costs about $380 in parts with the FieldNode core, or about $254 without it, so the $250 budget is not met.

![Hero render](../media/hero.png)

*Figure 1. SlopeWatch on a 25 degree slope: three tilt stakes on the fall line, a crack gauge (purple) across a tension crack at the crest, and the mast with FieldNode core, siren and beacon at the toe. Grey figure: 1.75 m person for scale.*

## How it works

1. **Sense tilt.** Each tilt stake is a 48 mm steel pipe grouted 0.8 m into the slope's surface layer. A sealed capsule with a MEMS inclinometer sits inside the pipe about 300 mm below ground. When the surface layer creeps downslope, the stake rotates with it; the approach and its thresholds follow Uchimura et al. ([2015](https://www.sciencedirect.com/science/article/pii/S0038080615001122)).
2. **Sense cracks.** A crack gauge spans a tension crack near the crest, where movement often shows first: two anchor pins either side of the crack and a 100 mm linear displacement sensor between them, under a guard.
3. **Collect.** A four-core cable in conduit links all sensors on an RS-485 bus to the FieldNode core on the mast. Every 10 min the node switches the bus on, reads each capsule and the gauge, and switches it off.
4. **Decide.** The node computes the tilt and opening rate for each sensor and runs the alert rules below. Raw readings are kept on the node's flash for at least 90 days.
5. **Alarm.** In the warning state the node drives the siren and beacon directly from its 12 V rail, with no network needed, and raises its uplink rate from hourly to every 10 min.
6. **Notify and review.** Readings reach any LoRaWAN server (the lab's TwinKit gateway or The Things Network). An open alert service sends SMS or app messages to named people and plots inverse velocity against time ([Fukuzono, 1985](https://www.jstage.jst.go.jp/article/jls1964/22/2/22_2_8/_article)) for the engineer.

![Data and alert flow](../media/flow.png)

*Figure 2. Data and alert flow for one site. The local siren path does not depend on the network. All latencies are estimates.*

### Alert rules (proposed, awaiting Amish)

Table 1. Proposed alert states. Thresholds for crack opening are placeholders to be set per site.

| State | Entered when | Action |
| --- | --- | --- |
| Normal | No condition below | Read every 10 min; uplink hourly |
| Precaution | Any stake tilts faster than 0.01 degrees per hour averaged over 3 h, or the crack opens faster than 1 mm per day (placeholder) | Uplink every 10 min; message to the site manager and engineer; beacon flashes slowly |
| Warning | Any stake tilts faster than 0.1 degrees per hour over 1 h, confirmed on two consecutive readings, or the crack opens faster than 1 mm per hour (placeholder) | Siren and fast beacon on site; SMS to everyone on the list; inverse-velocity plot flagged |
| Silenced | Keyed switch at the mast | Siren off for 30 min, beacon stays on; the node re-arms automatically |

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

Table 2. Main components.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Tilt stake (3 per site) | 48 mm galvanized steel pipe, 1.0 m long, 0.8 m in ground, lower 450 mm in a 110 mm grout column | Couples the stake to the surface layer |
| 2 | Tilt sensor capsule (3) | Murata SCL3300 inclinometer, small microcontroller, RS-485 transceiver and regulator, potted in a 34 mm tube | Sits about 300 mm below ground to damp temperature swings |
| 3 | Stake head (3) | 120 mm PVC cap with cable gland facing downslope | Keeps rain out of the pipe; marks the stake |
| 4 | Crack displacement gauge | 100 mm linear potentiometer displacement sensor between two anchor pins, with guard | Re-settable when the crack opens past range |
| 5 | Sensor bus cable | Four-core shielded outdoor cable (power and RS-485) in corrugated conduit, about 60 m | Surface-laid in the prototype; buried where the ground allows |
| 6 | FieldNode core | Lab shared node: IP65 box, 6 W panel, LiFePO4 3.2 V 6 Ah, MPPT charger, STM32WL-class LoRaWAN radio | Costed in the FieldNode project; see its README |
| 7 | Siren and beacon alert unit | 12 V piezo siren, about 110 dB(A) at 1 m, and an amber LED beacon, switched by the node | Keyed silence switch at the mast |
| 8 | Mast and footing | 50 mm galvanized pipe, about 3.2 m, in a 0.6 m concrete footing | An existing pole or building can replace it |
| 9 | Gateway and alert software | Any LoRaWAN server; open alert service with SMS and inverse-velocity plot | Not shown in the media; gateway not in site cost |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view of one of each kit item, with numbered callouts matching the BOM. A site uses three stakes (items 1 to 3).*

![Cutaway of one tilt stake](../media/cutaway.png)

*Figure 4. Section through one tilt stake on its axis, showing the grout column, the capsule about 300 mm below ground and the lead to the cable gland.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

### Tilt resolution and thresholds

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Inclinometer sensitivity | 0.005 degrees near level | SCL3300 inclination mode ([Murata](https://www.murata.com/en-us/products/sensor/inclinometer/overview/lineup/scl3300)) | R1 met |
| Inclinometer noise | 0.001 degrees per √Hz | Same source; 10 s averaging makes noise negligible against thresholds | R1 met |
| Precaution rate over 3 h | 0.03 degrees of change | 0.01 degrees per hour; 6 times the sensitivity | |
| Warning rate over 1 h | 0.1 degrees of change | About 1.7 mm per hour at 1 m of stake length | |

### Temperature drift

Assumptions: SCL3300 offset drift up to 0.005 degrees per °C (datasheet class figure); daily soil surface range about 20 °C; damping at 0.3 m depth to about 10 to 15 % of the surface range in moist soil; sinusoidal daily cycle.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Daily range at the capsule | about 2 to 3 °C | 20 °C x 0.10 to 0.15 | |
| Apparent tilt change per day | about 0.010 to 0.015 degrees | x 0.005 degrees per °C | R2 (0.02) met |
| Peak apparent tilt rate | about 0.002 degrees per hour | Half-range x 2π / 24 h | R2 met, thin margin; about 5 times below the precaution threshold |
| Same sensor at the surface, unburied | about 0.1 degrees per day, about 0.013 degrees per hour | 20 °C x 0.005 | Would trip precaution daily; shows why the capsule is buried |

Heat conducted down the steel pipe from a sunlit head is not included and is an open question; a plastic pipe or an insulating plug above the capsule may be needed. The capsule's own temperature sensor allows a software correction later, and the CalRig chamber can measure each capsule's drift before deployment.

### Crack gauge

A 100 mm linear potentiometer read by a 12-bit converter gives steps of about 0.025 mm; the practical resolution is limited by the sensor's linearity and friction, and 0.1 mm (R3) is expected to be met with a sensor of 0.1 % linearity class.

### Data, radio and energy

Assumptions: 20-byte uplink; LoRaWAN EU868 at SF10 (about 0.4 s airtime) or SF12 (about 1.5 s); each capsule powered for about 2 s per reading at about 6 mA and 3.3 V (sensor 1.2 mA, microcontroller and transceiver about 5 mA); siren 0.25 A and beacon 0.2 A at 12 V; 85 % boost converter efficiency; FieldNode cell 3.2 V, 6 Ah.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Airtime at 6 uplinks per hour | about 2.4 s per hour (SF10), about 9 s per hour (SF12) | 0.07 % and 0.25 % of the 1 % EU868 duty cycle | R4 met |
| Sensor energy per 10 min cycle | about 0.15 J | 3 capsules x 40 mJ plus gauge and bus switching | |
| Average sensor load | under 1 mW | 0.15 J / 600 s = 0.25 mW, rounded up for bus standby | Far below FieldNode's 115 mW sensor allowance |
| Alarm power | about 5.4 W at 12 V; about 2 A from the cell | 12 V x 0.45 A / 0.85 / 3.2 V | R8 at risk on rail current |
| 30 min alarm energy | about 3.2 Wh, about 17 % of the cell | 5.4 W x 0.5 h / 0.85 | R8 met on energy |
| Bus voltage drop, 60 m, 20 mA | about 0.1 V | 0.5 mm² conductors, about 4.3 Ω loop | |
| Raw data per day | about 3 kB | 5 channels x 4 bytes x 144 readings | R12 met; 90 days is about 0.3 MB |

### Alarm reach

A siren of about 110 dB(A) at 1 m falls by 6 dB per doubling of distance in open ground: about 70 dB(A) at 100 m before ground and air absorption, so about 65 to 70 dB(A) in practice (R7 at risk). That is audible over a quiet village but not over running excavators, crushers or generators. Sites with machinery will need a second alert unit near the work face or a radio link to the operator; this is an open question.

### Cost

Table 3. Indicative parts cost for the reference site (see `bom/bom.csv`).

| Group | Indicative cost | Requirement |
| --- | --- | --- |
| Stakes, capsules and heads (items 1 to 3, three sets) | about $123 | |
| Crack gauge, cable, alert unit, mast, consumables (items 4, 5, 7, 8, 10) | about $131 | |
| **SlopeWatch-specific parts** | **about $254** | R11 not met, about 2 % over |
| FieldNode core (item 6, costed in FieldNode) | about $126 | |
| **Site total with FieldNode** | **about $380** | R11 not met, about 52 % over |
| LoRaWAN gateway, if the site has no coverage | not in site cost (TwinKit gateway about $285) | |

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **Budget.** Option A: raise `budget_usd` to $400 so a full site with its FieldNode fits. Option B: cost the FieldNode core in its own project, as SunSpoke does with the SwapCell pack, and close the remaining $4 by using an existing pole in place of the mast where one exists; the budget then covers SlopeWatch-specific parts. Option C: two stakes per site instead of three (about $339 with FieldNode), which weakens confirmation between stakes. Recommendation: B. `project.yaml` is unchanged.
- **Surface tilt stakes plus a crack gauge.** Alternatives are borehole in-place inclinometers (see deep movement but need a drill rig and cost far more), GNSS receivers (absolute position, but costly and slower to resolve millimeters), or crack gauges and wire extensometers alone (cheap, but only where cracks exist). Recommendation: tilt stakes plus one crack gauge.
- **Wired bus to one FieldNode.** One node and a cable bus costs about $27 per extra stake; a FieldNode on every stake costs about $126 per stake but avoids cables across moving ground. Recommendation: wired for the prototype, with a wireless stake variant recorded for later.
- **Inclinometer.** A dedicated MEMS inclinometer (SCL3300 class) rather than a general-purpose accelerometer, because its low noise and stated offset stability meet R1 and R2; a low-noise accelerometer (ADXL355 class) is the fallback. Recommendation: SCL3300.
- **Warning confirmation.** Warning on one stake confirmed on two consecutive readings (20 min) rather than requiring two stakes to agree, so a single moving block is not missed; review false alarms after a baseline period. Recommendation: single stake with two-reading confirmation.
- **Alert unit location.** On the mast at the toe for the prototype; a second unit near the work face or in the village, linked by LoRa, as an option after co-design.
- **Tailings dams in the pitch.** Keep them, with the scope limits in SLW-PRB-001 (supplementary layer only, installed with the owner's and engineer of record's permission, no claim to detect brittle failure), or narrow the pitch to waste dumps, pit walls and natural slopes. Recommendation: keep, with the limits stated in every document.
- **Alert thresholds.** Adopt the published 0.01 and 0.1 degrees per hour tilt-rate thresholds as defaults, with site values set by an engineer after a baseline period.

## Safety

> **Safety:** SlopeWatch is installed on ground that may already be moving and is meant to protect people from a slope failure. The two main hazards are harm to the installers and false confidence in the system. It is a research prototype and does not replace engineered monitoring, a trigger action response plan or evacuation planning.

- **Working on unstable slopes.** Install and service only with a partner's trained team, after a visual check by a competent person; never work below an actively moving face, below overhanging material or on a tailings dam crest or face without the owner's permit and the engineer of record's approval. Use a spotter, keep an escape route clear, and stop work in or after heavy rain.
- **False confidence and missed warnings.** A system that is silent is not proof of a safe slope. Brittle failures, failures deeper than the stakes, failures between stakes, earthquakes and heavy rain can all bring a slope down with little surface warning. Every site sign, SMS and document must say what SlopeWatch cannot detect. Flat batteries, cut cables and silenced sirens must raise a fault message.
- **False alarms.** Repeated false alarms teach people to ignore the siren. Thresholds and confirmation rules must be set with the community and reviewed after each alarm.
- **Lithium cell.** The FieldNode core holds a 19 Wh LiFePO4 cell. Use the FieldNode's fuse and cold-charge lockout, do not charge a damaged cell, and keep the box out of standing water.
- **Cement grout.** Wet cement is alkaline and can burn skin and eyes. Wear gloves and eye protection and wash off splashes at once.
- **Mast and height.** Erecting a 3.2 m mast needs two people; keep well clear of overhead power lines. An exposed mast on a ridge can attract lightning: bond the mast to an earth rod and fit surge protection where the long bus cable enters the node.
- **Noise.** A 110 dB(A) siren can damage hearing at close range. Mount it at least 3 m above ground and silence it only with the keyed switch.

## Open questions for TRL 3

- Measure temperature drift of a buried capsule, including heat conducted down a steel pipe, and choose steel or plastic pipe (R2).
- Confirm that the FieldNode 12 V rail can supply about 0.45 A for 30 min, or add a small local battery to the alert unit (R8).
- Decide how to protect a surface cable from rockfall and movement, and how to detect a cut cable.
- Check siren reach at a real site and decide whether sites with machinery need a second alert unit (R7).
- Set crack-gauge thresholds with a geotechnical partner.
- Confirm LoRaWAN coverage at candidate sites, or budget a gateway.
- Close the cost gap or approve a budget option (R11).
- Choose the first partner and site type for co-design.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
