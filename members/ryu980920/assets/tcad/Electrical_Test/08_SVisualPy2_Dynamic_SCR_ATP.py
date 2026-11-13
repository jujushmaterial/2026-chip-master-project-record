#setdep @node|-1@
#setdep @node|-2@
# CMP SPAD SVisualPy2 - exact-bias SCR and ATP spatial map.
# Parent -1 = SDevice2. Biases were emitted by SVisualPy1.
import os
import fnmatch
import numpy as np
VIS_NODE = @node@
SNODE = @node|-1@
VBD = float(@VBD_V@)
SCR_BIAS = float(@SCR_BIAS_V@)
ATP_BIAS = float(@ATP_BIAS_V@)
CENTER_R = 4.6875
EDGE_R = 12.5
Y_SI_SURFACE = 0.0
Y_GRATING_SI_INTERFACE = 0.300
SCR_E = 1.0e5
SCR_SEARCH_MAX_IF = 1.30
TDR_FILE = f"n{SNODE}_SCR_des.tdr"
ATP_FILE = f"n{SNODE}_ATP_des.tdr"
AUDIT_FILE = f"n{VIS_NODE}_SCR_ATP_audit.txt"
ATP_MAP_CSV = f"n{VIS_NODE}_ATP_map.csv"
if not 0 < SCR_BIAS < VBD < ATP_BIAS:
    raise RuntimeError("Invalid dynamic bias ordering")
# 절대 전압차 대신 각 후보 VBD에 대한 상대 바이어스 비율(%)을 검사한다.
SCR_BELOW_PCT_ACTUAL = 100.0 * (VBD - SCR_BIAS) / VBD
ATP_ABOVE_PCT_ACTUAL = 100.0 * (ATP_BIAS - VBD) / VBD
if not (np.isfinite(SCR_BELOW_PCT_ACTUAL) and 0.0 < SCR_BELOW_PCT_ACTUAL < 100.0 and
        np.isfinite(ATP_ABOVE_PCT_ACTUAL) and ATP_ABOVE_PCT_ACTUAL > 0.0):
    raise RuntimeError("Invalid percentage-based SCR/ATP biases")

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



# SCR: use the frozen threshold, junction bracketing and radial center rule.
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
    raise RuntimeError("Exact dynamic SCR TDR missing")


# SCR boundary diagnostic. Preserve the frozen SDE extraction rule, but
# do not prevent ATP analysis when the SCR threshold crossings are missing.
# Raw CSV retains NaN/Inf rows, filtered CSV is exactly the data used for SCR.
diag_raw_file = f"n{VIS_NODE}_SCR_cut_raw.csv"
diag_file = f"n{VIS_NODE}_SCR_cut.csv"
np.savetxt(
    diag_raw_file,
    np.column_stack((z_if_raw, ec_raw, nd_raw, hp_raw, agc_raw)),
    delimiter=",",
    header="DepthFromInterface_um,ElectricField_Vcm,NetDoping_cm3,hDensity_cm3,AvalancheGeneration_cm3s",
    comments="",
    fmt="%.12e"
)
np.savetxt(
    diag_file,
    np.column_stack((z_if, ec, nd)),
    delimiter=",",
    header="DepthFromInterface_um,ElectricField_Vcm,NetDoping_cm3",
    comments="",
    fmt="%.12e"
)

print("=== SCR BOUNDARY DIAGNOSTIC ===")
print("SCR bias (V):", SCR_BIAS)
print("Raw / filtered cut points:", len(y_raw), "/", len(z_if))
print("Net doping variable:", dname if dname is not None else "Donor - Acceptor")
print("Finite field / doping raw points:",
      int(np.isfinite(ec_raw).sum()), "/", int(np.isfinite(nd_raw).sum()))
print("Junction crossings (um):", jc)
print("E-field threshold crossings (um):", scrc)
print("Selected junction (um):", zj_if)
print("Selected lower / upper (um):", zsp_if, zsn_if)
print("SCR_OK:", int(scr_valid))
print("SCR diagnostic CSVs:", diag_raw_file, diag_file)
if not scr_valid:
    print("WARNING: Invalid SCR field boundaries; reporting SCR as unavailable.")
    print("WARNING: ATP analysis continues independently using the ATP TDR.")

if not os.path.isfile(ATP_FILE):
    raise RuntimeError(f"Missing target ATP TDR: {ATP_FILE}")
try:
    sv.load_file(ATP_FILE, name="ATPSTATE", alldata=True)
except TypeError:
    sv.load_file(ATP_FILE, name="ATPSTATE")
atp_plot = sv.create_plot(name="Plot_ATPState", dataset="ATPSTATE")

def atp_cut(radius, label):
    try:
        cut = sv.create_cutline("x", at=float(radius), plot=atp_plot, name=label)
    except TypeError:
        cut = sv.create_cutline(type="x", at=float(radius), plot=atp_plot, name=label)

    try:
        names = list(sv.list_variables(dataset=cut))
    except Exception:
        names = []

    def match(patterns):
        for pattern in patterns:
            for var in names:
                if fnmatch.fnmatch(var.lower(), pattern.lower()):
                    return var
        for var in patterns:
            if "*" not in var:
                try:
                    if get_data(cut, var).size > 0:
                        return var
                except Exception:
                    pass
        return None

    yn = match(["Y", "y"])
    jn = match(["jBreakdownProbability", "*jBreakdownProbability*",
                "*Joint*BreakdownProbability*"])
    if yn is None or jn is None:
        raise RuntimeError(f"ATP cut missing Y/jProbability at r={radius}")
    z, p = sort_unique_many(get_data(cut, yn)-Y_GRATING_SI_INTERFACE,
                            get_data(cut, jn))
    if z.size < 2:
        raise RuntimeError(f"ATP cut too small at r={radius}")
    return z, p

