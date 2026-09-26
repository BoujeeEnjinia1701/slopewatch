---
doc_id: SLW-PRB-001
title: SlopeWatch problem statement
project: SlopeWatch
doc_type: Problem statement
version: "0.4"
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
  change: Populate to TRL 2 (users, context, constraints, scope limits, cited prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Reflect SLW-DDR-001 (budget covers SlopeWatch-specific parts; tailings dams kept with limits); open questions updated
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# SlopeWatch problem statement

Many slope failures at mines and on hillsides are preceded by hours to months of slow, accelerating movement, but the people most exposed (workers at small mines and communities below waste dumps and steep slopes) rarely have any instrument that would show it. SlopeWatch aims to give them a low-cost, open network of tilt and crack sensors that measures the rate of movement and sounds a local alarm when it accelerates. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## The problem

Landslides are a large and growing cause of death. A global database of non-seismic fatal landslides recorded 4,862 events that killed 55,997 people from 2004 to 2016, 75 % of them in Asia, and found that landslides triggered by human activity, in particular construction, illegal mining and hill cutting, are increasing ([Froude and Petley, 2018](https://nhess.copernicus.org/articles/18/2161/2018/)). Mining adds its own hazards: tailings dams, waste dumps and pit walls. The failure of the Fundão tailings dam at Mariana, Brazil, in 2015 killed 19 people ([UK House of Commons Library](https://commonslibrary.parliament.uk/research-briefings/cdp-2023-0133/)), and the collapse at Brumadinho in 2019 killed 270 and released 9.7 million m³ of tailings ([Zhu, Zhang and Puzrin, 2024](https://www.nature.com/articles/s43247-023-01086-9)).

Many of these failures give warning through movement that speeds up before collapse. Satellite radar analysis of the 2020 Hpakant jade mine disaster in Myanmar, which killed at least 172 miners, found accelerated motion in the half year before the failure ([Hpakant multi-sensor study, 2021](https://www.sciencedirect.com/science/article/pii/S0924271621001489)). Plotting the inverse of surface velocity against time has been used since the 1980s to forecast the time of slope failure ([Fukuzono, 1985](https://www.jstage.jst.go.jp/article/jls1964/22/2/22_2_8/_article)).

Three gaps keep this knowledge from protecting people at small sites:

1. **Cost and skill.** Slope radar, robotic total stations and in-place inclinometer strings are designed for large operations with geotechnical staff. An estimated 44 million people work in artisanal and small-scale mining in 80 countries ([World Bank, 2021](https://www.worldbank.org/en/news/press-release/2021/05/03/better-working-conditions-can-improve-safety-and-productivity-of-artisanal-and-small-scale-miners-around-the-world)), and almost none of their pits, dumps or nearby hillsides are instrumented.
2. **No local alarm.** Where low-cost sensors are used, data often goes to a remote server that a site worker never sees. People on or below the slope need a siren and a light that work even when the network is down.
3. **Rate, not position.** A single survey of position says little. What matters is whether movement is steady, slowing or accelerating, which needs frequent, automatic readings and a simple rule that turns them into a warning.

Not every failure gives useful warning. The Brumadinho dam showed only about 30 mm of surface displacement in the year before a brittle failure, despite being fully instrumented ([Zhu, Zhang and Puzrin, 2024](https://www.nature.com/articles/s43247-023-01086-9)). SlopeWatch targets slopes that move progressively, and must say plainly that it cannot warn of every failure mode.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Small-scale or artisanal mine operator | Know when a pit wall, bench or waste dump is starting to move, and clear people from it in time | Open pits and dumps, often informal; little or no geotechnical support; workers below the slope all day |
| Mine or quarry site manager at a medium site | A low-cost first layer of monitoring on dumps and benches not covered by the main system | Some engineering staff; mobile coverage variable |
| Community below a slope or dump | A siren and light they trust, and a named person who receives alerts | Villages below waste dumps, road cuts or landslide-prone hillsides |
| Local government or civil protection officer | Readings they can act on, and a record of what happened | District disaster office, often with one staff member for a large area |
| Geotechnical engineer or university partner | Raw, time-stamped data in an open format to interpret movement and set thresholds | Visits occasionally; works remotely |

### Operating environment

- **Ground:** residual soil, weathered rock, loose dump material or compacted fill; slopes of about 15 to 45 degrees; stakes installed in the upper 1 m.
- **Climate:** ambient -10 to 50 °C at the surface in sun; heavy monsoon or tropical rain (the main trigger for most landslides); dust in the dry season.
- **Power and data:** no mains on the slope; mobile coverage patchy; a LoRaWAN gateway may be several kilometers away or absent.
- **People:** installers are site workers or community volunteers trained by a partner, working with hand tools on slopes that may already be moving.

## Constraints

- Garage-buildable prototype: the SlopeWatch-specific parts of one site within about $250 USD, with the FieldNode core costed in its own project (SLW-DDR-001 D1, decided by Amish on 2026-09-25, SLW-DDR-002). The reference site mounts the node on an existing pole, with a new mast as a site option; SLW-CAL-001 v0.2 puts the parts at $245, or $269 with the mast.
- Built on the lab's shared FieldNode power and radio core for power, logging and LoRaWAN, so SlopeWatch designs only its sensors, alert unit and rules.
- Installed and serviced by two trained people with hand tools; no drilling rig.
- A local alarm that does not depend on the network; remote alerts in addition, not instead.
- Open data format and any LoRaWAN server (for example the lab's TwinKit gateway or The Things Network).
- Must not be presented as a substitute for engineered monitoring. On tailings dams it may be installed only with the permission of the owner and the engineer of record, as a supplementary layer under the site's surveillance plan.

## Out of scope

- Detecting brittle failures, static liquefaction or internal erosion inside a tailings dam; these need piezometers, seepage monitoring and engineering review.
- Deep-seated movement below about 1 m (needs borehole inclinometers).
- Rainfall-only early warning (can be added later with a FieldNode rain gauge).
- Designing slope stabilization, drainage or evacuation plans; SlopeWatch informs them.
- The FieldNode core and the LoRaWAN gateway themselves (covered by FieldNode and TwinKit).

## Prior work

- **Low-cost MEMS tilt sensors on slopes.** Uchimura and colleagues placed MEMS tilt sensors in the surface layer of slopes in Japan and China and proposed tilt-rate thresholds of 0.01 degrees per hour for precaution and 0.1 degrees per hour for warning ([Uchimura et al., 2015](https://www.sciencedirect.com/science/article/pii/S0038080615001122)). SlopeWatch adopts this surface-tilt approach.
- **Wireless landslide networks.** Amrita University's wireless sensor network, with tiltmeters, inclinometers, pore pressure and moisture sensors, delivered real-time warnings in the Munnar district of Kerala in 2009 that led to evacuation alerts ([Amrita](https://www.amrita.edu/center/awna/landslide/)).
- **Inverse-velocity forecasting.** The Fukuzono method remains the common first tool to estimate time to failure from accelerating displacement ([Fukuzono, 1985](https://www.jstage.jst.go.jp/article/jls1964/22/2/22_2_8/_article)).
- **Satellite radar (InSAR).** InSAR can reveal slow precursory movement over wide areas, as at Hpakant, but revisit times of days and processing delays make it a planning tool rather than a local alarm.
- **Tailings governance.** The Global Industry Standard on Tailings Management (2020) sets 77 auditable requirements covering design, monitoring and emergency response ([UNEP](https://www.unep.org/news-and-stories/press-release/new-global-industry-standard-tailings-management-aims-improve-safety)); the Global Tailings Portal lists more than 1,800 facilities disclosed by about 100 companies ([GRID-Arendal](https://tailing.grida.no/about)). Small and informal operators are largely outside both.

## Open questions

- Which partner and which first site type: an artisanal gold mining cooperative, a quarry, or a hillside community with a district disaster office? Proposed, awaiting Amish (SLW-DDR-001 O2).
- Tailings dams stay in the pitch with the scope limits above (SLW-DDR-001 D2; decided by Amish, 2026-09-25: go with recommendation, SLW-DDR-002).
- Who receives alerts and who is allowed to sound or silence the siren? This is a community decision, to be settled in co-design.
- What stake spacing and how many stakes per site are needed on typical small-mine benches and dumps?
- Is there LoRaWAN coverage at candidate sites, or does each site need its own gateway?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
