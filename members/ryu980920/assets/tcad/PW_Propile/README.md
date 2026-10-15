# PW_Propile — PW-only SVisualPy (v1.0 원본 + v1.2.1 CompactDOE)

2026-10-12 CMP2에서 제작한 **PW 중심 profile-screening v1.0 원본**과 2026-10-15에 실제 27조건 분석에 사용한 **v1.2.1 CompactDOE 최종판**을 함께 보관한다. 폴더명 `PW_Propile`은 요청한 표기를 따른다. 이 작업은 공개 문헌 제약 기반 **surrogate baseline** 재현에 속하며, 실제 파운드리 레시피를 복원하거나 전기적 baseline을 확정한 결과가 아니다.

## 1. 배경과 파일

[Triple-DNW v0.4](../Triple_DNW/CMP_SPAD_TripleDNW_ProfileScreening_SVisualPy_v0.4_DeepTail.md)의 composite SCORE는 PW 직접 항목 15%, DNW 직접 항목 45%, 공동 지표 35%, Split 5%로 구성되었다. 따라서 DNW 조건을 고정한 PW DOE에서는 PW의 shallow peak 및 junction-side tail에 집중하는 별도 분석이 필요했다.

- [CMP_SPAD_PW_ProfileScreening_SVisualPy_v1.0.py](CMP_SPAD_PW_ProfileScreening_SVisualPy_v1.0.py): CMP2 원본 455줄을 **변경 없이 보존**.
- [CMP_SPAD_PW_ProfileScreening_SVisualPy_v1.2.1_CompactDOE.py](CMP_SPAD_PW_ProfileScreening_SVisualPy_v1.2.1_CompactDOE.py): **2026-10-15 최종판**, SDE 실측이 아닌 **SDE 원본 PLX 수치 샘플**과 직접 비교하며 SWB 지표를 8개만 출력.
- `README.md`: 코드 사용법·지표·근거·한계 설명.
- PW DOE 입력: [27조건 CSV](../../data/PW_Propile/CMP_SPAD_PW_Case27_27DOE_SWB.csv) ([데이터 README](../../data/PW_Propile/README.md)). 아직 SProcess 결과가 아닌 입력표다.
- CMP2의 원본 `.py`와 `.txt` 내용은 동일하므로 동일 코드의 중복 사본은 올리지 않는다.
- SProcess는 기존 [Triple-DNW Stage 2 v0.3](../Triple_DNW/CMP_SPAD_TripleDNW_SProcess_v0.3_Stage2_DOE_PLX_only.txt)을 그대로 사용한다.

## 2. v1.0 입력과 실행 흐름 (아래 2~8절은 원본 버전 설명)

```text
공통 STI Stage 1 restart
 -> Triple-DNW SProcess Stage 2
 -> DNW/PW implant -> common WELL RTA
 -> post-RTA A_R_r4p6.plx (필수)
 -> final F_r4p6.plx (선택)
 -> PW-only SVisualPy v1.0 -> PW metrics / CSV / graphs / SWB DOE
```

- SWB 연결: `#setdep @node|sprocess@`, 노드 변수 `@node@`와 `@node|sprocess@`.
- 필수 입력: `n{SNODE}_A_R_r4p6.plx` (BActive, PActive); 선택 입력: `n{SNODE}_F_r4p6.plx`.
- r=4.6875 µm depth cut을 사용한다. BActive/PActive의 독립 x/y pair도 읽고 필요하면 depth를 보간한다.
- **SWB SCORE는 post-RTA A** 프로파일로 계산한다. Final F는 별도 진단한다.
- DNW PActive는 **BActive=PActive crossing(JUNC)** 계산에만 쓰며 DNW 점수·peak·sigma·tail 지표는 계산하지 않는다.

## 3. PW 27조건 DOE

DNW는 81조건 중 최저 SCORE인 **1009B Case 27**로 고정한다.

