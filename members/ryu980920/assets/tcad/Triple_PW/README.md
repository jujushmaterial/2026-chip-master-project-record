# Triple-PW Stage 2 SProcess — 155 keV Deep 고정 / Mid 18조건

## 1. 목적과 현재 상태

2026-10-20의 PW 도핑 프로파일 screening 후, **PW Fixed + Mid + Deep**로 구분하여 SDE surrogate baseline의 **150~350 nm Boron 부족 영역**을 보정하는 1차 Mid DOE용 SProcess 코드를 보존한다.

- **코드:** [CMP_SPAD_TriplePW_155Deep_Mid18_SProcess_v0.4.cmd](CMP_SPAD_TriplePW_155Deep_Mid18_SProcess_v0.4.cmd)
- **출처:** 기존 [Triple-DNW Stage 2 v0.3](../Triple_DNW/CMP_SPAD_TripleDNW_SProcess_v0.3_Stage2_DOE_PLX_only.txt)의 공정/마스크 흐름을 유지하면서 Mid Boron Implant, 14개 SWB 입력, Triple-PW Dose 계산을 추가한 v0.4.
- **연구 기록:** [2026-10-20 Timeline](../../../timeline/2026-10/2026-10-20.md), [2026-10-21 Timeline](../../../timeline/2026-10/2026-10-21.md)
- **후처리:** [PW SVisualPy v1.3.0 PeakAudit](../PW_Propile/CMP_SPAD_PW_ProfileScreening_SVisualPy_v1.3.0_PeakAudit.py)
- **상태 (2026-10-20 기록 시점):** 명령·DOE 설계 및 입력 파라미터 계산 확인. 당시 Triple-PW 18조건은 미실행이었다. **2026-10-21에 1차 18조건의 실제 SProcess/SVisualPy 결과를 확인했으며**, 아래 §9에서 후속 현황을 기록한다. SDevice 검증은 미완료.

본 구현은 공개문헌 제약 기반 **surrogate process**이며 foundry 제조 recipe 복원이 아니다.

## 2. SWB 연결과 의존성

- Graph: `sprocess1` (Stage 1 native STI seed) → `sprocess` (이 Stage 2 .cmd) → `svisualpy` (PW Profile Screening).
- 명령 의존성: `#setdep @node|sprocess1@`.
- 필수 seed: `n@node|sprocess1@_STI_RESTART_fps.tdr`. 기존 native STI 구조를 새로 생성하지 않고 seed에서 재시작.
- 최종 정량용 출력: `n@node@_F_r4p6.plx` (r=4.6875 µm cut; BActive/PActive). 추가로 r=0/r=13의 B/A/F PLX와 diagnostics 출력.
- 기존 SVisualPy v1.3.0에서 `#setdep @node|sprocess@`와 `n@node|sprocess@_F_r4p6.plx`를 사용한다.
- 실제 SWB `sprocess_fps.cmd`가 여기 보존된 코드와 일치하는지 실행 전 확인한다.

## 3. 고정조건 — SWB experiment row에 입력 [surrogate DOE assumption]

| 공정/조건 | 값 |
|---|---|
| DNW Case 15 total dose | 2.95×10¹³ cm⁻² |
| DNW Main / Trim / Deep Energy | 955 / 550 / 1485 keV |
| DNW Trim / Deep fraction | 0.254237288135593 / 0.237288135593220 |
| PW Fixed | **36 keV, 6.18×10¹² cm⁻²** |
| PW Deep | **155 keV, 2.8×10¹² cm⁻²** |
| PW Mid | Energy/Dose는 DOE 변수 |
| DNW+PW 공통 WELL RTA | **1050°C / 30 s, 한 번** |

주의: 기존 Stage 2에 있던 **P+ contact activation spike 1050°C/1.5 s는 별도 후속 공정으로 보존**했다. 이는 DNW/PW별로 독립 anneal을 부여하는 것이 아니다. 모든 **등록 SWB Parameter**는 코드에서 수치 하드코딩하지 않고 `@PARAMETER@`로 받는다. 고정값은 SWB experiment row로 고정한다.

## 4. Input Parameter — 총 14개, CSV 열 순서

기존 12개를 보존하고 맨 뒤에 2개만 추가한다.

