# Dual-DNW DOE 데이터

[상위 데이터 안내](../README.md) · [Dual-DNW TCAD 코드/설명](../../tcad/Dual_DNW/README.md)

## Dual-DNW가 무엇인가?

**Single-DNW**는 DNW를 하나의 implant profile로 조정해 SDE surrogate target에 맞추려 했지만, peak 위치와 profile 폭을 함께 맞추는 데 한계가 있었다. **Dual-DNW**는 DNW phosphorus implant를 **Main**(약 1 µm peak/profile body)과 **Shallow Trim**(junction-side의 얕은 농도 기여)으로 나누어 두 구성의 상대 기여를 조절하는 공정 캘리브레이션 단계다. 실제 foundry 제조법이라고 주장하지 않는다.

## DOE의 흐름 및 보유 CSV

| DOE | 구성과 목적 | 무엇을 확인하고 다음 단계로 넘어갔는가? |
|---|---|---|
| **64-case Dual-DNW** | Main/Trim Energy, Trim Fraction, DNW Dose, PW Trim Fraction의 조합. 폭을 늘리면서 main peak 위치를 맞출 수 있는지 screening | single-DNW 최대 sigma 279.7 nm 대비 Dual-DNW 최대 약 297.3 nm로 증가했지만 target 380.6 nm에 부족. 높은 Trim Fraction은 peak를 지나치게 shallow하게 이동시키고 width gain은 포화 |
| **108-case Dual-DNW** | DNW Dose 2.4/2.6/2.8e13, Main E 955/975/995, Trim E 550/600/650, Trim Frac 0.10/0.15/0.20/0.25 (`3×3×3×4=108`) | main peak를 비교적 맞춘 후보에서도 1.4–1.6 µm deep-tail PActive가 부족했고 Main Energy만 높이면 main peak도 함께 이동. Deep component를 별도 추가한 Triple-DNW로 전환 |

이 표는 과거 연구일지의 요약이다. **64-case와 108-case의 실제 결과 CSV 모두 아래에 등록했다.**

## 참고 기록

- [2026-10-06: 108-case 분석 → Triple-DNW 도입](../../../timeline/2026-10/2026-10-06.md)
- [Triple-DNW 데이터](../Triple-DNW/README.md): 후속 DOE를 왜 수행했는지와 25-case 결과/81-case 입력 CSV

## 현재 보관된 결과 파일

| 파일 | 자료 성격 | 이 데이터를 확보한 목적 |
|---|---|---|
| [64DOE.csv](64DOE.csv) | **실제 64-case 결과**(SWB header 3행 포함) | 250-case Single-DNW의 sigma 부족으로 Main+Shallow Trim implant를 도입. DNW Dose(2.6/3.0e13) × Main E(935/955) × Trim E(650/750) × Trim Frac(0.15/0.25/0.35/0.45) × PW Trim Frac(0.500/0.525) = **64개**. Sigma 최대 **297.34 nm**였지만 해당 main peak가 **842.41 nm**로 target 1017.3 nm보다 얕아져 peak와 폭의 trade-off를 확인. 그래서 108-case 추가 DOE가 필요했음 |
| [0928A.csv](0928A.csv) + [0928B.csv](0928B.csv) | **동일한 108-case DOE를 SWB에서 54+54로 나눠 실행한 실제 결과**. 두 파일 모두 SWB header 3행 포함 | 64-case에서 sigma는 증가했지만 main peak 이동과 width 부족이 남아 DNW Dose 3수준 × Main E 3 × Trim E 3 × Trim Fraction 4 = **108개 refinement**를 수행. `SCORE`, `DNW_RP`, `DNW_PK_R`, `DNW_SIG`, `JUNC`, `P462_R`, `SPLIT`을 평가하여 **Main peak와 deep-tail을 별도로 조절해야 하는지** 판단. 이후 Deep implant를 추가하는 Triple-DNW 도입 근거를 확보 |

**108-case 세부 범위:** DNW Dose `2.4/2.6/2.8e13 cm^-2`, Main E `955/975/995 keV`, Trim E `550/600/650 keV`, DNW Trim Frac `0.10/0.15/0.20/0.25`. PW `85/36 keV`, PW Trim Frac `0.525`, PW total `2.06e13 cm^-2`, RTA `1050 °C/30s` 고정.

**원본 검증:** A/B 각각 54개 결과행, 전체 108개 독립 파라미터 tuple, 중복 0. A/B는 두 연구가 아니라 **한 DOE의 실행 배치 분할**이다. CSV에는 별도의 SWB node ID 열이 없으므로 n72/n124라는 이름만으로 해당 행을 판정하지 않고 입력 parameter tuple로 대조한다.

**핵심 발견:** Main E 975 keV의 SCORE 최저 후보(`DNW_DOSE=2.4e13`, Trim E 550, Trim Frac 0.25)는 Rp 약 1015.3 nm로 target(1017.3 nm)에 근접했으나 1.4–1.6 µm 이후 deep-tail 부족이 남았다. Main E를 995 keV로 올리면 tail은 일부 보강되지만 Rp가 약 1031.3 nm로 깊어지는 coupling이 있었다. 따라서 [Triple-DNW](../Triple-DNW/README.md)로 전환하였다.

**64-case 원본 검증:** 전달된 `64DOE.csv`는 **고유 64조합**이며 DNW Dose **2.6/3.0e13 cm⁻²**만 포함하고 **2.8e13 cm⁻² 조건은 없다**. 기존 2026-09-28 연구일지에서 `Dual.csv`로 언급한 64-case 결과에 대응한다. 64/108-case 원본 결과는 현재 모두 확보했다.

**참고:** [2026-09-28 64-case 분석](../../../timeline/2026-09/2026-09-28.md) · [2026-10-06 108-case 분석](../../../timeline/2026-10/2026-10-06.md).
