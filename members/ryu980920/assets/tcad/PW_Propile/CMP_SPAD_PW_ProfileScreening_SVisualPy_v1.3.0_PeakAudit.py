#setdep @node|sprocess@
# =============================================================================
# CMP SPAD | PW-only SDE PLX direct profile screening | SVisualPy v1.3.0 (Global Peak + Split Audit)
# 2026-10-19
# =============================================================================
# This is PW-only process-profile screening, NOT SCR/VBD/ATP verification.
# Reference: numeric BActive/PActive depth samples from frozen SDE baseline PLX
#            at r=4.6875 um (NOT an analytic Gaussian).
# Process input: n<sprocess_node>_F_r4p6.plx (final F); same basis across DOE.
# SWB compatibility: original eight PW12_* DOE variables retained unchanged in name.
# Additional PW12_* diagnostics are exported as DOE: values (optional SWB Output
# Variables); all metrics + peak audit always saved in per-node CSV/TXT files.
# IMPORTANT: PW12_MAIN_NM is the legacy 30-170 nm SHALLOW window maximum.
# It is NOT the global maximum or necessarily a resolved local peak.
# Split and SCORE use the new extended-window rebound; old/new SCORES not identical.
# No SProcess edits, no added SWB input Parameters, no electrical claims.
# =============================================================================
import csv
import math
import os
import traceback
import numpy as np

VIS_NODE = "@node@"
PROCESS_NODE = "@node|sprocess@"

# Actual SDE reference samples are embedded below to avoid runtime file paths,
# __file__, multiline-text quoting, and a separate per-node reference PLX copy.
# Numeric values are preserved from the original uploaded SDE PLX; paired depths.
# Baseline SDE original PLX numerical samples (0-0.9 um + next bracketing point).
# [project baseline] Reference is exact PLX extracted samples, not Gaussian fit.
# The original full SDE PLX file SHA256 is recorded for provenance:
# SHA256: 0ddbabdb5f9a58e66c1815a87df2f7053446ff161d82cb16ed4687e172856a2e
# No multiline strings or long single-line literals are used.
SDE_BACTIVE_POINTS = [
    (0.0007919848, 5.2712222e+17),
    (0.0033144534, 5.3038196e+17),
    (0.0058369219, 5.3357718e+17),
    (0.0083593607, 5.3670646e+17),
    (0.010881829, 5.3976841e+17),
    (0.013404298, 5.4276168e+17),
    (0.015926766, 5.4568494e+17),
    (0.018449205, 5.4853686e+17),
    (0.020971674, 5.5131617e+17),
    (0.023494142, 5.5402161e+17),
    (0.02853905, 5.5920601e+17),
    (0.038628894, 5.6863651e+17),
    (0.048718739, 5.7675909e+17),
    (0.068898442, 5.8884897e+17),
    (0.089078131, 5.9511346e+17),
    (0.10925781, 5.9536289e+17),
    (0.12943749, 5.8958969e+17),
    (0.14961718, 5.7796874e+17),
    (0.16979687, 5.6084858e+17),
    (0.18997656, 5.3873406e+17),
    (0.21015625, 5.1226161e+17),
    (0.23033594, 4.8216883e+17),
    (0.25051562, 4.4926048e+17),
    (0.27069531, 4.1437298e+17),
    (0.290875, 3.783396e+17),
    (0.31105469, 3.4195837e+17),
    (0.33123437, 3.0596429e+17),
    (0.35141406, 2.7100717e+17),
    (0.37159375, 2.376357e+17),
    (0.39177344, 2.0628816e+17),
    (0.41195312, 1.7728941e+17),
    (0.43213281, 1.508536e+17),
    (0.4523125, 1.270918e+17),
    (0.46240235, 1.1622286e+17),
    (0.47249219, 1.0602317e+17),
    (0.49267188, 8.7588879e+16),
    (0.51285157, 7.166718e+16),
    (0.53303124, 5.8088952e+16),
    (0.55321093, 4.6652551e+16),
    (0.57339062, 3.7137383e+16),
    (0.59357031, 2.9315681e+16),
    (0.61375, 2.2962207e+16),
    (0.63392969, 1.7861788e+16),
    (0.65410938, 1.3814744e+16),
    (0.67428907, 1.0640397e+16),
    (0.69446875, 8.1789112e+15),
    (0.71464844, 6.2917692e+15),
    (0.73482813, 4.8611963e+15),
    (0.75500782, 3.7888267e+15),
    (0.77518751, 2.9938838e+15),
    (0.7953672, 2.4110969e+15),
    (0.81554686, 1.988536e+15),
    (0.85590624, 1.4705435e+15),
    (0.93662499, 1.0943536e+15),
]
SDE_PACTIVE_POINTS = [
    (0.0007919848, 9.9289159e+15),
    (0.0033144534, 1.0103521e+16),
    (0.0058369219, 1.0280744e+16),
    (0.0083593607, 1.0460615e+16),
    (0.010881829, 1.0643163e+16),
    (0.013404298, 1.082842e+16),
    (0.015926766, 1.1016416e+16),
    (0.018449205, 1.1207182e+16),
    (0.020971674, 1.140075e+16),
    (0.023494142, 1.1597149e+16),
    (0.02853905, 1.199857e+16),
    (0.038628894, 1.2836788e+16),
    (0.048718739, 1.3723884e+16),
    (0.068898442, 1.5653081e+16),
    (0.089078131, 1.7803193e+16),
    (0.10925781, 2.0191622e+16),
    (0.12943749, 2.2835986e+16),
    (0.14961718, 2.5753935e+16),
    (0.16979687, 2.8962942e+16),
    (0.18997656, 3.2480073e+16),
    (0.21015625, 3.6321734e+16),
    (0.23033594, 4.0503394e+16),
    (0.25051562, 4.5039287e+16),
    (0.27069531, 4.9942105e+16),
    (0.290875, 5.5222676e+16),
    (0.31105469, 6.0889625e+16),
    (0.33123437, 6.6949048e+16),
    (0.35141406, 7.3404175e+16),
    (0.37159375, 8.0255051e+16),
    (0.39177344, 8.7498226e+16),
    (0.41195312, 9.5126467e+16),
    (0.43213281, 1.0312851e+17),
    (0.4523125, 1.1148883e+17),
    (0.46240235, 1.1579729e+17),
    (0.47249219, 1.2018749e+17),
    (0.49267188, 1.2919997e+17),
    (0.51285157, 1.3849714e+17),
    (0.53303124, 1.4804524e+17),
    (0.55321093, 1.5780594e+17),
    (0.57339062, 1.6773647e+17),
    (0.59357031, 1.7778983e+17),
    (0.61375, 1.8791505e+17),
    (0.63392969, 1.9805759e+17),
    (0.65410938, 2.081597e+17),
    (0.67428907, 2.1816098e+17),
    (0.69446875, 2.2799891e+17),
    (0.71464844, 2.3760944e+17),
    (0.73482813, 2.4692774e+17),
    (0.75500782, 2.5588883e+17),
    (0.77518751, 2.6442836e+17),
    (0.7953672, 2.7248335e+17),
    (0.81554686, 2.7999301e+17),
    (0.85590624, 2.9314828e+17),
    (0.93662499, 3.1064956e+17),
]

