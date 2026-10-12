# PW_Propile — PW 27조건 DOE 데이터

> `PW_Propile`이라는 이름은 사용자 요청에 맞춘 보관 폴더명이다. PW profile-screening **코드**는 [TCAD/PW_Propile](../../tcad/PW_Propile/README.md)에 보관한다.

## 등록한 CSV

| 파일 | 구분 | 결과 |
|---|---|---|
| [CMP_SPAD_PW_Case27_27DOE_SWB.csv](CMP_SPAD_PW_Case27_27DOE_SWB.csv) | **SWB experiment 입력표** (27행, `index` + 12개 공정 파라미터) | **27조건 설계 완료; SProcess 실행 결과 미확인** |

**CSV만으로 PW profile의 실제 개선을 주장하지 않는다.**

## 설계 목적

Triple-DNW 81조건 분석에서 최저 SCORE였던 `1009B Case 27`의 DNW를 고정하고, PW를 SDE surrogate baseline에 맞추기 위한 국소 실험이다.

- 기존 PW peak: `PW_PK_R=1.422565`로 SDE reference보다 약 **42.26% 높음**.
- 기존 PW peak depth: 약 `100 nm` vs SDE 기준 `109.3 nm`.
- BActive=PActive metallurgical crossing: `397.556 nm` vs SDE `462.697 nm`.

변경하는 변수는 **PW Trim Energy = 85/90/95 keV (3수준)**, **PW Trim Fraction = 0.500부터 0.700까지 0.025 간격 (9수준)**으로 `3×9=27`개의 SWB 입력 조합이다.

고정 조건: DNW total `2.95e13 cm^-2`, Main/Trim/Deep Energy `975/550/1525 keV`, PW Fixed Energy `36 keV`, PW Total Dose `2.06e13 cm^-2`, common WELL RTA `1050°C / 30s`.

원래 PW 조건 `Trim E=85 keV`, `Trim frac=0.525`가 포함되어 있어 비교 기준으로 이용할 수 있다. Trim 분율 증가에 따라 Fixed Dose는 종속적으로 감소하며, **PW Total Dose를 고정**한다.

## 분석 코드 및 해석

- [PW-only SVisualPy v1.0 원본과 평가식](../../tcad/PW_Propile/README.md): PW peak, shallow shape, tail RMSE, PW462 및 split을 분석하며 SWB에 10개 지표를 출력하도록 작성.
- [2026-10-12-2 연구일지](../../../timeline/2026-10/2026-10-12-2.md): DOE 필요성, 변수 선정 이유 및 SVisualPy v0.4→v1.0 변경사항.
- DNW 81조건 실행 결과와 별도 후속 DNW DOE는 [Triple-DNW 데이터](../Triple-DNW/README.md)에서 관리한다.

**주의:** 이 CSV는 실험 **입력 조건표**이지 실행 결과가 아니다. SWB에서 고정한 파라미터도 SProcess command에서는 `@PARAMETER@`로 참조해야 한다. `JUNC`는 doping crossover이지 SDevice의 SCR 위치가 아니다.
