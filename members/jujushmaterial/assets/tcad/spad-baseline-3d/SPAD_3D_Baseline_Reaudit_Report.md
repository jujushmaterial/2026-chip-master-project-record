# SPAD 3D Baseline Re-audit Report

## 1. Executive decision

**Final status: READY WITH SURROGATE ASSUMPTIONS**

공개 문헌은 2024 Reference의 device class, vertical stack family, junction type, nominal size, non-axisymmetric layout character, modified-DNW breakdown fingerprint를 충분히 제약한다. 그러나 exact GDS, PW/DNW XY mask, 25 µm boundary definition, STI1-STI7 좌표·폭·깊이, contact polygons, full BEOL optical stack은 공개하지 않는다.

따라서 실제 foundry mask/recipe 복원은 불가능하지만, 다음 조건을 지키면 방어 가능한 3D Reference surrogate 구현은 가능하다.

1. 2024 Reference를 25 µm-class **rectilinear staircase quasi-circular** device로 구현한다. [직접 실측] [그림 판독 추정]
2. 2D cylindrical baseline은 electrical fingerprint source로 유지하되 실제 3D mask로 간주하지 않는다. [surrogate assumption]
3. frozen doping과 process model을 먼저 고정하고 geometry-only split을 수행한다.
4. STI branch, staircase resolution, STI depth, contact/boundary, Gao lattice clipping을 명시적 surrogate assumption으로 등록한다.
5. `VBD`, SCR, central/peripheral field, breakdown onset/location이 보존되는지 확인한 후에만 EMW와 `Q=∫G×ATP dV` 비교로 진행한다.
6. measured PDP, simulated PDP, ATP-weighted Q, SCR-integrated G, local photogeneration을 같은 수치로 취급하지 않는다.

이 보고서는 좌표를 새로 생성하거나 기존 2D baseline을 자동 수정하지 않는다.

## 2. 근거 계층

| Level | Meaning | Use in 3D baseline |
|---|---|---|
| L1 | 2024 target paper 직접 정보 | Device identity와 validation anchor로 사용 |
| L2 | 2017-2023 동일 연구계열 constraint | 공개되지 않은 topology의 범위를 제한 |
| L3 | Figure-only qualitative topology | Shape/ordering만 사용; pixel-to-length 변환 금지 |
| L4 | Frozen 2D surrogate assumption | Initial 3D port에 유지 가능하나 문헌 직접값으로 주장 금지 |
| L5 | New 3D surrogate decision | Human-approved candidate/split로 등록; foundry fact로 주장 금지 |

## A. 3D Reference에서 확정 가능한 것

| Item | Confirmed statement | Provenance | Source |
|---|---|---|---|
| Technology | 28 nm FD-SOI CMOS | [직접 실측] | P10 pp.1-2 |
| Vertical architecture | SPAD below BOX, CMOS/electronics above BOX | [직접 실측] [동일 연구계열 constraint] | P01-P05, P10 Fig. 1 |
| Junction | PW anode / modified-DNW cathode junction | [직접 실측] | P10 Figs. 1-2, §2.3 |
| Cell class | 25 µm diode, quasi-circular | [직접 실측] | P10 p.2, §2.1.1; p.6, §2.3 |
| Actual layout nature | Rectilinear/staircase full-cell with contacts and non-axisymmetric surroundings | [직접 실측] [그림 판독 추정] | P10 Fig. 6; P08 Fig. 18 |
| Electrical fingerprint | Room-temperature VBD ≈15.8 V | [직접 실측] | P10 §2.3 |
| Reference optical identity | No intentional periodic square optical pattern | [직접 실측] | P10 Figs. 5,8,10-12 |
| Illumination family | FSI; no ARC; no microlens | [직접 실측] | P10 pp.6,10 |
| BEOL condition | Metal opening over photosensitive area; BEOL dielectrics remain; CMOS areas screened by metal/dummy | [직접 실측] | P10 pp.6,10 |
| Native isolation | Native STI exists because of process/design rules | [직접 실측] | P10 §2.1.2 |

확정할 수 없는 것은 exact outline이다. `quasi-circular`는 수학적 원을 의미하지 않으며, Figure 6은 실제 layout이 staircase/rectilinear임을 보여준다. 3D Reference를 2D half-cell의 단순 회전으로 만들 근거는 없다.