| 순서 | Parameter | 역할 |
|---:|---|---|
| 1 | `DNW_DOSE` | Triple-DNW total dose |
| 2 | `DNW_E` | DNW main energy |
| 3 | `DNW_TRIM_E` | DNW trim energy |
| 4 | `DNW_DEEP_E` | DNW deep energy |
| 5 | `DNW_TRIM_FRAC` | DNW trim fraction |
| 6 | `DNW_DEEP_FRAC` | DNW deep fraction |
| 7 | `PW_TRIM_E` | **PW Deep energy** (레거시 이름 유지) |
| 8 | `PW_FIXED_E` | PW Fixed energy |
| 9 | `PW_TRIM_FRAC` | **PW Deep dose/Total dose** (레거시 이름 유지) |
| 10 | `PW_TOTAL_DOSE` | PW Fixed+Mid+Deep dose 합 |
| 11 | `RTA_T` | 공통 WELL RTA 온도 |
| 12 | `RTA_t` | 공통 WELL RTA 시간 |
| 13 | `PW_MID_E` | **신규 Mid energy** |
| 14 | `PW_MID_DOSE` | **신규 Mid dose** |

`PW_FIXED_FRAC`, `PW_MID_FRAC`는 **SWB Input Parameter가 아닌 계산 파생값**이다. 혼동 방지를 위해 `PW_TRIM_*` 명칭은 유지하되 이번 단계에서는 **Deep PW**를 지칭한다.

## 5. Dose 계산 방식

```text
PW_TRIM_DOSE  = PW_TOTAL_DOSE * PW_TRIM_FRAC    # Deep PW
PW_FIXED_DOSE = PW_TOTAL_DOSE - PW_TRIM_DOSE - PW_MID_DOSE
PW_FIXED_FRAC = PW_FIXED_DOSE / PW_TOTAL_DOSE
PW_MID_FRAC   = PW_MID_DOSE / PW_TOTAL_DOSE
```

| Mid Dose [cm⁻²] | Fixed Dose [cm⁻²] | Deep Dose [cm⁻²] | Total PW Dose [cm⁻²] | PW_TRIM_FRAC |
|---:|---:|---:|---:|---:|
| 3×10¹² | 6.18×10¹² | 2.8×10¹² | 1.198×10¹³ | 0.23372287145242070 |
| 6×10¹² | 6.18×10¹² | 2.8×10¹² | 1.498×10¹³ | 0.18691588785046729 |
| 9×10¹² | 6.18×10¹² | 2.8×10¹² | 1.798×10¹³ | 0.15572858731924360 |

동일한 Fixed/Deep 절대 Dose를 유지하기 위해 Total과 fraction은 **Mid Dose에 따라 연동**한다. 별도로 SWB 값을 무작위 Cartesian sweep하면 관계가 깨질 수 있으므로 **실험 행별 pairing을 유지**한다. Code의 Fixed/Total 양수 검증도 적용된다.

## 6. Mid 18조건 DOE — 9개씩 분할 [surrogate DOE assumption]

| Group | Mid Energy [keV] | Mid Dose [cm⁻²] | 조건 |
|---|---|---|---:|
| 1 | 65 / 75 / 85 | 각 3 / 6 / 9×10¹² | 9 |
| 2 | 70 / 80 / 90 | 각 3 / 6 / 9×10¹² | 9 |
| **합계** | **6수준** | **3수준** | **18** |

18개 입력 CSV 전체와 Group1/Group2 9조건 파일은 로컬에서 제작 및 산술 검산했지만, **이번 GitHub 보존 범위에는 CSV 자체를 포함하지 않았다.** 사용자 제공 Group2 SWB CopyPasteData에서는 14개 Parameter 등록 및 9개 experiment 조합이 정합하는 것을 확인했으며, 이것은 **실제 SProcess 실행 완료를 의미하지 않는다**.

## 7. 평가 지표와 주의점

- 목표: Mid Implant로 **150~350 nm BActive 부족분**을 줄이되 350~500 nm Tail 과다와 **462.6966588 nm B462_R 초과**를 감시한다.
- Mid Implant 영향은 특정 깊이 구간에만 국한되지 않는다. 주입 Tail이 깊은 농도에 기여할 수 있다.
- 462.6966588 nm는 SDE 기준 **BActive/PActive doping crossover anchor**이고 실제 SDevice SCR 중심은 아니다.
- v1.3.0의 `PW12_SCORE`, `PW12_MAIN_R`, `PW12_B462_R`, `PW12_REBOUND_R`, SECOND PEAK 계열 Output을 동일 버전으로 비교한다. `SPLIT_OK=0`만으로 신규 Triple-PW 조건을 자동 탈락시키지 않는다.
- 최종 판단에는 SDE 대비 **150~350 nm 부족 적분**, **350~500 nm 초과 적분**, junction-side crossover 위치를 PLX 원시 데이터에서 확인해야 한다.
- VBD, SCR, avalanche/PEB, ATP, dark current 및 온도 특성은 **별도 SDevice 검증이 필요하다**.

