#setdep @node|-1@
#set VBD_V -1
#set SCR_BIAS_V -1
#set DARK_BIAS_V -1
#set ATP_BIAS_V -1
#set PEB_BIAS_V -1
# CMP SPAD SVisualPy1 - VBD 기반 상대 바이어스(%) 추출.
# Parent -1 = SDevice1; VBD/Bias는 SWB 추출 변수이며 공정 입력 파라미터가 아니다.
import os
import fnmatch
import numpy as np
VIS_NODE = @node@
SNODE = @node|-1@
# [surrogate evaluation assumption] 공통 SDE R0(15.7979980544 V)의
# SCR 15.6 V / ATP 17.0 V를 백분율로 환산한 4자리 소수 초기값.
# 비율을 바꿀 때에는 이 3개 값만 변경한다(기존 SWB 공정 Parameter는 그대로 유지).
SCR_BELOW_VBD_PCT = 1.2533
DARK_BELOW_VBD_PCT = 1.2533
ATP_ABOVE_VBD_PCT = 7.6086
PEB_BELOW_VBD_PCT = 0.10  # H2 early-edge diagnostic, surrogate assumption
IV_FILE = f"n{SNODE}_des.plt"
AUDIT_FILE = f"n{VIS_NODE}_VBD_dynamic_bias_audit.txt"

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


if not np.isfinite(vbd) or vbd <= 0.0:
    raise RuntimeError(f"Invalid ionization-integral VBD: {vbd}")
if not (0.0 < SCR_BELOW_VBD_PCT < 100.0 and
        0.0 < DARK_BELOW_VBD_PCT < 100.0 and
        ATP_ABOVE_VBD_PCT > 0.0):
    raise RuntimeError("Invalid percent-based bias settings")
scr_bias = float(vbd * (1.0 - SCR_BELOW_VBD_PCT / 100.0))
dark_bias = float(vbd * (1.0 - DARK_BELOW_VBD_PCT / 100.0))
atp_bias = float(vbd * (1.0 + ATP_ABOVE_VBD_PCT / 100.0))
peb_bias = float(vbd * (1.0 - PEB_BELOW_VBD_PCT / 100.0))
if not (0.0 < scr_bias < vbd < atp_bias and 0.0 < dark_bias < vbd):
    raise RuntimeError("Invalid SCR/DARK/VBD/ATP bias ordering")
with open(AUDIT_FILE, "w") as audit:
    audit.write(f"VBD_V={vbd:.12g}\n")
    audit.write(f"SCR_below_VBD_pct={SCR_BELOW_VBD_PCT:.12g}\n")
    audit.write(f"DARK_below_VBD_pct={DARK_BELOW_VBD_PCT:.12g}\n")
    audit.write(f"ATP_above_VBD_pct={ATP_ABOVE_VBD_PCT:.12g}\n")
    audit.write(f"SCR_BIAS_V={scr_bias:.12g}\n")
    audit.write(f"DARK_BIAS_V={dark_bias:.12g}\n")
    audit.write(f"ATP_BIAS_V={atp_bias:.12g}\n")
emit("VBD_V", vbd)
emit("SCR_BIAS_V", scr_bias)
emit("DARK_BIAS_V", dark_bias)
emit("ATP_BIAS_V", atp_bias)
emit("PEB_BIAS_V", peb_bias)
print("SVISUALPY1: H2 VBD and SCR/DARK/PEB/ATP biases exported")
