# H3 — STI5 계면 트랩 밀도 감소에 따른 Dark Current 민감도 실험

> 상태 (2026-11-16): 계획·코드 작성 단계. **Sentaurus T-2022.03에서 실행/수렴, mesh 영역 매칭, 물리적 개선 여부는 미검증**. 원본 SDE와 기존 진단/암전류 덱은 수정하지 않음.

## 1. H3 연구 질문

28 nm FD-SOI SPAD에서 `Bulk/R.STI5` Si/SiO₂ 계면의 전기적으로 활성인 트랩을 줄이면, 소자 구조와 도핑을 바꾸지 않고도 역바이어스 Dark Current가 감소하는가?

- H1: DNW 깊이/농도 변화로 ATP 개선
- H2: Trim DNW Mask 끝 반경 변화로 PEB/전계 개선
- **H3: STI5 계면의 활성 트랩 면밀도 `STI5_NIT` 변화로 Dark Current 개선 여부 검증**
- H3는 **수소의 실제 확산·반응·결합률을 시뮬레이션하지 않음**. `N_it` 감소는 패시베이션 후 상태에 대한 surrogate proxy.

## 2. 근거와 입력의 성격

- Suliman et al., *Solid-State Electronics* 46 (2002), 837–845, DOI https://doi.org/10.1016/S0038-1101(01)00344-6 : U-shaped trench Si/SiO₂ 계면의 **midgap `D_it ≈ 1e11 cm^-2 eV^-1` [직접 실측]**.
- `D_it`(에너지별 밀도)와 SDevice `Level`의 `N_it`(총 면밀도)은 단위가 다름. `N_it=1e11 cm^-2`는 문헌을 **직접 적분·변환해 얻은 값이 아닌 [surrogate assumption]**.
- Kwon et al., *IEEE Trans. Electron Devices* 51 (2004), 1346–1349, DOI https://doi.org/10.1109/TED.2004.832714 : **D₂** annealing의 STI sidewall trap passivation 및 CMOS APS dark-current 감소 실측. H₂/FD-SOI SPAD 동일 조건의 직접 증거는 아님.
- Tsetseris & Pantelides, *Phys. Rev. B* 70 (2004) 245320, DOI https://doi.org/10.1103/PhysRevB.70.245320 : Si/SiO₂ 계면 `P_b` center에 대한 H₂ 패시베이션 반응의 이론적 근거.

## 3. SWB 실험 입력 (3조건)

| Case | `STI5_NIT` [cm^-2] | 의미 |
|---|---:|---|
| H3-0 | 0 | STI5 명시적 트랩이 비활성인 검증 대조군 (원본 trap-free deck과 일치 여부 확인) |
| H3-1 | 1e11 | 초기 활성 트랩 기준 [surrogate assumption] |
| H3-2 | 5e10 | 활성 트랩 50% 감소 [surrogate assumption] |

추가 **SWB Parameter** 및 모든 행의 입력:

| Parameter | H3-0 | H3-1 | H3-2 | 단위 |
|---|---:|---:|---:|---|
| `STI5_NIT` | 0 | 1e11 | 5e10 | cm^-2 |
| `STI5_ET` | 0 | 0 | 0 | eV, fromMidBandGap |
| `STI5_SIGMA_N` | 1e-15 | 1e-15 | 1e-15 | cm² |
| `STI5_SIGMA_P` | 1e-15 | 1e-15 | 1e-15 | cm² |

`STI5_ET`와 두 capture cross-section은 **미보정 [surrogate assumption]**으로 고정한다. 네 값 모두 **SDevice/SVisualPy 내에서 `@PARAMETER@` 참조**이고, 숫자는 SWB 실험 행에만 입력한다.

기존에 SWB 등록한 `PW_Dose`, `DNW_Dose`, `MeshScale` 및 연구 공정 파라미터를 코드에서 수치로 바꾸지 않는다.

## 4. 기준 소자와 SWB 연결

- SDE 소스: `members/jujushmaterial/assets/tcad/spad-baseline-static-freeze/SDE_reference_baseline_v1.3_redarea_uniform_meshconv.txt`.
- SDE 전기 출력: **우측 반경 단면 `n@node@_msh.tdr`**, SDevice `Math { Cylindrical }`; 전체 평면 반사 mesh `_full_reference_msh.tdr`가 아님.
- SDE의 STI5: `R.STI5` (Oxide), 벌크: `Bulk` (Silicon); SDE surrogate 치수상 STI5 반경 12.2–12.8 µm.
- 생성 TDR의 **실제 region 이름과 `Bulk/R.STI5` 계면이 존재하는지** SVisual에서 필수 확인.
- 기존 공통 VBD 진단 덱 (별도 SDevice 노드) + **H3_SDevice_DarkCurrent.cmd** (feedback ON) + 바로 다음 **H3_SVisualPy_DarkCurrent.py**.
- Python script는 upstream Dark SDevice `@node|-1@`을 사용하고, `@node|sdevice@`가 **기존 ionization-integral VBD 진단 노드**를 가리키는 원본 SWB 배치를 전제한다. 분기/재배치 시 이 참조를 확인할 것.
- H3의 `#setdep @node|sde@`, `Grid="n@node|sde@_msh.tdr"` 유지.
- **주의:** 진단 VBD는 trap-free 공통 SDE 기준값이며, H3 trap 추가 후의 VBD를 새롭게 계산한 값이 아님. H3 전계/항복 변화를 확증하려면 별도 trap-aware 진단/공간분포 검토가 필요.

## 5. H3가 변경한 물리 모델

