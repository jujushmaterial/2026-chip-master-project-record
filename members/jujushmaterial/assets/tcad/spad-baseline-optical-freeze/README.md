# SPAD Baseline Optical Freeze

CMP SPAD **2D Reference optical screening baseline** 동결본.

## Production baseline

```text
Optical SDE  -> CMP_SPAD_2D_EMW_Reference_Optical_SDE_v1.0.txt
SNMESH       -> CMP_SPAD_2D_EMW_Reference_SNMesh_SWB_RuntimeSafe_v0.3.txt
EMW          -> CMP_SPAD_2D_EMW_Reference_940nm_EMW_SWB_v0.2.1_periodicX_cpmlY_detectorfix.txt
Metric       -> CMP_SPAD_2D_EMW_Reference_SVisualPy_SCRSlabMetric_v0.2.txt
```

Diagnostic:
`CMP_SPAD_2D_EMW_Reference_SVisualPy_MetricExtractor_v0.1.txt`

Convergence:
`CMP_SPAD_2D_EMW_Reference_SNMesh_FineConvergence_v0.4.txt`

## Frozen metric

```text
ReferencePitch = N/A
ReferenceFF    = N/A
G_SCR_slab_2D = 6.03348761659e21 cm^-3 s^-1 um^2
```

Fine mesh:
`6.03317864225e21 cm^-3 s^-1 um^2`

Relative change:
`-0.005121%`

Production v0.3을 유지하고 v0.4는 convergence evidence로 보존한다.

상세 기록:
`CMP_SPAD_2D_Reference_EMW_Baseline_Freeze_Report_2026-08-28.md`

> 현재 metric은 center electrical SCR boundaries를 lateral aperture에 적용한 2D central-SCR slab proxy이다. final 3D optical claim이나 exact ATP×G integration과 동일시하지 않는다.