## 8. 파일 관리

- 이 폴더는 **Triple-PW Stage 2 공정 코드와 설명**을 보존한다. 기존 `Triple_DNW` 원본, `PW_Propile` 분석기 원본을 덮어쓰지 않는다.
- 재현에 필요한 `sprocess1` STI seed/리소스는 현재 SWB 프로젝트의 Stage 1을 사용한다.
- 추가 변경 시 `v0.4`를 조용히 덮어쓰지 말고 버전 변경과 Timeline의 의사결정 근거를 함께 기록한다.

---

## 9. 2026-10-21 실제 1차 Mid 결과와 후속 DOE

### 9.1 완료된 1차 Triple-PW Mid 18조건 (65~90 keV)

10월 20일 설계한 1차 DOE **Group1 (65/75/85 keV) 9조건 + Group2 (70/80/90 keV) 9조건**은 다음 날 실제 결과 `1020A.csv`, `1020B.csv`로 회수·분석되었다. 동일한 SVisualPy v1.3.0 PeakAudit에서:

| 결과 | 18조건 집계 |
|---|---:|
| PW12_RUN_OK=1 | **18/18** |
| PW12_SPLIT_OK=1 | **16/18** |
| PW12_ALL_OK=1 | **12/18** |
| PW12_SECOND_FOUND=1 | **11/18** |
| 최저 PW12_SCORE | **29.3376483366** |

- 최저 SCORE: **Mid 80 keV / 9×10¹² cm⁻²**, MAIN_R **1.00230482958**, B462_R **1.01569023746**. 내부 screening에서는 유망하지만 SDE와의 깊이별 잔차가 남는다.
- 85 keV / 9×10¹²: SCORE **34.4511621648**, MAIN_R **0.958232549563**, B462_R **1.04486825776**, SECOND Peak 약 **240 nm**. 사용자 SDE 오버랩에서 0.5~0.65 µm 일부 구간의 Boron 부족이 관찰되었다.
- 85 keV에서는 Mid Dose 3/6/9×10¹²를 비교했다. 높은 Dose는 Main·Mid 농도를 높이지만 Shoulder 및 Junction-side 과다농도와 trade-off가 있다.
- **SPLIT_OK=1은 두 번째 피크가 모두 사라졌다는 의미가 아니다.** 지표는 SVisualPy의 잠정 surrogate criteria이다.
- 462.6966588 nm는 SDE BActive/PActive 도핑 교차 anchor이며 실측 Junction 또는 SDevice SCR가 아니다.

### 9.2 후속 고Energy·저Dose 18조건 (설계 완료 / 시뮬레이션 전)

**의사결정:** 기존 SCORE의 Main Peak 항목이 좋은 후보라도 0~150 nm/약 0.5~0.65 µm의 SDE 오버랩 잔차가 남는다. 이번에는 Mid 분포를 깊게 이동시키고 Dose를 낮추는 방향을 실험하되, Main_R 감소는 별도 Shallow 보정 전까지 기록하여 추후 평가한다. 이것은 **개선이 검증된 결론이 아닌 실험 가설**이다.

| 그룹 | PW_MID_E [keV] | Energy별 PW_MID_DOSE [×10¹² cm⁻²] | 조건 |
|---|---|---|---:|
| Group1 | 87.5 / 92.5 / 97.5 | 4.5/5.5/6.5 ; 3.0/4.0/5.0 ; 2.0/3.0/4.0 | 9 |
| Group2 | 90 / 95 / 100 | 3.5/4.5/5.5 ; 2.5/3.5/4.5 ; 1.5/2.5/3.5 | 9 |
| **합계** | **6개 Energy** | **각 3개 Dose** | **18** |