## B. Direct numeric value가 있는 것

### B.1 2024 Reference 및 같은 칩의 직접값

| Parameter | Value | Applies to | Provenance | Source/qualification |
|---|---:|---|---|---|
| Diode diameter | 25 µm | Reference and patterned family | [직접 실측] | P10 p.2; defining mask boundary는 미공개 |
| VBD | ≈15.8 V | 2024 SPAD family | [직접 실측] | P10 p.6, §2.3, room temperature |
| VHV0 | ≈16.1 V | Active-quench detection setup | [직접 실측] | P10 p.6; electronics threshold 포함 |
| VHV0 temperature slope | +11 mV/°C | Reference/patterned cells | [직접 실측] | P10 p.8, Fig. 8(a) |
| Total dead time | ≈1.1 µs | 2024 active-quench measurement | [직접 실측] | P10 p.7, §3 |
| Comparable-DCR region | below Vex≈0.7 V, about 5% VBD | Reference vs patterns | [직접 실측] | P10 p.8, Fig. 8(b) |
| Activation energy | 0.25 ± 0.05 eV | 2024 cells | [직접 실측] | P10 p.8, Fig. 9 |

### B.2 Same-lineage direct stack values

| Parameter | Value | Applies to | Provenance | Source/qualification |
|---|---:|---|---|---|
| Upper Si | 7 nm | Same 28 nm FD-SOI platform | [직접 실측] [동일 연구계열 constraint] | P04 p.1; P05 p.1; P10에는 수치 재기재 없음 |
| BOX | 25 nm | Same 28 nm FD-SOI platform | [직접 실측] [동일 연구계열 constraint] | P04 pp.1,3; P05 p.1 |
| Modified-DNW VBD predecessors | 15.6-15.8 V | P06/P08 modified-DNW cells | [직접 실측] | P06 Table I; P08 Table 1 |

### B.3 Gao Square patterned variant 직접값

| Parameter | Value | Provenance | Source | Restriction |
|---|---:|---|---|---|
| Pitch | 480 nm in x and y | [직접 실측] | P10 p.6, §2.2.2 | Patterned variant only |
| Optical FF | 15% | [직접 실측] | P10 p.6 | Silicon area / square unit-cell area |
| Silicon square | 186 × 186 nm² | [직접 실측] | P10 p.6 | FF15 patterned variant only |
| STI separation | 294 nm | [직접 실측] | P10 p.6 | FF15 patterned variant only |
| Optical anchor | SCR 180 nm from grating/silicon-substrate interface | [논문 직접 시뮬레이션] | P07 p.4; P10 p.5 | STI depth가 아님 |

이 patterned-variant 값들은 unpatterned Reference의 FF/pitch 또는 native STI dimensions가 아니다.

## C. Same-lineage constraint만 있는 것

| Constraint | Evidence | What it allows | What it does not allow |
|---|---|---|---|
| Modified DNW is deeper and less doped | P03/P08: one implant, dose about 70% lower, energy 25% higher [논문 직접 시뮬레이션] | High-VBD branch identity와 relative process direction | Absolute dose, energy, concentration, depth reconstruction |
| Active-zone STI2/3/4 | P09 Fig. 1 Reference/Fusion [직접 실측] | Active STI의 presence/removal topology split | 2024 exact branch, width, spacing, depth |
| Peripheral STI5 | P06 Fig. 7; P08 Fig. 14; P09 Fig. 1 [직접 실측] | Overlap/aligned/shifted topology split | Exact overlap length, width, XY vertices |
| STI6/NW/contact-side relation | P06 Fig. 2 [직접 실측] | Peripheral ordering/topology | 2024 exact coordinate/size |
| BFMOAT/guard action | P02/P03 [직접 실측] [논문 직접 시뮬레이션] | Lower-field guard concept | 2024 guard width/mask reuse |
| SCR extraction method | P07 Figs. 2-3 [논문 직접 시뮬레이션] | Field threshold and drift/diffusion-based extraction | Frozen SCR bounds의 문헌 직접 인증 |
| 2D electrical + 3D optical coupling | P07/P10 [논문 직접 시뮬레이션] | Comparable methodology for Q/PDP proxy | Actual 3D electrical mask identity |
| 180 nm anchor | P07/P10 [논문 직접 시뮬레이션] | Optical hotspot/SCR relative alignment check | STI depth 또는 absolute junction coordinate |

