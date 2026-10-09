# CMP SPAD 3D Reference Baseline — SDE Candidate-B v2.6

**확정일:** 2026-10-09 · **연구자:** 주상현(A, jujushmaterial)  
**확정 범위:** 3D 구조·도핑·mesh 생성용 SDE 코드 baseline. **3D SDevice 전기적 특성 검증 완료를 의미하지 않음.**

## 1. 확정 코드 전문 및 원본 보존

- [Candidate-B v2.6 SDE 전체 코드](./CMP_SPAD_3D_CandidateB_v2.6_RadialCoarseBulk_UpperSiZFixed_DualMSH.txt)
- 파일명: `CMP_SPAD_3D_CandidateB_v2.6_RadialCoarseBulk_UpperSiZFixed_DualMSH.txt`
- **1,012줄 / 44,815 bytes / ASCII LF**
- **원본 Git blob SHA:** `da5e8d0dc2534cd80d0ba0b2bcb811c990b00a6b`
- 사용자 승인 코드와 **byte-for-byte 동일**하게 GitHub에 기록하였다. 원본 머리말 및 일부 출력 문구에 남은 `v2.4`는 이전 버전에서 승계된 주석이다. 이번 기록은 실행 코드를 수정하지 않고 파일명과 문서에서 **v2.6**임을 명확히 한다.

## 2. 구조 및 baseline 정체성

본 구조는 Gao 2024의 28 nm FD-SOI, 25 µm-class quasi-circular reference 계열을 제약으로 하되 실제 비공개 GDS/foundry 공정을 복원한 것이 아닌 **literature-constrained surrogate**이다.

| 구조/설정 | 채택 값 또는 정의 | 근거 성격 |
|---|---|---|
| Bulk | Silicon 원통, 반경 24 µm, z=-10~+0.300 µm | [surrogate assumption] |
| UpperSi / BOX | 7 nm / 25 nm | [동일 연구계열 constraint] |
| Active native STI | STI1·STI2·STI3·STI4가 있는 Cartesian-grid staircase | [surrogate assumption] layout |
| Peripheral | staircase STI5 + peripheral STI6/7 | [surrogate assumption] layout |
| Active grid | 17×17 seg.; 유효 257 cells = STI oxide 188 + Si×Si 69 | SDE 구조 정의 |
| 접촉 | anode / cathode / substrate | SDE 구조 정의 |
| PW/Boron `PeakVal` | 5.95×10¹⁷ cm⁻³ | [역산/fit] frozen 2D electrical parameter |
| DNW/Phosphorus `PeakVal` | 3.15×10¹⁷ cm⁻³ | [역산/fit] frozen 2D electrical parameter |
| 2D frozen 전기지문 | VBD 15.7979980544 V, SCR center proxy 0.180202945597 µm | **2D 결과**, 3D 검증값 아님 |

PW/DNW/NW/P+는 3D `General` analytic Gaussian profile로 구현되며, lateral 분포는 `r=hypot(x,y)`에 의존한다. 농도 peak 및 `LatFactor=0.8`의 대응 관계는 frozen 2D에서 가져왔으나, 2D–3D 농도 field 완전 일치와 전기적 동등성은 **추후 검증 대상**이다. Native STI의 구체 폭·좌표·공정값은 논문 비공개이므로 공정 실측값이라고 주장하지 않는다. Reference에는 의도적 optical periodic pattern과 FF/pitch 정의가 없다.

## 3. Dual MSH 동작

| 생성물 | UpperSi 7 nm | Dopants | 목적 |
|---|---|---|---|
| `n@node@_msh.tdr` | **Oxide**, frozen 2D electrical surrogate convention | Bulk의 PW/DNW/NW/P+ 포함 | SDevice 2D→3D electrical 비교 |
| `n@node@_physical_msh.tdr` | **Silicon**, 실제 FD-SOI 적층 | 동일 Bulk doping 정의 포함 | 3D 실제 재료 구조·도핑 및 optical geometry 기반 |

첫 번째 MSH 생성 후 기존 69개 UpperSi region을 Silicon으로 복구하고 두 번째 meshing을 실행한다. **두 MSH는 재료가 다르므로 동일한 전기적 경계조건을 가진다고 단정하지 않는다.** Physical MSH의 UpperSi에는 별도 implant가 정의되지 않는다. EMW 광학 시뮬레이션의 mesh/광학 물성은 별도 solver 검증이 필요하다.

## 4. v2.6 확정 Mesh 전략

**MeshScale=1.50**. 단 UpperSi 두께 방향 **Zmax=3.5 nm, Zmin=2.5 nm는 고정**한다. 아래 공간 및 수치는 *mesh 설정값*이지 SDevice 수렴 검증 결과가 아니다.

