---
doc_id: SLW-CAL-001
title: SlopeWatch sizing calculations
project: SlopeWatch
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (tilt resolution, temperature drift with pipe conduction, crack gauge, airtime and latency, alarm reach, energy and rail current, bus cable, mast wind load, installation, data, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# SlopeWatch sizing calculations

On paper, SlopeWatch meets seven of its thirteen requirements (five by calculation, two by design), has four at risk, misses none and leaves two that only a field trial can show. This issue applies Amish's decisions of 2026-09-25 (SLW-DDR-002): the reference site mounts the node on an existing pole, with a new mast as a site option, so R11 is met at $245 against $250 ($269 with the optional mast); and the keyed silence switch moves to its own post about 5 m from the siren, which cuts the level there from about 105 to about 95 dB(A). The four at risk are the remote alert time at the slowest radio setting (R6), siren reach (R7), the FieldNode 12 V rail current during an alarm (R8) and the FieldNode enclosure temperature (R9). The v0.1 calculations changed four details of the TRL 2 concept: the sensor capsule moves from 0.3 m to 0.4 m deep, because at 0.3 m wet soil lets the daily temperature cycle through faster than R2 allows; the crack gauge gets its own RS-485 reader; the precaution beacon is limited to 1 % duty, because a 5 % slow flash would drain the cell in a long precaution spell; and the crack-gauge precaution rate is taken over 24 h. Every number here is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B5], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that any slope is safe or that an alarm will come in time. SlopeWatch cannot warn of brittle failures, deep-seated movement or failures between its stakes. See SLW-PRC-001, Safety.

## Scope and method

The note checks every requirement in SLW-REQ-001 v0.4 against the design in SLW-PRC-001 v0.4 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `SITE` and `derived()`, so the pipe, capsule depth, grout column, gauge, mast and cable run used here are the ones in the STEP files and in drawing SLW-DWG-001. It reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes the results table to `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is the reference site of SLW-REQ-001: three stakes 10 m apart on the fall line of a 25 degree face (20 m of face, 8.5 m of rise), a crack gauge 8 m above the top stake, and the node on an existing pole (or the optional mast) 15 m beyond the toe, with the keyed switch on its own post about 5 m from the siren, and ambient -10 to 50 °C at the surface.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Inclinometer | SCL3300-D01 in mode 1: ±90 degrees, noise density 0.0024 degrees per √Hz, angle output 0.0055 degrees per LSB; offset temperature drift ±0.005 degrees per K | Murata [datasheet](https://www.murata.com/-/media/webrenewal/products/sensor/pdf/datasheet/datasheet_scl3300-d01.ashx) and [product page](https://www.murata.com/en-us/products/sensor/inclinometer/overview/lineup/scl3300), both checked 2026-09-25 |
| Reading | Bus on for 12 s every 10 min: 2 s start-up and a 10 s average | Design choice |
| Soil temperature | Sinusoidal daily cycle; surface range 20 K in moist and wet soil, 30 K in dry soil; diffusivity 0.3, 0.6 and 1.0 mm²/s and conductivity 0.4, 1.0 and 1.6 W/mK for dry, moist and wet soil | Handbook ranges for mineral soils; to be confirmed at a site |
| Pipe heating | 160 mm of bare pipe between ground and head in full sun (900 W/m², absorptance 0.6), 10 W/m²K to air; steel 50 W/mK; buried pipe treated as a fin losing heat to the soil; steady state (no heat capacity), so an upper bound | Screening values |
| Crack gauge | 12-bit converter on a 100 mm potentiometer of 0.1 % linearity; steel rod and aluminum body see a 30 K daily range under the guard | Typical parts |
| Radio | LoRaWAN EU868, 125 kHz, coding rate 4/5, 20-byte payload plus 13 bytes of overhead; 45 mA at 3.3 V while transmitting; network server 5 s, alert service 30 s and SMS delivery 60 s | Semtech airtime formula; service times assumed |
| Siren | 110 dB(A) at 1 m; spherical spreading; air absorption 0.015 dB/m near 3 kHz; 0 to 3 dB excess ground attenuation | Typical 12 V piezo siren; order of magnitude from ISO 9613-1 |
| Energy | FieldNode cell 3.2 V, 6 Ah, 80 % usable, 85 % of capacity at -10 °C; rail converters 90 %; core 4 mWh/day (FND-CAL-001); capsule 6 mA and reader 5.5 mA at 5 V; siren 0.25 A and beacon 0.2 A at 12 V | FieldNode figures; parts typical; cold factor assumed |
| Wind | 35 m/s gust (735 Pa); drag coefficients 1.2 (panel, pole, alert unit) and 1.3 (boxes); medium soil 18 kN/m³, Kp = 3 | Screening values as in FND-CAL-001 and WWT-CAL-001; not a code check |

## A. Tilt measurement (R1)

- **Resolution and range.** The angle output steps by 0.0055 degrees in every mode. Mode 1 spans ±90 degrees; modes 3 and 4, the low-noise inclination modes, stop at ±10 degrees [A1], which would not meet the ±30 degree range of R1. The firmware must therefore use mode 1.
- **Noise.** A 10 s average in mode 1 has 0.00054 degrees of noise [A2]. A least-squares rate over 1 h (7 readings) has 0.00061 degrees per hour of noise, 164 times below the warning rate; over 3 h (19 readings) it is 74 times below the precaution rate [A3], [A4].
- **Meaning.** The warning rate of 0.1 degrees per hour is 1.75 mm per hour at 1 m from the pivot, and the precaution change over 3 h is 5.5 output steps [A5]. **R1 is met on paper.**

## B. Temperature drift of a buried capsule (R2)

The daily soil temperature wave shrinks with depth by exp(-z/d), where d is the damping depth, 91 to 166 mm for dry to wet soil [B2]. Heat also runs down the steel pipe from its sunlit exposed length, which absorbs 4.17 W in full sun [B1] and would sit up to 8.8 K above the soil at ground level [B3]; the buried pipe sheds that heat to the soil within about 0.1 m.

*Table 2. Daily temperature range at the capsule and apparent tilt, against R2 (0.02 degrees per day and 0.002 degrees per hour) [B2].*

| Capsule depth | Soil, surface range | Soil range at capsule | Added by pipe | Apparent tilt per day | Peak apparent rate | R2 |
| --- | --- | --- | --- | --- | --- | --- |
| 0.3 m | Dry, 30 K | 1.10 K | 1.36 K | 0.0123 degrees | 0.00161 degrees/h | Met |
| 0.3 m | Moist, 20 K | 1.94 K | 0.34 K | 0.0114 degrees | 0.00149 degrees/h | Met |
| 0.3 m | Wet, 20 K | 3.28 K | 0.13 K | 0.0170 degrees | **0.00223 degrees/h** | **Not met** |
| 0.4 m | Dry, 30 K | 0.37 K | 0.82 K | 0.0059 degrees | 0.00078 degrees/h | Met |
| 0.4 m | Moist, 20 K | 0.89 K | 0.15 K | 0.0052 degrees | 0.00068 degrees/h | Met |
| 0.4 m | Wet, 20 K | 1.79 K | 0.05 K | 0.0092 degrees | 0.00120 degrees/h | Met |

- **The TRL 2 depth misses R2 in wet soil.** Wet soil carries the daily wave deeper, and the peak apparent rate at 0.3 m exceeds 0.002 degrees per hour. At 0.4 m every case passes; the design case (wet soil) has a margin of 1.66 on the hourly limit and 2.18 on the daily limit, and the precaution threshold is 8.3 times the thermal rate [B5]. The capsule now sits 0.4 m deep, the depth R9 already names.
- **Pipe conduction matters in dry soil.** In dry soil the pipe adds more than the soil does (0.82 K against 0.37 K at 0.4 m), because dry soil conducts heat away poorly. The steel pipe still passes, so the TRL 2 question of steel or plastic pipe does not need a plastic pipe for R2. Closed-cell foam plugs above and below the capsule stop air in the pipe from carrying heat down.
- **Unburied, the sensor would fail.** At the surface the same sensor would show 0.100 degrees per day and 0.0131 degrees per hour [B4], above the precaution threshold every sunny day. The TRL 2 figures stand.
- **R2 is met on paper.** It rests on the handbook soil values and on a steady-state pipe model; rain soaking into warm ground can change soil temperature faster than a daily sine wave, which only site data can show.

## C. Crack gauge (R3)

- **Resolution.** A 12-bit reading of the 100 mm stroke steps by 0.0244 mm; the 0.1 % linearity class gives 0.10 mm of absolute error [C1]. The rate of opening, which drives the alerts, depends on repeatability rather than linearity. **R3 is met by design** (datasheet class); re-setting after 100 mm needs only a spanner on the rod clamp.
- **Thermal swing.** The 580 mm steel rod and 260 mm aluminum body under the guard change length by 0.39 mm over a 30 K day, a peak apparent rate of 0.051 mm per hour [C2]. Over a 3 h window that reads as up to 1.22 mm per day, above the 1 mm per day precaution placeholder; over a 24 h window it cancels [C3]. The crack-gauge precaution rate is therefore taken over 24 h. The 1 mm per hour warning placeholder is 20 times the thermal rate, and at that rate the stroke lasts 100 h [C4].
- **Reader.** The gauge sits about 60 m of cable from the node, too far for a clean analog signal on a cable shared with the RS-485 bus. It gets the capsule's board without the inclinometer, in a small IP67 box (BOM line 4, +$6).

## D. Sampling, airtime and alert latency (R4, R5, R6)

- **Airtime.** A 20-byte uplink takes 72 ms at SF7, 247 ms at SF9, 453 ms at SF10 and 1,810 ms at SF12 [D1]; the TRL 2 figures of 0.4 s and 1.5 s were low. Six uplinks an hour use 0.08 % of the time at SF10 and 0.30 % at SF12, within the 1 % EU868 limit [D2]. **R4 is met on paper.**
- **Fair use.** On a private TwinKit gateway only the duty cycle applies. On The Things Network, whose fair-use policy allows 30 s a day, hourly uplinks fit at SF9 and SF10 (5.9 s and 10.9 s) but not at SF12 (43.5 s), and 10 min uplinks in the precaution or warning state exceed it from SF10 upward (65.2 s at SF10) [D3]. An alert state is short, but a site that lives at SF12 on The Things Network exceeds fair use, so under SLW-DDR-002 such a site uses its own TwinKit gateway.
- **Local alarm.** From the start of the reading that confirms a warning to the siren takes 13.4 s: bus start-up, the 10 s average, polling four devices and the decision [D4]. **R5 is met by design** (60 s).
- **Remote alert.** Warning to SMS takes 95 to 97 s at the first try. If that uplink is lost, the duty-cycle wait before a retry is 45 s at SF10 and 179 s at SF12, giving 141 s (2.3 min) and 278 s (4.6 min) [D5]. **R6 is at risk**: met on paper where coverage exists, with little margin at SF12. A site without LoRaWAN coverage needs a gateway (TwinKit, about $290 in parts) or gets no remote alert.

## E. Alarm reach (R7)

- **Open ground.** The siren gives 65.5 to 68.5 dB(A) at 100 m [E1] and reaches 65 dB(A) out to about 105 to 139 m [E2]. **R7 is at risk**: met in open, quiet ground with 0.5 dB to spare over soft ground, before any allowance for a siren that falls short of its rating or for wind.
- **Near machinery.** Against 80 dB(A) of running plant, an alarm 15 dB above ambient reaches only about 5 m [E3]. Sites with machinery need a second alert unit at the work face or a radio pager for operators (D7 option).
- **Close range.** A switch box on the mast, as in v0.1, would sit at about 105 dB(A), and 2 m from the mast the level is about 102 dB(A); at 105 dB(A) the NIOSH limit allows about 4 min [E4]. Under SLW-DDR-002 the keyed switch stands on its own post about 5 m from the mast, on a 7 m lead, where the level is 95.5 dB(A) and the NIOSH allowance about 43 min [E5]. Silencing takes seconds; people should still not stand at the mast during an alarm.

## F. Energy and rail current (R8)

- **Sensor load.** The bus draws 1.44 J per reading, 2.67 mW average from the cell, or 0.064 Wh per day [F1]. The TRL 2 figure of under 1 mW assumed 2 s of power per reading; the 10 s average raises it, still far below the FieldNode 100 mW sensor allowance.
- **Uplinks.** Hourly uplinks sit inside the FieldNode core budget, which assumes a 15 min report. Uplinks every 10 min at SF12 add 10.8 mWh per day [F2].
- **Alarm.** The siren and beacon take 5.4 W at 12 V, 6.0 W from the cell: 3.00 Wh for a 30 min alarm, plus 0.67 Wh for a 30 min silenced period with the beacon flashing at 50 % [F3].
- **Precaution beacon.** A slow flash at 5 % duty would cost 3.20 Wh per day; at 1 % it costs 0.64 Wh per day [F4]. Five sunless days in precaution with one alarm need 20.06 Wh at 5 % duty, more than the 13.06 Wh the cell holds at -10 °C, but 7.26 Wh (56 %) at 1 % duty [F5], [F7]. The beacon's slow flash is therefore limited to 1 % duty (for example 100 ms every 10 s). In the normal state the same five days with one alarm need 4.01 Wh [F6]. The average load in precaution is 29.8 mW, within the FieldNode 100 mW allowance [F8].
- **Rail current.** The alarm draws 0.45 A from the 12 V rail and 2.00 A from the cell at 3.0 V (0.33 C, within the 5 A cell fuse) [F9]. FieldNode does not state the 12 V rail's current rating. **R8 is met on energy and at risk on the rail current** until FieldNode specifies at least 0.5 A continuous on its 12 V rail. Under SLW-DDR-002 that request goes to FieldNode (a cross-repo action), rather than giving the alert unit its own battery.

## G. Sensor bus cable (R4, R9)

- **Length.** The reference layout needs 53.8 m of cable, 59.2 m with 10 % slack, within the 60 m in the BOM [G1].
- **Voltage drop.** The 0.5 mm² loop measures 4.07 Ω; with all 23.5 mA drawn at the far end it drops 0.096 V of the 5 V rail, leaving 1.30 V above the capsule regulators' need [G2]. The bus uses the FieldNode 5 V port rather than 12 V, because the capsules' linear regulators would waste more than half the power at 12 V. RS-485 over 59 m is far inside its 1,200 m class limit [G3].
- **Ports.** The bus (5 V, ground, A, B) takes one FieldNode M12 5-pin port. The alert unit takes the other: 12 V, ground, siren drive, beacon drive and the silence switch, which fits FieldNode's one-rail-per-port rule (FND-DDR-001). The FieldNode pinout itself is still open (FND-DDR-001, O2).

## H. Mast in wind

- **Loads.** The mast is a site option (SLW-DDR-002); where it is used, a 35 m/s gust puts 51 N on the panel, 29 N on the node enclosure, 48 N on the siren, horn and beacon and 136 N on the mast: 264 N and a base moment of 541 N·m [H1]. The switch box is no longer on the mast.
- **Mast.** The 48.3 x 3.2 mm pipe sees 113 MPa, a factor of 2.1 on the 235 MPa yield [H2], and deflects 62 mm at the top [H3]. The alert unit on the mast adds about 40 % to the base moment of a node alone. An existing pole must carry the same loads; the installer checks it by eye and with the site owner.
- **Footing.** The 320 mm by 600 mm footing resists 704 N sideways in medium soil, a factor of 2.7 [H4]. Soft or wet ground needs a site check. This is not a code check.

## I. Installing one stake (R10)

- **Materials.** Each hole is 110 mm by 820 mm (7.8 L of spoil); the grout column takes 3.64 L, about 7.3 kg of dry mix [I1].
- **Time.** Augering (15 min), mixing (5 min), setting and grouting (5 min), backfilling (8 min), fitting the capsule and head (7 min) and checking the reading (3 min) add up to 43 min against the 45 min of R10 [I2]. The grout then sets for 24 h before the baseline starts [I3]. **R10 is not verifiable at TRL 3**: the estimate is at the limit and the auger rate depends on the ground; only a timed installation can show it.

## J. Data (R12)

A 28-byte record per reading gives 363 kB for 90 days in binary, or 1.04 MB as CSV, against the 16 MB FieldNode flash [J1]. **R12 is met on paper.**

## K. Cost (R11)

The BOM has 10 lines, all priced, totaling $395.00 with the FieldNode core and the optional mast [K1]. Under SLW-DDR-001 D1 the FieldNode core ($126) is costed in FieldNode, and under SLW-DDR-002 the reference site mounts the node on an existing pole, so the $250 `budget_usd` covers the SlopeWatch-specific parts without the mast: $245.00, $5.00 (2.0 %) within budget [K2]. A site that needs the mast and footing (line 8, $24) comes to $269.00, $19.00 over; the reference site with the FieldNode core comes to $371.00 [K3]. The three stake sets cost $123.00, $41.00 per extra stake plus about 10 m of cable [K4]. The TRL 3 changes added $6 for the crack-gauge reader and $1 for foam plugs; SLW-DDR-002 added $8 for the switch post and lead (line 7, $25 to $33). **R11 is met on paper** for the reference site. A LoRaWAN gateway, where needed, is outside the site cost.

## L. Results against every requirement

*Table 3. Requirement status from this note [L]. At-risk items first; none is unmet.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R6 | Remote alert | 1.6 min at the first try; 4.6 min worst at SF12 with one lost uplink | 5 min, where coverage exists | **At risk** |
| R7 | Alarm audible | 65.5 to 68.5 dB(A) at 100 m in open ground; about 5 m near running plant | 65 dB(A) at 100 m | **At risk** |
| R8 | Energy autonomy | 7.3 Wh of 13.1 Wh in the worst case; 0.45 A on a 12 V rail with no stated rating | 5 days, one 30 min alarm | **At risk** (rail current) |
| R9 | Survive burial and weather | Capsule, head and gland IP67 by parts; FieldNode interior above 60 °C in 45 °C sun (FND-CAL-001) | IP67 at 0.4 m; node IP65; -10 to 50 °C | **At risk** |
| R1 | Measure surface tilt | 0.0055 degree step, 0.00054 degree noise, ±90 degrees in mode 1 | 0.01 degrees, ±30 degrees | Met on paper |
| R2 | Limit false tilt from temperature | 0.0092 degrees per day, 0.0012 degrees per hour (wet soil, 0.4 m) | 0.02 per day, 0.002 per hour | Met on paper |
| R4 | Sample and report | 10 min readings; 10.9 s per hour at SF12 | 10 min; 60 and 10 min uplinks | Met on paper |
| R12 | Open, local data | 363 kB for 90 days | 90 days, CSV, any server | Met on paper |
| R11 | Affordable | $245 for the reference site (existing pole); $269 with the optional mast | $250, SlopeWatch-specific parts, reference site | Met on paper |
| R3 | Measure crack opening | 100 mm stroke, 0.024 mm step, 0.10 mm linearity | 100 mm, 0.1 mm | Met by design |
| R5 | Local alarm without a network | 13 s | 60 s | Met by design |
| R10 | Installable by a small team | 43 min estimate | 45 min, hand tools | Not verifiable at TRL 3 |
| R13 | Trustworthy alarms | Needs a field record | One false warning per year or fewer | Not verifiable at TRL 3 |

Counts: 0 not met, 4 at risk, 5 met on paper, 2 met by design, 2 not verifiable at TRL 3. In v0.1, R11 was not met ($261 with a new mast).

## Checks against the TRL 2 figures

| TRL 2 claim (SLW-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| 0.005 degree sensitivity | 0.0055 degree output step; mode 1 needed for ±30 degrees | Precis updated |
| Capsule 0.3 m deep meets R2, thin margin | Misses R2 in wet soil; 0.4 m meets it | Capsule moved to 0.4 m |
| Pipe conduction not included | Adds 0.05 to 0.82 K at 0.4 m | Precis updated |
| Airtime about 0.4 s (SF10), 1.5 s (SF12) | 0.453 s and 1.810 s | Precis updated |
| Sensor load under 1 mW | 2.67 mW with a 10 s average | Precis updated |
| 30 min alarm about 3.2 Wh, about 2 A | 3.00 Wh, 2.00 A | Precis updated |
| Beacon duty not set | 1 % needed in precaution | Precis updated |
| Siren about 65 to 70 dB(A) at 100 m | 65.5 to 68.5 dB(A) | Stands |
| Bus drop about 0.1 V | 0.096 V | Stands |
| About 3 kB per day | 363 kB for 90 days (about 4 kB per day) | Stands |
| About $254 without FieldNode, $380 with | $261 and $387 in v0.1; $245 and $371 for the reference site in v0.2 (SLW-DDR-002) | Precis, BOM notes and README updated |
| TwinKit gateway about $285 | About $290 (TwinKit TRL 3 BOM) | Updated |
