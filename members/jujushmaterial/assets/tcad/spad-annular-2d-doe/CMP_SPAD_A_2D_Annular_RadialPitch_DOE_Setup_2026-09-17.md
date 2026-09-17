# CMP SPAD A — 2D Annular FF=15% Radial-Pitch DOE Setup Record

## 1. Record scope

이 문서는 A(주상현)의 940 nm optical-structure 연구에서, frozen 28 nm FD-SOI surrogate reference를 유지한 채 proposed concentric annular Si/STI optical pattern의 radial pitch를 2D Sentaurus EMW로 screening하기 위해 구성한 DOE와 코드의 현재 상태를 기록한다.

현재 단계는 final 3D annular optical claim이 아니라 2D diametric/radial screening 단계이다. 전체 DOE의 최종 optical 결과는 아직 확정하지 않았으며, 초기 pitch case의 SDE/TDR geometry를 확인한 상태이다.

## 2. 연구 질문과 고정 조건

A의 독립 연구 질문은 동일한 FD-SOI SPAD electrical core와 동일 Si pattern fill factor에서 square optical pattern을 concentric annular pattern으로 바꾸고 radial pitch를 조절할 때 940 nm SCR/active-region photogeneration이 증가하는지를 확인하는 것이다.

고정 조건:
- common frozen surrogate baseline electrical/core geometry
- native STI1/2/3/4 및 peripheral STI5 유지
- PW/DNW profile 및 SCR 위치 유지
- Upper Si = 7 nm
- BOX = 25 nm
- native STI depth = 300 nm
- wavelength = 940 nm
- proposed annular intentional optical-pattern Si FF = 15%
- optical material/source convention은 frozen Reference EMW와 동일 계열 사용

Reference에는 intentional periodic optical pattern이 없으므로 Reference FF는 N/A이다.

## 3. Workbench 프로젝트와 flow

서버 프로젝트 절대경로:

```text
/user/semi/semi7/Myproject/CMB_baseline_EMW_split/
```

Workbench flow:

```text
SDE -> SNMESH -> EMW -> SVisualPy
```

현재 입력 parameter:

```text
DNW_Dose    = 3.15e17 cm^-3  # analytic Gaussian PeakVal, physical implant dose 아님
PW_Dose     = 5.95e17 cm^-3  # analytic Gaussian PeakVal, physical implant dose 아님
MeshScale   = 0.4
RadialPitch = DOE independent variable [um]
```

이번 A geometry DOE에서 실제로 변화시키는 독립변수는 `RadialPitch` 하나이다.

## 4. 사용 코드

현재 DOE에 사용하는 파일:

```text
CMP_SPAD_A_Annular2D_FF15_RadialPitch_SDE_v1.1.txt
CMP_SPAD_A_Annular2D_FF15_SNMesh_v1.0.txt
CMP_SPAD_A_Annular2D_FF15_940nm_EMW_v1.0.txt
CMP_SPAD_A_Annular2D_FF15_SVisualPy_DOE_v1.1.txt
```

v1.1에서 핵심 수정된 파일은 SDE와 SVisualPy이다. SNMESH와 EMW는 v1.0을 유지한다.

## 5. Frozen native STI geometry

오른쪽 half 기준 surrogate native STI geometry:

```text
STI1 = 0.700 ~ 1.300 um, width 0.600 um
STI2 = 2.975 ~ 3.275 um, width 0.300 um
STI3 = 6.100 ~ 6.400 um, width 0.300 um
STI4 = 9.225 ~ 9.525 um, width 0.300 um
STI5 = 12.200 ~ 12.800 um, width 0.600 um
```

A의 radial-pitch DOE에서는 이 native STI의 위치·폭·깊이를 sweep하지 않는다.

## 6. Annular pattern aperture와 FF 정의

현재 intentional optical pattern의 radial aperture는 다음처럼 정의한다.

```text
r_pattern_inner = 0.55 um  # central anode-window edge
r_pattern_outer = 12.20 um # STI5 start
```

이 범위는 `[surrogate design definition]`이며 foundry 공개값으로 주장하지 않는다.

FF는 2D 단면의 단순 길이비 `RingWidth / RadialPitch`로 계산하지 않는다. 3D concentric annular geometry를 가정하여 각 Si ring의 면적

```text
A_i = pi * (r_outer,i^2 - r_inner,i^2)
```

을 합산하고 finite aperture의 마지막 partial cell까지 반영하여

```text
A_Si,intentional-annular / A_pattern-aperture = 0.15
```

가 되도록 `RingWidth`를 각 `RadialPitch`에서 자동 역산한다.

따라서:
- independent variable = RadialPitch
- dependent variable = RingWidth
- `PatternFF_3D = 0.15`가 primary geometry constraint

## 7. Native STI overlap 처리

