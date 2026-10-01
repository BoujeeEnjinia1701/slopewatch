"""SlopeWatch parametric model (build123d), TRL 3, constructable design (SLW-DDR-003).

Run from the repo root:  python cad/src/model.py            export STEP and STL, print the checks
                         python cad/src/model.py --check    print the constructability checks only
Exports STEP and STL into cad/step and cad/stl:
    slopewatch-stake.step / .stl         one tilt stake (items 1 to 3, bus lead, stand tube, collars, foam plug)
    slopewatch-crack-gauge.step / .stl   crack displacement gauge with reader box and guard (item 4)
    slopewatch-mast.step / .stl          mast, footing, earth rod, FieldNode massing and the alert unit (items 6 to 8)
    slopewatch-switch-post.step / .stl   keyed silence switch on its own post, about 5 m from the mast (item 7)
    slopewatch-arrangement.step / .stl   the four assemblies side by side on level ground (drawing SLW-DWG-001)

Axes: Z is up and the local ground surface at each assembly is z = 0. Each assembly is built on
its own axis at x = y = 0. On a site, +X points downslope. The FieldNode core and the alert unit
face -Y. The FieldNode core is massing only, sized from the FieldNode constructable design
(FND-DDR-003: back plate, V-blocks, band clamps, enclosure, panel); FieldNode is the source of
truth for its own geometry and is built to its own plan (FND-BLD-001).

build_components() returns every component as a Comp(name, shape, bom, group); the grouping
functions stake(), crack_gauge(), mast(), switch_post() keep the keys the media scripts use.
checks() tests that parts which must touch do touch and parts which must not touch are apart.
The same PARAMS feed docs/04-calcs/sizing.py (SLW-CAL-001), the drawing SLW-DWG-001
(cad/src/sheets.py), the build plan pictures (cad/src/build_plan_media.py) and the concept media.
"""
import math
import sys
from collections import namedtuple
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 tilt stake: galvanized pipe OD x wall, total length, length below ground (pipe bottom at -embed)
    "pipe": (48.3, 3.2), "pipe_l": 1000.0, "embed": 800.0,
    #   screwed malleable-iron end cap on the threaded bottom end: OD, height, floor thickness
    "pipe_cap": (60.0, 28.0, 9.0),
    #   grout column: augered hole diameter and grout height above the pipe bottom; grout base below the cap
    "grout_d": 110.0, "grout_l": 450.0, "grout_base": 20.0,
    # 2 sensor capsule: tube OD x length; depth of the capsule center below ground (0.4 m, SLW-CAL-001 B);
    #   foam plug above it (plug_l); since SLW-DDR-003 a PVC stand tube (OD, wall) below it sets the depth,
    #   and two printed centring collars (OD, length) hold the capsule on the pipe axis
    "capsule": (34.0, 130.0), "capsule_depth": 400.0, "plug_l": 80.0,
    "stand": (40.0, 2.0), "collar": (41.5, 15.0),
    # 3 stake head (SLW-DDR-003): 110 x 50 mm PVC drainage reducer (50 socket ID, OD), 110 mm pipe
    #   (wall), 110 mm end cap (OD). Head OD x height above its underside, overlap of the socket on the pipe;
    #   two M20 conduit fittings for 20 mm conduit, upslope (bus in) and downslope (bus out)
    "head": (110.0, 170.0), "head_overlap": 40.0, "socket": (50.2, 56.0), "head_wall": 3.2, "head_cap_d": 116.0,
    "gland": (28.0, 40.0), "fitting": (28.0, 25.0, 30.0), "conduit": (20.0, 14.0),
    # 4 crack gauge: anchor spacing across the crack, pin OD, pin length, pin depth below ground,
    #   sensor axis height, sensor body OD x length (100 mm stroke), plunger out at installation,
    #   clamp block (W x D x H), ball joint radius, extension rod OD; guard (L x W x H, sheet t, foot width),
    #   reader box (L x W x H), ground pegs (OD x length)
    "anchor_span": 900.0, "pin_d": 20.0, "pin_l": 700.0, "pin_embed": 500.0,
    "gauge_z": 110.0, "gauge_body": (25.0, 260.0), "stroke": 100.0, "plunger_out": 15.0,
    "clamp": (40.0, 40.0, 60.0), "ball_r": 7.0, "rod_d": 8.0,
    "guard": (1150.0, 200.0, 250.0, 1.5, 25.0), "reader": (80.0, 60.0, 45.0), "peg": (8.0, 300.0),
    # 8 mast: pipe OD x wall, height above ground, footing diameter x depth, earth rod (dia, length, offset)
    "mast": (48.3, 3.2), "mast_h": 3200.0, "footing": (320.0, 600.0), "earth_rod": (16.0, 1200.0, 450.0),
    # 6 FieldNode core (massing from the FieldNode constructable design, FND-DDR-003): enclosure W x D x H,
    #   bottom height, back plate back-face offset from the pole axis, back plate (W x H x t), panel
    #   (X x slope x t), tilt, panel center (y, z above node bottom), band slot offset
    "node": (150.0, 90.0, 200.0), "node_z0": 1750.0, "node_plate_y0": -42.0, "node_plate": (180.0, 320.0, 3.0),
    "panel": (290.0, 200.0, 17.0), "panel_tilt": 40.0, "panel_c": (-115.0, 385.0), "node_slot_x": 51.0,
    # pole mounting shared by the node and the alert unit (FND-DDR-003): V-block W x D x H; band width x t
    "vblock": (60.0, 33.0, 20.0), "band": (12.0, 1.0),
    # 7 alert unit (SLW-DDR-003): side-mounted on the pole or mast on its own back plate (W x H x t) with two
    #   V-blocks and two band clamps; plate bottom below the mast top; alert box (W x D x H) on the plate
    #   holding the driver, horn on its front (dia x length, faces -Y), beacon on its top (dia x height);
    #   band slot offset
    "alert_plate": (160.0, 360.0, 3.0), "alert_drop": 250.0, "alert_box": (120.0, 90.0, 120.0),
    "siren_box": 120.0, "horn": (110.0, 140.0), "beacon": (110.0, 220.0), "alert_slot_x": 60.0,
    # keyed silence switch box (W x D x H) and center height; on its own post (OD x wall, height above
    #   ground, length driven in) about 5 m from the mast on the +Y side, on a lead in conduit; since
    #   SLW-DDR-003 the box sits on a back plate (W x H x t) held to the post by two hose clips
    "switch_box": (100.0, 60.0, 70.0), "switch_z": 1300.0, "switch_plate": (100.0, 160.0, 3.0), "switch_slot_x": 26.0,
    "switch_post": (26.9, 2.6, 1400.0, 500.0), "switch_offset": 5000.0, "switch_lead_m": 7.0,
    # layout of the arrangement drawing (x of each assembly axis on level ground; not site spacing)
    "arr_x": (0.0, 1300.0, 2900.0, 4400.0),
}

