# CES 2026 VL53L9 계열 자료의 CMP SPAD 공동 dToF 연구 활용 보고서

**문서 목적:** CES 2026에서 소개된 STMicroelectronics VL53L9 계열과, 후속 공식 자료인 `VL53L9CX Datasheet (DS14879 Rev.7)` 및 `STEVAL-VL53L9 Data Brief (DB5805 Rev.2)`를 CMP 28 nm FD-SOI SPAD 공동연구에서 어떻게 사용할지 정리한다.  
**문서 성격:** 공용 참고자료 / system-level benchmark 사용 원칙  
**기준 연구:** `shared/decisions/SPAD_연구계획서.md`  
**작성 기준일:** 2026-08-28

---

# 1. 결론

이번에 확보한 두 ST 공식 자료는 모두 CMP 공동연구에 사용할 가치가 있다. 다만 역할이 다르다.

1. **CES 2026 VL53L9 소개**
   - 연구의 **산업적 출발점**으로 사용한다.
   - 고해상도 SPAD 기반 dToF LiDAR가 실제 제품에서 요구하는 장거리, 낮은 반사율 대응, 강한 주변광 대응, 고해상도 zone 등의 필요성을 보여준다.
   - 우리 SPAD의 절대 성능 기준이나 구조 복제 근거로 사용하지 않는다.

2. **VL53L9CX Datasheet — DS14879 Rev.7**
   - 세 자료 중 **Python dToF 최종평가에 가장 유용한 정량 자료**이다.
   - target reflectance, ambient irradiance, exposure time, detection-rate 정의, maximum range, accuracy, temporal precision 등의 공개 characterization을 제공한다.
   - 우리 모델의 `system scenario anchor` 및 `external validation envelope`로 사용한다.

3. **STEVAL-VL53L9 Data Brief — DB5805 Rev.2**
   - CES에서 소개된 VL53L9 계열이 실제 개발용 evaluation board와 연결되어 있음을 보여주는 **제품 구현·개발 환경 근거**로 사용한다.
   - 회로도, 전원 rail, MIPI/I3C interface, oscillator, EEPROM, level shifter 등의 실제 evaluation hardware 구성을 확인할 수 있다.
   - 그러나 photon budget이나 SPAD 검출성능을 직접 정하는 데이터는 DS14879보다 적다.

따라서 최종 연구 스토리는 다음과 같이 정리한다.

```text
CES 2026
산업적 dToF 요구 확인
        ↓
VL53L9CX Datasheet
공개된 실제 system-level test condition / performance 확인
        ↓
STEVAL-VL53L9
실제 evaluation hardware 구현 및 개발 가능성 확인
        ↓
28 nm FD-SOI SPAD 문헌 계열
소자 수준 optical/electrical 개선 근거
        ↓
A: G 개선 / B: ATP·dark·PEB 개선
        ↓
G × ATP integration
        ↓
Python 940 nm dToF
Baseline / A / B / A+B 상대 비교
```

---

# 2. 기존 CMP 연구 방향과의 정합성

현재 CMP SPAD 공동연구의 최종 목적은 VL53L9 내부 SPAD를 복제하는 것이 아니다.

공통 surrogate baseline에서:

- A는 940 nm에서 concentric annular Si/STI optical structure를 통해 photogeneration `G`를 개선한다.
- B는 DNW/PW/thermal profile engineering을 통해 SCR 위치를 유지하면서 PEB, dark-generation, ATP, temperature robustness를 개선한다.
- 마지막에는 `G × ATP` 공간적 곱·적분을 통해 detector-level effective detection quantity를 구성한다.
- 이후 동일한 Python dToF 시스템 조건에서 Baseline / A-only / B-only / A+B를 비교한다.

현재 연구계획서의 핵심 질문은 다음과 같다.

> 같은 940 nm 송수신 시스템에서 detector만 baseline/A/B/A+B로 바꿨을 때 최대 측정거리와 거리 RMSE가 얼마나 바뀌는가?

