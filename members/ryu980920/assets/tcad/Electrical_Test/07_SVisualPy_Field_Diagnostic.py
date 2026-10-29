#setdep @node|sdevice@
# CMP SPAD | independent 15.0 V SDE-vs-SProcess field diagnostic, v1.0
# Pure diagnostic: leaves 06_SVisualPy_VBD_SCR.py and SDevice Physics unchanged.
# Intended SWB node: a NEW SVisualPy after the same SDevice as node 06.
# Required SDE source: a copy named SDE_baseline_V150_des.tdr in this run
# directory; or absolute filename in environment CMP_SPAD_SDE_V150_TDR.
# Workbench registered process parameters are NEVER changed here.

import csv
import fnmatch
import os
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np

VIS_NODE = @node@
DEVICE_NODE = @node|sdevice@
PROC_TDR = f"n{DEVICE_NODE}_V150_des.tdr"
SDE_TDR = os.environ.get("CMP_SPAD_SDE_V150_TDR", "SDE_baseline_V150_des.tdr")
PREFIX = f"n{VIS_NODE}_field15"

# Published static-freeze reference coordinate definitions (um).
# Raw Y is NOT directly comparable between SProcess and SDE.
INTERFACE_PROC_Y_UM = 0.300
INTERFACE_SDE_Y_UM = 0.000
BIAS_V = 15.0
RADII_UM = [4.6875, 12.5, 16.0, 17.0, 18.0]
DEPTH_MIN_UM = 0.0
DEPTH_MAX_UM = 1.30
DEPTH_STEP_UM = 0.005
# Do not interpolate across large gaps where cutline crosses oxide/STI.
MAX_BRACKET_GAP_UM = 0.12


def choose_variable(dataset, patterns):
    variables = list(sv.list_variables(dataset=dataset))
    for pattern in patterns:
        for name in variables:
            if fnmatch.fnmatch(name.lower(), pattern.lower()):
                return name
    return None


def data(dataset, name):
    return np.asarray(sv.get_variable_data(varname=name, dataset=dataset), dtype=float).ravel()


def field_magnitude(dataset):
    # Same scalar preferences as the static-freeze SVisualPy script.
    scalar = choose_variable(dataset, ["AbsElectricField", "Abs(ElectricField-V)", "ElectricField"])
    if scalar is not None:
        values = data(dataset, scalar)
        if values.ndim == 1:
            return np.abs(values)
    ex = choose_variable(dataset, ["ElectricField-X", "ElectricField/x", "*ElectricField*X*"])
    ey = choose_variable(dataset, ["ElectricField-Y", "ElectricField/y", "*ElectricField*Y*"])
    if ex is None or ey is None:
        raise RuntimeError("Neither scalar |E| nor both E-field vector components exist in " + str(dataset))
    return np.hypot(data(dataset, ex), data(dataset, ey))


def silicon_cut(source, label, radius, interface_y):
    cname = "Cut_%s_r%s" % (label, str(radius).replace(".", "p"))
    try:
        cut = sv.create_cutline("x", at=radius, dataset=source, materials=["Silicon"], name=cname)
    except TypeError:
        # Older SVisualPy argument conventions: same fallback as baseline.
        cut = sv.create_cutline("x", at=radius, dataset=source, name=cname)

    yname = choose_variable(cut, ["Y", "y"])
    if yname is None:
        raise RuntimeError("Missing Y coordinate on " + cname)
    y = data(cut, yname)
    e = field_magnitude(cut)
    avar = choose_variable(cut, ["AvalancheGeneration", "*AvalancheGeneration*", "ImpactIonization", "*ImpactIonization*"])
    aval = data(cut, avar) if avar else np.full(y.size, np.nan)

    if not (len(y) == len(e) == len(aval)):
        raise RuntimeError("Cutline arrays have inconsistent lengths: " + cname)
    z = y - interface_y
    valid = np.isfinite(z) & np.isfinite(e)
    z, e, aval = z[valid], e[valid], aval[valid]
    order = np.argsort(z, kind="mergesort")
    z, e, aval = z[order], e[order], aval[order]
    # Merge repeated mesh coordinates; missing Avalanche remains NaN.
    if z.size:
        unique_z, inverse = np.unique(z, return_inverse=True)
        ne = np.bincount(inverse, weights=e)
        count = np.bincount(inverse)
        have_av = np.isfinite(aval)
        na = np.bincount(inverse[have_av], weights=aval[have_av], minlength=len(unique_z))
        ca = np.bincount(inverse[have_av], minlength=len(unique_z))
        avg_av = np.full(len(unique_z), np.nan)
        np.divide(na, ca, out=avg_av, where=ca > 0)
        z, e, aval = unique_z, ne / count, avg_av
    return {"z": z, "e": e, "aval": aval, "has_avalanche": avar is not None,
            "avalanche_name": avar or "MISSING"}