# Reference site layout used by the calculations (m); the media scene compresses these distances
SITE = {
    "slope_deg": 25.0,            # face angle
    "stake_spacing_m": 10.0,      # along the fall line between stakes
    "gauge_to_stake1_m": 8.0,     # crest crack gauge to the top stake (cable run)
    "stake3_to_toe_m": 5.0,
    "toe_to_mast_m": 15.0,        # mast set back from the toe, clear of runout
    "riser_m": 1.8,               # cable up the mast to the node port
    "drip_loop_m": 1.0,           # per stake and at the gauge
    "slack": 0.10,                # 10 % for routing around obstacles
}

BOM = {  # model key: (BOM line, name)
    "stake": (1, "Tilt stake, pipe and grout"),
    "capsule": (2, "Tilt sensor capsule"),
    "head": (3, "Stake head with conduit fittings"),
    "gauge": (4, "Crack displacement gauge with reader"),
    "cable": (5, "Sensor bus cable in conduit"),
    "node": (6, "FieldNode core (massing)"),
    "alert": (7, "Siren and beacon alert unit"),
    "switch": (7, "Keyed silence switch on its own post"),
    "mast": (8, "Mast, footing and earth rod"),
}

Comp = namedtuple("Comp", "name shape bom group")


def derived(p=PARAMS, s=SITE):
    """Dimensions the calc note, the drawing and the build plan quote, computed from PARAMS and SITE."""
    od, t = p["pipe"]
    idia = od - 2 * t
    cap_top = -p["capsule_depth"] + p["capsule"][1] / 2
    cap_bot = -p["capsule_depth"] - p["capsule"][1] / 2
    fall_m = 2 * s["stake_spacing_m"]
    cable = (s["gauge_to_stake1_m"] + fall_m + s["stake3_to_toe_m"] + s["toe_to_mast_m"] + s["riser_m"]
             + 4 * s["drip_loop_m"])
    cod, ch, cfl = p["pipe_cap"]
    cap_bottom = -p["embed"] - cfl                      # underside of the screwed end cap
    hole_bot = cap_bottom - p["grout_base"]
    gr = p["grout_d"] / 2
    grout_vol = (math.pi * gr ** 2 * (-p["embed"] + p["grout_l"] - hole_bot)
                 - math.pi * (cod / 2) ** 2 * ch - math.pi * (od / 2) ** 2 * (p["grout_l"] - (ch - cfl))) / 1e6
    a = p["anchor_span"] / 2
    cw = p["clamp"][0]
    ball_c = a - cw / 2 - 10 - p["ball_r"]              # ball centres, measured from the crack line
    body_x0 = -ball_c + p["ball_r"] + 8                 # sensor body starts after the upslope rod end shank
    body_x1 = body_x0 + p["gauge_body"][1]
    plunger_x1 = body_x1 + p["plunger_out"]
    coupling_x1 = plunger_x1 + 20
    rod_x1 = ball_c - p["ball_r"] - 8
    H = p["mast_h"]
    hb = H - p["alert_drop"]
    aw, ad, ah = p["alert_box"]
    box_z0 = hb + 220
    return {
        "pipe_id": idia,
        "pipe_area_mm2": math.pi / 4 * (od ** 2 - idia ** 2),
        "stake_top": p["pipe_l"] - p["embed"],
        "head_bot": p["pipe_l"] - p["embed"] - p["head_overlap"],
        "head_top": p["pipe_l"] - p["embed"] + p["head"][1] - p["head_overlap"],
        "cap_top": cap_top, "cap_bot": cap_bot,
        "stand_l": cap_bot + p["embed"],
        "endcap_bot": cap_bottom, "hole_bot": hole_bot, "hole_depth": -hole_bot,
        "grout_top": -p["embed"] + p["grout_l"],
        "grout_vol_l": grout_vol,
        "hole_vol_l": math.pi * gr ** 2 * (-hole_bot) / 1e6,
        "ball_c": ball_c, "body_x0": body_x0, "body_x1": body_x1, "plunger_x1": plunger_x1,
        "coupling_x1": coupling_x1, "rod_x1": rod_x1, "rod_l": rod_x1 - coupling_x1,
        "mast_top": H,
        "alert_plate_z0": hb, "alert_box_z0": box_z0, "siren_z": box_z0 + ah / 2,
        "alert_top": box_z0 + ah + p["beacon"][1],
        "alert_zc": box_z0 + (ah + p["beacon"][1]) / 2,
        "node_zc": p["node_z0"] + p["node"][2] / 2,
        "panel_cz": p["node_z0"] + p["panel_c"][1],
        "cable_m": cable * (1 + s["slack"]),
        "cable_m_net": cable,
        "fall_m": fall_m,
        "rise_m": fall_m * math.sin(math.radians(s["slope_deg"])),
    }


