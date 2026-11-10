# CMP SPAD — 6개 전기 노드 실행 검증 기준

## 1. 노드와 덱 연결 확인

SNMesh2 이후 배치: **SDevice1 → SVisualPy1 → SDevice2 → SVisualPy2 → SDevice3 → SVisualPy3**.

SNMesh2에서 Mesh를 읽는 상대 참조:
- SDevice1: `n@node|-1@_msh.tdr`
- SDevice2: `n@node|-3@_msh.tdr`
- SDevice3: `n@node|-5@_msh.tdr`

SVisualPy1은 SDevice1의 PLT를 읽는다. SVisualPy2는 SDevice2에서 만든 `_SCR_des.tdr`와 `_ATP_des.tdr`를 읽는다. SVisualPy3은 SDevice3 PLT와 SDevice1 VBD 진단 PLT를 읽는다.

## 2. 동적 SCR·ATP 평가전압 확인

SVisualPy1에서 `DOE:`로 `VBD_V`, `SCR_BIAS_V`, `ATP_BIAS_V`가 **모두 숫자로 출력**되어야 한다. SDevice2의 전처리 덱에서는 `@SCR_BIAS_V@`와 `@ATP_BIAS_V@`가 실제 숫자 `Goal`로 치환되어야 한다.

고정 15.6 V·17.0 V의 `When(Contact=... voltage=...)` Snapshot을 선택하는 대신, SDevice2는 **각 실험에서 계산한 두 전압**에 도달하고 `_SCR_des.tdr`, `_ATP_des.tdr`를 생성해야 한다.

## 3. P0 실제 실행 시험 — 최종 통과 전 필수 확인

1. P0 한 조건을 SVisualPy1까지 실행해 `VBD_V`와 두 평가전압, 기록 파일을 확인한다.
2. 과거 P0 VBD 약 15.02598 V가 재현된다면 SCR 전압은 약 14.827982 V, ATP 전압은 약 16.227982 V가 된다. **실제 사용값은 이번 실행에서 추출한 VBD**를 따른다.
3. SDevice2의 전처리된 `pp*_des.cmd`에서 두 `Goal`이 숫자인지 확인한다. `-1` 또는 미치환 `@...@`가 들어 있으면 안 된다.
4. SDevice2가 양쪽 목표전압에서 수렴하고 `_SCR_des.tdr`·`_ATP_des.tdr`를 생성하는지 확인한다. SVisualPy2에서 `SCR_OK=1`, `ATP_OK=1` 및 SCR 중심·폭과 ATP 분포를 확인한다.
5. SDevice3이 SCR 평가전압까지 Feedback 활성화 상태로 계산되고 SVisualPy3에서 `Dark_OK=1`, `INear_pAum2`가 출력되는지 확인한다. 15.6 V가 범위를 벗어나는 경우 해당 지표가 NA여도 실패 사유가 아니다.
6. 이전 B측 `ATP_peak=0.422`와 비교하려면 통일된 ATP 물리 모델로 공통 SDE 기준을 다시 계산한다.

**검증 상태:** 덱 참조와 전압 계산의 정적 검토는 수행했지만 실제 Synopsys Sentaurus Workbench/T-2022.03 환경의 6노드 실행은 수행하지 못했다. 따라서 **실제 실행 통과 여부는 미확인**이다.
