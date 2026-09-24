#setdep @node|sprocess@
import os
import fnmatch
import numpy as np

VIS_NODE = @node@
SNODE = @node|sprocess@

AR_FILE = f"n{SNODE}_A_R_r4p6.plx"
F_FILE  = f"n{SNODE}_F_r4p6.plx"

PREFIX = f"n{VIS_NODE}_profile"
METRICS_FILE = f"{PREFIX}_metrics.txt"
AR_CSV = f"{PREFIX}_AR_compare.csv"
F_CSV  = f"{PREFIX}_F_compare.csv"

# SDE surrogate baseline targets
SDE_PW_RP_UM = 0.1093
SDE_PW_PEAK = 5.95e17
SDE_PW_SIGMA_UM = 0.2000

SDE_DNW_RP_UM = 1.0173
SDE_DNW_PEAK = 3.15e17
SDE_DNW_SIGMA_UM = 0.3806

# Frozen analytic PW/DNW crossing target
SDE_CROSS_UM = 0.4626966588130754

PW_BG = 1.0e15
PW_WINDOW = (0.0, 0.60)
PW_MAIN_WINDOW = (0.03, 0.25)
DNW_WINDOW = (0.20, 1.80)
MOMENT_WINDOW = (0.0, 2.50)
PROFILE_MAX_UM = 2.50
LOG_FLOOR = 1.0e14
DNW_SLOPE_WINDOW = (0.30, 0.60)

PW_SPLIT_MIN_SEP_UM = 0.03
DNW_SPLIT_MIN_SEP_UM = 0.08

PW_SAMPLE_NM = [100, 200, 250, 300, 400, 450, 500]
DNW_SAMPLE_NM = [450, 500, 600, 800, 1000, 1200, 1400]

# Composite SCORE weights: lower is better, not percent error.
W_PW_RP = 0.05
W_PW_PK = 0.04
W_PW_SHAPE = 0.06

W_DNW_RP = 0.08
W_DNW_PK = 0.08
W_DNW_SIG = 0.12
W_DNW_SHAPE = 0.17

W_JUNC = 0.10
W_P462 = 0.13
W_SLOPE = 0.12
W_SPLIT = 0.05

PW_RP_SCALE_NM = 20.0
DNW_RP_SCALE_NM = 50.0
DNW_SIG_SCALE_NM = 60.0
JUNC_SCALE_NM = 20.0

np.set_printoptions(precision=8, suppress=False)


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


def interp(x, y, xq):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.size < 2 or xq < x[0] or xq > x[-1]:
        return np.nan
    return float(np.interp(xq, x, y))


def gaussian(x, peak, rp, sigma):
    x = np.asarray(x, dtype=float)
    return peak * np.exp(-0.5 * ((x - rp) / sigma) ** 2)


def crossings(x, y, level, lo=-np.inf, hi=np.inf):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    x = x[m]
    y = y[m]
    if x.size < 2:
        return np.array([], dtype=float)
    idx = np.argsort(x, kind="mergesort")
    x = x[idx]
    y = y[idx]
    x1, x2 = x[:-1], x[1:]
    y1, y2 = y[:-1], y[1:]
    hit = (y2 != y1) & ((y1 - level) * (y2 - level) <= 0.0)
    if not np.any(hit):
        return np.array([], dtype=float)
    t = (level - y1[hit]) / (y2[hit] - y1[hit])
    good = (t >= 0.0) & (t <= 1.0)
    xc = x1[hit][good] + t[good] * (x2[hit][good] - x1[hit][good])
    return xc[(xc >= lo) & (xc <= hi)]


def crossing_between_profiles(x, a, b, lo, hi):
    return crossings(x, a - b, 0.0, lo=lo, hi=hi)


def peak_in_window(x, y, lo, hi):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y) & (x >= lo) & (x <= hi)
    if not np.any(m):
        return np.nan, np.nan
    xx = x[m]
    yy = y[m]
    k = int(np.argmax(yy))
    return float(xx[k]), float(yy[k])


