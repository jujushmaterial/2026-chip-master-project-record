# Triple_DNW

## 1. 목적

이 폴더는 CMP 28 nm FD-SOI SPAD **surrogate baseline reconstruction** 과정에서 DNW deep-side doping profile을 보강하기 위한 **Triple-DNW calibration flow**를 보관한다.

본 flow는 실제 ST foundry recipe를 복원하는 것이 아니다. SDE 공통 baseline의 PW/DNW active doping profile을 제약조건으로 사용하는 **surrogate process calibration**이며, 최종 SDevice electrical validation 및 baseline freeze 이전의 **profile-screening 단계**이다.

---

## 2. Triple-DNW를 도입한 이유

기존 Dual-DNW refinement 108개 조건을 비교한 결과, 우수 후보인 n72/n124 등은 약 1 µm 부근 DNW main peak를 비교적 잘 재현했으나, **1.4–1.8 µm의 deep-side PActive tail**이 SDE target보다 부족하였다.

Main DNW Energy를 높이면 깊은 영역의 농도가 일부 증가하지만, 이미 정합한 main peak 위치도 함께 움직일 수 있다. 따라서 main peak와 deep tail을 서로 더 독립적으로 제어할 추가 implant component가 필요했다.

Triple-DNW는 phosphorus implant를 다음 세 성분으로 나눈다.

### Main DNW

- Energy: `DNW_E`
- Dose fraction: `DNW_MAIN_FRAC = 1 - DNW_TRIM_FRAC - DNW_DEEP_FRAC`
- 역할: 약 1 µm 부근 DNW main peak 및 profile body 형성

### Trim/Assist DNW

- Energy: `DNW_TRIM_E`
- Dose fraction: `DNW_TRIM_FRAC`
- 역할: shallow/junction-side phosphorus contribution 보강

### Deep DNW

- Energy: `DNW_DEEP_E`
- Dose fraction: `DNW_DEEP_FRAC`
- 역할: 1.4–1.8 µm 부근 deep-side phosphorus tail 보강

총 DNW dose는 다음과 같이 유지한다.

```text
DNW_DOSE = DNW_MAIN_DOSE + DNW_TRIM_DOSE + DNW_DEEP_DOSE
```

각 DNW component 사이에는 별도 anneal을 두지 않는다. DNW 3개 component, PW 및 NW implant 후 **하나의 common WELL RTA**를 사용한다.

---

## 3. 현재 SProcess 실행 구조

Dual-DNW와 마찬가지로 공통 SOI/STI 형성은 Stage 1에서 한 번 수행하고, Stage 2를 각 DOE experiment에서 실행한다.

```text
SProcess Stage 1 (Dual_DNW와 공통)
SOI definition
-> native STI etch/fill
-> STI densification
-> restart-capable TDR 저장
          |
          v
SProcess Stage 2 x DOE cases
restart TDR load
-> Main + Trim + Deep DNW
-> PW
-> NW
-> common WELL RTA
-> post-RTA PLX
-> local UpperSi/BOX removal
-> P+ contact implants
-> fixed spike
-> final PLX
          |
          v
SVisualPy v0.4 profile screening
```

### Stage 1

공통으로 재사용하는 파일:

```text
../Dual_DNW/CMP_SPAD_DualDNW_SProcess_v0.2_Stage1_CommonSTISeed.txt
```

역할:

- SOI 및 reference native STI structure 생성
- STI densification
- 후속 DOE가 공유하는 post-STI restart TDR 저장

출력:

```text
n<node>_STI_RESTART_fps.tdr
```

Stage 1은 DOE branching 앞에서 한 번만 수행한다. 이 폴더에는 동일한 Stage 1 복사본을 따로 보관하지 않는다.

### Stage 2

파일:

```text
CMP_SPAD_TripleDNW_SProcess_v0.3_Stage2_DOE_PLX_only_RECONSTRUCTED.txt
```

Workbench dependency:

```tcl
#setdep @node|sprocess1@
```

Stage 1의 `n@node|sprocess1@_STI_RESTART_fps.tdr`를 확인한 뒤 `init tdr`로 읽는다. Stage 2에는 SOI region 생성, STI etch/fill 및 STI densification을 다시 넣지 않는다.

이 파일은 **과거 대화에서 작성했던 Stage 2 command를 재구성한 버전**이다. 과거 실행 파일과 바이트 단위로 동일한 원본임이 검증된 것은 아니므로 `RECONSTRUCTED` 표기를 유지한다.