# ------------------------------------------------------------------ primitives
def _b():
    import build123d as b
    return b


def zcyl(x, y, z0, z1, r):
    b = _b()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)


def ztube(x, y, z0, z1, ro, ri):
    return zcyl(x, y, z0, z1, ro) - zcyl(x, y, z0 - 1, z1 + 1, ri)


def xcyl(x0, x1, y, z, r):
    b = _b()
    return b.Pos((x0 + x1) / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, abs(x1 - x0))


def ycyl(x, y0, y1, z, r):
    b = _b()
    return b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, abs(y1 - y0))


def bx(x0, x1, y0, y1, z0, z1):
    b = _b()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def rod(p1, p2, r):
    """Round bar between two points (massing)."""
    b = _b()
    v = [p2[i] - p1[i] for i in range(3)]
    L = math.sqrt(sum(c * c for c in v))
    return b.Solid.make_cylinder(r, L, b.Plane(origin=p1, z_dir=tuple(c / L for c in v)))


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _hull(pts):
    pts = sorted(set((round(x, 6), round(y, 6)) for x, y in pts))

    def cross(o, a, b_):
        return (a[0] - o[0]) * (b_[1] - o[1]) - (a[1] - o[1]) * (b_[0] - o[0])
    lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def _hull_prism(pts, z0, z1):
    b = _b()
    face = b.Polygon(*_hull(pts), align=None)
    return b.Pos(0, 0, z0) * b.extrude(face, z1 - z0)


def band_clamp(R, y_front, slot_x, zc, w=12.0, t=1.0, n=144):
    """A worm-drive band round a pole of radius R (axis at the origin), through two slots in a plate
    whose front face is at y_front (< 0), and across the plate front. Polygon circles are
    circumscribed so the band never cuts into the pole."""
    k = 1 / math.cos(math.pi / n)
    circ = lambda r: [(r * k * math.cos(2 * math.pi * i / n), r * k * math.sin(2 * math.pi * i / n)) for i in range(n)]  # noqa: E731
    outer = circ(R + t) + [(slot_x + t / 2, y_front - t), (-slot_x - t / 2, y_front - t)]
    inner = circ(R) + [(slot_x - t / 2, y_front), (-slot_x + t / 2, y_front)]
    return _hull_prism(outer, zc - w / 2, zc + w / 2) - _hull_prism(inner, zc - w / 2 - 1, zc + w / 2 + 1)


def vblock(R, y_back, zc, p=PARAMS):
    """V-block on the back of a plate (back face at y_back < 0), 90 degree V seating a pole of radius R."""
    b = _b()
    w, d, h = p["vblock"]
    blk = bx(-w / 2, w / 2, y_back, y_back + d, zc - h / 2, zc + h / 2)
    y_pt = -R * math.sqrt(2)
    s = 80.0
    cut = b.Pos(0, y_pt + s / math.sqrt(2), zc) * b.Rot(0, 0, 45) * b.Box(s, s, h + 4)
    return blk - cut


