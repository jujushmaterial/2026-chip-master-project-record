# CMP SPAD 2D Reference EMW Baseline 구축·검증·동결 보고서

**문서 상태:** 2D Reference optical screening baseline **FREEZE**  
**작성일:** 2026-08-28  
**연구 담당:** A — 주상현, optical/device structure  
**프로젝트:** CMP(Chip Master Project) SPAD 공동연구  
**TCAD 환경:** Synopsys Sentaurus T-2022.03  
**사용 도구:** SDE → Sentaurus Mesh(SNMESH) → Sentaurus Device EMW(FDTD) → SVisual/SVisualPy  
**최우선 연구 기준:** `SPAD_연구계획서.md`

---

## 1. 문서 목적

이 문서는 CMP SPAD 연구에서 사용할 **2D Reference EMW screening baseline**이 어떤 문헌적 근거와 전기 baseline을 바탕으로 만들어졌는지, Sentaurus에서 실제 어떤 geometry/mesh/source/boundary/material 조건을 사용했는지, 어떤 오류와 수정 과정을 거쳤는지, 최종 OpticalGeneration 결과와 SCR 기반 정량지표가 어떻게 도출되었는지, mesh refinement 후 결과가 얼마나 수렴했는지를 상세히 기록한다.

본 문서의 목적은 다음과 같다.

1. Reference optical baseline을 이후 Gao Square 및 Proposed Annular 연구에서 변하지 않는 기준점으로 동결한다.
2. Reference의 optical 조건과 metric을 숫자로 재현 가능하게 기록한다.
3. “그림상 빨간 hotspot이 많아 보인다”와 같은 정성 판정에서 벗어나 동일 조건의 `G` 기반 정량 비교가 가능하도록 한다.
4. 2D screening과 최종 3D optical claim을 명확히 분리한다.
5. 후속 결과에 맞추기 위해 baseline 조건을 사후 변경하는 일을 방지한다.

---

# 2. 연구 전체에서 이 baseline의 위치

CMP SPAD 프로젝트의 공통 baseline은 **Literature-Constrained Surrogate 28-nm FD-SOI SPAD Baseline**이다.

본 연구는 ST VL53L9 내부 소자를 복제하거나 실제 foundry recipe를 역설계하는 연구가 아니다. 공개된 2017–2024 28 nm FD-SOI SPAD 연구계열에서 공개된 topology, stack, measured/simulated constraints를 이용하여 전기적으로·광학적으로 일관된 surrogate reference를 구축한다.

A의 optical 연구는 다음 세 구조를 비교한다.

| Case | 의미 | Optical periodic pattern |
|---|---|---|
| Reference | 공통 baseline | 없음 |
| Gao Square | 선행연구 benchmark | 480 nm pitch, FF 15% |
| Proposed Annular | 본 연구 제안 | FF 15%, radial pitch sweep |

Reference에는 의도적인 optical periodic pattern이 없으므로 **Reference FF와 pitch는 N/A**로 유지한다.

2D EMW의 목적은 빠른 screening 및 경향 확인이며, 최종 optical claim은 3D EMW에서 수행한다.

---

# 3. 문헌 근거

## 3.1 Gao et al., Photonics 2024

주 기준 논문:

> S. Gao et al., “Shallow Trench Isolation Patterning to Improve Photon Detection Probability of Single-Photon Avalanche Diodes Integrated in FD-SOI CMOS Technology,” *Photonics*, vol. 11, no. 6, 526, 2024.  
> DOI: 10.3390/photonics11060526

본 연구가 직접 가져가는 핵심은 다음과 같다.

### [논문 직접 실측 / 직접 기술]
- 28 nm CMOS FD-SOI
- quasi-circular SPAD
- standard process를 기반으로 하되 modified Deep N-well implantation 사용
- reference와 patterned SPAD를 동일 geometry 기반으로 비교
- room-temperature diode reverse I–V에서 `VBD ≈ 15.8 V`
- photosensitive area는 metallic BEOL opening을 두어 빛이 들어오도록 구성
- ARC 없음
- microlens 없음

