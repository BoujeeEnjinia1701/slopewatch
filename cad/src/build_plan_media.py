"""SlopeWatch prototype build plan pictures (SLW-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|bus|site ...]
With no argument it draws everything; a sheet, joint or step number after its group draws only
that one (for example: python cad/src/build_plan_media.py sheets 101). Every 3D picture is drawn
from cad/src/model.py (build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/SLW-DWG-101 to 115        making sketches for the made and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/bus.png             bus and alert wiring at block level (matplotlib)
    docs/05-build-plan/site.png            reference site layout with cable runs (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, SITE, derived, build_components, fuse, bx, zcyl, ycyl, ztube  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
REV2 = {"105", "111", "116"}      # making sketches revised by the decisions of 2026-10-02
D = derived(P)
A = build_components(P)
ST, GA, MA, SW = A["stake"], A["gauge"], A["mast"], A["switch"]
XS, XG, XM, XW = P["arr_x"]

COL = {"pipe": "#78716C", "endcap": "#44403C", "grout": "#D6D3D1", "stand": "#E5E7EB", "capsule": "#0F766E",
       "collars": "#7C3AED", "plug": "#FDE68A", "lead": "#111827", "tape": "#1F2937", "reducer": "#F59E0B",
       "headtube": "#FFB000", "headcap": "#F59E0B", "band": "#E5E7EB", "label": "#F8FAFC", "arrow": "#111827", "fittings": "#374151", "conduit": "#334155", "screws": "#111827",
       "pins": "#57534E", "clamps": "#94A3B8", "setscrews": "#111827", "studs": "#111827", "balls": "#64748B",
       "sensor": "#7C3AED", "coupling": "#374151", "rod": "#A8A29E", "guard": "#9CA3AF", "pegs": "#44403C",
       "reader": "#0E7490", "mast": "#94A3B8", "footing": "#D6D3D1", "earth": "#15803D", "node": "#1E3A8A",
       "nplate": "#A8A29E", "vblock": "#57534E", "band": "#6B7280", "aplate": "#A8A29E", "abox": "#C2410C",
       "horn": "#9A3412", "beacon": "#F59E0B", "post": "#94A3B8", "splate": "#A8A29E", "sbox": "#C2410C"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def S(group, *keys):
    return fuse([group[k].shape for k in keys])


def at(shape, x=0.0, y=0.0, z=0.0):
    import build123d as b
    return b.Pos(x, y, z) * shape


def win(sh, x0, x1, y0, y1, z0, z1):
    import build123d as b
    return sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "pipe": part("Stake pipe with screwed end cap", S(ST, "pipe", "endcap"), COL["pipe"]),
        "grout": part("Grout column (cast in the hole)", ST["grout"].shape, COL["grout"]),
        "stand": part("Stand tube", ST["stand"].shape, COL["stand"]),
        "capsule": part("Sensor capsule with centring collars", S(ST, "capsule", "collars", "lead"), COL["capsule"]),
        "plug": part("Foam plug", ST["plug"].shape, COL["plug"]),
        "head": part("Stake head, tape wrap and screws", S(ST, "reducer", "headtube", "headcap", "tape", "screws", "mark_band", "mark_label", "mark_arrow"), COL["reducer"]),
        "fittings": part("Conduit fittings and bus conduit", S(ST, "fittings", "conduit_st"), COL["fittings"]),
        "pins": part("Anchor pins (2)", GA["pins"].shape, COL["pins"]),
        "clamps": part("Clamp blocks (2) with set screws and studs", S(GA, "clamps", "setscrews", "studs"), COL["clamps"]),
        "sensor": part("Displacement sensor, ball joints, extension rod", S(GA, "balls", "sensor", "coupling", "rod"), COL["sensor"]),
        "reader": part("Reader box with conduit fitting", S(GA, "reader", "reader_screws", "reader_fitting"), COL["reader"]),
        "guard": part("Guard and ground pegs", S(GA, "guard", "pegs"), COL["guard"]),
        "mast": part("Mast, footing, cap, earth rod and bond (site option)", S(MA, "mast_pipe", "footing", "mast_cap", "earth_rod", "bond_clamps", "bond"), COL["mast"]),
        "node": part("FieldNode core, built to its own plan", S(MA, "node", "node_plate", "node_vblocks", "node_bands"), COL["node"]),
        "aplate": part("Alert unit back plate and V-blocks", S(MA, "alert_plate", "alert_vblocks"), COL["aplate"]),
        "abox": part("Alert box with horn, beacon and glands", S(MA, "alert_box", "alert_nuts", "horn", "beacon", "alert_glands"), COL["abox"]),
        "abands": part("Alert unit band clamps (2)", MA["alert_bands"].shape, COL["band"]),
        "post": part("Switch post and cap", S(SW, "post", "post_cap"), COL["post"]),
        "splate": part("Switch back plate and hose clips", S(SW, "switch_plate", "switch_bands"), COL["splate"]),
        "sbox": part("Keyed switch box", S(SW, "switch_box", "switch_gland", "switch_key"), COL["sbox"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    import build123d as b
    M = made()
    short = {"pipe": "Stake pipe and end cap", "grout": "Grout column (cast)", "stand": "Stand tube",
             "capsule": "Capsule with collars", "plug": "Foam plug", "head": "Stake head, tape, screws",
             "fittings": "Conduit fittings, conduit", "pins": "Anchor pins (2)", "clamps": "Clamp blocks (2)",
             "sensor": "Sensor, ball joints, rod", "reader": "Reader box", "guard": "Guard and pegs",
             "mast": "Mast option (shortened)", "node": "FieldNode core", "aplate": "Alert back plate, V-blocks",
             "abox": "Alert box, horn, beacon", "abands": "Alert band clamps (2)", "post": "Switch post (shortened)",
             "splate": "Switch plate, hose clips", "sbox": "Keyed switch box"}
    H = P["mast_h"]
    # the mast and the switch post are drawn shortened (a middle length taken out) so the small parts stay readable
    gap = 90.0
    mast_lo = win(M["mast"].shape, -600, 600, -300, 300, -650, 300)
    mast_hi = b.Pos(0, 0, 300 + gap - (H - 500)) * win(M["mast"].shape, -100, 100, -100, 100, H - 500, H + 10)
    post_lo = win(M["post"].shape, -60, 60, -60, 60, -600, 250)
    post_hi = b.Pos(0, 0, 250 + gap - (P["switch_post"][2] - 400)) * win(M["post"].shape, -60, 60, -60, 60, P["switch_post"][2] - 400, P["switch_post"][2] + 10)
    zn, za, zs = P["node_z0"] - 400, D["alert_plate_z0"] - 300, P["switch_z"] - 350
    YF, XF = -800.0, -1450.0
    place = {"pipe": (0, 0, 0), "grout": (-220, 0, -100), "stand": (-400, 0, 250), "capsule": (-530, 0, 250),
             "plug": (-650, 0, 250), "head": (0, 0, 250), "fittings": (0, 0, 470),
             "pins": (1300, 0, 0), "clamps": (1300, 0, 250), "sensor": (1300, 0, 450), "guard": (1300, 0, 700),
             "reader": (1300, 0, 1000), "node": (XF + 450, YF - 150, -zn), "aplate": (XF + 950, YF, -za),
             "abox": (XF + 950, YF - 350, -za), "abands": (XF + 950, YF + 300, -za),
             "splate": (XF - 650, YF - 200, -zs), "sbox": (XF - 650, YF - 450, -zs)}
    parts = []
    for k, p in M.items():
        if k == "mast":
            sh = b.Pos(XF, YF, 0) * (mast_lo + mast_hi)
        elif k == "post":
            sh = b.Pos(XF - 650, YF, 0) * (post_lo + post_hi)
        else:
            sh = b.Pos(*place[k]) * p.shape
        parts.append(Part(short[k], sh, p.color, None, (0, 0, 0), p.alpha))
    return bv.overview(parts, OUT / "overview.png", "SlopeWatch prototype: every component, pulled apart",
                       subtitle="Numbered in build order: stake 1 to 7 (one of three) and crack gauge 8 to 12 on the right; switch post 18 to 20, "
                                "mast option 13, FieldNode 14 and alert unit 15 to 17 on the left. Mast and post drawn shortened",
                       elev=18, azim=-62, size=(13, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    M = made()
    base = dict(project="SlopeWatch", date=DATE)
    out = []
    stake_ctx = [M[k] for k in ("grout", "stand", "head")]

    def sheet(no, *a, **k):
        if only is None or no in only:
            if str(no) in REV2:
                k = dict(k, date="2026-10-02", rev="P2", revisions=[("P1", "Making sketch for the prototype build plan", "2026-10-01", "AC"),
                                                  ("P2", "SLW-DEC-001: head marking, wall holes, 60.3 mm site mast", "2026-10-02", "AC")])
            out.append(bv.component_sheet(*a, dwg_no=f"SLW-DWG-{no}", **k, **{x: y for x, y in base.items() if x not in k}))

    pipe = S(ST, "pipe", "endcap")
    sheet(101, Part("Stake pipe", pipe, COL["pipe"]), stake_ctx + [M["capsule"]],
          title="SlopeWatch stake pipe with end cap (make 3): making sketch",
          material="Galvanized steel pipe 48.3 x 3.2 mm (1.5 in), threaded one end; malleable-iron cap",
          view_shape=S(ST, "endcap") + ztube(0, 0, -P["embed"], D["stake_top"], P["pipe"][0] / 2, D["pipe_id"] / 2), inset_view=(12, -60),
          notes=["Make three. Cut 1,000 mm of 48.3 x 3.2 mm galvanized pipe with",
                 "  one end threaded 1.5 in (have the merchant cut and thread it).",
                 "Screw the 1.5 in malleable-iron end cap onto the threaded end with",
                 "  thread sealant, hand tight plus a quarter turn with a pipe wrench.",
                 "File the other (top) end square and deburr inside and out.",
                 "Paint a ground mark round the pipe 200 mm below the top; the pipe",
                 "  goes into the ground up to this mark (800 mm buried).",
                 "Touch up cut galvanizing with zinc-rich paint.",
                 "Do not drill the head screw holes yet: they are drilled through",
                 "  the head's socket at assembly so they line up (step 6).",
                 "Fit: the cap keeps grout and water out of the bottom; the stand",
                 "  tube stands on the cap's floor inside the pipe.",
                 "Check: blow down the pipe; no light or air through the cap."])

    sheet(102, Part("Stand tube", ST["stand"].shape, COL["stand"]), [part("End cap", ST["endcap"].shape, COL["endcap"]), M["capsule"]],
          title="SlopeWatch stand tube (make 3): making sketch", material="PVC pressure pipe 40 mm OD, 2 mm wall",
          view_shape=ST["stand"].shape, inset_view=(12, -60),
          notes=[f"Make three. Cut {D['stand_l']:.0f} mm of 40 mm OD PVC pipe, ends square.",
                 "Deburr both ends; chamfer the outside edges 1 mm so it slides",
                 "  down the 41.9 mm bore of the stake pipe without catching.",
                 f"Its length sets the capsule depth: capsule centre {P['capsule_depth']:.0f} mm",
                 "  below ground when the stand tube sits on the end cap floor.",
                 "Fit: drops down the pipe and stands on the cap floor, 0.95 mm",
                 "  clear of the bore all round. The capsule's lower collar sits on",
                 "  its top rim; the capsule itself is 1 mm inside the rim.",
                 "Mark the length on the tube; check it with a tape before cutting,",
                 "  since a 10 mm error moves the capsule 10 mm.",
                 f"Check: {D['stand_l']:.0f} mm long, within 2 mm; slides freely down an offcut",
                 "  of the stake pipe."])

    collar = ST["collars"].shape & bx(-30, 30, -30, 30, D["cap_bot"] - 1, D["cap_bot"] + P["collar"][1] + 1)
    sheet(103, Part("Centring collar", collar, COL["collars"]), [part("Capsule", ST["capsule"].shape, COL["capsule"]), M["stand"]],
          title="SlopeWatch capsule centring collar (make 6): making sketch", material="ASA, 3D printed, 100 % infill",
          view_shape=at(collar, z=-D["cap_bot"]), inset_view=(20, -60),
          notes=["Make six, two per capsule. Print ASA flat, 100 % infill.",
                 f"Ring {P['collar'][0]} mm outside, {P['capsule'][0]:.0f} mm inside, {P['collar'][1]:.0f} mm long.",
                 "Print one first and check it: it must be a light press fit on",
                 "  the capsule tube and slide freely in an offcut of the stake",
                 "  pipe (bore 41.9 mm). Adjust the outside size in steps of 0.2 mm.",
                 "Fit: one collar flush with each end of the capsule, with a drop",
                 "  of polyurethane adhesive. They hold the capsule on the pipe axis",
                 "  so it tilts with the pipe; 0.2 mm clearance to the bore.",
                 "The lower collar rests on the stand tube's top rim.",
                 "Check: on the capsule, both collars turn freely in the pipe offcut",
                 "  and the capsule does not rock when held level."])

    cap = S(ST, "capsule", "collars")
    sheet(104, Part("Sensor capsule", cap, COL["capsule"]), [M["stand"], M["plug"], part("End cap", ST["endcap"].shape, COL["endcap"])],
          title="SlopeWatch sensor capsule (make 3): making sketch", material="Polycarbonate tube 34 x 2 mm, potted electronics",
          view_shape=at(cap, z=P["capsule_depth"]), inset_view=(12, -60),
          notes=[f"Make three. Tube {P['capsule'][0]:.0f} mm OD x {P['capsule'][1]:.0f} mm, polycarbonate, 2 mm wall.",
                 "Board: inclinometer, microcontroller, RS-485 transceiver and 3.3 V",
                 "  regulator, at most 28 mm wide, flashed and bench-read first.",
                 "Mark the board's X axis with an arrow on the tube label: the arrow",
                 "  points downslope when the capsule is lowered (step 4).",
                 "Lead: 0.8 m of 4-core 0.25 mm2 shielded cable, out of the top centre.",
                 "Seal the bottom with a glued disc, slide the board in on a",
                 "  printed carrier square to the tube, and pot it full with",
                 "  polyurethane potting compound; cure as its maker says.",
                 "Glue a centring collar flush on each end (SLW-DWG-103).",
                 "Fit: rests on the stand tube on its lower collar, centred in the",
                 "  pipe by both collars; the foam plug sits 10 mm above it.",
                 "Check: reads within 0.1 degree of a spirit level on the bench."])

    head = S(ST, "reducer", "headtube", "headcap", "fittings", "mark_band", "mark_label", "mark_arrow")
    sheet(105, Part("Stake head", head, COL["reducer"]), [M["pipe"], M["fittings"]],
          title="SlopeWatch stake head (make 3): making sketch", material="Stock PVC drainage fittings, 110 mm",
          view_shape=at(head, z=-D["head_bot"]), inset_view=(18, -60),
          notes=["Make three from stock 110 mm PVC drainage parts: a 110 x 50 mm",
                 "  concentric reducer, a 110 mm end cap and 94 mm of 110 mm pipe.",
                 "Cut the 110 pipe square to 94 mm and deburr.",
                 "Drill two 20.5 mm holes for the M20 conduit fittings, opposite each",
                 "  other, centred 46 mm up from the pipe's lower end (check the",
                 "  fitting's datasheet). One faces upslope, one downslope.",
                 "Push the pipe fully into the reducer's 110 socket and the cap onto",
                 "  its top; solvent-cement both joints.",
                 "Paint the outside signal amber. Round the cap skirt wind 25 mm",
                 "  retroreflective tape; stick a 40 x 30 mm ID label on the -Y side and",
                 "  an arrow on the crown pointing downslope (+X).",
                 "Fit: the reducer's 50 mm socket goes over the stake pipe on a tape",
                 "  wrap; two M5 self-tapping screws hold it, drilled through the",
                 "  socket into the pipe at assembly, 20 mm above the socket rim.",
                 "Check: the head stands 330 mm above ground on the stake."])

    pin1 = GA["pins"].shape & bx(-500, -400, -50, 50, -600, 300)
    sheet(106, Part("Anchor pin", pin1, COL["pins"]), [M["clamps"], M["sensor"]],
          title="SlopeWatch anchor pin (make 2): making sketch", material="Mild steel round bar 20 mm, galvanized or painted",
          view_shape=at(pin1, x=P["anchor_span"] / 2), inset_view=(18, -60),
          notes=[f"Make two. Cut {P['pin_l']:.0f} mm of 20 mm round bar.",
                 "Grind a point 30 mm long on one end, about 4 mm across the tip.",
                 "Chamfer the top edge 2 mm so a sledge does not mushroom it.",
                 f"Paint a ring {P['pin_embed']:.0f} mm from the tip: drive to this ring, which",
                 f"  leaves {P['pin_l'] - P['pin_embed']:.0f} mm above ground.",
                 "Paint the exposed part (or use galvanized bar).",
                 f"Fit: driven upright {P['anchor_span']:.0f} mm apart, one each side of the crack,",
                 "  on a line square to it. Each carries a clamp block with its",
                 "  centre 110 mm above ground.",
                 "Check: a level on the pin shows it upright within 2 degrees."])

    blk = GA["clamps"].shape & bx(-500, -400, -50, 50, 0, 200)
    sheet(107, Part("Clamp block", blk, COL["clamps"]), [M["pins"], M["sensor"]],
          title="SlopeWatch crack gauge clamp block (make 2): making sketch", material="Aluminium square bar 40 x 40 mm, 6082",
          view_shape=at(blk, x=P["anchor_span"] / 2, z=-P["gauge_z"]), inset_view=(25, -50),
          notes=[f"Make two the same. Saw {P['clamp'][2]:.0f} mm off 40 x 40 mm bar; file square.",
                 "Bore: drill 20.5 mm right through the 40 x 40 faces, on centre.",
                 "Stud hole: on one 40 x 60 side face, at mid-height (30 mm up)",
                 "  and centred, drill 5.0 mm 12 deep and tap M6 10 deep.",
                 "Set screw hole: on the opposite side face, 45 mm up and centred,",
                 "  drill 6.8 mm through into the bore and tap M8.",
                 "Fit: slides onto the pin; the stud face points at the other pin",
                 "  across the crack. Set the block centre 110 mm above ground and",
                 "  tighten the M8 set screw onto the pin.",
                 "Screw the M6 stud of a rod-end ball joint 10 mm into the stud hole",
                 "  with medium threadlocker.",
                 "Check: the block slides on a 20 mm bar with no shake beyond 0.5 mm."])

    rod1 = GA["rod"].shape
    sheet(108, Part("Extension rod", rod1, COL["rod"]), [M["sensor"], M["clamps"]],
          title="SlopeWatch crack gauge extension rod: making sketch", material="Stainless steel round bar 8 mm, 304",
          view_shape=b.Rot(0, -90, 0) * at(rod1, x=-(D["coupling_x1"] + D["rod_x1"]) / 2, z=-P["gauge_z"]), inset_view=(25, -50),
          notes=[f"Cut {D['rod_l']:.0f} mm of 8 mm stainless bar, ends square.",
                 "Centre-drill each end in a drill press with the bar held",
                 "  upright in a V-block; drill 5.0 mm 15 deep and tap M6.",
                 "Screw an M6 x 20 stud into each end with medium threadlocker,",
                 "  10 mm in and 10 mm out.",
                 "Fit: one end into the coupling nut on the sensor's plunger; the",
                 "  other into the downslope rod-end ball joint on its stud.",
                 "Set the plunger 15 mm out of the sensor body before tightening,",
                 "  so the gauge can read 85 mm of opening and 15 mm of closing.",
                 f"Check: {D['rod_l']:.0f} mm long within 1 mm; straight within 1 mm",
                 "  when rolled on a flat bench."])

    g = GA["guard"].shape
    sheet(109, Part("Guard", g, COL["guard"]), [M["pins"], M["clamps"], M["sensor"], M["reader"]],
          title="SlopeWatch crack gauge guard: making sketch", material="Galvanized steel sheet 1.5 mm",
          inset_view=(25, -55),
          notes=["Blank 1,150 x 750 mm of 1.5 mm galvanized sheet. Fold lines along",
                 "  the 1,150 mm length at 25, 275, 475 and 725 mm from one edge.",
                 "Fold the two outer 25 mm strips out (feet) and the 250 mm legs",
                 "  down, to an inverted channel 200 wide, 250 high, with feet.",
                 "Have it folded by a sheet metal shop, or fold it between two",
                 "  1.2 m steel angles clamped to a bench.",
                 "Peg holes: four 9 mm, centred in the feet, 40 and 455 mm from",
                 "  the upslope end. Only the upslope half is pegged, so the crack",
                 "  can open under the downslope half.",
                 "Reader screw holes: two 4.5 mm in the web, 100 and 150 mm from",
                 "  the upslope end, 52 mm to one side of the centre line.",
                 "Fit: stands over the gauge on its feet, 48 mm above the pin tops.",
                 "Check: the web is flat and the legs square within 3 mm."])

    rd = S(GA, "reader")
    sheet(110, Part("Reader box", rd, COL["reader"]), [M["guard"], M["pins"], M["clamps"]],
          title="SlopeWatch crack gauge reader box: drilling sketch", material="Bought IP67 box 80 x 60 x 45 mm",
          view_shape=at(rd, x=P["anchor_span"] / 2), inset_view=(-30, -55),
          notes=["A bought IP67 box, 80 x 60 x 45 mm, holding the reader board.",
                 "Base (the face that goes against the guard web): two 4 mm holes",
                 "  50 mm apart on the long centre line, matching the web holes.",
                 "  Seal under each screw head with a nylon washer.",
                 "Downslope end: one 20.5 mm hole, centred, for the M20 conduit",
                 "  fitting that carries the bus out.",
                 "Upslope end: one 12.5 mm hole for an M12 gland for the sensor lead.",
                 "Fit the reader board on its standoffs; terminate the sensor lead",
                 "  and the bus in lever connectors as the bus diagram shows.",
                 "Fit: hangs under the guard web at the upslope end, lid down,",
                 "  12 mm clear of the upslope pin.",
                 "Check: lid gasket seated; the box hangs level."])

    ap = MA["alert_plate"].shape
    hb = D["alert_plate_z0"]
    sheet(111, Part("Alert unit back plate", ap, COL["aplate"]), [M["abox"], part("V-blocks", MA["alert_vblocks"].shape, COL["vblock"]), M["abands"]],
          title="SlopeWatch alert unit back plate: making sketch", material="Aluminium sheet 3 mm, 5052 or 6061",
          view_shape=at(ap, z=-hb), inset_view=(18, 130),
          notes=[f"Blank {P['alert_plate'][0]:.0f} x {P['alert_plate'][1]:.0f} mm of 3 mm aluminium; round corners 2 mm.",
                 "Heights from the bottom edge; sideways from the centre line.",
                 f"Band slots 6 x 15 mm at {P['alert_slot_x']:.0f} mm each side, centred 20 and",
                 "  190 mm up: chain drill 3 mm, file square.",
                 "V-block screws: 4.5 mm at 18 mm each side, 20 and 190 mm up,",
                 "  countersunk from the front.",
                 "Alert box screws: 5.5 mm at 45 mm each side, 235 and 325 mm up.",
                 "Wall holes: four 6.5 mm at 70 mm each side, 45 and 315 mm up, for",
                 "  M6 coach screws into a timber pole or wall.",
                 "Deburr every hole and edge.",
                 "Fit: V-blocks on the back; the alert box on the front, top part;",
                 "  the two band clamps go round the pole through the slots below",
                 "  the box. The top 110 mm stands above a mast top.",
                 "Check: lay the V-blocks and box on it and look through each hole."])

    vb = MA["alert_vblocks"].shape & bx(-40, 40, -50, 0, hb, hb + 40)
    sheet(112, Part("V-block", vb, COL["vblock"]), [part("Back plate", MA["alert_plate"].shape, COL["aplate"]), M["abands"], part("Pole", win(MA["mast_pipe"].shape, -30, 30, -30, 30, hb - 150, hb + 300), COL["mast"])],
          title="SlopeWatch alert unit V-block (make 2): making sketch", material="Aluminium flat bar 60 x 40 mm, 6082 or 6061",
          view_shape=at(vb, z=-(hb + 20)), inset_view=(30, 60),
          notes=["Make two, the same as the FieldNode V-block (FND-DWG-102).",
                 "Saw a 20 mm slice off 60 x 40 mm bar; saw and file it to",
                 "  60 wide x 33 deep x 20 tall. The flat back goes on the plate.",
                 "Scribe a 90 degree V on both 60 x 33 faces with a 45 degree square:",
                 "  50.3 mm wide at the front face, point 7.8 mm from the back face.",
                 "Saw inside both lines and file to them; keep the V faces flat.",
                 "Break the V's front edges 0.5 mm.",
                 "Drill 3.3 mm 14 deep and tap M4 12 deep in the back face, 18 mm",
                 "  each side of centre, half way up.",
                 "Fit: two M4 countersunk screws from the front of the plate. A",
                 "  48.3 mm pole touches both V faces; 40 to 70 mm poles also seat.",
                 "Check: on a 48 mm tube it must not rock."])

    ab = MA["alert_box"].shape
    bz0 = D["alert_box_z0"]
    yb = P["node_plate_y0"] - P["alert_plate"][2] - P["alert_box"][1] / 2
    holes = (zcyl(-30, yb, bz0 - 1, bz0 + 4, 8.1) + zcyl(30, yb, bz0 - 1, bz0 + 4, 8.1)
             + zcyl(0, yb, bz0 + P["alert_box"][2] - 4, bz0 + P["alert_box"][2] + 1, 5)
             + ycyl(0, yb - P["alert_box"][1] / 2 - 1, yb - P["alert_box"][1] / 2 + 4, bz0 + P["alert_box"][2] / 2, 5))
    abd = ab - holes
    sheet(113, Part("Alert box", abd, COL["abox"]), [M["aplate"], part("Horn and beacon", S(MA, "horn", "beacon"), COL["horn"])],
          title="SlopeWatch alert box: drilling sketch", material="Bought IP65 box 120 x 90 x 120 mm, corner holes outside the seal",
          view_shape=at(abd, y=-yb, z=-bz0), inset_view=(18, -60),
          notes=["A bought IP65 box, 120 wide x 90 deep x 120 tall, with four corner",
                 "  screw holes outside the lid seal (90 x 90 mm apart).",
                 "Bottom: two 16.2 mm holes 30 mm each side of centre, for M16",
                 "  glands: the lead to the node and the switch lead.",
                 "Top: one 10 mm hole, centred, for the beacon lead; the beacon base",
                 "  covers it with its own gasket and three screws.",
                 "Front (lid side faces forward): one 10 mm hole, centred, for the",
                 "  horn leads; the horn's flange and gasket cover it.",
                 "Tape the faces, pilot drill 3 mm slowly, open with a step drill.",
                 "Fit the MOSFET driver inside on its standoffs.",
                 "Fit: four M5 screws through the corner holes and the back plate,",
                 "  nyloc nuts behind the plate.",
                 "Check: every hole covered by a gland, gasket or flange."])

    post = SW["post"].shape
    sheet(114, Part("Switch post", S(SW, "post", "post_cap"), COL["post"]), [M["splate"], M["sbox"]],
          title="SlopeWatch keyed switch post: making sketch", material="Galvanized steel tube 26.9 x 2.6 mm (3/4 in)",
          view_shape=post, inset_view=(15, -60),
          notes=[f"Cut {P['switch_post'][2] + P['switch_post'][3]:,.0f} mm of 26.9 x 2.6 mm galvanized tube.",
                 "Cut the lower end at 45 degrees so it drives more easily; file",
                 "  the top end square and deburr.",
                 f"Paint a ground mark {P['switch_post'][3]:.0f} mm from the lower tip.",
                 "Touch up cut ends with zinc-rich paint.",
                 "Push a 27 mm plastic tube cap onto the top end.",
                 f"Fit: driven upright {P['switch_post'][3]:.0f} mm into the ground with a post",
                 "  driver, about 5 m from the mast on the side away from the horn.",
                 "The switch back plate clamps to it with two hose clips, the switch",
                 f"  box centre {P['switch_z']:,.0f} mm above ground.",
                 "Check: upright within 2 degrees; does not move when pushed by hand."])

    sp = SW["switch_plate"].shape
    sheet(115, Part("Switch back plate", sp, COL["splate"]), [part("Post", win(SW["post"].shape, -30, 30, -30, 30, 1100, 1500), COL["post"]), M["sbox"]],
          title="SlopeWatch keyed switch back plate: making sketch", material="Galvanized steel sheet 3 mm",
          view_shape=at(sp, z=-(P["switch_z"] - P["switch_plate"][1] / 2)), inset_view=(18, -60),
          notes=[f"Blank {P['switch_plate'][0]:.0f} x {P['switch_plate'][1]:.0f} mm of 3 mm galvanized sheet; round corners.",
                 "Heights from the bottom edge; sideways from the centre line.",
                 f"Hose clip slots 6 x 15 mm at {P['switch_slot_x']:.0f} mm each side, centred 18",
                 "  and 142 mm up: chain drill 3 mm, file square.",
                 "Box screw holes: four 4.5 mm at 40 mm each side, 52 and 108 mm",
                 "  up (match them to your box's corner holes).",
                 "Deburr and touch up with zinc-rich paint.",
                 "Fit: the back of the plate bears on the post; two 20 to 32 mm",
                 "  stainless hose clips go round the post, through the slots and",
                 "  across the plate front, above and below the box.",
                 "Check: the plate does not turn on the post when the clips are tight."])

    mp = S(MA, "mast_pipe")
    sheet(116, Part("Mast pipe", S(MA, "mast_pipe", "mast_cap"), COL["mast"]), [M["aplate"], M["abox"], M["node"]],
          title="SlopeWatch mast (site option): making sketch", material="Galvanized steel pipe 48.3 x 3.2 mm (1.5 in)",
          view_shape=mp, inset_view=(10, -60),
          notes=["Only where the site has no 40 to 70 mm pole for the node and the",
                 "  alert unit. Prototype mast: 3,750 mm of 48.3 x 3.2 mm galvanized pipe",
                 "  (fenced test slope only); a working site uses 60.3 x 3.6 mm pipe.",
                 "File both ends square; touch up with zinc-rich paint.",
                 "Paint a ground mark 550 mm from the lower end.",
                 "Push a 48 mm plastic pipe cap onto the top end.",
                 "Fit: cast 550 mm into a 320 mm x 600 mm concrete footing, plumb.",
                 f"FieldNode bottom {P['node_z0']:,.0f} mm above ground; alert unit back plate",
                 f"  {D['alert_plate_z0']:,.0f} to {D['alert_plate_z0'] + P['alert_plate'][1]:,.0f} mm, its top 110 mm above the mast top.",
                 "Bonding clamp round the mast 20 to 40 mm above the footing;",
                 "  16 mm2 bond to the earth rod clamp 450 mm away.",
                 "Check: plumb within 1 degree after the concrete has set."])
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []

    def jn(n, parts, title, sub, **kw):
        if only is None or n in only:
            out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))

    zb = -P["embed"]
    w = (-70, 70, -70, 70, D["hole_bot"] - 5, zb + 140)
    jn(1, [part("Stake pipe", win(ST["pipe"].shape, *w), COL["pipe"]),
           part("Screwed end cap", win(ST["endcap"].shape, *w), COL["endcap"]),
           part("Stand tube on the cap floor", win(ST["stand"].shape, *w), COL["stand"]),
           part("Grout round the cap and pipe", win(ST["grout"].shape, *w), COL["grout"])],
       "the stake's bottom end, cut open", "The cap keeps grout out of the pipe; 20 mm of grout under the cap",
       cut="+Y", elev=12, azim=-80, size=(8, 6))
    w = (-60, 60, -60, 60, D["cap_bot"] - 60, D["cap_top"] + 110)
    jn(2, [part("Stake pipe (bore 41.9 mm)", win(ST["pipe"].shape, *w), COL["pipe"]),
           part("Stand tube", win(ST["stand"].shape, *w), COL["stand"]),
           part("Centring collars", win(ST["collars"].shape, *w), COL["collars"]),
           part("Sensor capsule", win(ST["capsule"].shape, *w), COL["capsule"]),
           part("Foam plug, slit for the lead", win(ST["plug"].shape, *w), COL["plug"]),
           part("Capsule lead", win(ST["lead"].shape, *w), COL["lead"])],
       "capsule in the pipe, cut open", "Collars hold the capsule on the pipe axis; it rests on the stand tube, 0.4 m below ground",
       cut="+Y", elev=10, azim=-80, size=(8, 6.5))
    w = (-70, 70, -70, 70, D["head_bot"] - 40, D["stake_top"] + 40)
    jn(3, [part("Stake pipe", win(ST["pipe"].shape, *w), COL["pipe"]),
           part("Tape wrap", win(ST["tape"].shape, *w), COL["tape"]),
           part("Reducer socket", win(ST["reducer"].shape, *w), COL["reducer"]),
           part("M5 self-tapping screw (one each side)", win(ST["screws"].shape, *w), COL["screws"]),
           part("Capsule lead", win(ST["lead"].shape, *w), COL["lead"])],
       "head socket on the pipe, cut open", "The 50 mm socket slides over the tape wrap; two screws go through it into the pipe wall",
       cut="+Y", elev=12, azim=-75, size=(8, 6))
    w = (-200, 200, -80, 80, D["stake_top"] - 60, D["head_top"] + 10)
    jn(4, [part("Head (reducer, 110 tube, end cap)", win(S(ST, "reducer", "headtube", "headcap", "mark_band"), *w), COL["reducer"]),
           part("Conduit fitting, bus in (upslope)", win(ST["fittings"].shape, -200, 0, -80, 80, w[4], w[5]), COL["fittings"]),
           part("Conduit fitting, bus out (downslope)", win(ST["fittings"].shape, 0, 200, -80, 80, w[4], w[5]), COL["fittings"]),
           part("20 mm conduit", win(ST["conduit_st"].shape, *w), COL["conduit"]),
           part("Stake pipe", win(ST["pipe"].shape, *w), COL["pipe"])],
       "conduit fittings in the head", "Bus in on the upslope side, bus out on the downslope side; lock nuts inside the head",
       cut="+Y", elev=18, azim=-70, size=(8, 6))
    a = P["anchor_span"] / 2
    gz = P["gauge_z"]
    w = (-a - 40, -a + 120, -40, 40, gz - 60, gz + 60)
    jn(5, [part("Anchor pin (upslope)", win(GA["pins"].shape, *w), COL["pins"]),
           part("Clamp block", win(GA["clamps"].shape, *w), COL["clamps"]),
           part("M8 set screw onto the pin", win(GA["setscrews"].shape, *w), COL["setscrews"]),
           part("M6 stud", win(GA["studs"].shape, *w), COL["studs"]),
           part("Rod-end ball joint", win(GA["balls"].shape, *w), COL["balls"]),
           part("Sensor body", win(GA["sensor"].shape, *w), COL["sensor"])],
       "upslope clamp block, ball joint and sensor", "The ball joint lets the crack open, close or shear without bending the sensor. Seen from above",
       elev=48, azim=-105, size=(8, 6))
    w = (D["body_x1"] - 60, D["coupling_x1"] + 60, -30, 30, gz - 30, gz + 30)
    jn(6, [part("Sensor body", win(GA["sensor"].shape, D["body_x1"] - 60, D["body_x1"], -30, 30, gz - 30, gz + 30), COL["sensor"]),
           part("Plunger, 15 mm out", win(GA["sensor"].shape, D["body_x1"], D["plunger_x1"], -30, 30, gz - 30, gz + 30), "#A78BFA"),
           part("M6 coupling nut", win(GA["coupling"].shape, *w), COL["coupling"]),
           part("Extension rod (stud into its end)", win(GA["rod"].shape, *w), COL["rod"])],
       "plunger to extension rod", "The coupling joins the plunger thread to the rod's stud; set 15 mm of plunger out first",
       elev=20, azim=-60, size=(8, 5.5))
    w = (a - 120, a + 40, -40, 40, gz - 60, gz + 60)
    jn(7, [part("Anchor pin (downslope)", win(GA["pins"].shape, *w), COL["pins"]),
           part("Clamp block", win(GA["clamps"].shape, *w), COL["clamps"]),
           part("Set screw", win(GA["setscrews"].shape, *w), COL["setscrews"]),
           part("Rod-end ball joint on its stud", win(S(GA, "balls", "studs"), *w), COL["balls"]),
           part("Extension rod", win(GA["rod"].shape, *w), COL["rod"])],
       "downslope clamp block and rod end", "The second ball joint screws onto the rod's stud and onto the block's stud",
       elev=48, azim=-75, size=(8, 6))
    gl, gw, gh = P["guard"][:3]
    w = (-gl / 2 - 10, -a + 120, -gw / 2 - 40, gw / 2 + 40, -60, gh + 10)
    jn(8, [part("Guard (cut open)", win(GA["guard"].shape, *w), COL["guard"]),
           part("Ground peg through the foot", win(GA["pegs"].shape, *w), COL["pegs"]),
           part("Reader box under the web", win(GA["reader"].shape, *w), COL["reader"]),
           part("Reader screws", win(GA["reader_screws"].shape, *w), COL["screws"]),
           part("Conduit fitting, bus out", win(GA["reader_fitting"].shape, *w), COL["fittings"]),
           part("Upslope pin and clamp", win(S(GA, "pins", "clamps"), *w), COL["pins"])],
       "guard foot, peg and reader box (upslope end)", "Pegs only on the upslope half; the reader hangs under the web, lid down. Near half cut away",
       cut="+Y", elev=22, azim=-128, size=(8, 6))
    zc = D["alert_plate_z0"] + 190
    w = (-90, 90, -70, 50, zc - 8, zc + 8)
    jn(9, [part("Mast or pole", win(MA["mast_pipe"].shape, *w), COL["mast"]),
           part("Back plate", win(MA["alert_plate"].shape, *w), COL["aplate"]),
           part("V-block", win(MA["alert_vblocks"].shape, *w), COL["vblock"]),
           part("Band clamp, through the slots", win(MA["alert_bands"].shape, *w), COL["band"])],
       "alert unit V-block and band clamp", "Cut level with the upper band, seen from above. The pole bears on both V faces",
       elev=80, azim=-90, size=(8, 6))
    bz0 = D["alert_box_z0"]
    w = (-90, 90, -300, 30, bz0 - 40, bz0 + 200)
    jn(10, [part("Back plate", win(MA["alert_plate"].shape, *w), COL["aplate"]),
            part("Alert box", win(MA["alert_box"].shape, *w), COL["abox"]),
            part("M5 screws, nyloc nuts behind", win(MA["alert_nuts"].shape, *w), COL["screws"]),
            part("Horn on the front", win(MA["horn"].shape, *w), COL["horn"]),
            part("Beacon on the top", win(MA["beacon"].shape, *w), COL["beacon"]),
            part("Glands underneath", win(MA["alert_glands"].shape, *w), COL["fittings"]),
            part("Mast top and cap", win(S(MA, "mast_pipe", "mast_cap"), *w), COL["mast"])],
        "alert box on its back plate", "Seen from behind and to one side: four corner screws, nyloc nuts on the back of the plate beside the pole",
        elev=14, azim=40, size=(8, 6.5))
    zc = P["switch_z"]
    w = (-70, 70, -100, 30, zc - 95, zc + 95)
    jn(11, [part("Switch post", win(SW["post"].shape, *w), COL["post"]),
            part("Back plate", win(SW["switch_plate"].shape, *w), COL["splate"]),
            part("Hose clips through the slots", win(SW["switch_bands"].shape, *w), COL["band"]),
            part("Keyed switch box", win(S(SW, "switch_box", "switch_gland", "switch_key"), *w), COL["sbox"])],
        "keyed switch box on its post", "Two hose clips, above and below the box, hold the plate to the post",
        elev=15, azim=-140, size=(8, 6))
    er_x = P["earth_rod"][2]
    w = (-180, er_x + 60, -170, 170, -250, 120)
    jn(12, [part("Concrete footing (cut open)", win(MA["footing"].shape, *w), COL["footing"]),
            part("Mast pipe", win(MA["mast_pipe"].shape, *w), COL["mast"]),
            part("Earth rod", win(MA["earth_rod"].shape, *w), COL["earth"]),
            part("Rod clamp and mast bonding clamp", win(MA["bond_clamps"].shape, *w), COL["endcap"]),
            part("16 mm2 bond conductor", win(MA["bond"].shape, *w), "#16A34A")],
        "mast foot and earth bond (site option)", "The bond runs from a clamp on the mast to a clamp on the earth rod",
        cut="+Y", elev=15, azim=-70, size=(8, 6))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        if only is None or n in only:
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    pipe = part("Stake pipe", ST["pipe"].shape, COL["pipe"])
    st(1, [pipe], [mv(part("Screwed end cap", ST["endcap"].shape, COL["endcap"]), (0, 0, -150))],
       "end cap onto the stake pipe", "Thread sealant; hand tight plus a quarter turn. Paint the ground mark 200 mm below the top",
       elev=12, azim=-60)
    pc = M["pipe"]
    st(2, [pc], [mv(M["grout"], (0, 0, 420))], "set the pipe and pour the grout",
       f"Auger a 110 mm hole {D['hole_depth']:.0f} mm deep; pipe plumb in it, to its ground mark; grout to 450 mm up; backfill above",
       elev=10, azim=-60)
    stake_set = [pc, M["grout"]]
    st(3, stake_set, [mv(M["stand"], (0, 0, 1000))], "stand tube down the pipe",
       "After the grout has set for 24 h. It stands on the cap floor and sets the capsule depth",
       elev=10, azim=-60, label_done=False)
    st(4, stake_set + [M["stand"]], [mv(M["capsule"], (0, 0, 900))], "capsule down onto the stand tube",
       "Lower it on its lead, arrow on the label downslope, until the lower collar rests on the stand tube",
       elev=10, azim=-60, label_done=False)
    st(5, stake_set + [M["stand"], M["capsule"]], [mv(M["plug"], (0, 0, 700))], "foam plug above the capsule",
       "Slit it, put the lead in the slit, push it down with a rod to 10 mm above the capsule",
       elev=10, azim=-60, label_done=False)
    top = lambda p_: Part(p_.name, win(p_.shape, -300, 300, -300, 300, -120, 600), p_.color, None, p_.explode, p_.alpha)  # noqa: E731
    below = [top(M["pipe"]), top(M["capsule"])]
    st(6, below, [mv(part("Tape wrap", ST["tape"].shape, COL["tape"]), (0, 0, 0)),
                  mv(part("Stake head", S(ST, "reducer", "headtube", "headcap", "mark_band", "mark_label", "mark_arrow"), COL["reducer"]), (0, 0, 250)),
                  mv(part("M5 screws (2)", ST["screws"].shape, COL["screws"]), (0, 0, 0))],
       "head onto the pipe", "Top of the stake. Tape wrap on the pipe top, head pushed on; drill 4.2 mm through socket and pipe; two M5 screws",
       elev=12, azim=-60, label_done=False)
    head_on = below + [top(M["head"])]
    fc = S(ST, "fittings", "conduit_st")
    st(7, head_on, [mv(part("Fitting and conduit, bus in (upslope)", win(fc, -400, 0, -100, 100, 0, 600), COL["fittings"]), (-160, 0, 0)),
                    mv(part("Fitting and conduit, bus out (downslope)", win(fc, 0, 400, -100, 100, 0, 600), COL["conduit"]), (160, 0, 0))],
       "conduit fittings and the bus",
       "Fittings through the head, lock nuts inside; bus in upslope, out downslope; join at lever connectors; cap on",
       elev=15, azim=-60, label_done=False)
    st(8, [], [mv(M["pins"], (0, 0, 600))], "drive the anchor pins",
       f"{P['anchor_span']:.0f} mm apart, one each side of the crack, on a line square to it; drive to the painted ring",
       elev=15, azim=-60)
    gtop = lambda p_: Part(p_.name, win(p_.shape, -800, 800, -400, 400, -150, 1200), p_.color, None, p_.explode, p_.alpha)  # noqa: E731
    st(9, [gtop(M["pins"])], [mv(M["clamps"], (0, 0, 350))], "clamp blocks onto the pins",
       "Stud faces toward each other across the crack; block centres 110 mm above ground; set screws tight",
       elev=18, azim=-60, label_done=False)
    st(10, [gtop(M["pins"]), M["clamps"]], [mv(M["sensor"], (0, -250, 120))], "sensor and extension rod onto the studs",
       "Plunger 15 mm out; upslope ball joint on its stud first, then the rod's ball joint on the downslope stud",
       elev=18, azim=-60, label_done=False)
    rd = part("Reader box", S(GA, "reader", "reader_screws", "reader_fitting"), COL["reader"])
    st(11, [part("Guard", GA["guard"].shape, COL["guard"])], [mv(rd, (0, 0, -250))], "reader box under the guard",
       "Guard upside down on the bench; two M4 screws through web and box base, nylon washers; lid faces down",
       elev=-25, azim=-60, label_done=False)
    st(12, [gtop(M["pins"]), M["clamps"], M["sensor"]], [mv(part("Guard with the reader box under it, and pegs", win(S(GA, "guard", "pegs", "reader", "reader_screws", "reader_fitting"), -800, 800, -400, 400, -150, 1200), COL["guard"]), (0, 0, 450))],
       "guard over the gauge",
       "Plug the sensor lead into the reader; lower the guard on its feet; four pegs on the upslope half only",
       elev=18, azim=-60, label_done=False)
    mast_only = part("Mast, footing, cap, earth rod and bond", S(MA, "mast_pipe", "footing", "mast_cap", "earth_rod", "bond_clamps", "bond"), COL["mast"])
    st(13, [part("Concrete footing", MA["footing"].shape, COL["footing"])],
       [mv(part("Mast pipe and cap", S(MA, "mast_pipe", "mast_cap"), COL["mast"]), (0, 0, 800)),
        mv(part("Earth rod, clamps and bond", S(MA, "earth_rod", "bond_clamps", "bond"), COL["earth"]), (0, 0, 600))],
       "mast and earth rod (site option)",
       "Mast plumb in the wet footing, braced for 3 days; drive the earth rod 450 mm away; clamp the bond",
       elev=12, azim=-60, size=(8, 7))
    node = part("FieldNode core", S(MA, "node", "node_plate", "node_vblocks", "node_bands"), COL["node"])
    lo, hi = P["node_z0"] - 400, P["node_z0"] + 700
    mast_w = part("Mast or pole", win(S(MA, "mast_pipe"), -60, 60, -60, 60, lo, hi), COL["mast"])
    st(14, [mast_w], [mv(node, (0, -350, 0))], "FieldNode core onto the pole",
       f"Built and checked to FieldNode's own plan; V-blocks on the pole, two band clamps; node bottom {P['node_z0']:,.0f} mm up",
       elev=15, azim=-55, label_done=True)
    hb = D["alert_plate_z0"]
    aplate = part("Back plate and V-blocks", S(MA, "alert_plate", "alert_vblocks"), COL["aplate"])
    abox = part("Alert box with horn, beacon and glands", S(MA, "alert_box", "alert_nuts", "horn", "beacon", "alert_glands"), COL["abox"])
    st(15, [aplate], [mv(abox, (0, -250, 0))], "alert box onto its back plate (on the bench)",
       "V-blocks on the back with M4 countersunk screws; box through its corner holes, four M5 screws, nyloc nuts behind",
       elev=15, azim=-55, label_done=True)
    mtop = part("Mast or pole top", win(S(MA, "mast_pipe", "mast_cap"), -60, 60, -60, 60, hb - 500, P["mast_h"] + 20), COL["mast"])
    st(16, [mtop], [mv(part("Alert unit", S(MA, "alert_plate", "alert_vblocks", "alert_box", "alert_nuts", "horn", "beacon", "alert_glands"), COL["abox"]), (0, -350, 0)),
                    mv(part("Band clamps (2)", MA["alert_bands"].shape, COL["band"]), (0, 300, 0))],
       "alert unit onto the pole",
       "Siren at least 3 m above ground; bands round the pole and through the slots; horn facing the work area",
       elev=15, azim=-55, label_done=True, size=(8, 7))
    st(17, [], [mv(part("Switch post", SW["post"].shape, COL["post"]), (0, 0, 500)),
                mv(part("Post cap", SW["post_cap"].shape, COL["endcap"]), (0, 0, 900))],
       "drive the switch post", "About 5 m from the mast, away from the horn; drive 500 mm to the ground mark; cap on",
       elev=12, azim=-60)
    st(18, [part("Switch post (top part)", win(S(SW, "post", "post_cap"), -60, 60, -60, 60, 1050, 1450), COL["post"])], [mv(part("Back plate with keyed switch box", S(SW, "switch_plate", "switch_box", "switch_gland", "switch_key"), COL["sbox"]), (0, -200, 0)),
                         mv(part("Hose clips (2)", SW["switch_bands"].shape, COL["band"]), (0, 150, 0))],
       "switch box onto its post", f"Box on the plate (four M4 screws); plate on the post, box centre {P['switch_z']:,.0f} mm up; two hose clips",
       elev=15, azim=-55, label_done=False, size=(8, 7))
    return out


# ----------------------------------------------------------------- bus and site figures
def bus():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    RED, BLU, GRY, ORA = "#B91C1C", "#1D4ED8", "#6B7280", "#C2410C"
    ax.text(2, 70, "SlopeWatch prototype: bus and alert wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "One four-core cable runs from the crack gauge reader through each stake head to FieldNode port A. "
            "Joins are lever connectors inside each head.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/slopewatch", fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.8, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.1, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    # sensor chain along the top
    ys, h = 44, 13
    xs = [2, 24, 46, 68]
    blk(xs[0], ys, 17, h, "Crack gauge reader", "under the guard;\nsensor lead in by\nM12 gland", "#0E7490")
    for i, x in enumerate(xs[1:], 1):
        blk(x, ys, 17, h, f"Stake {i} head", "capsule lead joined\nto bus in and out\n(lever connectors)", "#CA8A04")
    blk(92, 38, 25, 21, "FieldNode core", "built to its own plan\nM12 5-pin, field-wired plugs\nport A: 5 V rail, bus\nport B: 12 V rail, alert", "#1E3A8A")
    for x0, x1 in zip(xs[:-1], xs[1:]):
        ax.annotate("", xy=(x1, ys + 6), xytext=(x0 + 17.6, ys + 6), arrowprops=dict(arrowstyle="-", color=INK, lw=2.4))
    ax.plot([85.6, 92], [ys + 6, ys + 6], color=INK, lw=2.4)
    for x0 in (19.3, 41.3, 63.3):
        ax.text(x0 + 2.4, ys + 7.8, "conduit", fontsize=6.6, color=MUT, ha="center")
    ax.text(88.8, ys + 7.8, "surge\nprotector", fontsize=6.6, color=MUT, ha="center")
    # core table
    ax.text(4, 37, "Bus cable: four-core shielded outdoor cable, 0.5 mm2, in 20 mm corrugated conduit, about 60 m in all.", fontsize=8, color=INK)
    rows = [("Red", "+5 V", "port A pin 1; switched on 12 s every 10 min", RED),
            ("Blue", "RS-485 A", "port A pin 2; twisted pair with B", BLU),
            ("Black", "0 V", "port A pin 3; the shield joins 0 V at the node end only", INK),
            ("White", "RS-485 B", "port A pin 4; 120 ohm terminator at the node and at the reader", GRY)]
    for i, (c, f, n, col) in enumerate(rows):
        y = 33 - i * 3.1
        ax.add_patch(plt.Rectangle((4, y - 0.9), 3, 1.8, color=col))
        ax.text(8.2, y, c, fontsize=7.8, color=INK, va="center")
        ax.text(15, y, f, fontsize=7.8, color=INK, va="center", fontweight="bold")
        ax.text(24, y, n, fontsize=7.8, color=MUT, va="center")
    # alert side
    blk(92, 8, 25, 18, "Alert box", "MOSFET driver: siren and\nbeacon; port B (12 V):\npin 1 12 V, pin 3 0 V,\npin 5 keyed switch input", ORA)
    ax.annotate("", xy=(104.5, 26.6), xytext=(104.5, 37.6), arrowprops=dict(arrowstyle="-", color=ORA, lw=2.2))
    ax.text(105.5, 32, "port B lead, 12 V\n(down the pole\nin cable ties)", fontsize=6.8, color=ORA, va="center")
    blk(62, 8, 22, 12, "Keyed switch box", "on its own post about\n5 m away; 7 m lead\nin conduit, 2 x 0.5 mm2", ORA)
    ax.plot([84.6, 92], [14, 14], color=ORA, lw=2.2)
    ax.text(4, 15.5, "Switch contact to port B pin 5 (keyed switch input); pins 2 and 4 of port B are unused.",
            fontsize=7.6, color=MUT)
    ax.text(4, 11.6, "Order of joins in a stake head: bus in, bus out and capsule lead, colour to colour,\n"
            "one lever connector per core. Label every cable end with its stake number.", fontsize=7.6, color=MUT, linespacing=1.4)
    ax.text(4, 6.2, "Safety: all wiring is extra-low voltage (5 V and 12 V). Connect port B last, with the siren muted by the keyed switch.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    out = OUT / "bus.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def site():
    import math
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    s = SITE
    th = math.radians(s["slope_deg"])
    fig = plt.figure(figsize=(12, 6.2), dpi=150)
    ax = fig.add_axes([0.04, 0.12, 0.92, 0.72]); ax.set_aspect("equal"); ax.set_axis_off()
    # side section along the fall line, horizontal distance from the crack
    gx = 0.0
    xs1 = gx + s["gauge_to_stake1_m"] * math.cos(th)
    stakes = [xs1 + i * s["stake_spacing_m"] * math.cos(th) for i in range(3)]
    toe = stakes[-1] + s["stake3_to_toe_m"] * math.cos(th)
    mx = toe + s["toe_to_mast_m"]
    zf = lambda x: (toe - min(x, toe)) * math.tan(th)  # noqa: E731
    xg = [-6, toe, mx + 9]
    ax.fill_between([-6, toe, mx + 9], [zf(-6), 0, 0], -2.5, color="#E7E5E4", zorder=0)
    ax.plot(xg, [zf(-6), 0, 0], color=INK, lw=1.2)
    ax.plot([gx, gx], [zf(gx), zf(gx) - 1.2], color="#7C3AED", lw=1)
    ax.text(gx, zf(gx) + 1.2, "crack gauge\nacross the crest crack", ha="center", fontsize=8, color="#7C3AED")
    for i, x in enumerate(stakes, 1):
        ax.plot([x, x], [zf(x) - 0.8, zf(x) + 0.33], color=INK, lw=2.2)
        ax.text(x + 0.4, zf(x) + 0.9, f"stake {i}", fontsize=8, color=INK)
    ax.plot([mx, mx], [0, 3.2], color=INK, lw=2)
    ax.add_patch(plt.Rectangle((mx - 0.25, 1.75), 0.5, 0.2, color="#1E3A8A"))
    ax.add_patch(plt.Rectangle((mx - 0.2, 3.2), 0.4, 0.3, color="#C2410C"))
    ax.text(mx - 0.6, 1.85, "FieldNode", fontsize=8, color="#1E3A8A", va="center", ha="right")
    ax.text(mx - 0.6, 3.35, "alert unit, siren 3.2 m up", fontsize=8, color="#C2410C", va="center", ha="right")
    ax.text(mx, 3.8, "existing pole (or the mast option)", ha="center", va="bottom", fontsize=8, color=INK)
    sx = mx + 5
    ax.plot([sx, sx], [0, 1.4], color=INK, lw=1.4)
    ax.text(sx, 1.7, "keyed switch post\nabout 5 m from the pole", ha="center", fontsize=8, color="#C2410C")
    # conduit run
    pts = [(gx, zf(gx))] + [(x, zf(x)) for x in stakes] + [(toe, 0), (mx, 0)]
    ax.plot([p[0] for p in pts], [p[1] + 0.12 for p in pts], color=AC, lw=1.4, ls="--")
    ax.plot([mx, sx], [0.08, 0.08], color="#C2410C", lw=1.2, ls=":")
    ax.text((toe + mx) / 2, 0.55, "bus conduit on the surface, pegged every 1 m", fontsize=8, color=AC, ha="center")
    # dimensions
    yd = -2.0
    marks = [gx] + stakes + [toe, mx]
    labels = [f"{s['gauge_to_stake1_m']:.0f} m", f"{s['stake_spacing_m']:.0f} m", f"{s['stake_spacing_m']:.0f} m",
              f"{s['stake3_to_toe_m']:.0f} m", f"{s['toe_to_mast_m']:.0f} m"]
    for (a_, b_), lab in zip(zip(marks[:-1], marks[1:]), labels):
        ax.annotate("", xy=(a_, yd), xytext=(b_, yd), arrowprops=dict(arrowstyle="<->", color=MUT, lw=0.8))
        ax.text((a_ + b_) / 2, yd - 0.55, lab, ha="center", va="top", fontsize=8, color=MUT)
    ax.text(-6, yd - 0.55, "along the slope:", ha="left", va="top", fontsize=8, color=MUT)
    ax.set_xlim(-7, mx + 10); ax.set_ylim(-3.6, max(zf(-6) + 2.5, 5.0))
    fig.text(0.03, 0.96, "Reference site: where each part goes", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.915, f"Section down the fall line of a {s['slope_deg']:.0f} degree face, drawn to scale. "
             f"Bus cable about {D['cable_m']:.0f} m with slack and drip loops. Never work below an actively moving face.",
             fontsize=8.5, color=MUT, va="top")
    fig.text(0.03, 0.02, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.02, "github.com/BoujeeEnjinia1701/slopewatch", fontsize=7, color=AC, ha="right", family="monospace")
    out = OUT / "site.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "bus": bus, "site": site}
    args = sys.argv[1:] or list(fns)
    i = 0
    while i < len(args):
        w = args[i]; i += 1
        nums = []
        while i < len(args) and args[i].isdigit():
            nums.append(int(args[i])); i += 1
        r = fns[w](set(nums)) if nums else fns[w]()
        print(w, "->", r)
