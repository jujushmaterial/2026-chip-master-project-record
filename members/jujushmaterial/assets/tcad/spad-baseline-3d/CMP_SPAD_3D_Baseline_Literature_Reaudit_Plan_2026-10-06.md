# CMP SPAD 3D Baseline Literature Re-audit Plan
## 2026-10-06 — Codex 논문 재분석 이후 3D Reference 재검토 계획

## 0. 문서 목적

이 문서는 현재까지 구축한 2D literature-constrained surrogate baseline과 2D annular EMW screening 결과를 유지하면서, **최종 3D Reference / Gao Square / Proposed Annular 비교를 시작하기 전에 기존 핵심 논문을 Codex로 처음부터 다시 분석하고, 그 결과를 근거로 3D baseline geometry를 재검토하기 위한 실행 계획**을 기록한다.

현재 단계에서는 3D Reference의 exact XY mask를 임의로 확정하거나, 비공개 geometry를 TCAD 결과에 맞추어 역산하지 않는다.

핵심 순서는 다음과 같다.

```text
기존 핵심 논문 full-text 재분석
    ↓
논문별 provenance MD 생성
    ↓
통합 literature constraint matrix 생성
    ↓
기존 2D frozen baseline과 재대조
    ↓
3D Reference surrogate XY geometry 재검토
    ↓
SDE 3D → SDevice/SVisualPy electrical validation
    ↓
Reference 3D EMW
    ↓
Gao Square 3D + electrical invariance + EMW validation
    ↓
문헌과 차이 분석
    ↓
Annular 7-case 3D
```

---

## 1. 현재 유지하는 연구 정체성

- 공통 baseline은 **Gao 2024의 28 nm FD-SOI quasi-circular reference SPAD 계열을 중심으로 앞선 동일 연구계열 논문으로 제약한 surrogate baseline**이다.
- 실제 STMicroelectronics foundry mask/process recipe를 복원한다고 주장하지 않는다.
- 2D baseline에서 이미 확보한 electrical/vertical fingerprint는 3D baseline을 재검토할 때의 기준점으로 유지한다.
- Reference에는 intentional periodic optical pattern이 없다.
- Gao Square는 baseline이 아니라 **선행 optical benchmark**이다.
- Proposed Annular는 동일 baseline core 위에서 FF=15%를 유지하며 radial pitch를 변화시키는 A의 구조이다.
- 2D EMW는 screening 결과이며 final optical claim은 3D EMW로만 한다.

---

## 2. 현재 frozen 2D surrogate baseline — 3D 재검토 기준

### 2.1 Electrical fingerprint

현재 GitHub에 동결된 2D surrogate baseline의 주요 target:

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
- 위 PeakVal은 implant dose가 아니라 SDE analytic Gaussian profile의 concentration parameter이다.
- 3D geometry를 만들면서 이 값들을 자동으로 재-fit하지 않는다.
- 3D에서 결과가 달라질 경우 먼저 3D lateral geometry, edge field, mesh, contact/domain 효과를 분석한다.

### 2.2 Vertical stack / existing surrogate cross-section

```text
Upper Si    = 0.007 µm
BOX         = 0.025 µm
STI depth   = 0.300 µm
active characteristic half-size = 12.5 µm

Representative 2D cross-section surrogate:
STI1 = 0.700–1.300 µm
STI2 = 2.975–3.275 µm
STI3 = 6.100–6.400 µm
STI4 = 9.225–9.525 µm
STI5 = 12.200–12.800 µm
```

주의:
- STI2/3/4/5의 위 좌표는 **기존 2D surrogate cross-section 위치**이다.
- 이것을 그대로 3D ring radius라고 해석하지 않는다.
- exact foundry mask dimension이라고 주장하지 않는다.
- 3D Reference는 기존 representative cut과 문헌의 pseudo/quasi-circular layout topology를 동시에 만족하는 surrogate로 정의한다.

---

## 3. 다음 작업의 최우선 단계 — Codex 논문 full-text 재분석

### 3.1 목적

기존 연구계획서의 문헌 요약을 그대로 재사용하는 것이 아니라, **우리가 지금까지 사용한 핵심 논문 원문 PDF를 Codex가 처음부터 끝까지 다시 읽고 구조/공정/전기/광학/TCAD 관련 근거를 새 MD로 재구축**한다.

특히 다음을 재검증한다.

