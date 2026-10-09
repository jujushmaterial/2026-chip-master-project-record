# DEC-001 — SPAD A 3D Annular Validation 후보 7개 → 17개 확장

## 1. 기본 정보

- 결정일: **2026-10-09**
- 담당: **주상현 (Member A; optical/structure)**
- 관련 프로젝트: 28 nm FD-SOI SPAD 940 nm concentric annular Si/STI optical structure
- 활동/결정 상태: **3D 검증 대상 및 비교 설계 확정 (계획 결정)** / **3D 전기·광학 결과 미검증**
- 변경 전 결정: [2026-10-06, Annular 7-case validation set](../../members/jujushmaterial/timeline/2026-10/2026-10-06.md)
- 관련 연구 방향: [SPAD 연구계획서](SPAD_연구계획서.md)

## 2. 배경 및 변경 이유

2026-09-28의 160-case **2D EMW radial-pitch screening** 결과를 사용하여 2026-10-06에 Annular 7개 case를 3D 검증 후보로 결정했다. 이후 사용자가 제시한 SCR-integrated optical generation 및 Gmax_SCR 대 radial pitch 그래프에서 국소 peak/valley 및 완만한 구간을 검토했다.

기존 7개는 최고 성능 후보와 저성능 대조군을 포함하지만, **2D에서 나타나는 급상승/급하락 또는 국소 peak–valley 응답이 실제 3D concentric annular 구조에서도 재현되는지**를 검증하기에는 대표 구간이 제한적이다.

따라서 기존 7개를 삭제하거나 교체하지 않고, 경향성 확인 및 peak–valley contrast용 10개를 추가하여 **Annular 17개**로 확장한다. 선택 이유는 연구 계획 및 2D screening의 관찰에 근거한 **검증 목적**이며, 3D에서 peak·valley나 성능 순위가 유지된다고 확정한 결과가 아니다.

## 3. 확정 후보 집합

### 3.1 변경 전 기존 7개 (전부 유지)

**200 / 215 / 750 / 775 / 835 / 900 / 1000 nm**

### 3.2 신규 추가 10개

**390 / 650 / 675 / 685 / 715 / 730 / 760 / 810 / 880 / 960 nm**

### 3.3 최종 확정 17개 (오름차순)

**200 / 215 / 390 / 650 / 675 / 685 / 715 / 730 / 750 / 760 / 775 / 810 / 835 / 880 / 900 / 960 / 1000 nm**

총 비교 구조는 **Annular 17개 + Reference 3D 1개 + Gao Square 480 nm, Si pattern FF15% 3D 1개 = 19개**다. Reference에는 의도적 periodic optical pattern이 없으므로 Reference의 pitch/optical FF를 정의하지 않는다.

## 4. 17개 후보별 목적

| Radial pitch (nm) | 구분 | 3D 검증에서의 역할 |
|---:|---|---|
| 200 | 기존 | 2D global-worst / low-pitch negative control |
| 215 | 기존 | 저성능 구간의 인접 재현성 및 경향 확인 |
| 390 | 신규 | 저·중간 pitch 완만한 변화 구간의 경향성 control |
| 650 | 신규 | 첫 번째 급상승·국소 peak 후보 주변 |
| 675 | 신규 | 첫 번째 하락·valley 후보 주변 |
| 685 | 신규 | 다음 전이 상승 구간의 대표점 |
| 715 | 신규 | 다음 전이 하락 구간의 대표점 |
| 730 | 신규 | 급변 구간의 상승·국소 peak 후보 주변 |
| 750 | 기존 | Reference 초과 positive-gain 구간의 benchmark candidate |
| 760 | 신규 | 전이 구간의 하락·valley 후보 주변 |
| 775 | 기존 | 강한 SCR 적분 광생성량 국소 peak 후보 |
| 810 | 신규 | 775 nm 이후 고피치 하락/valley 비교점 |
| 835 | 기존 | 2D Gmax_SCR 전역 최대 후보 (hotspot metric) |
| 880 | 신규 | 835 nm 이후 hotspot 응답 저하 비교점 |
| 900 | 기존 | 2D G_SCR_Int 및 Gain_Ref 전역 최대 후보 |
| 960 | 신규 | 900 nm 이후 적분 광생성량 하락/valley 비교점 |
| 1000 | 기존 | 높은 pitch 경향성 upper-bound control |

표의 peak/valley 표현은 **선정 목적과 예상 구간의 명칭**이다. 모든 후보가 두 2D 지표 모두에서 수학적으로 정확한 국소 극값이라고 주장하지 않는다. 두 지표의 극값이 서로 다른 pitch에 위치할 수도 있다.

## 5. 3D 검증 시 핵심 질문

1. **Regime/trend consistency:** 200/215, 390, 1000 nm 등 저·중·고 pitch 구간에서 2D가 보여준 상대 경향이 3D에서도 유지되는가?
2. **Peak–valley contrast:** 650↔675, 685↔715, 730↔760, 775↔810, 835↔880, 900↔960 nm 주변의 성능 변화가 3D에서 유지·약화·반전되는가?
3. **Metric distinction:** SCR 적분 광생성량 최적점(2D: 900 nm)과 SCR 내부 단일 최대 광생성률 최적점(2D: 835 nm)이 3D에서도 서로 다르게 나타나는가?
4. **Causality check:** 급격한 변화가 순수 광학 간섭·회절뿐 아니라 N_Radial 변화, native STI overlap, finite aperture, 실효 Si fill factor 및 numerical mesh/경계의 영향을 받는가?
5. **Final design:** 3D EMW에서 가장 우수한 SCR/active-region integrated photogeneration과 spatial distribution, polarization sensitivity를 보이는 후보는 무엇인가?