def halfmax_metrics(x, y, peak_x, peak_y, lo, hi):
    if not np.isfinite(peak_x) or not np.isfinite(peak_y) or peak_y <= 0.0:
        return np.nan, np.nan, np.nan, 1.0
    c = crossings(x, y, 0.5 * peak_y, lo=lo, hi=hi)
    left = c[c < peak_x]
    right = c[c > peak_x]
    truncated = 0.0
    if left.size:
        xl = float(left[-1])
    else:
        xl = float(lo)
        truncated = 1.0
    xr = float(right[0]) if right.size else np.nan
    width = xr - xl if np.isfinite(xr) else np.nan
    return xl, xr, width, truncated


def moving_average(y, n=5):
    y = np.asarray(y, dtype=float)
    if y.size < n or n < 2:
        return y.copy()
    pad = n // 2
    yp = np.pad(y, (pad, pad), mode="edge")
    ker = np.ones(n, dtype=float) / float(n)
    z = np.convolve(yp, ker, mode="valid")
    return z[:y.size]


def split_metrics(x, y, lo, hi, min_sep_um):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y) & (x >= lo) & (x <= hi)
    xx = x[m]
    yy = y[m]
    empty = {
        "second_depth": np.nan,
        "second_value": np.nan,
        "second_ratio": 0.0,
        "valley_depth": np.nan,
        "valley_value": np.nan,
        "valley_ratio": 1.0,
        "severity": 0.0,
    }
    if xx.size < 7:
        return empty
    ys = moving_average(yy, 5)
    loc = np.where((ys[1:-1] > ys[:-2]) & (ys[1:-1] >= ys[2:]))[0] + 1
    if loc.size < 2:
        return empty
    order = loc[np.argsort(ys[loc])[::-1]]
    main_idx = int(order[0])
    second_idx = None
    for candidate in order[1:]:
        candidate = int(candidate)
        if abs(xx[candidate] - xx[main_idx]) >= min_sep_um:
            second_idx = candidate
            break
    if second_idx is None:
        return empty
    second_ratio = float(ys[second_idx] / ys[main_idx]) if ys[main_idx] > 0.0 else 0.0
    left_idx = min(main_idx, second_idx)
    right_idx = max(main_idx, second_idx)
    if right_idx - left_idx < 2:
        return {
            "second_depth": float(xx[second_idx]),
            "second_value": float(yy[second_idx]),
            "second_ratio": second_ratio,
            "valley_depth": np.nan,
            "valley_value": np.nan,
            "valley_ratio": 1.0,
            "severity": 0.0,
        }
    valley_idx = left_idx + int(np.argmin(ys[left_idx:right_idx + 1]))
    lower_peak = min(float(ys[main_idx]), float(ys[second_idx]))
    valley_ratio = float(ys[valley_idx] / lower_peak) if lower_peak > 0.0 else 1.0
    valley_ratio = min(max(valley_ratio, 0.0), 1.0)
    second_ratio = min(max(second_ratio, 0.0), 1.0)
    severity = second_ratio * (1.0 - valley_ratio)
    return {
        "second_depth": float(xx[second_idx]),
        "second_value": float(yy[second_idx]),
        "second_ratio": second_ratio,
        "valley_depth": float(xx[valley_idx]),
        "valley_value": float(yy[valley_idx]),
        "valley_ratio": valley_ratio,
        "severity": severity,
    }


def dose_integral(x, y, lo, hi, background=0.0):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y) & (x >= lo) & (x <= hi)
    if np.count_nonzero(m) < 2:
        return np.nan
    xx = x[m]
    yy = np.maximum(y[m] - background, 0.0)
    return float(np.trapz(yy, xx) * 1.0e-4)


def sigma_equiv(x, y, lo, hi, background=0.0):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y) & (x >= lo) & (x <= hi)
    if np.count_nonzero(m) < 3:
        return np.nan
    xx = x[m]
    ww = np.maximum(y[m] - background, 0.0)
    area = np.trapz(ww, xx)
    if area <= 0.0:
        return np.nan
    mu = np.trapz(xx * ww, xx) / area
    var = np.trapz((xx - mu) ** 2 * ww, xx) / area
    return float(np.sqrt(max(var, 0.0)))