이번 ST 공식 자료는 이 구조를 변경하지 않는다. 오히려 **Python 단계의 system scenario를 실제 상용 dToF 제품의 공개 characterization과 연결할 수 있게 해준다.**

---

# 3. CES 2026 VL53L9의 역할

CES 2026에서 ST VL53L9 Time-of-Flight sensor는 고해상도 direct-ToF 3D LiDAR 제품 사례로 제시되었다.

프로젝트에서 CES 자료를 사용하는 목적은 다음과 같다.

- SPAD 기반 dToF가 실제 산업에서 사용되고 있음을 보여준다.
- 최대 약 2.3k distance zones의 고해상도 sensing 요구를 보여준다.
- 장거리 ranging, edge/object detection, 2D IR + depth map, on-chip processing과 같은 산업적 요구를 연구 배경으로 연결한다.
- 940 nm NIR 환경에서 SPAD의 유효 검출성능을 개선할 필요성을 설명하는 product-level motivation으로 사용한다.

## CES 자료에서 하지 않을 것

- CES가 DCR, pile-up, afterpulsing을 공식적으로 하나의 병목 목록으로 발표했다고 주장하지 않는다.
- CES 5 cm~10 m 소개 수치를 우리 detector 성능 target으로 사용하지 않는다.
- VL53L9 내부 SPAD가 Gao 2024 28 nm FD-SOI SPAD와 동일하다고 주장하지 않는다.
- VL53L9의 내부 process, doping, SPAD geometry를 역추정하여 baseline으로 사용하지 않는다.

---

# 4. VL53L9CX Datasheet의 핵심 가치

문서:

- STMicroelectronics
- `VL53L9CX`
- `DS14879`
- Rev.7
- 2026-07-10 revision history 기준

이 문서는 CMP의 **system-level quantitative benchmark**로 가장 유용하다.

---

# 5. VL53L9CX에서 공개된 주요 시스템 정보

VL53L9CX는 다음 구성요소가 하나의 dToF 3D LiDAR module 안에 통합된 것으로 설명된다.

- SPAD array
- post-processing SoC
- two VCSELs
- dedicated VCSEL driver
- physical IR filters
- metasurface optical elements
- receiver lens
- embedded PMIC

공식 설명에서는:

- 최대 54 × 42 zones
- 최대 2.3k zones
- 최대 100 Hz processed output
- wide FoV
- strong ambient light 대응
- BSI stacked direct-ToF technology

를 제시한다.

이 정보는 **우리 연구가 단일 SPAD 수준에서 시작하지만 최종적으로 dToF system performance와 연결해야 하는 이유**를 뒷받침한다.

---

# 6. dToF Python 모델에 직접 활용 가치가 큰 공개 시험조건

VL53L9CX datasheet는 ranging characterization에 사용한 조건을 공개한다.

## 6.1 Target reflectance

공식 시험 target:

| Target | Visible reflectance | Infrared reflectance |
|---|---:|---:|
| Gray 17% | 17% | **12%** |
| Light gray 62% | 62% | **58%** |

우리 연구는 940 nm이므로 Python dToF에서 사용할 때에는 visible reflectance가 아니라 **IR reflectance 12% / 58%**를 기준으로 해석하는 것이 적절하다.

### 프로젝트 사용 방식

이 값은 ST 내부 SPAD 특성값이 아니다.  
우리 Python 최종평가에서는 다음처럼 사용할 수 있다.

- low-reflectance case: `rho = 0.12`
- high-reflectance case: `rho = 0.58`

**프로젝트 라벨:** `[system scenario assumption]`  
단, 숫자 자체의 출처는 ST 공식 characterization condition이다.

## 6.2 Ambient illumination

ST characterization에는 다음 ambient 조건이 사용된다.

- dark: `0 W/m²`
- outdoor cloudy equivalent: `1.25 W/m²`
- outdoor sunny equivalent: `10 W/m²`

또한 문서에서는 각각 5 klx와 40 klx equivalent daylight 조건을 함께 설명한다.

### 프로젝트 사용 방식