가장 중요한 제한은 P10 Reference가 P09의 Reference, Fusion, aligned+Fusion 중 어느 mask와 동일한지 공개되지 않았다는 점이다. 따라서 active STI2/3/4와 overlapping STI5는 현재 baseline을 제약하는 가장 가까운 topology지만 `[동일 연구계열 constraint]`를 넘지 못한다.

## D. 그림으로 topology만 확인 가능한 것

| Figure evidence | Usable information | Prohibited extraction |
|---|---|---|
| P02 Fig. 2 | Square와 octagonal-like staircase, orthogonal-mask 구현 | 2018 step dimensions를 2024에 이식 |
| P05 Fig. 2(c) | Contacts, resistor, electronics가 포함된 non-axisymmetric full-cell character | 25 µm arrow를 특정 PW/DNW diameter로 선언 |
| P06 Fig. 2 | STI5와 STI6의 peripheral ordering, rectilinear layout | Pixel distance로 STI width/spacing 계산 |
| P06 Fig. 7 | Reference/aligned/shifted STI5 relation | Numerical overlap/offset 추출; scale not respected |
| P08 Fig. 16 | All-optimization quasi-circular partial layout | 이를 2024 Reference로 자동 식별 |
| P08 Fig. 18 | Octagonal vs circular/quasi-circular staircase implementation | 완전한 원 또는 exact vertices 추출 |
| P09 Fig. 1 | STI2/3/4 active, STI5 peripheral, Fusion/alignment topology | Numerical coordinates/depth 추출 |
| P10 Fig. 6 | 2024 outer staircase character, square array, boundary clipping | GDS 복원, lattice origin/edge rule 추출 |

Figure evidence는 3D topology 선택을 제한하지만 실제 nm/µm 좌표를 생성하지 않는다.

## E. Exact coordinate가 미공개인 것

- 25 µm를 정의하는 mask boundary.
- PW, DNW, NW, BFMOAT의 XY polygons와 vertical doping boundaries.
- Staircase vertex 수, step resolution, corner placement.
- Anode, cathode, substrate contact polygons.
- Native STI1-STI7의 width, length, spacing, depth, overlap, XY coordinates.
- 2024 Reference의 exact active-STI/peripheral-STI branch.
- Gao Square lattice origin, full-SPAD cell count, boundary clipping/exclusion rule.
- Upper BEOL dielectric thicknesses와 optical constants.
- Absolute PW/DNW implant dose, energy, anneal temperature/time.
- 2024 SDevice mesh, avalanche model, lifetime, interface-defect density.
- Optical polarization과 finite full-cell boundary condition.

이 항목은 `[미공개]`이며 그림 pixel 또는 VBD 역맞춤으로 복원하지 않는다.

## F. 기존 2D surrogate에서 그대로 유지할 수 있는 것

`유지`는 문헌 직접값 승격이 아니라 initial 3D port에서 변수를 불필요하게 동시에 바꾸지 않는다는 뜻이다.

| Frozen item | Initial action | Provenance status | Reason |
|---|---|---|---|
| VBD 15.7979980544 V | Electrical target fingerprint로 유지 | [surrogate assumption] [동일 연구계열 constraint] | P08-P10 modified-DNW 15.8 V class와 일치 |
| Upper Si 0.007 µm | 유지 | [동일 연구계열 constraint] | P04/P05 direct 7 nm |
| BOX 0.025 µm | 유지 | [동일 연구계열 constraint] | P04/P05 direct 25 nm |
| DNW PeakVal 3.15e17 cm^-3 | Initial profile parameter로 고정 | [surrogate assumption] | Geometry split과 doping split 분리 목적 |
| PW PeakVal 5.95e17 cm^-3 | Initial profile parameter로 고정 | [surrogate assumption] | Implant dose가 아닌 analytic concentration parameter |
| SCR p/n/center/width | 2D reference fingerprint로 보존 | [surrogate assumption] | 3D 재추출 비교 기준; 문헌값은 아님 |
| Active half-size 12.5 µm | Nominal characteristic envelope로 유지 | [surrogate assumption] [동일 연구계열 constraint] | P10 25 µm diode class와 compatible |
| STI depth 0.300 µm | First-pass frozen assumption으로 유지 | [surrogate assumption] | Literature value가 아니므로 later sensitivity 필수 |
| STI1-STI5 2D intervals | 2D reference deck에만 유지 | [surrogate assumption] | 3D radius/XY coordinate로 전환 금지 |

