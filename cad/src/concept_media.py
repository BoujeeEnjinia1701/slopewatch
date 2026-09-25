"""SlopeWatch concept massing model and media (TRL 2).

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

# ---------------- 1 to 3: tilt stakes (three, down the fall line at Y = 0) ----------------
STAKE_X = (-2300.0, -500.0, 1200.0)
PIPE_R, PIPE_L, EMBED = 24.0, 1000.0, 800.0      # 48 mm pipe, 1.0 m long, 0.8 m in ground
GROUT_R, GROUT_L = 55.0, 450.0                   # 110 mm grout column around the lower pipe
CAPSULE_R, CAPSULE_L, CAPSULE_DEPTH = 17.0, 130.0, 300.0
HEAD_R, HEAD_L = 60.0, 170.0

stakes = capsules = heads = None
for sx in STAKE_X:
    gz = surface_z(sx)
    pipe = Pos(sx, 0, gz - EMBED + PIPE_L / 2) * Cylinder(PIPE_R, PIPE_L)
    grout = Pos(sx, 0, gz - EMBED + GROUT_L / 2) * (Cylinder(GROUT_R, GROUT_L) - Cylinder(PIPE_R, GROUT_L + 2))
    cap = Pos(sx, 0, gz - CAPSULE_DEPTH) * Cylinder(CAPSULE_R, CAPSULE_L)
    top = gz - EMBED + PIPE_L
    head = (Pos(sx, 0, top + HEAD_L / 2 - 40) * Cylinder(HEAD_R, HEAD_L)
            + Pos(sx + HEAD_R, 0, top + 20) * Rot(0, 90, 0) * Cylinder(14, 40))   # cable gland facing down-slope
    s = pipe + grout
    stakes = s if stakes is None else stakes + s
    capsules = cap if capsules is None else capsules + cap
    heads = head if heads is None else heads + head

# ---------------- 4: crack displacement gauge across the tension crack ----------------
GY = 900.0
a1, a2 = CRACK_X - 450, CRACK_X + 450
gauge = (Pos(a1, GY, CREST_Z - 200 + 150) * Cylinder(20, 700)          # anchor pins, 0.5 m in ground
         + Pos(a2, GY, CREST_Z - 200 + 150) * Cylinder(20, 700)
         + Pos(CRACK_X, GY, CREST_Z + 110) * Box(1000, 90, 60)          # guarded sensor body and rod
         + Pos(a1, GY, CREST_Z + 60) * Box(80, 120, 120)
         + Pos(a2, GY, CREST_Z + 60) * Box(80, 120, 120))
gauge_cover = Pos(CRACK_X, GY, CREST_Z + 170) * Box(1150, 200, 20)

# ---------------- 6 to 8: mast with FieldNode core and alert unit on the toe bench ----------------
MX, MY = 3400.0, -600.0
MAST_H = 3200.0
mast = (Pos(MX, MY, MAST_H / 2) * Cylinder(30, MAST_H)
        + Pos(MX, MY, -300) * Cylinder(160, 600))                        # concrete footing, 0.6 m deep
node_box = Pos(MX - 30 - 60, MY, 1500) * Box(120, 180, 220)
panel = Pos(MX - 30 - 60 - 60, MY, 2050) * Rot(0, -35, 0) * Box(260, 360, 25)
node = node_box + panel
siren = (Pos(MX, MY, MAST_H + 60) * Box(120, 120, 120)
         + Pos(MX, MY - 60 - 70, MAST_H + 60) * Rot(90, 0, 0) * Cylinder(55, 140)   # horn
         + Pos(MX, MY, MAST_H + 120 + 110) * Cylinder(55, 220))                    # beacon

# ---------------- 5: sensor bus cable in conduit, on the surface ----------------
def surf(x, y, lift=25.0):
    return (x, y, surface_z(x) + lift)


pts = [(STAKE_X[0] + 90, 0), (STAKE_X[1] + 90, 0), (STAKE_X[2] + 90, 0), (TOE_X, 0),
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
         + tube3(surf(STAKE_X[0] - 300, GY), surf(STAKE_X[0] + 90, 0), 10)
         + tube3((MX - 40, MY, 25), (MX - 40, MY, 1390), 10))

# Site scene: hero, blueprint and 3D viewer. BOM numbers on every SlopeWatch part.
parts = [
    Part("Ground: 25 degree slope with tension crack (site)", ground, GROUND, None),
    Part("Tilt stakes, pipe and grout (3)", stakes, STEEL, 1),
    Part("Tilt sensor capsules (3)", capsules, ACCENT, 2),
    Part("Stake heads with cable gland (3)", heads, "#D4A017", 3),
    Part("Crack displacement gauge", gauge + gauge_cover, "#7C3AED", 4),
    Part("Sensor bus cable in conduit", cable, "#111827", 5),
    Part("FieldNode core with 6 W panel", node, "#1E3A8A", 6),
    Part("Siren and beacon alert unit", siren, "#C2410C", 7),
    Part("Mast and footing", mast, "#94A3B8", 8),
]

# Person on the toe bench for scale (added as context so the figure stands on the bench,
# not at the bottom of the ground block where the kit helper would place it)
person = human_figure(1750.0, x=4700.0, y=700.0, z=0.0)
person.name = "1.75 m person"

render_all(
    parts, project="SlopeWatch", title="Slope movement monitor concept", dwg_no="SLW-DWG-010",
    key_figures=["3 grouted tilt stakes, 0.005 deg tilt sensitivity (sensor datasheet)",
                 "Precaution 0.01 deg/h, warning 0.1 deg/h tilt rate (proposed)",
                 "Crack gauge 100 mm range, 0.1 mm resolution",
                 "Reads every 10 min; siren within about 1 min (estimate)",
                 "About $380 per site with FieldNode, $254 without (indicative)"],
    cut=False, scale_figure=False, context=[person],
    flow={"title": "data and alert flow (latencies are estimates)", "unit": "min",
          "stages": [("Stakes, crack gauge", "read every 10 min"),
                     ("FieldNode at site", "rate vs threshold"),
                     ("LoRaWAN gateway", "hourly, 10 min on alert"),
                     ("Alert server", "inverse-velocity trend"),
                     ("People on alert list", "SMS, about 5 min")],
          "losses": [(1, "Local siren and beacon (estimate)", 1)]},
)



# ---------------- exploded view: one of each kit item laid out at a readable scale ----------------
# The site scene is about 10 m across, which makes a 48 mm stake too small to read, so the exploded
# view shows one stake, the crack gauge, a coil of bus cable and the mast set side by side.
def kit_layout():
    ex = []
    sx = 0.0
    pipe = Pos(sx, 0, PIPE_L / 2) * Cylinder(PIPE_R, PIPE_L)
    grout = Pos(sx, 0, GROUT_L / 2) * (Cylinder(GROUT_R, GROUT_L) - Cylinder(PIPE_R, GROUT_L + 2))
    cap = Pos(sx, 0, PIPE_L - CAPSULE_DEPTH + 120) * Cylinder(CAPSULE_R, CAPSULE_L)
    head = (Pos(sx, 0, PIPE_L + HEAD_L / 2 - 40) * Cylinder(HEAD_R, HEAD_L)
            + Pos(sx + HEAD_R, 0, PIPE_L + 20) * Rot(0, 90, 0) * Cylinder(14, 40))
    ex.append(Part("Tilt stake, pipe and grout (1 of 3)", pipe + grout, STEEL, 1))
    ex.append(Part("Tilt sensor capsule (1 of 3)", cap, ACCENT, 2, (0, 0, 650)))
    ex.append(Part("Stake head with cable gland (1 of 3)", head, "#D4A017", 3, (0, 0, 1050)))
    gx, gz = 1300.0, 0.0
    g = (Pos(gx - 450, 0, gz + 350) * Cylinder(20, 700) + Pos(gx + 450, 0, gz + 350) * Cylinder(20, 700)
         + Pos(gx, 0, gz + 800) * Box(1000, 90, 60)
         + Pos(gx - 450, 0, gz + 750) * Box(80, 120, 120) + Pos(gx + 450, 0, gz + 750) * Box(80, 120, 120)
         + Pos(gx, 0, gz + 860) * Box(1150, 200, 20))
    ex.append(Part("Crack displacement gauge", g, "#7C3AED", 4))
    coil = None
    for k in range(4):
        t = Pos(2550, 0, 320 + 18 * k) * Torus(260, 10)
        coil = t if coil is None else coil + t
    ex.append(Part("Sensor bus cable in conduit (coil)", coil, "#111827", 5))
    mx = 3500.0
    ex.append(Part("FieldNode core with 6 W panel",
                   Pos(mx - 90, 0, 1500) * Box(120, 180, 220)
                   + Pos(mx - 150, 0, 2050) * Rot(0, -35, 0) * Box(260, 360, 25), "#1E3A8A", 6, (-450, 0, 0)))
    ex.append(Part("Siren and beacon alert unit",
                   Pos(mx, 0, MAST_H + 60) * Box(120, 120, 120)
                   + Pos(mx, -130, MAST_H + 60) * Rot(90, 0, 0) * Cylinder(55, 140)
                   + Pos(mx, 0, MAST_H + 230) * Cylinder(55, 220), "#C2410C", 7, (0, 0, 450)))
    ex.append(Part("Mast and footing", Pos(mx, 0, MAST_H / 2) * Cylinder(30, MAST_H)
                   + Pos(mx, 0, -300) * Cylinder(160, 600), "#94A3B8", 8))
    return ex


_render(kit_layout(), concept.ROOT / "media" / "exploded.png", offsets=True, labels=True, azim=-70, elev=18,
        title="SlopeWatch: exploded view of one of each kit item",
        note="Numbers match bom/bom.csv. A site uses three stakes (items 1 to 3); item 9 (gateway and software) is not shown.")


# ---------------- cutaway: one tilt stake in the slope, cut on its axis ----------------
def stake_cutaway():
    gz = 0.0
    big = 6000.0
    cutter = Pos(0, big / 2, 0) * Box(big, big, big)
    # a 1.4 m block of slope around one stake; surface rises toward -X at the slope angle
    h = 700.0 * TAN
    blk = Polygon(*[(-700, -1300), (700, -1300), (700, -h), (-700, h)], align=None)
    block = extrude(Plane.XZ * blk, amount=450, both=True)
    bore = (Pos(0, 0, gz - EMBED + GROUT_L / 2) * Cylinder(GROUT_R, GROUT_L)
            + Pos(0, 0, gz - EMBED + PIPE_L / 2) * Cylinder(PIPE_R, PIPE_L))
    pipe = Pos(0, 0, gz - EMBED + PIPE_L / 2) * (Cylinder(PIPE_R, PIPE_L) - Cylinder(PIPE_R - 4, PIPE_L - 8))
    grout = Pos(0, 0, gz - EMBED + GROUT_L / 2) * (Cylinder(GROUT_R, GROUT_L) - Cylinder(PIPE_R, GROUT_L + 2))
    cap = Pos(0, 0, gz - CAPSULE_DEPTH) * Cylinder(CAPSULE_R, CAPSULE_L)
    potting = Pos(0, 0, gz - CAPSULE_DEPTH - CAPSULE_L / 2 - 60) * Cylinder(PIPE_R - 4, 120)
    top = gz - EMBED + PIPE_L
    head = (Pos(0, 0, top + HEAD_L / 2 - 40) * (Cylinder(HEAD_R, HEAD_L) - Pos(0, 0, -10) * Cylinder(HEAD_R - 5, HEAD_L - 10))
            + Pos(HEAD_R, 0, top + 20) * Rot(0, 90, 0) * Cylinder(14, 40))
    lead = tube3((0, 0, gz - CAPSULE_DEPTH + CAPSULE_L / 2), (0, 0, top + 40), 4) \
        + tube3((0, 0, top + 40), (HEAD_R + 20, 0, top + 20), 4)
    ps = [Part("Slope soil (site)", block - bore, GROUND, None),
          Part("Tilt stake: 48 mm pipe in 110 mm grout column", pipe + grout, STEEL, 1),
          Part("Tilt sensor capsule, about 300 mm below ground", cap, ACCENT, 2),
          Part("Stake head with cable gland", head, "#D4A017", 3),
          Part("Bus lead from capsule to gland", lead, "#111827", 5),
          Part("Foam plug below capsule", potting, "#E5E7EB", None)]
    out = []
    for p in ps:
        s = p.shape & cutter
        if s.volume > 1e-6:
            out.append(Part(p.name, s, p.color, p.bom))
    return out


_render(stake_cutaway(), concept.ROOT / "media" / "cutaway.png", azim=-90, elev=8, labels=True,
        title="SlopeWatch: cutaway of one tilt stake",
        note="Section on the stake axis. Burying the capsule damps the daily temperature swing that shifts the sensor offset.")
