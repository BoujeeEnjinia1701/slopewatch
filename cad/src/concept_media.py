"""SlopeWatch concept massing model and media (TRL 3, parts from cad/src/model.py).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. The slope profile lies in the XZ plane: the toe bench is at +X (Z = 0),
the face rises at 25 degrees toward -X, and the crest bench with a tension crack is at -X.
Y runs across the slope. The ground block is grey context; SlopeWatch parts are colored and
carry the BOM line number used in bom/bom.csv and the exploded view.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import (Box, Cylinder, Torus, Pos, Rot, Solid, Plane, Vector, Polygon, extrude)
import concept
from concept import Part, render_all, human_figure, _render

# ---------------- site geometry ----------------
SLOPE_DEG = 25.0
TAN = math.tan(math.radians(SLOPE_DEG))
TOE_X = 2000.0             # toe of the slope face
CREST_X = -3000.0          # crest of the slope face
CREST_Z = (TOE_X - CREST_X) * TAN      # about 2.33 m high face
X_MIN, X_MAX = -4800.0, 5400.0         # crest bench and toe bench extents
HALF_W = 1600.0                        # half width across the slope (Y)
BASE_Z = -1100.0                       # bottom of the ground block
CRACK_X = -3900.0                      # tension crack on the crest bench

GROUND = "#B8B0A2"
STEEL = "#6B7280"
ACCENT = "#0F766E"


def surface_z(x):
    """Ground surface height at x (mm)."""
    if x >= TOE_X:
        return 0.0
    if x <= CREST_X:
        return CREST_Z
    return (TOE_X - x) * TAN


def tube3(a, b, r):
    """Round rod between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


# Ground block: slope profile extruded across Y, with a tension crack on the crest bench
profile = Polygon(*[(X_MIN, BASE_Z), (X_MAX, BASE_Z), (X_MAX, 0), (TOE_X, 0),
                    (CREST_X, CREST_Z), (X_MIN, CREST_Z)], align=None)
ground = extrude(Plane.XZ * profile, amount=HALF_W, both=True)
crack = Pos(CRACK_X, 0, CREST_Z - 200) * Rot(0, 0, 8) * Box(70, 2 * HALF_W + 400, 420)
ground = ground - crack

# ---------------- parts from the parametric model (cad/src/model.py) ----------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import PARAMS as P, stake, crack_gauge, mast, switch_post, derived  # noqa: E402
D = derived(P)
PIPE_R = P["pipe"][0] / 2
HEAD_R = P["head"][0] / 2

# 1 to 3: tilt stakes, three down the fall line at Y = 0 (scene spacing compressed; site spacing 10 m)
STAKE_X = (-2300.0, -500.0, 1200.0)
stakes = capsules = heads = None
for sx in STAKE_X:
    gz = surface_z(sx)
    st = {k: Pos(sx, 0, gz) * v for k, v in stake().items()}
    s_ = st["stake"] + st["plugs"] + st["lead"]
    stakes = s_ if stakes is None else stakes + s_
    capsules = st["capsule"] if capsules is None else capsules + st["capsule"]
    heads = st["head"] if heads is None else heads + st["head"]

# 4: crack gauge across the tension crack on the crest bench
GY = 900.0
cg = crack_gauge()
gauge = Pos(CRACK_X, GY, CREST_Z) * (cg["gauge"] + cg["reader"])
a2 = CRACK_X + P["anchor_span"] / 2

# 6 to 8: mast with FieldNode core and alert unit on the toe bench
MX, MY = 3400.0, -600.0
MAST_H = P["mast_h"]
ms = {k: Pos(MX, MY, 0) * v for k, v in mast().items()}
node, siren, mast_s = ms["node"], ms["alert"], ms["mast"]
# 7: keyed silence switch on its own post, away from the siren (about 5 m on site, compressed here),
#    with its lead from the mast foot in conduit
SWX, SWY = 5100.0, 1200.0
sp = switch_post()
siren = (siren + Pos(SWX, SWY, 0) * (sp["post"] + sp["switch"])
         + tube3((MX + 30, MY + 30, 25), (SWX, SWY - 60, 25), 9))