def log_rmse(x, actual, target, lo, hi, floor=LOG_FLOOR):
    x = np.asarray(x, dtype=float)
    actual = np.asarray(actual, dtype=float)
    target = np.asarray(target, dtype=float)
    m = (
        np.isfinite(x) & np.isfinite(actual) & np.isfinite(target) &
        (x >= lo) & (x <= hi)
    )
    if np.count_nonzero(m) < 3:
        return np.nan
    a = np.maximum(actual[m], floor)
    t = np.maximum(target[m], floor)
    return float(np.sqrt(np.mean((np.log10(a) - np.log10(t)) ** 2)))


def shape_log_rmse(x, actual, target, lo, hi):
    x = np.asarray(x, dtype=float)
    actual = np.asarray(actual, dtype=float)
    target = np.asarray(target, dtype=float)
    m = (
        np.isfinite(x) & np.isfinite(actual) & np.isfinite(target) &
        (x >= lo) & (x <= hi)
    )
    if np.count_nonzero(m) < 3:
        return np.nan
    a = actual[m]
    t = target[m]
    amax = np.max(a)
    tmax = np.max(t)
    if amax <= 0.0 or tmax <= 0.0:
        return np.nan
    an = np.maximum(a / amax, 1.0e-5)
    tn = np.maximum(t / tmax, 1.0e-5)
    return float(np.sqrt(np.mean((np.log10(an) - np.log10(tn)) ** 2)))


def log_slope(x, y, lo, hi, floor=LOG_FLOOR):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = (
        np.isfinite(x) & np.isfinite(y) &
        (x >= lo) & (x <= hi) & (y > 0.0)
    )
    if np.count_nonzero(m) < 3:
        return np.nan
    xx = x[m]
    yy = np.maximum(y[m], floor)
    coeff = np.polyfit(xx, np.log10(yy), 1)
    return float(coeff[0])


def bounded_penalty(error_value):
    if error_value is None or not np.isfinite(error_value):
        return 1.0
    e = max(float(error_value), 0.0)
    return float(e / (1.0 + e))


def log_ratio_error(actual, target):
    if (
        actual is None or target is None or
        not np.isfinite(actual) or not np.isfinite(target) or
        actual <= 0.0 or target <= 0.0
    ):
        return np.nan
    return float(abs(np.log10(actual / target)))


def slope_ratio(actual, target):
    if (
        actual is None or target is None or
        not np.isfinite(actual) or not np.isfinite(target) or
        target == 0.0
    ):
        return np.nan
    return float(actual / target)


def slope_penalty(actual, target):
    if (
        actual is None or target is None or
        not np.isfinite(actual) or not np.isfinite(target) or
        actual == 0.0 or target == 0.0
    ):
        return 1.0
    if actual * target <= 0.0:
        return 1.0
    err = abs(np.log10(abs(actual / target)))
    return bounded_penalty(err)


def save_csv(filename, columns):
    names = list(columns.keys())
    arrays = [np.asarray(columns[k], dtype=float) for k in names]
    data = np.column_stack(arrays)
    np.savetxt(
        filename, data, delimiter=",",
        header=",".join(names), comments="", fmt="%.12e"
    )


def write_metric(fh, name, value):
    if value is None or not np.isfinite(value):
        fh.write(f"{name} = NA\n")
    else:
        fh.write(f"{name} = {float(value):.12g}\n")


def emit(fh, name, value):
    if value is None or not np.isfinite(value):
        fh.write(f"{name} = NA\n")
        print(f"DOE: {name} x")
    else:
        v = float(value)
        fh.write(f"{name} = {v:.12g}\n")
        print(f"DOE: {name} {v:.12g}")


def load_plx(filename, dataset):
    if not os.path.isfile(filename):
        return None
    sv.load_file(filename, name=dataset)
    xname = pickvar(dataset, ["X", "x", "*Depth*", "*Position*"])
    bname = pickvar(
        dataset,
        ["BActive", "*BActive*", "BoronActiveConcentration", "*Boron*Active*"]
    )
    pname = pickvar(
        dataset,
        ["PActive", "*PActive*", "PhosphorusActiveConcentration", "*Phosphorus*Active*"]
    )
    if xname is None or bname is None or pname is None:
        raise RuntimeError(
            f"PLX variables not found in {filename}: "
            f"X={xname}, BActive={bname}, PActive={pname}"
        )
    x = get_data(dataset, xname)
    b = get_data(dataset, bname)
    p = get_data(dataset, pname)
    return sort_unique_many(x, b, p)


