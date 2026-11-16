# 3D 구조 테스트 공통 전기 코드 사용 결정

## 1. 기본 정보

- 결정 식별자: `jujushmaterial-3d-electrical-baseline-2026-11-16` (개인 기록 식별자)
- 결정일/기록일: 2026-11-16 (KST)
- 결정자: 주상현 (`jujushmaterial`), 본 대화에서 향후 코드 사용 기준 기록을 명시적으로 요청함.
- 상태: **Accepted — 공통 코드 재사용 기준**
- 범위: 3D SPAD 구조 테스트의 전기 계산 및 후처리. 별도 팀 회의나 타 구성원의 승인 사실을 의미하지 않음.

## 2. 결정 배경

3D Candidate-B v2.6에서 SDevice 수렴 문제를 수정하고, SVisualPy의 좌표·SCR 경계·3D 적분 오류를 수정하여 VBD 및 SCR 숫자를 확보했다. 이후 구조마다 solver 및 추출 기준까지 함께 바꾸면 결과 차이의 원인을 분리하기 어렵다.

## 3. 검토한 선택지

| 선택지 | 장점 | 제한 |
|---|---|---|
| 확인된 SDevice v1.1 / SVisualPy v1.3을 공통 기준으로 사용 | 재현성과 구조 간 비교 기준 유지 | 구조가 기존 영역·좌표 계약을 지키는지 확인 필요 |
| 구조마다 물리모델/solver/추출 조건을 재조정 | 특수한 구조에 맞춘 조정 가능 | 구조 효과와 계산 방법 변경 효과가 혼재 |
| VBD 15.8 V 또는 SCR 180 nm에 맞추어 도핑 재보정 | 기존 숫자에 가까워질 가능성 | 동일 도핑 2D→3D 비교 목적을 변경하므로 현재 채택하지 않음 |

## 4. 최종 결정

**앞으로 3D 구조 테스트를 진행할 때 SDevice는 v1.1 ParDiSo, SVisualPy는 v1.3 VBD/SCR DOE 코드를 공통 기본 코드로 사용한다.**

- [SDE 기준 구조: Candidate-B v2.6](./CMP_SPAD_3D_CandidateB_v2.6_RadialCoarseBulk_UpperSiZFixed_DualMSH.txt)
- [공통 SDevice v1.1](./CMP_SPAD_3D_v2p6_SDevice_VBD_SCR_v1p1_ParDiSo.txt)
- [공통 SVisualPy v1.3](./CMP_SPAD_3D_v2p6_SVisualPy_VBD_SCR_DOE_v1p3.txt)
- [정확한 코드 해시](./baseline-manifest.json)

SDE v2.6은 reference 원본으로 보존하고 구조/메시 실험은 새 파일명 또는 별도 버전으로 만든다. 새 구조의 결과가 기존 수치에 맞지 않는다는 이유만으로 도핑, 전계 threshold 또는 좌표 원점을 조정하지 않는다.

## 5. 실행 전 호환 조건

1. 전체 Cartesian 3D이며 길이 단위는 µm이다. 전류는 전체 3D 소자의 A 단위를 사용한다.
2. 접촉 이름은 `anode`, `cathode`, `substrate`; anode/substrate=0 V, cathode sweep이다.
3. 전기 입력은 UpperSi=Oxide convention의 `n<SDE>_msh.tdr`이다. physical mesh를 연결하면 다른 실험 조건으로 분류한다.
4. SCR 적분 영역 이름은 `Bulk`, 원점은 STI 바닥 Z=0, 상면 Z=0.300 µm이다.
5. 기본 중심 cutline은 X=4.6875 µm, Y=0; 기본 ROI 반경은 12.5 µm, Z 범위는 −1.30~+0.30 µm이다.
6. 같은 실행의 PLT/log/마지막 TDR을 사용하고 Workbench 종속 노드 매크로가 올바르게 치환되어야 한다.

구조 변경으로 위 조건이 성립하지 않으면 값을 억지로 출력하지 않는다. 필요한 파라미터/영역 매핑 변경을 별도 버전으로 기록하고 reference와 새 구조에 대한 추출 의미가 같은지 검증한다. 모든 종류의 3D 소자에 무수정 적용 가능하다는 결정은 아니다.

## 6. 결과 판독 기준

- SDevice 정상 종료, VBD bracket 존재, SCR line/volume 플래그와 경고를 각각 확인한다.
- `VBD_OK=1`은 추출 성공이지 mesh convergence 또는 설계 성능 PASS가 아니다.
- `SCR15p6_OK=0`과 `SCR15p6_um=x`는 현 baseline의 15.6 V 결과가 없음을 뜻한다. 마지막 상태 SCR 실패와 혼동하지 않는다.
- SCR은 LAST 상태 기준이다. 구조마다 `SCR_bias_V`가 다르면 동일 전압 비교가 아니다. 공통 전압 snapshot 비교는 별도 실험으로 둔다.
- E-threshold 1e5 V/cm, sampled-min VBD, 원점 및 ROI를 비교 도중 변경하지 않는다. 변경하면 양쪽 baseline을 다시 처리하고 새 metric 이름/버전으로 기록한다.
- solver/memory 문제로 설정을 바꾸는 경우에도 변경 이유·전후 조건·reference 재현 결과를 남긴다.

## 7. 각 구조 실행 시 보관할 항목

| 분류 | 필수 기록 |
|---|---|
| 식별 | 구조 ID, 실행 시각/시간대, SWB node, SDE/SDevice/SVisualPy 버전과 SHA-256 |
| 구조 | 도핑 peak/깊이, 접촉, materials, 영역 이름, 메시 설정 및 품질/요소 수 |
| solver | 물리모델, 온도, solver, 수렴 기준, 최종 전압, 종료 이유, 시간·메모리 |
| 결과 | VBD, DeltaVBD, LastBias, SCR 중심/폭/부피/평가 전압, 모든 성공 플래그 |
| 근거 | 같은 실행의 PLT/log/TDR, metrics.json/csv, SCR_volume_details.json, 중심/주변부 CSV, coordinate diagnostics, 경고·API trace |
| 비교 | 비교 기준 run ID, 동일 전압 여부, mesh convergence 상태, 정의 변경 여부 |

실패 또는 미계산 값은 `x`/null과 이유를 보존하며 0으로 바꾸지 않는다. 원본 자료의 서버 보관과 GitHub 공개용 요약을 구분한다.

## 8. 예상 영향과 미완료 사항

향후 reference 및 구조 후보의 전기 계산 기준이 일관되게 유지된다. 아직 동일 전압 2D 비교, 3D mesh convergence, UpperSi 재료 민감도, PEB/ATP/DCR, EMW는 완료되지 않았다. 이 기준 채택이 기존 19개 3D 후보의 전기/광학 PASS를 선언하는 것은 아니다.

## 9. 관련 기록

- [현재 결과 보고서](./ELECTRICAL_BASELINE_REPORT_2026-11-16.md)
- [기존 SDE 채택](../../../timeline/2026-10/2026-10-09.md)
- [Annular 17개 및 총 19개 구조 계획](../../../../../shared/decisions/DEC-001-annular-3d-validation-17-cases-2026-10-09.md): 후보 구성은 이번 결정으로 변경하지 않음.

## 10. 수정 이력

- 2026-11-16: 사용자 지시에 따라 향후 3D 구조 테스트의 공통 SDevice/SVisualPy 버전과 변경 관리 기준을 기록.
