# CMP SPAD 3D Baseline Re-audit Decision Record
## 2026-10-06 — Codex 최종보고서 검토 및 3D Reference 구현 착수 기준

## 0. 문서 목적

Codex의 문헌 재감사 최종보고서 `SPAD_3D_Baseline_Reaudit_Report.md`를 프로젝트 기준으로 검토한 뒤, 현재 2D frozen surrogate baseline에서 3D Reference / Gao Square / Annular 구조로 넘어가기 위한 **의사결정과 구현 gate**를 기록한다.

이 문서는 Codex 최종보고서를 대체하지 않는다. 원문 근거와 상세 provenance는 최종보고서를 우선하며, 이 문서는 프로젝트 실행 관점의 결정사항을 정리한다.

---

## 1. 최종 판정

Codex 최종판정:

> **READY WITH SURROGATE ASSUMPTIONS**

해석:
- 2024 Reference의 exact GDS/mask를 복원할 수 있다는 의미가 아니다.
- 공개 문헌은 device family, junction topology, 25 µm-class quasi-circular identity, non-axisymmetric staircase character, modified-DNW high-VBD fingerprint, 7 nm upper Si / 25 nm BOX 등의 제약을 제공한다.
- exact PW/DNW XY mask, exact 25 µm boundary definition, STI1-STI7 치수/좌표/깊이, contact polygon, full BEOL optical stack 등은 미공개이다.
- 따라서 명시적 surrogate assumption과 sensitivity split을 전제로 3D Reference 구현을 시작할 수 있다.

---

## 2. 3D Reference의 프로젝트 정의

앞으로 3D Reference는 다음으로 정의한다.

> **공개된 2017–2024 28 nm FD-SOI SPAD 연구계열과 frozen 2D electrical fingerprint를 함께 만족하도록 구성한 literature-constrained 3D surrogate Reference**

구조적 identity:
- 28 nm FD-SOI CMOS
- 약 25 µm-class quasi-circular diode
- 실제 full-cell은 rotational symmetry가 아닌 rectilinear/staircase 및 non-axisymmetric layout
- PW anode / modified-DNW cathode junction
- upper Si 7 nm [동일 연구계열 constraint]
- BOX 25 nm [동일 연구계열 constraint]
- Reference에는 intentional periodic square/annular optical pattern 없음

금지:
- 2D half-cell을 단순 회전하여 actual 3D Reference라고 주장
- STI2/3/4/5를 concentric ring으로 변환
- exact Gao 2024 GDS reconstruction 주장

---

## 3. 기존 2D frozen baseline의 지위

3D 작업 시작 시 다음 electrical fingerprint는 유지한다.

```text
VBD              = 15.7979980544 V

SCR p-side       = 0.00952007710343 µm
SCR n-side       = 0.350885814092 µm
SCR center proxy = 0.180202945597 µm
SCR width        = 0.341365736988 µm

DNW analytic PeakVal = 3.15e17 cm^-3
PW analytic PeakVal  = 5.95e17 cm^-3
```

주의:
- DNW/PW PeakVal은 implant dose가 아니라 analytic concentration parameter.
- 위 SCR 좌표는 frozen 2D surrogate fingerprint이며 논문 직접값이 아니다.
- geometry-only 3D validation 완료 전 DNW/PW profile을 재-fit하지 않는다.

현재 stack / cross-sectional surrogate:
```text
Upper Si  = 0.007 µm
BOX       = 0.025 µm
STI depth = 0.300 µm [surrogate assumption]

Representative 2D intervals:
STI1 = 0.700–1.300 µm
STI2 = 2.975–3.275 µm
STI3 = 6.100–6.400 µm
STI4 = 9.225–9.525 µm
STI5 = 12.200–12.800 µm
```

STI interval 숫자는 2D surrogate deck에만 속하며 3D radius 또는 exact XY coordinate로 변환하지 않는다.

---

