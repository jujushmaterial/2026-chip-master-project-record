# V156 SCR Extraction Variant

이 문서는 baseline reconstruction 계산에서 사용하는 15.6 V SCR 추출용 SDevice / SVisualPy 변형 덱을 설명한다.

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

SCR extraction은 기존과 동일하게 center cutline에서 net-doping junction과 `|E| = 1.0e5 V/cm` crossing을 이용한다.

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

따라서 이 variant의 핵심 목적은 **15.6 V 이상 candidate의 SCR을 15.6 V 기준으로 직접 비교**하는 것이다. 기존 V150 diagnostic result를 15.6 V baseline SCR과 혼용하지 않는다.

## Important behavior

`BreakAtIonIntegral`을 사용하므로 candidate의 VBD가 15.6 V보다 낮아 V156 도달 전에 계산이 종료되면 `V156_des.tdr`이 생성되지 않을 수 있다. 이 경우 SVisualPy는 임의로 다른 bias의 SCR을 대신 사용하지 않고 SCR metric을 `NA`로 두며 `SCR_OK=0`으로 기록한다.

## Scope

이 두 파일은 baseline reconstruction refinement용이다. PEB, dark current, ATP, temperature robustness를 개선하기 위한 B-track 본 optimization용 physics 변경이 아니다.

## Source integrity

업로드된 두 코드는 2026-09-02 대화에서 사용자가 실행에 사용할 수 있도록 정리한 주석 제거 실행 원문을 그대로 등록했다.

```text
CMP_SPAD_BaselineImplementation_SDevice_V156SCR.txt    b1f2680e10bf3390f4cb55639eca8069d664674a
CMP_SPAD_BaselineImplementation_SVisualPy_V156SCR.txt  bf889e336beeb0d659579c99076b3f0cce921729
```