def at_depth(z, p, depth):
    if z.size < 2 or not (z[0] <= depth <= z[-1]):
        return np.nan
    return float(np.interp(depth, z, p))

# Validated T-2022.03 strategy: create explicit 2D ATP plot, precheck, 101 cuts.
atp_cut(CENTER_R, "ATP_CENTER_PRECHECK")
rr_list, zz_list, pp_list = [], [], []
atp_axis180 = np.nan
atp_peak180 = np.nan
atp_peak180_r_um = np.nan
errors = []
for i, radius in enumerate(np.linspace(0, EDGE_R, 101)):
    try:
        z, p = atp_cut(float(radius), f"ATP_MAP_{i:03d}")
    except Exception as exc:
        errors.append(f"r={radius:.6g}:{exc}")
        continue
    p180 = at_depth(z, p, 0.180)
    if i == 0:
        atp_axis180 = p180
    if np.isfinite(p180) and (
        not np.isfinite(atp_peak180) or p180 > atp_peak180
    ):
        atp_peak180 = p180
        atp_peak180_r_um = float(radius)
    rr_list.append(np.full(z.size, radius))
    zz_list.append(z)
    pp_list.append(p)
if not pp_list:
    raise RuntimeError("ATP sampling produced zero valid radial cuts")
rr = np.concatenate(rr_list)
zz = np.concatenate(zz_list)
pp = np.concatenate(pp_list)
good = np.isfinite(rr) & np.isfinite(zz) & np.isfinite(pp)
if not np.any(good):
    raise RuntimeError("No finite ATP probability samples")
rg, zg, pg = rr[good], zz[good], pp[good]
ind = int(np.argmax(pg))
atp_peak = float(pg[ind])
atp_peak_r_um = float(rg[ind])
atp_peak_z_nm = float(zg[ind] * 1000.0)
np.savetxt(
    ATP_MAP_CSV, np.column_stack((rr,zz,pp)), delimiter=",",
    header="Radius_um,DepthFromGratingSiInterface_um,jBreakdownProbability",
    comments="", fmt="%.12e"
)
atp_ok = bool(np.isfinite(atp_axis180) and np.isfinite(atp_peak180)
              and np.isfinite(atp_peak))
with open(AUDIT_FILE, "w") as audit:
    audit.write(f"VBD_V={VBD:.12g}\n")
    audit.write(f"SCR_below_VBD_pct={SCR_BELOW_PCT_ACTUAL:.12g}\n")
    audit.write(f"ATP_above_VBD_pct={ATP_ABOVE_PCT_ACTUAL:.12g}\n")
    audit.write(f"SCR_BIAS_V={SCR_BIAS:.12g}\n")
    audit.write(f"ATP_BIAS_V={ATP_BIAS:.12g}\n")
    audit.write(f"SCR_TDR={TDR_FILE}\n")
    audit.write(f"ATP_TDR={ATP_FILE}\n")
    audit.write(f"SCR_center_nm={scr_center_nm:.12g}\n")
    audit.write(f"SCR_width_nm={scr_width_nm:.12g}\n")
    audit.write(f"z_junction_if_um={zj_if:.12g}\n")
    audit.write(f"SCR_OK={int(scr_valid)}\n")
    audit.write(f"SCR_junction_crossings_if_um={jc.tolist()}\n")
    audit.write(f"SCR_field_crossings_if_um={scrc.tolist()}\n")
    audit.write(f"SCR_lower_if_um={zsp_if:.12g}\n")
    audit.write(f"SCR_upper_if_um={zsn_if:.12g}\n")
    audit.write(f"SCR_raw_cut_points={len(y_raw)}\n")
    audit.write(f"SCR_filtered_cut_points={len(z_if)}\n")
    audit.write(f"SCR_diagnostic_raw_csv={diag_raw_file}\n")
    audit.write(f"SCR_diagnostic_filtered_csv={diag_file}\n")
    audit.write(f"ATP_Vex_V={ATP_BIAS-VBD:.12g}\n")
    audit.write(f"ATP_success_cuts={len(pp_list)}/101\n")
    audit.write(f"ATP_cut_errors={errors}\n")
emit("SCR_bias_V", SCR_BIAS)
emit("SCR_center_nm", scr_center_nm)
emit("SCR_width_nm", scr_width_nm)
emit("SCR_OK", float(scr_valid))
emit("ATP_bias_V", ATP_BIAS)
emit("ATP_Vex_V", ATP_BIAS - VBD)
emit("ATP_axis180", atp_axis180)
emit("ATP_peak180", atp_peak180)
emit("ATP_peak180_r_um", atp_peak180_r_um)
emit("ATP_peak", atp_peak)
emit("ATP_peak_r_um", atp_peak_r_um)
emit("ATP_peak_z_nm", atp_peak_z_nm)
emit("ATP_OK", float(atp_ok))
print("SVISUALPY2: dynamic SCR and ATP processed")