def analyze_profile(x, b, p):
    sde_pw = gaussian(x, SDE_PW_PEAK, SDE_PW_RP_UM, SDE_PW_SIGMA_UM) + PW_BG
    sde_dnw = gaussian(x, SDE_DNW_PEAK, SDE_DNW_RP_UM, SDE_DNW_SIGMA_UM)

    pw_global_x, pw_global_peak = peak_in_window(
        x, b, PW_WINDOW[0], PW_WINDOW[1]
    )
    pw_x, pw_peak = peak_in_window(
        x, b, PW_MAIN_WINDOW[0], PW_MAIN_WINDOW[1]
    )
    dnw_x, dnw_peak = peak_in_window(
        x, p, DNW_WINDOW[0], DNW_WINDOW[1]
    )

    pw_l, pw_r, pw_w, pw_trunc = halfmax_metrics(
        x, b, pw_x, pw_peak, PW_WINDOW[0], PW_WINDOW[1]
    )
    dnw_l, dnw_r, dnw_w, dnw_trunc = halfmax_metrics(
        x, p, dnw_x, dnw_peak, 0.0, PROFILE_MAX_UM
    )

    xc = crossing_between_profiles(x, b, p, 0.10, 0.90)
    cross = float(xc[0]) if xc.size else np.nan

    pw_split = split_metrics(
        x, b, PW_WINDOW[0], PW_WINDOW[1], PW_SPLIT_MIN_SEP_UM
    )
    dnw_split = split_metrics(
        x, p, DNW_WINDOW[0], DNW_WINDOW[1], DNW_SPLIT_MIN_SEP_UM
    )
    overall_split = max(pw_split["severity"], dnw_split["severity"])

    pw_dose = dose_integral(
        x, b, MOMENT_WINDOW[0], MOMENT_WINDOW[1], background=PW_BG
    )
    dnw_dose = dose_integral(
        x, p, MOMENT_WINDOW[0], MOMENT_WINDOW[1], background=0.0
    )
    dnw_sigma = sigma_equiv(
        x, p, MOMENT_WINDOW[0], MOMENT_WINDOW[1], background=0.0
    )

    pw_log_err = log_rmse(
        x, b, sde_pw, PW_WINDOW[0], PW_WINDOW[1]
    )
    pw_shape_err = shape_log_rmse(
        x, b, sde_pw, PW_WINDOW[0], PW_WINDOW[1]
    )
    dnw_log_err = log_rmse(
        x, p, sde_dnw, DNW_WINDOW[0], DNW_WINDOW[1]
    )
    dnw_shape_err = shape_log_rmse(
        x, p, sde_dnw, DNW_WINDOW[0], DNW_WINDOW[1]
    )

    dnw_slope = log_slope(
        x, p, DNW_SLOPE_WINDOW[0], DNW_SLOPE_WINDOW[1]
    )
    sde_dnw_slope = log_slope(
        x, sde_dnw, DNW_SLOPE_WINDOW[0], DNW_SLOPE_WINDOW[1]
    )
    slope_r = slope_ratio(dnw_slope, sde_dnw_slope)

    b_at_sde_cross = interp(x, b, SDE_CROSS_UM)
    p_at_sde_cross = interp(x, p, SDE_CROSS_UM)

    sde_b_at_cross = float(
        gaussian(
            np.asarray([SDE_CROSS_UM]),
            SDE_PW_PEAK, SDE_PW_RP_UM, SDE_PW_SIGMA_UM
        )[0] + PW_BG
    )
    sde_p_at_cross = float(
        gaussian(
            np.asarray([SDE_CROSS_UM]),
            SDE_DNW_PEAK, SDE_DNW_RP_UM, SDE_DNW_SIGMA_UM
        )[0]
    )

    p462_r = (
        p_at_sde_cross / sde_p_at_cross
        if np.isfinite(p_at_sde_cross) and sde_p_at_cross > 0.0
        else np.nan
    )
    b462_r = (
        b_at_sde_cross / sde_b_at_cross
        if np.isfinite(b_at_sde_cross) and sde_b_at_cross > 0.0
        else np.nan
    )
    pw_pk_r = (
        pw_peak / SDE_PW_PEAK
        if np.isfinite(pw_peak) and SDE_PW_PEAK > 0.0
        else np.nan
    )
    dnw_pk_r = (
        dnw_peak / SDE_DNW_PEAK
        if np.isfinite(dnw_peak) and SDE_DNW_PEAK > 0.0
        else np.nan
    )

    p_pw_rp = bounded_penalty(
        abs(pw_x * 1000.0 - SDE_PW_RP_UM * 1000.0) / PW_RP_SCALE_NM
    )
    p_pw_pk = bounded_penalty(log_ratio_error(pw_peak, SDE_PW_PEAK))
    p_pw_shape = bounded_penalty(pw_shape_err)

    p_dnw_rp = bounded_penalty(
        abs(dnw_x * 1000.0 - SDE_DNW_RP_UM * 1000.0) / DNW_RP_SCALE_NM
    )
    p_dnw_pk = bounded_penalty(log_ratio_error(dnw_peak, SDE_DNW_PEAK))
    p_dnw_sig = bounded_penalty(
        abs(dnw_sigma * 1000.0 - SDE_DNW_SIGMA_UM * 1000.0) /
        DNW_SIG_SCALE_NM
    )
    p_dnw_shape = bounded_penalty(dnw_shape_err)

    p_junc = (
        bounded_penalty(
            abs(cross * 1000.0 - SDE_CROSS_UM * 1000.0) / JUNC_SCALE_NM
        )
        if np.isfinite(cross)
        else 1.0
    )
    p_p462 = bounded_penalty(
        log_ratio_error(p_at_sde_cross, sde_p_at_cross)
    )
    p_slope = slope_penalty(dnw_slope, sde_dnw_slope)
    p_split = min(max(overall_split, 0.0), 1.0)

    score = 100.0 * (
        W_PW_RP * p_pw_rp +
        W_PW_PK * p_pw_pk +
        W_PW_SHAPE * p_pw_shape +
        W_DNW_RP * p_dnw_rp +
        W_DNW_PK * p_dnw_pk +
        W_DNW_SIG * p_dnw_sig +
        W_DNW_SHAPE * p_dnw_shape +
        W_JUNC * p_junc +
        W_P462 * p_p462 +
        W_SLOPE * p_slope +
        W_SPLIT * p_split
    )

    out = {
        # Short DOE summary values
        "SCORE": score,
        "PW_RP": pw_x * 1000.0,
        "PW_PK_R": pw_pk_r,
        "DNW_RP": dnw_x * 1000.0,
        "DNW_PK_R": dnw_pk_r,
        "DNW_SIG": dnw_sigma * 1000.0,
        "JUNC": cross * 1000.0,
        "P462_R": p462_r,
        "SLOPE_R": slope_r,
        "SPLIT": overall_split,

        # Detailed PW values
        "PW_peak_depth_nm": pw_x * 1000.0,
        "PW_peak_cm3": pw_peak,
        "PW_global_peak_depth_nm": pw_global_x * 1000.0,
        "PW_global_peak_cm3": pw_global_peak,
        "PW_peak_ratio": pw_pk_r,
        "PW_halfmax_left_nm": pw_l * 1000.0,
        "PW_halfmax_right_nm": pw_r * 1000.0,
        "PW_FWHM_nm": pw_w * 1000.0,
        "PW_FWHM_truncated": pw_trunc,
        "PW_integrated_active_dose_cm2": pw_dose,
        "PW_log_profile_RMSE": pw_log_err,
        "PW_shape_log_RMSE": pw_shape_err,
        "PW_split_second_depth_nm": pw_split["second_depth"] * 1000.0,
        "PW_split_second_cm3": pw_split["second_value"],
        "PW_split_second_ratio": pw_split["second_ratio"],
        "PW_split_valley_depth_nm": pw_split["valley_depth"] * 1000.0,
        "PW_split_valley_cm3": pw_split["valley_value"],
        "PW_split_valley_ratio": pw_split["valley_ratio"],
        "PW_split_severity": pw_split["severity"],

        # Detailed DNW values
        "DNW_peak_depth_nm": dnw_x * 1000.0,
        "DNW_peak_cm3": dnw_peak,
        "DNW_peak_ratio": dnw_pk_r,
        "DNW_halfmax_left_nm": dnw_l * 1000.0,
        "DNW_halfmax_right_nm": dnw_r * 1000.0,
        "DNW_FWHM_nm": dnw_w * 1000.0,
        "DNW_FWHM_truncated": dnw_trunc,
        "DNW_sigma_equiv_nm": dnw_sigma * 1000.0,
        "DNW_integrated_active_dose_cm2": dnw_dose,
        "DNW_log_profile_RMSE": dnw_log_err,
        "DNW_shape_log_RMSE": dnw_shape_err,
        "DNW_split_second_depth_nm": dnw_split["second_depth"] * 1000.0,
        "DNW_split_second_cm3": dnw_split["second_value"],
        "DNW_split_second_ratio": dnw_split["second_ratio"],
        "DNW_split_valley_depth_nm": dnw_split["valley_depth"] * 1000.0,
        "DNW_split_valley_cm3": dnw_split["valley_value"],
        "DNW_split_valley_ratio": dnw_split["valley_ratio"],
        "DNW_split_severity": dnw_split["severity"],

        # Junction/tail values
        "SDE_target_crossing_nm": SDE_CROSS_UM * 1000.0,
        "PW_DNW_crossing_nm": cross * 1000.0,
        "PW_DNW_crossing_error_nm": (cross - SDE_CROSS_UM) * 1000.0,
        "PW_at_SDE_crossing_cm3": b_at_sde_cross,
        "DNW_at_SDE_crossing_cm3": p_at_sde_cross,
        "SDE_PW_at_crossing_cm3": sde_b_at_cross,
        "SDE_DNW_at_crossing_cm3": sde_p_at_cross,
        "PW_at_SDE_crossing_ratio": b462_r,
        "DNW_at_SDE_crossing_ratio": p462_r,
        "DNW_junction_side_log_slope": dnw_slope,
        "SDE_DNW_junction_side_log_slope": sde_dnw_slope,
        "DNW_junction_side_slope_ratio": slope_r,

        # SCORE components
        "SCORE_P_PW_RP": p_pw_rp,
        "SCORE_P_PW_PK": p_pw_pk,
        "SCORE_P_PW_SHAPE": p_pw_shape,
        "SCORE_P_DNW_RP": p_dnw_rp,
        "SCORE_P_DNW_PK": p_dnw_pk,
        "SCORE_P_DNW_SIG": p_dnw_sig,
        "SCORE_P_DNW_SHAPE": p_dnw_shape,
        "SCORE_P_JUNC": p_junc,
        "SCORE_P_P462": p_p462,
        "SCORE_P_SLOPE": p_slope,
        "SCORE_P_SPLIT": p_split,
    }

    for nm in PW_SAMPLE_NM:
        out[f"PW_C{nm}_cm3"] = interp(x, b, nm / 1000.0)
    for nm in DNW_SAMPLE_NM:
        out[f"DNW_C{nm}_cm3"] = interp(x, p, nm / 1000.0)

    return out, sde_pw, sde_dnw


