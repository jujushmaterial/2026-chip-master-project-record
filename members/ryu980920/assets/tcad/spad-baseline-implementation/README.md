# SPAD Baseline Implementation

CMP SPAD B-side의 문헌 제약 기반 surrogate baseline 구현에 사용 중인 현재 Sentaurus Workbench 덱 원문 보관 위치이다.

이 디렉터리의 5개 코드는 2026-08-30 기준 17-case baseline reconstruction 계산 set에서 실제 사용 중인 flow를 그대로 보존한다.

## Files

```text
CMP_SPAD_BaselineImplementation_SProcess.txt
CMP_SPAD_BaselineImplementation_SNMesh1.txt
CMP_SPAD_BaselineImplementation_SNMesh2.txt
CMP_SPAD_BaselineImplementation_SDevice.txt
CMP_SPAD_BaselineImplementation_SVisualPy.txt
```

## Flow

```text
SProcess
   ↓
SNMesh1 (Mesh2bnd)
   ↓
SNMesh2 (SProcess profile interpolation + electrical remesh)
   ↓
SDevice (VBD/SCR calibration)
   ↓
SVisualPy (VBD/SCR/field DOE extraction)
```

## Scope

- 목적: 공통 SDE/SDevice baseline의 electrical equivalence를 재현하는 surrogate baseline implementation
- 현재 단계: 17-case baseline reconstruction calibration 진행 중
- SProcess는 SWB에 등록된 9개 parameter를 모두 `@PARAMETER@` 형식으로 입력받는다.
- 현재 coarse calibration에서는 PW Trim Energy를 95 keV로 유지하고 DNW Dose/Energy 및 common RTA Temperature/Time sensitivity를 확인한다.
- 현재 SVisualPy의 SCR 값은 15.0 V snapshot 기반 diagnostic metric이며 최종 15.6 V common-baseline SCR 비교값으로 사용하지 않는다.
- 실제 ST foundry manufacturing recipe 복원을 의미하지 않는다.

## Source rule

이 폴더의 코드 원문은 2026-08-30에 사용자가 현재 SWB에서 사용 중인 덱으로 직접 제공한 파일만을 기준으로 등록하였다. 과거 버전 덱과 혼합하지 않는다.