frozen native STI가 intentional Si ring과 겹치는 경우에도 RingWidth를 다시 넓혀 보상하지 않는다. Gao benchmark와의 동일 pattern FF 비교를 유지하기 위해 intentional annular pattern 자체의 FF를 15%로 먼저 고정한다.

native STI overlap은 별도 diagnostic으로 계산한다.

```text
PatternFF_3D                   # primary constraint, target 0.15
FinalSiFraction_AfterNativeSTI # overlap 후 실제 남는 intentional Si fraction
NativeOverlapFraction_PatternSi
```

즉 `FinalSiFraction_AfterNativeSTI`는 geometry interaction diagnostic이며 최적화 독립변수가 아니다.

## 8. 2D geometry의 의미

SDE는 annular 3D-area rule로 계산한 ring width를 오른쪽 radial half의 Si/STI stripe 단면으로 구현한 뒤 x=0 mirror로 full diametric cross-section을 만든다.

중요한 제한:
- FF calculation: 3D annular area 기반
- SDE structure: annular pattern의 diameter/radial cross-section
- 2D EMW: out-of-plane extruded 2D FDTD screening
- 2D 결과를 exact 3D cylindrical/annular EMW result로 해석하지 않음
- 유망 pitch 후보는 이후 실제 3D concentric annular SDE/EMW로 재검증

작은 pitch에서 TDR에 STI/Si stripe가 매우 많이 보이는 것은 예상된 결과이다. 예를 들어 0.200 um pitch는 한쪽 radial aperture에 약 58개의 full period가 들어가고 mirror 후 양쪽에 반복되므로 전체 화면에서는 매우 조밀하게 보인다.

## 9. DOE 범위

1차 broad screening 범위:

```text
RadialPitch = 0.200 ~ 1.000 um
basic step  = 0.005 um = 5 nm
```

모든 5 nm grid를 포함하면 161 cases이나 `0.270 um` 한 점을 제외하여 최종 160 cases로 구성하였다.

최종 case 구성:

```text
0.200, 0.205, 0.210, ... 0.265,
# 0.270 excluded
0.275, 0.280, ... 0.480, ... 0.995, 1.000 um
```

총 DOE 수:

```text
161 nominal grid points - 1 excluded point = 160 cases
```

기존 SWB에 `RadialPitch=0.200` case가 이미 있었기 때문에 신규 import CSV에는 0.205~1.000 um 중 0.270 um를 제외한 159 cases를 넣었다.

## 10. 0.270 um 제외 이유

finite-aperture annular FF solver에서 0.270 um pitch는 pattern aperture 끝에 약 0.283 nm 수준의 매우 얇은 terminal STI fragment를 만들 수 있다.

현재 tensor mesh의 `minCellSize=5 nm`보다 훨씬 작은 feature이므로 geometry/mesh/time-step 측면에서 불필요한 수치 민감성을 유발할 수 있어 1차 screening에서 제외하였다.

이 제외는 물리적 최적 pitch 부정이 아니라 현재 2D numerical screening mesh에서의 numerical guard이다.

## 11. DOE import 방법

MobaXterm에서 다음 CSV를 생성하였다.

```bash
cd /user/semi/semi7/Myproject/CMB_baseline_EMW_split
printf 'DNW_Dose,PW_Dose,MeshScale,RadialPitch\n' > RadialPitch_import_159.csv
seq 205 5 1000 | awk '$1 != 270 {printf "3.15e17,5.95e17,0.4,%.3f\n",$1/1000}' >> RadialPitch_import_159.csv
```

검증:
- header 포함 160 lines
- 신규 experiments 159
- 0.480 um 포함 확인
- 0.270 um 미포함 확인

SWB Import Experiments에서는 header parsing 오류를 피하기 위해 headerless copy를 만들어 `Header=None`, `Skip First=0`으로 가져오는 우회법도 사용하였다.

parameter-column mapping:

```text
Column 0 -> DNW_Dose
Column 1 -> PW_Dose
Column 2 -> MeshScale
Column 3 -> RadialPitch
```

## 12. SNMESH 설정

`CMP_SPAD_A_Annular2D_FF15_SNMesh_v1.0.txt`:

```text
global maxCellSize x/y = 0.025 um
minCellSize            = 0.005 um
grading                = off
```

annular-pattern + SCR neighborhood:

```text
window = x[-12.20, 12.20], y[-0.340, 0.800] um
maxCellSize x/y = 0.010 um
```

critical yCuts:

```text
-0.332, -0.325, -0.300, 0.000, 0.800 um
```

## 13. EMW 설정

`CMP_SPAD_A_Annular2D_FF15_940nm_EMW_v1.0.txt`에서 모든 DOE case는 동일 조건을 사용한다.