- 3D top-view cell shape
- pseudo-circular / quasi-circular / octagonal 관계
- rectangular/staircase active layout 구현 방식
- PW / DNW / NW / BFMOAT / contact topology
- native STI1–7 역할과 위치 관계
- STI2/3/4 active-zone topology
- STI5 peripheral overlap/alignment 관계
- modified DNW identity
- 공개된 실제 치수와 비공개 치수
- VBD / SCR / field / DCR / ATP 관련 직접값
- optical pattern geometry와 FF 정의
- 2021/2024 optical simulation domain / boundary / source / metric
- 940 nm에서 직접 비교 가능한 수치의 존재 여부
- 그림의 scale 여부
- 논문별 구조가 서로 동일한 device인지, 역사적 다른 architecture인지

### 3.2 논문 inventory gate

사용자는 다음 단계에서 **“기존에 사용했던 핵심 논문 10편”**을 Codex로 다시 분석할 계획이다.

Codex 분석 시작 전에 반드시 실제 PDF inventory를 기준으로 10편의 정확한 목록을 먼저 확정한다.

현재 `SPAD_연구계획서.md`의 bibliography에는:
- 학술 논문/학회 논문 9편
- Synopsys EMW User Guide 1편
- 제품/CES 자료

가 분리되어 있으므로, 사용자가 말한 “10개 논문”과 현재 bibliography numbering이 정확히 일치하는지 **분석 전에 확인**한다.

절대 하지 않을 것:
- EMW manual을 임의로 10번째 “논문”으로 간주
- 파일 제목만 보고 중복/다른 논문을 합치기
- 현재 기억만으로 10편 목록을 확정

### 3.3 논문별 MD 산출물

각 논문마다 별도 MD를 생성하고 최소 다음 항목을 포함한다.

```text
1. 서지정보
2. 연구 목적
3. 사용 device / fabrication generation
4. 구조 topology
5. 공개된 geometry 수치
6. 비공개 geometry
7. process / doping 정보
8. electrical simulation methodology
9. optical simulation methodology
10. measurement methodology
11. VBD / SCR / E-field / DCR / ATP / PDP 값
12. 본 CMP baseline에 직접 사용할 수 있는 정보
13. 동일 연구계열 constraint로만 사용할 정보
14. 현재 baseline에 사용하면 안 되는 정보
15. figure/table별 핵심 내용
16. scale respected 여부
17. 구조 간 역사적 관계
18. 현재 연구계획과 충돌하는 내용
19. 불확실성 / 미공개 항목
20. 원문 인용 위치/page/figure/table
```

모든 수치는 다음 provenance 중 하나로 분류한다.

- [직접 실측]
- [논문 직접 시뮬레이션]
- [동일 연구계열 constraint]
- [그림 판독 추정]
- [역산/fit]
- [surrogate assumption]
- [system scenario assumption]

Codex는 논문에 없는 숫자를 채우지 않는다.

---

## 4. Codex 재분석 후 통합 MD

논문별 분석이 끝나면 별도의 통합 문서를 만든다.

권장 파일:
```text
SPAD_Literature_Constraint_Matrix_Codex_Reaudit.md
```

통합표에는 최소 다음 행을 둔다.

| Category | Parameter | Paper | Direct value | Device generation | Provenance | Can use for 2024 baseline? | Notes |
|---|---|---|---|---|---|---|---|
| Geometry | cell diameter | ... | ... | ... | ... | ... | ... |
| Geometry | top-view shape | ... | ... | ... | ... | ... | ... |
| STI | active STI2/3/4 | ... | ... | ... | ... | ... | ... |
| STI | peripheral STI5 | ... | ... | ... | ... | ... | ... |
| Stack | upper Si | ... | ... | ... | ... | ... | ... |
| Stack | BOX | ... | ... | ... | ... | ... | ... |
| Electrical | VBD | ... | ... | ... | ... | ... | ... |
| Electrical | SCR | ... | ... | ... | ... | ... | ... |
| Optical | grating/SCR anchor | ... | ... | ... | ... | ... | ... |
| Optical | square pitch/FF | ... | ... | ... | ... | ... | ... |

별도로 **conflict log**를 둔다.

예:
- old baseline assumption
- newly re-read evidence
- conflict
- effect on SDE/SDevice/EMW
- decision required

새 근거가 기존 baseline과 충돌하면 자동 수정하지 않는다.

---

## 5. 3D Reference baseline 재검토 원칙

### 5.1 가장 중요한 원칙

3D Reference는:

> **기존 frozen 2D surrogate baseline의 vertical/electrical fingerprint를 유지하면서, Codex 재분석으로 확인된 동일 연구계열의 non-axisymmetric pseudo/quasi-circular lateral topology를 반영한 3D literature-constrained surrogate**

로 정의한다.

### 5.2 금지

