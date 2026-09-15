# SPAD Baseline Implementation

CMP SPAD B-side의 문헌 제약 기반 surrogate baseline 구현에 사용하는 Sentaurus Workbench 덱 원문 보관 위치이다.

이 디렉터리에는 SProcess/SNMesh/SDevice baseline reconstruction flow의 현재 실행 원문을 보관한다. SCR 최종 비교용 SVisualPy는 혼용을 막기 위해 `../spad-baseline-implementation-SCR/`에서 15.6 V 기준 파일 하나만 관리한다. 목적은 실제 ST foundry manufacturing recipe를 복원하는 것이 아니라, 공통 SDE/SDevice electrical baseline과 전기적으로 동등한 surrogate process baseline을 구현하는 것이다.

## Baseline authority

공통 baseline의 구조와 electrical target은 프로젝트의 공통 SDE/SDevice baseline을 따른다.

현재 B-side SProcess 구현에서는 SDE에서 사용한 analytic PW/DNW profile을 process-calibration target으로 사용하고, 최종적으로 다음 electrical quantity가 공통 baseline과 정합되는지 SDevice에서 확인한다.

- breakdown voltage `VBD`
- SCR center 및 width
- central/peripheral electric field
- avalanche-generation peak position
- normalized doping-profile trend

현재 단계는 baseline reconstruction이며, PEB·dark current·ATP·temperature robustness 개선을 목표로 하는 B-track 본 optimization과 구분한다.

## Files

```text
CMP_SPAD_BaselineImplementation_SProcess.txt
CMP_SPAD_BaselineImplementation_SNMesh1.txt
CMP_SPAD_BaselineImplementation_SNMesh2.txt
CMP_SPAD_BaselineImplementation_SDevice.txt

# SCR 최종 비교용 SVisualPy
../spad-baseline-implementation-SCR/CMP_SPAD_BaselineImplementation_SVisualPy_V156SCR.txt
```

### CMP_SPAD_BaselineImplementation_SProcess.txt

B-side surrogate process baseline을 구현하는 Sentaurus Process command이다.

주요 역할:

- 공통 SDE v1.3 geometry를 기준으로 SOI/STI 구조 재현
- DNW / PW / NW implant 수행
- PW를 fixed shallow implant + deeper trim implant의 two-energy 구조로 구현
- DNW와 PW에 별도 anneal을 두지 않고 하나의 common WELL RTA 적용
- well RTA 이후 local UpperSi / BOX removal 수행
- shallow P+ anode/substrate contact implant 및 fixed short contact spike 적용
- final PLX/TDR 및 contact 포함 SProcess structure export
- PW/DNW profile 비교용 cut을 `r=0`, `r=4.6875 um`, `r=13 um`에서 저장
  - common RTA 전: `n@node@_B_R_r0/r4p6/r13.plx`
  - common RTA 후: `n@node@_A_R_r0/r4p6/r13.plx`
  - final profile: `n@node@_F_r0/r4p6/r13.plx`
  - `r=4.6875 um` cut은 SDE baseline과 PW/DNW active-profile을 같은 central-active-region 위치에서 비교하기 위해 추가
- 공정 단계별 TDR snapshot을 짧은 node 기반 이름으로 저장: `SOI`, `STI`, `DNW`, `PW`, `NW`, `RTA`, `BOX`, `PP`, `SPK`, final

현재 SWB Parameter로 등록된 다음 9개 값은 모두 command 내부에서 `@PARAMETER@` 형식으로 입력받는다.

```text
DNW_DOSE
DNW_E
PW_TRIM_E
PW_FIXED_E
PW_TRIM_FRAC
PW_FIXED_FRAC
PW_TOTAL_DOSE
RTA_T
RTA_t
```

현재 coarse baseline calibration에서는 다음 항목을 중심으로 sensitivity를 확인한다.

- DNW Dose
- DNW Energy
- Common RTA Temperature
- Common RTA Time

`PW_TRIM_E`는 현재 95 keV로 유지하며, baseline candidate 선정 후 SCR 위치의 fine correction이 필요할 때 dependent trim variable로 사용한다. 나머지 PW parameter도 SWB Parameter 상태를 유지하며 현재 experiment row에서 동일한 값으로 고정한다.

SProcess mesh는 현재 17-case 반복 계산을 위한 FINE-Lite calibration mesh이다. 최종 surrogate baseline freeze 전에는 true-FINE 조건의 재검증이 필요하다.

### Output-name compatibility

