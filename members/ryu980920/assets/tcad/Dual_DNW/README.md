# Dual_DNW

## 1. 목적

이 폴더는 CMP 28 nm FD-SOI SPAD **surrogate baseline reconstruction**에서 DNW profile을 재현하기 위한 현재 Dual-DNW calibration flow를 보관한다.

본 flow는 실제 ST foundry recipe를 복원하는 것이 아니다. 공개 문헌과 SDE baseline target을 기준으로, SProcess에서 전기적으로 동등한 target doping profile을 재현하기 위한 **surrogate process calibration**이다.

현재 단계는 최종 baseline freeze 이전의 profile calibration 단계이다.

---

## 2. Dual-DNW를 도입한 이유

기존 single-energy DNW 기반 250-point Large DOE를 분석한 결과, score/RMSE를 낮추는 방향과 SDE target의 물리적 profile shape을 재현하는 방향이 완전히 일치하지 않았다.

주요 확인 사항:

- DNW Dose 증가는 profile error를 줄이는 방향이었지만 DNW peak concentration을 높이고 profile을 더 좁게 만드는 경향이 있었다.
- 최저-score candidate에서도 DNW peak가 SDE target보다 높고, junction-side PActive가 부족했다.
- 250개 DOE 전체에서 DNW equivalent sigma의 최대값도 SDE target에 도달하지 못했다.
- 높은 thermal budget과 ramp 적용은 PW profile에는 영향을 주었지만 DNW width와 junction-side slope 개선은 제한적이었다.
- 따라서 현재 sampled range에서는 single-energy DNW의 main peak와 junction-side tail을 동시에 맞추기 어렵다고 판단하였다.

이 결과를 바탕으로 DNW를 두 개의 phosphorus implant로 분리하였다.

### Fixed/Main DNW

- Energy: `DNW_E`
- Dose fraction: `DNW_FIXED_FRAC = 1 - DNW_TRIM_FRAC`
- 역할: DNW main body와 약 1 um 부근의 main peak 형성

### Trim/Assist DNW

- Energy: `DNW_TRIM_E`
- Dose fraction: `DNW_TRIM_FRAC`
- 역할: shallow/junction-side phosphorus tail 보강 및 전체 DNW profile 폭 확장

총 DNW dose는 다음 관계를 유지한다.

```text
DNW_DOSE = DNW_FIXED_DOSE + DNW_TRIM_DOSE
```

두 DNW implant 사이에 별도 anneal은 없다. DNW, PW, NW implant 이후 **하나의 common WELL RTA**를 적용한다.

---

## 3. 현재 권장 SProcess 실행 구조

현재 DOE에서는 STI까지의 공통 공정을 매 experiment마다 반복하지 않는다.

```text
SProcess Stage 1
SOI definition
-> STI etch/fill
-> STI densification
-> restart-capable TDR 저장
          |
          v
SProcess Stage 2 x DOE cases
restart TDR load
-> Dual DNW
-> PW
-> NW
-> common WELL RTA
-> post-RTA PLX
-> local BOX removal
-> P+ implant
-> fixed spike
-> final PLX
          |
          v
SVisualPy profile screening
```

### Stage 1

파일:

```text
CMP_SPAD_DualDNW_SProcess_v0.2_Stage1_CommonSTISeed.txt
```

역할:

- SOI structure 생성
- native STI 형성
- STI densification
- 공통 post-STI 상태 저장

출력:

```text
n<node>_STI_RESTART_fps.tdr
```

저장 command:

```tcl
struct tdr=n@node@_STI_RESTART restart
```

`!restart`, `!Gas`, `!interfaces`는 사용하지 않는다.

Stage 1에는 DOE SWB Parameter가 없다. Workbench graph에서 Stage 1은 DOE branching 앞에서 **한 번만 실행**되어야 한다.

### Stage 2

파일:

```text
CMP_SPAD_DualDNW_SProcess_v0.2_Stage2_DOE_PLX_only.txt
```

Workbench dependency:

```tcl
#setdep @node|sprocess1@
```

Stage 1 seed를 다음 방식으로 읽는다.

```tcl
set SEED_NODE @node|sprocess1@
set SEED_TDR  n${SEED_NODE}_STI_RESTART_fps.tdr

if {![file exists $SEED_TDR]} {
   error "Required common STI restart TDR not found: $SEED_TDR"
}

init tdr=$SEED_TDR
```

