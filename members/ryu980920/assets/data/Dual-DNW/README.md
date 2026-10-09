# Dual-DNW DOE 데이터

[상위 데이터 안내](../README.md) · [Dual-DNW TCAD 코드/설명](../../tcad/Dual_DNW/README.md)

## Dual-DNW가 무엇인가?

**Single-DNW**는 DNW를 하나의 implant profile로 조정해 SDE surrogate target에 맞추려 했지만, peak 위치와 profile 폭을 함께 맞추는 데 한계가 있었다. **Dual-DNW**는 DNW phosphorus implant를 **Main**(약 1 µm peak/profile body)과 **Shallow Trim**(junction-side의 얕은 농도 기여)으로 나누어 두 구성의 상대 기여를 조절하는 공정 캘리브레이션 단계다. 실제 foundry 제조법이라고 주장하지 않는다.

## 기존 DOE의 흐름 (현재 CSV 파일은 미등록)

| DOE | 구성과 목적 | 무엇을 확인하고 다음 단계로 넘어갔는가? |
|---|---|---|
| **64-case Dual-DNW** | Main/Trim Energy, Trim Fraction, DNW Dose, PW Trim Fraction의 조합. 폭을 늘리면서 main peak 위치를 맞출 수 있는지 screening | single-DNW 최대 sigma 279.7 nm 대비 Dual-DNW 최대 약 297.3 nm로 증가했지만 target 380.6 nm에 부족. 높은 Trim Fraction은 peak를 지나치게 shallow하게 이동시키고 width gain은 포화 |
| **108-case Dual-DNW** | DNW Dose 2.4/2.6/2.8e13, Main E 955/975/995, Trim E 550/600/650, Trim Frac 0.10/0.15/0.20/0.25 (`3×3×3×4=108`) | main peak를 비교적 맞춘 후보에서도 1.4–1.6 µm deep-tail PActive가 부족했고 Main Energy만 높이면 main peak도 함께 이동. Deep component를 별도 추가한 Triple-DNW로 전환 |

이 표는 과거 연구일지의 요약이다. **현재 이 폴더에는 64/108-case의 원본 SWB 입력·결과 CSV가 등록되지 않았다.** 나중에 원본을 확보하면 연구일지의 날짜·조합수·실행 여부·파일명과 맞춰 추가한다.

## 참고 기록

- [2026-10-06: 108-case 분석 → Triple-DNW 도입](../../../timeline/2026-10/2026-10-06.md)
- [Triple-DNW 데이터](../Triple-DNW/README.md): 후속 DOE를 왜 수행했는지와 25-case 결과/81-case 입력 CSV

**상태:** 과거 Dual-DNW 연구 분석은 기록돼 있으나 이 폴더의 원본 CSV 업로드는 미완료.
