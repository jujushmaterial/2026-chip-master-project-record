#setdep @node|sprocess@
# =============================================================================
# CMP SPAD | PW-only Profile Screening SVisualPy v1.0 | 2026-10-12
# =============================================================================
# Source concept: Triple-DNW Profile Screening SVisualPy v0.4 (GitHub, main).
# Purpose: inspect PW Shallow Main Peak and junction-side Tail separately.
# DNW PActive is read internally ONLY to calculate the PW/DNW junction (JUNC).
# No DNW plots, DNW metrics, or DNW penalties are emitted.
#
# SCORE and shape reference are exploratory SURROGATE metrics, not measured
# performance and not comparable to v0.4 Triple-DNW SCORE.
# Frozen SDE single-point anchors are listed below; the rest of the SDE
# reference curve is an analytic Gaussian SURROGATE, NOT the full SDE PLX.
#
# This is an SVisualPy command; @node@ macros are resolved by Sentaurus SWB.
# =============================================================================

import os
import fnmatch
import numpy as np

VIS_NODE = @node@
SNODE = @node|sprocess@

AR_FILE = f"n{SNODE}_A_R_r4p6.plx"
F_FILE = f"n{SNODE}_F_r4p6.plx"  # optional, consistent with v0.4
PREFIX = f"n{VIS_NODE}_PW_v1p0"
METRICS_FILE = f"{PREFIX}_metrics.txt"
AR_CSV = f"{PREFIX}_AR_compare.csv"
F_CSV = f"{PREFIX}_F_compare.csv"
SH_PLOT_CSV = f"{PREFIX}_AR_shallow_plot.csv"
TAIL_PLOT_CSV = f"{PREFIX}_AR_tail_plot.csv"

# ----- Reference anchors: frozen SDE baseline -------------------------------
SDE_PW_PEAK_DEPTH_UM = 0.1093           # 109.3 nm, extracted anchor
SDE_PW_PEAK_CM3 = 5.954e17             # extracted anchor
SDE_PW_GAUSS_SIGMA_UM = 0.2000        # analytic Gaussian surrogate parameter
SDE_JUNCTION_DEPTH_UM = 0.4626966588130754
SDE_CROSS_CONC_CM3 = 1.159e17          # extracted crossing concentration
PW_BACKGROUND_CM3 = 1.0e15
LOG_FLOOR_CM3 = 1.0e14

# ----- Windows: exploratory, fixed across all DOE rows ----------------------
PW_PEAK_WINDOW_UM = (0.030, 0.250)   # preserve v0.4 PW main peak selection
SHALLOW_WINDOW_UM = (0.030, 0.200)
TAIL_SIGMA_WINDOW_UM = (0.200, 0.500)
TAIL_SCORE_WINDOW_UM = (0.300, 0.500)
ALL_SIGMA_WINDOW_UM = (0.000, 0.600)
PW_SPLIT_WINDOW_UM = (0.000, 0.600)
JUNC_SEARCH_WINDOW_UM = (0.100, 0.900)
PW_SPLIT_MIN_SEP_UM = 0.030
PW_SAMPLE_DEPTHS_NM = [100, 200, 250, 300, 350, 400, 450, 500]

# ----- PW-only SCORE: user-reviewed proposal, not a literature value ---------
# Each normalized error e >= 0 is bounded by e/(1+e), 0 best, 1 worst.
# Tail RMSE includes 462.7 nm, so PW462 adds deliberate local emphasis.
W_PEAK = 0.25
W_DEPTH = 0.10
W_SHAPE = 0.15
W_TAIL = 0.25
W_PW462 = 0.20
W_SPLIT = 0.05
RP_SCALE_NM = 20.0
LOG_RATIO_SCALE = np.log10(1.20)  # 20% multiplicative factor
LOG_RMSE_SCALE_DEX = 0.10


def _get(dataset, name):
    return np.asarray(sv.get_variable_data(varname=name, dataset=dataset), dtype=float)


