# CMP SPAD — B 공정개선 독립 검증 가설 (2026-11-10)

**상태: 가설 제안 / TCAD 미검증.** 아래의 H1·H2는 공통 P0 출발점에서 **각각 독립적으로** 검증한다. H1의 최적값을 H2 시작값으로 사용하지 않는다.

| 가설 | 접근 | 주요 목적 | 검증 상태 |
|---|---|---|---|
| [H1 — DNW Deep & Low Doping](H1_DNW_Deep_Low_Doping.md) | DNW 도핑을 더 깊고 낮은 농도로 형성 | SCR 유지, 고전계/BTBT/TAT/PEB 위험 감소 | 미검증 |
| [H2 — Selective Trim DNW Mask](H2_Selective_Trim_DNW_Mask.md) | Trim DNW의 반경 방향 Mask만 축소 | STI5 주변 국부 전계/PEB 저감, Cathode 연결 유지 | 미검증 |

## 두 가설의 공통 조건

- P0 기준: Triple-DNW + Triple-PW, common WELL RTA 1050°C / 30 s. [P0 Freeze 기록](https://github.com/jujushmaterial/2026-chip-master-project-record/blob/main/members/ryu980920/timeline/2026-10/2026-10-29.md).
- SCR center는 grating/Si interface 기준 공통 SDE R0 목표 **180.202945597 nm**에 정합하도록 PW Implant **Energy**만 종속 보정. PW Dose와 native STI2/3/4/5 구조는 고정.
- 실제 SCR 평가 전압은 case별 `VBD − 0.1979980544 V`, ATP는 기준 합의한 `VBD + 1.2020019456 V` 근사. 이는 bias 정의이며 특정 개선 결과가 아님.
- 공통 비교: SCR center/width, VBD, center/peripheral field 및 피크 위치, avalanche onset, reverse I–V, feedback-ON dark current, BTBT, SRH/field-enhanced TAT, ATP(r,z).
- 전계 감소만으로 일반 SRH 생성률 감소를 주장하지 않음. Trap/lifetime calibration 없이는 절대 DCR 감소를 주장하지 않고 상대 dark current/DCR proxy로 구분.
- 공통 SDE R0와 공정 출발점 P0는 **서로 다른 기준**이다. 개선 판정은 먼저 P0 대비 동일 평가 조건으로 수행한다.
- **H2는 기존 연구계획서에 없던 Implant Mask Geometry 변수 제안**이다. 기존 SProcess/SDevice 및 SWB parameter는 이 기록만으로 변경하지 않는다.
- 실제 ST 28 nm 공정 recipe나 DRC·마스크 제작 가능성이 확인된 것으로 주장하지 않는다.

[공통 연구계획서](https://github.com/jujushmaterial/2026-chip-master-project-record/blob/main/shared/decisions/SPAD_연구계획서.md) · [Electrical_Test README](../README.md)