# ------------------------------------------------------------------ components
def stake_components(p=PARAMS):
    """One tilt stake with its ground surface at z = 0."""
    d = derived(p)
    od, t = p["pipe"]
    ro, ri = od / 2, d["pipe_id"] / 2
    zb = -p["embed"]
    top = d["stake_top"]
    C = {}
    # 1: pipe with two 4.2 mm screw holes for the head, and the screwed end cap
    sz = d["head_bot"] + 20
    holes = ycyl(0, -40, 40, sz, 2.5)
    C["pipe"] = Comp("Stake pipe", ztube(0, 0, zb, top, ro, ri) - holes, 1, "stake")
    cod, ch, cfl = p["pipe_cap"]
    cz0 = zb - cfl
    C["endcap"] = Comp("Screwed end cap", zcyl(0, 0, cz0, cz0 + ch, cod / 2) - zcyl(0, 0, zb, cz0 + ch + 1, ro), 1, "stake")
    gr = p["grout_d"] / 2
    C["grout"] = Comp("Grout column", zcyl(0, 0, d["hole_bot"], d["grout_top"], gr)
                      - zcyl(0, 0, cz0, cz0 + ch, cod / 2) - zcyl(0, 0, cz0 + ch - 1, d["grout_top"] + 1, ro), 1, "stake")
    # 2: stand tube, collars, capsule, foam plug, lead
    so, sw = p["stand"]
    C["stand"] = Comp("Stand tube", ztube(0, 0, zb, d["cap_bot"], so / 2, so / 2 - sw), 1, "stake")
    cd, cl = p["capsule"]
    C["capsule"] = Comp("Tilt sensor capsule", zcyl(0, 0, d["cap_bot"], d["cap_top"], cd / 2), 2, "stake")
    kd, kl = p["collar"]
    C["collars"] = Comp("Centring collars (2)", ztube(0, 0, d["cap_bot"], d["cap_bot"] + kl, kd / 2, cd / 2)
                        + ztube(0, 0, d["cap_top"] - kl, d["cap_top"], kd / 2, cd / 2), 2, "stake")
    lead_r = 3.0
    lead_top = top + 50
    C["lead"] = Comp("Capsule lead", zcyl(0, 0, d["cap_top"], lead_top, lead_r), 2, "stake")
    pz0 = d["cap_top"] + 10
    C["plug"] = Comp("Foam plug", ztube(0, 0, pz0, pz0 + p["plug_l"], ri, lead_r), 10, "stake")
    # 3: head, from bought PVC drainage fittings
    sid, sod = p["socket"]
    hb = d["head_bot"]
    hr = p["head"][0] / 2
    hw = p["head_wall"]
    b = _b()
    cone_o = b.Pos(0, 0, top + 15) * b.Cone(sod / 2, hr + 3, 30)
    cone_i = b.Pos(0, 0, top + 15) * b.Cone(sid / 2, hr - hw, 30.01)
    red = (ztube(0, 0, hb, top, sod / 2, sid / 2) + (cone_o - cone_i)
           + ztube(0, 0, top + 30, top + 55, hr + 3, hr) + ztube(0, 0, top + 30, top + 33, hr, hr - hw))
    C["reducer"] = Comp("Reducer 110 to 50 mm", red - holes, 3, "stake")
    C["tape"] = Comp("Tape wrap", ztube(0, 0, hb + 5, top - 5, sid / 2, ro) - holes, 10, "stake")
    ht = d["head_top"]
    C["headtube"] = Comp("Head tube 110 mm", ztube(0, 0, top + 33, ht - 3, hr, hr - hw), 3, "stake")
    cap_r = p["head_cap_d"] / 2
    C["headcap"] = Comp("Head end cap", zcyl(0, 0, ht - 3, ht, cap_r) + ztube(0, 0, ht - 28, ht - 3, cap_r, hr), 3, "stake")
    fz = (top + 55 + ht - 28) / 2
    fd, fb, fl = p["fitting"]
    fit, cond = None, None
    co, ci = p["conduit"]
    for sg in (-1, 1):
        x_out = math.sqrt(hr ** 2 - 0) * sg
        fl_ = xcyl(x_out, x_out + sg * 3, 0, fz, fd / 2)
        body = xcyl(x_out + sg * 3, x_out + sg * (3 + fl), 0, fz, fb / 2) - xcyl(x_out, x_out + sg * (4 + fl), 0, fz, co / 2)
        xin = sg * math.sqrt((hr - hw) ** 2 - 14.0 ** 2)              # inner wall where the nut's rim bears
        thread = xcyl(xin - sg * 5, x_out, 0, fz, 9.5)
        nut = xcyl(xin, xin - sg * 5, 0, fz, 14.0) - xcyl(xin + sg, xin - sg * 6, 0, fz, 9.5)
        f = fl_ + body + thread + nut
        fit = f if fit is None else fit + f
        cdt = xcyl(x_out + sg * (3 + fl - 15), x_out + sg * (3 + fl + 90), 0, fz, co / 2) - xcyl(0, sg * 400, 0, fz, ci / 2)
        cond = cdt if cond is None else cond + cdt
    C["headtube"] = Comp("Head tube 110 mm", C["headtube"].shape - xcyl(-80, 80, 0, fz, 9.5), 3, "stake")
    C["fittings"] = Comp("Conduit fittings (2)", fit, 3, "stake")
    C["conduit_st"] = Comp("Conduit, bus in and out", cond, 5, "stake")
    # two M5 self-tapping screws through the socket into the pipe, on the +Y and -Y sides
    scr = None
    for sg in (-1, 1):
        s_ = ycyl(0, sg * (ri + 0.5), sg * sod / 2, sz, 2.5) + ycyl(0, sg * sod / 2, sg * (sod / 2 + 3.5), sz, 4.5)
        scr = s_ if scr is None else scr + s_
    C["screws"] = Comp("Head screws (2)", scr, 10, "stake")
    return C


