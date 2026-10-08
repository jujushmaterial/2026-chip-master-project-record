# Triple_DNW

CMP SPAD B-track Triple-DNW profile calibration에 사용한 SProcess, SVisualPy 및 DOE CSV 파일 보관 폴더이다.

## Files

### `CMP_SPAD_DualDNW_SProcess_v0.2_Stage1_CommonSTISeed.txt`
- 공통 SOI/STI 구조를 한 번 생성하고 후속 DOE를 위한 restart TDR을 저장한다.
- **Dual_DNW 원본과 변경 없음.**

### `CMP_SPAD_DualDNW_ProfileScreening_SVisualPy_v0.3_SDEAnchorFix.py`
- PW/DNW PLX profile을 읽어 SDE baseline target과 비교한다.
- **Dual_DNW 원본과 변경 없음.**

### `CMP_SPAD_TripleDNW_ProfileScreening_SVisualPy_v0.4_DeepTail.py`
- Triple-DNW DOE의 PW/DNW profile 및 SCORE를 분석한다.
- v0.3과 달리 `TAIL14_R`, `TAIL16_R`, `TAIL18_R`, `TAIL_RMSE` 추출 기능을 추가한 버전이다.

### `CMP_SPAD_TripleDNW_FinalSweep_Part1.csv`
- 첫 Triple-DNW DOE의 SWB 입력 조건 Part 1 (23 cases).

### `CMP_SPAD_TripleDNW_FinalSweep_Part2.csv`
- 첫 Triple-DNW DOE의 SWB 입력 조건 Part 2 (22 cases).

### `1006A.csv`
- 첫 Triple-DNW DOE Part A의 SProcess/SVisualPy 결과 (23 cases).

### `1006B.csv`
- 첫 Triple-DNW DOE Part B의 SProcess/SVisualPy 결과 (22 cases).

### `CMP_SPAD_TripleDNW_MainToDeep_FineSweep_25cases.csv`
- 후속 Main-to-Deep redistribution DOE의 SWB 입력 조건 (25 cases).
- 시뮬레이션 결과 파일이 아니다.

## Notes

- 첫 Triple-DNW 결과는 `1006A.csv`와 `1006B.csv`, 총 45 cases이다.
- 세 DOE 입력 CSV는 이전 산출물의 저장된 표 데이터에서 복원했다.
- **Triple-DNW SProcess Stage2 v0.3 실행 원문**은 아직 확보하지 못해 미등록 상태다. Dual-DNW Stage2를 Triple 실행 원본으로 잘못 등록하지 않는다.
- 연구 과정과 결과 해석은 `members/ryu980920/timeline/`에서 관리한다.
