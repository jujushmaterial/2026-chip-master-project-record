# Single-DNW (250-case Large DOE) 데이터

[상위 데이터 설명](../README.md) · [해당 SProcess/SVisualPy 코드](../../tcad/Large_DOE/README.md)

## 무엇을 확인하려고 돌렸나?

**Single-DNW**는 **DNW Phosphorus implant가 한 개**인 초기 공정 프로파일 모델이다. SDE surrogate DNW target에 근접하도록 DNW Dose/Energy, PW Fixed/Trim implant 및 common RTA를 넓게 탐색했다.

이 단계는 **SDE target을 맞출 수 있는 단일 DNW 공정 영역이 있는지 screening**하는 과정이지 실제 foundry recipe 복원이 아니다. 2주차 발표자료의 250-case LHS 구성 슬라이드(32번)에 해당한다.

## 결과 CSV

| 파일 | 종류 | 실험 구성 / 이 파일을 확보한 목적 |
|---|---|---|
| [250.csv](250.csv) | **실제 SProcess/SVisualPy 결과**, SWB 헤더 3행 + 250개 실험행 | **8개 공정변수의 LHS 250개** 결과로 PW/DNW peak·profile width·junction 등을 비교하고 Single-DNW의 형상 정합 한계를 판단 |

**8개 입력 변수:** `DNW_DOSE`, `DNW_E`, `PW_TRIM_E`, `PW_FIXED_E`, `PW_TRIM_FRAC`, `PW_TOTAL_DOSE`, `RTA_T`, `RTA_t`.

이 CSV에는 각 DOE 행의 입력 조건과 `F_PROFILE_SCORE`, `F_PW_log_profile_RMSE`, `F_DNW_log_profile_RMSE`, `F_PW_DNW_crossing_nm`, `F_DNW_peak_depth_nm`, `F_DNW_peak_cm3`, `F_DNW_sigma_equiv_nm` 등 **final-process `F_` 기반 지표**가 함께 들어 있다.

### 결과에서 다음 단계로 넘어간 이유

| 대표 조건 | 결과 | 해석 |
|---|---|---|
| SCORE 최소 (250개 중 98번째) | `F_PROFILE_SCORE=0.381788`, DNW sigma 약 **269.0 nm** | 종합 error가 가장 작다고 DNW width가 충분한 것은 아님 |
| DNW sigma 최대 (250개 중 50번째) | DNW sigma 약 **279.7 nm** | SDE target sigma **380.6 nm** 대비 약 **26.5% 부족** |

**결론:** Single-DNW만으로는 main-peak 및 width를 동시에 원하는 방향으로 맞추기 어려웠다. 이를 근거로 implant component를 **Main + Shallow Trim**으로 나눈 [Dual-DNW](../Dual-DNW/README.md) 실험으로 확장하였다.

**주의:** 이 250-case의 `F_PROFILE_SCORE`는 후속 Dual/Triple-DNW의 `SCORE`와 **동일한 계산 정의가 아니다**. 수치 크기를 직접 비교하면 안 된다.

**관련 PPT:** 첨부된 2주차 발표자료의 B-track 32번 ‘250개 대규모 실험계획법(DOE) 구성’ 슬라이드. 33번에는 당시 SProcess/SVisualPy command 원문이 포함된다.