def interpolate_without_large_gaps(x, y, grid):
    good = np.isfinite(x) & np.isfinite(y)
    x = x[good]
    y = y[good]
    result = np.full(grid.shape, np.nan)
    if x.size < 2:
        return result
    indices = np.searchsorted(x, grid, side="left")
    # Exact coordinate hits are valid even at the boundary.
    exact = (indices < len(x)) & (x[np.minimum(indices, len(x)-1)] == grid)
    result[exact] = y[indices[exact]]
    indices = np.searchsorted(x, grid, side="right")
    left, right = indices-1, indices
    inside = (left >= 0) & (right < len(x))
    safe_l = np.clip(left, 0, len(x)-1)
    safe_r = np.clip(right, 0, len(x)-1)
    gap = x[safe_r] - x[safe_l]
    usable = inside & (gap > 0) & (gap <= MAX_BRACKET_GAP_UM)
    result[usable] = y[safe_l[usable]] + (
        (grid[usable]-x[safe_l[usable]]) / gap[usable]
    ) * (y[safe_r[usable]]-y[safe_l[usable]])
    return result


def write_csv(path, columns):
    keys = list(columns)
    lengths = {len(np.atleast_1d(v)) for v in columns.values()}
    if len(lengths) != 1:
        raise RuntimeError("CSV array-length mismatch: " + str(path))
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(keys)
        for values in zip(*(columns[k] for k in keys)):
            writer.writerow([float(x) if np.isfinite(x) else "" for x in values])


def valid_peak(grid, arr):
    ok = np.isfinite(arr)
    if not np.any(ok):
        return float("nan"), float("nan")
    idx = np.where(ok)[0][np.argmax(arr[ok])]
    return float(arr[idx]), float(grid[idx])


def svg_plot(path, title, xlabel, ylabel, x, series):
    # Zero dependency plotting. Each curve is clipped at missing/NaN data gaps.
    W, H, l, r, top, bottom = 900, 520, 88, 25, 57, 70
    series = [(name, color, np.asarray(y, dtype=float)) for name, color, y in series]
    all_y = np.concatenate([y[np.isfinite(y)] for _, _, y in series])
    if not len(all_y):
        return False
    ymin = float(min(0.0, np.min(all_y)))
    ymax = float(np.max(all_y))
    if ymax <= ymin:
        ymax = ymin + 1.0
    ymax += (ymax - ymin) * 0.06
    xlo, xhi = float(np.min(x)), float(np.max(x))
    px = lambda v: l + (v-xlo)/(xhi-xlo)*(W-l-r)
    py = lambda v: top + (ymax-v)/(ymax-ymin)*(H-top-bottom)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<text x="{W/2}" y="27" font-family="Arial" font-size="19" text-anchor="middle">{escape(title)}</text>',
             f'<line x1="{l}" y1="{H-bottom}" x2="{W-r}" y2="{H-bottom}" stroke="#333"/>',
             f'<line x1="{l}" y1="{top}" x2="{l}" y2="{H-bottom}" stroke="#333"/>']
    for k in range(6):
        yval = ymin+(ymax-ymin)*k/5
        yp = py(yval)
        parts.append(f'<line x1="{l}" y1="{yp:.2f}" x2="{W-r}" y2="{yp:.2f}" stroke="#ececec"/>')
        parts.append(f'<text x="{l-8}" y="{yp+4:.2f}" font-family="Arial" font-size="11" text-anchor="end">{yval:.3g}</text>')
        xv = xlo+(xhi-xlo)*k/5
        parts.append(f'<text x="{px(xv):.1f}" y="{H-bottom+23}" font-family="Arial" font-size="12" text-anchor="middle">{xv:.0f}</text>')
    parts += [f'<text x="{W/2}" y="{H-14}" font-family="Arial" font-size="13" text-anchor="middle">{escape(xlabel)}</text>',
              f'<text x="18" y="{H/2}" font-family="Arial" font-size="13" transform="rotate(-90 18 {H/2})" text-anchor="middle">{escape(ylabel)}</text>']
    for i, (name, color, y) in enumerate(series):
        # Separate paths for disconnected Silicon cutline segments.
        run=[]
        def flush_run():
            if len(run)>1:
                parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.3" points="{" ".join(run)}"/>')
        for xx, yy in zip(x, y):
            if np.isfinite(yy):
                run.append(f"{px(xx):.2f},{py(yy):.2f}")
            else:
                flush_run(); run=[]
        flush_run()
        ax = l + i*240
        parts.append(f'<line x1="{ax}" y1="42" x2="{ax+25}" y2="42" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<text x="{ax+31}" y="46" font-family="Arial" font-size="12">{escape(name)}</text>')
    parts.append('</svg>')
    Path(path).write_text("\n".join(parts), encoding="utf-8")
    return True