## 4. Codex 재분석으로 확정된 가장 중요한 correction

### 4.1 2024 Reference exact STI branch는 공개되지 않음

2024 Reference가 2023 계열의:
- Reference
- Fusion
- Peripheral STI aligned + Fusion

중 정확히 어느 mask branch와 동일한지는 공개되지 않았다.

따라서:
- active STI2/3/4 presence
- peripheral STI5 overlap

은 **2024 exact mask fact**가 아니라 현재 baseline을 제약하는 **same-lineage primary surrogate candidate**로 취급한다.

권장 명칭:
```text
P09-Reference-like STI topology constrained surrogate
```

금지 명칭:
```text
2024 exact Reference STI layout
```

### 4.2 Mandatory STI sensitivity

Primary candidate:
- active STI2/3/4 present
- peripheral STI5 overlap

Mandatory splits:
- active STI2/3/4 removed/minimized
- STI5 aligned

Optional bound:
- STI5 shifted

목적은 15.8 V를 만드는 geometry를 찾는 것이 아니라, branch uncertainty가 VBD/SCR/peripheral field/PEB에 미치는 영향을 확인하는 것이다.

---

## 5. 3D lateral geometry candidate 전략

Codex 권고를 채택한다.

### Candidate A — Coarse staircase
- lower-complexity control
- mesh/debug 및 2D→3D mapping sanity에 유리
- perimeter/corner representation은 거칠 수 있음

### Candidate B — Medium staircase
- **recommended primary**
- P08 Fig.18 / P10 Fig.6의 rectilinear staircase visual character와 계산비용의 균형
- 중앙 junction, active STI, peripheral STI, NW/contact-side topology를 분리하여 구현
- primary 3D Reference 후보

### Candidate C — Fine staircase
- staircase resolution sensitivity upper bound
- finer shape가 실제 GDS에 더 정확하다고 주장하지 않음

선택 기준:
- 외형 유사도 단독 사용 금지
- frozen electrical fingerprint 안정성
- mesh convergence
- peripheral breakdown localization
- candidate 간 차이가 numerical noise보다 충분히 큰지

현재 프로젝트 권고:
> **Candidate B를 primary로 시작하고 A/C를 sensitivity bounds로 사용**

---

## 6. Surrogate Assumption Registry 필요사항

3D SDE 작성 전에 SA-01~SA-12를 case manifest에 등록한다.

| ID | Assumption |
|---|---|
| SA-01 | quasi-circular staircase resolution |
| SA-02 | 25 µm boundary assignment |
| SA-03 | primary active-STI branch |
| SA-04 | primary STI5 relation |
| SA-05 | STI1/6/7 realization |
| SA-06 | STI depth |
| SA-07 | contact-aware extent |
| SA-08 | Gao lattice origin / clipping |
| SA-09 | BEOL-effective stack |
| SA-10 | optical polarization aggregation |
| SA-11 | finite-domain boundary |
| SA-12 | avalanche / defect deck |

현재 바로 사용할 수 있는 provisional decisions:
- SA-01: Candidate B medium staircase primary
- SA-03: P09-Reference-like active STI2/3/4 present
- SA-04: peripheral STI5 overlap primary, aligned mandatory split
- SA-06: STI depth 0.300 µm을 initial frozen [surrogate assumption]으로 사용; 이후 sensitivity 수행
- frozen PW/DNW profile 유지
- geometry-only electrical PASS 전 doping 재-fit 금지

나머지 SA 항목은 실제 3D geometry specification / solver deck 작성 전에 별도 freeze한다.

---

## 7. TCAD split의 목적

잘못된 질문:
> 어떤 3D geometry가 VBD=15.8 V를 만드는가?

올바른 질문:
> 문헌 제약과 frozen 2D baseline을 모두 만족하는 plausible 3D geometry 중 어떤 realization이 electrical fingerprint를 가장 안정적으로 보존하는가?

따라서 geometry와 doping을 동시에 자유롭게 fit하지 않는다.