우리 Python dToF에서 ambient stress를 최소 세 단계로 구성할 수 있다.

```text
Ambient-0 : 0 W/m²
Ambient-1 : 1.25 W/m²
Ambient-2 : 10 W/m²
```

이렇게 하면 A/B/A+B detector case가 낮은 반사율 및 높은 background 조건에서 얼마나 버티는지를 같은 환경에서 비교할 수 있다.

---

# 7. Maximum range의 정의

ST는 maximum range capability를 단순히 “신호가 마지막으로 보이는 거리”로 정의하지 않는다.

공식 datasheet에서는 **99% detection rate**를 기준으로 maximum range를 설명한다.

예를 들어 1000번 측정했을 때:

- 990개 valid distance
- 나머지 10개는 specification 외 값이거나 invalid target status

인 수준을 99% detection-rate 예시로 설명한다.

이 정의는 우리 연구에 매우 유용하다.

현재 연구계획서에는 maximum measurable range를 예를 들어:

- detection probability threshold
- RMSE threshold
- false-alarm threshold

을 동시에 만족하는 최대 거리로 정의하도록 되어 있다.

따라서 기존 provisional `Pdet ≥ 95%` 예시보다, **ST 공개 characterization과 비교 가능한 supplementary criterion으로 `Pdet ≥ 99%`를 추가하는 것이 합리적**이다.

단, 이것은 연구계획의 detector comparison 원칙을 바꾸는 것이 아니라 **system-level reporting criterion을 추가하는 것**이다.

추천:

```text
Primary:
Rmax,95 = max R satisfying Pdet >= 0.95 and other project criteria

ST-inspired supplementary:
Rmax,99 = max R satisfying Pdet >= 0.99 and same RMSE/FAR criteria
```

이렇게 두 값을 동시에 기록하면 threshold 선택에 따른 결과 의존성도 보여줄 수 있다.

---

# 8. 공개 maximum range 데이터

## 8.1 Precision mode 54×42

| IR reflectance | Indoor 0 W/m² | Outdoor cloudy 1.25 W/m² |
|---|---:|---:|
| 12% | 8.8 m | 8.0 m |
| 58% | 8.8 m | 8.8 m |

## 8.2 Ambient mode 54×42

| IR reflectance | Indoor 0 W/m² | Outdoor sunny 10 W/m² |
|---|---:|---:|
| 12% | 8.5 m | 6.0 m |
| 58% | 8.5 m | 7.0 m |

## 8.3 Precision mode 24×20

| IR reflectance | Indoor 0 W/m² | Outdoor cloudy 1.25 W/m² |
|---|---:|---:|
| 12% | 8.8 m | 8.8 m |
| 58% | 8.8 m | 8.8 m |

## 8.4 Ambient mode 24×20

| IR reflectance | Indoor 0 W/m² | Outdoor sunny 10 W/m² |
|---|---:|---:|
| 12% | 8.5 m | 7.5 m |
| 58% | 8.5 m | 7.6 m |

---

# 9. Maximum range 데이터를 우리 연구에서 해석하는 방법

이 값들은 우리 결과와 직접 경쟁시키면 안 된다.

잘못된 표현:

> 우리 SPAD가 VL53L9보다 1.2 m 더 멀리 측정한다.

> baseline을 8.8 m가 나오도록 photon budget을 맞췄다.

> A+B 구조가 VL53L9의 maximum range를 개선했다.

올바른 사용:

> ST의 공개 characterization에서는 target IR reflectance와 ambient irradiance가 악화될수록 maximum valid range가 감소한다. 본 연구에서는 이러한 공개 환경 조건을 system-level stress scenario로 채택하고, 동일한 가상 송수신 시스템에서 Baseline/A/B/A+B detector의 상대적 성능 변화를 평가한다.

즉 VL53L9CX 값은 **external product performance envelope**이다.

우리 연구 결과는 다음으로 제한한다.

```text
Baseline vs A
Baseline vs B
Baseline vs A+B
```

그리고 상대 improvement만 주장한다.

---

# 10. Accuracy와 RMSE를 동일시하지 않는다