def write_compare_csv(filename, x, b, p, sde_pw, sde_dnw):
    m = np.isfinite(x) & (x >= 0.0) & (x <= PROFILE_MAX_UM)
    save_csv(
        filename,
        {
            "Depth_um": x[m],
            "Depth_nm": x[m] * 1000.0,
            "SProcess_BActive_cm3": b[m],
            "SProcess_PActive_cm3": p[m],
            "SDE_BActive_target_cm3": sde_pw[m],
            "SDE_PActive_target_cm3": sde_dnw[m],
        }
    )


def make_plot(csvfile, dataset, plotname, title):
    sv.load_file(csvfile, name=dataset)
    p = sv.create_plot(name=plotname, xy=True)
    sv.create_curve(
        name=f"{plotname}_SP_PW",
        plot=p, dataset=dataset,
        axisX="Depth_nm", axisY="SProcess_BActive_cm3"
    )
    sv.create_curve(
        name=f"{plotname}_SP_DNW",
        plot=p, dataset=dataset,
        axisX="Depth_nm", axisY="SProcess_PActive_cm3"
    )
    sv.create_curve(
        name=f"{plotname}_SDE_PW",
        plot=p, dataset=dataset,
        axisX="Depth_nm", axisY="SDE_BActive_target_cm3"
    )
    sv.create_curve(
        name=f"{plotname}_SDE_DNW",
        plot=p, dataset=dataset,
        axisX="Depth_nm", axisY="SDE_PActive_target_cm3"
    )
    sv.set_plot_prop(
        plot=p, show_grid=True, show_legend=True, title=title
    )
    sv.set_axis_prop(
        plot=p, axis="x", title="Depth from bulk-Si surface [nm]"
    )
    sv.set_axis_prop(
        plot=p, axis="y", title="Active concentration [cm^-3]", type="log"
    )
    return p