---

## 8. 3D electrical validation 순서

### Stage 1 — Frozen 2D reproduction
기존 deck을 다시 실행하여:
- VBD
- SCR
- field
- reverse I–V
가 reproducible한지 확인한다.

### Stage 2 — Simple 3D extrusion sanity
최종 구조가 아니라 mapping/debug용 구조.

확인:
- material mapping
- coordinate origin
- unit
- contact assignment
- 2D→3D dopant mapping
- profile conservation

### Stage 3 — Candidate A/B/C geometry-only split
고정:
- doping
- physics model
- STI depth
- contact convention

변수:
- outer staircase realization

### Stage 4 — Active STI split
- STI2/3/4 present
- removed/minimized

### Stage 5 — Peripheral STI split
- overlap/reference-like
- aligned
- shifted optional

### Stage 6 — Contact / STI depth / physics sensitivity
Primary topology가 정해진 후 별도로 수행한다.

---

## 9. Required electrical output gate

각 3D Reference candidate에서 최소 다음을 저장한다.

- VBD
- SCR p-side
- SCR n-side
- SCR center
- SCR width
- reverse I–V
- centerline E-field
- peak central E-field
- peripheral/corner E-field
- breakdown onset voltage
- breakdown onset location
- impact-ionization integral/location
- ATP map 및 line cuts
- dark-current components 가능한 범위
- mesh convergence
- 2D→3D dopant/profile conservation

현재 numerical tolerance는 임의로 만들지 않는다.

먼저:
1. mesh convergence
2. extraction repeatability
3. candidate-to-candidate numerical variation

을 확인한 후 project tolerance를 freeze한다.

---

## 10. 3D VBD가 frozen 2D와 다를 경우의 debug order

다음 순서를 지킨다.

```text
mesh convergence
→ contact / boundary
→ dopant mapping
→ coordinate / unit consistency
→ symmetry-removal effect
→ peripheral / corner field
→ avalanche model
```

위 확인 전:
- STI를 임의 이동
- PW/DNW profile 재-fit
- geometry+doping simultaneous fitting

을 하지 않는다.

---

## 11. Reference 3D optical gate

3D Reference가 electrical PASS된 뒤에만 940 nm EMW를 수행한다.

Reference optical identity:
- intentional periodic optical pattern 없음
- Reference FF/pitch 없음
- accepted native-STI branch 유지
- 동일 optical material/source/normalization rule 사용

저장:
- 3D G(x,y,z)
- SCR-integrated photogeneration
- active-region integrated G
- reflection/transmission 가능한 경우
- mesh/boundary/source metadata

이 Reference 결과가 Gao / Annular gain denominator가 된다.

---

## 12. Gao Square 3D benchmark

직접 확인된 unit-cell 값:
```text
pitch = 480 nm in x/y
FF = 15%
Si square = 186 × 186 nm²
STI separation = 294 nm
```

구현 원칙:
1. accepted unpatterned Reference full-cell geometry를 복제
2. PW/DNW, junction, outer staircase, contacts, native-STI branch 유지
3. photosensitive area에 intentional square pattern만 추가
4. interior unit-cell에는 480/186/294 nm direct value 사용
5. lattice origin / edge clipping / contact exclusion은 SA-08 surrogate variants로 등록
6. STI depth는 Reference와 동일한 surrogate value 사용
7. 180 nm optical anchor를 STI depth로 사용하지 않음

### Gao electrical invariance gate

EMW 전:
- VBD
- SCR
- central/peripheral field
- breakdown location
- impact-ionization hotspot
을 Reference와 비교한다.

Pattern clipping 때문에 새로운 unintended PEB가 생기는지도 확인한다.

---

## 13. Reference → Gao literature validation

우리 primary optical observable:
- G(x,y,z)
- G_SCR_Int
- Reference-normalized G gain

PDP와 직접 동일시하지 않는다.