- 기존 벌크 SRH(DopingDependence TempDependence Tunneling(Hurkx)), Auger, BTBT(Hurkx), avalanche(vanOverstraeten Eparallel), mobility 및 contact·bias·feedback ON 유지.
- **추가:** `Physics (RegionInterface="Bulk/R.STI5"){ Traps(Acceptor Level ... Conc=@STI5_NIT@ ...) }`.
- `SurfaceSRH`는 동시에 켜지 않음: 동일 계면 결함 생성·재결합을 이중 보정할 위험을 회피.
- `Traps`는 포획/방출 및 점유·트랩 전하 영향을 계산하지만, 별도 interface TAT/Hurkx 물리 모델이나 수소 확산 모델을 자동으로 추가하지 않는다.
- `Plot`에 명시적 계면 trap 진단장을 추가.
- `CurrentPlot`에 STI5 계면에서의 `eGapStatesRecombination`·`hGapStatesRecombination` 적분 추가.

## 6. 후처리 및 비교

- **공통 절대 역바이어스 14.0 V** [surrogate evaluation assumption]: 기존 SDevice 0→14 V ramp 내에서 `|I_anode|` 비교. H3 code에서 이 값은 **분석 상수**로 두며 SWB 공정 파라미터가 아니다.
- `H3_ICommon_A`: 14.0 V의 `|I_anode|` (단위 A), `H3_Common_OK`: 해당 전압에서 terminal I–V 및 STI5 진단 데이터 확보 여부.
- `H3_eGapCommon_native`, `H3_hGapCommon_native`: STI5 계면 전자/정공 trap의 **부호 있는 계면 적분값**, **단위/원통가중치 실행 검증 전 전류(A) 환산 금지**.
- 기존 `I50/I90/I156`, global SRH/BTBT/avalanche 생성 proxy, KCL 확인과 plots 보존. 기존 퍼센트는 세 **전역 bulk generation proxy 내부 구성비**일 뿐 STI5 생성량이나 terminal current 기여율이 아님.
- `H3_ICommon_A`가 모두 유효하면 `100 × [I(H3-1)-I(H3-2)] / I(H3-1)`로 상대 감소율 계산. **H3-0 대비 감소율이 아님**.
- 14.0 V가 실제 각 조건의 항복 아래인지, avalanche onset 및 trap charge 영향이 없는지는 별도 검증. `Dark_OK`를 H3 개선 판정으로 사용하지 않음.
- Trap 밀도가 감소해도 dark-current가 단조 감소하지 않을 수 있음; 계면 trap charge에 의한 field/BTBT/avalanche 변경을 함께 진단해야 함.

## 7. 실행 및 정적 확인 순서

1. **기존 SDE R0**의 region 이름과 우측 mesh 선택을 확인한 뒤 동일 SDE·MeshScale 사용.
2. 4개 H3 SWB 파라미터 등록; 고정값도 row 입력. 기존 SDE 입력 PW_Dose/DNW_Dose/MeshScale은 동일 experiment 값 유지.
3. H3-0 → H3-1 → H3-2 순서로 검증. H3-0에서 `Conc=0`에 따른 엔진 경고/미지원 발생 시, 별도 원본 trap-free SDevice/SVisualPy로 대조하고 README에 차이를 기록.
4. 전처리된 `pp*_des.cmd`에서 `@...@` 미치환 여부 및 `Bulk/R.STI5` 매칭 검사.
5. `n*_des.plt`의 terminal I–V, interface gap-states fields, TDR, Newton 수렴/KCL 확인. 필드가 없으면 H3 SVisualPy는 오류 중단.
6. 공통 14 V에서 `H3_Common_OK` 확인; 로그에 `H3_ICommon_A` 3조건 결과와 STI5 계면 적분 변화를 기록.
7. 추가로 trap-aware VBD 및 STI5/center E-field, Avalanche/BTBT 위치, ATP 영향을 확인하여 PEB·검출성능의 부작용 판단.
8. H3 성립 시 향후 동일 열 이력 N₂ vs N₂/H₂ 대조 실험 제안. **TCAD 상 `N_it` 감소만으로 실제 수소 패시베이션 효과가 입증되지는 않음**.

## 8. 출처/원본 보존

- 원본 Dark SDevice: `members/ryu980920/assets/tcad/spad-baseline-atp-dark-validation/CMP_SPAD_DarkCurrent_SDevice.txt`.
- 원본 Dark SVisualPy: `members/ryu980920/assets/tcad/spad-baseline-atp-dark-validation/CMP_SPAD_DarkCurrent_SVisualPy.txt`.
- 본 `H3/` 내 파일은 **원본을 복제하여 독립 수정**한 버전. 기존 `Electrical_Test/`, `H2_Mask_Sweep/`, 공유 SDE 원본은 변경하지 않음.
- 2026-11-16 연구 기록: `../../../timeline/2026-11/2026-11-16.md`.
- SDevice User Guide T-2022.03: Ch. 16 (SRH/SurfaceSRH), Ch. 17 (Traps / Visualizing Traps), Ch. 5 (CurrentPlot).

## 9. 테스트 상태

- [x] 코드상 SWB 변수 참조, H3 삽입 위치 및 기존 모델 불변 검토
- [ ] Sentaurus T-2022.03 SDevice 구문·`Traps` 런타임 검증
- [ ] `CurrentPlot` RegionInterface 적분/단위 검증
- [ ] SVisualPy에서 실제 변수명/데이터 로딩·출력 검증
- [ ] 계면 필드 및 `H3-0` 동등성 검증
- [ ] H3-1/H3-2 Dark Current 감소 및 신뢰성 검증
