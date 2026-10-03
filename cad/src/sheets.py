"""SlopeWatch general arrangement sheet SLW-DWG-001, Rev P5 (TRL 3, constructable design SLW-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/SLW-DWG-001.svg, .pdf and .png from the parametric model in cad/src/model.py
with .kit/drawing.py. Dimensions come from PARAMS and derived(), so they follow any parameter
change. The concept blueprint in media/ is SLW-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, SITE, arrangement, stake, derived  # noqa: E402

DATE = "2026-09-25"
DATE4 = "2026-10-01"
DATE5 = "2026-10-02"


def safe_views(part, workdir, names=("front", "top", "right", "iso"), line_weight=0.35):
    """Like drawing.project_views, but edge by edge so a degenerate projected edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name in names:
        origin, up = setups[name]
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected {', '.join(names)}; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    dl = 11   # room Sheet.add_ortho reserves for its overall dimensions
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.2
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.45 l0 0.9 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.45 l0 0.9 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.1, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.2
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.45 {a} l0.9 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.45 {-a} l0.9 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.1, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.0, 400, INK, anchor)]


def stake_section():
    """Half of one stake (y >= 0), viewed from -Y so the cut face shows."""
    from build123d import Box, Compound, Pos
    cutter = Pos(0, 500, 0) * Box(2000, 1000, 4000)
    return Compound(children=[s & cutter for s in stake().values()])


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = arrangement()
    views = safe_views(asm, work)
    sec = safe_views(stake_section(), work / "section", names=("front",))
    bb = asm.bounding_box()
    s = Sheet(project="SlopeWatch", title="General arrangement", dwg_no="SLW-DWG-001", rev="P5",
              author="Amish Chadha", date=DATE5, scale=None, theme="technical",
              material="Galvanized steel, cement grout, bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Keyed switch on own post 5 m from mast; mast a site option (DDR-002)", DATE, "AC"),
                         ("P3", "Layout and labels tidied", DATE, "AC"),
                         ("P4", "Constructable design (DDR-003)", DATE4, "AC"),
                         ("P5", "SLW-DEC-001: stake head marking, back plate wall holes", DATE5, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    xs, xg, xm, xw = P["arr_x"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zg = Z(0)
    L.append(f'<line x1="{x - 8:.2f}" y1="{zg:.2f}" x2="{x + w + 4:.2f}" y2="{zg:.2f}" stroke="{INK}" stroke-width="0.35"/>')
    L.append(_t(X(xm) - 3, zg - 1, "GROUND", 1.9, 600, MUTED, "end"))
    # mast heights on the right of the mast
    xr = X(bb.max.X) + 4
    for i, (zz, label) in enumerate(((D["alert_top"], f"{D['alert_top']:,.0f} top of beacon"),
                                     (P["mast_h"], f"{P['mast_h']:,.0f} mast"),
                                     (P["node_z0"], f"{P['node_z0']:,.0f} node"))):
        xd = xr + 5 * i
        L.append(ext(X(xm), Z(zz), xd + 1, Z(zz)))
        L += dim_v(xd, Z(zz), zg, label, side=1)
    L += dim_v(X(xm - P["footing"][0] / 2) - 3, zg, Z(-P["footing"][1]), f"{P['footing'][1]:.0f}")
    # stake depths on the left of the stake
    xl = X(bb.min.X) - 4
    L.append(ext(X(xs), Z(-P["embed"]), xl - 1, Z(-P["embed"])))
    L += dim_v(xl, zg, Z(-P["embed"]), f"{P['embed']:.0f} embed")
    L.append(ext(X(xs), Z(-P["capsule_depth"]), xl - 7, Z(-P["capsule_depth"])))
    L += dim_v(xl - 6, zg, Z(-P["capsule_depth"]), f"{P['capsule_depth']:.0f} capsule")
    # spacing along X
    zt = Z(-950)
    L += dim_h(X(xs), X(xg), zt, f"{xg - xs:,.0f}")
    L += dim_h(X(xg), X(xm), zt, f"{xm - xg:,.0f}")
    L += leader(X(xs), Z(D["head_top"]), X(xs) - 2, Z(1700), "1-3 TILT STAKE (DETAIL A)", "end")
    L += leader(X(xg) + 5, Z(P["gauge_z"] + 70), X(xg) + 8, Z(450), "4 CRACK GAUGE")
    L += leader(X(xm), Z(D["panel_cz"]), X(xm) - 12, Z(D["panel_cz"] + 500), "6 FIELDNODE CORE", "end")
    L += leader(X(xm), Z(D["siren_z"] + 200), X(xm) - 12, Z(P["mast_h"] + 700), "7 ALERT UNIT, SIDE MOUNTED", "end")
    L += leader(X(xw), Z(P["switch_z"] + 40), X(xw) - 4, Z(P["switch_z"] + 1100), "7 KEYED SWITCH POST", "end")
    L += leader(X(xm), Z(1000), X(xm) - 12, Z(1200), "8 MAST (SITE OPTION)", "end")

    # top view: note the facing
    x, y, w, h = c["top"]
    L.append(_t(x + w / 2, y + h + 14.5, "+X DOWNSLOPE ON SITE; NODE AND HORN FACE -Y", 1.8, 400, MUTED, "middle"))

    s._layers += L
    # detail A: stake section at 1:10 in the right column
    s.add_svg(sec["front"], 290, 40, 40, 120, scale=0.1, label="Detail A", sublabel="Stake section, scale 1:10")
    dx0, dy0 = 290, 40
    vx, vy, vw, vh = _viewbox(Path(sec["front"]).read_text())
    sbb = stake_section().bounding_box()
    kx = 0.1
    bx = dx0 + (40 - vw * kx) / 2
    by = dy0 + (120 - vh * kx) / 2
    SX = lambda mx: bx + (mx - sbb.min.X) * kx
    SZ = lambda mz: by + vh * kx - (mz - sbb.min.Z) * kx
    D2 = []
    D2.append(f'<line x1="{SX(sbb.min.X) - 4:.2f}" y1="{SZ(0):.2f}" x2="{SX(sbb.max.X) + 4:.2f}" y2="{SZ(0):.2f}" stroke="{INK}" stroke-width="0.3"/>')
    xr2 = SX(sbb.max.X) + 5
    D2 += leader(SX(P["capsule"][0] / 2 - 2), SZ(-P["capsule_depth"]), xr2 + 3, SZ(-P["capsule_depth"]), f"2 CAPSULE {P['capsule'][0]:.0f} x {P['capsule'][1]:.0f}")
    D2 += leader(SX(D["pipe_id"] / 2 - 3), SZ(D["cap_top"] + 50), xr2 + 3, SZ(D["cap_top"] + 110), "FOAM PLUG")
    D2 += leader(SX(P["stand"][0] / 2 - 1), SZ(-P["embed"] + 120), xr2 + 3, SZ(-P["embed"] + 90), "STAND TUBE 40")
    D2 += leader(SX(P["grout_d"] / 2 - 5), SZ(-P["embed"] + 200), xr2 + 3, SZ(-P["embed"] + 200), f"GROUT {P['grout_d']:.0f} x {P['grout_l']:.0f}")
    D2 += leader(SX(P["pipe"][0] / 2), SZ(-80), xr2 + 3, SZ(-40), f"1 PIPE {P['pipe'][0]} x {P['pipe'][1]}")
    D2 += leader(SX(P["head"][0] / 2 - 2), SZ(D["head_top"] - 40), xr2 + 3, SZ(D["head_top"]), f"3 HEAD {P['head'][0]:.0f}, CONDUIT IN AND OUT")
    D2 += dim_v(SX(sbb.min.X) - 3, SZ(D["head_top"]), SZ(0), f"{D['head_top']:.0f}")
    D2.append(_t(SX(0), SZ(0) - 1.2, "GROUND", 1.6, 600, MUTED, "middle"))
    s._layers += D2
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Stake {P['pipe'][0]} x {P['pipe'][1]} galv. pipe, {P['pipe_l']:.0f} long, {P['embed']:.0f} in ground, screwed end cap",
        f"Hole {P['grout_d']:.0f} dia x {D['hole_depth']:.0f}; grout {D['grout_vol_l']:.1f} L; capsule {P['capsule_depth']:.0f} deep on stand tube",
        f"Crack gauge: anchors {P['anchor_span']:.0f} apart, pins {P['pin_d']:.0f} x {P['pin_l']:.0f}, stroke {P['stroke']:.0f}",
        f"Mast (option) {P['mast'][0]} x {P['mast'][1]}, {P['mast_h']:,.0f} high; footing {P['footing'][0]:.0f} x {P['footing'][1]:.0f}",
        f"Switch post {P['switch_post'][0]} dia, {P['switch_post'][2]:,.0f} high, {P['switch_offset'] / 1000:.0f} m from mast on site",
        f"FieldNode massing per FND-DDR-003; node bottom {P['node_z0']:,.0f}; alert unit on V-blocks and bands",
        f"Bus 4-core 0.5 mm2 on the 5 V port; stakes {SITE['stake_spacing_m']:.0f} m apart, cable {D['cable_m']:.0f} m on site",
    ], x=276, y=171, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "SLW-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
