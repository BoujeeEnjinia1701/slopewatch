"""SlopeWatch parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    slopewatch-stake.step / .stl         one tilt stake (items 1 to 3, bus lead, foam plugs)
    slopewatch-crack-gauge.step / .stl   crack displacement gauge with reader box (item 4)
    slopewatch-mast.step / .stl          mast, footing, earth rod, FieldNode massing, siren and beacon (items 6 to 8)
    slopewatch-switch-post.step / .stl   keyed silence switch on its own post, about 5 m from the mast (item 7)
    slopewatch-arrangement.step / .stl   the four assemblies side by side on level ground (drawing SLW-DWG-001)

Axes: Z is up and the local ground surface at each assembly is z = 0. Each assembly is built on
its own axis at x = y = 0. On a site, +X points downslope. The FieldNode core faces -Y, as in the
FieldNode model (FND, cad/src/model.py), whose enclosure, panel and mounting dimensions are
repeated here as massing only; FieldNode remains the source of truth for its own geometry.

Main dimensions and interfaces only; not fabrication detail and not for fabrication. The same
PARAMS feed docs/04-calcs/sizing.py (SLW-CAL-001), the drawing SLW-DWG-001 (cad/src/sheets.py)
and the concept media (cad/src/concept_media.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 tilt stake: galvanized pipe OD x wall, total length, length below ground
    "pipe": (48.3, 3.2), "pipe_l": 1000.0, "embed": 800.0,
    #   grout column: diameter and height, cast around the lower pipe up from the bottom
    "grout_d": 110.0, "grout_l": 450.0,
    # 2 sensor capsule: tube OD x length; depth of the capsule center below ground (0.3 m at TRL 2,
    #   0.4 m from SLW-CAL-001 section B); foam plugs above and below the capsule
    "capsule": (34.0, 130.0), "capsule_depth": 400.0, "plug_l": 80.0,
    # 3 stake head: PVC cap OD x height, overlap onto the pipe; cable gland OD x length (downslope, +X)
    "head": (120.0, 170.0), "head_overlap": 40.0, "gland": (28.0, 40.0),
    # 4 crack gauge: anchor spacing across the crack, pin OD, pin length, pin depth below ground,
    #   sensor axis height, sensor body OD x length (100 mm stroke), guard (L x W x t), reader box
    "anchor_span": 900.0, "pin_d": 20.0, "pin_l": 700.0, "pin_embed": 500.0,
    "gauge_z": 110.0, "gauge_body": (25.0, 260.0), "stroke": 100.0,
    "guard": (1150.0, 200.0, 20.0), "reader": (80.0, 60.0, 45.0),
    # 8 mast: pipe OD x wall, height above ground, footing diameter x depth, earth rod (dia, length, offset)
    "mast": (48.3, 3.2), "mast_h": 3200.0, "footing": (320.0, 600.0), "earth_rod": (16.0, 1200.0, 450.0),
    # 6 FieldNode core (massing from FieldNode PARAMS): enclosure W x D x H, bottom height,
    #   back plate offset from mast axis, panel (X x slope x t), tilt, panel center (y, z above node bottom)
    "node": (150.0, 90.0, 200.0), "node_z0": 1750.0, "node_plate_y0": -42.0, "node_plate": (180.0, 320.0, 3.0),
    "panel": (290.0, 200.0, 17.0), "panel_tilt": 40.0, "panel_c": (-115.0, 385.0),
    # 7 alert unit: siren box (cube side) on the mast top, horn (dia x length, faces -Y), beacon (dia x height),
    #   keyed silence switch box (W x D x H) and its center height; since SLW-DDR-002 the switch sits on its
    #   own post (OD x wall, height above ground, length driven in) about 5 m from the mast on the +Y side,
    #   away from the horn, on a lead in conduit (switch_lead_m)
    "siren_box": 120.0, "horn": (110.0, 140.0), "beacon": (110.0, 220.0),
    "switch_box": (100.0, 60.0, 70.0), "switch_z": 1300.0,
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
    "head": (3, "Stake head with cable gland"),
    "gauge": (4, "Crack displacement gauge with reader"),
    "cable": (5, "Sensor bus cable in conduit"),
    "node": (6, "FieldNode core (massing)"),
    "alert": (7, "Siren and beacon alert unit"),
    "switch": (7, "Keyed silence switch on its own post"),
    "mast": (8, "Mast, footing and earth rod"),
}


def derived(p=PARAMS, s=SITE):
    """Dimensions the calc note and the drawing quote, computed from PARAMS and SITE."""
    od, t = p["pipe"]
    idia = od - 2 * t
    cap_top = -p["capsule_depth"] + p["capsule"][1] / 2
    cap_bot = -p["capsule_depth"] - p["capsule"][1] / 2
    fall_m = 2 * s["stake_spacing_m"]
    cable = (s["gauge_to_stake1_m"] + fall_m + s["stake3_to_toe_m"] + s["toe_to_mast_m"] + s["riser_m"]
             + 4 * s["drip_loop_m"])
    return {
        "pipe_id": idia,
        "pipe_area_mm2": math.pi / 4 * (od ** 2 - idia ** 2),
        "stake_top": p["pipe_l"] - p["embed"],
        "head_top": p["pipe_l"] - p["embed"] + p["head"][1] - p["head_overlap"],
        "cap_top": cap_top, "cap_bot": cap_bot,
        "grout_top": -p["embed"] + p["grout_l"],
        "grout_vol_l": math.pi / 4 * (p["grout_d"] ** 2 - od ** 2) * p["grout_l"] / 1e6
                       + math.pi / 4 * p["grout_d"] ** 2 * 20 / 1e6,     # plus a 20 mm base below the pipe
        "hole_vol_l": math.pi / 4 * p["grout_d"] ** 2 * (p["embed"] + 20) / 1e6,
        "mast_top": p["mast_h"],
        "alert_top": p["mast_h"] + p["siren_box"] + p["beacon"][1],
        "node_zc": p["node_z0"] + p["node"][2] / 2,
        "panel_cz": p["node_z0"] + p["panel_c"][1],
        "cable_m": cable * (1 + s["slack"]),
        "cable_m_net": cable,
        "fall_m": fall_m,
        "rise_m": fall_m * math.sin(math.radians(s["slope_deg"])),
    }


def _y_cyl(r, h):
    from build123d import Cylinder, Rot
    return Rot(90, 0, 0) * Cylinder(r, h)


def _x_cyl(r, h):
    from build123d import Cylinder, Rot
    return Rot(0, 90, 0) * Cylinder(r, h)


def stake(p=PARAMS):
    """One tilt stake with its ground surface at z = 0. Returns {key: shape}."""
    from build123d import Cylinder, Pos
    d = derived(p)
    od, t = p["pipe"]
    ro, ri = od / 2, d["pipe_id"] / 2
    z_bot = -p["embed"]
    pipe = Pos(0, 0, z_bot + p["pipe_l"] / 2) * (Cylinder(ro, p["pipe_l"]) - Cylinder(ri, p["pipe_l"] + 2))
    bottom_plug = Pos(0, 0, z_bot + 10) * Cylinder(ri, 20)
    grout = (Pos(0, 0, z_bot + p["grout_l"] / 2) * (Cylinder(p["grout_d"] / 2, p["grout_l"]) - Cylinder(ro, p["grout_l"] + 2))
             + Pos(0, 0, z_bot - 10) * Cylinder(p["grout_d"] / 2, 20))
    cap = Pos(0, 0, -p["capsule_depth"]) * Cylinder(p["capsule"][0] / 2, p["capsule"][1])
    plugs = (Pos(0, 0, d["cap_top"] + 10 + p["plug_l"] / 2) * Cylinder(ri, p["plug_l"])
             + Pos(0, 0, d["cap_bot"] - 10 - p["plug_l"] / 2) * Cylinder(ri, p["plug_l"]))
    top = d["stake_top"]
    hr, hh = p["head"][0] / 2, p["head"][1]
    hz = top - p["head_overlap"] + hh / 2
    head = (Pos(0, 0, hz) * (Cylinder(hr, hh) - Pos(0, 0, -8) * Cylinder(hr - 5, hh - 14))
            + Pos(0, 0, top - p["head_overlap"] + 4) * (Cylinder(hr - 5, 8) - Cylinder(ro, 10))   # reducer ring
            + Pos(hr + p["gland"][1] / 2 - 4, 0, top + 20) * _x_cyl(p["gland"][0] / 2, p["gland"][1]))
    lead = (Pos(0, 0, (d["cap_top"] + top + 30) / 2) * Cylinder(4, top + 30 - d["cap_top"])
            + Pos(hr / 2 + 10, 0, top + 30) * _x_cyl(4, hr + 20))
    return {"stake": pipe + bottom_plug + grout, "capsule": cap, "plugs": plugs, "head": head, "lead": lead}


def crack_gauge(p=PARAMS):
    """Crack gauge centered on the crack line (x = 0), ground at z = 0. Returns {key: shape}."""
    from build123d import Box, Cylinder, Pos
    a = p["anchor_span"] / 2
    zc = -p["pin_embed"] + p["pin_l"] / 2
    pins = Pos(-a, 0, zc) * Cylinder(p["pin_d"] / 2, p["pin_l"]) + Pos(a, 0, zc) * Cylinder(p["pin_d"] / 2, p["pin_l"])
    gz = p["gauge_z"]
    clamps = Pos(-a, 0, gz) * Box(60, 60, 80) + Pos(a, 0, gz) * Box(60, 60, 80)
    bd, bl = p["gauge_body"]
    body = Pos(-a + 30 + bl / 2, 0, gz) * _x_cyl(bd / 2, bl)                  # sensor body on the upslope anchor
    rod = Pos((-a + 30 + bl + a - 30) / 2, 0, gz) * _x_cyl(4, (a - 30) - (-a + 30 + bl) + 2)   # plunger extension rod
    gl, gw, gt = p["guard"]
    guard = (Pos(0, 0, gz + 60) * Box(gl, gw, gt)
             + Pos(0, gw / 2 - 5, gz - 5) * Box(gl, 10, 110) + Pos(0, -gw / 2 + 5, gz - 5) * Box(gl, 10, 110))
    rw, rd, rh = p["reader"]
    reader = Pos(-a, -gw / 2 - rd / 2 - 20, rh / 2 + 150) * Box(rw, rd, rh)
    return {"gauge": pins + clamps + body + rod + guard, "reader": reader}


def mast(p=PARAMS):
    """Mast with footing, earth rod, FieldNode massing and alert unit; ground at z = 0. Returns {key: shape}."""
    from build123d import Box, Cylinder, Pos, Rot
    d = derived(p)
    od, t = p["mast"]
    H = p["mast_h"]
    fd, fdep = p["footing"]
    pole = Pos(0, 0, (H - fdep + 50) / 2) * (Cylinder(od / 2, H + fdep - 50) - Cylinder(od / 2 - t, H + fdep - 48))
    footing = Pos(0, 0, -fdep / 2) * (Cylinder(fd / 2, fdep) - Cylinder(od / 2, fdep + 2))
    er_d, er_l, er_x = p["earth_rod"]
    rod = Pos(er_x, 0, 50 - er_l / 2) * Cylinder(er_d / 2, er_l)
    bond = Pos(er_x / 2, 0, 30) * _x_cyl(4, er_x)
    # FieldNode core massing (numbers from FieldNode PARAMS)
    nw, nd, nh = p["node"]
    pw, ph, pt = p["node_plate"]
    y_back = p["node_plate_y0"] - pt
    z0 = p["node_z0"]
    plate = Pos(0, p["node_plate_y0"] - pt / 2, z0 - 40 + ph / 2) * Box(pw, pt, ph)
    enc = Pos(0, y_back - nd / 2, z0 + nh / 2) * Box(nw, nd, nh)
    vblocks = Pos(0, (p["node_plate_y0"] - od / 2) / 2 - 2, z0 - 20) * Box(50, 20, 30) \
        + Pos(0, (p["node_plate_y0"] - od / 2) / 2 - 2, z0 + 230) * Box(50, 20, 30)
    px, pl, pth = p["panel"]
    panel = Pos(0, p["panel_c"][0], z0 + p["panel_c"][1]) * Rot(-p["panel_tilt"], 0, 0) * Box(px, pl, pth)
    posts = (Pos(80, -60, z0 + 300) * Box(25, 3, 200) + Pos(-80, -60, z0 + 300) * Box(25, 3, 200))
    ant = Pos(58, y_back - nd / 2, z0 - 95) * Cylinder(5, 190)
    node = plate + enc + vblocks + panel + posts + ant
    # alert unit on the mast top (the keyed switch is on its own post, see switch_post())
    s = p["siren_box"]
    siren = Pos(0, 0, H + s / 2) * Box(s, s, s)
    hd, hl = p["horn"]
    horn = Pos(0, -s / 2 - hl / 2, H + s / 2) * _y_cyl(hd / 2, hl)
    bd, bh = p["beacon"]
    beacon = Pos(0, 0, H + s + bh / 2) * Cylinder(bd / 2, bh)
    alert = siren + horn + beacon
    return {"mast": pole + footing + rod + bond, "node": node, "alert": alert}


def switch_post(p=PARAMS):
    """Keyed silence switch box on its own driven post, ground at z = 0 (SLW-DDR-002). Returns {key: shape}."""
    from build123d import Box, Cylinder, Pos
    od, t, above, embed = p["switch_post"]
    L = above + embed
    post = Pos(0, 0, above - L / 2) * (Cylinder(od / 2, L) - Cylinder(od / 2 - t, L + 2))
    cap = Pos(0, 0, above + 5) * Cylinder(od / 2 + 2, 10)
    sw, sd, sh = p["switch_box"]
    box = Pos(0, -(od / 2 + sd / 2 + 5), p["switch_z"]) * Box(sw, sd, sh)      # faces the mast (-Y)
    gland = Pos(0, -(od / 2 + sd / 2 + 5), p["switch_z"] - sh / 2 - 12) * Cylinder(8, 24)
    return {"post": post + cap, "switch": box + gland}


def arrangement(p=PARAMS):
    """Stake, crack gauge, mast and switch post side by side on level ground, for drawing SLW-DWG-001."""
    from build123d import Compound, Pos
    xs, xg, xm, xw = p["arr_x"]
    parts = []
    for k, sh in stake(p).items():
        parts.append(Pos(xs, 0, 0) * sh)
    for k, sh in crack_gauge(p).items():
        parts.append(Pos(xg, 0, 0) * sh)
    for k, sh in mast(p).items():
        parts.append(Pos(xm, 0, 0) * sh)
    for k, sh in switch_post(p).items():
        parts.append(Pos(xw, 0, 0) * sh)
    return Compound(children=parts)


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
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm, volume {shape.volume / 1e6:.2f} L")
    d = derived()
    print(f"capsule center {PARAMS['capsule_depth']:.0f} mm deep; grout {d['grout_vol_l']:.2f} L; "
          f"reference-site cable {d['cable_m']:.1f} m")


if __name__ == "__main__":
    export_all()