# ---------------- 5: sensor bus cable in conduit, on the surface ----------------
def surf(x, y, lift=25.0):
    return (x, y, surface_z(x) + lift)


pts = [(STAKE_X[0] + 110, 0), (STAKE_X[1] + 110, 0), (STAKE_X[2] + 110, 0), (TOE_X, 0),
       (MX - 200, MY), (MX - 40, MY)]
cable = None
for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
    # split each run so it follows the slope surface
    n = 6
    for k in range(n):
        xa = x0 + (x1 - x0) * k / n; ya = y0 + (y1 - y0) * k / n
        xb = x0 + (x1 - x0) * (k + 1) / n; yb = y0 + (y1 - y0) * (k + 1) / n
        seg = tube3(surf(xa, ya), surf(xb, yb), 14)
        cable = seg if cable is None else cable + seg
# branch from the crack gauge down to the first stake, and riser up the mast to the node
cable = (cable + tube3(surf(a2 + 60, GY), surf(STAKE_X[0] - 300, GY), 10)
         + tube3(surf(STAKE_X[0] - 300, GY), surf(STAKE_X[0] + 110, 0), 10)
         + tube3((MX - 40, MY, 25), (MX - 40, MY, P["node_z0"] - 60), 10))

# Site scene: hero, blueprint and 3D viewer. BOM numbers on every SlopeWatch part.
parts = [
    Part("Ground: 25 degree slope with tension crack (site)", ground, GROUND, None),
    Part("Tilt stakes, pipe and grout (3)", stakes, STEEL, 1),
    Part("Tilt sensor capsules (3)", capsules, ACCENT, 2),
    Part("Stake heads with conduit fittings (3)", heads, "#D4A017", 3),
    Part("Crack displacement gauge with reader", gauge, "#7C3AED", 4),
    Part("Sensor bus cable in conduit", cable, "#111827", 5),
    Part("FieldNode core with 6 W panel", node, "#1E3A8A", 6),
    Part("Alert unit and keyed switch post", siren, "#C2410C", 7),
    Part("Mast, footing and earth rod (site option)", mast_s, "#94A3B8", 8),
]

# Person on the toe bench for scale (added as context so the figure stands on the bench,
# not at the bottom of the ground block where the kit helper would place it)
person = human_figure(1750.0, x=4700.0, y=700.0, z=0.0)
person.name = "1.75 m person"

render_all(
    parts, project="SlopeWatch", title="Slope movement monitor concept", dwg_no="SLW-DWG-010",
    key_figures=["3 grouted tilt stakes, capsule 0.4 m deep; 0.0055 deg output step",
                 "Precaution 0.01 deg/h, warning 0.1 deg/h (decided 2026-09-25)",
                 "Thermal drift 0.0012 deg/h worst case (wet soil), R2 limit 0.002",
                 "Reads every 10 min; siren 13 s after a confirmed warning",
                 "$304 SlopeWatch parts on an existing pole; mast option +$28; FieldNode $126"],
    cut=False, scale_figure=False, context=[person],
    flow={"title": "data and alert flow (latencies are estimates)", "unit": "min",
          "stages": [("Stakes, crack gauge", "read every 10 min"),
                     ("FieldNode at site", "rate vs threshold"),
                     ("LoRaWAN gateway", "hourly, 10 min on alert"),
                     ("Alert server", "inverse-velocity trend"),
                     ("People on alert list", "SMS, 1.6 to 4.6 min")],
          "losses": [(1, "Local siren and beacon, no network (estimate)", 0.2)]},
)



