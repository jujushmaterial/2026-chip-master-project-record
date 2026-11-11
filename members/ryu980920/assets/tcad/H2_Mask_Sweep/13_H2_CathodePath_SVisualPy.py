#setdep @node|-1@
# SVisualPy quantitative forward-bias terminal-current diagnostics.
# 13th SWB node, immediately after 12_H2_CathodePath_SDevice.cmd.
# Do NOT declare cathode continuity from these currents alone: review 2D
# NetDoping, eCurrent/Vector and eQuasiFermi along the DNW corridor.
# The substrate is co-ramped to -0.30 V; a measured cathode current is NOT
# sufficient to classify connected/disconnected.
import os
import fnmatch
import numpy as np

VIS_NODE=@node@
SDEV_NODE=@node|-1@
MASK_UM=float(@Mask@)
FILE=f'n{SDEV_NODE}_des.plt'
TDR=f'n{SDEV_NODE}_FWD_des.tdr'
if not os.path.isfile(FILE) or not os.path.isfile(TDR):
    raise RuntimeError(f'Forward-bias I-V or TDR missing: {FILE}, {TDR}')
sv.load_file(FILE,name='H2CONN')

def match(patterns):
    names=list(sv.list_variables(dataset='H2CONN'))
    for p in patterns:
        for name in names:
            if fnmatch.fnmatch(name.lower(),p.lower()):
                return name
    return None

def get(name):
    return np.asarray(sv.get_variable_data(varname=name,dataset='H2CONN'),dtype=float)

def interp(x,y,target):
    m=np.isfinite(x)&np.isfinite(y)
    x,y=x[m],y[m]
    if len(x)<2 or not x.min()<=target<=x.max():
        return np.nan
    ix=np.argsort(x)
    return float(np.interp(target,x[ix],y[ix]))

vn=match(['*cathode*OuterVoltage*','*cathode*InnerVoltage*'])
ia=match(['*anode*TotalCurrent*'])
ic=match(['*cathode*TotalCurrent*'])
isub=match(['*substrate*TotalCurrent*'])
if None in [vn,ia,ic,isub]:
    raise RuntimeError('H2 forward I-V terminal variables missing')
v=-get(vn)  # positive magnitude when cathode is forward-biased negative
ai=get(ia); ci=get(ic); si=get(isub)
report={}
for volts, suffix in [(0.10,'0p10'),(0.30,'0p30')]:
    report[f'FWD_I_anode_{suffix}_A']=abs(interp(v,ai,volts))
    report[f'FWD_I_cathode_{suffix}_A']=abs(interp(v,ci,volts))
    report[f'FWD_I_substrate_{suffix}_A']=abs(interp(v,si,volts))
    a=interp(v,ai,volts); c=interp(v,ci,volts); s=interp(v,si,volts)
    denom=abs(a)+abs(c)+abs(s)
    report[f'FWD_KCL_residual_{suffix}']=abs(a+c+s)/denom if denom>0 else np.nan
# Numerical QC, NOT an electrical-connectivity threshold.
KCL_TOL=1.0e-2  # 1% current-closure criterion [surrogate QA assumption]
report['H2_FWD_Data_OK']=float(np.isfinite(report['FWD_I_cathode_0p30_A'])
       and np.isfinite(report['FWD_KCL_residual_0p30'])
       and report['FWD_KCL_residual_0p30'] <= KCL_TOL)
with open(f'n{VIS_NODE}_H2_CathodePath_metrics.txt','w') as f:
    f.write(f'Mask_um={MASK_UM:.12g}\nSource={FILE}\nTDR={TDR}\n')
    f.write('Judgement=REVIEW_REQUIRED_NET_DOPING_CURRENT_VECTOR_QUASIFERMI\n')
    f.write('Bias=Anode_0V_Cathode_and_Substrate_minus0p30V\n')
    for k,value in report.items():
        f.write(f'{k}={value:.12g}\n')
for k,vv in report.items():
    if np.isfinite(vv):
        print(f'DOE: {k} {vv:.12g}')
    else:
        print(f'DOE: {k} x')
print('H2_CATHODE_PATH: numeric forward currents only; connectivity requires physical path review')
