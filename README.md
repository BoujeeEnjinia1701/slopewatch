# SlopeWatch

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mining · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $250 USD · **Difficulty:** 3 of 5

A network of low-cost tilt and displacement sensors for waste dumps, tailings dams, pit walls and landslide-prone slopes, reporting through FieldNode and alerting when movement accelerates.

![SlopeWatch concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement SLW-DWG-001 (PDF)](cad/drawings/SLW-DWG-001.pdf) · [Calculations SLW-CAL-001](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Many slopes speed up before they fail, and the rate of movement, not a single position, is what tells people to leave. SlopeWatch measures that rate with MEMS tilt sensors buried in grouted stakes and a crack gauge at the crest, following a published surface-tilt method with precaution and warning thresholds of 0.01 and 0.1 degrees per hour ([Uchimura et al., 2015](https://www.sciencedirect.com/science/article/pii/S0038080615001122)). All sensors share one FieldNode power and radio core, and the siren and beacon on site are driven by that node directly, so the alarm still works when the network does not.

It is open and garage-buildable because the sites that most need monitoring, small mines, quarries and hillside villages, cannot buy slope radar or pay for geotechnical staff. The stakes are steel pipe and hand-mixed grout, the electronics are off the shelf, and the data format and alert rules are open, so a local partner can build, repair and audit the system and an engineer can check every reading.

## Burning platform

Landslides killed 55,997 people in 4,862 non-seismic events from 2004 to 2016, and slides triggered by human activity, including illegal mining and hill cutting, are increasing ([Froude and Petley, 2018](https://nhess.copernicus.org/articles/18/2161/2018/)). Mining failures add to the toll: the Brumadinho tailings dam collapse in Brazil killed 270 people in 2019 ([Zhu, Zhang and Puzrin, 2024](https://www.nature.com/articles/s43247-023-01086-9)), and the 2020 slope failure at the Hpakant jade mines in Myanmar killed at least 172 miners after about half a year of accelerating movement visible from satellite ([Hpakant multi-sensor study, 2021](https://www.sciencedirect.com/science/article/pii/S0924271621001489)).

The people most exposed have the least monitoring. An estimated 44 million people work in artisanal and small-scale mining across 80 countries ([World Bank, 2021](https://www.worldbank.org/en/news/press-release/2021/05/03/better-working-conditions-can-improve-safety-and-productivity-of-artisanal-and-small-scale-miners-around-the-world)), mostly without any instrument on the pit walls and dumps above them. Not every failure gives surface warning (Brumadinho moved only about 30 mm in its final year), so SlopeWatch is a first layer for slopes that move progressively, not a guarantee.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Artisanal and small-scale mining | Tilt stakes on pit walls and benches above working areas, with a siren where people dig |
| Quarrying and aggregates | Monitoring benches, stockpiles and overburden dumps at sites with no geotechnical system |
| Mine waste management | Waste rock dumps and, with the owner's and engineer of record's permission, a supplementary layer on tailings embankments |
| Roads and railways | Cut slopes above roads in hill districts, alerting maintenance crews after heavy rain |
| Disaster risk management | Community landslide early warning run by a district disaster office or village committee |
| Research and education | An open, repeatable field instrument for university geotechnical projects and threshold studies |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| Brazil | The Fundão (2015, 19 deaths) and Brumadinho (2019, 270 deaths) tailings failures ([UK House of Commons Library](https://commonslibrary.parliament.uk/research-briefings/cdp-2023-0133/); [Zhu, Zhang and Puzrin, 2024](https://www.nature.com/articles/s43247-023-01086-9)) drove new rules for large dams; small mines and dumps remain largely unmonitored. |
| Myanmar | The 2020 Hpakant jade mine failure killed at least 172 miners after months of accelerating movement ([Hpakant multi-sensor study, 2021](https://www.sciencedirect.com/science/article/pii/S0924271621001489)); informal mining continues on waste slopes. |
| Ghana | Informal (galamsey) pits collapse regularly; on 3 September 2026 a pit collapse in the Ashanti Region killed seven miners ([Ghana News Agency](https://gna.org.gh/2026/09/seven-dead-one-trapped-after-galamsey-pit-collapses/)). |
| India | Asia accounts for 75 % of fatal landslides ([Froude and Petley, 2018](https://nhess.copernicus.org/articles/18/2161/2018/)); a university wireless sensor network in Munnar, Kerala, delivered real-time warnings that led to evacuation alerts ([Amrita](https://www.amrita.edu/center/awna/landslide/)), showing that local networks can work. |
| Italy | The national inventory lists more than 620,000 landslides ([ISPRA IFFI](https://www.progettoiffi.isprambiente.it/en/inventory/)); low-cost stakes suit the many small slopes that official networks cannot cover. |
| Japan | The surface-tilt method and thresholds SlopeWatch adopts were developed on slopes in Japan and China ([Uchimura et al., 2015](https://www.sciencedirect.com/science/article/pii/S0038080615001122)), giving a high-income reference for validation. |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. Geotechnical safety is the third mining gap, and the same hardware serves hillside communities. In the same month, a pit collapse at an informal gold mine in Ghana's Ashanti Region killed seven miners ([Ghana News Agency, 2026](https://gna.org.gh/2026/09/seven-dead-one-trapped-after-galamsey-pit-collapses/)), a reminder that the smallest sites carry the least protection.

## Problem

Slope and tailings failures often give warning through slow movement, but monitoring is costly and many small mines and hillside communities have none.

## Concept

A network of low-cost tilt and displacement sensors for waste dumps, tailings dams, pit walls and landslide-prone slopes, reporting through FieldNode and alerting when movement accelerates.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Three tilt stakes: 48.3 mm steel pipe grouted 0.8 m into the slope, each with a sealed MEMS inclinometer capsule 0.4 m below ground
- Crack displacement gauge (100 mm range) with its own bus reader, across a tension crack at the crest
- RS-485 sensor bus cable in conduit
- FieldNode power and radio core (shared lab component) on a mast at the toe
- Siren and beacon alert unit driven by the node, with a keyed silence switch
- Gateway and alert software: any LoRaWAN server, SMS alerts and an inverse-velocity plot

Checked by calculation at TRL 3 ([SLW-CAL-001](docs/04-calcs/01-sizing.md)): readings every 10 min; the siren starts about 13 s after a confirmed warning with no network; temperature drift of a buried capsule stays within 0.0012 degrees per hour, about eight times below the precaution threshold; five sunless days in the precaution state with one alarm use about 7.3 Wh of the FieldNode cell's 13.1 Wh at -10 °C. The SlopeWatch-specific parts cost $261 per site with a new mast, $11 over the $250 budget, and $237 on an existing pole; the FieldNode core ($126) is costed in its own project. Siren reach near machinery, the FieldNode 12 V rail current and the remote alert time at the slowest radio setting are at risk. See the [design precis](docs/02-concept.md) and [requirements](docs/03-requirements.md), including the requirement not met.

The priced bill of materials is in [bom/bom.csv](bom/bom.csv); the parametric model is `cad/src/model.py`, with STEP and STL files in `cad/step/` and `cad/stl/`.

## Safety

> Installing sensors on unstable ground is hazardous. Only trained teams should work on slopes, never below an actively moving face, and never on a tailings dam without the owner's permit and the engineer of record's agreement. The system is a research prototype that does not replace engineered monitoring: a silent siren is not proof of a safe slope, and some failures give no surface warning.
>
> The FieldNode core holds a LiFePO4 cell: use its fuse and cold-charge lockout. Wet cement grout burns skin and eyes; wear gloves and eye protection. Bond the mast to an earth rod and keep clear of overhead power lines.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (SLW-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `SLW-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Gap-filling areas set.
