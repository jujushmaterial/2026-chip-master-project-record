#setdep @node|sdevice@

# CMP SPAD / SProcess electrical baseline equivalence check
# v0.5: compact DOE output, SDE static-freeze v2.2 algorithms preserved.
#
# Reference: members/jujushmaterial/assets/tcad/spad-baseline-static-freeze/
#            CMP_SPAD_Stage1_SVisualPy_v2.2_DOE_compact.txt
# SDevice:   CMP_SPAD_BaselineImplementation_SDevice.txt (same physics and
#            ionization-integral settings as SDE static-freeze SDevice).
#
# Workbench output ONLY: VBD_V, SCR_center_nm, SCR_width_nm.
# Fixed SCR evaluation voltage 15.6V; do not substitute a VBD+Vex snapshot.
# SDE coordinate: z_if = raw_y - 0.0um (SDE bulk surface at -0.3um).
# SProcess coordinate: z_if = raw_y - 0.300um (bulk surface at 0.0um).
# VBD criterion: first voltage where min(PhiElectron, PhiHole) crosses 1.
# SCR edges: |E|=1e5 V/cm crossings bracketing net-doping zero crossing.

import os
import fnmatch
import numpy as np

VIS_NODE = @node@
SNODE = @node|sdevice@

CENTER_R = 4.6875
Y_SI_SURFACE = 0.0
Y_GRATING_SI_INTERFACE = 0.300
SCR_E = 1.0e5
SCR_SEARCH_MAX_IF = 1.30
EVAL_BIAS = 15.6

IV_FILE = f"n{SNODE}_des.plt"
TDR_FILE = f"n{SNODE}_V156_des.tdr"
AUDIT_FILE = f"n{VIS_NODE}_VBD_SCR_audit.txt"


def pickvar(dataset, patterns):
    names = list(sv.list_variables(dataset=dataset))
    for pat in patterns:
        p = pat.lower()
        for name in names:
            if fnmatch.fnmatch(name.lower(), p):
                return name
    return None


def get_data(dataset, varname):
    return np.asarray(
        sv.get_variable_data(varname=varname, dataset=dataset),
        dtype=float
    )


