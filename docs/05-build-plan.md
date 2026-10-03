---
doc_id: SLW-BLD-001
title: SlopeWatch prototype build plan
project: SlopeWatch
doc_type: Build plan
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan from the template, with pictures by component and step; design made constructable (SLW-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Decisions of 2026-10-02 carried in: stake head marking, mast conditions in stop S5, logging only until thresholds are set in stop S7"
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Decisions carried into the pictures and text: wall holes in the alert unit back plate, the 60.3 mm site mast, the port pin assignment and rail voltages, stake head marking and its pictures; cost figures from SLW-CAL-001 v0.4"
---

# SlopeWatch prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component of one site kit pulled apart and numbered in build order. One of the three tilt stakes is shown; the mast and the switch post are drawn shortened.*

The prototype is one site kit for a slope: three tilt stakes grouted into the slope, each holding a sealed tilt sensor capsule 0.4 m below ground; a crack gauge across a tension crack at the crest; one cable in conduit joining them to a FieldNode core on a pole at the toe; a siren and beacon alert unit clamped to the same pole; and a keyed silence switch on its own post about 5 m away. Figure 1 shows the 20 components in the order you make or fit them, and Figure 2 shows where each goes on the slope. The made parts are cut and drilled steel pipe and bar, a printed collar, potted capsules, stake heads assembled from stock drainage fittings, a machined aluminium clamp block, a folded steel guard and three flat plates; the boxes are bought and drilled, and the FieldNode core is built to its own plan. The work is sawing, drilling, tapping and filing steel and aluminium, one 3D print, potting electronics, augering and grouting, and wiring at screw and lever terminals. The SlopeWatch parts cost about $304 for the reference site, from the bill of materials.

![Figure 2. Reference site layout](05-build-plan/site.png)

*Figure 2. Where each part goes on the reference site, along the fall line.*

> **Safety:** Installing on a slope that may already be moving is the main hazard. Work only with a trained team after a competent person has looked at the slope, never below an actively moving face or overhanging material, never on a tailings dam without the owner's permit and the engineer of record's agreement, and stop in or after heavy rain. Wet cement grout burns skin and eyes: wear gloves and eye protection. The siren gives about 110 dB(A) at 1 m: wear hearing protection when testing it. The FieldNode core holds a lithium iron phosphate cell: follow the safety stops in its own build plan. A silent siren is not proof of a safe slope.

## 2. What changed to make it buildable

The concept showed what SlopeWatch does; several of its parts could not be made or fixed as drawn. Each change below keeps what the system does, and all of them are recorded in decision record SLW-DDR-003, accepted by Amish on 2026-10-02.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Sensor capsule | Loose in the pipe between two foam plugs, 4 mm from the wall | Two printed collars that hold it on the pipe axis, resting on a plastic stand tube that sets its depth (Figure 8) | The capsule must tilt with the pipe; the stand tube sets 0.4 m without measuring down a hole |
| Pipe bottom | An unspecified internal plug | A screwed iron end cap, with grout under it (Figure 4) | A stock fitting that keeps grout and water out |
| Stake head | A 120 mm cap on a ring that is not sold, with no fixing | A head made from stock 110 mm drainage fittings, sealed on a tape wrap and held by two screws (Figure 10) | Every part can be bought; the head cannot be lifted off |
| Bus at each stake | One cable gland | Two conduit fittings, bus in upslope and bus out downslope, joined inside the head (Figure 11) | The bus has to pass through every stake |
| Crack gauge fixings | Solid blocks round the pins, with nothing holding the sensor | Clamp blocks with set screws, ball joints and a coupled extension rod (Figures 14, 16, 17) | The crack can open, close or shear without bending the sensor |
| Crack gauge guard | Passed through the pins and floated above the ground | A folded channel on feet, pegged on its upslope half (Figure 19) | Clears the gauge; the crack can open under it |
| Reader box | Floated beside the gauge | Hangs under the guard web (Figure 19) | Protected and fixed |
| Alert unit | Stood loose on the open top of the mast | A box on a back plate clamped to the pole with V-blocks and band clamps, like the FieldNode core (Figures 23, 25) | Works on an existing pole as well as on the mast |
| Keyed switch | Floated beside its post | A back plate held to the post by two hose clips (Figure 28) | Fixed without drilling the post |
| Mast earth bond | No clamps | A rod clamp, a mast bonding clamp and a bond conductor (Figure 30) | The usual way to bond a mast |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Upslope" and "downslope" are along the fall line of the slope. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4. Make three of every stake part (sections 3.1 to 3.5), one for each stake.

### 3.1 Stake pipe with end cap (make 3)

![Figure 3. Making sketch of the stake pipe](../cad/drawings/SLW-DWG-101.png)

*Figure 3. Stake pipe making sketch (SLW-DWG-101).*

**What it is and what it is made from.** The steel tube that is grouted into the slope and tilts with it. Galvanized steel pipe 48.3 mm outside and 3.2 mm wall (1.5 in), 1,000 mm long, threaded at the bottom end, with a screwed 1.5 in malleable-iron end cap.

**How to make it.**

1. Have the merchant cut 1,000 mm of pipe and thread one end 1.5 in.
2. Screw the end cap onto the threaded end with thread sealant, hand tight plus a quarter turn with a pipe wrench.
3. File the top end square and deburr it inside and out.
4. Paint a ground mark round the pipe 200 mm below the top. The pipe goes into the ground up to this mark, 800 mm deep.
5. Touch up the cut galvanizing with zinc-rich paint.
6. Do not drill the head screw holes yet; they are drilled through the head at step 6 so they line up.

**How it fits the parts next to it.**

![Figure 4. Joint 1: the bottom of the stake, cut open](05-build-plan/joint-01.png)

*Figure 4. The end cap keeps grout and water out; 20 mm of grout runs under it, and the stand tube stands on the cap's floor inside.*

The pipe stands in a 110 mm hole augered 829 mm deep. Grout fills the hole from the bottom to 450 mm above the pipe's bottom end, round the cap and the pipe, and tamped soil fills the hole above the grout.

**Check before moving on.** Blow down the pipe with the cap on: no air comes out at the cap.

### 3.2 Stand tube (make 3)

![Figure 5. Making sketch of the stand tube](../cad/drawings/SLW-DWG-102.png)

*Figure 5. Stand tube making sketch (SLW-DWG-102).*

**What it is and what it is made from.** A plastic tube that stands inside the stake pipe and sets the depth of the capsule. PVC pressure pipe 40 mm outside, 2 mm wall, 335 mm long.

**How to make it.**

1. Measure and mark 335 mm; check the mark with a tape, since a 10 mm error moves the capsule 10 mm.
2. Cut square and deburr both ends.
3. Chamfer the outside edges by 1 mm so the tube slides down the pipe without catching.

**How it fits the parts next to it.** It drops down the pipe and stands on the end cap's floor, 1 mm clear of the bore all round. The capsule's lower collar sits on its top rim (Figure 8).

**Check before moving on.** 335 mm long, within 2 mm, and it slides freely down an offcut of the stake pipe.

### 3.3 Centring collars (make 6)

![Figure 6. Making sketch of the centring collar](../cad/drawings/SLW-DWG-103.png)

*Figure 6. Centring collar making sketch (SLW-DWG-103).*

**What it is and what it is made from.** A ring on each end of the capsule that holds it on the axis of the pipe, so the capsule tilts exactly as the pipe tilts. ASA plastic, 3D printed at 100 % infill, 41.5 mm outside, 34 mm inside and 15 mm long. Two per capsule.

**How to make it.**

1. Print one collar flat in ASA in an enclosed printer.
2. Try it: it must be a light press fit on the capsule tube and slide freely in an offcut of the stake pipe. If not, change the outside size in steps of 0.2 mm and print again.
3. Print the other five.

**How it fits the parts next to it.** One collar is glued flush with each end of the capsule with a drop of polyurethane adhesive. In the pipe there is 0.2 mm between the collar and the bore.

**Check before moving on.** On a capsule, both collars turn freely in the pipe offcut, and the capsule does not rock in it.

### 3.4 Sensor capsule (make 3)

![Figure 7. Making sketch of the sensor capsule](../cad/drawings/SLW-DWG-104.png)

*Figure 7. Sensor capsule making sketch (SLW-DWG-104).*

**What it is and what it is made from.** The sealed tilt sensor. A board carrying the inclinometer, a small microcontroller, an RS-485 transceiver and a 3.3 V regulator, potted in a polycarbonate tube 34 mm outside, 2 mm wall and 130 mm long, with a 0.8 m lead of four-core 0.25 mm² shielded cable out of the top centre.

**How to make it.**

1. Flash the board and read its tilt on the bench before potting it.
2. Mark the board's X axis with an arrow on a label on the tube. The arrow points downslope when the capsule is installed.
3. Glue a disc into the bottom of the tube.
4. Slide the board in on a printed carrier that holds it square to the tube, lead out of the top.
5. Fill the tube with polyurethane potting compound and cure it as its maker says.
6. Glue a centring collar flush on each end (section 3.3).

**How it fits the parts next to it.**

![Figure 8. Joint 2: the capsule in the pipe, cut open](05-build-plan/joint-02.png)

*Figure 8. The collars hold the capsule on the pipe axis; the lower collar rests on the stand tube; the foam plug sits 10 mm above the capsule with the lead through its slit.*

The capsule hangs on its lead as it goes down the pipe and comes to rest on the stand tube's rim, its centre 400 mm below ground. An 80 mm foam plug, slit for the lead, is pushed down to 10 mm above it.

**Check before moving on.** Laid on a level bench, the capsule reads within 0.1 degree of a spirit level in both directions.

### 3.5 Stake head (make 3)

![Figure 9. Making sketch of the stake head](../cad/drawings/SLW-DWG-105.png)

*Figure 9. Stake head making sketch (SLW-DWG-105).*

**What it is and what it is made from.** A rain-proof head on top of the stake, where the capsule's lead joins the bus. Stock 110 mm PVC drainage fittings: a 110 x 50 mm concentric reducer, 94 mm of 110 mm pipe and a 110 mm end cap, with two M20 conduit fittings for 20 mm corrugated conduit.

**How to make it.**

1. Cut the 110 mm pipe square to 94 mm and deburr it.
2. Drill two 20.5 mm holes opposite each other, centred 46 mm up from the pipe's lower end; check the hole size on the conduit fitting's datasheet first.
3. Push the pipe fully into the reducer's 110 mm socket and solvent-cement it.
4. Dry-fit the end cap; it is cemented after the bus is joined (step 7).
5. Paint the head signal amber with a retroreflective band, and fix a stake ID label and a downslope arrow on the crown, so the stake is seen and can be reported on.

**How it fits the parts next to it.**

![Figure 10. Joint 3: the head socket on the pipe, cut open](05-build-plan/joint-03.png)

*Figure 10. The 50 mm socket slides over a tape wrap on the top of the pipe; two screws go through the socket into the pipe wall.*

The reducer's 50 mm socket goes 40 mm over the top of the stake pipe. Three turns of self-amalgamating tape round the pipe take up the gap and seal it. Two M5 stainless self-tapping screws, one each side, go through the socket into 4.2 mm holes in the pipe wall, 20 mm above the socket's rim.

![Figure 11. Joint 4: the conduit fittings in the head](05-build-plan/joint-04.png)

*Figure 11. The bus comes in on the upslope side and goes out on the downslope side; each fitting's lock nut is inside the head.*

**Check before moving on.** The head stands 330 mm above the ground mark on a pipe offcut, and both fittings point along the same line.

### 3.6 Anchor pins (make 2)

![Figure 12. Making sketch of the anchor pin](../cad/drawings/SLW-DWG-106.png)

*Figure 12. Anchor pin making sketch (SLW-DWG-106).*

**What it is and what it is made from.** The two steel pins driven into the ground either side of the crack; each carries one end of the crack gauge. Mild steel round bar 20 mm, 700 mm long, galvanized or painted.

**How to make it.**

1. Cut 700 mm of bar.
2. Grind a point 30 mm long on one end, about 4 mm across the tip.
3. Chamfer the top edge by 2 mm so a sledge does not spread it.
4. Paint a ring 500 mm from the tip; the pin is driven to this ring, leaving 200 mm above ground.

**How it fits the parts next to it.** Driven upright 900 mm apart, one each side of the crack, on a line square to it. Each carries a clamp block (Figure 14).

**Check before moving on.** A level on the pin shows it upright within 2 degrees.

### 3.7 Clamp blocks (make 2)

![Figure 13. Making sketch of the clamp block](../cad/drawings/SLW-DWG-107.png)

*Figure 13. Clamp block making sketch (SLW-DWG-107).*

**What it is and what it is made from.** A block that slides onto an anchor pin and carries a ball joint for the gauge. Aluminium square bar 40 x 40 mm, 6082 class, 60 mm long. Both blocks are the same.

**How to make it.**

1. Saw 60 mm off the bar and file it square.
2. Drill a 20.5 mm hole right through the middle of the two 40 x 40 mm faces.
3. On one 40 x 60 mm side face, at mid-height and centred, drill 5.0 mm 12 deep and tap M6 10 deep for the ball-joint stud.
4. On the opposite side face, 45 mm up and centred, drill 6.8 mm through into the bore and tap M8 for the set screw.
5. Deburr all edges and the bore.

**How it fits the parts next to it.**

![Figure 14. Joint 5: the upslope clamp block, ball joint and sensor](05-build-plan/joint-05.png)

*Figure 14. The block slides onto the pin, the set screw bears on the pin, and the sensor hangs on the ball joint.*

Each block slides onto its pin with its stud face pointing at the other pin, and is set with its centre 110 mm above the ground. The M8 set screw on the outer face clamps it to the pin. The M6 stud of a rod-end ball joint screws 10 mm into the stud hole with medium threadlocker.

**Check before moving on.** The block slides on a 20 mm bar with no more than 0.5 mm of shake.

### 3.8 Extension rod

![Figure 15. Making sketch of the extension rod](../cad/drawings/SLW-DWG-108.png)

*Figure 15. Extension rod making sketch (SLW-DWG-108).*

**What it is and what it is made from.** The rod that carries the sensor's movement across the crack to the downslope pin. Stainless steel round bar 8 mm, 501 mm long, with an M6 stud in each end.

**How to make it.**

1. Cut 501 mm of bar, ends square.
2. Hold the bar upright in a V-block in a drill press, centre-drill each end, drill 5.0 mm 15 deep and tap M6.
3. Screw an M6 x 20 stud into each end with medium threadlocker, 10 mm in and 10 mm out.

**How it fits the parts next to it.**

![Figure 16. Joint 6: plunger to extension rod](05-build-plan/joint-06.png)

*Figure 16. A coupling nut joins the sensor's plunger to the rod.*

![Figure 17. Joint 7: the downslope clamp block and rod end](05-build-plan/joint-07.png)

*Figure 17. The rod's other end screws into the second ball joint, which sits on the downslope block's stud.*

Set the plunger 15 mm out of the sensor body before tightening the coupling, so the gauge can read 85 mm of opening and 15 mm of closing.

**Check before moving on.** 501 mm long within 1 mm, and straight within 1 mm when rolled on a flat bench.

### 3.9 Guard

![Figure 18. Making sketch of the guard](../cad/drawings/SLW-DWG-109.png)

*Figure 18. Guard making sketch (SLW-DWG-109).*

**What it is and what it is made from.** A cover over the crack gauge that keeps off sun, rain, animals and boots. Galvanized steel sheet 1.5 mm, folded to a channel 1,150 long, 200 wide and 250 high, with 25 mm feet.

**How to make it.**

1. Cut a blank 1,150 x 750 mm.
2. Mark fold lines along the 1,150 mm length at 25, 275, 475 and 725 mm from one edge.
3. Fold the two outer 25 mm strips outward (the feet) and the two 250 mm legs down. Have a sheet metal shop fold it, or fold it between two 1.2 m steel angles clamped to a bench.
4. Drill four 9 mm peg holes centred in the feet, 40 and 455 mm from the upslope end.
5. Drill two 4.5 mm holes in the web for the reader box, 100 and 150 mm from the upslope end and 52 mm to one side of the centre line.

**How it fits the parts next to it.**

![Figure 19. Joint 8: guard foot, peg and reader box at the upslope end](05-build-plan/joint-08.png)

*Figure 19. The guard stands on its feet 48 mm above the pin tops; pegs hold its upslope half; the reader box hangs under the web.*

Four 8 mm x 300 mm ground pegs go through the feet on the upslope half only, so the ground can open under the downslope half without the guard holding the crack together.

**Check before moving on.** The web is flat and the legs square to it within 3 mm.

### 3.10 Reader box

![Figure 20. Drilling sketch of the reader box](../cad/drawings/SLW-DWG-110.png)

*Figure 20. Reader box drilling sketch (SLW-DWG-110).*

**What it is and what it is made from.** A bought IP67 box, 80 x 60 x 45 mm, holding the reader board that turns the crack gauge's signal into a bus reading. The board is the capsule's board without the inclinometer.

**How to make it.**

1. In the base, drill two 4 mm holes 50 mm apart on the long centre line, to match the guard's web holes.
2. In the downslope end, drill one 20.5 mm hole, centred, for an M20 conduit fitting.
3. In the upslope end, drill one 12.5 mm hole for an M12 gland for the sensor lead.
4. Fit the reader board on its standoffs, and wire the sensor lead and the bus to it as Figure 31 shows.

**How it fits the parts next to it.** It hangs under the guard web at the upslope end, lid down, on two M4 screws with nylon sealing washers, 12 mm clear of the upslope pin (Figure 19). The bus conduit runs from its fitting along the ground inside the guard and out of the guard's open downslope end, with a 0.5 m slack loop.

**Check before moving on.** The lid gasket is seated and the box hangs level.

### 3.11 Alert unit back plate

![Figure 21. Making sketch of the alert unit back plate](../cad/drawings/SLW-DWG-111.png)

*Figure 21. Alert unit back plate making sketch (SLW-DWG-111).*

**What it is and what it is made from.** The plate the alert box is screwed to and that clamps to the pole. Aluminium sheet 3 mm, 5052 or 6061 class, 160 x 360 mm.

**How to make it.** Measure heights up from the bottom edge and sideways from the centre line.

1. Cut the blank, square, and round the corners to about 2 mm.
2. Band slots: four slots 6 wide and 15 tall, 60 each side of centre, centred 20 and 190 up. Chain drill with a 3 mm drill and file them square.
3. V-block screw holes: four 4.5 mm holes, 18 each side of centre, 20 and 190 up, countersunk from the front.
4. Alert box screw holes: four 5.5 mm holes, 45 each side of centre, 235 and 325 up.
5. Wall holes: four 6.5 mm holes, 70 each side of centre, 45 and 315 up (45 in from each end), for coach screws when the unit goes on a timber pole or a wall instead of a steel pole.
6. Deburr every hole on both faces.

**How it fits the parts next to it.** The V-blocks sit on its back, the alert box on the top part of its front. The two band clamps go round the pole and through the slots, below the box. On the mast, the top 110 mm of the plate stands above the mast top so the beacon clears it. On a timber pole or wall, leave off the V-blocks and bands and fix the plate with four M6 coach screws through the wall holes; the screw heads clear the alert box by 3 mm.

**Check before moving on.** Lay the V-blocks and the box on it and look through each hole: they line up without forcing a screw.

### 3.12 V-blocks (make 2)

![Figure 22. Making sketch of the V-block](../cad/drawings/SLW-DWG-112.png)

*Figure 22. V-block making sketch (SLW-DWG-112).*

**What it is and what it is made from.** A block with a V cut in it that the pole sits in, one at each band clamp. Aluminium flat bar 60 x 40 mm, 6082 or 6061 class. It is the same part as the FieldNode V-block.

**How to make it.**

1. Saw two 20 mm slices off the bar; saw and file each to 60 wide, 33 deep and 20 tall. The 60 x 20 mm face is the back face; file it flat.
2. On each 60 x 33 mm face, scribe the V with a 45 degree square: 50.3 mm wide at the front face, its point 7.8 mm from the back face.
3. Saw just inside both lines and file to them, keeping the V faces flat.
4. Break the sharp front edges of the V by 0.5 mm.
5. In the back face, 18 each side of centre and half way up, drill 3.3 mm 14 deep and tap M4 12 deep.

**How it fits the parts next to it.**

![Figure 23. Joint 9: V-block and band clamp, seen from above](05-build-plan/joint-09.png)

*Figure 23. The pole bears on both faces of the V; the band goes round the pole, through the plate's slots and across the plate front.*

Each block is held to the back of the plate by two M4 countersunk screws put in from the front with a drop of medium threadlocker. A 48.3 mm pole touches both faces of the V and never the bottom; poles of 40 to 70 mm also seat on both faces.

**Check before moving on.** Held against a 48 mm tube, the block does not rock.

### 3.13 Alert box

![Figure 24. Drilling sketch of the alert box](../cad/drawings/SLW-DWG-113.png)

*Figure 24. Alert box drilling sketch (SLW-DWG-113).*

**What it is and what it is made from.** A bought IP65 box, 120 wide, 90 deep and 120 tall, with four corner screw holes outside the lid seal. It holds the siren and beacon driver; the horn mounts on its front and the beacon on its top.

**How to make it.**

1. Tape the faces. Pilot drill every hole 3 mm slowly and open it with a step drill.
2. Bottom: two 16.2 mm holes 30 each side of centre for M16 glands, one for the lead to the node and one for the switch lead.
3. Top: one 10 mm hole, centred, for the beacon lead.
4. Front: one 10 mm hole, centred, for the horn leads.
5. Fit the driver inside on its standoffs. Fit the horn with its flange and gasket over the front hole and the beacon with its base gasket over the top hole, each with the screws its maker supplies.

**How it fits the parts next to it.**

![Figure 25. Joint 10: the alert box on its back plate](05-build-plan/joint-10.png)

*Figure 25. Seen from behind: four screws through the box's corner holes and the plate, nyloc nuts on the back of the plate beside the pole.*

**Check before moving on.** Every hole in the box is covered by a gland, a gasket or a flange.

### 3.14 Switch post

![Figure 26. Making sketch of the switch post](../cad/drawings/SLW-DWG-114.png)

*Figure 26. Switch post making sketch (SLW-DWG-114).*

**What it is and what it is made from.** The post that carries the keyed silence switch about 5 m from the siren, where the sound is about 95 dB(A) instead of about 106 dB(A) at the pole. Galvanized steel tube 26.9 x 2.6 mm (0.75 in), 1,900 mm long, with a push-on plastic cap.

**How to make it.**

1. Cut 1,900 mm of tube; cut the lower end at 45 degrees so it drives more easily, and file the top end square.
2. Paint a ground mark 500 mm from the lower tip.
3. Touch up the cut ends with zinc-rich paint and push the cap onto the top.

**How it fits the parts next to it.** Driven upright 500 mm into the ground, about 5 m from the pole on the side away from the horn. The switch back plate clamps to it with the box centre 1,300 mm above the ground (Figure 28).

**Check before moving on.** Upright within 2 degrees, and it does not move when pushed by hand.

### 3.15 Switch back plate

![Figure 27. Making sketch of the switch back plate](../cad/drawings/SLW-DWG-115.png)

*Figure 27. Switch back plate making sketch (SLW-DWG-115).*

**What it is and what it is made from.** The plate that holds the keyed switch box on its post. Galvanized steel sheet 3 mm, 100 x 160 mm.

**How to make it.** Measure heights up from the bottom edge and sideways from the centre line.

1. Cut the blank and round the corners.
2. Hose clip slots: four slots 6 wide and 15 tall, 26 each side of centre, centred 18 and 142 up; chain drill 3 mm and file square.
3. Box screw holes: four 4.5 mm holes, 40 each side of centre, 52 and 108 up; check them against your box's corner holes first.
4. Deburr and touch up with zinc-rich paint.

**How it fits the parts next to it.**

![Figure 28. Joint 11: the keyed switch box on its post](05-build-plan/joint-11.png)

*Figure 28. The plate bears on the post; two hose clips, above and below the box, hold it there.*

The switch box (a bought IP65 box, 100 x 60 x 70 mm, with the keyed switch on its front and an M16 gland underneath) is screwed to the plate through its corner holes with four M4 screws.

**Check before moving on.** With the clips tight, the plate does not turn on the post.

### 3.16 Mast (site option)

![Figure 29. Making sketch of the mast](../cad/drawings/SLW-DWG-116.png)

*Figure 29. Mast making sketch (SLW-DWG-116).*

**What it is and what it is made from.** Only where the site has no 40 to 70 mm pole for the FieldNode core and the alert unit. The prototype's mast is galvanized steel pipe 48.3 x 3.2 mm and stands on a fenced test slope only. A mast for a working site is the heavier 60.3 x 3.6 mm pipe, unless local gust data show winds well below 35 m/s (the 48.3 mm pipe has a factor of 1.7 on yield in a 35 m/s gust, the 60.3 mm pipe 2.9); the V-blocks and bands fit both. Pipe, 3,750 mm long, cast 550 mm into a concrete footing 320 mm across and 600 mm deep, with a push-on top cap, a 16 mm earth rod 1.2 m long and a bond.

**How to make it.**

1. Cut 3,750 mm of pipe; file both ends square and touch them up.
2. Paint a ground mark 550 mm from the lower end.
3. Push the cap onto the top end.

**How it fits the parts next to it.**

![Figure 30. Joint 12: the mast foot and earth bond](05-build-plan/joint-12.png)

*Figure 30. A bonding clamp round the mast just above the footing, a clamp on the earth rod 450 mm away, and a 16 mm² green and yellow conductor between them.*

The FieldNode core's bottom is 1,750 mm above the ground. The alert unit's back plate runs from 2,950 to 3,310 mm, with the siren's centre at about 3.2 m.

**Check before moving on.** Plumb within 1 degree once the concrete has set.

### 3.17 Bus and alert wiring

![Figure 31. Bus and alert wiring](05-build-plan/bus.png)

*Figure 31. Block-level wiring. One four-core cable chains the reader and the three stake heads to FieldNode port A; the alert box takes port B.*

The bus cable is four-core shielded outdoor cable, 0.5 mm², about 60 m in 20 mm corrugated conduit: red +5 V, black 0 V, blue RS-485 A and white RS-485 B, with the shield joined to 0 V at the node end only and a 120 ohm terminator across A and B at the node and at the reader. In each stake head, join bus in, bus out and the capsule lead colour to colour, one lever connector per core. The bus ends in a field-wired M12 5-pin plug with a surge protector at the node, on port A, the 5 V port: pin 1 +5 V (red), pin 2 RS-485 A (blue), pin 3 0 V (black), pin 4 RS-485 B (white). The alert box takes 12 V from port B, the 12 V port, on a 0.75 mm² lead with its own M12 plug, run down the pole in cable ties: pin 1 12 V, pin 3 0 V, pin 5 the keyed switch input, which joins it on a 7 m two-core lead in conduit; the alert unit leaves pins 2 and 4 of port B unused. Label each port on the node with its rail voltage, 5 V on port A and 12 V on port B, and label each plug with its port. Label every cable end with its stake or box.

**Check before moving on.** With nothing powered, every core reads continuous end to end and no core reads to any other core or to the shield.

### 3.18 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Inclinometer (line 2).** Murata SCL3300 class, run in its ±90 degree mode, on the capsule board.
- **Crack displacement sensor (line 4).** Linear potentiometer, 100 mm stroke, 0.1 % linearity class, 25 mm body or smaller, with an M6 rod-end ball joint at each end and a removable plunger-end joint; plus a spare M6 rod-end ball joint, two M6 studs, an M6 coupling nut and two M8 set screws.
- **Stake head parts (line 3).** 110 x 50 mm concentric drainage reducer whose 50 mm socket is 50 to 51 mm inside; 110 mm drainage pipe and end cap; two M20 IP66 conduit fittings for 20 mm corrugated conduit; three five-way lever connectors per head; two M5 x 16 stainless self-tapping screws per head; for the marking, signal amber paint, 25 mm retroreflective tape about 0.35 m per head, a printed UV-stable vinyl ID label and a vinyl arrow.
- **Bus cable and conduit (line 5).** 60 m of four-core shielded outdoor cable, 0.5 mm², UV and burial rated; 20 mm corrugated UV-rated conduit; conduit clips with ground pegs, one per metre.
- **FieldNode core (line 6).** Built and checked to the FieldNode build plan (FND-BLD-001); its two band clamps fit the pole used here.
- **Alert unit (line 7).** 12 V piezo siren of about 110 dB(A) at 1 m with a sealing flange; 12 V amber LED beacon of about 0.2 A with a gasketed base; two-channel MOSFET driver board; IP65 boxes 120 x 90 x 120 mm and 100 x 60 x 70 mm with corner holes outside the seal; keyed switch rated IP65; two 12 mm stainless band clamps for the pole; two 20 to 32 mm stainless hose clips for the switch post; two M16 glands and one more for the switch box.
- **Mast extras (line 8).** 48 mm push-on plastic pipe cap, 16 mm x 1.2 m earth rod with its clamp, a pipe bonding clamp and 16 mm² green and yellow conductor.
- **Consumables (line 10).** Thread sealant, self-amalgamating tape, polyurethane potting compound and adhesive, zinc-rich paint, medium threadlocker, closed-cell foam backer rod 40 mm for the plugs, cable ties, heat-shrink, dielectric grease, surge protector, marking tape, ground pegs 8 mm x 300 mm, about 25 kg of bagged cement grout for three stakes, and 0.1 m³ of concrete for the mast footing where the mast is used.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Steps 1 to 7 are repeated for each of the three stakes. Install the stakes from the top of the slope down, and never work below a stake team.

### Step 1: end cap onto the stake pipe

![Step 1](05-build-plan/step-01.png)

On the bench. Thread sealant on the thread; screw the cap on hand tight plus a quarter turn. Paint the ground mark 200 mm below the top.

### Step 2: set the pipe and pour the grout

![Step 2](05-build-plan/step-02.png)

Auger a 110 mm hole 829 mm deep, square to the slope surface measured with a level on a straight edge laid down the fall line. Mix the grout by hand to a pourable paste. Pour about 20 mm into the bottom, stand the pipe in the hole to its ground mark, hold it plumb with two props, and pour grout round it to 450 mm above its bottom end, rodding out the air. Fill the rest of the hole with soil tamped in layers. **Hold point:** leave the grout 24 h to set before step 3.

### Step 3: stand tube down the pipe

![Step 3](05-build-plan/step-03.png)

Drop the stand tube down the pipe; it stands on the cap's floor. Check with a marked rod that its top is 465 mm below the ground mark.

### Step 4: capsule down onto the stand tube

![Step 4](05-build-plan/step-04.png)

Turn the capsule so the arrow on its label points downslope, and lower it on its lead, without twisting it, until the lower collar rests on the stand tube.

### Step 5: foam plug above the capsule

![Step 5](05-build-plan/step-05.png)

Slit an 80 mm length of foam backer rod along its length, put the lead in the slit, and push the plug down the pipe with a rod until it is 10 mm above the capsule.

### Step 6: head onto the pipe

![Step 6](05-build-plan/step-06.png)

Wrap three turns of self-amalgamating tape round the top 30 mm of the pipe. Thread the capsule lead through the head and push the head's socket down over the tape until the pipe top meets the reducer. Turn the head so its fittings face upslope and downslope. Drill 4.2 mm through the socket into the pipe on each side, 20 mm above the socket's rim, and drive the two M5 screws.

### Step 7: conduit fittings and the bus

![Step 7](05-build-plan/step-07.png)

Fit the two conduit fittings through the head, lock nuts inside. Bring the bus conduit from upslope into the upslope fitting and on to the next stake from the downslope fitting. Join bus in, bus out and the capsule lead at the lever connectors (Figure 31), tuck them into the head, and cement the end cap on. **Hold point:** continuity check of section 3.17 passes for this stake.

### Step 8: drive the anchor pins

![Step 8](05-build-plan/step-08.png)

Mark a line square to the crack. Drive one pin 450 mm each side of the crack on that line, upright, to its painted ring, with a sledge and a driving cap.

### Step 9: clamp blocks onto the pins

![Step 9](05-build-plan/step-09.png)

Slide a block onto each pin with its stud face toward the other pin and its centre 110 mm above the ground; tighten the set screws. Screw a ball joint's stud into each block.

### Step 10: sensor and extension rod onto the studs

![Step 10](05-build-plan/step-10.png)

Set the plunger 15 mm out of the sensor body and tighten the coupling and rod onto it. Fit the sensor's upslope ball joint on the upslope stud, then the rod's ball joint on the downslope stud. Adjust the downslope block's height until the rod is level, then retighten its set screw.

### Step 11: reader box under the guard

![Step 11](05-build-plan/step-11.png)

On the bench, with the guard upside down: two M4 screws with nylon washers through the web into the box's base, lid facing away from the web.

### Step 12: guard over the gauge

![Step 12](05-build-plan/step-12.png)

Plug the sensor lead into the reader and connect the bus conduit to the reader's fitting. Lower the guard over the gauge onto its feet and drive four pegs through the upslope feet.

### Step 13: mast and earth rod (site option)

![Step 13](05-build-plan/step-13.png)

Only where there is no 40 to 70 mm pole. Dig the footing hole 320 mm across and 600 mm deep, 15 m beyond the toe. Pour 50 mm of concrete, stand the mast in it to its ground mark, fill with concrete, plumb it and brace it for 3 days. Drive the earth rod 450 mm away, leaving 50 mm above ground, and fit the clamps and bond. **Hold point:** safety stop S5.

### Step 14: FieldNode core onto the pole

![Step 14](05-build-plan/step-14.png)

Build and check the FieldNode core to its own plan, then clamp it to the pole with its V-blocks and band clamps, its bottom 1,750 mm above the ground, facing the same way as the horn will.

### Step 15: alert box onto its back plate

![Step 15](05-build-plan/step-15.png)

On the bench. Screw the V-blocks to the back of the plate. Screw the alert box to the front through its four corner holes with M5 screws, nyloc nuts on the back of the plate.

### Step 16: alert unit onto the pole

![Step 16](05-build-plan/step-16.png)

With a second person on a stable ladder, hold the unit with the pole in both V-blocks, the siren at least 3 m above the ground and the horn facing the work area. Pass each band round the pole and through its two slots, worm-drive housing behind the pole, and tighten. **Hold point:** safety stop S5.

### Step 17: drive the switch post

![Step 17](05-build-plan/step-17.png)

About 5 m from the pole, on the side away from the horn, with a post driver, to the ground mark.

### Step 18: switch box onto its post

![Step 18](05-build-plan/step-18.png)

Screw the switch box to its plate with four M4 screws. Hold the plate against the post with the box centre 1,300 mm above the ground and fit the two hose clips through the slots, above and below the box.

### Step 19: lay the bus and connect the node

![Step 19](05-build-plan/site.png)

Lay the bus conduit on the surface from the reader down through each stake to the pole, pegged every metre, with a slack loop at each stake and at the crack. Run the switch lead in its conduit from the switch post to the pole. Fit the surge protector and the M12 plugs. **Hold point:** safety stops S6 and S7 before port B is connected.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of SLW-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Capsule on the bench | R1 | Each capsule on a level bench, then on a 5 degree wedge, read through a USB to RS-485 adapter | Reads level within 0.1 degree; the wedge within 0.1 degree of 5 |
| Capsule centred in the pipe | R1 | Lower a capsule with its collars into a pipe offcut; tilt the offcut 1 degree | The capsule's reading follows the offcut within 0.05 degree |
| Seals | R9 | Look at every gland, fitting, gasket and tape wrap; hose water over a stake head for 5 min | No water inside the head or the boxes |
| Bus continuity | R4, R12 | Meter each core end to end before power | Every core continuous; no core to another core or to the shield |
| Readings every 10 min | R4 | Node powered; log for 1 h | Six readings from each of the three capsules and the gauge |
| Crack gauge range | R3 | Slide the downslope block 10 mm along a test bar, then back | Reading changes by 10 mm within 0.2 mm and returns |
| Local alarm without a network | R5 | Network off; force a warning in the test firmware | Siren and beacon start within 60 s |
| Keyed silence | R5 | Turn the key during a test alarm | Siren stops, beacon stays on, siren re-arms after 30 min |
| Alert rail current | R8 | Clamp meter on the port B lead during a 30 min test alarm | 0.45 A or less, and the node's 12 V rail stays within 5 % |
| Stake installation time | R10 | Time two people installing one stake, steps 2 to 7 | 45 min or less, plus the 24 h grout set |
| Siren level | R7 | Sound level meter at 100 m in open ground and at the switch post | 65 dB(A) or more at 100 m; about 95 dB(A) at the switch post |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before anyone goes onto the slope.** A competent person has looked at the slope that day; no one will work below an actively moving face or overhanging material; there is a spotter and a clear escape route; it is not raining hard and has not been; for a tailings dam, the owner's permit and the engineer of record's agreement are in hand.
- **S2. Before augering or driving.** Buried services have been checked with the site owner; the auger operator has a firm stance; no one stands downslope of the auger or the sledge.
- **S3. Before mixing grout.** Gloves, eye protection and long sleeves on; clean water at hand to wash off splashes.
- **S4. Before the FieldNode cell goes in.** Every safety stop of the FieldNode build plan has been passed.
- **S5. Before raising the mast or climbing to fit the alert unit.** Two people; a stable ladder footed by the second person; no overhead power line within reach of the mast or ladder; the mast's concrete has set for at least 3 days; the earth bond is fitted. The prototype mast stands only on a fenced test slope, and no one stands under it in high wind.
- **S6. Before the siren first sounds.** Hearing protection on everyone within 10 m; neighbours and site workers told that a test is coming, so a test is not taken for a real alarm.
- **S7. Before leaving the site.** The keyed switch is locked with its key held by the named person; every SMS recipient knows the system is a research prototype; signs at the site say what SlopeWatch cannot detect. Until a geotechnical partner has set the site's thresholds, the system logs only and raises no public alarm.

## 7. Tools, skills and workspace

**Tools.** Hacksaw with a 24 teeth per inch blade (or a bandsaw); pipe cutter and pipe wrench; bench vice with soft jaws; bench drill with a V-block; drills 2.5 to 20.5 mm; step drill to 20 mm; countersink; M4, M6 and M8 taps and tap drills; flat and half-round files; deburring tool; scriber, engineer's square, 45 degree square, steel rule, tape and calipers; aviation snips and two 1.2 m steel angles (or a sheet metal shop) for the guard; 3D printer that prints ASA; soldering iron, wire strippers and ferrule crimper; multimeter and clamp meter; USB to RS-485 adapter and laptop; hand post-hole auger 110 mm and an extension to 0.9 m; sledge hammer with a driving cap; post driver for the switch post; spirit level and a 1.5 m straight edge; bucket, trowel and rodding bar for grout; spade and shovel; stable ladder; sound level meter; stopwatch.

**Skills.** No certified trade is needed. Basic metalwork (marking out, sawing, drilling, tapping, filing), simple sheet folding or the use of a sheet metal shop, potting electronics, through-hole soldering and crimping, mixing and placing grout and concrete, and safe work on slopes with a trained team. All circuits are extra-low voltage: 5 V on the bus and 12 V on the alert unit, from the FieldNode cell. No mains wiring is part of this build.

**Workspace.** A workshop bench about 1.2 x 0.6 m with a metalwork corner kept apart from the electronics, a ventilated place for the printer and for potting, and a test slope with a partner's permission for steps 2 to 19.

**Personal protective equipment.** Safety glasses for cutting, drilling, driving and grouting; cut-resistant gloves for sheet and bar, chemical-resistant gloves for grout and potting; hearing protection when sawing, driving and testing the siren; safety boots and a hard hat on the slope; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 79 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/SLW-DWG-101` to `SLW-DWG-116`.
- General arrangement: `cad/drawings/SLW-DWG-001.pdf`, Rev P5.
- Calculations: `docs/04-calcs/01-sizing.md` (SLW-CAL-001 v0.4) and `docs/04-calcs/sizing.py`; crack gauge [C2], siren level [E5], mast [H1] to [H4] and the site mast [H2b], [H2c], installation [I1], [I2], cost [K2], [K3].
- Bill of materials: `bom/bom.csv` and `bom/bom-notes.md`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (SLW-DDR-003), with SLW-DDR-001 and SLW-DDR-002; design decisions register `docs/06-design-decisions.md` (SLW-DEC-001).
- Requirements: `docs/03-requirements.md` (SLW-REQ-001 v0.7).
- FieldNode core: the FieldNode repository, build plan FND-BLD-001 and decision record FND-DDR-003.
