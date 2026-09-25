# SlopeWatch

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mining · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $250 USD · **Difficulty:** 3 of 5

A network of low-cost tilt and displacement sensors for waste dumps, tailings dams, pit walls and landslide-prone slopes, reporting through FieldNode and alerting when movement accelerates.

## Concept rationale

Measuring movement rate, not just position, gives the hours to days of warning that let people move out of the way.

## Burning platform

Tailings dam and landslide disasters have killed hundreds of people in recent years, and monitoring is weakest at small sites.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. Geotechnical safety is the third mining gap, and the same hardware serves hillside communities.

## Problem

Slope and tailings failures give warning through slow movement, but monitoring is costly and many small mines and hillside communities have none.

## Concept

A network of low-cost tilt and displacement sensors for waste dumps, tailings dams, pit walls and landslide-prone slopes, reporting through FieldNode and alerting when movement accelerates.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- MEMS inclinometer in grouted stake
- Crack displacement gauge
- FieldNode power and radio core
- Siren and light alert unit
- Gateway and alert software

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Installing sensors on unstable ground is hazardous. Only trained teams should work on slopes, and the system is a research prototype that does not replace engineered monitoring.

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