Geometry-only 3D port가 완료되기 전에는 DNW/PW profiles를 재-fit하지 않는다.

## G. 기존 2D surrogate에서 재검토가 필요한 것

| Item | Why review is needed | Review method |
|---|---|---|
| Axisymmetric outer boundary | Actual 2024 layout is staircase/non-axisymmetric | Candidate A/B/C geometry-only split |
| 12.5 µm boundary meaning | Diode diameter mask definition unknown | Envelope, junction boundary, optical aperture를 분리 |
| STI2/3/4 presence | P10 exact P09 branch correspondence unknown | Present vs removed/minimized split |
| STI5 topology | Overlap/aligned/shifted alternatives exist | Reference-like vs aligned split |
| STI depth 0.300 µm | No published numerical depth | Depth sensitivity after topology selection |
| Contact/substrate boundary | Full-cell contact layout unpublished | Contact-minimal vs contact-aware electrical split |
| SCR coordinate origin | 180 nm anchor와 frozen center의 origin/definition이 다름 | Common interface-relative coordinate plot |
| 3D dopant mapping | 2D profile extrusion may change total dopant/field near corners | 2D/3D center cut and integrated dopant audit |
| Avalanche/defect model | P06/P08 use different models/calibrations | Frozen model primary, physics-model split later |
| Optical stack | Simplified model and fabricated BEOL differ | Simplified vs BEOL-effective EMW sensitivity |

재검토는 VBD를 맞추기 위한 자유 fit이 아니라 frozen 2D fingerprint의 3D 안정성을 확인하는 절차다.

## H. 3D lateral mask에 필요한 surrogate assumption

| Assumption ID | Needed assumption | Why necessary | Literature constraint | Remaining freedom |
|---|---|---|---|---|
| SA-01 | Quasi-circular staircase resolution | Exact vertices 미공개 | P08 Fig. 18, P10 Fig. 6 | Step count/resolution, corner approximation |
| SA-02 | 25 µm boundary assignment | Defining layer 미공개 | P10 states diode diameter 25 µm | PW/DNW/envelope/aperture mapping |
| SA-03 | Primary active-STI branch | P10 Reference branch 미공개 | P09 Reference/Fusion topology | STI2/3/4 present or removed/minimized |
| SA-04 | Primary STI5 relation | P10 exact relation 미공개 | P06/P08/P09 overlap/aligned alternatives | Overlap vs aligned realization |
| SA-05 | STI1/6/7 realization | Labels/order only partly shown | P06 Fig. 2, P10 Fig. 1 | Exact polygons and sizes |
| SA-06 | STI depth | Numerical process depth 미공개 | Fixed by process only | Frozen 0.300 µm and sensitivity alternatives |
| SA-07 | Contact-aware extent | Contact polygons 미공개 | PW anode, DNW/NW cathode topology | Minimal contacts vs schematic contact blocks |
| SA-08 | Gao lattice origin/clipping | Full-SPAD tiling rule 미공개 | 480 nm/186 nm/294 nm direct unit cell | Center origin, edge origin, clipping/exclusion |
| SA-09 | BEOL-effective stack | Thickness/constants 미공개 | Dielectric present, metal opening direct | Effective layers and refractive indices |
| SA-10 | Optical polarization aggregation | Polarization 미공개 | Normal incidence only | Orthogonal runs or average |
| SA-11 | Finite-domain boundary | Unit-cell vs full-cell mismatch | Periodic square simulation precursor | PML/symmetry/finite aperture choice |
| SA-12 | Primary avalanche/defect deck | Papers use different models | P06/P08 physics trends | Frozen deck plus controlled sensitivity |

모든 SA 항목은 case manifest에 기록해야 하며 논문 직접값처럼 표현하지 않는다.

