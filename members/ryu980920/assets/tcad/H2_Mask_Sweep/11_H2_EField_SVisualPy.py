#setdep @node|-4@
# H2 field/avalanche diagnostics, to run as the 11th Workbench node.
# Parent SDevice2 is node -4 (node 7). Uses @Mask@ in every DOE row.
# Sampling from Silicon-only cuts. Quantitative results require Sentaurus execution.
# IMPORTANT: SCR/PEB cutline names include the snapshot tag to prevent collisions.
# All sampled radial cutlines must succeed; never silently report partial maxima.
import fnmatch
import os
import numpy as np

VIS_NODE = @node@
SDEVICE2_NODE = @node|-4@
MASK_END_UM = float(@Mask@)
VBD = float(@VBD_V@)
PEB_BIAS = float(@PEB_BIAS_V@)
SCR_BIAS = float(@SCR_BIAS_V@)
CENTER_R_UM = 4.6875
STI5_LO, STI5_HI = 12.20, 12.80
MASK_HALF_WIDTH_UM = 0.25
PERIPH_LO, PERIPH_HI = 11.60, 16.65
Y_LO, Y_HI = 0.0, 1.60   # raw device Y depth in um, not z_if
if not (np.isfinite(VBD) and 0.0 < SCR_BIAS < PEB_BIAS < VBD):
    raise RuntimeError('H2 bias order invalid: SCR < PEB < VBD required')


def pickvar(ds, patterns):
    names = list(sv.list_variables(dataset=ds))
    for p in patterns:
        for name in names:
            if fnmatch.fnmatch(name.lower(), p.lower()):
                return name
    return None


def values(ds, name):
    return np.asarray(sv.get_variable_data(varname=name, dataset=ds), dtype=float)


def field_abs(ds):
    scalar = pickvar(ds, ['AbsElectricField', 'Abs(ElectricField-V)', 'ElectricField'])
    if scalar is not None:
        a = values(ds, scalar)
        if a.ndim == 1:
            return np.abs(a)
    ex = pickvar(ds, ['ElectricField-X', 'ElectricField/x', '*ElectricField*X*'])
    ey = pickvar(ds, ['ElectricField-Y', 'ElectricField/y', '*ElectricField*Y*'])
    if ex is None or ey is None:
        raise RuntimeError('ElectricField components not found in cutline dataset')
    return np.hypot(values(ds, ex), values(ds, ey))


def create_silicon_cut(ds, plot, r, i, tag):
    # Keep the material constraint. Falling back to an oxide-inclusive cut
    # would bias the STI5 comparison and must not be silently accepted.
    try:
        return sv.create_cutline('x', at=float(r), dataset=ds,
                                 materials=['Silicon'], name=f'H2_{tag}_{i:03d}')
    except TypeError:
        try:
            return sv.create_cutline('x', at=float(r), plot=plot,
                                     materials=['Silicon'], name=f'H2_{tag}_{i:03d}')
        except TypeError as exc:
            raise RuntimeError('SVisualPy build lacks material-filtered cutline API') from exc


def sample_radii():
    # General PEB region 50-nm grid, STI5/Mask-edge windows at 25 nm.
    rr = [CENTER_R_UM]
    rr.extend(np.arange(PERIPH_LO, PERIPH_HI + 0.001, 0.05))
    rr.extend(np.arange(12.10, 12.90 + 0.001, 0.025))
    rr.extend(np.arange(MASK_END_UM - MASK_HALF_WIDTH_UM,
                        MASK_END_UM + MASK_HALF_WIDTH_UM + 0.001, 0.025))
    rr = [x for x in rr if 0 <= x <= 24]
    return np.unique(np.round(rr, 6))


def summarize(data, lo_r, hi_r, quantity, center_only=False):
    r, y, ef, av = data.T
    m = ((r >= lo_r - 1e-7) & (r <= hi_r + 1e-7)
         & (y >= Y_LO - 1e-9) & (y <= Y_HI + 1e-9))
    if center_only:
        # Keep central SCR physics consistent with prior r=4.6875 analysis.
        m &= (y >= 0.30)
    a = ef if quantity == 'E' else av
    m &= np.isfinite(a)
    if not np.any(m):
        return (np.nan, np.nan, np.nan)
    ids = np.where(m)[0]
    k = ids[np.argmax(a[ids])]
    return (float(a[k]), float(r[k]), float(y[k]))


def format_num(x):
    return 'NA' if not np.isfinite(x) else f'{x:.12g}'


def emit(name, value):
    print(f'DOE: {name} {format_num(value) if np.isfinite(value) else "x"}')