def _pick_exact(names, options):
    lower = {str(name).lower(): name for name in names}
    for option in options:
        if option.lower() in lower:
            return lower[option.lower()]
    return None


def _pick_pattern(names, patterns, reject_suffixes=()):
    for pat in patterns:
        for name in names:
            s = str(name).lower()
            if s.endswith(tuple(z.lower() for z in reject_suffixes)):
                continue
            if fnmatch.fnmatch(s, pat.lower()):
                return name
    return None


def _unique_sorted(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.shape != y.shape:
        raise ValueError("PLX x and y lengths are inconsistent")
    keep = np.isfinite(x) & np.isfinite(y)
    x, y = x[keep], y[keep]
    if len(x) < 2:
        raise ValueError("PLX has fewer than two valid data points")
    order = np.argsort(x, kind="mergesort")
    x, y = x[order], y[order]
    xu, inv = np.unique(x, return_inverse=True)
    # Duplicate depth locations: same policy as original v0.4 (arithmetic mean).
    yu = np.bincount(inv, weights=y) / np.maximum(np.bincount(inv), 1)
    return xu, yu


def _load_plx(filename, dataset):
    if not os.path.isfile(filename):
        return None
    sv.load_file(filename, name=dataset)
    names = list(sv.list_variables(dataset=dataset))
    print(f"PW_ONLY: {filename} variables={names}")
    common_x = _pick_exact(names, ["X", "x", "Depth", "Position"])
    if common_x is None:
        common_x = _pick_pattern(names, ["*Depth*", "*Position*"], (" y",))
    bx = _pick_exact(names, ["BActive x", "BoronActiveConcentration x"])
    if bx is None:
        bx = _pick_pattern(names, ["*BActive* x", "*Boron*Active* x"])
    px = _pick_exact(names, ["PActive x", "PhosphorusActiveConcentration x"])
    if px is None:
        px = _pick_pattern(names, ["*PActive* x", "*Phosphorus*Active* x"])
    by = _pick_exact(names, ["BActive y", "BActive", "BoronActiveConcentration y",
                             "BoronActiveConcentration"])
    if by is None:
        by = _pick_pattern(names, ["*BActive* y", "*Boron*Active* y",
                                     "*BActive*", "*Boron*Active*"], (" x",))
    py = _pick_exact(names, ["PActive y", "PActive", "PhosphorusActiveConcentration y",
                             "PhosphorusActiveConcentration"])
    if py is None:
        py = _pick_pattern(names, ["*PActive* y", "*Phosphorus*Active* y",
                                     "*PActive*", "*Phosphorus*Active*"], (" x",))
    bx = bx if bx is not None else common_x
    px = px if px is not None else common_x
    if any(v is None for v in (bx, px, by, py)):
        raise RuntimeError(f"Required BActive/PActive PLX series not found: {filename}; {names}")
    xb, b = _unique_sorted(_get(dataset, bx), _get(dataset, by))
    xp, p = _unique_sorted(_get(dataset, px), _get(dataset, py))
    if xb.size == xp.size and np.allclose(xb, xp, rtol=0, atol=1e-12):
        return xb, b, p
    lo, hi = max(xb[0], xp[0]), min(xb[-1], xp[-1])
    if hi <= lo:
        raise RuntimeError("BActive and PActive depth ranges do not overlap")
    x = np.unique(np.concatenate([xb[(xb >= lo) & (xb <= hi)],
                                  xp[(xp >= lo) & (xp <= hi)]]))
    return x, np.interp(x, xb, b), np.interp(x, xp, p)


def _target_pw(x):
    return (SDE_PW_PEAK_CM3 * np.exp(-0.5 *
            ((np.asarray(x) - SDE_PW_PEAK_DEPTH_UM) / SDE_PW_GAUSS_SIGMA_UM) ** 2)
            + PW_BACKGROUND_CM3)


def _interp(x, y, pos):
    if len(x) < 2 or pos < x[0] or pos > x[-1]:
        return np.nan
    return float(np.interp(pos, x, y))


def _segment(x, *ys, window):
    lo, hi = window
    mask = np.isfinite(x) & (x >= lo) & (x <= hi)
    for y in ys:
        mask &= np.isfinite(y)
    return (x[mask], *[y[mask] for y in ys])


def _peak(x, y, window):
    xx, yy = _segment(x, y, window=window)
    if xx.size == 0:
        return np.nan, np.nan
    k = int(np.argmax(yy))
    return float(xx[k]), float(yy[k])


def _crossings(x, y, level, window):
    keep = np.isfinite(x) & np.isfinite(y)
    xx, yy = x[keep], y[keep]
    if xx.size < 2:
        return np.array([], dtype=float)
    yy = yy - level
    hit = (yy[:-1] * yy[1:] <= 0) & (yy[:-1] != yy[1:])
    if not np.any(hit):
        return np.array([], dtype=float)
    xc = xx[:-1][hit] - yy[:-1][hit] * (xx[1:][hit] - xx[:-1][hit]) / (yy[1:][hit] - yy[:-1][hit])
    return xc[(xc >= window[0]) & (xc <= window[1])]


def _moving_average(y, n=5):
    if y.size < n:
        return y.copy()
    pad = n // 2
    return np.convolve(np.pad(y, (pad, pad), mode="edge"),
                       np.ones(n) / float(n), mode="valid")[:y.size]


def _pw_split(x, y):
    xx, yy = _segment(x, y, window=PW_SPLIT_WINDOW_UM)
    empty = dict(second_depth=np.nan, second_ratio=0.0, valley_ratio=1.0, severity=0.0)
    if xx.size < 7:
        return empty
    smooth = _moving_average(yy)
    loc = np.where((smooth[1:-1] > smooth[:-2]) & (smooth[1:-1] >= smooth[2:]))[0] + 1
    if loc.size < 2:
        return empty
    order = loc[np.argsort(smooth[loc])[::-1]]
    primary = int(order[0])
    second = next((int(z) for z in order[1:]
                   if abs(xx[int(z)] - xx[primary]) >= PW_SPLIT_MIN_SEP_UM), None)
    if second is None:
        return empty
    ratio = float(smooth[second] / smooth[primary]) if smooth[primary] > 0 else 0.0
    left, right = sorted((primary, second))
    if right - left < 2:
        return dict(second_depth=float(xx[second]), second_ratio=ratio,
                    valley_ratio=1.0, severity=0.0)
    valley = float(np.min(smooth[left:right + 1]))
    small_peak = float(min(smooth[primary], smooth[second]))
    valley_ratio = np.clip(valley / small_peak, 0.0, 1.0) if small_peak > 0 else 1.0
    ratio = np.clip(ratio, 0.0, 1.0)
    return dict(second_depth=float(xx[second]), second_ratio=float(ratio),
                valley_ratio=float(valley_ratio), severity=float(ratio * (1.0 - valley_ratio)))


def _shape_rmse(x, actual, target, window):
    xx, aa, tt = _segment(x, actual, target, window=window)
    if xx.size < 3 or max(aa) <= 0 or max(tt) <= 0:
        return np.nan
    a = np.maximum(aa / max(aa), 1.0e-5)
    t = np.maximum(tt / max(tt), 1.0e-5)
    return float(np.sqrt(np.mean((np.log10(a) - np.log10(t)) ** 2)))


def _log_rmse(x, actual, target, window):
    xx, aa, tt = _segment(x, actual, target, window=window)
    if xx.size < 3:
        return np.nan
    a = np.maximum(aa, LOG_FLOOR_CM3)
    t = np.maximum(tt, LOG_FLOOR_CM3)
    return float(np.sqrt(np.mean((np.log10(a) - np.log10(t)) ** 2)))


def _sigma_equiv(x, y, window):
    # Concentration-weighted standard deviation *within this depth window*.
    # This is NOT the separate implant's longitudinal straggle.
    xx, yy = _segment(x, y, window=window)
    if xx.size < 3:
        return np.nan
    w = np.maximum(yy - PW_BACKGROUND_CM3, 0.0)
    area = np.trapz(w, xx)
    if area <= 0:
        return np.nan
    mean = np.trapz(xx * w, xx) / area
    variance = np.trapz((xx - mean) ** 2 * w, xx) / area
    return float(np.sqrt(max(variance, 0.0))) * 1000.0  # nm


def _p_bound(error):
    if not np.isfinite(error):
        return 1.0  # Missing metric must not improve SCORE.
    e = max(float(error), 0.0)
    return e / (1.0 + e)


def _p_ratio(actual, target):
    if (not np.isfinite(actual) or not np.isfinite(target) or
            actual <= 0 or target <= 0):
        return 1.0
    return _p_bound(abs(np.log10(actual / target)) / LOG_RATIO_SCALE)


def _p_rmse(value):
    return _p_bound(value / LOG_RMSE_SCALE_DEX)


def _analyze(x, b, p):
    target = _target_pw(x)
    rp_um, pk = _peak(x, b, PW_PEAK_WINDOW_UM)
    shape = _shape_rmse(x, b, target, SHALLOW_WINDOW_UM)
    tail_rmse = _log_rmse(x, b, target, TAIL_SCORE_WINDOW_UM)
    b462 = _interp(x, b, SDE_JUNCTION_DEPTH_UM)
    split = _pw_split(x, b)
    crossing = _crossings(x, b - p, 0.0, JUNC_SEARCH_WINDOW_UM)
    # Preserve the original v0.4 convention: first BActive/PActive crossing.
    junc_nm = float(crossing[0] * 1000.0) if crossing.size else np.nan

    sig_sh = _sigma_equiv(x, b, SHALLOW_WINDOW_UM)
    sig_tail = _sigma_equiv(x, b, TAIL_SIGMA_WINDOW_UM)
    sig_all = _sigma_equiv(x, b, ALL_SIGMA_WINDOW_UM)
    target_sig_sh = _sigma_equiv(x, target, SHALLOW_WINDOW_UM)
    target_sig_tail = _sigma_equiv(x, target, TAIL_SIGMA_WINDOW_UM)
    target_sig_all = _sigma_equiv(x, target, ALL_SIGMA_WINDOW_UM)

    p_peak = _p_ratio(pk, SDE_PW_PEAK_CM3)
    p_rp = _p_bound(abs(rp_um * 1000.0 - SDE_PW_PEAK_DEPTH_UM * 1000.0) / RP_SCALE_NM)
    p_shape = _p_rmse(shape)
    p_tail = _p_rmse(tail_rmse)
    p_462 = _p_ratio(b462, SDE_CROSS_CONC_CM3)
    p_split = float(np.clip(split["severity"], 0.0, 1.0))
    score = 100.0 * (W_PEAK * p_peak + W_DEPTH * p_rp + W_SHAPE * p_shape +
                     W_TAIL * p_tail + W_PW462 * p_462 + W_SPLIT * p_split)

    result = dict(
        PW_SCORE=score,
        PW_SH_RP=rp_um * 1000.0,
        PW_SH_PK_R=pk / SDE_PW_PEAK_CM3 if np.isfinite(pk) else np.nan,
        PW_SH_SIG=sig_sh,
        PW_TAIL_SIG=sig_tail,
        PW_TAIL_RMSE=tail_rmse,
        PW462_R=b462 / SDE_CROSS_CONC_CM3 if np.isfinite(b462) else np.nan,
        JUNC=junc_nm,
        PW_SPLIT=split["severity"],
        PW_ALL_SIG=sig_all,
        PW_SH_PK_CM3=pk,
        PW_SH_SHAPE_RMSE=shape,
        PW_SH_SIG_TARGET=target_sig_sh,
        PW_TAIL_SIG_TARGET=target_sig_tail,
        PW_ALL_SIG_TARGET=target_sig_all,
        PW_SH_SIG_DELTA=sig_sh - target_sig_sh,
        PW_TAIL_SIG_DELTA=sig_tail - target_sig_tail,
        PW_ALL_SIG_DELTA=sig_all - target_sig_all,
        PW462_CM3=b462,
        PW_TARGET_462_CM3=SDE_CROSS_CONC_CM3,
        JUNC_ERR_NM=junc_nm - SDE_JUNCTION_DEPTH_UM * 1000.0,
        JUNC_CROSSINGS_COUNT=float(crossing.size),
        PW_SPLIT_SECOND_NM=split["second_depth"] * 1000.0,
        PW_SPLIT_SECOND_RATIO=split["second_ratio"],
        PW_SPLIT_VALLEY_RATIO=split["valley_ratio"],
        P_PK=p_peak, P_RP=p_rp, P_SHAPE=p_shape, P_TAIL=p_tail,
        P_PW462=p_462, P_SPLIT=p_split,
    )
    for depth_nm in PW_SAMPLE_DEPTHS_NM:
        pos = depth_nm / 1000.0
        actual = _interp(x, b, pos)
        ref = _interp(x, target, pos)
        result[f"PW_C{depth_nm}_CM3"] = actual
        result[f"PW_C{depth_nm}_TARGET_GAUSS_CM3"] = ref
        result[f"PW_C{depth_nm}_R"] = actual / ref if np.isfinite(actual) and ref > 0 else np.nan
    return result, target


def _save_csv(path, columns):
    np.savetxt(path, np.column_stack([np.asarray(v, dtype=float) for v in columns.values()]),
               delimiter=",", header=",".join(columns), comments="", fmt="%.12e")


def _write_compare(path, x, b, target, depth_range):
    xx, bb, tt = _segment(x, b, target, window=depth_range)
    _save_csv(path, {"Depth_nm": xx * 1000.0,
                     "SProcess_BActive_cm3": bb,
                     "SDE_PW_GaussianSurrogate_cm3": tt})


def _make_pw_plot(csvpath, dataset, plotname, caption):
    # Plot data are pre-cropped to control x-range without relying on
    # Sentaurus Visual version-specific axis-limits keywords.
    sv.load_file(csvpath, name=dataset)
    plot = sv.create_plot(name=plotname, xy=True)
    sv.create_curve(name=f"{plotname}_SProcess", plot=plot, dataset=dataset,
                    axisX="Depth_nm", axisY="SProcess_BActive_cm3")
    sv.create_curve(name=f"{plotname}_Target", plot=plot, dataset=dataset,
                    axisX="Depth_nm", axisY="SDE_PW_GaussianSurrogate_cm3")
    sv.set_plot_prop(plot=plot, show_grid=True, show_legend=True, title=caption)
    sv.set_axis_prop(plot=plot, axis="x", title="Depth from bulk-Si surface [nm]")
    sv.set_axis_prop(plot=plot, axis="y", title="BActive [cm^-3]", type="log")
    return plot


def _write_value(fp, key, val):
    if val is None or not np.isfinite(val):
        fp.write(f"{key} = NA\n")
    else:
        fp.write(f"{key} = {float(val):.12g}\n")


def _emit(fp, key, value):
    _write_value(fp, key, value)
    if value is None or not np.isfinite(value):
        print(f"DOE: {key} x")
    else:
        print(f"DOE: {key} {float(value):.12g}")


# ----- Evaluate post-RTA dataset; final profile is diagnostic if available ---
ar = _load_plx(AR_FILE, "PW_AR_PLX")
if ar is None:
    raise RuntimeError(f"Required SProcess post-RTA PLX not found: {AR_FILE}")

x_ar, b_ar, p_ar = ar
m_ar, pw_target_ar = _analyze(x_ar, b_ar, p_ar)
_write_compare(AR_CSV, x_ar, b_ar, pw_target_ar, ALL_SIGMA_WINDOW_UM)
_write_compare(SH_PLOT_CSV, x_ar, b_ar, pw_target_ar, (0.0, 0.250))
_write_compare(TAIL_PLOT_CSV, x_ar, b_ar, pw_target_ar, (0.200, 0.500))

try:
    _make_pw_plot(SH_PLOT_CSV, "PW_SH_CSV", "PW_Shallow_Compare",
                  "PW Shallow 0-250 nm | post-RTA | SDE Gaussian surrogate")
    _make_pw_plot(TAIL_PLOT_CSV, "PW_TAIL_CSV", "PW_Tail_Compare",
                  "PW Junction-side Tail 200-500 nm | post-RTA | SDE Gaussian surrogate")
except Exception as exc:
    print(f"PW_ONLY: Plot warning (metrics still available): {exc}")

f = _load_plx(F_FILE, "PW_FINAL_PLX")
m_final = None
if f is not None:
    x_f, b_f, p_f = f
    m_final, target_f = _analyze(x_f, b_f, p_f)
    _write_compare(F_CSV, x_f, b_f, target_f, ALL_SIGMA_WINDOW_UM)

SUMMARY_KEYS = [
    "PW_SCORE", "PW_SH_RP", "PW_SH_PK_R", "PW_SH_SIG", "PW_TAIL_SIG",
    "PW_TAIL_RMSE", "PW462_R", "JUNC", "PW_SPLIT", "PW_ALL_SIG",
]

with open(METRICS_FILE, "w", encoding="utf-8") as fp:
    fp.write("CMP SPAD PW-only Profile Screening SVisualPy v1.0\n")
    fp.write(f"post_RTA_PLX = {AR_FILE}\n")
    fp.write(f"optional_final_PLX = {F_FILE if f is not None else 'NA'}\n")
    fp.write("DOE_basis = post_RTA_AR_profile\n")
    fp.write("score_definition = PW_only_bounded_weighted_sum; lower_is_better; not_percent\n")
    fp.write("score_reference = extracted_SDE_peak_and_crossing_anchors_plus_analytic_Gaussian_surrogate\n")
    fp.write("full_SDE_PLX_available = NO\n")
    fp.write("sigma_definition = window_truncated_concentration_weighted_std_not_implant_straggle\n")
    fp.write("JUNC_definition = first_BActive_equals_PActive_crossing_within_100_to_900_nm\n")
    fp.write("JUNC_in_PW_SCORE = NO\n")
    fp.write("SDE_PW_peak_depth_nm = 109.3\n")
    fp.write("SDE_PW_peak_cm3 = 5.954e17\n")
    fp.write("SDE_cross_depth_nm = 462.6966588130754\n")
    fp.write("SDE_cross_concentration_cm3 = 1.159e17\n")
    fp.write("shallow_window_nm = 30,200\n")
    fp.write("tail_sigma_window_nm = 200,500\n")
    fp.write("tail_score_window_nm = 300,500\n")
    fp.write("all_sigma_window_nm = 0,600\n")
    fp.write("score_weights = peak:0.25,depth:0.10,shallow_shape:0.15,tail_rmse:0.25,PW462:0.20,split:0.05\n")
    fp.write("score_scales = peak_and_PW462:log10(1.20),Rp:20nm,RMSE:0.10dex\n")
    fp.write("WARNING = Tail_score_window_contains_462nm; PW462_adds_extra_local_weight\n")
    fp.write("WARNING = SDE_curve_is_surrogate; SDE_462_point_is_independently_extracted_anchor\n")
    fp.write("WARNING = PW_Shallow/Tail_are_depth_windows_not_isolated_implant_components\n")
    fp.write("\n[POST_RTA_DETAIL]\n")
    for name in sorted(m_ar):
        _write_value(fp, "AR_" + name, m_ar[name])
    if m_final is not None:
        fp.write("\n[FINAL_DETAIL]\n")
        for name in sorted(m_final):
            _write_value(fp, "F_" + name, m_final[name])
    fp.write("\n[DOE_SUMMARY]\n")
    for name in SUMMARY_KEYS:
        _emit(fp, name, m_ar.get(name, np.nan))

try:
    sv.windows_style(style="grid")
except Exception:
    pass
print("PW_ONLY_PROFILE_SCREENING_V1P0: COMPLETE")