## I. 가능한 3D surrogate XY mask 전략

구체 좌표는 제안하지 않는다. 세 candidate 모두 동일 vertical stack, frozen doping, contact convention, STI depth assumption을 사용해 geometry effect만 비교한다.

### Candidate A - Coarse staircase

- 소수의 orthogonal steps로 25 µm-class quasi-circular envelope를 근사.
- Active-zone STI와 peripheral STI의 역할만 보존.
- 목적: mesh/debug가 쉬운 lower-complexity electrical negative/control model.
- 장점: 빠른 mesh convergence와 2D-to-3D mapping audit.
- 한계: corner density와 perimeter length가 실제 layout과 다를 가능성.

### Candidate B - Medium staircase, recommended primary

- P08 Fig. 18과 P10 Fig. 6의 visual character를 따르는 중간 수준 rectilinear staircase.
- 중앙 PW/DNW junction, native active STI candidate, peripheral STI5, NW/cathode/contact-side topology를 분리.
- 목적: 문헌 topology와 계산 비용의 균형을 가진 primary 3D Reference surrogate.
- 권고: P09 Reference-like active STI2/3/4 + overlapping STI5를 **primary same-lineage candidate**로 사용하되 exact 2024 mask라고 주장하지 않음.
- 필수 split: active STI removal 및 STI5 alignment.

### Candidate C - Fine staircase

- Candidate B보다 더 세밀한 orthogonal approximation으로 perimeter/corner sensitivity 상한을 평가.
- 목적: staircase resolution이 VBD, peripheral field, PEB, optical aperture에 미치는 mesh/geometry sensitivity 확인.
- 한계: GDS 정보 없이 finer geometry가 더 정확하다고 주장할 수 없음.

### Strategy decision

Candidate B를 primary로 권고하고 A/C를 sensitivity bounds로 사용한다. 선택 기준은 외형 유사도가 아니라 frozen electrical fingerprint의 안정성, mesh convergence, peripheral breakdown localization이다.

## J. TCAD split으로 검증해야 하는 항목

### J.1 Correct question

잘못된 질문: “어떤 geometry가 VBD=15.8 V를 만드는가?”

올바른 질문: “문헌 제약과 frozen 2D baseline을 만족하는 plausible 3D geometry 중 어떤 realization이 electrical fingerprint를 안정적으로 보존하는가?”

### J.2 Split order

1. **2D frozen reproduction:** 기존 deck에서 VBD/SCR/field fingerprint 재현 확인.
2. **3D extrusion sanity:** 단순 test extrusion으로 material, contact, dopant mapping, coordinate origin 확인.
3. **Candidate A/B/C split:** doping, models, STI depth, contacts를 고정하고 outer XY staircase만 변경.
4. **Active-STI split:** STI2/3/4 present vs removed/minimized.
5. **Peripheral-STI split:** overlap/reference-like vs aligned; shifted는 optional bound.
6. **Contact split:** minimal electrical contacts vs contact-aware surrogate.
7. **STI-depth sensitivity:** primary topology가 정해진 후 별도 수행.
8. **Physics-model sensitivity:** geometry selection 후 avalanche/defect model split.
9. **Gao Square insertion:** Reference geometry와 doping을 고정하고 optical pattern만 추가.

### J.3 Required electrical outputs

- VBD.
- SCR p-side/n-side, center, width using the same declared extraction rule.
- Centerline electric field and peak field.
- Peripheral/corner electric field.
- Breakdown onset voltage and location.
- Impact-ionization integral/location.
- ATP map and selected line cuts.
- Dark current components: SRH, BTBT/TAT/interface contribution when available.
- Mesh convergence: center, STI edge, junction edge, contacts.
- 2D-to-3D dopant/profile conservation.

### J.4 Acceptance logic

Numerical tolerance를 문헌에서 만들지 않는다. Run 전에 project-level tolerance를 선언하고 다음 순서로 pass/fail한다.

1. Mesh-converged인가?
2. Contact/boundary와 dopant mapping이 2D definition과 일치하는가?
3. VBD가 frozen 15.798 V fingerprint와 predeclared tolerance 내에 있는가?
4. SCR bounds/center/width가 동일 extraction rule에서 안정적인가?
5. Central field가 유지되고 새로운 corner/PEB가 발생하지 않는가?
6. Geometry candidates 간 차이가 model/mesh noise보다 큰가?