절대적인 2D 수치나 순위의 완벽한 일치를 **3D의 통과조건으로 요구하지 않는다**. 2D EMW는 extruded geometry screening이며 정확한 원형 3D 전자기 해석이 아니다.

## 6. 고정조건 및 실행 Gate

- **940 nm**, 공통 optical material/source normalization과 입사·boundary 조건.
- 의도적으로 설계한 **Si pattern FF=15% 고정**. Ring width는 각 radial pitch에 따라 FF를 맞추기 위한 종속변수이며, pitch와 width를 독립적으로 동시 sweep하지 않는다.
- STI depth는 주 sweep 변수가 아니며 frozen 조건으로 고정한다.
- Common frozen electrical core를 유지한다. 3D SDE Candidate-B v2.6 Reference의 **코드 채택과 3D SDevice electrical validation 완료는 서로 다르다**.
- Gao Square benchmark: **480 nm pitch / FF15% / 186×186 nm² Si square** (문헌 구조 benchmark).
- 19개 구조 각각에 대해 **SDE → SDevice → SVisualPy → electrical PASS → EMW**의 순서를 따른다.
- 전기 확인: VBD, SCR p/n-side·center·width, reverse I–V, central/peripheral electric field, breakdown onset, avalanche/impact-ionization location. Tolerance는 mesh convergence 및 extraction repeatability를 확인한 후 freeze한다.
- Reference 3D 및 Gao Square 3D의 electrical/optical benchmark를 먼저 검증하고, 그 후 Annular 17개를 동일 조건에서 평가한다.

## 7. 평가 지표 및 해석 제한

- Primary optical metric: **3D SCR-integrated photogeneration, G_SCR_Int** 및 Reference 대비 normalized gain.
- Secondary: **Gmax_SCR**, radial/azimuthal/vertical G(x,y,z) distribution, polarization sensitivity.
- Annular case 간 실제 FinalSiFF 및 N_Radial, native STI 중첩·경계 효과를 함께 기록한다. Intentional FF15%가 **전체 구조의 실효 FinalSiFF까지 정확히 같음을 의미하지 않는다**.
- 2D에서 보인 peak–valley contrast가 3D에서 사라지거나 반전되면 실패 사실과 원인을 별도로 기록하며, 이를 숨기고 2D 최적 pitch를 그대로 final claim으로 사용하지 않는다.
- Optical G와 ATP 또는 measured PDP를 동일 지표로 혼용하지 않는다. 최종 A+B 통합은 G×ATP 공간 적분이며 940 nm dToF 성능 평가는 별도 단계다.

## 8. 변경 영향과 남은 작업

### 변경된 내용

- **Annular optical validation 대상:** 7 → **17개**.
- **전체 3D optical comparison 구조:** 9 → **19개**.
- 검증 목적에 **저·중·고 pitch 경향성 + 국소 peak–valley contrast의 2D↔3D 일치성 평가** 추가.

### 변경하지 않는 내용

- 28 nm FD-SOI literature-constrained surrogate baseline의 정체성.
- 3D Reference Candidate-B v2.6 SDE 기준 코드 및 frozen doping/calibration.
- Reference native STI 유지, 의도적 FF15%는 square/annular pattern에만 적용.
- A와 B의 독립 연구변수, SCR 정합 원칙, 최종 A+B 평가식 및 공통 시스템 조건.

### 미완료 작업

- [ ] Reference v2.6의 3D electrical fingerprint 및 mesh convergence 확인.
- [ ] Reference/Gao Square 480 nm, FF15% 3D 전기·광학 benchmark.
- [ ] Annular 17개 SDE 구조/mesh 생성, case manifest 및 N_Radial/FinalSiFF 기록.
- [ ] 각 case별 SDevice/SVisualPy electrical PASS.
- [ ] 17개 annular 940 nm 3D EMW 실행.
- [ ] 2D–3D trend·rank/peak–valley consistency 및 numerical sensitivity 분석.
- [ ] 3D 광학 결과를 근거로 최종 annular pitch/design 확정.

계산비용 관리 차원에서 구간별로 **단계적으로 실행할 수 있으나**, 승인된 **최종 검증 후보 17개를 임의로 축소하거나 바꾸지 않는다**. 변경이 필요하면 별도 결정 기록에 사유를 남긴다.

## 9. 근거·기존 기록

- [160-case 2D radial-pitch DOE CSV](../../members/jujushmaterial/assets/tcad/spad-annular-2d-doe/2026-09-28-annular-2d-doe-160cases.csv)
- [2D DOE 분석 보고서](../../members/jujushmaterial/assets/tcad/spad-annular-2d-doe/CMP_SPAD_A_2D_Annular_RadialPitch_DOE_Analysis_2026-09-28.md)
- [2026-10-06 7개 선정 및 이후 3D baseline 감사 기록](../../members/jujushmaterial/timeline/2026-10/2026-10-06.md)
- [2026-10-09 3D SDE baseline v2.6 채택 및 후속 계획](../../members/jujushmaterial/timeline/2026-10/2026-10-09.md)
- 사용자가 본 대화에 제시한 두 2D 그래프의 빨간 박스 위치와 **17개 확대안을 명시적으로 선택한 대화**.
- AI 사용: ChatGPT (검증 설계 후보 구분·결정사항 구조화). 결과 데이터 자체를 새로 생성하거나 3D 계산을 실행하지 않음.

## 10. 수정 이력

- **2026-10-09:** 기존 7개를 보존하고 10개를 추가하는 17-case 3D validation 확장안을 결정 및 기록. 2026-10-06의 7-case 결정은 역사적 기록으로 유지하되, **현재 실행 대상은 본 문서의 17개**로 갱신한다.
