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

## 원문 command 주석 주의

보관한 command는 실제 실행본을 **수정하지 않고 원문 그대로** 저장하였다. 따라서 일부 과거 주석이 현재 freeze 상태와 맞지 않게 남아 있다.

- Optical SDE v1.0 상단의 `Electrical calibration is not frozen`, `Stage-1 provisional point: DNW_Dose=3.10e17` 문구는 파생 당시의 과거 주석이다. 현재 authoritative electrical freeze는 Workbench `DNW_Dose=3.15e17`, `PW_Dose=5.95e17`, `MeshScale=0.40`, `VBD=15.7979980544 V`이다.
- EMW v0.2.1의 `Detector sampling is intentionally sparse` 주석은 과거 문구이며 실제 active code는 PeriodicOblique global error norm 요구에 따라 `StepX=StepY=StepZ=1`이다.

원문 보존을 위해 command 자체의 주석을 고쳐 쓰지 않았고, 현재 기준값은 상세 freeze 보고서와 이 README를 우선한다.

> 현재 metric은 center electrical SCR boundaries를 lateral aperture에 적용한 2D central-SCR slab proxy이다. final 3D optical claim이나 exact ATP×G integration과 동일시하지 않는다.
