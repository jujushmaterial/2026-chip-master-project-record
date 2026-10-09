# Triple-DNW DOE 데이터

[상위 데이터 안내](../README.md) · [Triple-DNW TCAD 코드/설명](../../tcad/Triple_DNW/README.md) · [2026-10-09 상세 연구일지](../../../timeline/2026-10/2026-10-09.md)

## Triple-DNW란?

Dual-DNW의 **Main + Shallow Trim**만으로는 약 1 µm main peak 정합 후에도 **1.4–1.8 µm의 깊은 phosphorus tail**을 충분히 채우기 어려웠다. 이를 보완하기 위해 **Deep DNW implant**를 추가한 **Main + Shallow Trim + Deep** 구성이다. 목적은 공통 SDE surrogate DNW profile에 맞추는 것으로, 실제 ST 공정 recipe 복원이 아니다.

## DOE가 이어진 이유 — 45 → 25 → 81

| 단계 | 기준/관측된 문제 | 다음 실험의 설계 이유 |
|---|---|---|
| **45-case 최초 Triple-DNW** | Deep E 1300–1700 keV (5) × Deep 추가 dose 1.0–5.0e12 cm⁻² (9). 1700 keV SCORE 최저 후보는 sigma가 target에 가깝지만 1.8 µm overshoot. **1500 keV / Deep 5.0e12 / Total 2.90e13의 Balanced 후보**는 T14/T16/T18=0.838/0.897/0.838로 균형적이나 main peak 농도가 +12.7% 과다 | 기존 Balanced 후보를 다음 25-case의 **기준점(anchor)**으로 채택. Total/Trim dose를 **고정**하고 Main dose 일부를 Deep으로 **재분배**, 과다 peak를 낮추면서 tail을 채울 수 있는지 검증 |
| **25-case Main-to-Deep** (결과 보관) | Deep E 1500/1525/1550/1575/1600 (5) × Deep frac 0.1724–0.2414 (5). Main 1.80→1.60e13, Deep 5.0→7.0e12, **Total 2.90e13 고정** | **Case 4** (Deep 1500, frac 0.2241): T14/T16/T18=0.934/1.079/0.991, PK ratio 1.0626, sigma 369.23 nm, P462 ratio 0.8193, Rp 1031.3 nm. Tail shape는 개선됐지만 junction-side 부족, main peak가 target 1017.3 nm보다 깊음, T16 overshoot가 남음. 최저 SCORE Case 15는 T16/T18 overshoot가 더 커서 다음 기준으로 선택하지 않음 |
| **81-case 후속 Full Factorial** (설계 완료, 결과 미확보) | 25-case **Case 4**를 재현 기준으로 유지하고 **Trim 절대 dose / Main E / Deep E / Deep 절대 dose** 4변수를 3수준씩 확대 | Shallow Trim dose를 Main에서 재분배하여 junction-side를 채우고 main peak를 얕게 유도; Deep dose 증분은 **Total DNW dose 증가**로 공급하여 Main 과다 감소를 방지할 수 있는지 검증. 1500 keV tail 균형과 1525 keV의 peak/sigma 유리함을 함께 비교 |

**45→25:** Main에서 Deep으로 **이동 (Total 고정)**. **25→81:** Trim 증가는 **Main에서 이동**, Deep 추가량은 **Total 증가**. 이 두 설계는 dose conservation 정책이 서로 다르다.

## 여기에 보관된 CSV 파일

| 파일 | 종류·구성 | 얻은 목적 / 진행 상태 |
|---|---|---|
| [1006_A.csv](1006_A.csv) + [1006_B.csv](1006_B.csv) | **실제 45-case 결과 A 23개 + B 22개**(SWB header 포함) | Dual-DNW의 deep tail 부족을 해결하기 위해 **Deep E 1300/1400/1500/1600/1700 keV × Deep 절대 Dose 1.0–5.0e12 cm⁻²(9수준)** 실험. Main/Trim 절대 Dose 고정, Deep dose를 추가하며 Total dose 증가. 1700 keV SCORE 최저 후보는 1.8 µm overshoot, 1500 keV Tail RMSE 최저 후보는 T14/T16/T18 균형이 좋아 **25-case 기준 후보**가 됨. **하나의 DOE이며 중복 조합 없음** |
| [2026-10-09-triple-dnw-main-to-deep-25cases-results-raw.csv](2026-10-09-triple-dnw-main-to-deep-25cases-results-raw.csv) | **실행 결과** 25개 (`1008_.csv` 원본 보존, SWB header 3행 포함) | 45-case Balanced 후보에서 시작한 **Total 고정 Main→Deep 재분배**의 실제 경향·최저 SCORE·최저 Tail RMSE 후보를 비교. **25개 결과 확보/분석 완료** |
| **81-case 후속 결과: 아직 미등록** | **4변수 Full Factorial 81-case** (기존 SWB 입력 40+41로 분할) | 25-case Case 4에서 남은 **P462 부족·peak depth·deep-tail 불균형**을 검증할 예정. **결과 확보·분석 후에만 결과 CSV를 등록** |