Stage 2에는 다음 공정이 의도적으로 존재하지 않는다.

- `line clear`
- initial SOI `region` 생성
- `M_STI`
- STI etch
- STI oxide fill
- STI densification

따라서 Stage 2는 새 구조를 생성하지 않고 Stage 1에서 저장된 동일 post-STI state에서 바로 well implant를 시작한다.

---

## 4. 현재 SWB Parameter

Stage 2에서 사용하는 SWB Parameter는 다음 10개이다.

```text
DNW_DOSE
DNW_E
DNW_TRIM_E
DNW_TRIM_FRAC
PW_TRIM_E
PW_FIXED_E
PW_TRIM_FRAC
PW_TOTAL_DOSE
RTA_T
RTA_t
```

### DNW derived values

```tcl
set DNW_FIXED_FRAC [expr 1.0-$DNW_TRIM_FRAC]
set DNW_FIXED_DOSE [expr $DNW_DOSE*$DNW_FIXED_FRAC]
set DNW_TRIM_DOSE  [expr $DNW_DOSE*$DNW_TRIM_FRAC]
```

### PW derived values

`PW_FIXED_FRAC`는 SWB Parameter가 아니다.

```tcl
set PW_FIXED_FRAC [expr 1.0-$PW_TRIM_FRAC]
set PW_FIXED_DOSE [expr $PW_TOTAL_DOSE*$PW_FIXED_FRAC]
set PW_TRIM_DOSE  [expr $PW_TOTAL_DOSE*$PW_TRIM_FRAC]
```

따라서 DOE CSV에도 `PW_FIXED_FRAC`를 추가하지 않는다.

---

## 5. 현재 Dual-DNW calibration 설계

현재 structured calibration의 intended design은 다음과 같다.

### Sweep

```text
DNW_DOSE      = 2.60e13 / 2.80e13 / 3.00e13 cm^-2
DNW_E         = 935 / 955 keV
DNW_TRIM_E    = 650 / 750 keV
DNW_TRIM_FRAC = 0.15 / 0.25 / 0.35 / 0.45
PW_TRIM_FRAC  = 0.500 / 0.525
```

총 조합:

```text
3 x 2 x 2 x 4 x 2 = 96 cases
```

### 이번 calibration에서 고정

```text
PW_TRIM_E     = 85 keV
PW_FIXED_E    = 36 keV
PW_TOTAL_DOSE = 2.06e13 cm^-2
RTA_T         = 1050 C
RTA_t         = 30 s
```

위 DNW 범위는 **surrogate exploration range**이며 최종 공정값이 아니다.

현재 단계에서는 implant profile 자체의 영향을 분리하기 위해 common WELL RTA를 고정한다.

---

## 6. PLX 출력

Stage 2는 profile-first screening을 위해 TDR 대신 PLX를 중심으로 출력한다.

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

주 profile comparison 위치는:

```text
r = 4.6875 um
```

이다.

Dual-DNW calibration의 primary score는 **post-RTA `A_R_r4p6` profile**을 기준으로 계산한다. Final profile은 후속 P+ 및 spike 이후 변화 확인용으로 유지한다.

---

## 7. SVisualPy profile screening

파일:

```text
CMP_SPAD_DualDNW_ProfileScreening_SVisualPy_v0.1.py
```

SVisualPy는 SProcess PLX와 SDE surrogate baseline target을 비교한다.

상세 metric은 `n<node>_profile_metrics.txt`에 저장하고, SWB DOE table에는 다음 10개 핵심값만 표시한다.

| Output | 의미 | 목표 방향 |
|---|---|---|
| `SCORE` | 종합 profile matching score | 낮을수록 좋음 |
| `PW_RP` | PW interior main peak depth [nm] | 109.3 nm 부근 |
| `PW_PK_R` | PW peak / SDE PW peak | 1에 가까울수록 좋음 |
| `DNW_RP` | DNW main peak depth [nm] | 1017.3 nm 부근 |
| `DNW_PK_R` | DNW peak / SDE DNW peak | 1에 가까울수록 좋음 |
| `DNW_SIG` | DNW equivalent sigma [nm] | 380.6 nm 부근 |
| `JUNC` | PW/DNW metallurgical crossing [nm] | 462.7 nm 부근 |
| `P462_R` | SDE crossing 위치의 PActive / target | 1에 가까울수록 좋음 |
| `SLOPE_R` | DNW junction-side log slope / target | 1에 가까울수록 좋음 |
| `SPLIT` | two-lobe severity | 0에 가까울수록 좋음 |