ar = load_plx(AR_FILE, "AR_PLX")
fr = load_plx(F_FILE, "F_PLX")

if ar is None:
    raise RuntimeError(f"Required post-RTA PLX not found: {AR_FILE}")

x_ar, b_ar, p_ar = ar
m_ar, sde_pw_ar, sde_dnw_ar = analyze_profile(x_ar, b_ar, p_ar)
write_compare_csv(AR_CSV, x_ar, b_ar, p_ar, sde_pw_ar, sde_dnw_ar)

try:
    make_plot(
        AR_CSV, "AR_COMPARE", "Plot_AR_ProfileCompare",
        "SProcess post-RTA vs SDE baseline - r=4.6875 um"
    )
except Exception as exc:
    print(f"PROFILE: AR plot warning: {exc}")

m_f = None
if fr is not None:
    x_f, b_f, p_f = fr
    m_f, sde_pw_f, sde_dnw_f = analyze_profile(x_f, b_f, p_f)
    write_compare_csv(F_CSV, x_f, b_f, p_f, sde_pw_f, sde_dnw_f)
    try:
        make_plot(
            F_CSV, "F_COMPARE", "Plot_F_ProfileCompare",
            "SProcess final vs SDE baseline - r=4.6875 um"
        )
    except Exception as exc:
        print(f"PROFILE: F plot warning: {exc}")