SProcess final TDR basename은 짧은 이름인 `n@node@`로 저장되어 `n<node>_fps.tdr`이 생성된다. SNMesh1과 SNMesh2도 이에 맞춰 `n@node|sprocess@_fps.tdr`를 각각 geometry input 및 SubMesh profile source로 사용하도록 정합화했다. 따라서 현재 SProcess -> SNMesh1 -> SNMesh2 연결에서 legacy `BL_*_CH7R4_FINELITE_fps.tdr` 이름은 더 이상 사용하지 않는다.

### CMP_SPAD_BaselineImplementation_SNMesh1.txt

SProcess 결과에서 device remesh에 사용할 geometry boundary를 추출하는 첫 번째 Sentaurus Mesh pass이다.

주요 역할:

- upstream SProcess node에 dependency 설정
- upstream SProcess의 `n@node|sprocess@_fps.tdr`을 입력으로 사용
- `Mesh2bnd` Tools operation 수행
- `useDFISEcoordinates` 유지
- geometry boundary인 `n@node@_bnd.tdr` 생성

이 단계는 doping profile을 새 mesh에 interpolation하는 단계가 아니다. SProcess structure에서 boundary representation을 추출하는 geometry pass이다.

### CMP_SPAD_BaselineImplementation_SNMesh2.txt

SNMesh1에서 얻은 boundary에 SProcess doping/profile 데이터를 다시 mapping하고 SDevice용 electrical mesh를 생성하는 두 번째 Sentaurus Mesh pass이다.

주요 역할:

- immediately upstream SNMesh1의 `n@node|-1@_bnd.tdr`을 geometry input으로 사용
- SProcess의 `n@node|sprocess@_fps.tdr`을 `SubMesh` profile source로 사용
- SProcess field/profile을 새로운 device mesh에 interpolation
- 최종 `n@node@_msh.tdr` 생성

Electrical refinement는 다음 영역을 구분해 적용한다.

- global / deep bulk
- broad depletion region
- PW/DNW/NW doping-profile region
- expected SCR/multiplication region
- PW/DNW metallurgical-junction region
- thin UpperSi / BOX stack
- central P+ anode
- native STI1–STI4
- STI5 / active edge / PEB-sensitive peripheral region
- outer well / substrate pickup region

이 mesh refinement 값은 numerical surrogate setting이며 실제 foundry mesh를 의미하지 않는다.

### CMP_SPAD_BaselineImplementation_SDevice.txt

SProcess에서 구현한 candidate가 공통 electrical baseline과 얼마나 가까운지 확인하는 VBD/SCR calibration용 Sentaurus Device command이다.

현재 제공된 17-case flow에서는 immediately upstream SNMesh2의 `n@node|-1@_msh.tdr`을 입력 mesh로 사용한다.

주요 physics 및 breakdown 설정:

- `Fermi`
- `EffectiveIntrinsicDensity(OldSlotboom)`
- doping-dependent mobility
- `HighFieldSaturation(GradQuasiFermi)`
- `SRH`, `Auger`
- `Avalanche(vanOverstraeten GradQuasiFermi)`
- `AvalPostProcessing`
- `BreakAtIonIntegral`
- `ComputeIonizationIntegrals(direction="eGradQuasiFermi")`

VBD는 ionization-integral criterion을 이용해 평가한다.

주요 snapshot:

```text
15.0 V
15.4 V
15.6 V
15.8 V
16.0 V
16.4 V
18.0 V
20.0 V
22.0 V
24.0 V
```

`BreakAtIonIntegral` 조건을 사용하므로 candidate의 breakdown이 특정 snapshot bias보다 먼저 발생하면 그 이후 TDR은 생성되지 않을 수 있다.

### SCR 최종 비교용 SVisualPy

현재 baseline reconstruction의 공식 SCR 비교는 `../spad-baseline-implementation-SCR/CMP_SPAD_BaselineImplementation_SVisualPy_V156SCR.txt` 하나만 사용한다.

- 평가 bias: **15.6 V**
- 입력 snapshot: `V156_des.tdr`
- SCR 정의: center cutline에서 net-doping zero crossing을 junction으로 잡고, junction 양쪽의 `|E| = 1.0e5 V/cm` crossing을 SCR boundary로 사용
- project coordinate: `z_if = raw_y - 0.300 um`
- SCR crossing 검색범위: **-0.300 ~ +1.30 um**
  - raw coordinate로는 **0.000 ~ 1.600 um**
  - 즉 bulk-Si physical surface부터 검색

과거의 15.0 V `V150` SVisualPy는 초기 candidate에서 위치 이동을 임시 확인하기 위한 diagnostic 파일이었고, SDE baseline과의 최종 동일-bias 비교에 부적합하므로 current asset에서 삭제하였다.