3D VBD가 달라졌을 때 점검 순서는 mesh → contact/boundary → dopant mapping → symmetry removal → peripheral field → avalanche model이다. 이 과정을 끝내기 전에 geometry와 doping을 동시에 재-fit하지 않는다.

## K. Gao Square 3D validation에 필요한 정보

### K.1 Directly confirmed unit cell

- Pitch: 480 nm. [직접 실측]
- FF: 15%, silicon area / square unit-cell area. [직접 실측]
- Silicon square: 186 × 186 nm². [직접 실측]
- STI separation: 294 nm. [직접 실측]
- Equal x/y period, square pattern. [직접 실측] [논문 직접 시뮬레이션]

Source: P10 p.6, §2.2.2; the design lineage begins in P07 Table I.

### K.2 Full-SPAD implementation rule

1. Start from the accepted unpatterned 3D Reference geometry.
2. Keep PW/DNW doping, junction, contacts, outer staircase, and native-STI branch fixed.
3. Add only the square optical pattern in the photosensitive-area mask domain.
4. Use the direct 480/186/294 nm unit-cell values in the interior.
5. Treat lattice origin, outer-edge clipping, and contact exclusion as SA-08 variants.
6. Use the same assumed process STI depth as Reference; do not derive depth from 180 nm.
7. Run SDevice/SVisualPy on Reference and Square to check electrical invariance before EMW gain claims.

### K.3 Required invariance checks

- VBD and SCR remain within predeclared comparison tolerances.
- Central and peripheral field changes are reported separately.
- No unintended PEB or new impact-ionization hotspot appears at clipped pattern edges.
- ATP map is either recomputed for Square or the reuse of Reference ATP is explicitly labeled, matching P10's limitation.
- DCR/afterpulsing effects are not inferred from EMW alone.

## L. Reference → Gao validation에서 비교할 수 있는 문헌 수치

| Literature result | Condition | Compare directly to | Do not compare directly to |
|---|---|---|---|
| Optical field magnitude up to 30% gain | 500 nm, FF15, 10 nm trial period, local/profile | Same-condition local optical field profile | 480 nm/940 nm full-SPAD gain |
| Photogeneration up to 60% gain | 500 nm, FF15, 10 nm trial period | Same-condition local G profile | SCR-integrated 940 nm G or measured PDP |
| P07 simulated PDP band gains | 480 nm pitch, FF15/20/25, 400-1000 nm, 2D ATP + 3D FDTD | Compatible simulated Q/PDP spectral trend under matching assumptions | Absolute measured PDP or exact 940 nm number |
| Simulated PDP gain up to 700% | Selected wavelengths, model-specific | Qualitative resonance/upper-bound behavior | 940 nm direct target or measured gain |
| P09 absolute PDP ≈4.2-12% | 620 nm, aligned+Fusion, passive quench | Different-architecture context only | P10 Reference→Square gain |
| P10 FF15 peak gains 28%, 62% | 645 nm peak, Vex 0.4/0.5 V | Same-chip measured PDP relative gain context | Pure optical G gain or 940 nm gain |
| P10 FF15 spectral-average gains 33%, 55% | 400-1000 nm average, Vex 0.4/0.5 V | Broad-band measured context | Single-wavelength 940 nm Q gain |
| P10 FF25 gains up to 131% | High bias, afterpulsing risk | Composite measured upper context | Pure optical enhancement |

### L.1 Recommended comparison hierarchy

1. Reference/Square use identical full-cell geometry, BEOL, source, mesh, boundary, and normalization.
2. Compare local `E` and `G` only to matching local/profile literature metrics.
3. Compare `G_SCR_Int` only as a simulation observable; do not call it PDP.
4. Compute `Q = ∫G×ATP dV` using a declared ATP map and integration volume.
5. Compare Q-derived relative spectral trends to P07/P10 compatible simulation trends.
6. Use P10 measured PDP gains as external experimental context with BEOL, electronics, dead time, afterpulsing caveats.

### L.2 940 nm limitation