### [논문 직접 optical benchmark]
2024 논문은 simulation을 통해 **480 nm pitch**를 선택했으며 fabrication용 pattern FF로 15%, 20%, 25%를 사용했다.

FF=15%, pitch=480 nm의 대표 square geometry:
- SOI square = **186 × 186 nm²**
- STI separation = **294 nm**
- `186 + 294 = 480 nm`

이 square pattern은 본 연구의 Reference가 아니라 **Gao Square Benchmark**이다.

### [동일 연구계열 optical constraint]
grating/Si interface에서 SCR에 대응하는 optical anchor는 약 **180 nm**이다. 본 연구에서는 이 값을 전기 baseline과 optical coordinate를 정합하는 anchor로 사용한다.

### [논문 방법론]
fixed incident illumination에서 local photogeneration `G`는 구조 내부의 multiple interference에 의해 결정되며, STI geometry를 이용해 SCR에서 `G`를 증가시키는 것이 optical optimization의 핵심이다.

PDP 방법론은 개념적으로

\[
PDP(\lambda)
=
\frac{1}{\Phi_{photons}(\lambda)}
\iiint ATP(\mathbf r)\,G(\mathbf r,\lambda)\,dV
\]

형태이다.

따라서 A의 optical 연구 목적은 한 점의 maximum field를 키우는 것이 아니라 **SCR/active-region과 photogeneration의 공간적 overlap을 높이는 것**이다.

---

## 3.2 동일 연구계열 electro-optical methodology

동일 연구계열의 선행 방법에서는 electrical simulation을 2D cylindrical로 계산하고 optical simulation을 3D로 수행한 뒤 electrical 결과를 3D로 mapping한다. SCR와 quasi-neutral collection region을 함께 고려하며, electric-field criterion과 minority-carrier drift/diffusion ratio를 이용해 active-region 범위를 정한다.

이 때문에 본 연구에서도 `y≈0.18 µm` 한 줄의 OpticalGeneration maximum을 final performance metric으로 사용하지 않는다.

---

## 3.3 Sentaurus EMW / FDTD 근거

Sentaurus T-2022.03 documentation에서 FDTD는 tensor mesh 기반이며 2D 및 3D optical excitation을 지원한다.

본 연구에서는 다음과 같이 적용한다.

- 2D Reference → fast screening / workflow validation
- Gao Square → small 3D periodic cell로 solver validation
- Proposed Annular → 2D screening 후 3D final
- 최종 Reference / Square / Annular 비교 → 3D EMW

따라서 현재 2D 결과를 **원통대칭으로 회전된 exact annular 3D 결과**라고 해석하지 않는다.

---

# 4. 공통 electrical baseline fingerprint

Optical baseline은 이미 동결된 electrical baseline과 좌표가 정합되어야 한다.

| Metric | Frozen value |
|---|---:|
| Workbench `DNW_Dose` | `3.15e17 cm^-3` Gaussian PeakVal |
| Workbench `PW_Dose` | `5.95e17 cm^-3` Gaussian PeakVal |
| `MeshScale` | `0.40` |
| `VBD` | **15.7979980544 V** |
| SCR p-side boundary | **0.00952007710343 µm** |
| SCR n-side boundary | **0.350885814092 µm** |
| SCR center proxy | **0.180202945597 µm** |
| SCR width | **0.341365736988 µm** |
| n-side QN end | **0.368542114729 µm** |
| Junction | **0.162696653385 µm** |
| central E-field max location | **0.162402346730 µm** |
| AvalancheGeneration/ImpactIonization peak | **0.172492191195 µm** |
| Ecenter | **415.640302289 kV/cm** |
| Eperiph | **302.936997033 kV/cm** |
| `R_E = Eperiph/Ecenter` | **0.728844136059** |