다음 방식으로 3D baseline을 만들지 않는다.

- 2D half-cell을 단순 회전하여 exact circular SPAD로 생성
- STI2/3/4/5를 concentric ring으로 자동 변환
- STI 위치를 자유변수로 sweep하여 VBD≈15.8 V가 되는 geometry를 역으로 선택
- geometry와 doping을 동시에 자유롭게 fit
- 논문 layout 그림 pixel 길이를 그대로 nm/µm로 선언
- 3D에서 VBD가 달라졌다는 이유만으로 PW/DNW doping을 즉시 재-fit
- 2022 all-optimized circular 구조를 2024 Reference로 대체

### 5.3 surrogate XY geometry가 여전히 비공개일 경우

Codex full-text 재분석 후에도 exact mask coordinates가 공개되지 않았다면:

1. 논문에서 확정된 topology를 먼저 고정한다.
2. 기존 2D representative cut을 보존한다.
3. 25 µm-class pseudo/quasi-circular footprint를 보존한다.
4. 2–3개의 **plausible surrogate XY mask 후보**를 정의할 수 있다.
5. 각 좌표는 반드시 [그림 판독 추정] 또는 [surrogate assumption]으로 라벨링한다.
6. 후보 선택을 위한 TCAD split은 허용하되, 목적은 **VBD를 맞추는 inverse fitting이 아니라 electrical fingerprint robustness 확인**이다.

즉 split의 질문은:

> “어떤 임의 geometry가 15.8 V를 만드는가?”

가 아니라:

> “문헌과 기존 2D surrogate를 모두 만족하는 plausible 3D mask들 중 어느 realization이 기존 electrical fingerprint를 가장 안정적으로 보존하는가?”

이다.

---

## 6. 3D Reference electrical validation

3D SDE 생성 후 EMW로 바로 가지 않는다.

먼저:

```text
3D SDE
  ↓
SDevice
  ↓
SVisualPy
```

로 다음을 확인한다.

- reverse I–V
- VBD
- SCR p-side
- SCR n-side
- SCR center
- SCR width
- center electric field
- peripheral electric field
- breakdown onset location
- impact-ionization / avalanche location
- contact/domain artifact
- mesh convergence

### tolerance

현재 단계에서 ±1%, ±x nm 같은 tolerance를 임의로 정하지 않는다.

먼저:
- 3D mesh convergence
- repeated extraction stability
- 2D vs 3D dimensional effect

를 확인한 뒤 acceptance tolerance를 freeze한다.

---

## 7. 3D Reference EMW

Electrical validation PASS 후 Reference에 대해 940 nm 3D EMW를 수행한다.

Reference:
- intentional periodic optical pattern 없음
- FF/pitch 정의하지 않음
- native STI topology 유지

추출:
- G(x,y,z)
- SCR-integrated photogeneration
- active-region integrated photogeneration
- reflection / transmission 가능 시 저장
- normalization metadata
- optical material data provenance
- mesh convergence

이 결과가 모든 이후 optical gain의 denominator가 된다.

---

## 8. Gao Square 3D benchmark

Reference PASS 후 동일 core를 복제하여 Gao Square를 생성한다.

고정 published geometry:
```text
pitch = 480 nm
FF = 15%
Si square = 186 × 186 nm²
STI separation = 294 nm
```

중요:
- Gao Square 또한 full SPAD level에서는 원형대칭 구조가 아니다.
- Reference electrical/native-STI core를 유지하고 intentional square optical pattern만 추가한다.
- 동일 3D domain, material, source, normalization, mesh rule을 사용한다.

### electrical invariance gate

Gao Square에서도 EMW 전에:

- VBD
- SCR center / width / boundaries
- E-field
- breakdown location

을 확인한다.

Optical pattern을 넣은 뒤 electrical fingerprint가 의미 있게 변했다면 원인을 분석한다.

---

## 9. Gao literature validation gate

Gao Square 3D EMW 후 바로 Annular로 넘어가지 않는다.

우선:

```text
Reference 3D EMW
vs
Gao Square 3D EMW
```

의 gain을 계산하고, Codex가 다시 정리한 2021/2024 논문의 compatible optical result와 비교한다.

### 중요한 metric 구분

우리의 주요 optical metric:
```text
SCR-integrated photogeneration
Reference-normalized G gain
```

논문의 measured PDP gain과는 동일 quantity가 아니다.

따라서:
- 논문 direct optical simulation quantity가 있으면 우선 비교
- PDP simulation은 methodology 차이를 확인하고 비교
- measured PDP gain은 secondary benchmark
- photogeneration gain = measured PDP gain이라고 등치하지 않음

