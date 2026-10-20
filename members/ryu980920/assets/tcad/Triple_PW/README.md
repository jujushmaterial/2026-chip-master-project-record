# Triple-PW Stage 2 SProcess — 155 keV Deep 고정 / Mid 18조건

## 1. 목적과 현재 상태

2026-10-20의 PW 도핑 프로파일 screening 후, **PW Fixed + Mid + Deep**로 구분하여 SDE surrogate baseline의 **150~350 nm Boron 부족 영역**을 보정하는 1차 Mid DOE용 SProcess 코드를 보존한다.

- **코드:** [CMP_SPAD_TriplePW_155Deep_Mid18_SProcess_v0.4.cmd](CMP_SPAD_TriplePW_155Deep_Mid18_SProcess_v0.4.cmd)
- **출처:** 기존 [Triple-DNW Stage 2 v0.3](../Triple_DNW/CMP_SPAD_TripleDNW_SProcess_v0.3_Stage2_DOE_PLX_only.txt)의 공정/마스크 흐름을 유지하면서 Mid Boron Implant, 14개 SWB 입력, Triple-PW Dose 계산을 추가한 v0.4.
- **연구 기록:** [2026-10-20 Timeline](../../../timeline/2026-10/2026-10-20.md)
- **후처리:** [PW SVisualPy v1.3.0 PeakAudit](../PW_Propile/CMP_SPAD_PW_ProfileScreening_SVisualPy_v1.3.0_PeakAudit.py)
- **상태:** 명령·DOE 설계 및 입력 파라미터 계산 확인. **이번 Triple-PW 18조건의 실제 SProcess 실행/PLX 검증 및 SDevice 검증은 미완료.** Sentaurus 엔진 실행 성공을 보장하지 않는다.

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
