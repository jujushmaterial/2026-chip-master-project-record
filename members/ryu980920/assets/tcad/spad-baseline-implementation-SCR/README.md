# V156 SCR Extraction Variant

이 문서는 baseline reconstruction 계산에서 사용하는 **공식 15.6 V SCR 추출용** SDevice / SVisualPy 덱을 설명한다. 과거 15.0 V SCR diagnostic은 current asset에서 제거했으며, SDE baseline과 SProcess candidate는 동일하게 15.6 V에서 비교한다.

## Files

```text
CMP_SPAD_BaselineImplementation_SDevice_V156SCR.txt
CMP_SPAD_BaselineImplementation_SVisualPy_V156SCR.txt
```

두 파일은 기존 baseline-calibration flow의 physics, breakdown definition, solver 방향을 새로 바꾸기 위한 코드가 아니다. 기존 계산 흐름을 유지한 상태에서 **VBD가 15.6 V 이상인 candidate에 대해 15.6 V static snapshot에서 SCR 위치를 직접 추출할 수 있도록 맞춘 보조 variant**이다.

## SDevice variant

`CMP_SPAD_BaselineImplementation_SDevice_V156SCR.txt`는 기존 baseline SDevice 조건을 유지한다.

- immediately upstream SMesh의 `n@node|-1@_msh.tdr` 사용
- `Avalanche(vanOverstraeten GradQuasiFermi)` 유지
- `AvalPostProcessing` 유지
- `BreakAtIonIntegral` 유지
- `ComputeIonizationIntegrals(direction="eGradQuasiFermi")` 유지
- 15.0 / 15.4 / **15.6** / 15.8 / 16.0 V 이상 snapshot 생성 조건 유지

이 variant의 목적은 15.6 V 이상까지 계산 가능한 candidate에서 `V156_des.tdr`이 생성되도록 하여, SVisualPy가 baseline과 같은 15.6 V 기준 SCR을 읽을 수 있게 하는 것이다.

## SVisualPy variant

`CMP_SPAD_BaselineImplementation_SVisualPy_V156SCR.txt`는 기존 15.0 V diagnostic extraction 대신 **15.6 V snapshot을 직접 사용**한다.

핵심 설정:

```text
EVAL_BIAS = 15.6
TDR_FILE  = n{SDevice node}_V156_des.tdr
```

현재 SProcess -> SMesh 좌표계를 그대로 사용한다.

```text
bulk-Si surface              raw y = 0.000 um
grating/Si interface anchor  raw y = 0.300 um
project common depth         z_if = raw_y - 0.300 um
```

SCR extraction은 center cutline에서 net-doping junction과 `|E| = 1.0e5 V/cm` crossing을 이용한다.

### 2026-09-15 SCR search-range correction

기존 V156 script는 junction과 electric-field crossing 검색의 lower bound를 `lo=0.0`으로 두고 있었다. 그러나 이 프로젝트의 좌표에서

```text
bulk-Si physical surface      z_if = -0.300 um
common anchor (raw y=0.300)   z_if =  0.000 um
```

이므로 `z_if=0`은 물리적 Si surface가 아니다. 실제 profile에서 p-side `|E|=1.0e5 V/cm` crossing이 `z_if<0`에 존재할 수 있고, 기존 `lo=0.0`은 이를 잘라내 `SCR_OK=0`을 만들 수 있었다.

수정 후:

```python
SCR_SEARCH_MIN_IF = -0.300
SCR_SEARCH_MAX_IF = 1.30
```

그리고 junction 및 SCR electric-field crossing 모두 `lo=SCR_SEARCH_MIN_IF`를 사용한다. 이는 raw coordinate 기준 `0.000~1.600 um`, 즉 bulk-Si physical surface부터의 검색이다.

**변경하지 않은 항목**
- evaluation bias = 15.6 V
- input snapshot = `V156_des.tdr`
- `SCR_E = 1.0e5 V/cm`
- net-doping zero crossing 기반 metallurgical junction 정의
- VBD ionization-integral extraction
- center/peripheral field 및 avalanche extraction

따라서 이번 수정은 SCR의 물리적 정의를 바꾼 것이 아니라, 기존 좌표계에서 유효한 p-side crossing을 누락하지 않도록 검색 범위를 바로잡은 것이다.

Workbench DOE에는 다음 SCR metric을 출력한다.

```text
VBD_V
SCR_p_nm
SCR_center_nm
SCR_n_nm
SCR_width_nm
Aval_peak_nm
Ecenter_kVpcm
Eperiph_kVpcm
R_E
SCR_OK
```

따라서 이 variant의 핵심 목적은 **15.6 V 이상 candidate의 SCR을 SDE baseline과 동일한 15.6 V 기준으로 직접 비교**하는 것이다. 15.0 V diagnostic SCR은 current workflow에서 사용하지 않으며 fallback으로도 사용하지 않는다.

## Important behavior

`BreakAtIonIntegral`을 사용하므로 candidate의 VBD가 15.6 V보다 낮아 V156 도달 전에 계산이 종료되면 `V156_des.tdr`이 생성되지 않을 수 있다. 이 경우 SVisualPy는 임의로 다른 bias의 SCR을 대신 사용하지 않고 SCR metric을 `NA`로 두며 `SCR_OK=0`으로 기록한다.

## Scope

이 두 파일은 baseline reconstruction refinement용이다. PEB, dark current, ATP, temperature robustness를 개선하기 위한 B-track 본 optimization용 physics 변경이 아니다. 특히 이번 수정은 process/physics 변경이 아니라 SVisualPy post-processing의 SCR search window correction이다.

## Source integrity

현재 authoritative pair는 아래 두 파일이다.

- SDevice V156SCR: 기존 physics / bias ramp / breakdown 설정 유지
- SVisualPy V156SCR: 2026-09-15에 SCR crossing search lower bound만 bulk-Si surface까지 확장

```text
CMP_SPAD_BaselineImplementation_SDevice_V156SCR.txt    b1f2680e10bf3390f4cb55639eca8069d664674a
CMP_SPAD_BaselineImplementation_SVisualPy_V156SCR.txt  fa0dfebdc2b80cdcf529efebcbb74daf7e567ead
```

과거 15.0 V diagnostic SVisualPy는 current asset에서 삭제했으며, 공식 SCR comparison에는 사용하지 않는다.