주의:
- `DNW_Dose`, `PW_Dose`는 이 SDE stage에서 physical implant dose `[cm^-2]`가 아니라 Gaussian analytic profile의 PeakVal `[cm^-3]`이다.
- `0.180203 µm`는 논문이 “SCR center”라고 직접 정의한 값이 아니라, 본 surrogate baseline에서 재현 가능한 representative spatial proxy로 정의하고 약 180 nm optical anchor에 정합한 값이다.

공통 optical 좌표:
- grating/bulk-Si optical reference: `y = 0`
- y가 증가하면 bulk 내부 방향

---

# 5. Optical SDE 구축

Electrical static baseline에서 full planar reference geometry를 optical derivative로 사용했다.

Reference identity에서 유지된 항목:
- ~25 µm class active geometry
- P-Well / modified DNW common electrical core
- native active-zone STI2, STI3, STI4
- peripheral STI5
- Upper Si ≈ 7 nm
- BOX ≈ 25 nm
- bulk Si
- intentional 480 nm optical periodic pattern 없음

Plane-wave excitation과 absorbing boundary를 위해 device 상부에 `t_Ambient = 1.00 µm`의 Ambient simulation region을 추가했다.

분류: **[surrogate simulation setting]**  
이는 실제 공정층이라고 주장하지 않는다.

주요 y coordinate:

```text
Ambient top                   ≈ -1.332 µm
UpperSi top                   ≈ -0.332 µm
UpperSi / BOX interface       ≈ -0.325 µm
BOX / bulk-Si interface       ≈ -0.300 µm
optical reference             =  0.000 µm
representative SCR proxy      = +0.180203 µm
bulk simulation bottom        = +10 µm
```

---

# 6. Sentaurus Mesh tensor-grid 구축

## 6.1 최초 `EnableEMW` 접근 실패

초기에는 `EnableEMW` workflow를 사용하려 했으나 학교 T-2022.03 설치환경에서 내부적으로 unsupported `-emw` path가 발생하여:

```text
Unknown option: -emw
```

오류가 발생했다.

전역 설치환경을 수정하지 않고 `EnableTensor` 기반 manual tensor-grid path로 전환했다.

## 6.2 Production mesh v0.3

```text
global maxCellSize x = 0.025 µm
global maxCellSize y = 0.025 µm
minCellSize          = 0.005 µm

OpticalActive:
x = -24 ~ +24 µm
y = -0.340 ~ +0.800 µm
max y cell = 0.010 µm

yCuts:
-0.332
-0.325
-0.300
 0.000
 0.800 µm

grading off
```

Production mesh SVisual 기준:
- Elements ≈ **1,010,640**
- Points ≈ **1,012,892**

`minCellSize=5 nm`와 `grading off`는 지나치게 작은 FDTD interface cell로 인한 CFL timestep collapse 위험을 줄이기 위한 **[surrogate numerical setting]**이다.

---

# 7. 940 nm EMW baseline

고정 source:

```text
Wavelength      = 940 nm
Direction       = fromTop
Incidence       = normal
Signal          = Harmonic
NRise           = 4
Polarization    = TE
Intensity       = 1 W/cm²
Temperature     = 300 K
```

`1 W/cm²`는 Reference / Square / Annular의 상대 비교를 위한 **[surrogate simulation normalization]**이다.

---

# 8. Optical material / CRI 실제 적용값

EMW 상세 log에서 940 nm에 실제 load된 optical properties:

| Material | n | k |
|---|---:|---:|
| Ambient | 1 | 0 |
| Oxide | **1.45121** | 0 |
| Silicon | **3.597** | **1.3689e-03** |

Silicon:
- relative permittivity ≈ **12.9384**
- electric conductivity ≈ **174.73 S/m**

최종 optical material 수는 3개:
1. Silicon
2. Oxide
3. Ambient

---

# 9. Boundary-condition 수정 이력