def finite_xy(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    return x[m], y[m]


def sort_unique_many(x, *ys):
    x = np.asarray(x, dtype=float)
    arrs = [np.asarray(y, dtype=float) for y in ys]

    m = np.isfinite(x)
    for a in arrs:
        m &= np.isfinite(a)

    x = x[m]
    arrs = [a[m] for a in arrs]

    idx = np.argsort(x, kind="mergesort")
    x = x[idx]
    arrs = [a[idx] for a in arrs]

    xu, inv = np.unique(x, return_inverse=True)
    outs = []
    for a in arrs:
        sums = np.bincount(inv, weights=a)
        counts = np.bincount(inv)
        outs.append(sums / np.maximum(counts, 1))
    return (xu, *outs)


def crossings(x, y, level, lo=-np.inf, hi=np.inf):
    x, y = finite_xy(x, y)
    if x.size < 2:
        return np.array([], dtype=float)

    idx = np.argsort(x, kind="mergesort")
    x = x[idx]
    y = y[idx]

    x1 = x[:-1]
    x2 = x[1:]
    y1 = y[:-1]
    y2 = y[1:]

    m = (
        (y2 != y1) &
        ((y1 - level) * (y2 - level) <= 0.0)
    )

    if not np.any(m):
        return np.array([], dtype=float)

    t = (level - y1[m]) / (y2[m] - y1[m])
    good_t = (t >= 0.0) & (t <= 1.0)

    xc = x1[m][good_t] + t[good_t] * (x2[m][good_t] - x1[m][good_t])

    # Same crossing-position filter as SDE static-freeze v2.2.
    return xc[(xc >= lo) & (xc <= hi)]


def bracket_crossings(vals, x0):
    vals = np.asarray(vals, dtype=float)
    vals = np.sort(vals[np.isfinite(vals)])
    lower = vals[vals <= x0]
    upper = vals[vals > x0]
    lo = float(lower[-1]) if lower.size else np.nan
    hi = float(upper[0]) if upper.size else np.nan
    return lo, hi


def vbd_from_phi(v, pe, ph):
    v, pe, ph = sort_unique_many(v, pe, ph)
    g = np.minimum(pe, ph)
    c = crossings(v, g, 1.0)
    return float(c[0]) if c.size else np.nan


def field_mag(dataset):
    scalar = pickvar(
        dataset,
        ["AbsElectricField", "Abs(ElectricField-V)", "ElectricField"]
    )
    if scalar is not None:
        a = get_data(dataset, scalar)
        if a.ndim == 1:
            return np.abs(a)

    exn = pickvar(
        dataset,
        ["ElectricField-X", "ElectricField/x", "*ElectricField*X*"]
    )
    eyn = pickvar(
        dataset,
        ["ElectricField-Y", "ElectricField/y", "*ElectricField*Y*"]
    )
    if exn is None or eyn is None:
        raise RuntimeError("Electric-field variable not found")

    ex = get_data(dataset, exn)
    ey = get_data(dataset, eyn)
    return np.sqrt(ex * ex + ey * ey)


def create_cut(direction, at, dataset, name):
    try:
        return sv.create_cutline(
            direction,
            at=at,
            dataset=dataset,
            materials=["Silicon"],
            name=name
        )
    except TypeError:
        return sv.create_cutline(
            direction,
            at=at,
            dataset=dataset,
            name=name
        )


def emit(name, value):
    if value is None or not np.isfinite(value):
        print(f"DOE: {name} x")
    else:
        print(f"DOE: {name} {float(value):.12g}")


# ----------------------------------------------------------------------
# 1. VBD: same data source, Phi pick rules and criterion as SDE baseline.
# ----------------------------------------------------------------------
if not os.path.isfile(IV_FILE):
    raise RuntimeError(f"Missing SDevice I-V file: {IV_FILE}")
sv.load_file(IV_FILE, name="IV")

vname = pickvar("IV", ["*cathode*OuterVoltage*", "*cathode*InnerVoltage*"])
iname = pickvar("IV", ["*anode*TotalCurrent*"])
if vname is None or iname is None:
    raise RuntimeError("I-V variables not found")

vv_raw = np.abs(get_data("IV", vname))
ii_raw = np.abs(get_data("IV", iname))
pename = pickvar("IV", ["PhiElectron", "*PhiElectron*"])
phname = pickvar("IV", ["PhiHole", "*PhiHole*"])

vbd = np.nan
if pename is not None and phname is not None:
    pe_raw = get_data("IV", pename)
    ph_raw = get_data("IV", phname)
    vbd = vbd_from_phi(vv_raw, pe_raw, ph_raw)


# ----------------------------------------------------------------------
# 2. SCR: same fixed 15.6V / center radius / E field / crossing rule.
# ----------------------------------------------------------------------
scr_center_nm = np.nan
scr_width_nm = np.nan
zj_if = np.nan
zsp_if = np.nan
zsn_if = np.nan
scr_valid = False
tdr_ok = os.path.isfile(TDR_FILE)

if tdr_ok:
    sv.load_file(TDR_FILE, name="STATE")
    # SDE reference creates an explicit state plot before taking a cut.
    sv.create_plot(name="Plot_State", dataset="STATE")

    center = create_cut("x", CENTER_R, "STATE", "CENTER")
    yname = pickvar(center, ["Y", "y"])
    if yname is None:
        raise RuntimeError("Cutline coordinate variable not found")

    y_raw = get_data(center, yname)
    ec_raw = field_mag(center)

    dname = pickvar(center, ["Doping", "DopingConcentration", "NetDoping"])
    if dname is not None:
        nd_raw = get_data(center, dname)
    else:
        dn = pickvar(center, ["DonorConcentration", "*Donor*"])
        an = pickvar(center, ["AcceptorConcentration", "*Acceptor*"])
        if dn is None or an is None:
            raise RuntimeError("Doping variables not found")
        nd_raw = get_data(center, dn) - get_data(center, an)

    # Match reference preprocessing exactly: hDensity and avalanche generation
    # arrays also participate in finite-data masking before SCR crossings.
    hname = pickvar(center, ["hDensity", "*hDensity*"])
    if hname is not None:
        hp_raw = get_data(center, hname)
    else:
        hp_raw = np.zeros_like(y_raw)
    agc_name = pickvar(
        center,
        [
            "AvalancheGeneration",
            "*AvalancheGeneration*",
            "ImpactIonization",
            "*ImpactIonization*"
        ]
    )
    if agc_name is not None:
        agc_raw = get_data(center, agc_name)
    else:
        agc_raw = np.zeros_like(y_raw)

    z_if_raw = y_raw - Y_GRATING_SI_INTERFACE
    z_surface_raw = y_raw - Y_SI_SURFACE
    z_if, z_surface, ec, nd, hp, agc = sort_unique_many(
        z_if_raw, z_surface_raw, ec_raw, nd_raw, hp_raw, agc_raw
    )

    # EXACT extraction structure of SDE static-freeze v2.2.
    jc = crossings(z_if, nd, 0.0, lo=0.0, hi=SCR_SEARCH_MAX_IF)
    zj_if = float(jc[0]) if jc.size else np.nan
    scrc = crossings(z_if, ec, SCR_E, lo=0.0, hi=SCR_SEARCH_MAX_IF)

    if np.isfinite(zj_if):
        zsp_if, zsn_if = bracket_crossings(scrc, zj_if)
    elif scrc.size >= 2:
        zsp_if = float(scrc[0])
        zsn_if = float(scrc[1])

    wsc = (
        zsn_if - zsp_if
        if np.isfinite(zsp_if) and np.isfinite(zsn_if)
        else np.nan
    )
    zsc_if = (
        0.5 * (zsp_if + zsn_if)
        if np.isfinite(zsp_if) and np.isfinite(zsn_if)
        else np.nan
    )
    scr_valid = bool(
        np.isfinite(zsp_if) and
        np.isfinite(zsn_if) and
        np.isfinite(wsc) and
        (wsc > 0.0) and
        np.isfinite(zsc_if)
    )
    scr_center_nm = zsc_if * 1000.0
    scr_width_nm = wsc * 1000.0
else:
    print("SVISUALPY: V156_TDR_MISSING; SCR outputs are NA, no bias fallback")

# Always leave trace data OUTSIDE SWB DOE columns.
with open(AUDIT_FILE, "w") as audit:
    audit.write(f"SDevice_node={SNODE}\n")
    audit.write(f"IV_FILE={IV_FILE}\n")
    audit.write(f"TDR_FILE={TDR_FILE}\n")
    audit.write(f"SCR_evaluation_bias_V={EVAL_BIAS}\n")
    audit.write(f"SCR_center_radius_um={CENTER_R}\n")
    audit.write(f"SProcess_interface_raw_y_um={Y_GRATING_SI_INTERFACE}\n")
    audit.write(f"SCR_electric_field_threshold_V_per_cm={SCR_E}\n")
    audit.write(f"SCR_search_min_if_um=0.0\n")
    audit.write(f"SCR_search_max_if_um={SCR_SEARCH_MAX_IF}\n")
    audit.write(f"SCR_TDR_exists={int(tdr_ok)}\n")
    audit.write(f"SCR_valid={int(scr_valid)}\n")
    audit.write(f"z_junction_if_um={zj_if}\n")
    audit.write(f"z_SCR_p_if_um={zsp_if}\n")
    audit.write(f"z_SCR_n_if_um={zsn_if}\n")
    audit.write(f"VBD_V={vbd}\n")
    audit.write(f"SCR_center_nm={scr_center_nm}\n")
    audit.write(f"SCR_width_nm={scr_width_nm}\n")

emit("VBD_V", vbd)
emit("SCR_center_nm", scr_center_nm)
emit("SCR_width_nm", scr_width_nm)
print("SVISUALPY: COMPLETE (SDE-equivalent VBD/SCR rules)")