---

## 4. 현재 SWB Parameter

첨부된 Stage 2 command에서 `@PARAMETER@` 형식으로 입력받는 항목은 다음 12개다.

```text
DNW_DOSE
DNW_E
DNW_TRIM_E
DNW_DEEP_E
DNW_TRIM_FRAC
DNW_DEEP_FRAC
PW_TRIM_E
PW_FIXED_E
PW_TRIM_FRAC
PW_TOTAL_DOSE
RTA_T
RTA_t
```

### DNW derived values

```tcl
set DNW_MAIN_FRAC [expr 1.0-$DNW_TRIM_FRAC-$DNW_DEEP_FRAC]
set DNW_MAIN_DOSE [expr $DNW_DOSE*$DNW_MAIN_FRAC]
set DNW_TRIM_DOSE [expr $DNW_DOSE*$DNW_TRIM_FRAC]
set DNW_DEEP_DOSE [expr $DNW_DOSE*$DNW_DEEP_FRAC]
```

따라서 `DNW_MAIN_FRAC`은 두 분율에 의해 결정되는 종속변수다.

### PW derived values

첨부 Stage 2 command는 다음과 같이 계산한다.

```tcl
set PW_FIXED_FRAC [expr 1.0-$PW_TRIM_FRAC]
set PW_FIXED_DOSE [expr $PW_TOTAL_DOSE*$PW_FIXED_FRAC]
set PW_TRIM_DOSE [expr $PW_TOTAL_DOSE*$PW_TRIM_FRAC]
```

**SWB 주의:** 위 목록은 현재 파일에서 참조하는 `@...@` 변수 목록이다. 실제 Workbench에 `PW_FIXED_FRAC`까지 등록되어 있는 구성이라면, 현재 command의 derived 처리와 SWB 등록 변수 간 정합을 별도로 확인해야 한다. SWB에 등록된 값은 sweep 여부와 관계없이 숫자로 hard-code해서는 안 된다.

---

## 5. Triple-DNW calibration 설계

### 첫 Triple-DNW DOE

Dual-DNW의 deep-tail 부족을 해결하기 위해 Deep DNW component를 추가한 탐색이다.

```text
DNW_DEEP_E = 1300 / 1400 / 1500 / 1600 / 1700 keV
DNW_DOSE   = 2.50e13 ~ 2.90e13 cm^-2 (9 levels)
```

총 조합:

```text
5 x 9 = 45 cases
```

첫 DOE에서는 Main absolute dose `1.80e13 cm^-2`와 Trim absolute dose `6.00e12 cm^-2`를 유지하면서 Deep absolute dose를 추가하는 방식으로 설계하였다. 실제 확보했던 결과 CSV는 23 + 22 = 45개 행이었다.

### 후속 Main-to-Deep fine DOE

첫 DOE 분석 후, Deep Energy와 Main/Deep dose 분배 효과를 좁은 범위에서 분리해 확인하도록 설계한 25개 조건이다.

```text
DNW_DEEP_E    = 1500 / 1525 / 1550 / 1575 / 1600 keV
DNW_DEEP_FRAC = 0.172413793 / 0.189655172 / 0.206896552
                / 0.224137931 / 0.241379310
```

총 조합:

```text
5 x 5 = 25 cases
```

이 단계에서는 총 DNW dose와 Trim absolute dose를 고정하고, **Main contribution 일부를 Deep contribution으로 재분배**하도록 설계하였다.

공통 고정조건(해당 DOE의 SWB experiment row 값):

```text
DNW_DOSE      = 2.90e13 cm^-2
DNW_E         = 975 keV
DNW_TRIM_E    = 550 keV
DNW_TRIM_FRAC = 0.206896552

PW_TRIM_E     = 85 keV
PW_FIXED_E    = 36 keV
PW_TRIM_FRAC  = 0.525
PW_TOTAL_DOSE = 2.06e13 cm^-2

RTA_T         = 1050 C
RTA_t         = 30 s
```

이는 **DOE 설계 조건**이며, 이 폴더의 두 코드 파일만으로 25-case 실행 완료 또는 성능 개선을 입증한 것은 아니다.

---

## 6. PLX 출력

Stage 2는 profile screening을 위해 PLX를 생성한다.

### Before common WELL RTA

```text
n@node@_B_R_r0.plx
n@node@_B_R_r4p6.plx
n@node@_B_R_r13.plx
```

