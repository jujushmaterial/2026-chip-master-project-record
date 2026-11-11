#!/usr/bin/env python3
"""Build H2-only variants from the checked CMP Electrical_Test source decks.

No source files are overwritten. TDR/PLX numerical validation requires Sentaurus.
Usage: python H2_prepare_decks.py /path/to/Electrical_Test
"""
from pathlib import Path
import argparse

SOURCE = {
  'sprocess': '02_SProcess2_TripleDNW_TriplePW_AbsoluteDose.cmd',
  'smesh': '04_SNMesh2_ProfileMapping.cmd',
  'vbd': '06_SVisualPy_VBD_SCR.py',
  'field': '07_SDevice2_Dynamic_SCR_ATP.cmd',
}
OUTPUT = {
  'sprocess': '02_H2_SProcess2_TrimMask.cmd',
  'smesh': '04_H2_SNMesh2_RefinedEdge.cmd',
  'vbd': '06_H2_SVisualPy1_VBD_Bias.py',
  'field': '07_H2_SDevice2_SCR_PEB_ATP.cmd',
}

def replace_once(s, old, new, label):
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exact one original anchor, got {count}: {old[:90]!r}')
    return s.replace(old, new, 1)

def generate(source_dir, output_dir):
    source_dir = Path(source_dir)
    output_dir = Path(output_dir)
    content = {name: (source_dir / path).read_text(encoding='utf-8') for name, path in SOURCE.items()}
    sp = content['sprocess']
    sp = replace_once(sp, 'set R_DNW_E   16.30\n',
        'set R_DNW_E   16.30\nset R_DNW_TRIM_E @Mask@\n', 'Mask parameter')
    sp = replace_once(sp,
        'mask name=M_DNW     left=$AXIS_EXT   right=$R_DNW_E     negative\n',
        'mask name=M_DNW     left=$AXIS_EXT   right=$R_DNW_E     negative\n'
        'mask name=M_DNW_TRIM left=$AXIS_EXT right=$R_DNW_TRIM_E negative\n',
        'Trim-specific mask')
    sp = replace_once(sp, '''   energy=${DNW_TRIM_E}<keV> \\
   dose=${DNW_TRIM_DOSE}<cm-2> \\
   tilt=${IMP_TILT}<degree> \\
   rotation=${IMP_ROT}<degree> \\
   mult.rot=${IMP_MROT} \\
   mask=M_DNW''',
        '''   energy=${DNW_TRIM_E}<keV> \\
   dose=${DNW_TRIM_DOSE}<cm-2> \\
   tilt=${IMP_TILT}<degree> \\
   rotation=${IMP_ROT}<degree> \\
   mult.rot=${IMP_MROT} \\
   mask=M_DNW_TRIM''',
        'Trim implant mask reference')
    sp = replace_once(sp,
        'WritePlx n@node@_F_r13.plx  y=13.0\n',
        'WritePlx n@node@_F_r13.plx  y=13.0\n'
        'WritePlx n@node@_F_r12p10.plx y=12.10\n'
        'WritePlx n@node@_F_r12p35.plx y=12.35\n'
        'WritePlx n@node@_F_r12p65.plx y=12.65\n',
        'Final-only STI5 PLX')
    sp = replace_once(sp, '# Registered SWB parameters (14):', '# Registered SWB parameters (15):', 'Count of SWB parameters')
    sp = replace_once(sp, '# RTA_T RTA_t\n', '# RTA_T RTA_t Mask\n', 'List of SWB parameters')
    sp = replace_once(sp, 'set R_DNW_TRIM_E @Mask@\n',
        '''set R_DNW_TRIM_E @Mask@
# H2 scope: adjust only the Trim DNW radial mask boundary.
if {$R_DNW_TRIM_E < 12.0 || $R_DNW_TRIM_E > $R_DNW_E} {
    error "H2 @Mask@ outside validated DOE design envelope 12.0..16.3 um"
}
puts "H2_TRIM_MASK_END_UM=$R_DNW_TRIM_E"
''', 'Mask parameter validation')
    sm = content['smesh']
    sm = replace_once(sm,
        'RefineWindow = rectangle [(11.600 -0.062), (16.000 2.100)]',
        'RefineWindow = rectangle [(11.600 -0.062), (16.650 2.100)]',
        'PEB refinement coverage to P0 Trim end')
    sm = replace_once(sm,
        'RefineWindow = rectangle [(0.000 0.400), (16.300 0.560)]',
        'RefineWindow = rectangle [(0.000 0.400), (16.650 0.560)]',
        'Junction refinement coverage')
    sv = content['vbd']
    sv = replace_once(sv, '#set ATP_BIAS_V -1\n',
        '#set ATP_BIAS_V -1\n#set PEB_BIAS_V -1\n', 'PEB SWB extraction variable')
    sv = replace_once(sv,
        'ATP_ABOVE_VBD_PCT = 7.6086',
        'ATP_ABOVE_VBD_PCT = 7.6086\nPEB_BELOW_VBD_PCT = 0.10  # H2 early-edge diagnostic, surrogate assumption',
        'PEB bias percent')
    sv = replace_once(sv,
        'atp_bias = float(vbd * (1.0 + ATP_ABOVE_VBD_PCT / 100.0))',
        'atp_bias = float(vbd * (1.0 + ATP_ABOVE_VBD_PCT / 100.0))\npeb_bias = float(vbd * (1.0 - PEB_BELOW_VBD_PCT / 100.0))',
        'PEB derived voltage')
    sv = replace_once(sv,
        'emit("ATP_BIAS_V", atp_bias)',
        'emit("ATP_BIAS_V", atp_bias)\nemit("PEB_BIAS_V", peb_bias)',
        'PEB DOE extraction')
    sv = replace_once(sv,
        'print("SVISUALPY1: VBD and percent-based SCR/DARK/ATP biases exported")',
        'print("SVISUALPY1: H2 VBD and SCR/DARK/PEB/ATP biases exported")',
        'Audit print')
    dv = content['field']
    dv = replace_once(dv,
        '  Plot(FilePrefix="n@node@_SCR")\n',
        '''  Plot(FilePrefix="n@node@_SCR")
  * H2: additional subbreakdown near-onset field/avalanche snapshot
  * PEB_BIAS_V = 0.999 * VBD, distinct from SCR-bias analysis.
  Quasistationary(
    InitialStep=1.0e-3 MinStep=1.0e-9 MaxStep=2.0e-3
    Increment=1.25 Decrement=2.0
    Goal { Name="cathode" Voltage=@PEB_BIAS_V@ }
  ){
    Coupled { Poisson Electron Hole }
  }
  Plot(FilePrefix="n@node@_PEB")
''', 'Subbreakdown PEB snapshot')
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = {'sprocess':sp,'smesh':sm,'vbd':sv,'field':dv}
    for key, body in generated.items():
        (output_dir/OUTPUT[key]).write_text(body, encoding='utf-8')
    return [output_dir/OUTPUT[key] for key in OUTPUT]

if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('source_dir', help='Original Electrical_Test directory checked out from GitHub')
    a.add_argument('--out', default='H2_generated', help='Generated output directory')
    args = a.parse_args()
    for path in generate(args.source_dir, args.out):
        print('GENERATED:',path)