def gauge_components(p=PARAMS):
    """Crack gauge centered on the crack line (x = 0), ground at z = 0; upslope anchor at -X."""
    d = derived(p)
    a = p["anchor_span"] / 2
    r = p["pin_d"] / 2
    zpb, zpt = -p["pin_embed"], -p["pin_embed"] + p["pin_l"]
    b = _b()
    pin = lambda x: zcyl(x, 0, zpb + 30, zpt, r) + b.Pos(x, 0, zpb + 15) * b.Cone(2, r, 30)  # noqa: E731
    C = {}
    C["pins"] = Comp("Anchor pins (2)", pin(-a) + pin(a), 4, "gauge")
    gz = p["gauge_z"]
    cw, cdp, chh = p["clamp"]
    blocks, screws, studs, balls = None, None, None, None
    for sg in (-1, 1):
        x = sg * a
        blk = bx(x - cw / 2, x + cw / 2, -cdp / 2, cdp / 2, gz - chh / 2, gz + chh / 2) - zcyl(x, 0, gz - chh, gz + chh, r + 0.25)
        ss = xcyl(x + sg * r, x + sg * (cw / 2 + 6), 0, gz + 15, 4.0)   # M8 set screw from the outer end face
        blk = blk - xcyl(x, x + sg * (cw / 2 + 1), 0, gz + 15, 4.0)
        face = x - sg * cw / 2                                         # face toward the crack
        st = xcyl(face, face - sg * 10, 0, gz, 3.0)                   # stud, 10 mm out of the block
        hole = xcyl(face, face + sg * 10, 0, gz, 3.0)
        blk = blk - hole
        stud_in = xcyl(face, face + sg * 10, 0, gz, 3.0)
        bc = sg * d["ball_c"]
        ball = b.Pos(bc, 0, gz) * b.Sphere(p["ball_r"]) + xcyl(bc, bc - sg * (p["ball_r"] + 8), 0, gz, 4.0)
        blocks = blk if blocks is None else blocks + blk
        screws = ss if screws is None else screws + ss
        sstud = st + stud_in
        studs = sstud if studs is None else studs + sstud
        balls = ball if balls is None else balls + ball
    C["clamps"] = Comp("Clamp blocks (2)", blocks, 4, "gauge")
    C["setscrews"] = Comp("Set screws (2)", screws, 4, "gauge")
    C["studs"] = Comp("Ball-joint studs (2)", studs, 4, "gauge")
    C["balls"] = Comp("Rod-end ball joints (2)", balls, 4, "gauge")
    bd, bl = p["gauge_body"]
    C["sensor"] = Comp("Displacement sensor", xcyl(d["body_x0"], d["body_x1"], 0, gz, bd / 2)
                       + xcyl(d["body_x1"], d["plunger_x1"], 0, gz, 3.0), 4, "gauge")
    hexc = b.Pos((d["plunger_x1"] + d["coupling_x1"]) / 2, 0, gz) * b.Rot(0, 90, 0) * b.extrude(
        b.RegularPolygon(6.0, 6), 10, both=True)
    C["coupling"] = Comp("Coupling", hexc, 4, "gauge")
    C["rod"] = Comp("Extension rod", xcyl(d["coupling_x1"], d["rod_x1"], 0, gz, p["rod_d"] / 2), 4, "gauge")
    # guard: folded inverted channel with foot flanges, pegged down on the upslope half only
    gl, gw, gh, gt, gf = p["guard"]
    web = bx(-gl / 2, gl / 2, -gw / 2, gw / 2, gh - gt, gh)
    legs = bx(-gl / 2, gl / 2, gw / 2 - gt, gw / 2, 0, gh) + bx(-gl / 2, gl / 2, -gw / 2, -gw / 2 + gt, 0, gh)
    feet = bx(-gl / 2, gl / 2, gw / 2, gw / 2 + gf, 0, gt) + bx(-gl / 2, gl / 2, -gw / 2 - gf, -gw / 2, 0, gt)
    pg_d, pg_l = p["peg"]
    peg_xy = [(x, sg * (gw / 2 + gf / 2)) for x in (-gl / 2 + 40, -120.0) for sg in (-1, 1)]
    guard = web + legs + feet
    pegs = None
    for x, y in peg_xy:
        guard = guard - zcyl(x, y, -1, gt + 1, pg_d / 2)
        pg = zcyl(x, y, gt - pg_l + 20, gt, pg_d / 2) + zcyl(x, y, gt, gt + 4, 8.0)
        pegs = pg if pegs is None else pegs + pg
    rl, rw, rh = p["reader"]
    ry0 = 22.0
    reader = bx(-a - rl / 2, -a + rl / 2, ry0, ry0 + rw, gh - gt - rh, gh - gt)
    rs = None
    for x in (-a - 25, -a + 25):
        s_ = zcyl(x, ry0 + rw / 2, gh - gt - 8, gh, 2.0) + zcyl(x, ry0 + rw / 2, gh, gh + 3, 4.0)
        guard = guard - zcyl(x, ry0 + rw / 2, gh - gt - 1, gh + 1, 2.0)
        reader = reader - zcyl(x, ry0 + rw / 2, gh - gt - 9, gh, 2.0)
        rs = s_ if rs is None else rs + s_
    C["guard"] = Comp("Guard", guard, 4, "gauge")
    C["pegs"] = Comp("Ground pegs (4)", pegs, 4, "gauge")
    C["reader"] = Comp("Reader box", reader, 4, "gauge")
    C["reader_screws"] = Comp("Reader screws (2)", rs, 4, "gauge")
    # reader conduit fitting on the bottom face, conduit down to the ground and out of the downslope end
    rg = xcyl(-a + rl / 2, -a + rl / 2 + 25, ry0 + rw / 2, gh - gt - rh / 2, 12.5)
    C["reader_fitting"] = Comp("Reader conduit fitting (downslope end)", rg, 4, "gauge")
    return C


def _node_components(p=PARAMS):
    """FieldNode core massing on the pole (axis at the origin), from FND-DDR-003."""
    od = p["mast"][0]
    R = od / 2
    nw, nd, nh = p["node"]
    pw, ph, pt = p["node_plate"]
    y0 = p["node_plate_y0"]
    yf = y0 - pt
    z0 = p["node_z0"]
    zb = z0 - 40
    clamps = (zb + 20, zb + 270)
    sx = p["node_slot_x"]
    plate = bx(-pw / 2, pw / 2, yf, y0, zb, zb + ph)
    for zc in clamps:
        for sg in (-1, 1):
            plate = plate - bx(sg * sx - 3.0, sg * sx + 3.0, yf - 1, y0 + 1, zc - 7.5, zc + 7.5)
    enc = bx(-nw / 2, nw / 2, yf - nd, yf, z0, z0 + nh)
    b = _b()
    px, pl, pth = p["panel"]
    panel = b.Pos(0, p["panel_c"][0], z0 + p["panel_c"][1]) * b.Rot(-p["panel_tilt"], 0, 0) * b.Box(px, pl, pth)
    t = math.radians(p["panel_tilt"])

    def on_panel(ly):
        lz = -pth / 2 - 4
        return (p["panel_c"][0] + ly * math.cos(t) + lz * math.sin(t),
                z0 + p["panel_c"][1] - ly * math.sin(t) + lz * math.cos(t))
    br = None
    for sg in (-1, 1):
        for ly in (70.0, -50.0):
            y2, z2 = on_panel(ly)
            r_ = rod((sg * 80, yf - 4, zb + ph - 12), (sg * 80, y2, z2), 4.0)
            br = r_ if br is None else br + r_
    ant = zcyl(58, yf - nd / 2, z0 - 190, z0, 5)
    C = {}
    C["node_plate"] = Comp("FieldNode back plate", plate, 6, "node")
    C["node"] = Comp("FieldNode core", enc + panel + br + ant, 6, "node")
    C["node_vblocks"] = Comp("FieldNode V-blocks (2)", vblock(R, y0, clamps[0], p) + vblock(R, y0, clamps[1], p), 6, "node")
    C["node_bands"] = Comp("FieldNode band clamps (2)", band_clamp(R, yf, sx, clamps[0]) + band_clamp(R, yf, sx, clamps[1]), 6, "node")
    return C


