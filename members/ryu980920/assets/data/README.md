# DOE 데이터 안내 (CMP SPAD — B: SProcess)

이 폴더는 **실험 조건표와 실제 시뮬레이션 결과 등 연구 데이터를 보관하는 곳**이다. 파일을 열지 않아도 어떤 구조의 어떤 목적의 DOE인지 판단할 수 있도록 하위 폴더별 `README.md`에 **이전 결과 → 이번 DOE의 질문 → sweep 변수/범위 → CSV 파일의 역할 → 다음 결정과 현재 상태**를 짧게 적는다.

## DNW 구조별 의미

| 구분 | 의미 | 연구 질문 | 데이터 폴더 |
|---|---|---|---|
| **Single-DNW / Large DOE** | DNW implant를 단일 profile component로 취급하는 초기 공정 탐색 | 한 개의 DNW 조건과 PW/RTA 조절만으로 SDE surrogate DNW profile을 재현할 수 있는가? | [Single-DNW/](Single-DNW/) — 250-case 실제 결과 등록. 코드: [Large_DOE](../tcad/Large_DOE/) |
| **Dual-DNW** | DNW를 **Main + Shallow Trim** 두 phosphorus implant component로 분리 | junction-side와 약 1 µm main peak 및 폭을 하나의 implant보다 유연하게 조절할 수 있는가? | [Dual-DNW/](Dual-DNW/) |
| **Triple-DNW** | DNW를 **Main + Shallow Trim + Deep** 세 phosphorus implant component로 분리 | Dual-DNW에서 남은 1.4–1.8 µm deep-tail 부족까지 별도 Deep component로 조절할 수 있는가? | [Triple-DNW/](Triple-DNW/) |
| **PW-only calibration** | Triple-DNW Case 27의 DNW를 고정하고 PW의 Fixed/Trim 분배를 검토 | PW peak 과다와 junction-side tail 오차를 동시에 줄일 수 있는가? | [PW_Propile/](PW_Propile/) — 27조건 SWB 입력표 (미실행) |

여기서 **DNW는 Deep N-Well**, Main/Trim/Deep은 실제 ST 제조 recipe 명칭이 아닌 **문헌 제약 기반 surrogate process에서의 implant component**를 뜻한다. 세 DNW component는 개별 anneal을 갖지 않고 PW implant와 함께 **공통 WELL RTA 1회**를 적용한다. **Double/Triple DNW는 서로 다른 공정 가설을 뜻하며 별도의 장치 2개/3개를 뜻하지 않는다.**

## 폴더와 파일의 역할

- `assets/tcad/`: Sentaurus SProcess 및 SVisualPy **명령·코드·설정과 도구 사용 설명**
- `assets/data/`: **실제 실행 결과**, **진단 CSV**, 사용자가 명시적으로 보관을 요청한 **DOE 입력 조건표**를 각각 구분하여 보관한다. 미실행 조건표에는 결과 미확보 상태를 명시한다.
- `timeline/`: **왜 이전 DOE의 후보를 선택하고 다음 DOE를 설계했는지** 날짜별 상세 의사결정과 실제 진행 상태

각 하위 폴더의 `README.md`를 먼저 읽는다. 실제 결과 CSV가 A/B로 나뉜 경우 **하나의 DOE**로 묶어 설명한다. 입력조건표는 simulation-result CSV가 아니다. 2026-10-12 사용자의 명시적 요청에 따라 DNW/PW 27조건 입력표를 추가 보관하고, 해당 파일을 `INPUT / NOT RUN`으로 문서화한다.

**2026-10-12 보관 현황:** 기존의 실행 결과 CSV 7개에 81-case 결과 `1009A.csv`(40) / `1009B.csv`(41), grid/fit 진단 `FIT.csv`, DNW 입력/비교표 3개(최종 27, 비교 28행, 초기안 archive 27), PW 입력표 1개를 더해 **총 14개 CSV**다. 새 27조건 DNW/PW DOE는 **설계 완료 / 결과 미확인** 상태다.

**이력:** 2026-10-09에는 81-case 입력 조건표(40/41)를 결과 미확보 상태라 삭제했다. 2026-10-12에는 81-case **실제 결과 CSV를 확보·등록**했고, 신규 DNW/PW 27-case **입력표도 사용자의 추가 요청으로 별도 구분하여 등록**했다. 81-case 입력표 40/41을 다시 올린 것은 아니다. 자세한 분석은 [2026-10-12-1](../../timeline/2026-10/2026-10-12-1.md), PW 설계/코드는 [2026-10-12-2](../../timeline/2026-10/2026-10-12-2.md)를 참고한다.

자세한 연구 배경: [공유 SPAD 연구계획서](../../../../shared/decisions/SPAD_연구계획서.md) · [2026-10-09 B 연구일지](../../timeline/2026-10/2026-10-09.md).