| 고정 DNW | 값 |
|---|---|
| Total dose | 2.95e13 cm^-2 |
| Main E / dose | 975 keV / 1.60e13 cm^-2 |
| Trim E / dose | 550 keV / 6.50e12 cm^-2 |
| Deep E / dose | 1525 keV / 7.00e12 cm^-2 |

PW는 **Trim Energy 85/90/95 keV × Trim Fraction 0.500–0.700 (0.025 간격, 9수준) = 27조건**이다. PW Fixed E=36 keV, Total PW Dose=2.06e13 cm^-2, common RTA=1050 °C/30 s는 SWB experiment row에서 고정한다. 기존 Case 27의 PW 조건(85 keV, 0.525)을 포함한다. 27조건은 **2026-10-12 시점에 설계 완료** 상태였으며 당시 시뮬레이션 결과는 아직 확인되지 않았다. **이후 2026-10-15에 27개 결과를 v1.2.1로 재평가함**(아래 10~13절).

SWB에 등록된 Parameter는 현재 sweep하지 않더라도 SProcess command에서 `@PARAMETER@`로 연결해야 한다. 기존 Stage 2에 `PW_FIXED_FRAC=1-PW_TRIM_FRAC` 계산이 존재하므로 실제 SWB에서 `PW_FIXED_FRAC`를 별도 등록했다면 코드와 등록 목록을 후속 점검해야 한다. 이 보관 작업에서는 SProcess를 변경하지 않는다.

## 4. Target과 깊이 구간

| 항목 | 기준 |
|---|---|
| SDE PW peak | 109.3 nm / 5.954e17 cm^-3 |
| SDE PW/DNW active crossing | 462.6966588 nm / 1.159e17 cm^-3 |
| PW peak search | 30–250 nm |
| Shallow shape | 30–200 nm |
| Tail sigma | 200–500 nm |
| Tail score RMSE | 300–500 nm |
| All sigma | 0–600 nm |
| Junction first crossing search | 100–900 nm |

현재 전체 SDE PLX를 직접 읽지 않는다. PW Shape/Tail의 reference는 SDE peak anchor와 `sigma=200 nm`, 배경 1e15 cm^-3을 이용한 **analytic Gaussian surrogate**이다. 462.7 nm의 crossing 농도는 따로 추출한 SDE anchor라 Gaussian 참조곡선과 일치한다고 가정하지 않는다. Shallow/Tail은 최종 PW curve의 **깊이 구간**이지 implant별 농도 분해값이 아니다.

## 5. PW-only SCORE (v1.0 원본)

```text
bounded(e) = e/(1+e), e>=0
ratio_penalty(a,t) = bounded(|log10(a/t)| / log10(1.20))
rp_penalty = bounded(|Rp_nm-109.3| / 20)
rmse_penalty = bounded(RMSE_dex / 0.10)

PW_SCORE = 100 * (
  0.25 * peak_ratio_penalty +
  0.10 * Rp_penalty +
  0.15 * shallow_shape_penalty +
  0.25 * tail_rmse_penalty +
  0.20 * PW462_ratio_penalty +
  0.05 * PW_split_penalty
)
```

낮을수록 유리하나 **퍼센트 오차가 아닌 surrogate profile-matching 점수**이며 DNW v0.4 SCORE와 서로 비교할 수 없다. PW462 깊이가 Tail RMSE 구간에도 포함되어 있으므로 해당 위치는 의도적으로 추가 강조된다. **JUNC는 SCORE에 직접 포함되지 않는다.**

## 6. SWB 출력 변수 10개

| 변수 | 의미 |
|---|---|
| `PW_SCORE` | PW-only weighted bounded score |
| `PW_SH_RP` | PW main peak depth (nm; 목표 109.3) |
| `PW_SH_PK_R` | PW peak / SDE peak (ratio) |
| `PW_SH_SIG` | 30–200 nm window equivalent sigma (nm) |
| `PW_TAIL_SIG` | 200–500 nm window equivalent sigma (nm) |
| `PW_TAIL_RMSE` | 300–500 nm log concentration RMSE (dex) |
| `PW462_R` | 462.697 nm BActive / 1.159e17 (ratio) |
| `JUNC` | 첫 BActive=PActive crossing (nm) |
| `PW_SPLIT` | 두 봉우리와 valley를 이용한 split severity |
| `PW_ALL_SIG` | 0–600 nm window equivalent sigma (nm) |