def analyze(tag, name):
    file = f'n{SDEVICE2_NODE}_{name}_des.tdr'
    if not os.path.isfile(file):
        raise RuntimeError(f'H2 required device snapshot missing: {file}')
    ds = 'H2STATE_' + tag
    sv.load_file(file, name=ds)
    plot = sv.create_plot(name='H2PLOT_' + tag, dataset=ds)
    samples = []
    errors = []
    radii = sample_radii()
    for i, radius in enumerate(radii):
        try:
            cd = create_silicon_cut(ds, plot, radius, i, tag)
            yn = pickvar(cd, ['Y', 'y'])
            an = pickvar(cd, ['AvalancheGeneration', '*AvalancheGeneration*'])
            if yn is None or an is None:
                raise RuntimeError('Y or AvalancheGeneration not in cut dataset')
            y = values(cd, yn)
            e = field_abs(cd)
            av = values(cd, an)
            if not (len(y) == len(e) == len(av)):
                raise RuntimeError('Cutline variable length mismatch')
            keep = (np.isfinite(y) & np.isfinite(e) & np.isfinite(av)
                    & (y >= Y_LO - 1e-9) & (y <= Y_HI + 1e-9))
            if not np.any(keep):
                raise RuntimeError("No finite Silicon samples within the H2 depth window")
            for yy, ee, aa in zip(y[keep], e[keep], av[keep]):
                samples.append((float(radius), float(yy), float(ee), max(float(aa),0.0)))
        except Exception as exc:
            errors.append(f'r={radius:.6f}: {exc}')
    # A missing cut is not an acceptable approximation of the maximum field.
    # Fail rather than silently ranking a case from an incomplete field map.
    if errors:
        raise RuntimeError('H2 '+tag+' cutline extraction incomplete ('+str(len(errors))+'/'+str(len(radii))+'): '+ '; '.join(errors[:4]))
    if not samples:
        raise RuntimeError('No silicon cutlines sampled')
    data = np.asarray(samples,dtype=float)
    if not np.any((data[:,0]>=CENTER_R_UM-1e-7)&(data[:,0]<=CENTER_R_UM+1e-7)):
        raise RuntimeError('H2 center reference cut missing')
    np.savetxt(f'n{VIS_NODE}_H2_{tag}_samples.csv', data, delimiter=',',
               header='Radius_um,RawDepth_um,AbsElectricField_Vcm,AvalancheGeneration_cm3s',
               comments='',fmt='%.12e')
    regions = {
        'Center': (CENTER_R_UM-1e-6, CENTER_R_UM+1e-6, True),
        'STI5': (12.10, 12.90, False),
        'Mask': (MASK_END_UM-MASK_HALF_WIDTH_UM,
                 MASK_END_UM+MASK_HALF_WIDTH_UM, False),
        'Peripheral': (PERIPH_LO,PERIPH_HI,False),
    }
    out={}
    for region,(lo,hi,center) in regions.items():
        ev,er,ey = summarize(data,lo,hi,'E',center)
        av,ar,ay = summarize(data,lo,hi,'Aval',center)
        if not np.all(np.isfinite([ev, er, ey, av, ar, ay])):
            raise RuntimeError(f'H2 {tag} has no complete silicon E/Avalanche samples for {region}')
        out[f'E_{region}_kVcm'] = ev/1e3
        out[f'E_{region}_r_um'] = er
        out[f'E_{region}_rawY_um'] = ey
        out[f'Aval_{region}_cm3s'] = av
        out[f'Aval_{region}_r_um'] = ar
        out[f'Aval_{region}_rawY_um'] = ay
    c=out['E_Center_kVcm']
    out['E_Mask_over_Center']=(out['E_Mask_kVcm']/c if c > 0 else np.nan)
    out['E_STI5_over_Center']=(out['E_STI5_kVcm']/c if c > 0 else np.nan)
    out['E_Peripheral_over_Center']=(out['E_Peripheral_kVcm']/c if c > 0 else np.nan)
    # This is a location-comparison signal, not a certified PEB prediction.
    out['PeripheralAvalancheDominant'] = float(
        out['Aval_Peripheral_cm3s'] > out['Aval_Center_cm3s']
        and out['Aval_Peripheral_cm3s'] > 0
    )
    out['H2_valid_cuts'] = len(radii)-len(errors)
    out['H2_error_cuts'] = len(errors)
    with open(f'n{VIS_NODE}_H2_{tag}_metrics.txt','w') as f:
        f.write(f'Mask_um={MASK_END_UM:.12g}\nVBD_V={VBD:.12g}\n')
        f.write(f'SourceTDR={file}\n')
        f.write(f'Evaluation={tag}\n')
        f.write('Warning=PEB_RISK_SIGNAL_NOT_A_PROVEN_PEB_ONSET\n')
        f.write('Warning=STI5_and_Mask_windows_can_overlap\n')
        for key,value in out.items():
            f.write(f'{key}={format_num(value)}\n')
        for error in errors:
            f.write(f'CutError={error}\n')
    return out

# Same-relative-bias comparison at SCR and 99.9% VBD.
scr=analyze('SCR','SCR')
peb=analyze('PEB','PEB')
for key,value in peb.items():
    if key.startswith(('E_', 'Aval_')) or key in ['PeripheralAvalancheDominant','H2_error_cuts']:
        emit('H2_'+key,value)
emit('H2_E_Center_SCR_kVcm',scr['E_Center_kVcm'])
emit('H2_E_Mask_SCR_kVcm',scr['E_Mask_kVcm'])
emit('H2_E_STI5_SCR_kVcm',scr['E_STI5_kVcm'])
print('H2_FIELD_ANALYSIS: complete; classify PEB risk after P0 comparison and spatial visual review')
