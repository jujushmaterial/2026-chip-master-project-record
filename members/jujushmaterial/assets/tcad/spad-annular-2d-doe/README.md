# SPAD A — Annular FF15 2D Radial-Pitch DOE

이 폴더는 A(jujushmaterial)의 proposed concentric annular Si/STI optical structure에 대한 2D radial-pitch screening용 코드와 설정 기록을 보관한다.

## Status

- 단계: 2D screening DOE setup / initial geometry check
- 상태: In Progress
- final 3D optical claim: 아직 수행하지 않음

## Core rule

- Reference optical-pattern FF = N/A
- Proposed annular intentional optical-pattern Si FF = 15% fixed
- independent variable = `RadialPitch`
- dependent variable = `RingWidth`
- RingWidth는 finite 3D annulus area accounting으로 자동 계산
- frozen native STI1~5는 이동하지 않음
- native-STI overlap은 별도 diagnostic이며 15% pattern FF를 보상하기 위해 ring을 넓히지 않음

## DOE

- `RadialPitch = 0.200 ~ 1.000 um`
- basic step = `0.005 um`
- `0.270 um` 제외
- total = `160 cases`
- existing 0.200 case + imported 159 cases

## Files

- `CMP_SPAD_A_Annular2D_FF15_RadialPitch_SDE_v1.1.txt`
  - frozen baseline + intentional annular-pattern diametric cross-section 생성
  - exact annular area FF solver 및 native-STI overlap diagnostic
- `CMP_SPAD_A_Annular2D_FF15_SNMesh_v1.0.txt`
  - 2D tensor mesh
- `CMP_SPAD_A_Annular2D_FF15_940nm_EMW_v1.0.txt`
  - 940 nm TE EMW screening
- `CMP_SPAD_A_Annular2D_FF15_SVisualPy_DOE_v1.1.txt`
  - FF 검증, SCR-slab OpticalGeneration integration, DOE output
- `CMP_SPAD_A_RadialPitch_Split_160cases_5nm.txt`
  - 160-case split reference
- `RadialPitch_import_159.csv`
  - 기존 0.200 case를 제외한 SWB import용 159 cases
- `CMP_SPAD_A_2D_Annular_RadialPitch_DOE_Setup_2026-09-17.md`
  - 방법, 범위, 이유, metric, 현재 상태 상세 기록

## Important limitation

2D geometry는 annular 구조의 diametric/radial cross-section을 사용하지만 EMW가 이를 원통대칭으로 회전하여 계산하는 것은 아니다. 2D 결과는 screening용이며, selected candidate는 실제 3D concentric annular SDE/EMW로 검증해야 한다.