Sigma는 배경 농도를 제외한 concentration-weighted window standard deviation이며 **개별 이온 주입의 straggle이 아니다**. `JUNC`는 metallurgical doping crossing이며 **SCR center가 아니다**.

## 7. 출력 파일 / 그래프

모든 파일 접두사는 `n{VIS_NODE}_PW_v1p0`이다.

- `*_metrics.txt`: post-RTA 및 optional final 상세 지표, SCORE 구성요소, SWB 요약.
- `*_AR_compare.csv`: 0–600 nm SProcess BActive / Gaussian surrogate.
- `*_AR_shallow_plot.csv`: 0–250 nm shallow 비교 데이터.
- `*_AR_tail_plot.csv`: 200–500 nm tail 비교 데이터.
- `*_F_compare.csv`: final PLX가 있으면 추가 생성.
- SVisual plot: shallow, tail 두 개의 log-concentration overlay; SWB `DOE:` 핵심 변수 10개.

Plot 오류는 warning 처리하도록 작성되었지만 **실제 SWB end-to-end 정상 실행이 확인된 것은 아니다**.

## 8. 한계와 후속 검증

1. Gaussian surrogate와 SDE full PLX는 구분한다. PW462 추출 anchor도 별도 기준이다.
2. shape/tail RMSE는 sampled depth의 단순 평균이며 비균일 PLX grid에 민감할 수 있다.
3. split 판정의 moving average는 5개 sample index 기반이다.
4. 첫 crossing만 JUNC로 표시하고 여러 crossing의 수는 상세 TXT에 기록한다.
5. PW 후보를 DNW fine-DOE 후보와 결합한 뒤 final profile, SDevice VBD/SCR/field/avalanche 등을 재검증해야 한다.
6. 개선 시 v1.0 원본을 덮어쓰지 않고 별도 버전으로 관리한다.

## 9. 기록

- [2026-10-09: 25→81 설계](../../../timeline/2026-10/2026-10-09.md)
- [2026-10-12-1: 81결과와 DNW 27조건](../../../timeline/2026-10/2026-10-12-1.md)
- [2026-10-12-2: PW 27조건과 PW 분석기](../../../timeline/2026-10/2026-10-12-2.md)

**v1.0 당시 상태:** 원본 저장 완료, DNW/PW 각 27조건 DOE 설계 완료. 이후 현황은 아래 10~13절 및 2026-10-15-1/2 연구일지를 우선 참조.

---

## 10. v1.2.1 CompactDOE — 실제 27조건 분석에 사용한 최종 버전

### 목적과 v1.0 대비 변경점

| 항목 | v1.0 (보존) | v1.2.1 CompactDOE (추가) |
|---|---|---|
| SDE reference | Peak/Junction anchor + Gaussian surrogate | **원본 SDE PLX BActive/PActive 수치 샘플을 코드에 포함** |
| 주 평가 profile | **Post-RTA A 필수**, Final F 선택 | **Final F 필수**: n{SNODE}_F_r4p6.plx |
| Main Peak | Interior Peak와 농도비 | Shallow 30~170 nm Main Peak와 농도비 |
| Shallow 구간 | 30~200 nm | **30~110 nm** |
| Shoulder | 별도 정합 가중치 없음 | **110~350 nm** |
| Junction-side Tail | 300~500 nm | **350~600 nm** |
| Split | SCORE 5% | **SCORE 10% + REBOUND_R ≤ 5% 별도 잠정 제약** |
| 위치별 농도비 | 일부 anchor | **50~600 nm, 15개 깊이별 실제 BActive/SDE 비율** |
| SWB DOE 출력 | 10개 변수 | **8개 변수로 간소화** |
| 상세 자료 | v1.0 접두사 | v1.2.1 접두사의 metrics.txt, depth_points.csv, profile_F.csv |

