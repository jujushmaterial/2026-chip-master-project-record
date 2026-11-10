# H2 — 선택적 Trim DNW Mask 축소에 의한 STI5 주변 전계 제어

**상태:** 가설 제안 (2026-11-10) / 전기적 연결성·PEB·Dark Current 모두 미검증  
**담당:** 유용성(B), CMP SPAD  
**연구 범위:** [surrogate assumption] **기존 독립변수(DNW Dose/Energy·RTA)에 없던 Implant Mask Geometry 자유도 추가 제안**

## 연구 가설

> **STI5는 움직이지 않고 Trim DNW Implant의 반경 방향 마스크 끝만 안쪽으로 이동시키되 Main·Deep DNW의 Cathode 연결을 유지하면, 중앙 SCR 위치를 유지하면서 STI5 주변의 국부 고전계 및 Avalanche Triggering을 줄여 PEB와 dark-generation 위험을 개선할 수 있는가?**

**H1과 달리 H2는 수평 방향 도핑 영역·접합 끝의 공간적 위치를 바꾸는 실험**이다. Trim DNW Energy·Dose는 P0로 고정한다.

## P0 geometry [surrogate dimension]

| 영역 | 반경 범위 (µm) |
|---|---:|
| STI5 | 12.20–12.80 |
| PW Mask 끝 | 12.50 |
| Triple-DNW 공통 Mask 끝 | 16.30 |
| Cathode N-Well | 14.20–15.40 |

Triple-DNW: Trim 550 keV/7.50×10¹² cm⁻²; Main 955 keV/1.50×10¹³ cm⁻²; Deep 1485 keV/7.00×10¹² cm⁻². 모두 Phosphorus.

DNW Mask 전체를 12.2 µm 안쪽으로 단축하면 Cathode N-Well과의 **명목상 Implant 영역 중첩**이 사라질 수 있으므로, 초기에는 **Trim Mask만 별도 축소**하고 Main/Deep의 기존 16.30 µm Mask를 유지하는 방안을 검증한다. 실제 수송 연결성이 유지되는지는 별도 확인이 필요하다.

## 초기 DOE 후보 [surrogate assumption / 미확정]

| 조건 | Trim Mask 끝 (µm) | 의미 |
|---|---:|---|
| P0 | 16.30 | 기존 공통 DNW Mask |
| M1 | 14.00 | Cathode N-Well 시작보다 짧게; STI5는 여전히 직접 주입 영역 |
| M2 | 13.00 | STI5 외측 끝보다 긴 범위; STI5는 여전히 직접 주입 영역 |
| M3 | 12.00 | STI5 내측 시작보다 짧게; **최종 도핑이 0인 것은 아님** |

Main·Deep Mask, 3개 DNW Energy/Dose, common RTA, PW Dose, STI geometry 고정. PW Energy는 공통 중앙 SCR 위치를 위한 종속 보정에만 사용한다. Mask 경계 근처의 lateral straggle과 RTA 확산을 반드시 고려한다.

## 물리적 근거와 검증

- 동일 연구계열의 **peripheral STI5–PW/DNW junction overlap과 PEB/DCR의 연관성**은 H2의 배경이다. 하지만 그 연구의 **STI 이동/정렬 효과**가 DNW Trim Mask 축소 효과를 직접 입증하지 않는다.
- **전기적 연결성:** PActive−BActive 2D Net Doping Contour, 전자 밀도, eCurrent vector, 전자 준페르미 준위 및 별도 forward-bias 연결성/series resistance test로 Cathode 경로 점검.
- **PEB:** STI5 부근 field·avalanche 감소뿐 아니라 새 Trim Mask 끝에서 peak field/조기 avalanche가 발생하는지 반드시 확인.
- **Dark:** BTBT 및 field-enhanced TAT 감소 가능성 확인. 일반 SRH는 SCR 확장 때문에 증가할 수도 있음. Interface Trap 모델 없이는 STI5 계면 결함 기원의 DCR 감소 입증 불가.
- **검출 유지:** 중앙 SCR center≈180.203 nm 보정 후 ATP(r,z)·유효 검출영역 및 usable excess-bias margin 비교.

## 제조·연구 범위상의 Trade-off

서로 다른 well implant mask를 사용하는 것은 공정 개념으로 가능하지만, **추가 리소그래피·정렬 오차·마스크 비용**, 고에너지 이온 차폐 두께와 미세 공정 디자인 룰 문제가 따른다. 실제 ST 28 nm FD-SOI에서 가능하다고 주장하지 않음. 참고: [SKY130 NWI2 — same-mask multi-energy](https://sky130-process-tech.readthedocs.io/en/latest/steps/019-nwi2.html), [Split well implantation — separate mask 사례](https://patents.google.com/patent/US20210125879A1/en).

## 상태

**미검증:** 마스크/공정 덱 미변경, 실제 연결·PEB·Dark Current 개선 미확인. H2 채택과 기존 연구계획서의 변수 범위 확장은 **별도 기록·검토 대상**.

[공통 연구계획서](https://github.com/jujushmaterial/2026-chip-master-project-record/blob/main/shared/decisions/SPAD_연구계획서.md) · [P0 Freeze](https://github.com/jujushmaterial/2026-chip-master-project-record/blob/main/members/ryu980920/timeline/2026-10/2026-10-29.md).