## 9.1 v0.1 — all-CPML

```text
Xmin/Xmax = CPML
Ymin/Ymax = CPML
```

v0.1은:
- stable dt = 2.2476e-17 s
- actual dt = 2.2396e-17 s
- 140 steps/period
- termination = 25,236 steps
- runtime ≈ 49 min 36.68 s

까지 수렴했으나:

```text
Edge diffraction possible
```

warning 때문에 final baseline으로 사용하지 않았다.

## 9.2 v0.2 / v0.2.1

2D plane-wave screening boundary를:

```text
X = PeriodicOblique
Y = CPML
```

로 변경했다.

이 PeriodicOblique boundary는 **computational boundary**이며 Reference physical pitch/FF를 정의하지 않는다.

PeriodicOblique 상태에서 detector sparse sampling을 유지했더니:

```text
StepX/Y/Z must be 1 for ErrorNorm = global
```

오류가 발생하여 v0.2.1에서:

```text
StepX = 1
StepY = 1
StepZ = 1
```

로 고정했다.

---

# 10. Final production EMW — v0.2.1

```text
Wavelength = 940 nm
TE
normal incidence
Harmonic
Intensity = 1 W/cm²

X = PeriodicOblique
Y = CPML
CPML Thickness = 15 cells

Detector:
Type = Periodic
Tolerance = 0.001
StepX/Y/Z = 1
BreakOnError = Yes
```

Production run:

```text
Excitation plane       = -1.2824 µm
Stable timestep        = 2.2476e-17 s
Actual timestep        = 2.2396e-17 s
Steps per period       = 140
Termination            = 7,456 steps
Total wall time        = 14 min 22.11 s
Time-stepping runtime  = 14 min 13.82 s
Edge diffraction warning = 없음
```

---

# 11. SVisual optical outputs

실제 확인:
- `OpticalGeneration`
- `AbsorbedPhotonDensity`
- `AbsorbedPowerDensity`
- `PowerFluxDensity`
- electric-field optical output

native STI와 thin stack이 940 nm field를 변조하며 Silicon 내부에 interference/scattering pattern을 형성한다.

Reference는 “SCR에 빛이 거의 들어오지 않는 구조”가 아니다. 대표 SCR depth에도 상당한 generation이 존재한다. 다만 x 방향 peak/dip가 강하므로 intentional optical optimization이 완료된 구조도 아니다.

---

# 12. y = 0.180203 µm anchor diagnostic

active aperture:
- `x = -12.5 ~ +12.5 µm`
- points = **1007**

Production result:

| Metric | Value |
|---|---:|
| G mean | **7.02041144773e20 cm⁻³ s⁻¹** |
| G median | **6.64647433545e20** |
| G min | **2.32163286775e19** |
| G max | **1.82989614940e21** |
| G std | **3.97491834167e20** |
| CV | **0.566194498894** |
| P10 | **1.96600129378e20** |
| P90 | **1.37159093068e21** |
| max/mean | **2.60653690033** |

해석:
- 940 nm generation은 representative SCR depth까지 충분히 도달한다.
- lateral nonuniformity가 크다.
- anchor cutline은 diagnostic이며 primary performance metric이 아니다.

---

# 13. Electrical SCR boundary 기반 2D metric

Frozen electrical center-cutline SCR boundaries:

```text
p-side = 0.00952007710343 µm
n-side = 0.350885814092 µm
width  = 0.341365736988 µm
center = 0.180202945597 µm
```

이 boundary를 active aperture 전체에 적용한 **central-SCR slab proxy**를 정의했다.

\[
G_{SCR,slab}^{2D}
=
\int_{y_p}^{y_n}
\int_{-12.5}^{12.5}
G(x,y)\,dx\,dy
\]

Numerical integration:
- y samples = **69**
- interval ≈ 5.02 nm
- slab area = **8.53414342471 µm²**

Production:

| Metric | Production v0.3 |
|---|---:|
| `G_SCR_slab_2D` | **6.03348761659e21 cm⁻³ s⁻¹ µm²** |
| `G_SCR_slab_average` | **7.06982214421e20 cm⁻³ s⁻¹** |
| nominal 1 µm extrusion equivalent rate | **6.03348761659e9 s⁻¹** |
| Gain vs Reference | **1.000000** |

1 µm extrusion rate는 2D diagnostic normalization일 뿐 full 3D SPAD의 absolute generation rate가 아니다.

---

# 14. Depth-profile 주의

SCR slab 내부의 lateral-integral maximum은 p-side sample `y=0.00952007710343 µm`에서 나타났다.

그러나 이를 “전체 optical peak가 p-side boundary에 있다”고 해석하지 않는다. search domain 자체가 SCR 안으로 제한되어 있기 때문이다. wider depth profile을 별도로 계산해야 실제 depth maximum을 판단할 수 있다.

---

# 15. Fine mesh convergence

v0.4에서는 물리조건을 바꾸지 않고 mesh만 refinement했다.

```text
global x/y max cell: 25 nm → 20 nm
active y max cell:   10 nm → 8 nm
minCellSize:          5 nm 유지
grading:              off 유지
critical yCuts:       동일
```

Fine mesh:
- Mesh Dimensions = **2417 × 655**
- Total cells = **1,583,135**
- production 대비 cell 수 = **+56.647%**

Fine EMW:
- stable dt = **1.3049e-17 s**
- actual dt = **1.3010e-17 s**
- 241 steps/period
- termination = **12,594 steps**
- wall time = **36 min 46.84 s**
- Edge diffraction warning 없음

Fine metric:

| Metric | Fine v0.4 |
|---|---:|
| `G_SCR_slab_2D` | **6.03317864225e21** |
| `G_SCR_slab_average` | **7.06946009927e20** |
| Anchor G mean | **7.03320896356e20** |
| Anchor CV | **0.566356647785** |
| Anchor G min | **1.84841838469e19** |
| Anchor G max | **1.85291718702e21** |

---

# 16. Mesh convergence 판정

Primary metric change:

\[
\Delta G_{SCR}
=
\frac{G_{fine}-G_{prod}}{G_{prod}}\times100
=
\boxed{-0.005121\%}
\]

Comparison:

| Metric | Production | Fine | Relative change |
|---|---:|---:|---:|
| `G_SCR_slab_2D` | 6.03348761659e21 | 6.03317864225e21 | **-0.005121%** |
| `G_SCR_slab_average` | 7.06982214421e20 | 7.06946009927e20 | **-0.005121%** |
| Anchor G mean | 7.02041144773e20 | 7.03320896356e20 | **0.1823%** |
| Anchor CV | 0.566194498894 | 0.566356647785 | **0.0286%** |
| EMW termination steps | 7,456 | 12,594 | **+68.91%** |
| Wall time | 14m22.11s | 36m46.84s | **2.56×** |

**Mesh convergence: PASS**

cell 수는 약 **56.65%** 증가했지만 integrated SCR-slab generation은 약 **0.0051%**만 변했다. 반면 runtime은 약 **2.56×** 증가했다.

따라서:
- v0.3 = production/sweep mesh
- v0.4 = convergence evidence

로 보존한다.

---

# 17. 최종 2D Reference EMW baseline freeze

Production code set:

```text
CMP_SPAD_2D_EMW_Reference_Optical_SDE_v1.0.txt
CMP_SPAD_2D_EMW_Reference_SNMesh_SWB_RuntimeSafe_v0.3.txt
CMP_SPAD_2D_EMW_Reference_940nm_EMW_SWB_v0.2.1_periodicX_cpmlY_detectorfix.txt
CMP_SPAD_2D_EMW_Reference_SVisualPy_SCRSlabMetric_v0.2.txt
```

