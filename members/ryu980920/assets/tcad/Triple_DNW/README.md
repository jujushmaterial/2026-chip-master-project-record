# Triple_DNW

CMP SPAD B-track의 Triple-DNW surrogate profile calibration에 사용하는 SProcess command와 SVisualPy 분석 코드를 보관한다.

## Files

### `CMP_SPAD_TripleDNW_SProcess_v0.3_Stage2_DOE_PLX_only_RECONSTRUCTED.txt`

- 공통 STI Stage 1에서 저장한 restart TDR을 입력으로 사용하는 SProcess Stage 2 command.
- Main / Trim / Deep DNW implantation과 PW/NW implantation 후 공통 WELL RTA를 한 번 수행한다.
- 공정 전·후 및 final PW/DNW profile 비교용 PLX를 출력한다.
- DOE용 PLX-only 버전으로, SDevice 연결용 TDR은 출력하지 않는다.
- 이전 CMP 대화의 코드를 재구성한 파일이므로 파일명과 내용에 **RECONSTRUCTED**를 명시한다.

### `CMP_SPAD_TripleDNW_ProfileScreening_SVisualPy_v0.4_DeepTail.md`

- SProcess가 출력한 post-RTA 및 final PLX를 읽어 SDE surrogate baseline의 PW/DNW profile과 비교하는 SVisualPy 코드.
- Dual-DNW의 기존 profile-matching SCORE 계산은 유지하고, `TAIL14_R`, `TAIL16_R`, `TAIL18_R`, `TAIL_RMSE` 분석을 추가한다.
- DOE metric, 상세 결과 TXT, profile 비교 CSV 및 그래프를 출력한다.
- 실행 코드는 Markdown 파일 내부의 Python 코드 블록에 보관되어 있다.
