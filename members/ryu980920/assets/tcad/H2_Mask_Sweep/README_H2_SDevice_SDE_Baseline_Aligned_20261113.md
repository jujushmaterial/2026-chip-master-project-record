# H2 SDevice – SDE baseline 모델 정합 버전 (2026-11-13)

기준: 공유 GitHub 레포 `jujushmaterial/2026-chip-master-project-record`

- SDE VBD: `members/jujushmaterial/assets/tcad/spad-baseline-static-freeze/CMP_SPAD_VBD_Diagnostic_SDevice_v1.1_dependency_fix.txt`
- SDE ATP: `members/ryu980920/assets/tcad/spad-baseline-atp-dark-validation/CMP_SPAD_Diagnostic_ATP_SDevice.txt`
- SDE Dark Current: `members/ryu980920/assets/tcad/spad-baseline-atp-dark-validation/CMP_SPAD_DarkCurrent_SDevice.txt`
- H2 원본: `members/ryu980920/assets/tcad/H2_Mask_Sweep/`

## 교체할 4개 파일

1. `05_SDevice_VBD_SCR.cmd`: **VBD 물리 모델을 SDE baseline과 동일**하게 유지. 기본 SRH/Auger, `vanOverstraeten GradQuasiFermi`, `Iterations=30`, `AvalPostProcessing`, `BreakAtIonIntegral` 유지. 기존 H2 SWB mesh 연결 및 동적 VBD 추출은 유지.
2. `07_H2_SDevice2_SCR_PEB_ATP.cmd`: **SDE ATP 모델로 정합**. `SRH(...Tunneling(Hurkx))`, `Band2Band(Model=Hurkx)`, `Enormal`, `vanOverstraeten ElectricField`, `Iterations=100`, `MinElectricField=2.0e5`, ionization paths 출력. H2의 `@SCR_BIAS_V@`, `@PEB_BIAS_V@`, `@ATP_BIAS_V@` 및 세 단계 TDR 이름 그대로 유지.
3. `09_SDevice3_DarkCurrent.cmd`: 기존 H2 Dark Current 모델이 SDE baseline과 일치해 **물리 모델 수정 없음**. `Iterations=30`으로 baseline과 동일하게 함. `@DARK_BIAS_V@`와 feedback ON 유지.
4. `12_H2_CathodePath_SDevice.cmd`: **원본 그대로** 포함. SDE baseline에 대응되지 않는 독립 진단이며 물리 설정을 임의 변경하지 않음.

## 중요한 구별

- **SDE VBD 자체는 Hurkx TAT/BTBT를 사용하지 않음**. VBD에서 Hurkx를 넣지 말 것.
- **SDE ATP는 Hurkx를 사용하고 ElectricField driving force를 사용**. VBD의 GradQuasiFermi와는 의도적으로 다름.
- **SDE Dark Current는 Hurkx와 Eparallel, impact-ionization feedback ON을 사용**.
- `SDevice2`의 `CurrentPlot`은 semiconductor-integrated generation diagnostics를 추가로 출력하며 물리 모델 자체는 바꾸지 않음.
- H2 전압 정의는 SDE의 고정 전압 sweep과 달리 동적으로 VBD를 참조함. 동일 `Vex`/동일 기준 전압·온도에서 평가해야 결과를 직접 비교할 수 있음.
- H2의 mask/implant geometry 및 doping은 SDE baseline과 동일하지 않음. 이 패키지는 **물리 모델 정합**용이며, 구조/도핑의 동일성을 보장하지 않음.
- 현재 TCAD 환경에서 직접 실행하거나 node 결과의 수렴 여부를 검증한 것은 아님.
- SDevice3의 potential/electric-field 모니터 좌표는 H2 원본을 보존한 값. 모델 비교 시에는 동일 좌표계 변환과 실제 소자 위치를 확인할 것.

## SWB parameter 연결 점검

- 네 노드 공정 SWB 매개변수(DNW_DOSE, DNW_E, PW_TRIM_E, PW_FIXED_E, PW_TRIM_FRAC, PW_FIXED_FRAC, PW_TOTAL_DOSE, RTA_T, RTA_t)는 SDevice 덱의 직접 입력값이 아니며 여기서 임의 하드코딩하지 않음.
- 기존 H2 동적 편향 SWB 변수 `SCR_BIAS_V`, `PEB_BIAS_V`, `ATP_BIAS_V`, `DARK_BIAS_V` 모두 `@...@` 형태로 유지.

## 실행 전 확인

1. 4개 기존 H2 `.cmd` 백업 후 동일한 파일명으로 교체.
2. SNMesh2가 생성한 `n@node|-1@_msh.tdr` 및 참조 상대 노드가 현 13-node SWB 순서에서 유효한지 확인.
3. SVisualPy1 VBD 추출 후 동적 편향 변수 업데이트 확인.
4. SDevice2에서 SCR/PEB/ATP 3개 goal-state TDR 및 ATP 확률 필드 확인.
5. SDevice3의 feedback-ON 전류 수렴 및 CurrentPlot을 확인.
