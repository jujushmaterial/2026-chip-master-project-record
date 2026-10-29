# Electrical_Test 07 — SVisualPy 15.0 V 전계·Avalanche 비교 진단

> **상태: 코드 작성·구문 검사·Mock SVisualPy 데이터 실행 검증 완료. 실제 Synopsys SVisual T-2022.03 환경 및 원본 TDR 실행은 미검증.** 이 진단은 공식 SDE baseline의 VBD 및 15.6 V SCR 판정 덱을 변경하지 않는다.

## 1. 역할

공식 SDE static-freeze와 현재 SProcess 후보의 **동일 15.0 V** 결과를 비교한다.

- SProcess: 현재 실험의 `n@node|sdevice@_V150_des.tdr` (같은 SWB experiment branch)
- SDE: 공식 baseline의 `V150_des.tdr` (서로 다른 기존 SDE 실험의 결과)
- 공통 기준: grating/Si interface로부터의 깊이 `z_if` (µm)
  - SDE: `z_if = Y_raw - 0.000 µm`
  - SProcess: `z_if = Y_raw - 0.300 µm`
- 결과는 **15.0 V에서의 원인 분석용**이며 `06_SVisualPy_VBD_SCR.py`의 15.6 V SCR 판정을 대신하지 않는다.

## 2. SWB에서 사용하는 순서

1. 기존 `SProcess1 → SProcess2 → SNMesh1 → SNMesh2 → SDevice → SVisualPy(06)`은 **변경하지 않는다.**
2. 같은 `SDevice`에 연결되는 **독립 SVisual(Python 모드) 진단 노드**를 추가하고, `[07_SVisualPy_Field_Diagnostic.py](07_SVisualPy_Field_Diagnostic.py)` 전체 코드를 입력한다. 맨 첫 줄은 `#setdep @node|sdevice@`다.
3. **SDE의 V150 TDR 연결:** 현재 SProcess 실험과 다른 브랜치에 있는 SDE TDR은 `#setdep @node|sdevice@`만으로 자동 전달되지 않는다. 다음 중 한 가지를 수행한다.
   - 추천: SDE 공식 baseline의 `n5_V150_des.tdr`(현재 SVisual 화면의 예시 이름)을 **진단 노드 실행 디렉터리**에 `SDE_baseline_V150_des.tdr`이라는 이름으로 복사한다. `n5`는 예시일 뿐 실제 SDE node ID를 확인한다.
   - 또는 새 SVisual 프로세스가 시작되기 전 환경변수 `CMP_SPAD_SDE_V150_TDR`에 **SDE V150 TDR의 절대 경로**를 지정한다. 예: Bash `export CMP_SPAD_SDE_V150_TDR=/실제/경로/n5_V150_des.tdr`. 환경변수가 Workbench 실행 프로세스까지 전달되는지도 확인한다.
4. SProcess 쪽 TDR은 **그 실험의 `@node|sdevice@`를 기준으로 자동 지정**된다. 실제 파일 존재를 검사하며 없는 경우 명확한 예외를 내고 중단한다.
5. 우선 정상 완료된 **1000°C·10초** 실험에서 실행한다. 950°C·10초처럼 15.0 V 도달 전 SDevice가 실패한 조건은 `V150_des.tdr`이 없을 수 있으므로 이 진단을 수행할 수 없다.

## 3. 출력 파일

모든 결과는 실행 노드 번호를 앞에 붙여 생성한다. 예: `n77_field15_...`.

| 파일 | 의미 |
|---|---|
| `n*_field15_r4p6875_compare.csv` | 중앙 대표 위치 r=4.6875 µm, 공통 깊이 격자, 두 구조 |E|, AvalancheGeneration, 차이 |
| `n*_field15_r12p5_compare.csv` | Active-region 주변부 r=12.5 µm의 동일 비교 |
| `n*_field15_r16p0_compare.csv`, `r17p0`, `r18p0` | X≈16~18 µm의 국소 고전계 부위 추가 분석 |
| `n*_field15_r*_E.svg` | 각 Cutline의 **전계 크기** SVG 비교 그래프 (Y축 kV/cm) |
| `n*_field15_r*_Avalanche.svg` | AvalancheGeneration이 있으면 로그 변환 SVG 비교 그래프 |
| `n*_field15_peak_summary.csv` | Cutline별 최대 |E|와 해당 공통 깊이, Avalanche 최대 및 양쪽 데이터 겹치는 점 수 |
| `n*_field15_audit.txt` | 입력 파일, 좌표 정의, 고정 bias, full-Silicon 최대값 함수 가능 여부, 출력 파일 목록 |

`AvalancheGeneration` 데이터가 없으면 **0으로 대체하지 않고 결측값으로 남긴다.** 비교 CSV의 빈 칸은 공통 격자 범위 밖, 실리콘 분리 구간 또는 실제 데이터 누락을 의미한다.

**정확한 전체 2D Silicon 최대 전계:** SVisual User Guide T-2022.03의 `calculate_field_value`는 2D Silicon material 조건의 최대값과 좌표를 추출하는 기능을 제공한다. 하지만 Python wrapper의 Keyword 인자가 설치 버전에 따라 다를 수 있어 코드는 대표적인 호출 규약을 시도하며, 실제 지원되지 않으면 `fullSilicon_Emax=UNAVAILABLE`로 기록한다. **Cutline 최대값을 전체 소자의 정확한 최대값으로 보고하지 않는다.**

## 4. 수치 비교 시 주의

- 두 데이터셋 모두 15.0 V·300 K의 **SDevice 시뮬레이션 결과**로 비교한다. `ElectricField-Y`가 아니라 `Abs(ElectricField-V)` 또는 `|E|`를 사용한다.
- 공통 깊이 격자: 0~1.30 µm, 5 nm 간격. 원본 메쉬의 깊이 간격이 0.12 µm를 초과하면 그 사이를 임의로 보간하지 않는다. 이 값은 **진단용 보간 제한**이며 SCR/물리 모델 설정값이 아니다.
- 12.5 µm 및 16~18 µm는 edge/peripheral **탐색 위치**다. 정확한 avalanche 시작 지점이라고 먼저 가정하지 않는다.
- 15.0 V의 AvalancheGeneration 최대는 **breakdown onset 자체가 아니다.** Ionization-integral VBD의 정의는 기존 05/06 덱을 따른다.
- 실제 SWB 입력 Parameter 14개(`DNW_E` 등)는 **이 진단 덱에서 변경하지 않는다**. Implant·RTA 값을 하드코딩하거나 Sweep하지 않는다.

## 5. 검증 상태

- `[통과]` Python 구문 검사 (SWB `@node@`/`@node|sdevice@` 변환 후).
- `[통과]` Mock SVisual API에서 SDE/SProcess의 서로 다른 raw Y를 같은 `z_if`로 정렬.
- `[통과]` CSV 5개, |E| SVG 5개, Avalanche SVG 5개, summary/audit 생성.
- `[미검증]` 실제 Sentaurus Visual 2022.03의 2D TDR 파일 및 Python wrapper `calculate_field_value` 동작.
- `[미검증]` 실제 출력 전계 및 SDE 대비 수치 차이. 데이터 확보 전에는 VBD 감소 원인을 특정하지 않는다.
