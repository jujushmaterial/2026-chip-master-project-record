# H2 마스크 축소 실험 — 실행 및 분석 안내

> **상태:** GitHub에 덱과 분석 코드를 등록한 상태이며, 실제 Sentaurus T-2022.03 실행·수렴 및 물리 결과 검증은 아직 수행하지 않았다. 기존 `Electrical_Test` 폴더는 변경하지 않는다.

## 1. 연구 목적 및 DOE

Trim DNW 주입 마스크의 끝 반경을 바꾸었을 때 Dark Current, Cathode 전류 경로, STI5 및 마스크 끝 전계, 주변부 조기 항복(PEB) 위험을 비교한다.

- SWB 입력 파라미터: **`Mask`** (`@Mask@`, 단위 µm).
- 조건 6개: **16.30(P0), 14.00, 13.00, 12.50, 12.20, 12.00 µm**.
- 나머지 14개 Implant 및 공통 RTA 파라미터는 **모든 SWB Experiment 행에서 P0 값으로 고정**한다. 등록된 SWB 파라미터를 `.cmd`에서 수치로 하드코딩하지 않는다.
- Main/Deep DNW 마스크 끝은 16.30 µm, PW 마스크 끝은 12.50 µm이며, 변경 대상은 **Trim DNW 마스크 하나**뿐이다.
- STI5의 반경 12.20~12.80 µm는 문헌 미공개 치수에 대한 **[surrogate dimension]**이다.
- DOE 입력 파일: `H2_SWB_6cases_15Params.csv` (15개 입력 파라미터, 6행).

## 2. SWB Tool 배치 순서 — 총 13개 노드

| 순서 | SWB Tool | 덱 파일 | 역할 |
|---:|---|---|---|
| 1 | SProcess1 | `01_SProcess1_CommonSTI.cmd` | 공통 STI 구조 생성 |
| 2 | SProcess2 | `02_H2_SProcess2_TrimMask.cmd` | `@Mask@` 조건에 따른 Trim DNW 주입 |
| 3 | SNMesh1 | `03_SNMesh1_Mesh2bnd.cmd` | Boundary 추출 |
| 4 | SNMesh2 | `04_H2_SNMesh2_RefinedEdge.cmd` | 전기 Mesh 및 도핑 매핑 |
| 5 | SDevice1 | `05_SDevice_VBD_SCR.cmd` | Ionization Integral 기반 VBD |
| 6 | SVisualPy1 | `06_H2_SVisualPy1_VBD_Bias.py` | VBD 및 평가전압 추출 |
| 7 | SDevice2 | `07_H2_SDevice2_SCR_PEB_ATP.cmd` | SCR·PEB·ATP 상태 계산 |
| 8 | SVisualPy2 | `08_SVisualPy2_Dynamic_SCR_ATP.py` | SCR 및 ATP 추출 |
| 9 | SDevice3 | `09_SDevice3_DarkCurrent.cmd` | Feedback ON Dark I–V |
| 10 | SVisualPy3 | `10_SVisualPy3_DarkCurrent.py` | Dark Current 지표 추출 |
| 11 | SVisualPy4 | `11_H2_EField_SVisualPy.py` | 중앙·STI5·Mask 끝 전계/ Avalanche |
| 12 | SDevice4 | `12_H2_CathodePath_SDevice.cmd` | Cathode 전류 경로 진단 |
| 13 | SVisualPy5 | `13_H2_CathodePath_SVisualPy.py` | Cathode 단자 전류 및 KCL 추출 |

**노드 연결 주의:** 현재 덱은 이 직렬 순서를 기준으로 `@node|-n@` 참조를 사용한다. 그래프를 분기하거나 Tool을 삽입하면 전처리된 `pp*_des.cmd`의 Mesh/TDR 경로와 `#setdep`를 다시 확인해야 한다.

## 3. SProcess 및 Mesh 출력

- SProcess2는 **최종** `n<node>_fps.tdr`을 저장한다. 중간 TDR을 추가 생성하지 않는다.
- 최종 PLX는 반경 **0, 4.6875, 12.10, 12.35, 12.65, 13.0 µm**, 총 6개다.
- 기존 공통 RTA 전·후 PLX는 각 3개씩 유지하므로 공정 전체 PLX는 조건당 12개다.
- SNMesh2의 주변부 정밀화 영역은 최대 r=16.65 µm까지 확장되어 P0의 Mask=16.3 µm도 포함한다.
- 최종 도핑 비교 시 STI5 산화막 내부가 아니라 **STI5 인접 및 아래 Silicon의 활성 도핑과 Net Doping**을 확인한다.

## 4. 평가전압 및 주요 분석 방법

| 항목 | 평가 조건 | 판독 내용 |
|---|---|---|
| VBD | SDevice1 Ionization Integral | 후보별 항복전압 |
| SCR | 각 후보의 **98.7467% VBD** | 중앙 SCR 위치·폭 |
| Dark Current | 각 후보의 **98.7467% VBD** | `INear_pAum2`와 P0 대비 감소율 |
| 공통전압 Dark Current | 6조건 VBD 최솟값의 **90%** | 동일 절대전압에서 P0 대비 감소율 |
| PEB 전계 진단 | 각 후보의 **99.9% VBD** | Silicon 내 중앙·STI5·Mask 끝의 최대 전계 및 위치 |
| ATP | 각 후보의 **107.6086% VBD** | ATP 공간분포와 지표 |
| Cathode 경로 | Cathode와 Substrate를 함께 **−0.30 V**로 인가 | 전류·KCL·내부 전류 경로 검토 |