P07/P10 spectra include 940 nm within 400-1000 nm, but no audited table gives a dedicated exact 940 nm Reference→FF15 gain. Therefore the project's 940 nm `G_SCR_Int`, `Q`, and gain are new simulation outputs and must not be labeled as direct literature reproduction. [미공개]

## M. 3D baseline 구현 가능 여부

### M.1 Final status

**READY WITH SURROGATE ASSUMPTIONS**

### M.2 Why not READY

- Exact 2024 GDS/mask coordinates are absent.
- P10 Reference의 exact P09 STI branch가 미공개다.
- Native STI dimensions/depth와 contact polygons가 미공개다.
- Full BEOL optical stack와 polarization/boundary details가 미공개다.
- 2D frozen SCR/STI coordinates는 문헌 직접값이 아니다.

### M.3 Why not NOT READY

- Device family, junction topology, size class, non-axis layout character, modified-DNW fingerprint가 충분히 확정된다.
- 7 nm/25 nm stack constraints와 PW/DNW/contact topology가 반복 확인된다.
- 2D frozen baseline은 이미 VBD/SCR electrical fingerprint를 제공한다.
- Gao Square unit-cell dimensions은 직접 공개되어 있다.
- Unknowns can be isolated as geometry/model splits without simultaneous free fitting.

### M.4 Conditions to start implementation

1. Candidate B를 primary XY strategy로 승인하거나 다른 candidate를 명시.
2. 25 µm characteristic envelope의 적용 boundary를 case manifest에 기록.
3. Primary STI branch를 `P09-Reference-like surrogate` 또는 다른 named variant로 선택.
4. Frozen 0.300 µm STI depth를 literature value가 아닌 initial assumption으로 등록.
5. Contact/boundary, avalanche/defect model, BEOL-effective stack, polarization strategy를 case manifest에 고정.
6. Geometry-only electrical validation을 통과하기 전 doping 재-fit과 EMW performance claim을 금지.

### M.5 Recommended first implementation

- Geometry: Candidate B medium staircase.
- Device identity: `Ref2024-unpatterned-P09ReferenceConstrained-surrogate`.
- Doping/vertical process: frozen 2D baseline 그대로 port.
- Native STI: active STI2/3/4 present + peripheral STI5 overlap as primary same-lineage candidate; removal/alignment을 mandatory split으로 실행.
- STI depth: frozen 0.300 µm initial assumption, sensitivity pending.
- Output gate: VBD/SCR/central-peripheral field/onset-location/mesh convergence.
- Optical work: electrical gate 통과 후 Reference 940 nm, then Gao Square 480 nm/FF15.

이 권고는 2024 foundry mask를 복원한다는 뜻이 아니라 가장 추적 가능한 시작점을 선택한다는 뜻이다.

## 3. 필수 연구질문 12개에 대한 답

### Q1. 2024 quasi-circular Reference의 3D top-view geometry에서 직접 알 수 있는 범위는?

25 µm diode class, quasi-circular label, rectilinear/staircase character, contacts와 주변 회로로 인한 비축대칭성까지다. Exact vertices, PW/DNW boundary, native STI coordinates, contact masks는 미공개다.

### Q2. 완전한 rotational symmetry로 취급해도 되는가?

아니다. 원통대칭은 2D electrical surrogate의 계산 가정이며 실제 layout identity가 아니다.

### Q3. circular/pseudo-circular/quasi-circular는 실제 mask에서 어떻게 구현되는가?

Orthogonal rectangular shapes를 계단형으로 배치한 approximation이다. P02, P06, P08, P10의 layout evidence가 이를 반복적으로 지지한다.

### Q4. STI2/3/4/5의 3D topology는 어디까지 알 수 있는가?

P09 Reference에서 STI2/3/4는 active zone, STI5는 junction perimeter overlap에 위치한다. Fusion은 STI2/3/4를 제거/최소화하고 aligned variant는 STI5를 junction edge에 맞춘다. Exact width, depth, spacing, vertices와 P10 Reference의 exact branch는 미공개다.

### Q5. Frozen 2D STI 위치/폭 중 문헌 근거와 순수 surrogate는?

Active-zone STI와 peripheral STI의 역할·순서·overlap/alignment topology는 문헌 constraint다. `0.700-1.300`, `2.975-3.275`, `6.100-6.400`, `9.225-9.525`, `12.200-12.800 µm`의 수치와 폭은 모두 `[surrogate assumption]`이다.

