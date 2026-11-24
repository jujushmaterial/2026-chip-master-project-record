# CMP SPAD — DNW/PW 109 DOE (2026-11-25)

## 배포 범위
- 기존 Electrical_Test는 수정하지 않는다. 본 폴더는 신규 독립 버전이다.
- 전기 평가 덱 6개는 사용자가 첨부한 실제 로컬 덱 및 이후 수정·검증본을 기준으로 한다. SDevice 3개 모두 Math의 Iterations=100, Number_of_Threads=64로 확정. 초기 Coupled(Iterations=200)는 유지.
- 01~04 공정·메쉬 덱은 기존 Electrical_Test의 동일 Git blob을 복사한 참고본이다. 사용자의 현재 서버에 있는 공정·메쉬 덱과 바이트 동일성은 재확인되지 않았다.
- 공정 14개 SWB 입력만 유지한다. ATP_X를 추가 등록하지 않는다. 이미 등록한 ATP_X는 삭제. 나머지 14개 공정 변수는 하드코딩하지 않는다.
- 모든 수치는 문헌 기반 surrogate 공정 조건이며 실제 파운드리 recipe를 의미하지 않는다.

## DOE
| 변수 | Sweep | Final (P0) |
|---|---|---|
| DNW_TRIM_E (keV) | 600, 660, 680, 700 | 550 |
| DNW_TRIM_DOSE (cm^-2) | 5.00e12, 5.50e12, 6.00e12 | 7.50e12 |
| PW_TRIM_E (keV) | 135, 145, 155 | 145 |
| PW_TRIM_DOSE (cm^-2) | 3.24e12, 3.60e12, 3.96e12 | 3.60e12 |

108 full factorial + Final 1 = 109. Batch1: Final 첫 행 + 6.00e12 (37), Batch2: 5.50e12 (36), Batch3: 5.00e12 (36). 다른 10개 공정 변수는 Final 고정. 공통 RTA 1050 C/30 s. 기존 STI 및 mask 유지.

## SWB 연결 순서
1. SProcess1: 01_SProcess1_CommonSTI.cmd
2. SProcess2: 02_SProcess2_TripleDNW_TriplePW_AbsoluteDose.cmd
3. SNMesh1: 03_SNMesh1_Mesh2bnd.cmd
4. SNMesh2: 04_SNMesh2_ProfileMapping.cmd
5. SDevice1: sdevice_des.cmd
6. SVisualPy1: svisualpy_vis.py
7. SDevice2: sdevice1_des.cmd
8. SVisualPy2: svisualpy1_vis.py
9. SDevice3: sdevice2_des.cmd
10. SVisualPy3: svisualpy2_vis.py

기존 상대 노드 참조와 tool alias 유지. 현재 서버의 tool 순서/alias가 다르면 별도 확인 필요.

## 평가
- SDevice1 ionization-integral VBD 기준. SCR 및 Dark Bias = 0.987467*VBD. ATP = 1.05*VBD (고정된 내부 평가 상수, SWB 입력 아님).
- SVisualPy1은 #set 선언 및 DOE 출력으로 VBD_V, SCR_BIAS_V, DARK_BIAS_V, ATP_BIAS_V, SD2_END_V, SD2_T_SCR, SD2_T_V150, SD2_T_VBD, SD2_T_VEX05, SD2_T_VEX10, SD2_T_ATP, SD2_T_VEX15, SD3_T_BD50, SD3_T_BD90, SD3_T_BD95를 전달한다.
- SD2 ramp end = max(SCR,15 V,VBD,VBD+0.5,VBD+1.0,1.05*VBD,VBD+1.5). SD2 normalized Time = target/end. SD3 end = DARK_BIAS_V; BD50/90/95 time = target/end. Time은 정규화 변수이며 초가 아니다.
- SD2 7개, SD3 8개 snapshot 요청을 유지. SD3의 12/13/14 V When은 통과 단계에서 저장될 수 있고 실제 도달 범위를 넘는 TDR은 없을 수 있다.
- ATP_SCR_center: 각 조건 SCR Center (r=4.6875 um, z_if=y_raw-0.300 um)에서 jBreakdownProbability 보간. SCR 기준 |E|=100 kV/cm. 기존 180 nm 출력은 참고용으로 보존.
- 전계 peak, PW/DNW 쪽 peak-to-100 kV/cm 평균 감소 기울기 및 100/200/300/400 kV/cm 유지 길이, STI5 주변 전계 proxy 출력. 이는 보조 지표이며 PEB onset 자체의 입증이 아니다.
- SCR 위치는 사후 filtering하며 허용 범위는 미확정. SProcess Final 대비 비교. A+B 통합은 필수 목표에서 제외. Dark current는 절대 DCR이 아니다.
- 원래 모델 유지: SD1 GradQuasiFermi, SD2 ElectricField, SD3 Eparallel. SD1과 SD2의 항복 기준이 정확히 일치한다고 가정하지 않는다.

## 검증 상태 및 실행 주의
- 실제 첨부 전기 덱 6개 연결, 15개 자동 변수, 109행/14열, 327건 Python 구문 검사, 모의 데이터 기반 VBD/SCR/ATP/전계/Dark 추출을 확인했다. 실제 SWB 및 Sentaurus 수렴 검증은 하지 않았다.
- 마지막 실제 SWB 로그에서 n21의 SD2_END_V undefined 오류가 보고되었다. n20의 최신 코드 적용/전처리 및 실행 후 해결되었는지는 확인되지 않았다. 전체 109조건 실행 전에 Final의 SDevice1 -> SVisualPy1 순서로 실행하고 DOE 출력의 수치와 downstream 전처리 파일을 확인한다. -1 또는 x인 채로 실행하지 않는다.
- SWB scheduler의 CPU 할당 및 동시 실행 job 수와 64 threads 설정을 함께 확인한다. 병렬화 속도 개선은 미검증.
- VALIDATION_RESULT.txt에는 로컬 정적/모의 검사 결과를 기록한다.