- 전계 분석 기준: 중앙 r=4.6875 µm Cutline, STI5 주변 r=12.10~12.90 µm, 각 후보 Mask 끝 ±0.25 µm.
- 전계 단위는 kV/cm, Avalanche Generation의 단위는 cm⁻³s⁻¹이다. 최대 전계와 Avalanche의 **위치도 별도 진단 파일**에 저장된다.
- STI5와 Mask 끝 분석 영역이 겹칠 수 있으므로 단일 최대값을 독립적인 두 물리 현상으로 해석하지 않는다.
- **PEB 위험**은 전계 최대값 하나로 확정할 수 없다. 99.9% VBD 부근의 Avalanche/ionization 공간분포를 함께 확인해야 한다.
- **Cathode 연결 여부**는 순방향 전류 하나만으로 확정하지 않는다. 최종 Net Doping TDR의 N형 경로와 `eCurrent/Vector`, `eQuasiFermi`를 함께 판독한다.
- Dark Current 감소를 실측 DCR 감소라고 주장하지 않는다.

## 5. 최종 비교 CSV — 정확히 14개 열

`H2_compare_cases.py`는 6개 조건의 진단 결과를 읽어 아래 열만 기록한다.

```csv
Mask_um,VBD_V,INear_pAum2,Icommon_pAum2,DarkReduction_Near_pct,DarkReduction_Common_pct,Ecenter_kVcm,ESTI5_kVcm,EMask_kVcm,EMask_r_um,AvalMask_cm3s,ForwardI_RelativeP0,CathodeConnectivity,PEBRisk
```

- `Ecenter_kVcm`은 중앙 **한 반경 Cutline**의 최대 전계이며 활성영역 전체의 최대값은 아니다.
- `EMask_kVcm`과 `EMask_r_um`은 Mask 끝 ±0.25 µm 내의 최대 전계와 반경 위치다.
- `AvalMask_cm3s`는 Mask 주변의 최대 Avalanche Generation이지 PEB 발생 확률이 아니다.
- `ForwardI_RelativeP0`는 P0 대비 −0.30 V Cathode 단자 전류비이며 연결성의 확정 증거가 아니다.
- `CathodeConnectivity`와 `PEBRisk`는 물리적 공간분포 검토 전 **`REVIEW_REQUIRED`**로 남긴다. 두 항목에 임의 합격·불합격 수치를 부여하지 않는다.
- 필수 입력 또는 전계 샘플링이 누락되면 **일부 값만 채운 최종 CSV를 만들지 않고 오류로 중단**한다.

### 집계 실행

1. `H2_manifest_template.csv`의 6개 행에 실제 `VBD_V`, Dark I–V CSV, Dark/Field/Cathode 지표 파일의 경로를 입력한다.
2. Cathode 연결성 및 PEB 위험에 대한 공간분포 검토가 끝나면 해당 상태값을 입력한다. 미검토 상태라면 비워 둔다.
3. 아래 명령으로 최종 결과를 만든다.

```bash
python H2_compare_cases.py H2_manifest_template.csv -o H2_results.csv
```

## 6. 실행 전 검사

1. `Mask=16.30`인 P0 한 조건을 먼저 실행하여 기존 P0 대비 VBD 및 도핑 매핑 차이를 확인한다.
2. `n<node>_fps.tdr`, 최종 PLX 6개, `n<node>_SCR_des.tdr`, `n<node>_PEB_des.tdr`, `n<node>_ATP_des.tdr`가 생성됐는지 확인한다.
3. SVisualPy의 Silicon 재료 필터 및 Electric Field/Avalanche 변수명이 설치된 Sentaurus 버전에서 정상 동작하는지 확인한다.
4. Dark I–V가 목표 평가전압에 도달하는지, 전류의 KCL 오차가 적절한지 확인한다.
5. Cathode 진단에서 단자 전류뿐 아니라 실제 전자 전류 벡터와 도핑 연결 경로를 검토한다.
6. PEB 평가 시 최대 전계·Avalanche 발생 좌표 및 Ionization 경로를 비교한다.

## 7. 코드 관리 및 검증 범위

- 이 폴더에는 실제 사용하는 13개 노드 덱이 포함되어 있다.
- `H2_prepare_decks.py`는 과거 `Electrical_Test`의 대응 파일로부터 H2 변형 덱을 다시 만들 때만 사용하는 선택적 생성 스크립트다.
- `test_h2_static.py`는 SWB 치환 후 Python 구문, 6조건·15개 입력, 14열 집계, 누락 데이터 차단 등을 **가상 데이터**로 검사한다.
- 정적 테스트를 통과했다는 기록은 **실제 Sentaurus 수렴 또는 물리적 개선 검증**을 의미하지 않는다.
- 기존 `Electrical_Test` 소스와 공통 baseline은 변경하지 않는다.

