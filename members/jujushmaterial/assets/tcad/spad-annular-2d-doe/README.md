# SPAD A — Annular FF15 2D Radial-Pitch DOE

이 폴더는 A(jujushmaterial)의 proposed concentric annular Si/STI optical structure에 대한 2D radial-pitch screening용 코드와 설정 기록을 보관한다.

## Status

- 단계: 160-case 2D screening DOE 완료 / 1차 radial-pitch response 분석 완료
- 상태: In Progress
- 2D integrated global optimum: 900 nm (Gain_Ref = 1.112922, Reference 대비 +11.292%)
- Gmax_SCR hotspot maximum: 835 nm
- preliminary 3D validation set: 750 / 775 / 835 / 900 / 1000 nm
- final 3D optical claim: 아직 수행하지 않음

## Core rule

- Reference optical-pattern FF = N/A
- Proposed annular intentional optical-pattern Si FF = 15% fixed
- independent variable = `RadialPitch`
- dependent variable = `RingWidth`
- RingWidth는 finite 3D annulus area accounting으로 자동 계산
- frozen native STI1~5는 이동하지 않음
- native-STI overlap은 별도 diagnostic이며 15% pattern FF를 보상하기 위해 ring을 넓히지 않음

## DOE

- `RadialPitch = 0.200 ~ 1.000 um`
- basic step = `0.005 um`
- `0.270 um` 제외
- total = `160 cases`
- existing 0.200 case + imported 159 cases

## Files

- `CMP_SPAD_A_Annular2D_FF15_RadialPitch_SDE_v1.1.txt`
  - frozen baseline + intentional annular-pattern diametric cross-section 생성
  - exact annular area FF solver 및 native-STI overlap diagnostic
- `CMP_SPAD_A_Annular2D_FF15_SNMesh_v1.0.txt`
  - 2D tensor mesh
- `CMP_SPAD_A_Annular2D_FF15_940nm_EMW_v1.0.txt`
  - 940 nm TE EMW screening
- `CMP_SPAD_A_Annular2D_FF15_SVisualPy_DOE_v1.1.txt`
  - FF 검증, SCR-slab OpticalGeneration integration, DOE output
- `CMP_SPAD_A_RadialPitch_Split_160cases_5nm.txt`
  - 160-case split reference
- `RadialPitch_import_159.csv`
  - 기존 0.200 case를 제외한 SWB import용 159 cases
- `CMP_SPAD_A_2D_Annular_RadialPitch_DOE_Setup_2026-09-17.md`
  - 방법, 범위, 이유, metric, 현재 상태 상세 기록

## Important limitation

2D geometry는 annular 구조의 diametric/radial cross-section을 사용하지만 EMW가 이를 원통대칭으로 회전하여 계산하는 것은 아니다. 2D 결과는 screening용이며, selected candidate는 실제 3D concentric annular SDE/EMW로 검증해야 한다.


---

## 11. 2D DOE analysis result — 2026-09-28

- total: 160 cases, RadialPitch 200–1000 nm, 270 nm excluded
- PatternFF: 15% for all cases
- first `Gain_Ref > 1`: **730 nm**
- 2D integrated global optimum: **900 nm**
- 900 nm `G_SCR_Int=6.714802e+21`
- 900 nm `Gain_Ref=1.112922` (**+11.292%** vs Reference)
- global `Gmax_SCR` hotspot: **835 nm**, `3.175725e+21`

900 nm는 finite annular aperture + frozen native-STI geometry에서 얻은 **2D extruded screening optimum**이며 exact 3D concentric-annular optimum으로 확정하지 않는다.

### Analysis files

- [Detailed analysis](CMP_SPAD_A_2D_Annular_RadialPitch_DOE_Analysis_2026-09-28.md)
- [160-case data](2026-09-28-annular-2d-doe-160cases.csv)
- [Excel workbook](2026-09-28-annular-2d-doe-analysis.xlsx)
- [G_SCR_Int plot](2026-09-28-g-scr-int-vs-radial-pitch.svg)
- [Gmax_SCR plot](2026-09-28-gmax-scr-vs-radial-pitch.svg)
- [Gain_Ref plot](2026-09-28-gain-ref-vs-radial-pitch.svg)

Preliminary 3D validation set: `750 / 775 / 835 / 900 / 1000 nm`.


## Repository analysis package

2026-09-28 160-case DOE 분석 결과는 원본/분석/시각화 파일을 분리하여 함께 보관한다.

- raw scalar table: `2026-09-28-annular-2d-doe-160cases.csv`
- editable analysis workbook: `2026-09-28-annular-2d-doe-analysis.xlsx`
- clean vector plot image: `2026-09-28-g-scr-int-vs-radial-pitch.svg`
- clean vector plot image: `2026-09-28-gmax-scr-vs-radial-pitch.svg`
- clean vector plot image: `2026-09-28-gain-ref-vs-radial-pitch.svg`

Plot은 DOE point marker를 강조하지 않고 **single connected line**으로 표시한다. `Gain_Ref` plot에는 Reference 기준인 `Gain_Ref=1` horizontal line을 포함한다. SVG는 GitHub에서 바로 확인 가능한 vector image이고, XLSX는 데이터와 chart를 편집할 수 있는 분석본이다.

Excel에서 chart를 다시 만들 때는 `RadPitch_nm`을 numeric x-axis로 사용하는 **XY Scatter with Straight Lines**를 권장하며 marker는 `None`으로 설정한다. 일반 Line chart의 category axis를 사용할 경우 270 nm 제외 구간의 실제 x-spacing이 보존되지 않을 수 있다.