REF_SHA256 = "0ddbabdb5f9a58e66c1815a87df2f7053446ff161d82cb16ed4687e172856a2e"
SDE_JUNC_NM = 462.6966588130754
GRID_STEP_UM = 0.005
GRID_START_UM = 0.030
GRID_END_UM = 0.900
FLOOR = 1.0e12

# Surrogate screening choices; not a published SPAD acceptance criterion.
SH_RANGE = (0.030, 0.110)
MID_RANGE = (0.110, 0.350)
TAIL_RANGE = (0.350, 0.600)
ALL_RANGE = (0.030, 0.600)
MAIN_SEARCH = (0.030, 0.170)
SPLIT_SEARCH = (0.030, 0.900)      # Scan post-shallow all the way to 900 nm
GLOBAL_SEARCH = (0.030, 0.900)     # Global BActive peak audit window
SHALLOW_MATCH_TOLERANCE_NM = 15.0 # Local peak must exist near window maximum
SECOND_MIN_SEPARATION_NM = 30.0
SMOOTH_N = 5                      # 5 * 5 nm = 25 nm smoothing
SPLIT_REPORT_MIN = 0.005          # 0.5% rise; below = not resolved
SPLIT_OK_MAX = 0.05               # 5% rise; [surrogate assumption]
PEAK_DEPTH_OK_MAX_NM = 25.0
PEAK_RATIO_OK_MAX_REL_ERR = 0.15
B462_OK_RANGE = (0.70, 1.30)
SHAPE_SCORE_SCALE_DEX = 0.10
PEAK_SCORE_SCALE_LOG = math.log10(1.20)
POSITION_SCORE_SCALE_NM = 20.0
SPLIT_SCORE_SCALE = 0.05