def _alert_components(p=PARAMS, R=None):
    """Alert unit on the pole or mast (axis at the origin), side-mounted (SLW-DDR-003)."""
    d = derived(p)
    R = p["mast"][0] / 2 if R is None else R
    pw, ph, pt = p["alert_plate"]
    y0 = p["node_plate_y0"]
    yf = y0 - pt
    hb = d["alert_plate_z0"]
    clamps = (hb + 20, hb + 190)
    sx = p["alert_slot_x"]
    plate = bx(-pw / 2, pw / 2, yf, y0, hb, hb + ph)
    for zc in clamps:
        for sg in (-1, 1):
            plate = plate - bx(sg * sx - 3.0, sg * sx + 3.0, yf - 1, y0 + 1, zc - 7.5, zc + 7.5)
            plate = plate - ycyl(sg * 18, yf - 1, y0 + 1, zc, 2.25)        # V-block screws, countersunk
    aw, ad, ah = p["alert_box"]
    bz0 = d["alert_box_z0"]
    box = bx(-aw / 2, aw / 2, yf - ad, yf, bz0, bz0 + ah)
    # four M5 screws through the box's corner holes and the plate, nyloc nuts behind the plate
    nuts = None
    for sx_ in (-45, 45):
        for sz in (bz0 + 15, bz0 + ah - 15):
            plate = plate - ycyl(sx_, yf - 1, y0 + 1, sz, 2.75)
            n_ = ycyl(sx_, y0, y0 + 5, sz, 4.5) - ycyl(sx_, y0 - 1, y0 + 6, sz, 2.5)
            nuts = n_ if nuts is None else nuts + n_
    hd, hl = p["horn"]
    horn = ycyl(0, yf - ad, yf - ad - hl, bz0 + ah / 2, hd / 2)
    bd, bh = p["beacon"]
    beacon = zcyl(0, yf - ad / 2, bz0 + ah, bz0 + ah + bh, bd / 2)
    glands = zcyl(-30, yf - ad / 2, bz0 - 20, bz0, 8.0) + zcyl(30, yf - ad / 2, bz0 - 20, bz0, 8.0)
    C = {}
    C["alert_plate"] = Comp("Alert unit back plate", plate, 7, "alert")
    C["alert_vblocks"] = Comp("Alert unit V-blocks (2)", vblock(R, y0, clamps[0], p) + vblock(R, y0, clamps[1], p), 7, "alert")
    C["alert_bands"] = Comp("Alert unit band clamps (2)", band_clamp(R, yf, sx, clamps[0]) + band_clamp(R, yf, sx, clamps[1]), 7, "alert")
    C["alert_box"] = Comp("Alert box (driver inside)", box, 7, "alert")
    C["alert_nuts"] = Comp("Alert box screws and nuts (4)", nuts, 7, "alert")
    C["horn"] = Comp("Siren horn", horn, 7, "alert")
    C["beacon"] = Comp("Beacon", beacon, 7, "alert")
    C["alert_glands"] = Comp("Alert box glands (2)", glands, 7, "alert")
    return C


def mast_components(p=PARAMS):
    """Mast with footing, earth rod and bond, ground at z = 0 (site option, SLW-DDR-002)."""
    od, t = p["mast"]
    R = od / 2
    H = p["mast_h"]
    fd, fdep = p["footing"]
    C = {}
    C["mast_pipe"] = Comp("Mast pipe", ztube(0, 0, -fdep + 50, H, R, R - t), 8, "mast")
    C["footing"] = Comp("Concrete footing", zcyl(0, 0, -fdep, 0, fd / 2) - zcyl(0, 0, -fdep + 50, 1, R), 8, "mast")
    C["mast_cap"] = Comp("Mast top cap", ztube(0, 0, H - 25, H, R + 2, R) + zcyl(0, 0, H, H + 4, R + 2), 8, "mast")
    er_d, er_l, er_x = p["earth_rod"]
    C["earth_rod"] = Comp("Earth rod", zcyl(er_x, 0, 50 - er_l, 50, er_d / 2), 8, "mast")
    clamp = bx(er_x - 15, er_x + 15, -15, 15, 18, 43) - zcyl(er_x, 0, 0, 60, er_d / 2)
    mclamp = ztube(0, 0, 20, 40, R + 4, R)
    C["bond_clamps"] = Comp("Earth clamps (2)", clamp + mclamp, 8, "mast")
    C["bond"] = Comp("Bond conductor", xcyl(R + 4, er_x - 15, 0, 30, 3.5), 8, "mast")
    return C


def switch_components(p=PARAMS):
    """Keyed silence switch box on its own driven post, ground at z = 0 (SLW-DDR-002, SLW-DDR-003)."""
    od, t, above, embed = p["switch_post"]
    R = od / 2
    C = {}
    C["post"] = Comp("Switch post", ztube(0, 0, -embed, above, R, R - t), 7, "switch")
    C["post_cap"] = Comp("Post cap", ztube(0, 0, above - 15, above, R + 2, R) + zcyl(0, 0, above, above + 4, R + 2), 7, "switch")
    pw, ph, pt = p["switch_plate"]
    zc = p["switch_z"]
    yb = -R
    yf = yb - pt
    clamps = (zc - 62, zc + 62)
    sx = p["switch_slot_x"]
    plate = bx(-pw / 2, pw / 2, yf, yb, zc - ph / 2, zc + ph / 2)
    for z in clamps:
        for sg in (-1, 1):
            plate = plate - bx(sg * sx - 3.0, sg * sx + 3.0, yf - 1, yb + 1, z - 7.5, z + 7.5)
    for z in (zc - 28, zc + 28):
        for sg in (-1, 1):
            plate = plate - ycyl(sg * 40, yf - 1, yb + 1, z, 2.25)         # switch box screws
    C["switch_plate"] = Comp("Switch back plate", plate, 7, "switch")
    C["switch_bands"] = Comp("Hose clips (2)", band_clamp(R, yf, sx, clamps[0]) + band_clamp(R, yf, sx, clamps[1]), 7, "switch")
    sw, sd, sh = p["switch_box"]
    box = bx(-sw / 2, sw / 2, yf - sd, yf, zc - sh / 2, zc + sh / 2)
    C["switch_box"] = Comp("Keyed switch box", box, 7, "switch")
    C["switch_gland"] = Comp("Switch box gland", zcyl(0, yf - sd / 2, zc - sh / 2 - 20, zc - sh / 2, 8.0), 7, "switch")
    C["switch_key"] = Comp("Key switch", ycyl(0, yf - sd, yf - sd - 18, zc, 11.0), 7, "switch")
    return C


