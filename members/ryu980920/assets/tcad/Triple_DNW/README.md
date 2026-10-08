# Triple_DNW

CMP SPAD B-track의 Triple-DNW profile calibration에 사용한 DOE 입력값, SProcess 결과, SVisualPy 분석 코드를 보관하는 폴더이다.

## Files

### `CMP_SPAD_TripleDNW_ProfileScreening_SVisualPy_v0.4_DeepTail.py`

- SProcess가 출력한 PW/DNW PLX profile을 읽어 SDE surrogate baseline과 비교한다.
- 기존 profile matching SCORE와 함께 `TAIL14_R`, `TAIL16_R`, `TAIL18_R`, `TAIL_RMSE`를 추출한다.

### `CMP_SPAD_TripleDNW_FinalSweep_Part1.csv`

- 첫 Triple-DNW DOE의 SWB 입력 조건 Part 1 (23 cases).

### `CMP_SPAD_TripleDNW_FinalSweep_Part2.csv`

- 첫 Triple-DNW DOE의 SWB 입력 조건 Part 2 (22 cases).

### `1006A.csv`

- 첫 Triple-DNW DOE Part A의 SProcess/SVisualPy 결과 (23 cases).

### `1006B.csv`

- 첫 Triple-DNW DOE Part B의 SProcess/SVisualPy 결과 (22 cases).

### `CMP_SPAD_TripleDNW_MainToDeep_FineSweep_25cases.csv`

- 후속 Main-to-Deep dose redistribution 5 × 5 DOE의 SWB 입력 조건 (25 cases).
- 실험 결과가 아닌 실행용 조건표이다.

## Notes

- 첫 Triple-DNW 결과: `1006A.csv` + `1006B.csv`, 총 45 cases.
- 위 DOE 입력 CSV 3개는 이전 산출물의 저장된 표 데이터에서 복원한 파일이다.
- Triple-DNW SProcess command와 대표 PLX 원본은 아직 이 폴더에 등록되지 않았다.
- 날짜별 연구 활동과 결과 해석은 `members/ryu980920/timeline/`에서 관리한다.