# ---------------- exploded view: one of each kit item laid out at a readable scale ----------------
# The site scene is about 10 m across, which makes a 48 mm stake too small to read, so the exploded
# view shows one stake, the crack gauge, a coil of bus cable and the mast set side by side.
def kit_layout():
    ex = []
    st = {k: Pos(0, 0, P["embed"]) * v for k, v in stake().items()}      # stake stands on z = 0
    ex.append(Part("Tilt stake: pipe, end cap, grout, stand tube, plug (1 of 3)", st["stake"] + st["plugs"], STEEL, 1))
    ex.append(Part("Tilt sensor capsule (1 of 3)", st["capsule"], ACCENT, 2, (0, 0, 750)))
    ex.append(Part("Stake head with conduit fittings (1 of 3)", st["head"], "#D4A017", 3, (0, 0, 650)))
    cg = crack_gauge()
    gx = 1300.0
    ex.append(Part("Crack displacement gauge with reader", Pos(gx, 0, P["pin_embed"]) * (cg["gauge"] + cg["reader"]),
                   "#7C3AED", 4))
    coil = None
    for k in range(4):
        t = Pos(2550, 0, 320 + 18 * k) * Torus(260, 10)
        coil = t if coil is None else coil + t
    ex.append(Part("Sensor bus cable in conduit (coil)", coil, "#111827", 5))
    ms = {k: Pos(3600.0, 0, P["footing"][1]) * v for k, v in mast().items()}
    ex.append(Part("FieldNode core with 6 W panel", ms["node"], "#1E3A8A", 6, (0, -700, 0)))
    ex.append(Part("Alert unit on its back plate", ms["alert"], "#C2410C", 7, (0, 0, 450)))
    sp = switch_post()
    ex.append(Part("keyed switch on its own post", Pos(4300.0, 0, P["switch_post"][3]) * (sp["post"] + sp["switch"]),
                   "#C2410C", 7))
    ex.append(Part("Mast, footing and earth rod (site option)", ms["mast"], "#94A3B8", 8))
    return ex


_render(kit_layout(), concept.ROOT / "media" / "exploded.png", offsets=True, labels=True, azim=-70, elev=18,
        title="SlopeWatch: exploded view of one of each kit item",
        note="Numbers match bom/bom.csv. A site uses three stakes (items 1 to 3); item 9 (gateway and software) is not shown.")


# ---------------- cutaway: one tilt stake in the slope, cut on its axis ----------------
def stake_cutaway():
    big = 6000.0
    cutter = Pos(0, big / 2, 0) * Box(big, big, big)
    # a 1.4 m block of slope around one stake; surface rises toward -X at the slope angle
    h = 700.0 * TAN
    blk = Polygon(*[(-700, -1300), (700, -1300), (700, -h), (-700, h)], align=None)
    block = extrude(Plane.XZ * blk, amount=450, both=True)
    st = stake()
    bore = Pos(0, 0, -D["hole_depth"] / 2) * Cylinder(P["grout_d"] / 2, D["hole_depth"])
    ps = [Part("Slope soil (site)", block - bore, GROUND, None),
          Part("Tilt stake: 48.3 mm pipe in 110 mm grout column", st["stake"], STEEL, 1),
          Part("Tilt sensor capsule, 0.4 m below ground", st["capsule"], ACCENT, 2),
          Part("Stake head with conduit fittings", st["head"], "#D4A017", 3),
          Part("Capsule lead and bus conduit", st["lead"], "#111827", 5),
          Part("Foam plug above the capsule; stand tube below", st["plugs"], "#E5E7EB", None)]
    out = []
    for p in ps:
        s_ = p.shape & cutter
        if s_.volume > 1e-6:
            out.append(Part(p.name, s_, p.color, p.bom))
    return out


_render(stake_cutaway(), concept.ROOT / "media" / "cutaway.png", azim=-90, elev=8, labels=True,
        title="SlopeWatch: cutaway of one tilt stake",
        note="Section on the stake axis. At 0.4 m the daily soil temperature swing is damped enough to meet R2 (SLW-CAL-001).")