def build_components(p=PARAMS):
    """Every component, by assembly: {'stake': {...}, 'gauge': {...}, 'mast': {...}, 'switch': {...}}.
    The mast assembly holds the mast, the FieldNode massing and the alert unit."""
    m = mast_components(p)
    m.update(_node_components(p))
    m.update(_alert_components(p))
    return {"stake": stake_components(p), "gauge": gauge_components(p), "mast": m, "switch": switch_components(p)}


# ------------------------------------------------------------------ groupings used by the media scripts
def _grp(C, keys):
    return fuse([C[k].shape for k in keys])


def stake(p=PARAMS):
    """One tilt stake with its ground surface at z = 0. Returns {key: shape}."""
    C = stake_components(p)
    return {"stake": _grp(C, ["pipe", "endcap", "grout", "stand"]), "capsule": _grp(C, ["capsule", "collars"]),
            "plugs": C["plug"].shape, "head": _grp(C, ["reducer", "tape", "headtube", "headcap", "fittings", "screws"]),
            "lead": _grp(C, ["lead", "conduit_st"])}


def crack_gauge(p=PARAMS):
    """Crack gauge centered on the crack line (x = 0), ground at z = 0. Returns {key: shape}."""
    C = gauge_components(p)
    return {"gauge": _grp(C, ["pins", "clamps", "setscrews", "studs", "balls", "sensor", "coupling", "rod", "guard", "pegs"]),
            "reader": _grp(C, ["reader", "reader_screws", "reader_fitting"])}


def mast(p=PARAMS):
    """Mast with footing, earth rod, FieldNode massing and alert unit. Returns {key: shape}."""
    C = mast_components(p)
    N = _node_components(p)
    A = _alert_components(p)
    return {"mast": _grp(C, list(C)), "node": _grp(N, list(N)), "alert": _grp(A, list(A))}


def switch_post(p=PARAMS):
    """Keyed silence switch on its own post. Returns {key: shape}."""
    C = switch_components(p)
    return {"post": _grp(C, ["post", "post_cap"]), "switch": _grp(C, ["switch_plate", "switch_bands", "switch_box", "switch_gland", "switch_key"])}