VL53L9CX datasheet는 `accuracy`를 ground truth 대비 error로 정의한다.

예를 들어 precision mode 54×42에서 공개된 long-range accuracy 수준은 target/ambient 조건에 따라 sub-percent 범위로 제시된다.

그러나 이것을 우리 Monte Carlo의 `RMSE`와 동일한 지표라고 부르면 안 된다.

우리 최종 metric:

\[
RMSE_R =
\sqrt{
\frac{1}{N}
\sum_i
(\hat R_i-R_{true})^2
}
\]

ST datasheet의 accuracy와 정의가 다르다.

따라서 최종 발표에서는:

```text
Our result:
- RMSE vs distance
- Rmax
- Pdet vs distance

ST external reference:
- published accuracy
- published temporal precision
- published maximum range
```

로 구분한다.

---

# 11. Precision / temporal noise와 RMSE를 동일시하지 않는다

VL53L9CX datasheet는 precision을 temporal noise로 정의한다.

즉 여러 frame의 depth value에 대한 시간축 standard deviation 성격이다.

예를 들어 precision mode 54×42의 공개 characterization에서는 short-range absolute temporal noise와 long-range relative precision이 각각 제시된다.

이 역시 우리 RMSE와 다른 지표이다.

### 연구에서의 사용

- ST precision → 상용 제품의 temporal stability 참고값
- Our RMSE → 동일 Monte Carlo scenario에서 detector case 간 직접 비교 metric

서로 같은 축에서 하나의 수치처럼 비교하지 않는다.

---

# 12. Resolution과 binning 정보의 의미

VL53L9CX는 resolution에 따라 여러 output mode를 제공한다.

- 54 × 42
- 24 × 20
- 18 × 14
- 12 × 10
- 8 × 6
- 4 × 4

datasheet에서는 zone이 macro-SPAD 단위로 결합되고, Dynamic SPAD Selection(DSS)이 signal rate를 관리하는 것으로 설명한다.

이 정보는 **상용 dToF에서 detector-level event를 그대로 사용하는 것이 아니라 spatial aggregation과 firmware-level control이 함께 동작한다는 점**을 보여준다.

### 중요한 한계

54×42와 24×20에서 maximum range가 다르더라도 이를 단순히:

> binning만 바꾸면 range가 증가했다.

라고 해석하지 않는다.

각 profile은 exposure, power mode, ranging mode 등 다른 설정도 함께 변할 수 있으므로 여러 system variable이 동시에 작용한다.

우리 연구에서는 resolution/binning을 직접 변수로 추가하지 않고, **detector case 비교의 공정성을 위해 동일한 system configuration을 유지한다.**

---

# 13. STEVAL-VL53L9 Data Brief의 역할

문서:

- STMicroelectronics
- `STEVAL-VL53L9`
- `DB5805`
- Rev.2
- April 2026

이 문서는 evaluation board based on VL53L9CX Time-of-Flight sensor를 설명한다.

첫 페이지에서:

- VL53L9CX 기반 evaluation board
- 2.3 K zones
- MIPI / I3C
- STM32 / Raspberry Pi / Rockchip 호환
- 71° diagonal FoV
- 55 × 42° FoV
- 1° angular resolution
- 5 cm ~ 9 m ranging

을 제시한다.

## 이 자료의 가장 큰 가치

CES에서 소개된 제품 개념이 실제 developer-accessible hardware로 이어진다는 점을 보여준다.

즉:

```text
CES product concept
    ↓
VL53L9CX commercial module
    ↓
STEVAL-VL53L9 evaluation board
    ↓
real system integration / development
```

이라는 연결이 가능하다.

이는 CMP 발표에서 **산업적 relevance**를 설명할 때 강한 보조 근거가 된다.

---

# 14. STEVAL 회로도에서 확인할 수 있는 것

DB5805에는 다음 board-level implementation이 공개된다.

- VL53L9CX sensor
- MIPI data path
- I3C/I2C connection
- XSHUT
- SYNC_IN
- interrupt
- application clock
- level shifters
- 12 MHz oscillator
- EEPROM
- separate power rails