- Full-factorial 공통 Dose grid가 아닌 **Energy별 dose-adjusted screening**. Dose 수준이 다르므로 Energy 주효과는 바로 분리할 수 없다.
- **기존 14개 SWB Parameter 순서 및 Triple-PW SProcess v0.4 그대로 사용**. Fixed 36 keV/6.18×10¹², Deep 155 keV/2.8×10¹², DNW Case15, common WELL RTA 1050°C/30s 유지.
- `PW_TOTAL_DOSE = Fixed + Mid + Deep`, `PW_TRIM_FRAC = Deep/PW_TOTAL_DOSE`를 각 SWB Experiment에서 동기화. 전체18 및 Group1/Group2 각9 CSV **산술 검증 완료**.
- 새 CSV 파일은 이 GitHub 커밋에 **포함하지 않음**. 현재 후속 18조건에 대한 **Sentaurus 결과는 미확보**.

### 9.3 다음 검증

- 약 **0.5~0.65 µm**에서 SDE BActive 부족이 감소했는지, **350~500 nm**의 초과농도와 **462.7 nm B462_R**이 어떻게 변화하는지 별도로 비교한다.
- **150~350 nm** Shoulder/Second Peak를 확인하고, 0~150 nm의 Main Peak 및 표면 차이는 후속 Shallow/Surface 보정 대상으로 분리한다.
- 후보별 Final PLX의 구간별 부족/초과 적분 및 BActive=PActive 실제 crossing 위치를 추출한 뒤 SDevice **VBD/SCR/field/PEB/ATP/dark-current/온도** 검증으로 이어간다.

상세 판단 근거와 활동의 완료/미완료 구분: [2026-10-21 연구일지](../../../timeline/2026-10/2026-10-21.md).

---

## 10. 2026-10-23 고Energy·저Dose 결과와 ABC108 후속 DOE

### 10.1 고Energy·저Dose Mid 18조건 실행 결과

10월 21일 설계했던 **87.5~100 keV / Energy별 저Dose Mid 18조건**은 `1021A.csv`, `1021B.csv`로 결과를 회수하여 SVisualPy v1.3.0 및 SDE 오버랩을 검토했다. 이 절은 10월 21일 설계 당시의 §9.2 **'실행 전' 기록을 덮어쓰지 않는 후속 결과**이다.

| 지표 | 직전 1차 Mid DOE | 후속 고Energy·저Dose Mid DOE |
|---|---:|---:|
| RUN_OK | 18/18 | 18/18 |
| SPLIT_OK | 16/18 | 12/18 |
| ALL_OK | 12/18 | 4/18 |
| SECOND_FOUND | 11/18 | 18/18 |
| 최저 SCORE | 29.33765 | 38.46906 |

- 새 DOE의 최저 SCORE 후보는 **87.5 keV / 6.5×10¹² cm⁻²**이다(`MAIN_R=0.88926`, `B462_R=1.02792`, `REBOUND_R=0.02851`).
- Mid Dose **4.5×10¹² cm⁻² 고정**에서 87.5/90/95 keV 순으로 SCORE **38.61190/40.96787/45.68923**, MAIN_R **0.85290/0.84581/0.83374**, B462_R **0.99975/1.01087/1.04183**, REBOUND_R **0.00512/0.01943/0.05892**.
- PLX 시각비교에서도 87.5 keV 후보가 90/95 keV 대비 Main–Mid 구간의 SDE 기준형상에 가까웠다. 따라서 **고Energy·저Dose에서 의도한 profile-shape 개선은 확인되지 않았고**, 저Energy·고Dose 및 다중 PW 주입 보정 방향으로 전환했다.
- 0.5~0.65 µm 깊이의 부족 여부는 **원시 PLX의 구간별 오차 적분 전에는 확정하지 않는다**. SCORE는 전기적 소자 성능의 직접 척도가 아니다.

### 10.2 PLX 직접비교에 따른 세 Implant 보정 방향

| 구간/변수 | 보정 방향 [surrogate DOE assumption] | 목표 및 제약 |
|---|---|---|
| PW Fixed (Shallow) | Energy 36 keV 유지, Dose 6.18→최대 9.0×10¹² | Peak 위치 유지 및 농도 보정; Mid 기여와 과보정 감시 |
| PW Mid | Energy 70~85 keV 방향으로 낮추고 Dose 5~11×10¹² 탐색 | Main–Mid 부족 보완; Second Peak·Shoulder 감시 |
| PW Deep (레거시 `PW_TRIM_E`) | Energy 155→145~150 keV, Dose 2.8→최대 3.6×10¹² | Mid–Deep 연결부 보완 가설; B462_R/깊은 Tail·도핑 교차 변화 감시 |