```text
Wavelength      = 940 nm
Incidence       = normal / fromTop
Polarization    = TE
Signal          = Harmonic
Intensity       = 1.0 W/cm^2
Temperature     = 300 K
X boundary      = PeriodicOblique
Y boundary      = CPML
CPML thickness  = 15
TotalTimeSteps  = 50000
Detector StepX/Y/Z = 1/1/1
```

## 14. Frozen SCR와 optical metric

SVisualPy는 frozen electrical baseline의 SCR fingerprint를 사용한다.

```text
SCR p-side  = 0.00952007710343 um
SCR n-side  = 0.350885814092 um
SCR center  = 0.180202945597 um
SCR width   = 0.341365736988 um
```

Reference denominator:

```text
G_REF_SCR_INT = 6.03348761659e21 cm^-3 s^-1 um^2
```

primary ranking metric:

```text
G_SCR_Int
G_SCR_Avg
Gain_Ref
GainPct_Ref
```

`Gain_Ref = G_SCR_Int(annular case) / G_REF_SCR_INT`로 정의한다.

보조 diagnostic:

```text
G180_Avg
G180_Max
G180_BandAvg
R180_Max_um
Gmax_SCR
Rmax_SCR_um
Ymax_SCR_um
YPeakInt_nm
dYPeak_nm
```

단일 hotspot maximum만으로 최적 pitch를 선정하지 않는다.

## 15. SWB DOE output fields

SVisualPy v1.1은 다음 항목을 `DOE:` 형식으로 출력한다.

```text
RadPitch_nm
RingWidth_nm
AnnSTI_nm
PatternFF
FinalSiFF
NativeOvPct
N_Radial
G_SCR_Int
G_SCR_Avg
Gain_Ref
GainPct_Ref
G180_Avg
G180_Max
G180_BandAvg
R180_Max_um
Gmax_SCR
Rmax_SCR_um
Ymax_SCR_um
YPeakInt_nm
dYPeak_nm
```

## 16. Reference baseline의 geometric Si fraction diagnostic

Reference의 공식 optical-pattern FF는 N/A이다. 단, 현재 A comparison aperture `r=0.55~12.20 um`에서 native STI1~4를 concentric annulus로 해석한 equivalent geometric Si-area fraction은 비교용 diagnostic으로 계산할 수 있다.

```text
native-STI area fraction ~= 8.3817%
equivalent geometric Si fraction ~= 91.6183%
```

이 값은 `[surrogate geometry calculation]`이며 Gao의 optical-pattern FF=15%와 동일 개념의 공식 Reference FF로 사용하지 않는다.

## 17. 현재 확인 상태

확인된 사실:
- SWB에 `RadialPitch` parameter가 등록됨
- 160-case DOE 구성이 준비됨
- 0.200, 0.205, 0.210, 0.215 um 등 초기 SDE/TDR geometry에서 조밀한 intentional Si/STI stripe가 생성되는 것을 확인함
- 작은 pitch에서 많은 stripe가 보이는 것은 radial aperture 내 period 수가 많고 mirror된 diametric cross-section이기 때문임

아직 미완료:
- 160-case 전체 EMW 결과 완료/정리
- Gain_Ref vs pitch curve 분석
- local maximum / plateau clustering
- 약 5개 3D candidate 선정
- 실제 3D concentric annular SDE/EMW 검증
- Gao Square 480 nm / FF15%와 최종 동일조건 3D 비교

## 18. 후보 선정 원칙

2D screening 종료 후 단순 상위 1~5개만 선택하지 않는다.

- low-pitch regime 대표
- mid-pitch regime 대표
- high-pitch regime 대표
- local maximum
- stable plateau

등을 고려해 약 5개 후보를 선정한 뒤 3D EMW로 재검증한다.

## 19. Provenance classification

- Gao square 480 nm / FF15 / 186x186 nm2 / 294 nm separation: `[논문 직접 보고]`
- frozen SCR 및 Reference 2D optical metric: `[본 프로젝트 TCAD 결과]`
- native STI absolute dimensions: `[surrogate assumption]`
- annular pattern aperture 0.55~12.20 um: `[surrogate design definition]`
- 0.200~1.000 um DOE range 및 5 nm step: `[DOE design choice]`
- 0.270 um 제외: `[numerical screening choice]`
- Reference equivalent geometric Si fraction 91.6183%: `[surrogate geometry calculation]`

## 20. AI 사용 및 검증

- 사용한 AI: ChatGPT
- 사용 목적: annular FF area solver 설계 보조, SDE/SVisualPy 코드 작성·검토, DOE 범위 구성, 기록 구조화
- 검증 방법: 실제 SDE/SNMesh/EMW/SVisualPy deck 내용, SWB `gtree.dat`, MobaXterm에서 생성한 CSV의 line count/head/tail/grep 결과, 초기 TDR geometry와 대조