## SWB relationship

```text
SProcess
    |
    v
SNMesh1
  Mesh2bnd
    |
    v
SNMesh2
  SProcess profile interpolation
  + electrical remesh
    |
    v
SDevice
  VBD / SCR / field calculation
    |
    v
SVisualPy
  DOE metric extraction
```

17-case baseline calibration에서는 각 experiment의 SProcess parameter가 달라질 수 있으므로 SProcess profile → SNMesh2 mapping → SDevice 결과가 같은 experiment branch에서 연결되어야 한다.

## Coordinate convention

SProcess와 SMesh DF-ISE output에서 사용하는 현재 depth 기준은 다음과 같다.

```text
bulk-Si surface              raw y = 0.000 um
grating/Si interface anchor  raw y = 0.300 um
project common depth         z_if = raw_y - 0.300 um
```

SVisualPy는 위 기준으로 SCR 및 avalanche position을 project common coordinate에 변환한다.

`180 nm` optical anchor는 grating/Si interface에서 SCR 방향으로 약 180 nm라는 공통 optical/electrical reference이며 STI depth를 의미하지 않는다.

## Current calibration scope

현재 17-case set은 performance optimization DOE가 아니라 surrogate baseline reconstruction을 위한 calibration set이다.

현재 비교하는 주요 process axis:

- DNW Dose
- DNW Energy
- Common RTA Temperature
- Common RTA Time

baseline candidate는 VBD 하나만으로 선정하지 않고 다음 항목을 함께 본다.

- SDE target 대비 PW/DNW profile plausibility
- VBD proximity
- SCR center / width
- central/peripheral electric-field distribution
- avalanche onset/peak position

PEB, dark current, ATP 및 temperature robustness는 baseline candidate 선정 기준으로 사용하지 않으며, surrogate baseline freeze 이후 B-track 본 연구에서 평가한다.

## Current SCR comparison rule

- SDE baseline과 SProcess candidate의 SCR은 **동일하게 15.6 V**에서 비교한다.
- candidate가 `VBD < 15.6 V`라 `V156_des.tdr`이 생성되지 않으면 SCR metric은 `NA` / `SCR_OK=0`으로 남긴다.
- 이 경우 15.0 V SCR로 대체하지 않는다.
- `z_if=0`은 physical Si surface가 아니라 raw y=0.300 um의 common anchor이므로, p-side SCR boundary가 약간 음수가 될 수 있다.
- 따라서 SCR crossing 검색은 `z_if=-0.300~+1.30 um`에서 수행한다.
- `SCR_E=1.0e5 V/cm`, junction 정의, VBD extraction physics는 변경하지 않았다.
- 현재 FINE-Lite mesh 결과는 calibration용이며 최종 freeze 결과가 아니다.
- implant/anneal parameter는 surrogate process parameter이며 실제 ST foundry recipe로 주장하지 않는다.


## Source integrity

이 디렉터리는 current SProcess/SNMesh/SDevice baseline implementation 원문을 보관한다. 과거 15.0 V SCR diagnostic SVisualPy는 15.6 V common-baseline 비교와의 혼용을 막기 위해 삭제했으며, 현재 SCR extractor의 authoritative copy는 `../spad-baseline-implementation-SCR/`의 V156 파일이다.

Git blob SHA:

```text
CMP_SPAD_BaselineImplementation_SProcess.txt   1bcef61e880ebcdb1b8b6af896222067953d7b1c
CMP_SPAD_BaselineImplementation_SNMesh1.txt    521b7df15dadb259b157b3f8c50c5c893069cd8a
CMP_SPAD_BaselineImplementation_SNMesh2.txt    face33ae20d1efc870baf6a462eebc6f10acf04d
CMP_SPAD_BaselineImplementation_SDevice.txt    9fc75e10aa88d212203c354b7fc49e02bb1cb67e
```

## Notes

- 이 디렉터리는 baseline implementation용 current working asset을 보존한다.
- 실제 ST manufacturing recipe 복원을 의미하지 않는다.
- SWB Parameter로 등록된 값은 sweep 여부와 관계없이 command에서 숫자로 hard-code하지 않는다.
- 현재 fixed parameter는 SWB experiment row에서 동일 값으로 유지한다.
- ATP / dark-current 분석용 별도 덱은 `../spad-baseline-atp-dark-validation/`에서 관리한다.
- 개인 날짜별 연구 기록은 `members/ryu980920/timeline/`에서 관리한다.