SDE 원본 PLX 샘플을 코드에 포함했지만 이는 **SDE 기준 TCAD 프로파일**이지 실제 제작 소자에서 측정한 doping data가 아니다. Gauss surrogate에서 실제 SDE 기준곡선으로 변경했으므로 **v1.0 SCORE와 v1.2.1 SCORE의 절댓값은 직접 비교 불가**다.

### 실행

- SWB dependency: #setdep @node|sprocess@.
- 필수 입력: **n@node|sprocess@_F_r4p6.plx** (BActive, PActive). 변수명과 깊이축이 유효해야 한다.
- 분석 cut: **r=4.6875 µm**, SDE 원본 동일 cut.
- 참조 샘플은 코드에 내장하므로 별도 SDE PLX 파일 복사 불필요.
- 실제 Sentaurus SWB의 27조건에서 **PW12_RUN_OK=1, 27/27**을 확인했다. 정상 계산과 분석 결과를 확인한 것이며 **SDevice VBD/SCR 검증은 아니다**.

### SCORE 정의 [surrogate scoring assumption]

SCORE는 모든 세부 오차를 유한한 penalty로 바꾼 뒤 가중 합산한 **0~100 scale mismatch 점수**로, **낮을수록 좋다**. 절대 농도 정합률(%)과 동일시하지 않는다.

| SCORE 요소 | 가중치 |
|---|---:|
| Shallow Main Peak 위치 오차 | 10% |
| Main Peak 농도 오차 | 10% |
| Shallow 30~110 nm Peak-normalized log shape RMSE | 10% |
| Shoulder 110~350 nm Peak-normalized log shape RMSE | 20% |
| Tail 350~600 nm Peak-normalized log shape RMSE | 25% |
| 462.6966588 nm BActive 농도비 오차 | 15% |
| Split rebound penalty | 10% |
| **합계** | **100%** |

모든 구간 형상 오차, 정량 농도비, 점수의 각 기여도는 상세 파일에서 확인할 수 있다. 462.7 nm 기준점은 **SDE baseline의 BActive=PActive 도핑 crossover anchor**로 **SDevice SCR 중심이 아니다**. SPLIT_OK의 5% 경계와 ALL_OK의 잠정 관문(예: B462 비율 0.70~1.30)은 **논문 보고 기준이 아닌 내부 surrogate threshold**다.

## 11. SWB Output Variables — **핵심 8개만 등록**

| SWB 변수 | 뜻 | 기준 |
|---|---|---|
| **PW12_SCORE** | 전체 PW 프로파일 mismatch 점수 | **낮을수록 유리** |
| **PW12_MAIN_NM** | Shallow Main Peak 깊이 [nm] | SDE ~109.3 nm |
| **PW12_MAIN_R** | Main Peak 농도 / SDE Peak | 1 근접 |
| **PW12_B462_R** | 462.7 nm BActive / SDE | 1 근접 |
| **PW12_REBOUND_R** | Valley→Second Peak의 농도 상승 / Main Peak 농도 | 0 근접 |
| **PW12_SPLIT_OK** | Rebound ≤ 5% | 1 통과 |
| **PW12_ALL_OK** | 잠정 Peak/Tail/Split 관문 통과 | 1 통과 |
| **PW12_RUN_OK** | 코드 정상 실행 | 1 |

실행 후 상세 출력 파일 접두사는 **n{VIS_NODE}_PW_v1p2p1**이다.

- **\*_metrics.txt**: 전체 계량 항목·Depthwise ratio·SCORE 성분별 penalty.
- **\*_depth_points.csv**: 위치별 SProcess BActive, SDE BActive, 농도비 및 %.
- **\*_profile_F.csv**: 30~900 nm의 BActive/PActive overlay 원시 데이터.
- **\*_ShallowShoulder_plot.csv**, **\*_JunctionTail_plot.csv**: 시각화용 곡선 자료.
- 실패 시 **\*_error.txt**와 **DOE: PW12_RUN_OK 0**으로 실패를 표시.