### After common WELL RTA

```text
n@node@_A_R_r0.plx
n@node@_A_R_r4p6.plx
n@node@_A_R_r13.plx
```

### Final process

```text
n@node@_F_r0.plx
n@node@_F_r4p6.plx
n@node@_F_r13.plx
```

중앙 active-region의 주 비교 cut은 `r = 4.6875 µm`이다.

Primary SCORE와 DOE summary는 **post-RTA `A_R_r4p6` profile**을 기준으로 계산한다. Final `F_r4p6`는 local etch/P+ implant/fixed spike 이후 변화를 확인하는 데 사용한다.

본 Stage 2 파일은 PLX-only 버전이다. SDevice용 final TDR을 생성하지 않으므로 후속 electrical verification에서는 TDR-enabled flow가 별도로 필요하다.

---

## 7. SVisualPy profile screening

파일:

```text
CMP_SPAD_TripleDNW_ProfileScreening_SVisualPy_v0.4_DeepTail.md
```

Markdown 파일 내부의 `python` 코드 블록에 SVisualPy 코드가 보존되어 있다. 실제 실행에는 코드 블록 내용이 SVisualPy script로 사용되어야 한다.

기존 Dual-DNW v0.3과 동일한 PW/DNW profile-matching SCORE 계산을 유지하면서, deep-tail 비교에 필요한 진단 지표 네 개를 추가하였다.

### PLX paired-variable compatibility

기존 v0.3 loader와 동일하게 다음 형태를 모두 처리한다.

```text
X / BActive / PActive
```

또는 curve별 paired layout:

```text
BActive x
BActive y
PActive x
PActive y
```

PW/DNW profile의 좌표 grid가 서로 다르면 overlap 구간에서 공통 grid로 정렬한다.

### SWB DOE 출력

| Output | 의미 | 목표 방향 |
|---|---|---|
| `SCORE` | 종합 profile matching score | 낮을수록 좋음 |
| `PW_RP` | PW interior main peak depth [nm] | 109.3 nm 부근 |
| `PW_PK_R` | PW peak / SDE target PW peak | 1에 가까울수록 좋음 |
| `DNW_RP` | DNW main peak depth [nm] | 1017.3 nm 부근 |
| `DNW_PK_R` | DNW peak / SDE target DNW peak | 1에 가까울수록 좋음 |
| `DNW_SIG` | DNW equivalent sigma [nm] | 380.6 nm 부근 |
| `JUNC` | BActive=PActive metallurgical crossing [nm] | 462.7 nm 부근 |
| `P462_R` | SDE crossing depth의 PActive / target | 1에 가까울수록 좋음 |
| `SLOPE_R` | DNW junction-side log slope / target | 1에 가까울수록 좋음 |
| `SPLIT` | secondary-peak / valley 기반 two-lobe severity | 0에 가까울수록 좋음 |
| `TAIL14_R` | 1.4 µm의 PActive / analytic target | 1에 가까울수록 좋음 |
| `TAIL16_R` | 1.6 µm의 PActive / analytic target | 1에 가까울수록 좋음 |
| `TAIL18_R` | 1.8 µm의 PActive / analytic target | 1에 가까울수록 좋음 |
| `TAIL_RMSE` | 1.2–1.8 µm 구간 deep-tail log RMSE | 낮을수록 좋음 |

상세 metric과 비교 profile은 다음 파일로 출력한다.

```text
n<node>_profile_metrics.txt
n<node>_profile_AR_compare.csv
n<node>_profile_F_compare.csv
```

### PW peak 처리 및 Two-lobe detection

- PW main peak는 `30–250 nm` 범위에서 추출한다. Surface/global maximum은 별도의 상세 metric으로 유지한다.
- PW와 DNW 모두 secondary peak와 valley를 분석해 split severity를 계산한다.
- `TAIL14_R`, `TAIL16_R`, `TAIL18_R`, `TAIL_RMSE`는 **진단용**으로 추가되었으며 기존 `SCORE` 가중합에는 포함되지 않는다.

---

## 8. Composite SCORE

Triple-DNW v0.4의 Composite SCORE 가중치와 산식은 Dual-DNW v0.3과 동일하다.

`SCORE`는 percent error가 아니라 정규화된 profile mismatch penalty의 가중합이다.