Diagnostic:
```text
CMP_SPAD_2D_EMW_Reference_SVisualPy_MetricExtractor_v0.1.txt
```

Convergence validation:
```text
CMP_SPAD_2D_EMW_Reference_SNMesh_FineConvergence_v0.4.txt
```

Frozen production metric:

\[
\boxed{
G_{SCR,Ref}^{2D,slab}
=
6.03348761659\times10^{21}
\;\mathrm{cm^{-3}s^{-1}\mu m^2}
}
\]

정확한 명칭:

> **Reference 2D central-SCR slab integrated OpticalGeneration**

---

# 18. 물리적 해석

현재 Reference는 SCR depth에 generation이 없는 구조가 아니다. `y≈0.180203 µm`에서 평균 `G≈7.02e20 cm^-3 s^-1`가 확인된다.

그러나 anchor CV≈0.566이므로 x 방향 photogeneration은 매우 강하게 modulation된다. 즉 native STI reference는:
- SCR에 generation이 존재
- intentional periodic optimization은 없음
- constructive/destructive interference가 lateral distribution을 크게 바꿈

으로 해석한다.

Proposed Annular의 올바른 목표:

> **동일 Si FF=15%에서 radial pitch를 변화시켜 940 nm photogeneration field와 SCR/active collection region의 공간적 overlap을 증가시키고 Reference 및 Gao Square보다 integrated useful generation을 높이는 것**

---

# 19. Baseline validity 판정

| Validation item | Status |
|---|---|
| Literature-constrained reference identity | PASS |
| Reference native STI retained | PASS |
| Intentional periodic pattern absent | PASS |
| UpperSi / BOX preserved | PASS |
| SDE → tensor mesh | PASS |
| 940 nm FDTD | PASS |
| Optical CRI mapping | PASS |
| Boundary artifact correction | PASS |
| Harmonic convergence | PASS |
| OpticalGeneration extraction | PASS |
| Anchor cutline automation | PASS |
| SCR-slab integration | PASS |
| Mesh convergence | PASS |
| 2D Reference screening baseline | **FREEZE** |
| x-dependent exact 2D SCR map | PENDING |
| Final 3D Reference optical claim | PENDING |
| Gao Square 3D validation | NEXT |

---

# 20. 명확한 한계

1. 현재 2D EMW는 exact annular 3D simulation이 아니다.
2. PeriodicOblique-X는 numerical plane-wave screening boundary이며 Reference physical pitch가 아니다.
3. `G_SCR_slab`은 center electrical SCR p/n boundary를 lateral aperture에 펼친 proxy이다.
4. 1 W/cm²는 internal comparison normalization이다.
5. 현재 설치된 Sentaurus optical database를 사용하며 실제 foundry BEOL 전체 optical constants를 복원했다고 주장하지 않는다.
6. 현재 `G`만으로 absolute PDP를 주장하지 않는다.
7. final A+B는 spatial `G × ATP` integration으로 평가한다.

---

# 21. 다음 단계

Reference 2D baseline은 더 이상 임의 보정하지 않는다.

다음은 **Gao Square 480 nm / FF=15% small 3D periodic unit-cell optical solver validation**이다.

고정 benchmark:
- pitch = **480 nm**
- FF = **15%**
- Si = **186 × 186 nm²**
- STI separation = **294 nm**
- wavelength = **940 nm**
- same source normalization
- same CRI convention
- periodic lateral boundary
- normal incidence

이후 Proposed Annular에서 FF=15%를 유지한 radial-pitch screening으로 진행한다.

---

# 22. Evidence classification