with open(METRICS_FILE, "w") as fh:
    fh.write(f"source_postRTA = {AR_FILE}\n")
    fh.write(f"source_final = {F_FILE if fr is not None else 'NA'}\n")
    fh.write("SCORE_basis = POST_RTA_AR_profile\n")
    fh.write("SCORE_interpretation = lower_is_better_not_percent_error\n")
    fh.write(f"SDE_PW_peak_depth_nm = {SDE_PW_RP_UM*1000.0:.12g}\n")
    fh.write(f"SDE_PW_peak_cm3 = {SDE_PW_PEAK:.12g}\n")
    fh.write(f"SDE_DNW_peak_depth_nm = {SDE_DNW_RP_UM*1000.0:.12g}\n")
    fh.write(f"SDE_DNW_peak_cm3 = {SDE_DNW_PEAK:.12g}\n")
    fh.write(f"SDE_DNW_sigma_nm = {SDE_DNW_SIGMA_UM*1000.0:.12g}\n")
    fh.write(f"SDE_crossing_nm = {SDE_CROSS_UM*1000.0:.12g}\n")

    fh.write("\n[POST_RTA_DETAIL]\n")
    for key in sorted(m_ar.keys()):
        write_metric(fh, f"AR_{key}", m_ar[key])

    if m_f is not None:
        fh.write("\n[FINAL_DETAIL]\n")
        for key in sorted(m_f.keys()):
            write_metric(fh, f"F_{key}", m_f[key])

    # Only these ten values are exposed to the SWB DOE table.
    fh.write("\n[DOE_SUMMARY]\n")
    for key in [
        "SCORE",
        "PW_RP",
        "PW_PK_R",
        "DNW_RP",
        "DNW_PK_R",
        "DNW_SIG",
        "JUNC",
        "P462_R",
        "SLOPE_R",
        "SPLIT",
    ]:
        emit(fh, key, m_ar.get(key, np.nan))

try:
    sv.windows_style(style="grid")
except Exception:
    pass

print("PROFILE_SCREENING_DUAL_DNW_SCORE: COMPLETE")