def arrangement(p=PARAMS):
    """Stake, crack gauge, mast and switch post side by side on level ground, for drawing SLW-DWG-001."""
    from build123d import Compound, Pos
    xs, xg, xm, xw = p["arr_x"]
    parts = []
    for fn, x in ((stake, xs), (crack_gauge, xg), (mast, xm), (switch_post, xw)):
        for sh in fn(p).values():
            parts.append(Pos(x, 0, 0) * sh)
    return Compound(children=parts)


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch or stay apart. Returns (description, overlap mm3, gap mm, expectation, ok)."""
    A = build_components(p)
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    S = lambda g, k: A[g][k].shape  # noqa: E731
    s = lambda k: S("stake", k)  # noqa: E731
    chk("End cap screwed on the pipe", s("endcap"), s("pipe"), "touch")
    chk("Grout round the pipe", s("grout"), s("pipe"), "touch")
    chk("Grout round the end cap", s("grout"), s("endcap"), "touch")
    chk("Stand tube on the end cap floor", s("stand"), s("endcap"), "touch")
    chk("Stand tube clear of the pipe bore", s("stand"), s("pipe"), 0.5)
    chk("Collars on the capsule", s("collars"), s("capsule"), "touch")
    chk("Lower collar on the stand tube", s("collars"), s("stand"), "touch")
    chk("Collars a slip fit in the pipe bore", s("collars"), s("pipe"), 0.1)
    chk("Capsule clear of the pipe bore", s("capsule"), s("pipe"), 3.0)
    chk("Capsule clear of the stand tube (sits on the collar)", s("capsule"), s("stand"), 0.5)
    chk("Foam plug fills the pipe bore", s("plug"), s("pipe"), "touch")
    chk("Foam plug clear of the upper collar", s("plug"), s("collars"), 5.0)
    chk("Lead through the foam plug", s("lead"), s("plug"), "touch")
    chk("Lead leaves the capsule top", s("lead"), s("capsule"), "touch")
    chk("Lead clear of the pipe", s("lead"), s("pipe"), 5.0)
    chk("Tape wrap on the pipe", s("tape"), s("pipe"), "touch")
    chk("Reducer socket on the tape wrap", s("reducer"), s("tape"), "touch")
    chk("Reducer socket clear of the bare pipe (tape between)", s("reducer"), s("pipe"), 0.5)
    chk("Head screws in the reducer socket", s("screws"), s("reducer"), "touch")
    chk("Head screws into the pipe wall", s("screws"), s("pipe"), "touch")
    chk("Head tube in the reducer's 110 socket", s("headtube"), s("reducer"), "touch")
    chk("End cap on the head tube", s("headcap"), s("headtube"), "touch")
    chk("Conduit fittings through the head tube", s("fittings"), s("headtube"), "touch")
    chk("Conduit fittings clear of the reducer", s("fittings"), s("reducer"), 2.0)
    chk("Conduit fittings clear of the end cap", s("fittings"), s("headcap"), 2.0)
    chk("Conduit in the fittings", s("conduit_st"), s("fittings"), "touch")
    chk("Lead clear of the head tube", s("lead"), s("headtube"), 10.0)
    g = lambda k: S("gauge", k)  # noqa: E731
    chk("Clamp blocks a slide fit on the pins", g("clamps"), g("pins"), 0.1)
    chk("Set screws bear on the pins", g("setscrews"), g("pins"), "touch")
    chk("Set screws in the clamp blocks", g("setscrews"), g("clamps"), "touch")
    chk("Ball-joint studs in the clamp blocks", g("studs"), g("clamps"), "touch")
    chk("Ball joints on the studs", g("balls"), g("studs"), "touch")
    chk("Sensor body on the upslope ball joint", g("sensor"), g("balls"), "touch")
    chk("Coupling on the plunger", g("coupling"), g("sensor"), "touch")
    chk("Extension rod in the coupling", g("rod"), g("coupling"), "touch")
    chk("Extension rod into the downslope ball joint", g("rod"), g("balls"), "touch")
    chk("Sensor and rod clear of the guard", g("sensor") + g("rod"), g("guard"), 20.0)
    chk("Guard clear of the pins", g("guard"), g("pins"), 20.0)
    chk("Guard clear of the clamp blocks", g("guard"), g("clamps"), 20.0)
    chk("Pegs through the guard feet", g("pegs"), g("guard"), "touch")
    chk("Reader box under the guard web", g("reader"), g("guard"), "touch")
    chk("Reader screws through web and box", g("reader_screws"), g("reader"), "touch")
    chk("Reader box clear of the pin and clamp", g("reader"), g("pins") + g("clamps"), 10.0)
    chk("Reader fitting on the reader box", g("reader_fitting"), g("reader"), "touch")
    m = lambda k: S("mast", k)  # noqa: E731
    chk("Mast pipe in the footing", m("mast_pipe"), m("footing"), "touch")
    chk("Cap on the mast top", m("mast_cap"), m("mast_pipe"), "touch")
    chk("Earth clamp on the rod", m("bond_clamps"), m("earth_rod"), "touch")
    chk("Bond clamp on the mast", m("bond_clamps"), m("mast_pipe"), "touch")
    chk("Bond conductor between the clamps", m("bond"), m("bond_clamps"), "touch")
    for pre, who in (("node", "FieldNode"), ("alert", "Alert unit")):
        plate = m(f"{pre}_plate")
        chk(f"{who} V-blocks on the pole (V faces)", m(f"{pre}_vblocks"), m("mast_pipe"), "touch")
        chk(f"{who} V-blocks on the back plate", m(f"{pre}_vblocks"), plate, "touch")
        chk(f"{who} bands round the pole", m(f"{pre}_bands"), m("mast_pipe"), "touch")
        chk(f"{who} bands through the slots and across the plate", m(f"{pre}_bands"), plate, "touch")
        chk(f"{who} bands clear of the V-blocks", m(f"{pre}_bands"), m(f"{pre}_vblocks"), 0.5)
        chk(f"{who} back plate clear of the pole", plate, m("mast_pipe"), 10.0)
    chk("FieldNode core on its back plate", m("node"), m("node_plate"), "touch")
    chk("Alert box on its back plate", m("alert_box"), m("alert_plate"), "touch")
    chk("Alert box screws and nuts on the plate", m("alert_nuts"), m("alert_plate"), "touch")
    chk("Alert box nuts clear of the pole", m("alert_nuts"), m("mast_pipe") + m("mast_cap"), 5.0)
    chk("Horn on the alert box", m("horn"), m("alert_box"), "touch")
    chk("Beacon on the alert box", m("beacon"), m("alert_box"), "touch")
    chk("Glands on the alert box", m("alert_glands"), m("alert_box"), "touch")
    chk("Alert unit bands clear of the alert box", m("alert_bands"), m("alert_box"), 5.0)
    chk("Alert unit back plate clear of the mast cap", m("alert_plate"), m("mast_cap"), 5.0)
    chk("Alert unit clear of the FieldNode panel", m("alert_plate") + m("alert_box") + m("alert_glands"), m("node"), 100.0)
    w = lambda k: S("switch", k)  # noqa: E731
    chk("Cap on the switch post", w("post_cap"), w("post"), "touch")
    chk("Switch back plate against the post", w("switch_plate"), w("post"), "touch")
    chk("Hose clips round the post", w("switch_bands"), w("post"), "touch")
    chk("Hose clips through the slots and across the plate", w("switch_bands"), w("switch_plate"), "touch")
    chk("Switch box on its back plate", w("switch_box"), w("switch_plate"), "touch")
    chk("Hose clips clear of the switch box", w("switch_bands"), w("switch_box"), 5.0)
    chk("Gland on the switch box", w("switch_gland"), w("switch_box"), "touch")
    chk("Key switch on the switch box", w("switch_key"), w("switch_box"), "touch")
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:58s} overlap {v:9.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


def _compound(d):
    from build123d import Compound
    return Compound(children=list(d.values()))


def export_all():
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    items = {"slopewatch-stake": _compound(stake()), "slopewatch-crack-gauge": _compound(crack_gauge()),
             "slopewatch-mast": _compound(mast()), "slopewatch-switch-post": _compound(switch_post()),
             "slopewatch-arrangement": arrangement()}
    for name, shape in items.items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm, volume {shape.volume / 1e6:.2f} L")
    d = derived()
    print(f"capsule center {PARAMS['capsule_depth']:.0f} mm deep; hole {d['hole_depth']:.0f} mm; grout {d['grout_vol_l']:.2f} L; "
          f"reference-site cable {d['cable_m']:.1f} m")


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    export_all()
    print_checks()