| 항목 | 분류 |
|---|---|
| 28 nm FD-SOI / quasi-circular / modified DNW / VBD≈15.8 V | [논문 직접 실측/기술] |
| UpperSi≈7 nm / BOX≈25 nm | [동일 연구계열 constraint] |
| native STI topology | [동일 연구계열 constraint] |
| ~180 nm optical anchor | [동일 연구계열 simulation constraint] |
| 480 nm / FF15 / 186 nm square / 294 nm STI | [논문 직접 benchmark] |
| frozen VBD/SCR/E-field | [직접 TCAD 결과] |
| Ambient 1 µm | [surrogate simulation setting] |
| source 1 W/cm² | [surrogate simulation normalization] |
| tensor mesh cell sizes | [surrogate numerical setting] |
| PeriodicOblique-X / CPML-Y | [surrogate numerical boundary setting] |
| G_SCR slab values | [직접 TCAD post-processing result] |
| mesh convergence ΔG | [직접 TCAD 결과 + 계산] |

---

# 23. 보관 command 원문과 SHA-256

GitHub optical freeze folder에는 아래 command를 **원문 그대로** 보관한다.

| File | SHA-256 |
|---|---|
| `CMP_SPAD_2D_EMW_Reference_Optical_SDE_v1.0.txt` | `3c64aeefe8261feddc8d3a43bd4718905acb30d3cd6ddc90ae19bdf40a833166` |
| `CMP_SPAD_2D_EMW_Reference_SNMesh_SWB_RuntimeSafe_v0.3.txt` | `022fb05decc7ae4fe14783a48ebbfca10f64a14d0c9c7efb0aef92f56244cad7` |
| `CMP_SPAD_2D_EMW_Reference_940nm_EMW_SWB_v0.2.1_periodicX_cpmlY_detectorfix.txt` | `98d524d564bfe44462d03323919891358424705470f91065e609c43478d9f7f4` |
| `CMP_SPAD_2D_EMW_Reference_SVisualPy_MetricExtractor_v0.1.txt` | `ac358af99cceb4c15ea07bb7ee3a35ba2546f11317fc065660a6522a70d53a8e` |
| `CMP_SPAD_2D_EMW_Reference_SVisualPy_SCRSlabMetric_v0.2.txt` | `76b518fb621895db023d8667340b4258f64f38757cf451f717e1f7253e8b7db4` |
| `CMP_SPAD_2D_EMW_Reference_SNMesh_FineConvergence_v0.4.txt` | `d60cb844f625f60d8649e0b4f5ab9759163cfaa5a3fa36bb78c807cff08aeac1` |

---

# 24. 참고문헌

1. S. Gao et al., “Shallow Trench Isolation Patterning to Improve Photon Detection Probability of Single-Photon Avalanche Diodes Integrated in FD-SOI CMOS Technology,” *Photonics*, 11(6), 526, 2024. DOI: 10.3390/photonics11060526.
2. S. Gao et al., 28 nm FD-SOI SPAD electro-optical simulation/light-trapping 연구계열.
3. D. Issartel et al., 28 nm FD-SOI SPAD modified-DNW/STI/avalanche 연구계열.
4. Synopsys, *Sentaurus Device Electromagnetic Wave Solver User Guide*, T-2022.03.
5. Synopsys, *Sentaurus Mesh User Guide*, T-2022.03.
6. 프로젝트 기준문서 `SPAD_연구계획서.md`.

---

# 25. Freeze 선언

**2026-08-28 기준 다음을 2D Reference optical screening baseline으로 동결한다.**

```text
Geometry       = Optical SDE v1.0
ProductionMesh = RuntimeSafe SNMESH v0.3
EMW            = 940nm v0.2.1
Metric         = SCRSlabMetric v0.2
Convergence    = Fine SNMESH v0.4 validation PASS

ReferencePitch = N/A
ReferenceFF    = N/A

G_SCR_slab_2D
= 6.03348761659e21 cm^-3 s^-1 um^2
```

향후 Gao Square 또는 Annular 결과가 기대와 다르다는 이유만으로 이 baseline의 geometry/source/CRI/boundary/metric convention을 사후 변경하지 않는다. 변경이 필요한 새로운 근거가 발견되면 기존 가정, 새 근거, 충돌 내용, 결과 영향부터 별도로 기록한다.
