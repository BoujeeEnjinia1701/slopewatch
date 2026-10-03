"""SlopeWatch product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of one tilt stake (BOM items 1 to 3 with its bus lead):
a signal amber PVC stake head built from a reducer, a 110 mm pipe and an end cap, a retroreflective band, an
identification label, an arrow on the crown that points downslope, two cap screws and two M20 conduit
fittings (bus in upslope, bus out downslope) with the conduit running down to the ground; the galvanized pipe; and,
below ground, the grout column, the two closed-cell foam plugs and the potted sensor capsule with
its lead. Context is a compact patch of 25 degree slope with a topsoil layer, a few stones and the
corrugated conduit that carries the bus downslope. A quarter of the ground, grout, pipe and foam
plugs is cut away on the downslope front quadrant (+X, -Y) so the buried capsule shows.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
A research prototype, not a certified slope monitoring system.

Every main dimension and interface comes from PARAMS, SITE, derived() and stake() in model.py.
Axes as model.py: Z up, the ground surface at the stake axis at z = 0, +X downslope, the stake
on its own axis at x = y = 0. The pipe is split at ground level into an above-ground part (shell)
and a buried part (internal) so the detail view can show the head without the ground; both keep
the model.py pipe size and length. See docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Polygon, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, SITE, build_components, derived

TITLE = "SlopeWatch: buried tilt sensor stake for moving slopes"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); one tilt stake in a "
             "patch of 25 degree slope, downslope to the right, with the front quarter of the ground cut "
             "away to show the grout column and the sensor capsule 0.4 m below ground"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): stake head with label, "
             "band, screws and conduit fittings; galvanized pipe and grout column; foam plugs, sensor capsule "
             "and lead drawn out to the right"},
    {"name": "detail", "groups": ["shell"], "explode": False, "el": 22, "az": -35,
     "note": "Detail from the front right, slightly above (about 22 deg elevation): the stake head above "
             "ground without the slope, conduit fittings and the conduit run facing downslope at right"},
]

# Context patch (render prop, not site geometry)
PATCH_X = (-260.0, 280.0)      # upslope to downslope extent (mm)
PATCH_Y = (-200.0, 200.0)
PATCH_Z0 = -900.0              # flat underside, below the grout base
TOPSOIL = 45.0                 # topsoil layer thickness
CONDUIT_AT = (175.0, 26.0)     # x, y where the conduit rises out of the ground
CONDUIT_R = 10.0               # 20 mm corrugated conduit (BOM 5)

# Colours (restrained product palette; kit accent)
C_HEAD = "#E3A33A"             # stake head, painted for visibility (signal amber)
C_HEAD2 = "#C98A26"
C_REFLECT = "#F2F3F1"
C_ACCENT = "#0F766E"
C_LABEL = "#F4F4F2"
C_INK = "#1F2937"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_GALV = "#B7BDC3"
C_STEEL = "#A7ADB4"
C_GROUT = "#BDB8AE"
C_FOAM = "#46525C"
C_CAPSULE = "#E6E8EA"
C_CAP_END = "#2B2F36"
C_CABLE = "#20252B"
C_SOIL = "#9C8A72"
C_TOPSOIL = "#6E5F4C"
C_STONE = "#A39E96"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _ring(z, r_out, r_in, h):
    return Pos(0, 0, z) * (Cylinder(r_out, h) - Cylinder(r_in, h + 1))


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _hex_x(x, y, z, af, length):
    """Hex prism along X (across flats `af`), starting at x."""
    return Pos(x, y, z) * extrude(Plane.YZ * RegularPolygon(af / math.sqrt(3), 6), amount=length)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _xmax(s):
    return s.faces().sort_by(Axis.X)[-1].edges()


def _quadrant(z0, z1):
    """The cut-away front downslope quadrant (+X, -Y) between z0 and z1."""
    return _box(200, -200, (z0 + z1) / 2, 400, 400, z1 - z0)


def product_parts(P=PARAMS, S=SITE):
    D = derived(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    od, t = P["pipe"]
    ro, ri = od / 2, D["pipe_id"] / 2
    z_bot = -P["embed"]
    top = D["stake_top"]                                  # pipe top, 200 mm above ground
    hr, hh = P["head"][0] / 2, P["head"][1]
    hz0 = top - P["head_overlap"]                         # head underside, 160 mm above ground
    htop = D["head_top"]                                  # 330 mm above ground
    gd, gl = P["gland"]
    gz = (top + 55 + D["head_top"] - 28) / 2              # conduit fitting axis height, as model.py
    gx0 = hr - 4                                          # gland starts 4 mm inside the head wall
    slope = math.tan(math.radians(S["slope_deg"]))

    def surf(x):
        return -slope * x

    cut_low = _quadrant(PATCH_Z0 - 50, 0.0)               # cut-away below ground

    # ------------------------------------------------------------ stake head (BOM 3)
    # constructable design (SLW-DDR-003): 110 x 50 mm reducer, 110 mm pipe and end cap, two M20 conduit fittings
    # (bus in upslope, bus out downslope), all taken from model.py; marking decided 2026-10-02 (SLW-DEC-001)
    EH = (0, 0, 260)
    MS = build_components(P)["stake"]
    cap = MS["headcap"].shape
    cap = _fillet_try(cap, _top(cap), [8.0, 5.0, 3.0])
    add("Stake head reducer (PVC drainage, painted amber)", MS["reducer"].shape, C_HEAD, "painted", 3, "shell", (0, 0, 150))
    add("Stake head tube (PVC, painted amber)", MS["headtube"].shape, C_HEAD, "painted", 3, "shell", EH)
    add("Stake head end cap (PVC, painted amber)", cap, C_HEAD, "painted", 3, "shell", EH)
    add("Retroreflective band", MS["mark_band"].shape, C_REFLECT, "painted", 3, "shell", EH)
    add("Stake ID label", MS["mark_label"].shape, C_LABEL, "paper", 3, "shell", EH)
    lz = D["head_bot"] + 72
    ink = (_box(-10, -hr, lz + 8, 16, 14, 8) + _box(10, -hr, lz + 9, 18, 14, 3) + _box(0, -hr, lz - 2, 32, 14, 3))
    ink = (_ring(lz, hr + 0.7, hr + 0.1, 30) & ink)
    add("Stake ID label print", ink, C_INK, "paper", 3, "shell", EH)
    add("Downslope arrow on crown", MS["mark_arrow"].shape, C_INK, "painted", 3, "shell", EH)
    add("Cap screws (stainless)", MS["screws"].shape, C_STEEL, "metal", 3, "shell", EH)
    add("Conduit fittings, M20 (2)", MS["fittings"].shape, C_BLACK, "plastic", 3, "shell", (0, 0, 260))

    # ------------------------------------------------------------ bus conduit (BOM 5)
    fz = (top + 55 + htop - 28) / 2
    xs = hr + 3 + P["fitting"][2] + 90 - 15                  # conduit stub end, as model.py
    add("Conduit stubs at the head", MS["conduit_st"].shape, C_CABLE, "rubber", 5, "shell", (0, 0, 260))
    cx, cy = CONDUIT_AT
    ctop = surf(cx) + 70
    a, b, c = (xs - 2, 0.0, fz), (cx + 18, cy * 0.3, fz - 60), (cx, cy, ctop + 45)
    pts = [tuple((1 - u) ** 2 * a[i] + 2 * (1 - u) * u * b[i] + u ** 2 * c[i] for i in range(3))
           for u in [k / 10 for k in range(11)]]
    drip = _pipe(pts + [(cx, cy, ctop - 4)], CONDUIT_R)
    add("Bus conduit run to the ground", drip, C_CABLE, "rubber", 5, "shell", (120, 0, 260))

    # ------------------------------------------------------------ pipe (BOM 1), split at ground level
    EP = (0, 0, 0)
    upper = _zcyl(0, 0, top / 2, ro, top) - _zcyl(0, 0, top / 2, ri, top + 2)
    add("Galvanized pipe, above ground", upper, C_GALV, "metal", 1, "shell", EP)
    lower = _zcyl(0, 0, z_bot / 2, ro, -z_bot) - _zcyl(0, 0, z_bot / 2, ri, -z_bot + 2)
    lower -= cut_low
    add("Galvanized pipe, below ground", lower, C_GALV, "metal", 1, "internal", EP)
    plug = _zcyl(0, 0, z_bot + 10, ri, 20) - cut_low
    add("Pipe bottom plug", plug, C_DARK, "plastic", 1, "internal", EP)

    gr = P["grout_d"] / 2
    grout = (_zcyl(0, 0, z_bot + P["grout_l"] / 2, gr, P["grout_l"]) - _zcyl(0, 0, z_bot + P["grout_l"] / 2, ro,
                                                                              P["grout_l"] + 2))
    grout += _zcyl(0, 0, z_bot - 10, gr, 20)
    grout = _fillet_try(grout, [e for e in _top(grout) if e.radius > gr - 1], [4.0, 2.0])
    grout -= cut_low
    add("Grout column", grout, C_GROUT, "paper", 1, "internal", (0, 0, -180))

    # ------------------------------------------------------------ capsule and plugs (BOM 2, BOM 10)
    EC = (380, 0, 0)
    cd, cl = P["capsule"]
    cz = -P["capsule_depth"]
    tube = _zcyl(0, 0, cz, cd / 2, cl - 16)
    add("Sensor capsule tube (potted)", tube, C_CAPSULE, "plastic", 2, "internal", EC)
    ends = None
    for sgn in (-1, 1):
        e = _zcyl(0, 0, cz + sgn * (cl / 2 - 8), cd / 2 + 0.3, 16)
        e = _fillet_try(e, (_top(e) if sgn > 0 else _bottom(e)), [4.0, 2.5, 1.5])
        ends = e if ends is None else ends + e
    add("Capsule end caps", ends, C_CAP_END, "plastic", 2, "internal", EC)
    cband = _ring(cz + 22, cd / 2 + 0.3, cd / 2 - 0.2, 8)
    add("Capsule accent band", cband, C_ACCENT, "painted", 2, "internal", EC)
    clab = _ring(cz - 14, cd / 2 + 0.3, cd / 2 - 0.2, 34) & _box(0, -cd / 2, cz - 14, 26, cd, 40)
    add("Capsule label", Rot(0, 0, 40) * clab, C_LABEL, "paper", 2, "internal", EC)
    arrow_c = extrude(Plane.XZ * Polygon((-2, -10), (2, -10), (2, 2), (5, 2), (0, 10), (-5, 2), (-2, 2),
                                         align=None), amount=0.6)
    arrow_c = Rot(0, 0, 40) * (Pos(0, -cd / 2 - 0.2, cz - 14) * arrow_c)
    add("Capsule label print (up arrow)", arrow_c, C_INK, "paper", 2, "internal", EC)

    pl = P["plug_l"]
    plugs = (_zcyl(0, 0, D["cap_top"] + 10 + pl / 2, ri - 0.2, pl)
             + _zcyl(0, 0, D["cap_bot"] - 10 - pl / 2, ri - 0.2, pl)) - cut_low
    add("Closed-cell foam plugs", plugs, C_FOAM, "rubber", 10, "internal", EC)

    lead = _pipe([(0, 0, D["cap_top"] + 4), (0, 0, top + 18), (6, 0, top + 30), (gx0 + 2, 0, gz)], 3.0)
    add("Capsule bus lead", lead, C_CABLE, "rubber", 2, "internal", EC)

    # ------------------------------------------------------------ context: slope patch (not in the BOM)
    x0, x1 = PATCH_X
    y0, y1 = PATCH_Y
    above = Pos(0, 0, 0) * Rot(0, S["slope_deg"], 0) * Pos(0, 0, 1000) * Box(3000, 3000, 2000)
    above_top = Pos(0, 0, 0) * Rot(0, S["slope_deg"], 0) * Pos(0, 0, 1000 - TOPSOIL) * Box(3000, 3000, 2000)
    block = _box((x0 + x1) / 2, (y0 + y1) / 2, (PATCH_Z0 + 300) / 2, x1 - x0, y1 - y0, 300 - PATCH_Z0)
    g_top = D["grout_top"]
    hole = _zcyl(0, 0, (z_bot - 20 + g_top) / 2, gr, g_top - z_bot + 20) + _zcyl(0, 0, (g_top + 100) / 2, ro,
                                                                                  100 - g_top)
    trench = _pipe([(cx, cy, ctop), (cx, cy, surf(cx) - 150),
                    (x1 + 5, cy, surf(x1 + 5) - 150)], CONDUIT_R)
    cut_ctx = _quadrant(PATCH_Z0 - 50, 400)
    sub = block - above_top - hole - trench - cut_ctx
    add("Subsoil (cut away)", sub, C_SOIL, "rubber", None, "context", (0, 0, 0))
    topsoil = (block & above_top) - above - hole - trench - cut_ctx
    add("Topsoil layer", topsoil, C_TOPSOIL, "rubber", None, "context", (0, 0, 0))

    stones = None
    for (x, y, r) in [(-180, 120, 14), (-120, -150, 10), (-60, 150, 8), (120, 140, 12), (230, 70, 9),
                      (-210, -60, 7), (40, 90, 6)]:
        s = Pos(x, y, surf(x) - r * 0.35) * (Sphere(r) & Box(3 * r, 2.2 * r, 1.6 * r))
        stones = s if stones is None else stones + s
    add("Stones (surface)", stones, C_STONE, "rubber", None, "context", (0, 0, 0))

    # corrugated conduit (BOM 5): stub above ground with ribs, buried run downslope
    conduit = _pipe([(cx, cy, ctop), (cx, cy, surf(cx) - 150), (x1 + 4, cy, surf(x1 + 4) - 150)], CONDUIT_R)
    for k in range(6):
        conduit += _zcyl(cx, cy, surf(cx) + 8 + k * 11, CONDUIT_R + 1.2, 5)
    conduit -= _zcyl(cx, cy, ctop, CONDUIT_R - 2, 12)
    conduit += _zcyl(cx, cy, ctop - 3, CONDUIT_R + 1.5, 6) - _zcyl(cx, cy, ctop - 3, 4.5, 8)
    add("Corrugated conduit (bus cable)", conduit, C_DARK, "plastic", 5, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:40s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
