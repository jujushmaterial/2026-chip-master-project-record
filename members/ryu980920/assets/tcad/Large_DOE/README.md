# Large_DOE

CMP SPAD B-track의 **surrogate baseline doping-profile calibration을 위한 대규모 SProcess DOE** 작업 폴더이다.

현재 단계의 목적은 SDevice의 VBD/SCR을 먼저 맞추는 것이 아니라, SDE에서 정의한 baseline PW/DNW active doping profile을 SProcess에서 가능한 한 가깝게 재현할 수 있는 process region을 찾는 것이다. Profile screening으로 후보를 줄인 뒤, 선별된 후보만 SDevice에서 VBD 및 V156 SCR을 검증한다.

## Files

### `CMP_SPAD_BaselineImplementation_SProcess_v0.14_PLX_only_noTDR_nocomments.txt`

대규모 profile DOE를 위한 경량 SProcess command.

- 중간/final TDR 저장 명령을 제거하여 대규모 sweep 시 storage와 I/O를 줄였다.
- profile 비교용 PLX는 유지한다.
  - `B_R_r4p6`: common WELL RTA 전
  - `A_R_r4p6`: common WELL RTA 후
  - `F_r4p6`: final P+ implant 및 fixed spike 후
- 동일 진단을 위해 r=0, r=4.6875 um, r=13 um PLX를 출력한다.
- baseline profile의 주 비교 cut은 r=4.6875 um이다.
- DNW와 PW는 하나의 common WELL RTA를 공유한다.
- 별도 DNW/PW anneal은 사용하지 않는다.
- 이 버전은 TDR을 출력하지 않으므로 그대로 SDevice downstream input으로 사용할 수 없다. Profile 후보 선정 후 TDR-enabled verification flow로 다시 실행해야 한다.

### PW fraction handling

`PW_TRIM_FRAC`만 SWB parameter로 받고,

```tcl
set PW_FIXED_FRAC [expr 1.0-$PW_TRIM_FRAC]
```

으로 자동 계산한다.

따라서 `PW_FIXED_FRAC`은 독립 SWB parameter가 아니다.

현재 SProcess command에서 사용하는 SWB parameters:

- `DNW_DOSE`
- `DNW_E`
- `PW_TRIM_E`
- `PW_FIXED_E`
- `PW_TRIM_FRAC`
- `PW_TOTAL_DOSE`
- `RTA_T`
- `RTA_t`

## `CMP_SPAD_ProfileScreening_SVisualPy_v1.0.py`

SProcess PLX를 읽어 SDE baseline target과 profile을 자동 비교하기 위한 SVisualPy script.

기본 입력:

- `n{sprocess_node}_A_R_r4p6.plx` : post-RTA profile
- `n{sprocess_node}_F_r4p6.plx` : final profile

주요 추출 항목:

### PW

- peak depth
- peak concentration
- bulk-side half-width/FWHM-related metric
- second-peak ratio
- 100/200/250/300/400/450/500 nm concentration
- integrated active dose
- full-profile log RMSE
- normalized shape log RMSE

### DNW

- peak depth
- peak concentration
- FWHM
- left/right half-max position
- equivalent sigma
- 600/800/1000/1200/1400 nm concentration
- integrated active dose
- full-profile log RMSE
- normalized shape log RMSE

### Joint PW/DNW

- BActive=PActive metallurgical crossing
- target 대비 peak/crossing/sigma error
- post-RTA와 final profile 변화

출력 파일:

- `n*_profile_metrics.txt`
- `n*_profile_AR_compare.csv`
- `n*_profile_F_compare.csv`

SVisual 내에서 SProcess BActive/PActive와 SDE target curve를 overlay하도록 구성되어 있다.

## Current SDE target used by SVisualPy

현재 script에 들어간 profile target은 현재 SDE baseline profile에서 추출해 사용하는 project calibration target이다.

- PW peak depth: 109.3 nm
- PW peak concentration: 5.95e17 cm^-3
- PW sigma: 200 nm
- DNW peak depth: 1017.3 nm
- DNW peak concentration: 3.15e17 cm^-3
- DNW sigma: 380.6 nm

이 값들은 foundry implant recipe가 아니라 SDE baseline active-profile matching target으로 사용한다.

## Recommended flow

1. SWB에서 SProcess DOE를 실행한다.
2. 각 case에서 PLX만 저장한다.
3. SVisualPy로 PW/DNW profile metrics와 SDE 대비 error를 자동 추출한다.
4. peak/Rp/width/tail/crossing/full-profile error를 함께 보고 후보를 선별한다.
5. 상위 profile 후보만 TDR-enabled SProcess flow로 재실행한다.
6. SDevice에서 VBD≈15.8 V 및 V156 SCR≈baseline을 검증한다.
7. profile과 electrical equivalence를 함께 만족하는 surrogate baseline candidate를 freeze한다.

## Important interpretation notes

- metallurgical junction(BActive=PActive)은 SCR center가 아니다.
- profile peak/Rp 하나만 맞는 것을 baseline reproduction 성공으로 판단하지 않는다.
- 1D r=4.6875 um cut이 잘 맞더라도 최종 electrical equivalence는 SDevice에서 확인해야 한다.
- RTA 변화가 VBD/SCR에 미치는 영향이 작게 보인 기존 결과는 있었지만, **RTA 조건별 PLX profile sensitivity를 정량 비교해 low-sensitivity라고 확정한 상태는 아니다.** 따라서 RTA profile sensitivity는 아직 검증 항목이다.
- SVisualPy의 SDE target 수치는 현재 project baseline calibration용 값이며 실제 ST foundry process parameter로 주장하지 않는다.

## Status

- SProcess PLX-only/no-TDR command: 작성 완료
- PW fraction `1-x` 자동화: 적용 완료
- SVisualPy profile metric extractor: 작성 완료
- 대규모 DOE 실험: 진행 중
- RTA 조건별 PLX sensitivity 검증: 미완료
- 최종 surrogate baseline freeze: 미완료
