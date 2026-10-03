"""SlopeWatch sizing calculations, SLW-CAL-001 v0.3 (TRL 3, with the SLW-DDR-002 decisions and the
constructable design of SLW-DDR-003).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
Each printed line carries a tag such as [B3] that the note cites. Geometry comes from
cad/src/model.py (PARAMS, SITE and derived), the parts cost from bom/bom.csv and the budget from
project.yaml. First-principles estimates for a paper proof of concept; not a substitute for tests.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, SITE, derived  # noqa: E402

D = derived(P)


def tag(t, text):
    print(f"[{t}] {text}")


def db_sum(levels):
    return 10 * math.log10(sum(10 ** (x / 10) for x in levels))


print("SlopeWatch sizing, SLW-CAL-001 v0.3")
print(f"Geometry from cad/src/model.py: pipe {P['pipe'][0]} x {P['pipe'][1]} mm, capsule center "
      f"{P['capsule_depth']:.0f} mm deep, mast {P['mast_h']:.0f} mm, reference-site cable {D['cable_m']:.1f} m")

# ------------------------------------------------------------------ A. Tilt measurement (R1)
print("\nA. Tilt measurement")
# SCL3300-D01 datasheet, mode 1: +-1.2 g (+-90 deg), noise density 0.0024 deg/rtHz, angle output
# 0.0055 deg/LSB; modes 3 and 4 (inclination modes) are limited to +-10 deg.
ND_MODE1 = 0.0024          # deg/sqrt(Hz)
LSB = 90 / 2 ** 14          # deg per LSB of the angle output
T_AVG = 10.0                # s averaging per reading
sigma = ND_MODE1 * math.sqrt(1 / (2 * T_AVG))
tag("A1", f"angle output step {LSB:.4f} deg; mode 1 range +-90 deg (modes 3 and 4 only +-10 deg)")
tag("A2", f"noise over a {T_AVG:.0f} s average in mode 1: {sigma:.5f} deg (1 sigma)")


def slope_sigma(n, dt_h):
    t = [i * dt_h for i in range(n)]
    tm = sum(t) / n
    return sigma / math.sqrt(sum((x - tm) ** 2 for x in t))


s1 = slope_sigma(7, 1 / 6)
s3 = slope_sigma(19, 1 / 6)
tag("A3", f"tilt-rate noise, least squares over 1 h (7 readings): {s1:.5f} deg/h, {0.1 / s1:.0f} x below the 0.1 deg/h warning")
tag("A4", f"tilt-rate noise over 3 h (19 readings): {s3:.6f} deg/h, {0.01 / s3:.0f} x below the 0.01 deg/h precaution")
stake_len_above_pivot = 1.0   # m, a rotation of the stake read as displacement at 1 m
tag("A5", f"warning rate 0.1 deg/h is {math.radians(0.1) * stake_len_above_pivot * 1000:.2f} mm/h at 1 m; "
          f"precaution over 3 h is {0.03:.2f} deg, {0.03 / LSB:.1f} output steps")

# ------------------------------------------------------------------ B. Temperature drift (R2)
print("\nB. Temperature drift of a buried capsule")
DRIFT = 0.005               # deg/K, SCL3300 offset temperature drift (Murata product page)
OMEGA = 2 * math.pi / 86400
SOIL = {"dry": (0.3e-6, 0.4), "moist": (0.6e-6, 1.0), "wet": (1.0e-6, 1.6)}   # diffusivity m2/s, k W/mK
# pipe conduction from a sunlit exposed pipe length into the ground (fin model)
A_SUN, G_SUN, H_AIR, K_STEEL = 0.6, 900.0, 10.0, 50.0
exposed = (D["stake_top"] - P["head_overlap"]) / 1000          # m of bare pipe between ground and head
od = P["pipe"][0] / 1000
q_abs = A_SUN * G_SUN * od * exposed
g_air = H_AIR * math.pi * od * exposed
kA = K_STEEL * D["pipe_area_mm2"] / 1e6
tag("B1", f"exposed pipe {exposed * 1000:.0f} mm absorbs {q_abs:.2f} W in full sun; air loss {g_air:.3f} W/K")
R2_DAY, R2_HOUR = 0.02, 0.002


def drift_case(depth_m, soil, surf_range):
    alpha, k_soil = SOIL[soil]
    dd = math.sqrt(2 * alpha / OMEGA)
    soil_range = surf_range * math.exp(-depth_m / dd)
    gp = 2 * math.pi * k_soil / math.log(2 * depth_m / (P["grout_d"] / 2000))
    m = math.sqrt(gp / kA)
    dT0 = q_abs / (g_air + kA * m)
    pipe_excess = dT0 * math.exp(-m * depth_m)
    rng = soil_range + pipe_excess
    day = rng * DRIFT
    rate = rng / 2 * OMEGA * 3600 * DRIFT
    return dd, soil_range, dT0, pipe_excess, rng, day, rate


rows_b = []
for depth in (0.3, P["capsule_depth"] / 1000):
    for soil, srange in (("dry", 30.0), ("moist", 20.0), ("wet", 20.0)):
        dd, sr, dT0, pe, rng, day, rate = drift_case(depth, soil, srange)
        ok = day <= R2_DAY and rate <= R2_HOUR
        rows_b.append((depth, soil, srange, dd, sr, pe, rng, day, rate, ok))
for i, (depth, soil, srange, dd, sr, pe, rng, day, rate, ok) in enumerate(rows_b, 1):
    tag(f"B2.{i}", f"depth {depth:.1f} m, {soil} soil, surface range {srange:.0f} K: damping depth {dd * 1000:.0f} mm, "
                   f"soil range {sr:.2f} K, pipe adds {pe:.2f} K, total {rng:.2f} K; {day:.4f} deg/day, "
                   f"peak {rate:.5f} deg/h -> {'meets' if ok else 'MISSES'} R2")
_, _, dT0, _, _, _, _ = drift_case(0.4, "moist", 20.0)
tag("B3", f"pipe at ground level runs up to {dT0:.1f} K above the soil in full sun (steady state, no heat capacity)")
unb = 20.0 * DRIFT
tag("B4", f"unburied sensor, 20 K range: {unb:.3f} deg/day, peak {unb / 2 * OMEGA * 3600:.4f} deg/h")
wet4 = [r for r in rows_b if r[0] == P["capsule_depth"] / 1000 and r[1] == "wet"][0]
tag("B5", f"design case (0.4 m, wet): rate margin {R2_HOUR / wet4[8]:.2f} x, daily margin {R2_DAY / wet4[7]:.2f} x; "
          f"precaution threshold is {0.01 / wet4[8]:.1f} x the thermal rate")

# ------------------------------------------------------------------ C. Crack gauge (R3)
print("\nC. Crack gauge")
stroke = P["stroke"]
step = stroke / 4096
lin = 0.001 * stroke
body_l = P["gauge_body"][1]
rod_l = D["rod_l"]                      # steel extension rod between the coupling and the downslope ball joint (SLW-DDR-003)
alpha_rod, alpha_body = 12e-6, 23e-6
dT_gauge = 30.0
d_th = (rod_l * alpha_rod + body_l * alpha_body) * dT_gauge
tag("C1", f"12-bit step {step:.4f} mm; linearity error 0.1 % class {lin:.2f} mm over {stroke:.0f} mm")
tag("C2", f"steel rod {rod_l:.0f} mm and aluminum body {body_l:.0f} mm under the guard, {dT_gauge:.0f} K daily range: "
          f"{d_th:.2f} mm apparent daily swing, peak {d_th / 2 * OMEGA * 3600:.3f} mm/h")
tag("C3", f"over a 3 h window the thermal swing reads as up to {d_th / 2 * OMEGA * 3600 * 24:.2f} mm/day against the "
          f"1 mm/day precaution placeholder; over a 24 h window it cancels")
tag("C4", f"warning placeholder 1 mm/h is {1 / (d_th / 2 * OMEGA * 3600):.0f} x the thermal rate; "
          f"at 1 mm/h the {stroke:.0f} mm stroke lasts {stroke:.0f} h")

# ------------------------------------------------------------------ D. Sampling, airtime and latency (R4, R5, R6)
print("\nD. Sampling, airtime and alert latency")


def lora_airtime(pl, sf, bw=125e3, cr=1, preamble=8):
    de = 1 if sf >= 11 else 0
    ts = 2 ** sf / bw
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (preamble + 4.25) * ts + n * ts


PAYLOAD = 20
PHY = PAYLOAD + 13
air = {sf: lora_airtime(PHY, sf) for sf in (7, 9, 10, 12)}
tag("D1", "airtime, 20-byte payload: " + ", ".join(f"SF{k} {v * 1000:.0f} ms" for k, v in air.items()))
for sf in (10, 12):
    hr = 6 * air[sf]
    tag(f"D2.{sf}", f"SF{sf}, 6 uplinks per hour: {hr:.1f} s per hour, {hr / 3600 * 100:.2f} % of time (EU868 limit 1 %)")
day_norm = {sf: 24 * air[sf] for sf in (9, 10, 12)}
day_alert = {sf: 144 * air[sf] for sf in (9, 10, 12)}
tag("D3", "per day, hourly (normal): " + ", ".join(f"SF{k} {v:.1f} s" for k, v in day_norm.items())
    + "; every 10 min (precaution or warning): " + ", ".join(f"SF{k} {v:.1f} s" for k, v in day_alert.items())
    + "; The Things Network fair use 30 s/day")
t_bus = 2.0 + T_AVG + 4 * 0.1          # power-up, averaging, poll four devices
t_decide = 0.5
t_siren = t_bus + t_decide + 0.5
tag("D4", f"node time from start of the confirming reading to siren: {t_siren:.1f} s (R5 limit 60 s)")
T_NS, T_ALERT_SVC, T_SMS = 5.0, 30.0, 60.0
for sf in (10, 12):
    first = air[sf] + T_NS + T_ALERT_SVC + T_SMS
    wait = air[sf] * (1 / 0.01 - 1)
    retry = first + wait + air[sf]
    tag(f"D5.{sf}", f"SF{sf}: warning to SMS {first:.0f} s at the first try; with one lost uplink and the duty-cycle "
                    f"wait of {wait:.0f} s, {retry:.0f} s ({retry / 60:.1f} min) against 5 min")

# ------------------------------------------------------------------ E. Alarm reach (R7)
print("\nE. Alarm reach")
LW1 = 110.0                 # dB(A) at 1 m, typical 12 V piezo siren
ALPHA_AIR = 0.015           # dB/m near 3 kHz (order of magnitude from ISO 9613-1 tables)
GROUND = (0.0, 3.0)         # dB excess ground attenuation, hard to soft ground


def spl(r, g):
    return LW1 - 20 * math.log10(r) - ALPHA_AIR * r - g


tag("E1", f"at 100 m: {spl(100, GROUND[1]):.1f} to {spl(100, GROUND[0]):.1f} dB(A) against 65 dB(A)")
r65 = [next(r for r in range(1, 2000) if spl(r, g) < 65) - 1 for g in GROUND]
tag("E2", f"65 dB(A) reached out to about {r65[1]} to {r65[0]} m")
BG = 80.0
need = BG + 15
r_mach = next(r for r in range(1, 500) if spl(r, 0) < need) - 1
tag("E3", f"near running plant ({BG:.0f} dB(A) background) an alarm 15 dB above ambient ({need:.0f} dB(A)) reaches only "
          f"about {r_mach} m from the mast")
h_s = D["siren_z"]                      # siren centre on the side-mounted alert box (SLW-DDR-003)


def niosh_min(lp):
    return 8 * 60 / 2 ** ((lp - 85) / 3)


r_old = math.hypot((h_s - 1600) / 1000, 0.3)          # TRL 3 v0.1: switch box on the mast
r_switch = math.hypot((h_s - 1600) / 1000, P["switch_offset"] / 1000)   # SLW-DDR-002: own post about 5 m away
r_base = math.hypot((h_s - 1600) / 1000, 2.0)
lp_old, lp_sw = spl(r_old, 0), spl(r_switch, 0)
tag("E4", f"at a switch on the mast (ear 1.6 m, 0.3 m out): {lp_old:.1f} dB(A), NIOSH 85 dB(A) 8 h with 3 dB exchange "
          f"allows {niosh_min(lp_old):.1f} min; 2 m from the mast {spl(r_base, 0):.1f} dB(A)")
tag("E5", f"at the keyed switch on its own post {P['switch_offset'] / 1000:.0f} m from the mast (SLW-DDR-002): "
          f"{lp_sw:.1f} dB(A), NIOSH allows {niosh_min(lp_sw):.0f} min; lead {P['switch_lead_m']:.0f} m")

# ------------------------------------------------------------------ F. Energy and rail current (R8)
print("\nF. Energy and rail current")
RAIL_EFF = 0.90             # FieldNode rail converters (FND-CAL-001)
V5, V12 = 5.0, 12.0
I_CAP, I_READER, I_POT = 0.006, 0.005, 0.0005
T_ON = 2.0 + T_AVG
e_cycle = (3 * I_CAP + I_READER + I_POT) * V5 * T_ON + 4 * 0.05 * V5 * 0.033
p_sens = e_cycle / RAIL_EFF / 600
tag("F1", f"sensor bus {T_ON:.0f} s per 10 min reading: {e_cycle:.2f} J at the 5 V rail, {p_sens * 1000:.2f} mW average "
          f"from the cell, {p_sens * 24:.3f} Wh/day")
I_TX, V_RADIO = 0.045, 3.3
e_up = {sf: I_TX * V_RADIO * air[sf] for sf in (10, 12)}
e_alert_up = 144 * e_up[12] / 3600
tag("F2", f"extra uplinks every 10 min at SF12: {e_alert_up * 1000:.1f} mWh/day (hourly uplinks are inside the FieldNode "
          f"core budget, which assumes 15 min reports)")
I_SIREN, I_BEACON = 0.25, 0.20
p_alarm = (I_SIREN + I_BEACON) * V12
p_alarm_cell = p_alarm / RAIL_EFF
e_alarm = p_alarm_cell * 0.5
e_silenced = I_BEACON * V12 * 0.5 / RAIL_EFF * 0.5
tag("F3", f"alarm {p_alarm:.1f} W at 12 V, {p_alarm_cell:.1f} W from the cell; 30 min alarm {e_alarm:.2f} Wh; "
          f"30 min silenced with the beacon at 50 % duty {e_silenced:.2f} Wh")
duty = {0.05: None, 0.01: None}
for dty in duty:
    duty[dty] = I_BEACON * V12 * dty / RAIL_EFF
tag("F4", "precaution beacon (slow flash): " + "; ".join(f"{d * 100:.0f} % duty {p * 1000:.1f} mW, {p * 24:.2f} Wh/day"
                                                        for d, p in duty.items()))
CORE = 0.004                 # Wh/day, FieldNode core (FND-CAL-001)
CELL_USABLE = 3.2 * 6.0 * 0.80
COLD = 0.85                  # capacity factor at -10 degC (assumed)
days = 5
e_norm = days * (CORE + p_sens * 24) + e_alarm + e_silenced
e_prec = {d: days * (CORE + p_sens * 24 + e_alert_up + p * 24) + e_alarm + e_silenced for d, p in duty.items()}
tag("F5", f"cell usable {CELL_USABLE:.2f} Wh, {CELL_USABLE * COLD:.2f} Wh at -10 degC")
tag("F6", f"5 days no sun, normal state plus one alarm: {e_norm:.2f} Wh ({e_norm / (CELL_USABLE * COLD) * 100:.0f} % of the cold usable energy)")
for d, e in e_prec.items():
    tag(f"F7.{int(d * 100)}", f"5 days no sun, all in precaution with beacon at {d * 100:.0f} % duty, plus one alarm: {e:.2f} Wh "
                              f"({e / (CELL_USABLE * COLD) * 100:.0f} % of cold usable) -> {'meets' if e <= CELL_USABLE * COLD else 'MISSES'} R8")
avg_prec = p_sens + e_alert_up / 24 + duty[0.01]
tag("F8", f"average load in precaution at 1 % duty: {avg_prec * 1000:.1f} mW against the FieldNode 100 mW sensor allowance")
V_CELL_LOW = 3.0
i_cell = p_alarm_cell / V_CELL_LOW
tag("F9", f"alarm draws {I_SIREN + I_BEACON:.2f} A from the 12 V rail and {i_cell:.2f} A from the cell at {V_CELL_LOW} V "
          f"({i_cell / 6:.2f} C; FieldNode cell fuse 5 A); 12 V rail rating not stated by FieldNode")

# ------------------------------------------------------------------ G. Bus cable (R9, R4)
print("\nG. Sensor bus cable")
RHO_CU = 0.0172             # ohm mm2/m
A_CORE = 0.5
r_loop = 2 * D["cable_m"] * RHO_CU / A_CORE
i_bus = 3 * I_CAP + I_READER + I_POT
tag("G1", f"reference layout: fall line {D['fall_m']:.0f} m ({D['rise_m']:.1f} m rise at {SITE['slope_deg']:.0f} deg), "
          f"cable {D['cable_m_net']:.1f} m plus {SITE['slack'] * 100:.0f} % slack = {D['cable_m']:.1f} m (BOM 60 m)")
tag("G2", f"loop resistance {r_loop:.2f} ohm; {i_bus * 1000:.1f} mA with every device at the far end drops "
          f"{r_loop * i_bus:.3f} V of 5 V; a 3.3 V LDO with 0.3 V dropout keeps {V5 - r_loop * i_bus - 3.6:.2f} V margin")
tag("G3", f"RS-485 run {D['cable_m']:.0f} m against the 1,200 m class limit at low data rates")

# ------------------------------------------------------------------ H. Mast, wind and footing
print("\nH. Mast in wind")
V_GUST, RHO_AIR = 35.0, 1.2
q = 0.5 * RHO_AIR * V_GUST ** 2
pw, pl, _ = P["panel"]


def mast_case(Do, t, V=V_GUST):
    """Loads, base moment, stress and top deflection of the mast on a given pipe in a gust of V m/s."""
    q_ = 0.5 * RHO_AIR * V ** 2
    ld = [
        ("panel", pw * pl / 1e6, 1.2, D["panel_cz"] / 1000),
        ("node enclosure", P["node"][0] * P["node"][2] / 1e6, 1.3, D["node_zc"] / 1000),
        ("alert box, horn, beacon and back plate", (P["alert_box"][0] * P["alert_box"][2] + P["horn"][0] * P["horn"][1]
                                                    + P["beacon"][0] * P["beacon"][1]
                                                    + P["alert_plate"][0] * (P["alert_plate"][1] - P["alert_box"][2])) / 1e6,
         1.2, D["alert_zc"] / 1000),
        ("mast", Do * P["mast_h"] / 1e6, 1.2, P["mast_h"] / 2000),
    ]
    Fs = [(n, q_ * A * cd, z) for n, A, cd, z in ld]
    Ft = sum(f for _, f, _ in Fs)
    Mb = sum(f * z for _, f, z in Fs)
    Zs_ = math.pi * (Do ** 4 - (Do - 2 * t) ** 4) / (32 * Do) / 1e9
    I_ = Zs_ * Do / 2 / 1000
    Lm = P["mast_h"] / 1000
    df = sum(f * (z ** 2) * (3 * Lm - z) / (6 * 200e9 * I_) for _, f, z in Fs)
    st_ = Mb / Zs_ / 1e6
    return dict(F=Fs, Ftot=Ft, M=Mb, Zs=Zs_, stress=st_, factor=235 / st_, defl=df)


loads = [
    ("panel", pw * pl / 1e6, 1.2, D["panel_cz"] / 1000),
    ("node enclosure", P["node"][0] * P["node"][2] / 1e6, 1.3, D["node_zc"] / 1000),
    ("alert box, horn, beacon and back plate", (P["alert_box"][0] * P["alert_box"][2] + P["horn"][0] * P["horn"][1]
                                                + P["beacon"][0] * P["beacon"][1]
                                                + P["alert_plate"][0] * (P["alert_plate"][1] - P["alert_box"][2])) / 1e6,
     1.2, D["alert_zc"] / 1000),
    ("mast", P["mast"][0] * P["mast_h"] / 1e6, 1.2, P["mast_h"] / 2000),
]
F = [(n, q * A * cd, z) for n, A, cd, z in loads]
Ftot = sum(f for _, f, _ in F)
M = sum(f * z for _, f, z in F)
tag("H1", f"gust {V_GUST:.0f} m/s, {q:.0f} Pa: " + ", ".join(f"{n} {f:.0f} N" for n, f, _ in F)
    + f"; total {Ftot:.0f} N, base moment {M:.0f} N m")
Do, t = P["mast"]
Di = Do - 2 * t
Zs = math.pi * (Do ** 4 - Di ** 4) / (32 * Do) / 1e9
I = Zs * Do / 2 / 1000
stress = M / Zs / 1e6
tag("H2", f"mast {Do} x {t} mm: section modulus {Zs * 1e6:.2f} cm3, stress {stress:.0f} MPa, factor {235 / stress:.1f} on 235 MPa yield")
E = 200e9
L = P["mast_h"] / 1000
defl = sum(f * (z ** 2) * (3 * L - z) / (6 * E * I) for _, f, z in F)
tag("H3", f"top deflection in the gust {defl * 1000:.0f} mm ({defl / L * 1000:.0f} mm per m)")
fd, fdep = P["footing"][0] / 1000, P["footing"][1] / 1000
GAMMA, KP = 18000.0, 3.0
e_arm = M / Ftot
H_ult = 0.5 * GAMMA * fd * fdep ** 3 * KP / (e_arm + fdep)
m48 = mast_case(48.3, 3.2)
m60 = mast_case(60.3, 3.6)
tag("H2b", f"site mast 60.3 x 3.6 mm (SLW-DEC-001, 2026-10-02), same 35 m/s gust: total {m60['Ftot']:.0f} N, base moment {m60['M']:.0f} N m, "
           f"section modulus {m60['Zs'] * 1e6:.2f} cm3, stress {m60['stress']:.0f} MPa, factor {m60['factor']:.1f} on 235 MPa yield, "
           f"top deflection {m60['defl'] * 1000:.0f} mm")
v_yield48 = V_GUST * math.sqrt(m48["factor"])
v_yield60 = V_GUST * math.sqrt(m60["factor"])
v_f2 = V_GUST * math.sqrt(m48["factor"] / 2.0)
tag("H2c", f"local gust condition: stress grows with the square of the gust; the 48.3 mm mast reaches yield at {v_yield48:.0f} m/s and has a factor "
           f"of 2.0 at {v_f2:.0f} m/s; the 60.3 mm mast reaches yield at {v_yield60:.0f} m/s. A site installation uses the 60.3 mm mast unless "
           f"the local 3 s design gust is below {v_f2:.0f} m/s (factor 2.0 or better on the 48.3 mm mast); at {m48['factor']:.1f} the 48.3 mm mast "
           f"is for the fenced test slope only, with no one under the mast in high wind")
tag("H4", f"footing {fd * 1000:.0f} mm x {fdep * 1000:.0f} mm in medium soil: lateral capacity {H_ult:.0f} N "
          f"(load at {e_arm:.2f} m), factor {H_ult / Ftot:.1f}")
e60 = m60["M"] / m60["Ftot"]
H60 = 0.5 * GAMMA * fd * fdep ** 3 * KP / (e60 + fdep)
tag("H4b", f"the same footing under the 60.3 mm mast: load {m60['Ftot']:.0f} N at {e60:.2f} m, capacity {H60:.0f} N, factor {H60 / m60['Ftot']:.1f}")

# ------------------------------------------------------------------ I. Installation (R10)
print("\nI. Installing one stake")
tag("I1", f"hole {P['grout_d']:.0f} mm x {D['hole_depth']:.0f} mm, {D['hole_vol_l']:.1f} L of spoil; grout {D['grout_vol_l']:.2f} L, "
          f"about {D['grout_vol_l'] * 2.0:.1f} kg of dry mix")
tasks = [("auger the hole (about 55 mm/min in residual soil)", D["hole_depth"] / 55),
         ("mix grout by hand", 5), ("set the pipe plumb, pour and rod the grout", 5),
         ("backfill and tamp the upper hole", 8), ("fit stand tube, capsule with collars and plug; tape, head and conduit fittings; connect the bus", 8),
         ("check the reading on a handheld", 3)]
tt = sum(m for _, m in tasks)
tag("I2", "; ".join(f"{n} {m:.0f} min" for n, m in tasks) + f"; total {tt:.0f} min against 45 min")
tag("I3", "grout sets for 24 h before the baseline starts (not counted in R10)")

# ------------------------------------------------------------------ J. Data (R12)
print("\nJ. Data")
rec = 4 + 3 * 6 + 2 + 2 + 2
per_day = 144
flash = rec * per_day * 90
csv_line = 80
tag("J1", f"record {rec} B per reading; 90 days {flash / 1000:.0f} kB binary, {csv_line * per_day * 90 / 1e6:.2f} MB as CSV; "
          f"FieldNode flash 16 MB")

# ------------------------------------------------------------------ K. Cost (R11)
print("\nK. Cost")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
budget = None
for line in (ROOT / "project.yaml").read_text().splitlines():
    if line.startswith("budget_usd:"):
        budget = float(line.split(":")[1].split("#")[0])


def line_no(r):
    return int(r["item"].split()[0])


cost = {line_no(r): float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows}
OPTIONS = {n: c for n, c in cost.items() if n >= 11}        # lines 11 and up are site options, outside every total
cost = {n: c for n, c in cost.items() if n < 11}
total = sum(cost.values())
fn = cost.get(6, 0.0)
specific = total - fn
no_mast = specific - cost.get(8, 0.0)       # reference site since SLW-DDR-002: existing pole, mast is a site option
tag("K1", f"BOM {len(rows)} lines, all priced ({len(cost)} in the totals, {len(OPTIONS)} site options outside them); total with FieldNode core and the optional mast ${total:.2f}")
tag("K2", f"value-engineering target ${budget:.0f} (budget_usd, a hypothetical control target); estimated cost of the "
          f"constructable design, reference site (SlopeWatch-specific parts, existing pole, FieldNode costed in FieldNode) "
          f"${no_mast:.2f}: ${abs(budget - no_mast):.2f} {'under' if no_mast <= budget else 'over'} the target "
          f"({(no_mast / budget - 1) * 100:+.1f} %)")
tag("K3", f"site option, new mast and footing (line 8) +${cost.get(8, 0.0):.2f}: ${specific:.2f}, "
          f"${abs(budget - specific):.2f} {'under' if specific <= budget else 'over'} the target; "
          f"reference site with the FieldNode core ${no_mast + fn:.2f}")
tag("K3b", "site options outside every total: " + "; ".join(f"line {n} ${c:.2f}" for n, c in sorted(OPTIONS.items()))
    + f"; a 60.3 mm site mast in place of line 8 changes the site cost by +${OPTIONS.get(11, 0) - cost.get(8, 0):.2f}")
tag("K4", f"stakes, capsules and heads ${cost[1] + cost[2] + cost[3]:.2f}; per extra stake ${(cost[1] + cost[2] + cost[3]) / 3:.2f} "
          f"plus about 10 m of cable")

# ------------------------------------------------------------------ L. Results
print("\nL. Results against every requirement")
wet_rate = wet4[8]
results = [
    ("R6", "Remote alert", f"{(air[12] + T_NS + T_ALERT_SVC + T_SMS + air[12] * 99 + air[12]) / 60:.1f} min worst at SF12 with one lost uplink", "5 min, where coverage exists", "At risk"),
    ("R7", "Alarm audible", f"{spl(100, GROUND[1]):.1f} to {spl(100, GROUND[0]):.1f} dB(A) at 100 m", "65 dB(A) at 100 m", "At risk"),
    ("R8", "Energy autonomy", f"{e_prec[0.01]:.1f} Wh of {CELL_USABLE * COLD:.1f} Wh worst case; 12 V rail {I_SIREN + I_BEACON:.2f} A unrated", "5 days, one 30 min alarm", "At risk"),
    ("R9", "Survive burial and weather", "Capsule and gland IP67 by parts; FieldNode interior above 60 C in 45 C sun (FND-CAL-001)", "IP67 at 0.4 m; -10 to 50 C", "At risk"),
    ("R1", "Measure surface tilt", f"{LSB:.4f} deg step, {sigma:.5f} deg noise, +-90 deg in mode 1", "0.01 deg, +-30 deg", "Met on paper"),
    ("R2", "Limit false tilt from temperature", f"{wet4[7]:.4f} deg/day, {wet_rate:.5f} deg/h (wet soil, 0.4 m)", "0.02 deg/day, 0.002 deg/h", "Met on paper"),
    ("R4", "Sample and report", f"10 min reads; {6 * air[12]:.1f} s/h at SF12", "10 min; 60 and 10 min uplinks", "Met on paper"),
    ("R12", "Open, local data", f"{flash / 1000:.0f} kB for 90 days", "90 days, CSV, any server", "Met on paper"),
    ("R11", "Affordable", f"${no_mast:.2f} for the reference site (existing pole); ${specific:.2f} with the optional new mast",
     f"${budget:.0f} value-engineering target, SlopeWatch-specific, reference site",
     f"{'Under' if no_mast <= budget else 'Over'} the value-engineering target by ${abs(budget - no_mast):.2f}"),
    ("R3", "Measure crack opening", f"{stroke:.0f} mm stroke, {step:.3f} mm step, {lin:.2f} mm linearity", "100 mm, 0.1 mm", "Met by design"),
    ("R5", "Local alarm without a network", f"{t_siren:.0f} s", "60 s", "Met by design"),
    ("R10", "Installable by a small team", f"{tt:.0f} min estimate", "45 min, hand tools", "Not verifiable at TRL 3"),
    ("R13", "Trustworthy alarms", "Needs a field record", "1 false warning per year", "Not verifiable at TRL 3"),
]
for r in results:
    tag("L", " | ".join(r))
counts = {}
for r in results:
    counts[r[4]] = counts.get(r[4], 0) + 1
tag("L0", "counts: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "requirement", "value", "target", "status"])
    w.writerows(results)
print("wrote docs/04-calcs/results.csv")
