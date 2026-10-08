# Triple-DNW surrogate profile calibration

## 목적 및 연구 단계

이 폴더는 CMP 28 nm FD-SOI SPAD B-track의 **문헌 제약 기반 surrogate baseline doping-profile calibration** 중 Triple-DNW 실험을 기록한다. ST의 실제 foundry recipe를 복원하는 작업이 아니다.

2026-09-28 이후 108-case Dual-DNW refinement에서 main DNW peak가 비교적 잘 맞는 후보에서도 1.4–1.8 µm deep-side phosphorus tail 부족이 남았다. 이에 Main + Shallow/Trim에 **Deep DNW implant**를 추가해 deep-tail profile을 별도로 탐색했다.

이 폴더의 결과는 **profile screening**이며, SDevice VBD/SCR/field/avalanche verification 또는 baseline freeze가 완료되었다는 의미가 아니다.

## 파일 목록과 원본 상태

| 파일 | 역할 | 확인·보존 상태 |
|---|---|---|
| `CMP_SPAD_TripleDNW_ProfileScreening_SVisualPy_v0.4_DeepTail.py` | 45-case profile metrics 및 1.4/1.6/1.8 µm tail 추출 | 2026-10-06 생성된 전체 Python 원문 확인 후 보관 |
| `1006A.csv` | 첫 Triple-DNW 시뮬레이션 결과 Part A | 사용자가 전달한 23개 데이터 행의 원본 CSV 보관 |
| `1006B.csv` | 첫 Triple-DNW 시뮬레이션 결과 Part B | 사용자가 전달한 22개 데이터 행의 원본 CSV 보관 |
| `CMP_SPAD_TripleDNW_FinalSweep_Part1.csv` | 첫 DOE 입력 Part 1 (23 cases) | 이전 산출물의 인덱싱된 CSV 데이터에서 표 내용을 복원하여 보관 |
| `CMP_SPAD_TripleDNW_FinalSweep_Part2.csv` | 첫 DOE 입력 Part 2 (22 cases) | 이전 산출물의 인덱싱된 CSV 데이터에서 표 내용을 복원하여 보관 |
| `CMP_SPAD_TripleDNW_MainToDeep_FineSweep_25cases.csv` | 후속 5 × 5 DOE **설계 입력** | 이전 산출물의 인덱싱된 CSV 데이터에서 표 내용을 복원하여 보관 |

**보존 주의:** 이전에 생성한 세 DOE 입력 CSV는 보관함에서 읽은 표의 열과 수치를 유지하되 CSV 텍스트로 재직렬화했다. 따라서 원래 파일과 바이트·숫자 표기 방식이 동일하다고 주장하지 않는다. `1006A.csv`·`1006B.csv`는 전달된 SWB 3행 헤더와 데이터 행을 그대로 유지한다.

## 첫 Triple-DNW DOE: 45-case 결과

- 결과 CSV: `1006A.csv`의 23행 + `1006B.csv`의 22행 = **총 45개 실행 결과**
- `DNW_DEEP_E`: **1300 / 1400 / 1500 / 1600 / 1700 keV**
- 총 DNW Dose: **2.50e13–2.90e13 cm^-2**, 9개 수준
- 설계 목적: Main absolute dose **1.80e13 cm^-2**와 Shallow/Trim absolute dose **6.00e12 cm^-2**를 고정하고 Deep contribution을 추가하여 깊은 tail 개선 여부를 확인
- 주입 후 DNW/PW 별도 anneal이 아니라 공통 WELL RTA 1회 적용
- 과거 '48 cases' 언급과 달리, 현재 보존된 실제 결과는 45행이다. 차이 3개가 control/실패/미실행 중 무엇인지는 확인되지 않았다.

Composite SCORE만으로 최적점을 결정하지 않는다. 1700 keV 계열은 `DNW_SIG`와 SCORE에서는 유리하지만 위치별 tail이 deep-heavy해질 수 있다. 1500 keV 일부 조건은 1.4/1.6/1.8 µm tail ratio 균형 면에서 유리하다.

### SVisualPy v0.4 출력 및 해석 주의