### 차이가 큰 경우 확인

- geometry simplification
- native STI representation
- BEOL handling
- optical constants
- normal incidence
- lateral boundary
- domain size
- mesh
- SCR/active-region integration definition
- ATP coupling 여부
- quasi-neutral carrier collection
- polarization
- finite aperture

원인을 기록한 뒤 다음으로 진행한다.

---

## 10. Annular 7-case 3D validation

Reference/Gao validation 이후에만 진행한다.

현재 확정 case:

```text
200 / 215 / 750 / 775 / 835 / 900 / 1000 nm
```

역할:
- 200 nm: 2D global-worst negative control
- 215 nm: low-pitch bottom-regime control
- 750 nm: positive/high-pitch control
- 775 nm: integrated local peak
- 835 nm: Gmax_SCR hotspot optimum
- 900 nm: G_SCR_Int / Gain_Ref 2D global optimum
- 1000 nm: upper-bound control

모든 case:
- global Si pattern FF = 15%
- radial pitch만 independent variable
- ring width는 FF를 유지하는 dependent variable
- STI depth 고정
- baseline electrical/native-STI core 고정

### 모든 구조의 electrical check

Annular 각 case에서도:

```text
SDE → SDevice → SVisualPy → PASS → EMW
```

순서로 진행한다.

즉 총 비교 구조:
1. Reference
2. Gao Square
3–9. Annular 7 cases

모든 구조에서 VBD와 SCR이 의도치 않게 바뀌지 않았는지 기록한다.

---

## 11. 2D → 3D 검증의 해석 원칙

3D에서 2D와 exact ranking이 동일해야 하는 것은 아니다.

주요 검증 질문:

- 200/215 nm low-pitch negative-control regime이 3D에서도 상대적으로 불리한가?
- 835/900 nm high-performance regime이 3D에서도 상대적으로 유리한가?
- 2D screening이 후보군 selection에 유효했는가?
- 3D에서 optimum이 이동한다면 그 이유가 무엇인가?

최종 annular design은 3D EMW 결과로 결정한다.

---

## 12. 현재 작업 상태와 hold point

### 완료
- 2D surrogate baseline electrical freeze
- Reference 2D optical freeze
- 160-case annular 2D radial-pitch DOE
- 3D validation annular 7-case selection

### 현재 hold
- 3D Reference exact XY mask 확정
- 3D SDE code 작성
- Gao full-SPAD 3D code 작성

### hold 이유
기존 10개 핵심 논문을 Codex로 다시 full-text 분석하고, 새 provenance MD를 만든 후 3D geometry를 다시 검토하기로 결정함.

즉 현재 단계에서 기존 기억/요약만으로 3D baseline geometry를 확정하지 않는다.

---

## 13. Codex 작업 이후 재개 조건

다음 산출물이 준비되면 3D baseline 검토를 재개한다.

- [ ] 핵심 논문 10편 exact inventory
- [ ] 논문별 full-text analysis MD
- [ ] figure/table provenance 포함
- [ ] Literature Constraint Matrix
- [ ] conflict log
- [ ] 3D geometry에 사용 가능한 direct / constraint / unknown 항목 목록
- [ ] 기존 2D surrogate baseline과의 difference report

이후 ChatGPT/Codex 분석을 합쳐:
1. 3D Reference geometry specification 작성
2. 필요 시 surrogate mask A/B/C 생성
3. SDE 3D 구현
4. SDevice/SVisualPy validation
5. EMW validation

순서로 진행한다.

---

## 14. 최종 결정 요약

1. **현재 3D baseline 코딩을 잠시 중단한다.**
2. **기존 핵심 논문 10편을 Codex로 처음부터 다시 분석한다.**
3. 분석 결과는 새 MD 파일로 source/provenance 중심으로 기록한다.
4. 그 MD를 기준으로 기존 2D surrogate baseline을 다시 검토한다.
5. exact 3D lateral geometry가 계속 비공개이면 명시적 surrogate 후보를 정의한다.
6. TCAD split은 VBD/SCR target inverse-fit용이 아니라 plausible geometry의 robustness/electrical consistency 검증용으로 사용한다.
7. Reference 3D electrical PASS 후 EMW를 수행한다.
8. Gao Square 3D에서 electrical invariance와 optical literature validation을 수행한다.
9. Gao validation과 discrepancy analysis를 통과한 후에만 Annular 7 cases를 진행한다.
10. 모든 9개 최종 구조에서 SDevice/SVisualPy로 VBD/SCR invariance를 확인한 뒤 EMW 비교를 수행한다.

