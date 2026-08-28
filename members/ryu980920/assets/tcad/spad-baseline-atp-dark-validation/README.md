# SPAD Baseline ATP / Dark Validation

CMP SPAD B-side ATP 및 dark-current 계산에 사용한 Sentaurus command 보관 위치이다.

이 디렉터리의 목적은 공통 SPAD geometry/mesh를 입력으로 사용하여 B 연구에서 수행한 ATP 및 dark-current 계산 덱과 후처리 코드를 원문 그대로 보존하는 것이다.

## Common baseline authority

공통 electrical baseline의 VBD 및 SCR 위치는 아래 주상현 static-freeze 결과를 기준으로 사용한다.

`members/jujushmaterial/assets/tcad/spad-baseline-static-freeze/`

B의 ATP/dark 계산은 동일 SDE geometry와 mesh를 입력으로 사용하되, ATP 및 dark-current 평가 목적에 맞춘 별도 SDevice physics 설정을 사용한다. 따라서 B-side 덱에서 재계산되는 VBD/SCR 관련 값은 주상현 static-freeze 값과 소폭 차이가 날 수 있으며, 해당 값은 B-side diagnostic 결과로 보존한다. 공통 baseline VBD/SCR을 대체하는 값으로 사용하지 않는다.

주요 설정 차이의 예:

- common static-freeze diagnostic: `Avalanche(vanOverstraeten GradQuasiFermi)` 및 `ComputeIonizationIntegrals(direction="eGradQuasiFermi")`
- B ATP diagnostic deck: `Avalanche(vanOverstraeten ElectricField)`, `AvalPostProcessing`, `BreakdownProbability`
- B dark-current deck: `Avalanche(vanOverstraeten Eparallel)` with impact-ionization feedback ON

## Files

```text
CMP_SPAD_Diagnostic_ATP_SDevice_v1.0.txt
CMP_SPAD_DarkCurrent_SDevice_v1.0.txt
CMP_SPAD_Diagnostic_ATP_SVisualPy_v3.3.txt
CMP_SPAD_DarkCurrent_SVisualPy_v1.1.txt
```

### CMP_SPAD_Diagnostic_ATP_SDevice_v1.0.txt

- Workbench 역할: n5
- impact-ionization feedback OFF
- `AvalPostProcessing`
- ionization-integral / breakdown-path diagnostic
- `BreakdownProbability`
- `eBreakdownProbability`, `hBreakdownProbability`, `jBreakdownProbability` 출력
- above-breakdown ATP snapshot 생성을 위해 20 V까지 진행

### CMP_SPAD_DarkCurrent_SDevice_v1.0.txt

- Workbench 역할: n6
- impact-ionization feedback ON
- self-consistent reverse I-V 및 multiplied dark-current 계산
- SRH with Hurkx tunneling, BTBT, avalanche generation 포함
- `BreakCriteria`로 breakdown 부근 runaway 제한
- trap/lifetime calibration 전에는 절대 DCR이 아니라 상대 dark-current 또는 DCR proxy로 해석

### CMP_SPAD_Diagnostic_ATP_SVisualPy_v3.3.txt

- Workbench 역할: n8
- n5 직접 후처리
- VBD/SCR/field diagnostic 유지
- 2D TDR에서 radial cutline을 생성하여 sampled cylindrical ATP r-z map 재구성
- 주요 ATP metric:
  - `ATP_axis180`
  - `ATP_peak180`
  - `ATP_peak`
  - `ATP_peak_r_um`
  - `ATP_peak_z_nm`
- 기존 `r=4.6875 um`, `r=12.5 um` 값은 legacy diagnostic profile로만 유지

### CMP_SPAD_DarkCurrent_SVisualPy_v1.1.txt

- Workbench 역할: n9
- direct parent n6의 feedback-ON reverse I-V를 사용
- 현 SWB graph에서 n5 diagnostic VBD를 별도 참조
- I50/I90/I156 및 SRH/BTBT/avalanche generation-component metric 추출
- inverse-fit VBD는 diagnostic-only이며 `Dark_OK` 필수조건이 아님
- absolute DCR claim은 하지 않음

## SWB relationship

```text
Common SDE / mesh
    |
    +--> n5 ATP diagnostic SDevice
    |       |
    |       +--> n8 ATP SVisualPy
    |
    +--> n6 feedback-ON dark-current SDevice
            |
            +--> n9 dark-current SVisualPy
```

## Source integrity

Git blob SHA 기준 원문 일치값:

```text
CMP_SPAD_Diagnostic_ATP_SDevice_v1.0.txt    2b8cd60b50edc7d7404c47b1ebbfa039c3aae027
CMP_SPAD_DarkCurrent_SDevice_v1.0.txt       5227f68fa2acd6375a2dbcbadd19743e415d813d
CMP_SPAD_Diagnostic_ATP_SVisualPy_v3.3.txt  a6cd3906a1e664ac5c0bbea3b02e8f01c76ee50e
CMP_SPAD_DarkCurrent_SVisualPy_v1.1.txt     b2f352787eede4b7a481f6acb65df5e6874b6af9
```

## Notes

- 이 디렉터리는 ST foundry recipe 복원을 의미하지 않는다.
- B-side ATP/dark 결과는 이 디렉터리의 별도 diagnostic/dark-current deck으로 계산되었다.
- 공통 VBD/SCR 기준값은 주상현의 static-freeze baseline을 따른다.
- Sentaurus User Guide PDF, 대형 TDR, 실행 중간 binary는 이 디렉터리에 포함하지 않는다.
- 개인 timeline 기록은 별도로 `members/ryu980920/timeline/`에서 관리한다.