기존 10개 DOE metric `SCORE`, `PW_RP`, `PW_PK_R`, `DNW_RP`, `DNW_PK_R`, `DNW_SIG`, `JUNC`, `P462_R`, `SLOPE_R`, `SPLIT` 외에:

- `TAIL14_R`, `TAIL16_R`, `TAIL18_R`
- `TAIL_RMSE`

가 추가됐다. 원문 코드의 설명에 따라 deep-tail ratio/RMSE의 비교 reference는 아직 **analytic Gaussian DNW target**이다. 최종 full SDE reference PLX를 코드에 연결해 직접 spatial reference로 썼다고 서술하지 않는다. `SCORE` 계산에는 새 tail metric이 가산되지 않는다.

## 다음 DOE: Main-to-Deep redistribution 25 cases

**설계 입력 완료, 실행 결과 확인 전.**

- `DNW_DEEP_E`: 1500 / 1525 / 1550 / 1575 / 1600 keV
- `DNW_DEEP_FRAC`: 0.172413793 / 0.189655172 / 0.206896552 / 0.224137931 / 0.241379310
- 5 × 5 = 25개 입력 조합
- 고정: `DNW_DOSE=2.90e13`, `DNW_E=975`, `DNW_TRIM_E=550`, `DNW_TRIM_FRAC=0.206896552`, PW 조건, common RTA
- `DNW_MAIN_FRAC = 1 - DNW_TRIM_FRAC - DNW_DEEP_FRAC` (종속 계산)

의도는 **전체 Dose와 Shallow absolute dose를 유지하면서 Main dose 일부를 Deep으로 재분배**하여 과도한 main peak 농도를 낮추고 부족한 deep-tail을 보강할 수 있는지 확인하는 것이다. 개선은 아직 실험으로 검증된 결론이 아니다.

## 추후 추가해야 할 원본 자료

다음은 2026-10-06~08 이전 대화에서 공유·작성한 기록은 있으나, 이 폴더를 구축할 당시 원본 전체 내용을 직접 다시 읽을 수 없어 **업로드하지 않았다**.

1. **Triple-DNW SProcess v0.3 command 원문**: 대화에서 세 phosphorus implant와 공통 WELL RTA, `DNW_DEEP_E` / `DNW_DEEP_FRAC` 사용을 확인했지만 파일 전체 원문이 현재 접근 가능한 보관함에는 없음. 다른 버전으로 추정·재작성해 원본인 것처럼 저장하지 않는다.
2. **대표 Triple-DNW PLX 원본**: n545, n562, n606의 `A_R_r4p6` / `F_r4p6` 등은 이전 대화에서 언급됐으나 full PLX의 데이터 행을 확보하지 못했다. node별 Energy/Fraction 매핑은 결과와 직접 대조하여 확정할 것.
3. **Dual-DNW 및 SDE reference PLX**: n72/n124 `A_R`·`F` 및 SDE baseline PLX는 비교 근거로 별도 확인이 필요하다. Dual-DNW 자산과의 연결을 혼동하지 않는다.

### SProcess 원문을 확보했을 때 필수 검증

SWB에 등록된 항목은 sweep 여부와 관계없이 command에서 반드시 `@PARAMETER@`로 참조한다. 최신 Triple-DNW 기준 검토 대상:

```text
DNW_DOSE, DNW_E, DNW_TRIM_E, DNW_DEEP_E,
DNW_TRIM_FRAC, DNW_DEEP_FRAC,
PW_TRIM_E, PW_FIXED_E, PW_TRIM_FRAC, PW_TOTAL_DOSE,
RTA_T, RTA_t
```

`PW_FIXED_FRAC`와 `DNW_MAIN_FRAC`은 독립 DOE parameter로 다시 도입하지 않고 종속 계산한다. PW 조건·공통 RTA·STI 구조를 임의로 바꾸지 않는다.

## 후속 분석

Triple-DNW profile 후보 선정 후 PW Energy로 junction/SCR 위치를 SDE baseline에 맞추고, TDR-enabled SProcess → SDevice에서 VBD, SCR, field, avalanche 및 PEB 관련 거동을 검증해야 한다.

기존 파일: `../Dual_DNW/README.md`. 날짜별 기록: `../../../timeline/2026-10/` (로그 작성·갱신은 별도 작업).