이번 8개 변수만 Workbench의 Output Variables에 등록한다. v1.0의 PW_SCORE/PW462_R과 v1.2.1의 PW12_SCORE/PW12_B462_R은 이름과 계산 기준이 다르다.

## 12. 실제 27조건 v1.2.1 결과 — 2026-10-15

기존 PW DOE는 **DNW 1009B Case 27 (975/550/1525 keV)** 기반이며, 27조건 **전부 분석 완료**했다.

| 결과 | 값 |
|---|---|
| 분석 정상 완료 | 27/27 |
| SPLIT_OK | **10/27** |
| ALL_OK | **0/27** |
| 최저 SCORE | **59.4001** (85 keV / fraction 0.575) |
| 해당 최저 SCORE의 Main ratio / B462 ratio | **1.32177 / 0.15723** |
| 가장 양호한 Main Peak ratio | **0.97744** (95 keV / fraction 0.700; Main 110 nm) |
| 해당 조건의 B462 ratio / Split rebound | **0.36034 / 29.62%** |

**해석:** 95 keV 쪽 주입 Dose fraction 증가로 B462를 늘릴 수 있었지만 **중간 Second Peak 및 Split도 심해짐**. 최대 B462도 SDE의 약 36%여서 Dual-PW의 현재 탐색범위에서는 동시 합격조건 없음. 따라서 **Shallow / Deep / 향후 Mid**를 역할 분리하는 방향으로 실험을 확장한다.

## 13. 다음 연구 — Deep PW 9조건 선행 설계

이번 DOE는 **Triple-PW를 계획한 후 Deep implant 기여를 먼저 분리 평가하기 위한 9개 입력 설계**다. **아직 Mid Implant를 추가하지 않았으므로 PW는 Fixed+Deep 두 개**이며 기존 SProcess 사용이 가능하다.

- **36 keV Fixed Energy + 절대 Dose 6.18×10¹² cm⁻²**: 1차 고정 후보.
- **Deep Energy 105 / 120 / 135 keV** × **Deep 절대 Dose 1.6 / 2.0 / 2.4×10¹³ cm⁻²**.
- **DNW는 새로운 Case 15 (955/550/1485 keV)**로 고정 예정.
- **Common WELL RTA 1050°C / 30s** 고정.
- Total PW Dose = Fixed 절대 Dose + Deep 절대 Dose: **2.218 / 2.618 / 3.018×10¹³ cm⁻²**.
- PW_TRIM_FRAC = Deep Dose / Total Dose, PW_FIXED_FRAC = Fixed Dose / Total Dose; DOE 행마다 두 fraction 합을 1로 맞춘다.
- 실행 결과를 확보한 뒤 **SDE보다 실제로 부족한 구간**을 확인해 Mid Energy/Dose를 설계한다. Valley를 무조건 높이는 방식으로 설계하지 않는다.

**SWB 파라미터 정합 주의:** 기존 Stage 2 원본은 PW_FIXED_FRAC를 1−PW_TRIM_FRAC로 계산하지만, 사용자의 실제 SWB에는 PW_FIXED_FRAC가 Parameter로 등록되어 있다. 사용자가 등록한 값은 **sweep하지 않아도 command에서 @PW_FIXED_FRAC@ 형식으로 연결**해야 하므로 후속 SProcess revision에서 정합 검증이 필요하다. 이번 커밋은 **승인받은 SVisualPy·README·타임라인만 변경**하며 Stage 2 command나 9조건 미실행 CSV는 업로드하지 않는다.

### 관련 기록

- [2026-10-15-1 — DNW Case 15 후보 선정](../../../timeline/2026-10/2026-10-15-1.md).
- [2026-10-15-2 — PW 결과 분석과 Deep 9조건 설계](../../../timeline/2026-10/2026-10-15-2.md).