> **A/B는 서로 다른 연구가 아니며 단순 실행 분할이다.** 실제 81개 결과가 나오면 40개와 41개를 합쳐 비교한다. 기존 Batch A 첫 조건은 25-case Case 4 재현용이었다. **입력 CSV 두 파일은 결과 미확보 상태이므로 사용자 요청에 따라 GitHub에서 삭제했고, DOE 설계 내용만 남긴다.**

### 81-case 설계 범위 (결과 미확보)

| 변경한 실험 변수 | 3수준 | 왜 바꿨는가 |
|---|---|---|
| **Shallow Trim 절대 dose** | 6.00 / 6.25 / 6.50 ×10¹² cm⁻² | P462 junction-side 농도 부족 보강 + Main에서 재분배 |
| **Main Energy** | 965 / 970 / 975 keV | main peak가 14 nm 깊으므로 미세하게 shallow 이동 시도 |
| **Deep Energy** | 1475 / 1500 / 1525 keV | 1.4/1.6/1.8 µm 위치별 tail balance 조절 |
| **Deep 절대 dose** | 6.50 / 6.75 / 7.00 ×10¹² cm⁻² | Deep energy 변경에 따른 tail dose 민감도 확인 |

```text
D_Main  = 2.25e13 - D_Trim
D_Total = 2.25e13 + D_Deep
DNW_TRIM_FRAC = D_Trim / D_Total
DNW_DEEP_FRAC = D_Deep / D_Total
Main fraction = 1 - DNW_TRIM_FRAC - DNW_DEEP_FRAC

Total DNW Dose = 2.90 / 2.925 / 2.95e13 cm^-2
```

Main/Trim/Deep Energy와 dose는 surrogate calibration 수준이며 actual foundry values가 아니다. PW 조건 (`85/36 keV`, PW Trim frac `0.525`, PW total `2.06e13 cm^-2`), Shallow Trim Energy `550 keV`와 공통 RTA `1050 °C / 30 s`를 고정했다. 모든 SWB parameter는 command에서 `@PARAMETER@`로 참조한다.

## 데이터 해석 주의

- **현재 이 폴더의 45-case A/B 결과와 25-case 결과 CSV는 모두 실제 SProcess/SVisualPy 결과**다. 81-case는 설계한 DOE이며 실제 결과 CSV가 나오기 전까지 보관하지 않는다.
- `TAIL14_R / TAIL16_R / TAIL18_R / TAIL_RMSE`의 비교 기준은 현재 SVisualPy v0.4의 **analytic Gaussian reference**이고, 전체 원본 SDE PLX를 직접 fitting한 결과는 아니다.
- `P462_R`은 고정 깊이의 PActive ratio이며 SCR 자체는 아니다. profile screening으로 VBD/PEB/ATP/dark 개선을 주장하지 않는다.
- **45-case 결과 원본**은 실제 첨부 파일명인 `1006_A.csv`/`1006_B.csv`로 등록했다. 기존 로그의 `1006A.csv`/`1006B.csv`는 같은 45-case의 옛 표기다. 25-case 실험 **입력 조건** CSV는 현재 이 data 폴더에 미등록이다. 2026-10-09 추가로 업로드된 `1008_(1).csv`는 보관 중인 25-case `1008_.csv`와 내용이 정확히 같아 중복 저장하지 않았다. 필요한 경우 원본 그대로 추가하고 이 README의 파일 표를 갱신한다.

**데이터 보관 변경(2026-10-09):** 아직 결과가 나오지 않은 81-case SWB 입력 조건 CSV 2개(40/41)는 GitHub에서 삭제하였다. 분석이 끝난 실제 결과 CSV만 이 폴더에 올리는 원칙을 적용한다.