공개 board rail:

- `VBAT_LDD = 3.3 V`
- `VBAT_RX = 3.3 V`
- `AVDD = 2.8 V`
- `DVDD = 1.2 V`
- `IOVDD = 1.8 V`

이 정보는 evaluation hardware의 실제 전원/인터페이스 구현을 보여준다.

---

# 15. STEVAL 전원값을 photon budget에 사용하면 안 되는 이유

`VBAT_LDD`, `VBAT_RX`, `AVDD` 등은 **전기적 supply rail**이다.

이를 다음처럼 사용하면 안 된다.

```text
3.3 V × current = laser optical power
```

또는

```text
VBAT_LDD = VCSEL pulse energy
```

공식 자료에서 optical wall-plug efficiency, pulse waveform, per-pulse optical energy 등이 충분히 공개되지 않았기 때문이다.

따라서 board-level supply 값을 dToF optical photon budget으로 변환하지 않는다.

---

# 16. 9 m와 8.8 m의 관계

STEVAL data brief는 제품 설명에서 `5 cm to 9 m` ranging이라고 요약한다.

VL53L9CX detailed datasheet에서는 profile에 따라:

- Precision mode: below 5 cm to 8.8 m
- Ambient mode: 45 cm to 8.5 m

등의 상세 characterization이 제시된다.

이를 서로 충돌하는 값으로 처리할 필요는 없다.

권장 해석:

> STEVAL data brief의 9 m는 evaluation board/product-level rounded description이고, DS14879의 8.8 m/8.5 m 등은 특정 ranging mode와 test condition이 붙은 상세 characterization 값이다.

최종 정량 reference에서는 항상 **상세 조건이 공개된 DS14879 값에 우선순위**를 둔다.

---

# 17. 세 자료의 최종 역할 분담

| Source | Primary role | Quantitative importance |
|---|---|---:|
| CES 2026 VL53L9 | 산업적 배경 / motivation | 낮음 |
| VL53L9CX DS14879 | system scenario / benchmark / external validation | 매우 높음 |
| STEVAL-VL53L9 DB5805 | hardware implementation / evaluation environment | 중간 |
| Gao et al. FD-SOI SPAD papers | device/TCAD scientific basis | 매우 높음 |

---

# 18. 추천 Python dToF scenario

## Scenario S0 — Indoor, low reflectance

```yaml
wavelength_nm: 940
target_ir_reflectance: 0.12
ambient_irradiance_W_m2: 0
integration_reference_ms: 4
```

## Scenario S1 — Outdoor cloudy, low reflectance

```yaml
wavelength_nm: 940
target_ir_reflectance: 0.12
ambient_irradiance_W_m2: 1.25
integration_reference_ms: 10
```

## Scenario S2 — Outdoor sunny, low reflectance

```yaml
wavelength_nm: 940
target_ir_reflectance: 0.12
ambient_irradiance_W_m2: 10
integration_reference_ms: 16
```

각 scenario에서 high-reflectance counterpart를 추가한다.

```yaml
target_ir_reflectance: 0.58
```

따라서 최소 6개 standard stress condition을 구성할 수 있다.

### 주의

ST profile의 exposure를 그대로 사용하면 profile-specific system behavior가 섞일 수 있다.

최종 A/B/A+B detector fairness를 위해서는:

- scenario별로 exposure를 정한 뒤
- 그 scenario 안에서는 모든 detector case에 동일하게 적용한다.

---

# 19. Python 모델에서 여전히 별도 가정이 필요한 항목

ST 공식 자료만으로 아래 값은 충분히 확정할 수 없다.

- VCSEL pulse energy
- optical pulse width
- pulse repetition frequency의 상세 설정
- receiver effective aperture
- receiver optical transmission
- actual internal SPAD PDP at 940 nm
- actual internal DCR
- internal SPAD active area / count details required for our exact model
- TDC bin width
- laser timing jitter
- SPAD timing jitter
- exact histogram estimator internals
- proprietary DSS behavior
- proprietary post-processing pipeline

