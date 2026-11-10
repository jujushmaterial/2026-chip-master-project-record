# H1 — DNW 도핑의 심부 이동 및 저농도화

**상태:** 가설 수립 (2026-11-10) / DOE·TCAD 결과 미확보  
**담당:** 유용성(B), CMP SPAD  
**근거 수준:** [surrogate assumption] 개선 방향 + 2019/2022 동일 연구계열의 DNW 최적화 사례

## 연구 가설

> **DNW 도핑 프로파일을 P0 대비 더 깊고 낮은 농도로 형성하고, PW Energy로 SCR 위치를 유지하면 PW/DNW 접합 및 주변부 전계 집중이 완화되어 PEB 위험과 field-enhanced dark generation을 감소시킬 수 있는가?**

**DNW Energy 증가 + Dose 감소는 H1이라는 하나의 결합된 프로파일 설계 전략**이다. 단순 Energy 증가 효과와 Dose 감소 효과를 서로 다른 가설로 분리하지 않는다.

## P0 입력 [surrogate assumption]

| DNW Phosphorus implant | Energy (keV) | Dose (cm⁻²) |
|---|---:|---:|
| Trim | 550 | 7.50×10¹² |
| Main | 955 | 1.50×10¹³ |
| Deep | 1485 | 7.00×10¹² |

RTA 1050°C/30s, P0 Mask (DNW 끝 16.3 µm), native STI 및 PW Dose 고정. [P0 기록](https://github.com/jujushmaterial/2026-chip-master-project-record/blob/main/members/ryu980920/timeline/2026-10/2026-10-29.md).

## 독립 실험

1. P0의 Active/Total Dopant Profile, Net Doping, 2D field, SCR, VBD, PEB/ATP/Dark Current 확보.
2. DNW Energy/Dose를 조합해 **최종 활성 도핑 분포**의 실제 peak·shoulder·tail 이동과 접합 부근 농도 감소 여부 확인. Energy↑만으로 원하는 최종 Profile이 보장되지는 않는다.
3. PW Energy만 종속 보정하여 중앙 SCR center를 공통 R0 anchor 약 180.203 nm에 유지.
4. 같은 P0 평가 규칙으로 Ecenter/Eperiph, E peak 위치, 최초 avalanche 위치, dark components, ATP(r,z) 비교.

## 개선 가능성 및 Trade-off

- 기대: 접합 전계 완화 → BTBT 및 Hurkx 등 전계 강화 TAT 감소, 주변부 조기 Avalanche 완화 가능.
- 위험: SCR 폭 확대에 따른 SRH 증가, 중앙 ATP 저하, 주변부 field 재집중, usable excess-bias margin 악화.
- VBD가 증가하는 것만으로 성공이 아니다. **SCR 위치를 유지하면서 PEB/relative dark current 개선과 ATP 유지**가 합격 기준이다.
- 일반 SRH 감소를 전계 완화의 직접 결과로 등치하지 않고, absolute DCR(Hz/µm²)은 주장하지 않는다.

## 상태 및 출처

**미검증:** 실제 DOE 결과, 개선 폭, 최적값 없음.  
참고: Chaves de Albuquerque et al. (2019) *Lowering the Dark Count Rate of SPAD Implemented in CMOS FDSOI Technology*, DOI [10.1109/EUROSOI-ULIS45800.2019.9041916](https://doi.org/10.1109/EUROSOI-ULIS45800.2019.9041916). [공통 연구계획서](https://github.com/jujushmaterial/2026-chip-master-project-record/blob/main/shared/decisions/SPAD_연구계획서.md).
