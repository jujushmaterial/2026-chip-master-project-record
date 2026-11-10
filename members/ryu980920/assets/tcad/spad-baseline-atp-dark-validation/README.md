# SPAD 기준 소자 ATP 및 암전류 검증

CMP SPAD B측 ATP 및 dark-current 계산에 사용한 Sentaurus command 보관 위치이다.

이 디렉터리의 목적은 공통 SPAD geometry/mesh를 입력으로 사용하여 B 연구에서 수행한 ATP 및 dark-current 계산 덱과 후처리 코드를 원문 그대로 보존하는 것이다.

## 공통 기준

공통 electrical baseline의 VBD 및 SCR 위치는 아래 주상현 static-freeze 결과를 기준으로 사용한다.

`members/jujushmaterial/assets/tcad/spad-baseline-static-freeze/`

B의 ATP/dark 계산은 동일 SDE geometry와 mesh를 입력으로 사용하되, ATP 및 dark-current 평가 목적에 맞춘 별도 SDevice physics 설정을 사용한다. 따라서 B측 덱에서 재계산되는 VBD/SCR 관련 값은 주상현 static-freeze 값과 소폭 차이가 날 수 있으며, 해당 값은 B측 진단 결과로 보존한다. 공통 baseline VBD/SCR을 대체하는 값으로 사용하지 않는다.

주요 설정 차이의 예:

- 공통 고정 기준 진단 덱: `Avalanche(vanOverstraeten GradQuasiFermi)` 및 `ComputeIonizationIntegrals(direction="eGradQuasiFermi")`
- B측 ATP 진단 덱: `Avalanche(vanOverstraeten ElectricField)`, `AvalPostProcessing`, `BreakdownProbability`
- B측 암전류 덱: `Avalanche(vanOverstraeten Eparallel)`(충격 이온화 피드백 활성화)

## 파일 목록

```text
CMP_SPAD_Diagnostic_ATP_SDevice.txt
CMP_SPAD_DarkCurrent_SDevice.txt
CMP_SPAD_Diagnostic_ATP_SVisualPy.txt
CMP_SPAD_DarkCurrent_SVisualPy.txt
```

### CMP_SPAD_Diagnostic_ATP_SDevice.txt

- Workbench 역할: n5
- 충격 이온화 피드백 비활성화
- `AvalPostProcessing`
- 이온화 적분·항복 경로 진단
- `BreakdownProbability`
- `eBreakdownProbability`, `hBreakdownProbability`, `jBreakdownProbability` 출력
- 항복 이후 ATP 상태를 생성하기 위해 20 V까지 계산

### CMP_SPAD_DarkCurrent_SDevice.txt

- Workbench 역할: n6
- 충격 이온화 피드백 활성화
- 자체 일관적인 역방향 I–V 및 증배된 암전류 계산
- Hurkx 터널링을 적용한 SRH·BTBT·Avalanche 생성 포함
- `BreakCriteria`로 breakdown 부근 runaway 제한
- 트랩·수명 보정 이전에는 절대 DCR 대신 상대 암전류나 DCR 대리지표로 해석

### CMP_SPAD_Diagnostic_ATP_SVisualPy.txt

- Workbench 역할: n8
- n5 직접 후처리
- VBD·SCR·전계 진단 기능 유지
- 2D TDR에서 반경 방향 절단선을 만들어 표본화된 원통형 ATP r-z 분포를 재구성
- 주요 ATP 지표:
  - `ATP_axis180`
  - `ATP_peak180`
  - `ATP_peak`
  - `ATP_peak_r_um`
  - `ATP_peak_z_nm`
- 기존 `r=4.6875 um`, `r=12.5 um` 값은 SDevice/ATP diagnostic cut으로 유지
- SDE 기준 Mesh를 추가 의존성으로 읽고 활성 도핑 PLX를 `r=0`, `r=4.6875 um`, `r=13 um`에서 출력
- `r=4.6875 um`은 P+ anode overlap이 있는 기하학적 축 `r=0`과 분리하여 PW/DNW process-matching에 사용하는 central-active-region cut
- 주요 추가 출력: `n<visual-node>_stage1_py_SDE_baseline_r4p6875.plx`
- 기존 v3.3 VBD/SCR/field/ATP 계산 및 DOE metric 이름은 변경하지 않음

### CMP_SPAD_DarkCurrent_SVisualPy.txt

- Workbench 역할: n9
- 바로 앞 n6 노드의 피드백 활성화 역방향 I–V를 사용
- 현 SWB graph에서 n5 diagnostic VBD를 별도 참조
- I50/I90/I156 및 SRH/BTBT/avalanche generation-component metric 추출
- 역함수 맞춤법으로 계산한 VBD는 진단용이며 `Dark_OK` 필수조건이 아님
- 절대 DCR 개선을 주장하지 않음

## SWB 노드 연결 관계

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

## 원본 무결성

Git blob SHA 기준 원문 일치값:

```text
CMP_SPAD_Diagnostic_ATP_SDevice.txt    2b8cd60b50edc7d7404c47b1ebbfa039c3aae027
CMP_SPAD_DarkCurrent_SDevice.txt       5227f68fa2acd6375a2dbcbadd19743e415d813d
CMP_SPAD_Diagnostic_ATP_SVisualPy.txt  e2774e11ccc15068e9a6683711e56e7d1a283670
CMP_SPAD_DarkCurrent_SVisualPy.txt     b2f352787eede4b7a481f6acb65df5e6874b6af9
```

## 참고 사항

- 이 디렉터리는 ST foundry recipe 복원을 의미하지 않는다.
- B측 ATP/dark 결과는 이 디렉터리의 별도 diagnostic/dark-current deck으로 계산되었다.
- 공통 VBD/SCR 기준값은 주상현의 static-freeze baseline을 따른다.
- Sentaurus User Guide PDF, 대형 TDR, 실행 중간 binary는 이 디렉터리에 포함하지 않는다.
- 개인 timeline 기록은 별도로 `members/ryu980920/timeline/`에서 관리한다.