### Q6. 25 µm는 정확히 무엇의 diameter인가?

P10 표현상 diode diameter다. 그러나 PW, DNW, STI perimeter, optical opening 중 어느 mask boundary로 측정했는지는 미공개다.

### Q7. PW/DNW/active-area/STI perimeter를 3D에서 어떻게 구현하는 것이 가장 문헌에 충실한가?

PW/modified-DNW junction을 25 µm-class rectilinear staircase envelope 안에 두고, active STI와 peripheral STI를 독립 mask decisions로 구현하며, NW/contact-side structures를 별도 주변 topology로 둔다. 모든 STI를 concentric ring으로 바꾸지 않는다.

### Q8. Frozen VBD/SCR fingerprint를 3D에서 어떻게 검증해야 하는가?

동일 doping/model/contact를 유지한 geometry-only split에서 mesh-converged VBD, 동일 rule로 추출한 SCR bounds/center/width, central/peripheral field, breakdown onset/location을 비교한다.

### Q9. 3D VBD가 달라졌을 때 geometry/doping 재-fit 전에 무엇을 확인해야 하는가?

Mesh convergence, contact/boundary, 2D-to-3D dopant mapping, coordinate/unit consistency, symmetry-removal effect, peripheral/corner field, avalanche model 순서로 확인한다.

### Q10. Gao Square 480 nm/FF15%를 full-SPAD 3D에서 어떻게 구현해야 하는가?

승인된 unpatterned Reference outer geometry와 doping을 고정하고 photosensitive area에 480 nm x/y pitch, 186 nm silicon square, 294 nm STI separation을 적용한다. Lattice origin과 edge clipping은 명시적 surrogate variants로 처리하고 SDevice electrical invariance를 먼저 검증한다.

### Q11. Reference→Gao improvement를 어떤 문헌 수치와 비교할 수 있는가?

Matching-condition optical field/G profiles 및 compatible simulated PDP/Q spectral trends와 비교할 수 있다. Measured PDP gain은 external experimental context로만 사용한다. 500 nm/10 nm-period local G gain, 400-1000 nm average PDP gain, 645 nm peak gain을 940 nm SCR-integrated G gain과 직접 동일시하면 안 된다.

### Q12. 3D Reference SDE를 바로 구현할 수 있는가?

정확한 mask 복제는 불가능하지만 명시적 surrogate assumptions와 mandatory split을 전제로 구현할 수 있다. 최종 판정은 **READY WITH SURROGATE ASSUMPTIONS**이다.

## 4. 최종 실행 순서

1. Assumption registry SA-01-SA-12 승인 및 case manifest 작성.
2. Frozen 2D reproduction/mesh audit.
3. Candidate A/B/C geometry-only SDE/SDevice split.
4. Active-STI and STI5 branch split.
5. Candidate B primary geometry 확정.
6. Contact/STI-depth/model sensitivities.
7. 3D Reference electrical gate 승인.
8. Reference 940 nm full-cell EMW.
9. Gao Square 480 nm/FF15 full-cell implementation.
10. Square electrical invariance 확인.
11. Reference→Square `E`, `G`, `G_SCR_Int`, `ATP`, `Q` 비교.
12. Compatible literature simulation/measurement와 계층별 비교.
13. 그 이후 Annular 200/215/750/775/835/900/1000 nm set 진행.

## 5. Final claim boundary

허용되는 표현:

> 공개된 2017-2024 28 nm FD-SOI SPAD 연구계열과 frozen 2D electrical fingerprint를 함께 만족하도록 구성한 literature-constrained 3D surrogate Reference.

허용되지 않는 표현:

- STMicroelectronics foundry mask/recipe reproduction.
- Gao 2024 exact GDS reconstruction.
- 2D cylindrical model의 actual 3D geometry 등치.
- Frozen STI/SCR coordinates의 논문 직접값 주장.
- Measured PDP gain과 simulated SCR photogeneration gain의 등치.
- High-bias measured PDP gain을 pure optical gain으로 해석.

최종 목표는 그럴듯한 geometry가 아니라, 직접 근거와 surrogate assumption이 완전히 추적되는 3D baseline이다.