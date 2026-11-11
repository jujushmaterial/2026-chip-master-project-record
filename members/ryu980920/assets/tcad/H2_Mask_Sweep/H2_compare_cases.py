#!/usr/bin/env python3
"""H2 six-case comparison with EXACTLY 14 user-selected output columns.

Usage: python H2_compare_cases.py H2_manifest_template.csv -o H2_results.csv
Only structural/spatial review can assign CathodeConnectivity and PEBRisk.
A blank status yields REVIEW_REQUIRED; numerical metrics never auto-prove PEB.
"""
import argparse
import csv
import math
from pathlib import Path
import numpy as np

AREA_UM2 = math.pi * 12.5**2  # Preserves the current project normalization
EXPECTED_MASKS = (16.3, 14.0, 13.0, 12.5, 12.2, 12.0)
OUTPUT_COLUMNS = (
    'Mask_um', 'VBD_V', 'INear_pAum2', 'Icommon_pAum2',
    'DarkReduction_Near_pct', 'DarkReduction_Common_pct',
    'Ecenter_kVcm', 'ESTI5_kVcm', 'EMask_kVcm', 'EMask_r_um',
    'AvalMask_cm3s', 'ForwardI_RelativeP0',
    'CathodeConnectivity', 'PEBRisk',
)
ALLOWED_CONNECTIVITY = {'REVIEW_REQUIRED', 'CONNECTED', 'DISCONNECTED', 'INCONCLUSIVE'}
ALLOWED_PEB = {'REVIEW_REQUIRED', 'ELEVATED', 'LOW', 'INCONCLUSIVE'}


def read_metrics(path):
    result = {}
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            result[key.strip()] = value.strip()
    return result


def required_number(metrics, key, case, positive=False):
    try:
        value = float(metrics[key])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f'Mask={case}: missing/non-numeric {key}') from exc
    if not math.isfinite(value) or (positive and value <= 0.0):
        raise ValueError(f'Mask={case}: invalid {key}={value}')
    return value