| 단계 | refinement 대상 | 방향 |
|---|---|---|
| Global | 전체 도메인 | XY max 10.5 µm / XY min 3.15 µm, 깊은 Bulk coarse |
| M2 | r≤19.5 µm, z=-3.10~-1.20 µm | 원통형 coarse→medium transition |
| M2 | r≤17.3 µm, z=-1.70~-0.10 µm | DNW transition |
| M2 | r≤19.5 µm, z=-1.60~+0.300 µm | 수직 도핑 gradient의 제한된 refinement |
| M2 | r≤12.5 µm, z=-0.13~+0.300 µm | 잠정 SCR 주변 refinement (실제 solved SCR 아님) |
| M3 | BOX/UpperSi 및 anode | BOX 완화, UpperSi Z 해상도 고정 |
| M4 | 실제 Cartesian STI1–4 | 상부 STI-sidewall 국소 refinement |
| M5 | r=11.9–15.8 µm, z=-0.30~+0.332 µm | STI5/PEB annular *mesh-only* envelope |
| M5 | r=13.85–15.75 µm, z=-0.66~+0.300 µm | Cathode NW annular window |
| M5 | r=16.75–19.65 µm, z=-0.72~+0.332 µm | STI6/7 + outer pickup annular window |

임시 cylinder/annulus에서 `extract-refpolyhedron`으로 Ref/Eval window를 추출하고 생성된 임시 형상은 삭제한다. **실제 physical native-STI를 concentric ring으로 바꾸지 않는다.** `zCuts`를 제거하고 `fitInterfaces=FALSE`, `skipSameMaterialInterfaces=TRUE`, `maxNeighborRatio=5`를 적용한 mesh-only 변경이다. Tetrahedral element 자체는 직선 모서리 요소다.

## 5. 개발 버전 타임라인

| 버전 | 주요 조치 | 결과/상태 |
|---|---|---|
| v2.1 및 이전 | Boolean·contact imprint에서 B-rep 비정합 반복 | 원인 분리 |
| v2.2 M0/M1 | Bulk에 contact pre-imprint, 188개 ActiveSTI oxide를 전부 union하지 않음 | M0 geometry, M1 doped mesh 생성 성공 |
| v2.3 | UpperSi=Oxide electrical / UpperSi=Silicon physical **Dual MSH** | physical doping/geometry SVisual 확인 |
| v2.4 | wide cuboid/tile 기반 단계적 정밀화 | Stage5에서 boundary tree 폭증 확인 |
| v2.5 | 전체 mesh 1.5배 완화, UpperSi Z 3.5/2.5 nm 유지 | bulk 과밀 및 수직 격자 기둥 문제 관찰 |
| **v2.6** | **radial+depth-limited refinement, aggressive coarse bulk, narrow STI strips** | **사용자 검토 및 3D SDE baseline 채택** |

정확한 개별 이전 버전 작업일은 별도 로그가 확인되지 않으므로 버전 순서로 기록한다. v2.2 M1의 60,303 points / 320,170 tetrahedra는 **그 버전의 검증 로그**이며 v2.6 결과값으로 사용하지 않는다.

## 6. 확인된 사실과 미완료 Gate

**확인:** 사용자 SVisual 화면의 v2.6 3D 구조, doping concentration 컬러맵, 절단면 mesh를 기반으로 채택 결정. 기존 설계의 UpperSi·BOX·native STI·도핑 위치와 부합하는 형상 관찰.

**미완료:** v2.6 전체 mesher 로그의 최종 요소 수·품질·두 출력 비교, 정량 mesh convergence, 2D/3D boron/phosphorus line cuts, 3D VBD·SCR·reverse I–V·center/edge E-field·PEB·impact ionization·ATP, UpperSi 물질 전기 민감도, Reference 3D EMW. **3D electrical validated baseline이라고 주장하지 않는다.**

## 7. 근거 및 활동 기록

- [2026-10-09 v2.6 확정 타임라인](../../../timeline/2026-10/2026-10-09.md)
- [3D 문헌 재검토](./SPAD_3D_Baseline_Reaudit_Report.md)
- [3D 재검토 결정](./CMP_SPAD_3D_Baseline_Reaudit_Decision_Record_2026-10-06.md)
- [2D frozen SDE](../spad-baseline-static-freeze/SDE_reference_baseline_v1.3_redarea_uniform_meshconv.txt)
- [공동 SPAD 연구계획서](../../../../../shared/decisions/SPAD_연구계획서.md)

**AI 사용:** ChatGPT(코드 수정 보조, troubleshooting, 문서화). 실제 TCAD 실행은 사용자 서버에서 수행되었으며 이 문서는 사용자 이미지·대화 기록·SDE 원본을 근거로 한다. 실측/논문값, 2D 시뮬레이션, surrogate assumption, 미검증 결과를 구분한다.