### PW peak 처리

기존 extractor에서 PW surface point가 global maximum이면 `PW_RP = 0 nm`로 잡히는 문제가 있었다.

현재 script는 PW main peak를:

```text
30 nm <= depth <= 250 nm
```

범위에서 별도로 추출한다.

surface/global maximum은 상세 metric에 별도로 보존한다.

### Two-lobe detection

Dual-energy implant가 넓은 single profile이 아니라 두 개의 분리된 peak를 만들 수 있으므로 PW와 DNW 모두 second peak와 valley를 분석한다.

`SPLIT`은 second-peak strength와 valley depth를 함께 반영한 severity metric이다.

---

## 8. Composite SCORE

`SCORE`는 percent error가 아니다.

모든 component를 normalized penalty로 바꾼 뒤 가중합하여 계산한다.

현재 weight:

```text
PW
  PW Rp                5 %
  PW peak              4 %
  PW shape             6 %

DNW
  DNW Rp               8 %
  DNW peak             8 %
  DNW sigma           12 %
  DNW shape           17 %

Junction / Tail
  crossing            10 %
  PActive @ crossing  13 %
  junction slope      12 %

Split penalty          5 %
```

총합:

```text
100 %
```

따라서 SCORE가 낮을수록 전체 SDE target profile에 가까운 candidate라는 의미지만, **SCORE 하나만으로 최종 candidate를 결정하지 않는다.**

상위 candidate에서는 반드시 다음을 함께 확인한다.

- `DNW_SIG`
- `P462_R`
- `SLOPE_R`
- `SPLIT`
- `JUNC`
- 실제 PLX shape

---

## 9. SDE comparison targets

현재 SVisualPy에서 사용하는 target은 다음과 같다.

| Target | 값 | 분류 |
|---|---:|---|
| PW main peak depth | 109.3 nm | SDE baseline profile target |
| PW peak concentration | 5.95e17 cm^-3 | SDE baseline profile target |
| PW sigma | 200 nm | surrogate analytic target |
| DNW main peak depth | 1017.3 nm | SDE baseline profile target |
| DNW peak concentration | 3.15e17 cm^-3 | SDE baseline profile target |
| DNW sigma | 380.6 nm | SDE baseline profile target |
| PW/DNW crossing | 462.6966588 nm | analytic baseline crossing |

이 값들은 surrogate baseline calibration target이며 proprietary foundry process value로 해석하지 않는다.

또한 `BActive = PActive` metallurgical crossing은 SCR center와 동일하지 않다.

---

## 10. Candidate selection 이후 flow

Dual-DNW profile screening은 최종 electrical equivalence를 보장하지 않는다.

최종 flow는 다음과 같다.

```text
96-case Dual-DNW profile screening
        |
        v
top candidate group 선정
        |
        v
PW Fixed Energy fine tuning
        |
        v
PW Trim Energy / junction fine tuning
        |
        v
TDR-enabled SProcess rerun
        |
        v
SDevice verification
  - VBD
  - reverse I-V
  - V156 SCR position/width
  - electric field
  - avalanche / PEB-related behavior
        |
        v
true-FINE recheck
        |
        v
surrogate baseline freeze
```

최종 baseline freeze 전까지 profile score 최소 조건을 곧바로 최종 공정 조건으로 해석하지 않는다.

---

## 11. 현재 파일

```text
Dual_DNW/
├─ CMP_SPAD_DualDNW_SProcess_v0.2_Stage1_CommonSTISeed.txt
├─ CMP_SPAD_DualDNW_SProcess_v0.2_Stage2_DOE_PLX_only.txt
├─ CMP_SPAD_DualDNW_ProfileScreening_SVisualPy_v0.1.py
└─ README.md
```

이 폴더에서는 위 split/restart v0.2 SProcess flow를 현재 기준으로 사용한다.