비교 hierarchy:
1. matching-condition local E/G literature result
2. G_SCR_Int는 simulation observable로만 사용
3. ATP를 이용해 Q = ∫G×ATP dV
4. compatible simulated PDP/Q spectral trend와 비교
5. measured PDP gain은 experimental context로만 사용

중요 limitation:
- P07/P10 spectrum은 940 nm를 포함하지만
- audited source에서 dedicated exact 940 nm Reference→FF15 gain table은 확인되지 않음

따라서:
> 프로젝트의 940 nm G_SCR_Int / Q / gain은 **새로운 simulation output**

으로 취급한다.

500 nm local G gain, broadband PDP average, 645 nm PDP peak gain 등을 940 nm G gain과 직접 비교하지 않는다.

---

## 14. Gao validation discrepancy가 있을 때

Annular로 바로 넘어가지 않고 다음 원인을 분리한다.

- full-cell geometry simplification
- native STI branch
- lattice origin / clipping
- BEOL treatment
- optical constants
- source/incidence condition
- polarization
- lateral/finite-domain boundary
- mesh
- SCR integration definition
- ATP map / reuse
- quasi-neutral collection
- finite aperture

원인과 영향범위를 기록한 뒤 Annular 진행 여부를 결정한다.

---

## 15. Annular 7-case 결정 유지

Codex re-audit은 기존 2D DOE 후보선정 자체를 무효화하지 않았다.

현재 3D validation set:
```text
200 / 215 / 750 / 775 / 835 / 900 / 1000 nm
```

역할:
- 200: global-worst negative control
- 215: low-pitch negative-control representative
- 750: positive/high-pitch regime control
- 775: integrated local peak
- 835: Gmax_SCR hotspot maximum
- 900: G_SCR_Int/Gain_Ref 2D global optimum
- 1000: upper-bound control

최종 3D 비교 구조:
1. Reference
2. Gao Square 480 nm / FF15
3. Annular 200
4. Annular 215
5. Annular 750
6. Annular 775
7. Annular 835
8. Annular 900
9. Annular 1000

모든 case:
```text
SDE → SDevice → SVisualPy → electrical PASS → EMW
```

---

## 16. 전체 실행 순서 Freeze

```text
1. SA-01~SA-12 Assumption Registry / Case Manifest
2. Frozen 2D reproduction + mesh audit
3. 3D simple extrusion sanity
4. Candidate A/B/C geometry-only SDE/SDevice
5. Active-STI split
6. STI5 branch split
7. Candidate B primary geometry freeze
8. Contact / STI depth / physics sensitivity
9. 3D Reference electrical gate
10. Reference 940 nm full-cell EMW
11. Gao Square 480 nm / FF15 full-cell
12. Gao electrical invariance
13. Reference→Square E/G/G_SCR_Int/ATP/Q
14. Compatible literature hierarchy validation
15. discrepancy analysis
16. Annular 7-case 3D
17. 각 annular case electrical gate
18. 동일 조건 3D EMW
19. 2D→3D regime/rank consistency
20. final annular design freeze
```

---

## 17. Final claim boundary

허용:
> 공개된 2017–2024 28 nm FD-SOI SPAD 연구계열과 frozen 2D electrical fingerprint를 함께 만족하도록 구성한 literature-constrained 3D surrogate Reference.

금지:
- ST foundry mask/recipe reproduction
- Gao 2024 exact GDS reconstruction
- 2D cylindrical geometry = actual full 3D geometry
- frozen STI/SCR coordinate = literature direct value
- measured PDP gain = simulated SCR photogeneration gain
- high-bias PDP gain = pure optical gain

---

## 18. 현재 다음 작업

문헌 재감사 Phase 1–6은 종료한다.

다음 작업:
> **3D Reference Assumption Registry / Case Manifest v1.0 작성**

그 후 Candidate B의 3D geometry specification을 작성하고, actual SDE coding으로 진행한다.

