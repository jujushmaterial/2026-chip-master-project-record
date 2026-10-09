# DOE 데이터 안내 (CMP SPAD — B: SProcess)

이 폴더는 **실험 조건표와 실제 시뮬레이션 결과 등 연구 데이터를 보관하는 곳**이다. 파일을 열지 않아도 어떤 구조의 어떤 목적의 DOE인지 판단할 수 있도록 하위 폴더별 `README.md`에 **이전 결과 → 이번 DOE의 질문 → sweep 변수/범위 → CSV 파일의 역할 → 다음 결정과 현재 상태**를 짧게 적는다.

## DNW 구조별 의미

| 구분 | 의미 | 연구 질문 | 데이터 폴더 |
|---|---|---|---|
| **Single-DNW / Large DOE** | DNW implant를 단일 profile component로 취급하는 초기 공정 탐색 | 한 개의 DNW 조건과 PW/RTA 조절만으로 SDE surrogate DNW profile을 재현할 수 있는가? | [Single-DNW/](Single-DNW/) — 250-case 실제 결과 등록. 코드: [Large_DOE](../tcad/Large_DOE/) |
| **Dual-DNW** | DNW를 **Main + Shallow Trim** 두 phosphorus implant component로 분리 | junction-side와 약 1 µm main peak 및 폭을 하나의 implant보다 유연하게 조절할 수 있는가? | [Dual-DNW/](Dual-DNW/) |
| **Triple-DNW** | DNW를 **Main + Shallow Trim + Deep** 세 phosphorus implant component로 분리 | Dual-DNW에서 남은 1.4–1.8 µm deep-tail 부족까지 별도 Deep component로 조절할 수 있는가? | [Triple-DNW/](Triple-DNW/) |

여기서 **DNW는 Deep N-Well**, Main/Trim/Deep은 실제 ST 제조 recipe 명칭이 아닌 **문헌 제약 기반 surrogate process에서의 implant component**를 뜻한다. 세 DNW component는 개별 anneal을 갖지 않고 PW implant와 함께 **공통 WELL RTA 1회**를 적용한다. **Double/Triple DNW는 서로 다른 공정 가설을 뜻하며 별도의 장치 2개/3개를 뜻하지 않는다.**

## 폴더와 파일의 역할

- `assets/tcad/`: Sentaurus SProcess 및 SVisualPy **명령·코드·설정과 도구 사용 설명**
- `assets/data/`: 분석이 완료된 **실제 시뮬레이션 결과 CSV**와 데이터 해설. 실행 전 **입력 조건표는 원칙적으로 등록하지 않음**
- `timeline/`: **왜 이전 DOE의 후보를 선택하고 다음 DOE를 설계했는지** 날짜별 상세 의사결정과 실제 진행 상태

각 하위 폴더의 `README.md`를 먼저 읽는다. 실제 결과 CSV가 A/B로 나뉜 경우 **하나의 DOE**로 묶어 설명한다. DOE 설계·입력 단계의 사실은 `timeline/`에 기록하고, `assets/data/`의 CSV는 **결과를 확보·분석한 뒤** 등록한다.

**현재 보관한 CSV:** 실제 시뮬레이션 결과만 보관한다. Single-DNW 250-case 결과 1개, Dual-DNW 108-case 결과 2개(A/B 각각 54행), Triple-DNW 25-case 결과 1개, 총 **4개 CSV**.

**현재 미등록:** Dual-DNW 64-case 실제 결과(`Dual.csv` 또는 `Dual(1).csv`), Triple-DNW 45-case 결과(`1006A.csv`/`1006B.csv`), 진행 예정인 81-case 결과. **81-case 40/41개 입력 조건 CSV는 결과 확보 전이므로 2026-10-09에 GitHub에서 삭제했다.** 발표자료에 등장하는 250-case 이전의 PW/DNW 개별 공정 민감도 분석은 별도의 원시 결과 CSV가 있으면 추후 단계별로 추가한다.

자세한 연구 배경: [공유 SPAD 연구계획서](../../../../shared/decisions/SPAD_연구계획서.md) · [2026-10-09 B 연구일지](../../timeline/2026-10/2026-10-09.md).