def try_global_silicon_max(dataset):
    """Try documented 2D field maximum; do not substitute an XY max as global."""
    field = choose_variable(dataset, ["AbsElectricField", "Abs(ElectricField-V)"])
    function = getattr(sv, "calculate_field_value", None)
    if field is None or not callable(function):
        return None, "2D scalar |E| or calculate_field_value not exposed"
    # The Python wrapper signature differs among SVisual releases.
    variants = [
        {"max": True, "dataset": dataset, "field": field, "materials": ["Silicon"]},
        {"maximum": True, "dataset": dataset, "field": field, "materials": ["Silicon"]},
        {"max": True, "plot": "Plot_"+dataset, "field": field, "materials": ["Silicon"]},
    ]
    problems=[]
    for kwargs in variants:
        try:
            result = function(**kwargs)
            if isinstance(result, (tuple, list)) and len(result) >= 2:
                value = float(result[0]); coords = np.asarray(result[1], dtype=float).ravel()
                if np.isfinite(value) and len(coords) >= 2:
                    return (value, float(coords[0]), float(coords[1])), "native 2D Silicon max"
            problems.append("unrecognized return: " + repr(result)[:160])
        except Exception as exc:
            problems.append(type(exc).__name__+": "+str(exc)[:150])
    return None, "; ".join(problems)


def prepare_dataset(filename, name):
    if not os.path.isfile(filename):
        raise RuntimeError("Required 15.0 V TDR missing: " + filename)
    sv.load_file(filename, name=name)
    sv.create_plot(name="Plot_"+name, dataset=name)


prepare_dataset(PROC_TDR, "PROC15")
prepare_dataset(SDE_TDR, "SDE15")

zgrid = np.linspace(DEPTH_MIN_UM, DEPTH_MAX_UM,
                    int(round((DEPTH_MAX_UM-DEPTH_MIN_UM)/DEPTH_STEP_UM))+1)
z_nm = zgrid*1000.0
summary = []
files_generated=[]

for radius in RADII_UM:
    label = str(radius).replace(".", "p")
    proc = silicon_cut("PROC15", "PROC", radius, INTERFACE_PROC_Y_UM)
    sde = silicon_cut("SDE15", "SDE", radius, INTERFACE_SDE_Y_UM)
    pe = interpolate_without_large_gaps(proc["z"], proc["e"], zgrid)
    se = interpolate_without_large_gaps(sde["z"], sde["e"], zgrid)
    pa = interpolate_without_large_gaps(proc["z"], proc["aval"], zgrid)
    sa = interpolate_without_large_gaps(sde["z"], sde["aval"], zgrid)
    both_e = np.isfinite(pe) & np.isfinite(se)
    both_av = np.isfinite(pa) & np.isfinite(sa)
    de = np.where(both_e, pe-se, np.nan)
    da = np.where(both_av, pa-sa, np.nan)

    outcsv = f"{PREFIX}_r{label}_compare.csv"
    write_csv(outcsv, {
        "z_from_grating_Si_interface_nm": z_nm,
        "SProcess_E_V_per_cm": pe, "SDE_E_V_per_cm": se,
        "SProcess_minus_SDE_E_V_per_cm": de,
        "SProcess_Avalanche_cm_3_s_1": pa, "SDE_Avalanche_cm_3_s_1": sa,
        "SProcess_minus_SDE_Avalanche_cm_3_s_1": da,
    })
    files_generated.append(outcsv)
    outsvg = f"{PREFIX}_r{label}_E.svg"
    if svg_plot(outsvg, f"|E| at 15.0 V, r = {radius:g} um", "Depth from common interface (nm)",
                "|E| (kV/cm)", z_nm,
                [("SProcess", "#2676d1", pe/1000.0), ("SDE", "#d46c18", se/1000.0)]):
        files_generated.append(outsvg)
    if np.any(np.isfinite(pa)) or np.any(np.isfinite(sa)):
        # Same signed log1p transform on each dataset; use only nonnegative
        # generation (negative numerical noise is clamped to 0).
        outsvg = f"{PREFIX}_r{label}_Avalanche.svg"
        ap = np.where(np.isfinite(pa), np.log10(1+np.maximum(pa, 0)), np.nan)
        a0 = np.where(np.isfinite(sa), np.log10(1+np.maximum(sa, 0)), np.nan)
        if svg_plot(outsvg, f"AvalancheGeneration at 15.0 V, r = {radius:g} um",
                    "Depth from common interface (nm)", "log10(1 + Generation [cm^-3 s^-1])", z_nm,
                    [("SProcess", "#2676d1", ap), ("SDE", "#d46c18", a0)]):
            files_generated.append(outsvg)
    pmax, pz = valid_peak(zgrid, pe)
    smax, sz = valid_peak(zgrid, se)
    pamax, paz = valid_peak(zgrid, pa)
    samax, saz = valid_peak(zgrid, sa)
    summary.append([radius, pmax, pz*1000, smax, sz*1000,
                    pmax-smax, pamax, paz*1000, samax, saz*1000,
                    int(both_e.sum()), int(both_av.sum())])