```text
PW
  PW Rp                 5 %
  PW peak               4 %
  PW shape              6 %

DNW
  DNW Rp                8 %
  DNW peak              8 %
  DNW sigma            12 %
  DNW shape            17 %

Junction / Tail
  crossing             10 %
  PActive @ crossing   13 %
  junction slope       12 %

Split penalty           5 %

Total                 100 %
```

SCORE가 낮더라도 main peak, sigma, metallurgical crossing 및 deep-tail ratio가 함께 정합하는지는 별도로 확인해야 한다.

따라서 candidate는 `SCORE`, `DNW_RP`, `DNW_PK_R`, `DNW_SIG`, `JUNC`, `P462_R`, `SLOPE_R`, `SPLIT`, `TAIL14_R`, `TAIL16_R`, `TAIL18_R`, `TAIL_RMSE`와 PLX 형상을 함께 평가한다.

---

## 9. SDE comparison targets

현재 v0.4 SVisualPy에 실제로 지정된 기준값이다.

| Target | 값 | 분류 |
|---|---:|---|
| PW main peak depth | 109.3 nm | SDE baseline profile anchor |
| PW peak concentration | 5.954e17 cm^-3 | SDE baseline profile anchor |
| PW sigma | 200 nm | surrogate analytic target |
| DNW main peak depth | 1017.3 nm | SDE baseline profile anchor |
| DNW peak concentration | 3.147e17 cm^-3 | SDE baseline profile anchor |
| DNW sigma | 380.6 nm | surrogate analytic target/profile constraint |
| PW/DNW crossing depth | 462.6966588 nm | SDE baseline crossing anchor |
| crossing concentration | 1.159e17 cm^-3 | SDE baseline extracted anchor |

**v0.4 기준의 차이를 구분해야 한다.**

- `PW_PK_R`, `DNW_PK_R`, `P462_R`의 분모는 코드에 지정된 SDE 기준 peak/crossing 농도다.
- PW/DNW **shape reference, junction-side slope reference 및 deep-tail reference는 analytic Gaussian**으로 구성되어 있다.
- 따라서 deep-tail 진단값을 실제 full SDE PLX 전체에 직접 적합한 결과로 해석하지 않는다.
- `BActive=PActive` metallurgical crossing은 **SCR center가 아니다.**

모든 수치는 공개 문헌의 실제 제조 recipe가 아니라 프로젝트의 surrogate baseline calibration target으로 사용한다.

---

## 10. Candidate selection 이후 flow

Triple-DNW profile-screening에서 우수한 조건을 찾았다고 해서 electrical baseline을 확보한 것은 아니다.

```text
Triple-DNW profile DOE
       |
       v
SCORE + peak / sigma / junction / deep-tail comparison
       |
       v
top candidate group 선정
       |
       v
PW Energy 보정으로 junction/SCR 위치 정합 시도
       |
       v
TDR-enabled SProcess 재실행
       |
       v
SNMesh -> SDevice
  - VBD
  - reverse I-V
  - SCR position / width
  - central / peripheral electric field
  - avalanche / PEB-related behavior
       |
       v
mesh / temperature sensitivity 검토
       |
       v
surrogate baseline freeze 여부 판단
```

SCR 위치와 electrical characteristics 검증 없이 profile score 최소 조건을 최종 baseline으로 확정하지 않는다. ATP, dark-current, PEB 및 온도 안정성의 본격적인 개선 평가는 baseline freeze와 구분한다.

---

## 11. 현재 파일

```text
Triple_DNW/
├─ CMP_SPAD_TripleDNW_SProcess_v0.3_Stage2_DOE_PLX_only_RECONSTRUCTED.txt
├─ CMP_SPAD_TripleDNW_ProfileScreening_SVisualPy_v0.4_DeepTail.md
└─ README.md
```

- **SProcess v0.3:** Stage 1 공통 STI restart부터 Main/Trim/Deep DNW implant, 공통 WELL RTA, final PLX 출력까지 수행하는 **재구성 Stage 2** command이다. 정확한 과거 실행 원본임을 확인한 파일은 아니다.
- **SVisualPy v0.4:** 기존 Dual-DNW `SCORE` 계산 방식은 유지하고 deep-tail 진단 기능만 추가한 profile-screening script이다. 현재 파일 형식은 `.md`이며 실행 코드가 Markdown 코드 블록 안에 있다.
- 공통 Stage 1은 `../Dual_DNW/`에 보관한다. 본 폴더에는 위 **두 파일과 README만** 관리한다.