세 주입의 BActive 기여는 공간적으로 겹친다. **Shallow, Mid, Deep 농도를 각자 독립된 세 영역에서만 변화시킨다는 가정은 사용하지 않는다.**

### 10.3 3일 무인 병렬 실행을 위한 ABC108

실행 중 추가 조합 설계/피드백 반영이 어려워 **A·B·C 그룹 각 36행, 총 108행**을 사전에 확정했다.

| 그룹 | Shallow Dose [×10¹²] | Mid Energy [keV] | Mid Dose [×10¹²] | Deep Energy [keV] | Deep Dose [×10¹²] | 행 |
|---|---|---|---|---|---|---:|
| **A** | 6.18 / 7.6 / 9.0 | 70 / 75 / 80 | 5 / 7 / 9 / 11 | 155 | 2.8 | 36 |
| **B** | 6.18 | 75 / 85 | 5 / 7 / 9 | 145 / 150 / 155 | 2.8 / 3.4 | 36 |
| **C** | 7.0 / 8.0 / 9.0 | 70 / 75 / 80 | 6 / 8 | **(150, 3.2), (145, 3.6) 쌍** | 왼쪽 Energy와 쌍 지정 | 36 |
| **합계** | | | | | | **108** |

- Group C Deep Energy/Dose는 쌍으로 설정한다. 독립적인 Deep Energy/Dose 효과는 Group B를 활용해 해석한다.
- Group A와 B 사이에 같은 Shallow 6.18/Deep 155·2.8/Mid 75·(5,7,9)의 **3중복 조건**이 존재하여, **실행 행 108 / 고유 조합 105**이다.
- 기존 정상 분석된 **Mid 80 keV/9×10¹², Shallow 6.18, Deep 155/2.8**(A) 및 **Mid 85 keV/9×10¹², Shallow 6.18, Deep 155/2.8**(B)를 포함한다.
- DNW Case 15와 WELL 공통 RTA 1050°C/30s, `PW_FIXED_E=36` keV를 고정한다. PW Shallow Energy는 고정하되 **Dose는 A/C에서 변화**한다.
- 조건당 `PW_TOTAL_DOSE=Shallow+Mid+Deep`, `PW_TRIM_FRAC=Deep/PW_TOTAL_DOSE`를 계산하여 기존 14개 SWB Input Parameter와 일관되게 연결한다. `PW_FIXED_DOSE`는 내부 파생값이고 별도 SWB Input Parameter가 아니다.

사용자 제공 스크린샷에서 **A/B 그룹의 일부 SWB 입력 열과 셀 그룹화**를 확인했다. **CSV 108행의 산술 검증 완료**와 **SWB 전체 import/3일간의 실제 SProcess 성공**은 별개이다.

### 10.4 생성 DOE 파일 및 연구 상태

로컬에서 생성·검산한 파일명:

- `CMP_SPAD_TriplePW_ABC108_GroupA_36_SWB_14Params_NoIndex.csv`
- `CMP_SPAD_TriplePW_ABC108_GroupB_36_SWB_14Params_NoIndex.csv`
- `CMP_SPAD_TriplePW_ABC108_GroupC_36_SWB_14Params_NoIndex.csv`
- `CMP_SPAD_TriplePW_ABC108_ALL108_SWB_14Params_NoIndex.csv`
- `CMP_SPAD_TriplePW_ABC108_DOE_설계및검증.md`

**이 GitHub 변경에는 DOE CSV, PLX 원본 및 그래프 이미지 파일을 업로드하지 않았다.** SProcess v0.4의 등록 SWB Parameter 매크로와 공정 코드를 변경하지 않았다.

다음 단계는 108조건의 Final PLX 수집, **0~150 / 150~350 / 350~500 / 500~650 nm**의 SDE 대비 부족·초과 정량화, `B462_R` 및 실제 도핑 교차 위치 확인이다. 최종 electrical equivalent baseline의 SDevice VBD/SCR/field 검증과 B의 PEB/dark-current/ATP/온도 평가는 여전히 후속 과제다.

상세 결과와 방향 전환 근거: **[2026-10-23 연구일지](../../../timeline/2026-10/2026-10-23.md)**.