def abs_dark_at(path, voltage, case):
    with open(path, encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError(f'Mask={case}: empty dark I-V CSV')
    try:
        v = np.asarray([float(x['ReverseBias_V']) for x in rows])
        i = np.asarray([float(x['AbsAnodeCurrent_A']) for x in rows])
    except (KeyError, ValueError) as exc:
        raise ValueError(f'Mask={case}: invalid dark I-V columns') from exc
    finite = np.isfinite(v) & np.isfinite(i)
    v, i = v[finite], i[finite]
    if len(v) < 2 or np.any(i < 0):
        raise ValueError(f'Mask={case}: invalid dark I-V series')
    order = np.argsort(v, kind='mergesort')
    v, i = v[order], i[order]
    if not (v[0] <= voltage <= v[-1]):
        raise ValueError(f'Mask={case}: common V={voltage:.9g} outside dark I-V [{v[0]}, {v[-1]}]')
    value = float(np.interp(voltage, v, i)) / AREA_UM2 * 1.0e12
    if not math.isfinite(value):
        raise ValueError(f'Mask={case}: invalid interpolated dark current')
    return value


def review_field(record, key, allowed, case):
    status = record.get(key, '').strip().upper() or 'REVIEW_REQUIRED'
    if status not in allowed:
        raise ValueError(f'Mask={case}: unknown manual {key}={status!r}')
    return status


def reduction(value, baseline):
    return 100.0 * (1.0 - value / baseline)


def analyze(manifest, outpath):
    with open(manifest, encoding='utf-8-sig', newline='') as stream:
        cases = list(csv.DictReader(stream))
    if len(cases) != len(EXPECTED_MASKS):
        raise ValueError('Manifest must contain exactly six H2 rows')
    actual = [float(r['Mask']) for r in cases]
    if sorted(actual) != sorted(EXPECTED_MASKS):
        raise ValueError('Expected exactly one row for each of Mask=16.3,14,13,12.5,12.2,12.0')

    vbds = [required_number(r, 'VBD_V', r['Mask'], positive=True) for r in cases]
    common_voltage = 0.90 * min(vbds)  # Same voltage across all six devices.
    results = []
    for item in cases:
        case = float(item['Mask'])
        if not all(item.get(k, '').strip() for k in ('dark_iv_csv','dark_metrics','field_metrics','conn_metrics')):
            raise ValueError(f'Mask={case}: manifest missing a required file path')
        dark = read_metrics(item['dark_metrics'])
        field = read_metrics(item['field_metrics'])
        conn = read_metrics(item['conn_metrics'])

        if required_number(dark,'Dark_OK',case) != 1.0:
            raise ValueError(f'Mask={case}: Dark_OK did not pass')
        if field.get('Evaluation', '') != 'PEB':
            raise ValueError(f'Mask={case}: field_metrics must refer to PEB snapshot')
        if required_number(field,'H2_error_cuts',case) != 0.0:
            raise ValueError(f'Mask={case}: incomplete field sampling')
        if required_number(conn,'H2_FWD_Data_OK',case) != 1.0:
            raise ValueError(f'Mask={case}: invalid cathode diagnostic')
        if required_number(field,'H2_valid_cuts',case,positive=True) <= 0:
            raise ValueError(f'Mask={case}: field scan has no valid cuts')
        if 'Mask_um' in field and not math.isclose(required_number(field,'Mask_um',case),case,abs_tol=1e-6):
            raise ValueError(f'Mask={case}: field metric belongs to a different mask')
        if 'VBD_V' in field and not math.isclose(required_number(field,'VBD_V',case),float(item['VBD_V']),rel_tol=1e-5,abs_tol=1e-5):
            raise ValueError(f'Mask={case}: field metric VBD disagrees with manifest')
        if 'Mask_um' in conn and not math.isclose(required_number(conn,'Mask_um',case),case,abs_tol=1e-6):
            raise ValueError(f'Mask={case}: cathode metric belongs to a different mask')

        near = required_number(dark,'I_density_at_percentBelowVBD_A_per_um2',case,positive=True)*1e12
        common = abs_dark_at(item['dark_iv_csv'],common_voltage,case)
        if common <= 0.0:
            raise ValueError(f'Mask={case}: common dark current must be positive')
        i_forward = required_number(conn,'FWD_I_cathode_0p30_A',case)
        kcl = required_number(conn,'FWD_KCL_residual_0p30',case)
        if not 0.0 <= kcl <= 0.01:
            raise ValueError(f'Mask={case}: cathode diagnostic KCL closure exceeds 1%')
        if i_forward < 0.0:
            raise ValueError(f'Mask={case}: invalid cathode current')
        e_center = required_number(field,'E_Center_kVcm',case,positive=True)
        e_sti5 = required_number(field,'E_STI5_kVcm',case,positive=True)
        e_mask = required_number(field,'E_Mask_kVcm',case,positive=True)
        e_mask_r = required_number(field,'E_Mask_r_um',case)
        if not case-0.25-1e-5 <= e_mask_r <= case+0.25+1e-5:
            raise ValueError(f'Mask={case}: E_Mask_r_um is outside Mask±0.25 um window')
        aval = required_number(field,'Aval_Mask_cm3s',case)
        if aval < 0.0:
            raise ValueError(f'Mask={case}: AvalancheGeneration cannot be negative after clipping')
        results.append({
            'Mask_um':case, 'VBD_V':float(item['VBD_V']),
            'INear_pAum2':near, 'Icommon_pAum2':common,
            'Ecenter_kVcm':e_center, 'ESTI5_kVcm':e_sti5,
            'EMask_kVcm':e_mask, 'EMask_r_um':e_mask_r,
            'AvalMask_cm3s':aval, '_forward_I':i_forward,
            'CathodeConnectivity':review_field(item,'CathodeConnectivity',ALLOWED_CONNECTIVITY,case),
            'PEBRisk':review_field(item,'PEBRisk',ALLOWED_PEB,case),
        })

    baseline = next(r for r in results if math.isclose(r['Mask_um'],16.3,abs_tol=1e-8))
    if baseline['_forward_I'] <= 0.0:
        raise ValueError('P0 cathode current is zero; relative ratio is undefined')
    p0_forward = baseline['_forward_I']
    for row in results:
        row['DarkReduction_Near_pct'] = reduction(row['INear_pAum2'],baseline['INear_pAum2'])
        row['DarkReduction_Common_pct'] = reduction(row['Icommon_pAum2'],baseline['Icommon_pAum2'])
        row['ForwardI_RelativeP0'] = row['_forward_I']/p0_forward
        del row['_forward_I']

    outpath=Path(outpath)
    outpath.parent.mkdir(parents=True,exist_ok=True)
    with outpath.open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=OUTPUT_COLUMNS,extrasaction='raise')
        writer.writeheader()
        writer.writerows(results)
    return results,common_voltage


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('manifest')
    parser.add_argument('-o','--output',default='H2_results.csv')
    args=parser.parse_args()
    rows,common=analyze(args.manifest,args.output)
    print(f'Created {args.output}: {len(rows)} cases x {len(OUTPUT_COLUMNS)} columns')
    print(f'Common dark-current bias = {common:.12g} V (90% of minimum candidate VBD)')
    print('CathodeConnectivity/PEBRisk are manual physical-review statuses, not automatically inferred.')