따라서 이 값들은 억지로 VL53L9에서 역산하지 않는다.

필요하면 명시적으로:

`[system scenario assumption]`

으로 둔다.

---

# 20. 우리 detector 결과를 system model에 전달하는 방식

A/B 연구에서 최종적으로 필요한 detector input은 다음과 같다.

## Baseline

\[
Q_0 = \iiint G_0(\mathbf r)\,ATP_0(\mathbf r)\,dV
\]

## A-only

\[
Q_A = \iiint G_A(\mathbf r)\,ATP_0(\mathbf r)\,dV
\]

## B-only

\[
Q_B = \iiint G_0(\mathbf r)\,ATP_B(\mathbf r)\,dV
\]

## A+B

\[
Q_{AB} = \iiint G_A(\mathbf r)\,ATP_B(\mathbf r)\,dV
\]

필요할 경우 carrier collection probability를 추가한다.

\[
Q = \iiint G\cdot P_{\text{collection}}\cdot ATP\,dV
\]

이 값을 baseline normalization하여 relative PDP/effective detection factor로 Python dToF에 전달한다.

---

# 21. Dark-noise 입력

B 연구에서 absolute DCR calibration이 충분하지 않다면 TCAD dark current를 절대 DCR로 부르지 않는다.

다음과 같이 사용한다.

\[
k_B =
\frac{DCR_{\mathrm{proxy},B}}
{DCR_{\mathrm{proxy},0}}
\]

그리고 Python system scenario에서 baseline DCR을 별도 assumption 또는 literature reference로 둔다.

\[
DCR_B = k_B DCR_0
\]

이렇게 하면 ST 내부 DCR을 역산하거나 우리 TCAD dark current를 절대 DCR로 과장하지 않고 B의 상대적 개선효과만 반영할 수 있다.

---

# 22. 최종 출력

각 scenario에서:

1. Baseline
2. A-only
3. B-only
4. A+B

를 동일 조건으로 비교한다.

최종 graph:

- `Detection probability vs distance`
- `Range RMSE vs distance`
- `Signal/background expected count vs distance`
- `Maximum measurable range`
- optional `Rmax @ Pdet 95%`
- optional `Rmax @ Pdet 99%`

summary table:

| Case | Relative detection quantity | Relative dark factor | Rmax | ΔRmax vs baseline | RMSE | ΔRMSE |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 1.0 | 1.0 |  | 0 |  | 0 |
| A-only |  | 1.0 |  |  |  |  |
| B-only |  |  |  |  |  |  |
| A+B |  |  |  |  |  |  |

---

# 23. VL53L9 데이터와 우리 결과를 함께 보여주는 방법

추천 발표 구성:

## Figure A — Our detector comparison

```text
Pdet vs distance
Baseline / A / B / A+B
```

## Figure B — Our RMSE

```text
RMSE vs distance
Baseline / A / B / A+B
```

## Table C — ST published external envelope

```text
VL53L9CX:
reflectance
ambient condition
published maximum range
published accuracy
published temporal precision
```

이 세 가지를 분리한다.

VL53L9 line을 우리 graph의 다섯 번째 detector curve로 넣지 않는다.

---

# 24. 연구 발표에서 사용할 수 있는 연결 문장

> CES 2026에서 소개된 ST VL53L9은 다수의 distance zone과 장거리·주변광 대응이 요구되는 SPAD 기반 direct-ToF 3D LiDAR의 산업적 사례이다. 후속 VL53L9CX 공식 datasheet는 낮은 IR reflectance와 높은 ambient irradiance에서 maximum valid range가 감소하는 실제 system-level characterization을 공개한다. 본 연구는 VL53L9 내부 detector를 복제하지 않고, 공개된 28 nm FD-SOI SPAD 연구계열을 기반으로 광학적 photogeneration과 전기적 avalanche/dark 특성을 각각 개선한 뒤 동일한 940 nm 가상 dToF 시스템에서 baseline 대비 상대적 range 및 RMSE 개선을 평가한다.