summary_csv = PREFIX+"_peak_summary.csv"
with open(summary_csv, "w", newline="") as file:
    writer=csv.writer(file)
    writer.writerow(["r_um", "SProcess_cut_Emax_V_per_cm", "SProcess_cut_Emax_z_nm",
                     "SDE_cut_Emax_V_per_cm", "SDE_cut_Emax_z_nm", "Delta_cut_Emax_V_per_cm",
                     "SProcess_cut_Aval_max", "SProcess_cut_Aval_max_z_nm",
                     "SDE_cut_Aval_max", "SDE_cut_Aval_max_z_nm",
                     "overlap_E_points", "overlap_Aval_points"])
    writer.writerows(summary)
files_generated.append(summary_csv)

# Try native 2D (entire Silicon) maximum; if Python API does not provide it,
# do NOT mislabel a sample of five cutlines as an exact device-wide maximum.
global_proc, global_msg_proc = try_global_silicon_max("PROC15")
global_sde, global_msg_sde = try_global_silicon_max("SDE15")
logfile = PREFIX+"_audit.txt"
with open(logfile, "w") as file:
    file.write(f"SDevice_node={DEVICE_NODE}\n")
    file.write(f"SProcess_TDR={PROC_TDR}\nSDE_TDR={SDE_TDR}\n")
    file.write(f"evaluation_bias_V={BIAS_V}\n")
    file.write(f"SProcess_interface_raw_y_um={INTERFACE_PROC_Y_UM}\n")
    file.write(f"SDE_interface_raw_y_um={INTERFACE_SDE_Y_UM}\n")
    file.write("comparison_method=aligned radial Silicon cutlines at fixed 15.0 V\n")
    file.write(f"radial_cuts_um={RADII_UM}\n")
    file.write(f"depth_window_um={DEPTH_MIN_UM}..{DEPTH_MAX_UM}\n")
    file.write(f"interpolation_grid_um={DEPTH_STEP_UM}\n")
    file.write(f"interpolation_max_gap_um={MAX_BRACKET_GAP_UM}\n")
    for label, val, msg, raw_origin in [
        ("SProcess", global_proc, global_msg_proc, INTERFACE_PROC_Y_UM),
        ("SDE", global_sde, global_msg_sde, INTERFACE_SDE_Y_UM),
    ]:
        if val is None:
            file.write(f"{label}_fullSilicon_Emax=UNAVAILABLE\n{label}_fullSilicon_note={msg}\n")
        else:
            vmax, x, y = val
            file.write(f"{label}_fullSilicon_Emax_V_per_cm={vmax}\n")
            file.write(f"{label}_fullSilicon_max_x_um={x}\n")
            file.write(f"{label}_fullSilicon_max_z_if_um={y-raw_origin}\n")
            file.write(f"{label}_fullSilicon_note={msg}\n")
    file.write("No SWB DOE output: VBD/SCR baseline evaluation is unchanged.\n")
    file.write("NOTE: Cutline peaks are sampled/interpolated; they are not full-device maxima.\n")
    file.write("AvalancheGeneration peak magnitude at fixed bias is NOT proof of breakdown onset.\n")
    file.write("NOTE: Full Silicon Emax uses native 2D API only if exposed; otherwise NA.\n")
    file.write("files_generated="+",".join(files_generated)+"\n")

print("FIELD_DIAG: COMPLETE")
print("FIELD_DIAG: peak summary " + summary_csv)
print("FIELD_DIAG: audit " + logfile)
