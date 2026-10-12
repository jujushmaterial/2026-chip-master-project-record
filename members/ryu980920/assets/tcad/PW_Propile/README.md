# PW_Propile — PW-only SVisualPy v1.0

2026-10-12 CMP2에서 제작한 **PW 중심 profile-screening 분석 코드**의 원본 보관 폴더이다. 폴더명 `PW_Propile`은 요청한 표기를 따른다. 이 작업은 공개 문헌 제약 기반 **surrogate baseline** 재현에 속하며, 실제 파운드리 레시피를 복원하거나 전기적 baseline을 확정한 결과가 아니다.

## 1. 배경과 파일

[Triple-DNW v0.4](../Triple_DNW/CMP_SPAD_TripleDNW_ProfileScreening_SVisualPy_v0.4_DeepTail.md)의 composite SCORE는 PW 직접 항목 15%, DNW 직접 항목 45%, 공동 지표 35%, Split 5%로 구성되었다. 따라서 DNW 조건을 고정한 PW DOE에서는 PW의 shallow peak 및 junction-side tail에 집중하는 별도 분석이 필요했다.

- [CMP_SPAD_PW_ProfileScreening_SVisualPy_v1.0.py](CMP_SPAD_PW_ProfileScreening_SVisualPy_v1.0.py): CMP2 원본 455줄을 **변경 없이 보존**.
- `README.md`: 코드 사용법·지표·근거·한계 설명.
- CMP2의 원본 `.py`와 `.txt` 내용은 동일하므로 동일 코드의 중복 사본은 올리지 않는다.
- SProcess는 기존 [Triple-DNW Stage 2 v0.3](../Triple_DNW/CMP_SPAD_TripleDNW_SProcess_v0.3_Stage2_DOE_PLX_only.txt)을 그대로 사용한다.

## 2. 입력과 실행 흐름

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

PW는 **Trim Energy 85/90/95 keV × Trim Fraction 0.500–0.700 (0.025 간격, 9수준) = 27조건**이다. PW Fixed E=36 keV, Total PW Dose=2.06e13 cm^-2, common RTA=1050 °C/30 s는 SWB experiment row에서 고정한다. 기존 Case 27의 PW 조건(85 keV, 0.525)을 포함한다. 27조건은 **설계 완료** 상태이며 시뮬레이션 결과는 아직 확인되지 않았다.

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

**상태:** PW v1.0 원본 저장 완료, DNW/PW 각 27개 DOE 구성 완료; 신규 DOE 결과 및 PW v1.0 실기 실행 로그는 미확인.