---

# 25. 금지 주장

다음 표현은 사용하지 않는다.

- “우리 SPAD는 VL53L9보다 성능이 좋다.”
- “우리 구조가 VL53L9의 8.8 m를 10 m로 개선한다.”
- “VL53L9 내부 SPAD는 Gao 2024 구조이다.”
- “STEVAL의 3.3 V supply가 VCSEL optical power이다.”
- “ST의 accuracy가 우리 RMSE와 동일하다.”
- “ST의 temporal precision이 우리 RMSE와 동일하다.”
- “24×20이 54×42보다 range가 좋은 이유는 오직 binning 때문이다.”
- “CES가 DCR/pile-up/afterpulsing을 공식 병목으로 발표했다.”
- “ST datasheet에서 공개되지 않은 TDC/PDP/DCR/pulse energy를 역산해 실제 내부값이라고 주장한다.”

---

# 26. Source / provenance 관리

## Source A — CES 2026

- 자료: CES Innovation Awards 2026, ST VL53L9 Time-of-Flight sensor
- 역할: 산업적 motivation
- baseline numerical calibration: 사용 금지

## Source B — VL53L9CX Datasheet

- 기관: STMicroelectronics
- 문서: `DS14879`
- revision: Rev.7
- 역할:
  - official test condition
  - maximum range
  - accuracy
  - temporal precision
  - resolution/profile
  - system architecture
- 프로젝트 사용:
  - scenario anchor
  - external validation envelope

## Source C — STEVAL-VL53L9 Data Brief

- 기관: STMicroelectronics
- 문서: `DB5805`
- revision: Rev.2
- date: April 2026
- 역할:
  - evaluation-board implementation
  - real interface/power architecture
  - product-development bridge
- photon-budget source: 사용하지 않음

## Source D — FD-SOI SPAD literature

- Gao / Issartel / Chaves de Albuquerque / Vignetti 연구계열
- 역할:
  - device baseline
  - optical G
  - ATP
  - DCR/dark mechanism
  - STI influence
  - PW/DNW junction
  - 28 nm FD-SOI SPAD scientific basis

---

# 27. 연구 방향 변경 여부

**변경 없음.**

이번 자료는 기존 연구 방향과 충돌하지 않는다.

오히려 아래 부분을 강화한다.

- CES → 산업적 필요
- ST official datasheet → system-level scenario
- STEVAL → 실제 개발 hardware
- academic FD-SOI SPAD → device-level scientific basis
- TCAD → detector improvement
- Python → system-level relative impact

공통 surrogate baseline, A/B 독립성, 3D `G × ATP`, 동일 system condition, VL53L9 절대성능과의 직접 경쟁 금지 원칙은 그대로 유지한다.

---

# 28. 향후 반영 권장사항

1. `VL53L9CX DS14879`을 공용 reference로 유지한다.
2. `STEVAL-VL53L9 DB5805`를 공용 product/hardware reference로 유지한다.
3. Python dToF parameter file을 별도로 생성한다.
4. 각 parameter마다 출처 라벨을 둔다.
5. 공개되지 않은 값은 `[system scenario assumption]`으로 분리한다.
6. `Pdet >= 99%`를 ST-inspired supplementary maximum-range criterion으로 검토한다.
7. 최종 발표에서는 ST published performance와 our simulated relative comparison을 별도 표/그래프로 분리한다.
8. 실제 model parameter가 정해질 때마다 본 문서가 아니라 별도 `dtof_system_scenario` 문서/파일에서 versioning한다.

---

# 29. 한 줄 정리

> **CES 2026 VL53L9은 연구의 산업적 출발점, VL53L9CX DS14879는 Python dToF의 공개 system-condition/benchmark 근거, STEVAL-VL53L9 DB5805는 실제 evaluation hardware 구현 근거로 사용하며, 실제 detector 연구와 개선 주장은 Gao 계열 28 nm FD-SOI surrogate SPAD 및 우리 TCAD 결과에 한정한다.**
