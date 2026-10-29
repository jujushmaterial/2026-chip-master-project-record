# Electrical_Test — CMP SPAD 전기적 특성 검증 덱

> **2026-10-26 상태:** 코드 작성·기존 원본 보존·정적 파일 연결 검사 완료. 실제 Sentaurus Workbench 전체 실행 및 VBD/SCR 정합은 **아직 미검증**.

## 목적과 기준

28 nm FD-SOI quasi-circular SPAD의 문헌 제약 기반 surrogate 공정 후보를 SDE static-freeze baseline과 동일한 **VBD 및 15.6 V SCR 추출 방식**으로 평가한다. 실제 ST 파운드리 제조 recipe가 아니다.

- [SPAD 공동연구 기준계획서](../../../../../shared/decisions/SPAD_연구계획서.md)
- [공식 SDE static-freeze 참조](https://github.com/jujushmaterial/2026-chip-master-project-record/tree/main/members/jujushmaterial/assets/tcad/spad-baseline-static-freeze)
- [2026-10-26 작업일지](../../../timeline/2026-10/2026-10-26.md)

## Workbench 배치 순서

| 단계 | SWB Tool alias | 덱 | 역할 / 출력 |
|---:|---|---|---|
| 1 | `sprocess1` | [01_SProcess1_CommonSTI.cmd](01_SProcess1_CommonSTI.cmd) | 공통 SOI + native STI + densification → **restart-capable** `n<node>_STI_RESTART_fps.tdr` |
| 2 | `sprocess` | [02_SProcess2_TripleDNW_TriplePW_AbsoluteDose.cmd](02_SProcess2_TripleDNW_TriplePW_AbsoluteDose.cmd) | 동일 Stage 1 restart → Triple DNW/PW, NW, 공통 WELL RTA, BOX removal, P+ 및 contact → `n<node>_fps.tdr` + PLX |
| 3 | `snmesh1` | [03_SNMesh1_Mesh2bnd.cmd](03_SNMesh1_Mesh2bnd.cmd) | Stage 2 final `fps.tdr`에서 경계 추출 → `n<node>_bnd.tdr` |
| 4 | `snmesh2` | [04_SNMesh2_ProfileMapping.cmd](04_SNMesh2_ProfileMapping.cmd) | 바로 앞 SNMesh 1 `bnd.tdr` + **동일 Stage 2** `fps.tdr` 도핑 보간 → `n<node>_msh.tdr` |
| 5 | `sdevice` | [05_SDevice_VBD_SCR.cmd](05_SDevice_VBD_SCR.cmd) | 바로 앞 SNMesh 2 `msh.tdr` → `n<node>_des.plt` 및 `n<node>_V156_des.tdr` |
| 6 | `svisualpy` | [06_SVisualPy_VBD_SCR.py](06_SVisualPy_VBD_SCR.py) | 같은 SDevice의 I–V + 15.6 V snapshot → `VBD_V`, `SCR_center_nm`, `SCR_width_nm` |

**출처:** 01은 [Dual_DNW 기존 Stage 1](../Dual_DNW/CMP_SPAD_DualDNW_SProcess_v0.2_Stage1_CommonSTISeed.txt) 원문이고, 03·04·05는 [spad-baseline-implementation](../spad-baseline-implementation/)의 기존 SNMesh/SDevice 원문이다. 02와 06만 새 v0.5 코드다. 이전 덱은 덮어쓰지 않았다.

**주의:** `@node|-1@`는 직전 노드, `@node|sprocess1@`, `@node|sprocess@`, `@node|sdevice@`는 Workbench의 해당 alias를 참조한다. 위 순서를 유지하고 하나의 experiment branch에 연결해야 한다.

## 입력/출력 연결 확인 절차

1. SProcess 1에 `struct tdr=n@node@_STI_RESTART restart` 저장 성공.
2. SProcess 2가 **같은 Stage 1의** restart를 `init tdr=$SEED_TDR`로 불러오고 contacts 생성 후 `struct tdr=n@node@`로 **최종** `n<node>_fps.tdr` 저장.
3. SNMesh 1의 `inputFile`과 SNMesh 2의 `SubMesh.Geofile`이 **동일한 SProcess 2 실험의 `fps.tdr`**을 사용.
4. SNMesh 2의 `inputFile`은 직전 SNMesh 1의 `bnd.tdr`, SDevice `File.Grid`는 직전 SNMesh 2의 `msh.tdr`인지 확인.
5. SVisualPy의 `SNODE`가 해당 SDevice 노드인지, `des.plt`와 `V156_des.tdr`이 같은 실험 결과인지 확인.
6. 첫 실행 후 SProcess final PLX와 SNMesh 2의 mapped doping·contact를 비교하여 보간/좌표 오류가 없는지 재확인.

## Stage 2 SWB 등록 파라미터 (총 14개)

이번 버전부터 **Fraction 없이 각 Implant의 Energy·절대 Dose를 직접 지정**한다. 아래 값은 Shallow Dose **6.36×10¹² cm⁻²** 잠정 후보의 [surrogate assumption]이며 전부 SWB experiment row에서 설정한다. 등록된 파라미터는 스크립트에서 반드시 `@PARAMETER@`로 받는다.

| # | Parameter | 설정값 | 의미/단위 |
|---:|---|---:|---|
| 1 | `DNW_E` | 955 | Main keV |
| 2 | `DNW_MAIN_DOSE` | 1.50e13 | Main cm⁻² |
| 3 | `DNW_TRIM_E` | 550 | Trim keV |
| 4 | `DNW_TRIM_DOSE` | 7.50e12 | Trim cm⁻² |
| 5 | `DNW_DEEP_E` | 1485 | Deep keV |
| 6 | `DNW_DEEP_DOSE` | 7.00e12 | Deep cm⁻² |
| 7 | `PW_FIXED_E` | 36 | **Shallow** keV |
| 8 | `PW_FIXED_DOSE` | **6.36e12** | **Shallow** cm⁻² |
| 9 | `PW_MID_E` | 80 | Mid keV |
| 10 | `PW_MID_DOSE` | 8.00e12 | Mid cm⁻² |
| 11 | `PW_TRIM_E` | 145 | **Deep** keV |
| 12 | `PW_TRIM_DOSE` | 3.60e12 | **Deep** cm⁻² |
| 13 | `RTA_T` | 1050 / 1000 / 950 | 공통 WELL RTA °C |
| 14 | `RTA_t` | 30 / 10 / 10 | 공통 WELL RTA s |

기존 `DNW_DOSE`, `DNW_TRIM_FRAC`, `DNW_DEEP_FRAC`, `PW_TOTAL_DOSE`, `PW_TRIM_FRAC`는 새 Stage 2 등록변수에서 제외한다. `PW_FIXED`는 Shallow, `PW_TRIM`은 Deep이라는 기존 명칭 대응에 주의한다.

함께 배포한 [SWB_RTA_3cases_14Params_NoIndex.csv](SWB_RTA_3cases_14Params_NoIndex.csv)는 **Index 열 없는 14열**이다. 1050°C/30 s는 기존 조건, 1000°C/10 s는 우선 시험 조건, 950°C/10 s는 저온 탐색 조건이며 모든 Implant Energy/Dose는 같다.

Stage 1 STI densification과 Stage 2의 추가 **P+ contact activation spike(1050°C/1.5 s)**는 공통 WELL RTA와 별도로 유지한다. WELL RTA만 낮춘 것을 전체 thermal history가 동일 비율로 감소했다고 해석하지 않는다.

## 공식 SDE와 동일한 추출 조건

- **SDevice**: 300 K, `Avalanche(vanOverstraeten GradQuasiFermi)`, `AvalPostProcessing`, `BreakAtIonIntegral`, `ComputeIonizationIntegrals(direction="eGradQuasiFermi")` 사용. ATP 전용 `ElectricField` 모델과 섞지 않는다.
- **VBD**: `PhiElectron`·`PhiHole` 중 작은 값의 **첫 번째 1 crossing**에 대응하는 역방향 Cathode Voltage. 임의 I–V 전류 기준으로 판정하지 않는다.
- **SCR**: **고정 Cathode 15.6 V**, **r=4.6875 µm**, net doping zero crossing 양쪽의 **|E|=1.0×10⁵ V/cm** 교차로 경계 정의. 공통 interface 좌표 **z_if=0~1.30 µm**에서 탐색한다.
- **좌표**: 공식 SDE raw interface y=0.0 µm, SProcess raw interface y=0.300 µm이므로 새 SVisualPy에서 `z_if = y_raw - 0.300 µm` 적용.
- **출력**: Workbench DOE에는 `VBD_V`, `SCR_center_nm`, `SCR_width_nm`만 표시. 평가 바이어스·노드·스냅샷 유효 여부 등은 `n<node>_VBD_SCR_audit.txt`에 보존.
- 15.6 V에서 TDR이 생성되지 않으면 SCR은 `x`(NA)로 처리하며, 임의의 다른 전압이나 동일 excess bias로 대체하지 않는다.
- 이번 비교는 **동일한 15.6 V fixed-bias** 비교이며, 각 소자의 VBD 차이로 excess bias는 달라질 수 있다. **180 nm는 optical SCR anchor**이지 실제 SDE의 SCR center 측정값 자체가 아니다.

## 검증 상태

| 항목 | 결과 |
|---|---|
| 기존 4개 덱 GitHub 원문과 일치 | 확인 |
| 14개 SWB Parameter 매크로 및 fraction 제거 | 정적 검사 통과 |
| Stage 1 → 2 → SNMesh 1 → 2 → SDevice → SVisualPy 파일명/alias | 정적 검사 통과 |
| 공식 SDE VBD/SCR 추출 기준 | 코드 대조 통과 |
| RTA DOE 3행 입력 형식 및 고정 Implant | 검사 통과 |
| 실제 SWB 전 노드 실행·물리량 정합 | **아직 실행 검증 전** |

기존 [Triple-PW v0.4 PLX-only 덱](../Triple_PW/CMP_SPAD_TriplePW_155Deep_Mid18_SProcess_v0.4.cmd)과 원본 연구일지는 그대로 유지한다. 최종 전기적 동등성 주장은 실제 SDevice 결과 확보 후 판단한다.

## 07. SDE vs SProcess 전계·Avalanche 15.0 V 비교 진단 (2026-10-29 추가)

기존 06 VBD/SCR 분석과 **독립적인 SVisualPy 코드**를 추가했다. 공식 baseline과 SProcess 각각의 `V150_des.tdr`을 동일 **15.0 V** 조건으로 읽고 중앙 r=4.6875 µm, edge r=12.5 µm 및 주변 r=16/17/18 µm에서 `|E|`와 `AvalancheGeneration`을 공통 z 기준면으로 보정하여 비교한다. **06의 15.6 V SCR 추출 기준, 05 SDevice Physics 및 SWB 등록 Parameter는 변경하지 않는다.**

- [07_SVisualPy_Field_Diagnostic.py](07_SVisualPy_Field_Diagnostic.py) — 실제 SWB SVisual Python 모드 입력용 전체 코드
- [07_SVisualPy_Field_Diagnostic_Code.md](07_SVisualPy_Field_Diagnostic_Code.md) — Markdown 코드 복사본
- [07_Field_Diagnostic_Usage.md](07_Field_Diagnostic_Usage.md) — 실행 방법, SDE TDR 경로 연결, CSV/SVG 출력 정의, 해석 주의사항

**필수 외부 입력:** 공식 SDE의 `V150_des.tdr`은 동일 SProcess SWB branch에서 자동으로 전달되지 않는다. 해당 파일을 진단 노드 실행 디렉터리의 `SDE_baseline_V150_des.tdr`로 복사하거나 `CMP_SPAD_SDE_V150_TDR` 환경변수에 절대 경로를 지정한다. SProcess 측은 `n@node|sdevice@_V150_des.tdr`로 해당 실험을 자동 참조한다.

**출력:** 5개 위치의 비교 CSV, 각 위치의 E-field SVG, AvalancheGeneration이 존재하면 추가 SVG, peak summary CSV, audit TXT. 전체 Silicon 최대 전계와 좌표는 설치된 SVisualPy의 2D `calculate_field_value` API가 지원될 때에만 audit에 기록하며, 지원되지 않으면 `UNAVAILABLE`로 표기한다. Cutline 최대값을 2D 전체 최대값으로 대체하지 않는다.

**검증 상태:** Python 구문 및 Mock SVisualPy 실행 검증 완료. **실제 Sentaurus Visual T-2022.03에서의 원본 TDR 실행과 추출 결과는 아직 미검증.**