# Split hard gate is applied before ranking; score alone is NOT candidate status.
# Weighted bounded score: 0 best, 100 worst; NEVER 100 - matching percent.
WEIGHTS = {
    "PKPOS": 0.10,
    "PKCONC": 0.10,
    "SH": 0.10,
    "MID": 0.20,
    "TAIL": 0.25,
    "B462": 0.15,
    "SPLIT": 0.10,
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1.0e-12

# Diagnostic ratio depths [nm]. 462.696658... is the frozen SDE anchor.
DEPTHS_NM = [50, 75, 90, 150, 200, 250, 270, 300, 350,
             400, 450, SDE_JUNC_NM, 500, 550, 600]
SWB_RATIO_DEPTHS = [75, 200, 270, 300, 400, 500]


def _read_plx(path):
    # The project's PLX is an ASCII sectioned XY file, not a generic binary TDR.
    if not os.path.isfile(path):
        raise FileNotFoundError("Missing final F PLX: " + os.path.abspath(path))
    sections = {}
    name = None
    coords = []

    def flush():
        if name is None or len(coords) < 2:
            return
        arr = np.asarray(coords, dtype=float)
        good = np.isfinite(arr[:, 0]) & np.isfinite(arr[:, 1])
        arr = arr[good]
        if len(arr) < 2:
            raise ValueError("PLX section with too few finite points: " + name)
        xx, inv = np.unique(arr[:, 0], return_inverse=True)
        yy = np.bincount(inv, weights=arr[:, 1]) / np.bincount(inv)
        sections[name] = (xx, yy)

    with open(path, "r", encoding="utf-8-sig") as fh:
        for number, raw in enumerate(fh, 1):
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            if s.startswith('"') and s.endswith('"'):
                flush()
                name = s[1:-1].strip()
                coords = []
                continue
            tokens = s.split()
            if len(tokens) != 2 or name is None:
                raise ValueError("Unexpected PLX row %d: %s" % (number, s[:70]))
            coords.append((float(tokens[0]), float(tokens[1])))
    flush()
    return sections


def _ref_sections():
    out = {}
    for name, samples in (("BActive", SDE_BACTIVE_POINTS),
                          ("PActive", SDE_PACTIVE_POINTS)):
        ar = np.asarray(samples, dtype=float)
        out[name] = (ar[:, 0], ar[:, 1])
    return out


def _section(sections, stem):
    hits = [v for k, v in sections.items()
            if k.lower() == stem.lower() or k.lower().startswith(stem.lower() + "(")]
    if len(hits) != 1:
        raise RuntimeError("Exactly one %s section needed; found %d; available=%s" %
                           (stem, len(hits), list(sections)))
    return hits[0]


def _at(pair, z_um):
    x, y = pair
    if z_um < x[0] or z_um > x[-1]:
        raise ValueError("PLX range does not cover %.6f um" % z_um)
    return float(np.interp(z_um, x, y))


def _grid(pair, z):
    xx, yy = pair
    if z[0] < xx[0] or z[-1] > xx[-1]:
        raise ValueError("PLX range [%.6f, %.6f] does not cover requested grid" %
                         (xx[0], xx[-1]))
    out = np.interp(z, xx, yy)
    if not np.all(np.isfinite(out)) or np.any(out < 0.0):
        raise ValueError("Non-finite or negative active concentration on grid")
    return out


def _mask(z, lo, hi):
    return (z >= lo - 1.0e-10) & (z <= hi + 1.0e-10)


def _log_rmse(z, actual, reference, bounds, normalized=False,
              main_actual=None, main_reference=None):
    m = _mask(z, bounds[0], bounds[1])
    a = actual[m]
    r = reference[m]
    if len(a) < 3:
        raise ValueError("Too few values in shape window: %s" % (bounds,))
    if normalized:
        a = a / max(main_actual, FLOOR)
        r = r / max(main_reference, FLOOR)
        limit = 1.0e-12
    else:
        limit = FLOOR
    return float(np.sqrt(np.mean((np.log10(np.maximum(a, limit)) -
                                  np.log10(np.maximum(r, limit))) ** 2)))


def _rel_l1(z, actual, ref, bounds):
    m = _mask(z, bounds[0], bounds[1])
    x = z[m]
    num = float(np.trapz(np.abs(actual[m] - ref[m]), x))
    den = float(np.trapz(np.maximum(ref[m], FLOOR), x))
    return num / den


def _sigma(z, y, bounds):
    m = _mask(z, bounds[0], bounds[1])
    x = z[m]
    w = np.maximum(y[m], 0.0)
    a = float(np.trapz(w, x))
    if a <= 0:
        raise ValueError("Nonpositive concentration integral")
    mu = float(np.trapz(x * w, x) / a)
    var = float(np.trapz((x - mu)**2 * w, x) / a)
    return math.sqrt(max(0.0, var)) * 1000.0


def _window_peak(z, y, bounds):
    indices = np.where(_mask(z, bounds[0], bounds[1]))[0]
    j = int(indices[np.argmax(y[indices])])
    return float(z[j]), float(y[j])


def _smooth(y):
    n = SMOOTH_N
    return np.convolve(np.pad(y, (n // 2, n // 2), mode="edge"),
                       np.ones(n, dtype=float) / n, mode="valid")[:len(y)]


def _peak_diagnostics(z, b, raw_b, shallow_um, shallow_cm3):
    """Audit true global maximum, local post-shallow peaks, valley/rebound.

    - SHALLOW: legacy raw maximum in 30-170 nm; not assumed globally dominant.
    - GLOBAL: raw maximum over 30-900 nm, not a smoothed/windowed local peak.
    - SECOND: strongest RESOLVED post-shallow local maximum (by BActive value)
      identified on a smoothed 5 nm grid, with raw concentration interpolated
      at that peak's grid location. Not necessarily the second by depth order.
    - REBOUND: maximum smoothed rise above the preceding minimum anywhere
      after the shallow maximum (respecting 30 nm spacing), across 900 nm.
    For nonexistent second peaks the depth sentinel is -1 nm, ratio=0.
    """
    sm = _smooth(b)
    gz, gc = _window_peak(raw_b[0], raw_b[1], GLOBAL_SEARCH)
    indices = np.where(_mask(z, SPLIT_SEARCH[0], SPLIT_SEARCH[1]))[0]
    local = []
    # A local maximum MUST have points on both sides; a rising endpoint alone
    # is not a resolved peak. Both strict/flat-top extrema are accepted.
    for i in indices:
        if i <= 0 or i >= len(z) - 1:
            continue
        if ((sm[i] > sm[i-1] and sm[i] >= sm[i+1]) or
                (sm[i] >= sm[i-1] and sm[i] > sm[i+1])):
            local.append(int(i))
    shallow_valid = any(abs(z[i]-shallow_um)*1000.0 <= SHALLOW_MATCH_TOLERANCE_NM
                        and MAIN_SEARCH[0] <= z[i] <= MAIN_SEARCH[1]+1.e-10
                        for i in local)

    start = int(np.searchsorted(z, shallow_um, side="left"))
    after = np.arange(start, len(z), dtype=int)
    runmin = np.minimum.accumulate(sm[after])
    risearr = sm[after]-runmin
    eligible = after[z[after] >= shallow_um + SECOND_MIN_SEPARATION_NM/1000.0 - 1.e-10]
    if len(eligible) == 0:
        raise ValueError("Post-shallow search contains no points")
    rebound = max(0., float(np.max(risearr[eligible-start]))) / max(shallow_cm3,FLOOR)

    candidates = []
    for i in local:
        if z[i] < shallow_um + SECOND_MIN_SEPARATION_NM/1000.0 - 1.e-10:
            continue
        jmin = start + int(np.argmin(sm[start:i+1]))
        rise = max(0.,float(sm[i]-sm[jmin])) / max(shallow_cm3,FLOOR)
        if rise < SPLIT_REPORT_MIN:
            continue
        # Using raw PLX interpolation makes the reported peak height comparable
        # with the legacy shallow maximum (also taken from raw PLX).
        raw_cm3 = _at(raw_b, float(z[i]))
        candidates.append({"idx": i, "z_nm":float(z[i]*1000.0),
                           "cm3":raw_cm3, "smooth_cm3":float(sm[i]),
                           "valley_nm":float(z[jmin]*1000.0),
                           "valley_cm3":float(sm[jmin]), "rise_r":rise})
    chosen = max(candidates,key=lambda c:c["cm3"]) if candidates else None
    if chosen:
        sec_nm = chosen["z_nm"]
        sec_cm3 = chosen["cm3"]
        sec_ratio = sec_cm3 / max(shallow_cm3,FLOOR)
        valley_nm = chosen["valley_nm"]
        valley_cm3 = chosen["valley_cm3"]
        valley_ratio = valley_cm3/max(min(sec_cm3,shallow_cm3),FLOOR)
        valley_drop = max(0.,1.0-valley_ratio)
    else:
        sec_nm,sec_cm3,sec_ratio = -1.0,0.0,0.0
        valley_nm,valley_ratio,valley_drop = -1.0,1.0,0.0

    global_deep = (gz > shallow_um+SECOND_MIN_SEPARATION_NM/1000.0 and
                   gc > shallow_cm3)
    edge = (gz <= GLOBAL_SEARCH[0]+GRID_STEP_UM*0.5 or
            gz >= GLOBAL_SEARCH[1]-GRID_STEP_UM*0.5)
    m = {
        "REBOUND_R": rebound,
        "SECOND_FOUND": float(bool(chosen)),
        "SECOND_NM": sec_nm,            # backward compatibility: local peak
        "SECOND_R": sec_ratio,
        "SECOND_PEAK_NM": sec_nm,
        "SECOND_PEAK_CM3": sec_cm3,
        "SECOND_OVER_SHALLOW_R": sec_ratio,
        "SECOND_PEAK_COUNT":float(len(candidates)),
        "DOMINANT_SECOND":float(bool(chosen and sec_cm3>shallow_cm3)),
        "VALLEY_NM":valley_nm,
        "VALLEY_R":valley_ratio,
        "VALLEY_DROP":valley_drop,
        "GLOBAL_PEAK_NM":gz*1000.0,
        "GLOBAL_PEAK_CM3":gc,
        "GLOBAL_OVER_SHALLOW_R":gc/max(shallow_cm3,FLOOR),
        "GLOBAL_DEEP_DOMINANT":float(global_deep),
        "GLOBAL_AT_BOUNDARY":float(edge),
        "SHALLOW_PEAK_NM":shallow_um*1000.0,
        "SHALLOW_PEAK_CM3":shallow_cm3,
        "SHALLOW_RESOLVED":float(shallow_valid),
        "SPLIT":rebound,
    }
    audit = [("SHALLOW_WINDOW_MAX",shallow_um*1000.0,shallow_cm3,
              -1.0,-1.0,0.0,int(shallow_valid)),
             ("GLOBAL_RAW_MAX",gz*1000.0,gc,-1.0,-1.0,
              gc/max(shallow_cm3,FLOOR),int(edge))]
    for c in sorted(candidates,key=lambda v:v["z_nm"]):
        audit.append(("SELECTED_POST_SHALLOW" if c is chosen else "OTHER_POST_SHALLOW",
                      c["z_nm"],c["cm3"],c["valley_nm"],
                      c["valley_cm3"],c["cm3"]/max(shallow_cm3,FLOOR),
                      1 if c is chosen else 0))
    return m, audit


def _crossings(z, b, p):
    c = []
    for i in range(len(z) - 1):
        if z[i] < 0.1 or z[i+1] > 0.9 + 1.e-10:
            continue
        d0, d1 = float(b[i] - p[i]), float(b[i+1] - p[i+1])
        if d0 == 0.0:
            c.append(float(z[i]))
        elif d0 * d1 < 0.0:
            c.append(float(z[i] - d0*(z[i+1]-z[i])/(d1-d0)))
    return c


def _bounded(err):
    if not math.isfinite(err):
        raise ValueError("Non-finite scoring component")
    err = max(0.0, err)
    return err / (1.0 + err)


def _score_parts(main_nm, ref_nm, main_r, sh, mid, tail, b462_r, rebound):
    if main_r <= 0 or b462_r <= 0:
        raise ValueError("Nonpositive ratio in score")
    penalties = {
        "PKPOS": _bounded(abs(main_nm - ref_nm) / POSITION_SCORE_SCALE_NM),
        "PKCONC": _bounded(abs(math.log10(main_r)) / PEAK_SCORE_SCALE_LOG),
        "SH": _bounded(sh / SHAPE_SCORE_SCALE_DEX),
        "MID": _bounded(mid / SHAPE_SCORE_SCALE_DEX),
        "TAIL": _bounded(tail / SHAPE_SCORE_SCALE_DEX),
        "B462": _bounded(abs(math.log10(b462_r)) / PEAK_SCORE_SCALE_LOG),
        "SPLIT": _bounded(rebound / SPLIT_SCORE_SCALE),
    }
    contrib = {k: 100.0 * WEIGHTS[k] * penalties[k] for k in WEIGHTS}
    return sum(contrib.values()), contrib, penalties


def evaluate(proc_plx):
    actual = _read_plx(proc_plx)
    ref = _ref_sections()
    a_b, a_p = _section(actual, "BActive"), _section(actual, "PActive")
    r_b, r_p = _section(ref, "BActive"), _section(ref, "PActive")
    z = np.round(np.arange(GRID_START_UM, GRID_END_UM + GRID_STEP_UM / 2,
                           GRID_STEP_UM), 10)
    b, p = _grid(a_b, z), _grid(a_p, z)
    rb, rp = _grid(r_b, z), _grid(r_p, z)

    # Frozen SDE peak from its actual sampled points; candidate from 5nm grid.
    rmz, rmc = _window_peak(r_b[0], r_b[1], MAIN_SEARCH)
    amz, amc = _window_peak(a_b[0], a_b[1], MAIN_SEARCH)
    main_nm = amz * 1000.0
    main_r = amc / rmc
    b462 = _at(a_b, SDE_JUNC_NM / 1000)
    b462_ref = _at(r_b, SDE_JUNC_NM / 1000)
    b462_r = b462 / b462_ref
    p462 = _at(a_p, SDE_JUNC_NM / 1000)
    split, peak_audit = _peak_diagnostics(z, b, a_b, amz, amc)
    cross = _crossings(z, b, p)
    junc_nm = cross[0] * 1000.0 if cross else -1.0
    jerr_nm = junc_nm - SDE_JUNC_NM if cross else -999.0

    # Peak-normalized shape error: separate curve shape from absolute peak dose.
    sh = _log_rmse(z, b, rb, SH_RANGE, True, amc, rmc)
    mid = _log_rmse(z, b, rb, MID_RANGE, True, amc, rmc)
    tail = _log_rmse(z, b, rb, TAIL_RANGE, True, amc, rmc)
    all_lrmse = _log_rmse(z, b, rb, ALL_RANGE, False)
    all_l1 = _rel_l1(z, b, rb, ALL_RANGE)
    sig = _sigma(z, b, ALL_RANGE)

    score, contributions, penalties = _score_parts(
        main_nm, rmz * 1000.0, main_r, sh, mid, tail,
        b462_r, split["REBOUND_R"])
    # A window endpoint on an uninterrupted rising slope is NOT an identified
    # shallow peak. A dominating deep/global peak is NOT an acceptable single peak.
    split_ok = (bool(split["SHALLOW_RESOLVED"]) and
                split["REBOUND_R"] <= SPLIT_OK_MAX and
                not bool(split["GLOBAL_DEEP_DOMINANT"]) and
                not bool(split["GLOBAL_AT_BOUNDARY"]))
    main_ok = (bool(split["SHALLOW_RESOLVED"]) and
               abs(main_nm - rmz*1000.0) <= PEAK_DEPTH_OK_MAX_NM and
               abs(main_r - 1.0) <= PEAK_RATIO_OK_MAX_REL_ERR)
    tail_ok = B462_OK_RANGE[0] <= b462_r <= B462_OK_RANGE[1]
    all_ok = split_ok and main_ok and tail_ok

    m = {
        "PW12_SCORE": score,
        "PW12_RUN_OK": 1.0,
        "PW12_ALL_OK": float(all_ok),
        "PW12_SPLIT_OK": float(split_ok),
        "PW12_MAIN_OK": float(main_ok),
        "PW12_TAIL_OK": float(tail_ok),
        "PW12_MAIN_NM": main_nm,
        "PW12_MAIN_CM3": amc,
        "PW12_MAIN_R": main_r,
        "PW12_SH_ERR": sh,
        "PW12_MID_ERR": mid,
        "PW12_TAIL_ERR": tail,
        "PW12_ALL_ERR": all_l1,
        "PW12_ALL_LRMSE": all_lrmse,
        "PW12_ALL_SIG": sig,
        "PW12_B462_CM3": b462,
        "PW12_B462_R": b462_r,
        "PW12_JUNC_NM": junc_nm,
        "PW12_JUNC_ERR": jerr_nm,
        "PW12_NCROSS": float(len(cross)),
        "PW12_SDE_MAIN_NM": rmz * 1000.0,
        "PW12_SDE_MAIN_CM3": rmc,
        "PW12_SDE_B462_CM3": b462_ref,
    }
    for name, val in split.items():
        m["PW12_" + name] = float(val)

    # SWB selected ratio columns; rest in the separate depth-point CSV/TXT.
    for nm in SWB_RATIO_DEPTHS:
        m["PW12_B%d_R" % nm] = _at(a_b, nm/1000.) / _at(r_b, nm/1000.)

    # Optional decomposition for DOE rank explainability.
    for k, value in contributions.items():
        m["PW12_SC_" + k] = float(value)

    point_rows = []
    for nm in DEPTHS_NM:
        a = _at(a_b, nm/1000.0)
        r = _at(r_b, nm/1000.0)
        point_rows.append((nm, a, r, a/r, 100.0*a/r))
    return m, (z, rb, b, rp, p), point_rows, penalties, peak_audit


def _write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def _make_plots(z, rb, b, prefix):
    # Plot failure is optional and MUST NOT invalidate numeric DOE output.
    if "sv" not in globals():
        return
    for label, left, right in (("ShallowShoulder", 30, 350),
                               ("JunctionTail", 350, 600)):
        file_name = prefix + "_" + label + "_plot.csv"
        rows = [(round(zz * 1000, 6), r, a)
                for zz, r, a in zip(z, rb, b)
                if left <= zz * 1000 + 1.0e-8 <= right]
        _write_csv(file_name, ["Depth_nm", "SDE_BActive_cm3",
                               "SProcess_BActive_cm3"], rows)
        try:
            dataset = "PW12_" + label
            sv.load_file(file_name, name=dataset)
            plot = sv.create_plot(name=dataset, xy=True)
            sv.create_curve(name=dataset+"_SDE", plot=plot, dataset=dataset,
                            axisX="Depth_nm", axisY="SDE_BActive_cm3")
            sv.create_curve(name=dataset+"_SP", plot=plot, dataset=dataset,
                            axisX="Depth_nm", axisY="SProcess_BActive_cm3")
            sv.set_plot_prop(plot=plot, show_grid=True, show_legend=True,
                             title="PW v1.2 original SDE vs SProcess Final F")
            sv.set_axis_prop(plot=plot, axis="x", title="Depth [nm]")
            sv.set_axis_prop(plot=plot, axis="y", title="BActive [cm^-3]", type="log")
        except Exception as exc:
            print("PW12: Optional plot warning: " + repr(exc))


def _resolve_process_path():
    override = os.environ.get("CMP_PW_PLX", "").strip()
    if override:
        return override
    node = str(PROCESS_NODE).strip()
    if node.isdigit():
        return "n" + node + "_F_r4p6.plx"
    raise RuntimeError("SWB macro @node|sprocess@ unresolved; offline: set CMP_PW_PLX")


def main():
    src = _resolve_process_path()
    metrics, arrays, points, penalties, peak_audit = evaluate(src)
    node = str(VIS_NODE).strip()
    prefix = "n" + (node if node.isdigit() else "offline") + "_PW_v1p3p0"
    z, rb, b, rp, p = arrays
    curve_file = prefix + "_profile_F.csv"
    _write_csv(curve_file,
               ["Depth_nm", "SDE_BActive_cm3", "SProcess_BActive_cm3",
                "BActive_ratio", "BActive_percent", "SDE_PActive_cm3",
                "SProcess_PActive_cm3"],
               [(round(zz*1000.0, 6), rr, aa, aa/rr, 100.0*aa/rr, pr, pa)
                for zz, rr, aa, pr, pa in zip(z, rb, b, rp, p)])
    points_file = prefix + "_depth_points.csv"
    _write_csv(points_file,
               ["Depth_nm", "SProcess_BActive_cm3", "SDE_BActive_cm3",
                "Ratio", "Percent_of_SDE"], points)

    # Complete metrics and auditable peak list, available without new SWB
    # Output Variables. These are CSVs in the SVisualPy working directory.
    all_metrics_file = prefix + "_all_metrics.csv"
    sorted_keys = sorted(metrics)
    _write_csv(all_metrics_file, sorted_keys,
               [[metrics[k] for k in sorted_keys]])
    peak_audit_file = prefix + "_peak_audit.csv"
    _write_csv(peak_audit_file,
               ["Peak_kind","Depth_nm","BActive_cm3","Preceding_valley_nm",
                "Valley_BActive_smoothed_cm3","Peak_over_shallow_R","Status_flag"],
               peak_audit)

    # Emit DOE summary early: optional plotting must not swallow output.
    details_file = prefix + "_metrics.txt"
    with open(details_file, "w", encoding="utf-8") as handle:
        handle.write("CMP SPAD PW-only SVisualPy v1.3.0 extended peak audit / SDE original PLX comparison\n")
        handle.write("PW-only final-F doping profile; no VBD/SCR/ATP claim\n")
        handle.write("process_PLX = " + os.path.abspath(src) + "\n")
        handle.write("SDE_original_PLX_SHA256 = " + REF_SHA256 + "\n")
        handle.write("SDE_reference_type = original_SDE_PLX_embedded_numeric_samples\n")
        handle.write("depth_sampling_nm = 5; depth_eval_nm = 30:600\n")
        handle.write("main_search_nm = 30:170 (SHALLOW only; NOT the GLOBAL maximum)\n")
        handle.write("global_search_nm = 30:900 (RAW BActive maximum)\n")
        handle.write("split_search_nm = post shallow + 30 to 900 (5 nm smoothed)\n")
        handle.write("SCORE_v1.3_changed_vs_v1.2.1 = TRUE (extended rebound)\n")
        handle.write("missing_second_peak_nm = -1; second_ratio = 0\n")
        handle.write("windows_nm = SH:30-110, MID:110-350, TAIL:350-600\n")
        handle.write("shape_error_definition = peak_normalized_log10_RMSE_dex\n")
        handle.write("all_err_definition = integrated_absolute_difference_over_SDE_integral\n")
        handle.write("split_definition = extended_smoothed_post_shallow_rebound_over_shallow_window_max\n")
        handle.write("split_threshold_assumption = %.6g\n" % SPLIT_OK_MAX)
        handle.write("PW12_SCORE = bounded_weighted_error_NOT_percent_match\n")
        handle.write("PW12_ALL_OK = provisional_main_and_tail_and_split_gates\n")
        handle.write("PW12_JUNC_NM = BActive_equals_PActive_not_SDevice_SCR\n")
        handle.write("JUNC_input = DNW_from_same_process_PLX; not_in_PW12_SCORE\n")
        handle.write("SECOND_NM and SECOND_PEAK_NM -1 = no resolved post-shallow peak\n")
        handle.write("NO_JUNCTION_NM = -1; JUNC_ERR=-999; NCROSS=0\n")
        handle.write("Score_weights = " + repr(WEIGHTS) + "\n")
        handle.write("\n[DEPTHWISE_RATIOS]\n")
        for nm, act, ref, ratio, pct in points:
            handle.write("%.6f nm: SProcess %.6g cm-3 / SDE %.6g cm-3 = %.6f (%.2f%%)\n"
                         % (nm, act, ref, ratio, pct))
        handle.write("\n[SCORE_COMPONENTS_0_TO_100_POINT_CONTRIBUTIONS]\n")
        for key in WEIGHTS:
            handle.write("%s: %.8f points (scaled error %.8f)\n" %
                         (key, metrics["PW12_SC_" + key], penalties[key]))
        handle.write("\n[DOE_METRICS]\n")
        for key, val in metrics.items():
            handle.write("%s = %.12g\n" % (key, val))

    # Legacy eight metrics plus optional audited diagnostics go to SWB DOE.
    # IMPORTANT: all remaining calculated values and all score contributions
    # are still written to *_metrics.txt and *_depth_points.csv above.
    # The weighted scoring formula is preserved, but its rebound input and
    # peak/split gates are stricter than v1.2.1; scores MUST be recomputed.
    SWB_SUMMARY_KEYS = (
        "PW12_SCORE",      # integrated weighted mismatch; lower is better
        "PW12_MAIN_NM",    # shallow main peak depth [nm]
        "PW12_MAIN_R",     # main peak concentration / SDE target
        "PW12_B462_R",     # boron at SDE junction depth / SDE target
        "PW12_REBOUND_R",  # post-peak split rise / main peak concentration
        "PW12_SPLIT_OK",   # 1: meets provisional split limit
        "PW12_ALL_OK",     # 1: peak, tail and split provisional gates all pass
        "PW12_RUN_OK",     # 1: analysis completed
    )
    # SWB will collect only names registered as OUTPUT VARIABLES, not inputs.
    # Keep the eight pre-existing names in place; adding the optional names
    # below to Output Variables is needed only to view them in the SWB table.
    SWB_OPTIONAL_KEYS = (
        "PW12_SHALLOW_PEAK_NM",
        "PW12_SHALLOW_RESOLVED",
        "PW12_GLOBAL_PEAK_NM",
        "PW12_GLOBAL_PEAK_CM3",
        "PW12_GLOBAL_AT_BOUNDARY",
        "PW12_SECOND_PEAK_NM",
        "PW12_SECOND_OVER_SHALLOW_R",
        "PW12_DOMINANT_SECOND",
        "PW12_GLOBAL_DEEP_DOMINANT",
        "PW12_SECOND_FOUND",
    )
    for key in SWB_SUMMARY_KEYS + SWB_OPTIONAL_KEYS:
        print("DOE: %s %.12g" % (key, metrics[key]))
    print("PW12: Analysis complete; SCORE lower is better, ALL_OK=1 required for acceptance")
    print("PW12: Process = " + src)
    print("PW12: Output = " + details_file + " / " + points_file + " / " + all_metrics_file + " / " + peak_audit_file)
    _make_plots(z, rb, b, prefix)


# The SWB #PYTHON interpreter may not define __name__ or __file__.
# Top-level execution is intentional, and SWB substitutions remain strings.
print("PW12: START v1.3.0 peak audit, working directory = " + os.getcwd())
try:
    main()
except Exception as exc:
    print("PW12: ERROR " + repr(exc))
    traceback.print_exc()
    print("DOE: PW12_RUN_OK 0")
    node = str(VIS_NODE).strip()
    err_file = "n" + (node if node.isdigit() else "offline") + "_PW_v1p3p0_error.txt"
    try:
        with open(err_file, "w", encoding="utf-8") as fh:
            traceback.print_exc(file=fh)
    except Exception:
        pass
    raise