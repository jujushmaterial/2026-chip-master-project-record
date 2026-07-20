# 2026 Chip Master Project Record

## 1. Repository Overview

이 레포지토리는 **2026 차세대반도체 Chip Master Project 활동 과정을 시간순으로 기록하기 위한 공동 작업 공간**이다.

완성된 포트폴리오나 홍보용 결과물을 만드는 것이 아니라, 프로젝트 진행 중 각 구성원이 수행한 조사·설계·실험·분석·회의·문서 작성·문제 해결 과정을 추적 가능한 형태로 남기는 것을 목적으로 한다.

기록은 다음 질문에 답할 수 있어야 한다.

- 누가 수행했는가
- 언제 수행했는가
- 무엇을 수행했는가
- 왜 수행했는가
- 어떤 결과를 확인했는가
- 결과의 근거는 무엇인가
- 어떤 문제와 미완료 작업이 남아 있는가
- 다음에는 무엇을 해야 하는가

> 이 레포는 타임라인 기록용이다. 포트폴리오처럼 성과를 과장하거나 결과만 가공해서 작성하지 않는다.

---

## 2. Participants

| Member | GitHub ID | Personal Record Folder |
|---|---|---|
| Member A | [`jujushmaterial`](https://github.com/jujushmaterial) | `members/jujushmaterial/` |
| Member B | [`ryu980920`](https://github.com/ryu980920) | `members/ryu980920/` |

세부 담당 영역은 프로젝트 주제와 역할 분담이 확정된 뒤 추가한다.

---

## 3. Repository Structure

```text
2026-chip-master-project-record/
├─ README.md
├─ members/
│  ├─ jujushmaterial/
│  │  ├─ timeline/
│  │  ├─ references/
│  │  └─ assets/
│  └─ ryu980920/
│     ├─ timeline/
│     ├─ references/
│     └─ assets/
├─ shared/
│  ├─ meetings/
│  ├─ decisions/
│  ├─ references/
│  └─ assets/
└─ templates/
   ├─ daily-record-template.md
   ├─ meeting-template.md
   └─ decision-template.md
```

### Folder Purpose

- `members/<GitHub-ID>/timeline/`: 각 구성원이 직접 수행한 활동의 날짜별 기록
- `members/<GitHub-ID>/references/`: 개인적으로 검토한 논문, 공식 문서, 기술자료 목록
- `members/<GitHub-ID>/assets/`: 개인 기록에 연결되는 이미지, 그래프, 표, 데이터 및 캡처
- `shared/meetings/`: 공동 회의와 피드백 기록
- `shared/decisions/`: 프로젝트 방향에 영향을 주는 주요 의사결정 기록
- `shared/references/`: 두 구성원이 공통으로 사용하는 참고자료
- `shared/assets/`: 팀 공용 이미지, 그래프, 표 및 결과 자료
- `templates/`: 날짜별 활동 기록, 회의록, 의사결정 기록의 공통 양식

Git은 빈 폴더를 저장하지 않으므로, 아직 내용이 없는 폴더에는 `.gitkeep` 파일을 둔다.

---

## 4. Personal Timeline Rules

개인 활동은 아래 경로에 기록한다.

```text
members/<GitHub-ID>/timeline/YYYY-MM/YYYY-MM-DD.md
```

예시:

```text
members/jujushmaterial/timeline/2026-07/2026-07-20.md
```

### File Rules

1. 파일명은 실제 활동일을 기준으로 `YYYY-MM-DD.md` 형식을 사용한다.
2. 같은 날 여러 작업을 수행했다면 파일을 나누지 않고 하나의 날짜 파일에 소제목을 추가한다.
3. 나중에 기록한 경우 실제 활동일과 기록일을 구분한다.
4. 정확한 날짜를 확인할 수 없다면 날짜를 임의로 만들지 않는다.
5. 활동이 없었던 날은 파일을 만들 필요가 없다.
6. 과거 기록의 수치·결론을 수정하면 문서 하단의 수정 이력에 이유를 남긴다.

---

## 5. Required Daily Record Sections

모든 개인 타임라인에는 최소한 다음 항목을 포함한다.

1. 기본 정보
2. 활동 목표
3. 수행한 작업
4. 확인된 결과
5. 문제점 또는 한계
6. 주요 결정 사항
7. 미완료 작업
8. 다음 작업
9. 참고자료
10. 수정 이력

`templates/daily-record-template.md`를 복사하여 작성하는 것을 원칙으로 한다.

---

## 6. Activity Type

`활동 구분`은 다음 값 중 하나 이상을 사용한다.

- `Research`: 논문·기술자료 조사
- `Planning`: 프로젝트 계획과 일정 수립
- `Meeting`: 회의·면담·피드백
- `Design`: 구조·실험·시스템 설계
- `Experiment`: 실험 수행
- `Simulation`: 시뮬레이션 수행
- `Analysis`: 데이터와 결과 분석
- `Development`: 코드 또는 프로그램 개발
- `Documentation`: 문서와 발표 자료 작성
- `Troubleshooting`: 오류 분석과 문제 해결
- `Review`: 결과 검토와 상호 피드백
- `Other`: 그 밖의 활동

여러 활동이 포함되면 쉼표로 구분한다.

```text
활동 구분: Research, Analysis
```

---

## 7. Progress Status

`진행 상태`는 다음 값 중 하나를 사용한다.

- `Not Started`: 계획만 수립하고 시작하지 않음
- `In Progress`: 진행 중
- `Completed`: 계획한 범위 완료
- `Blocked`: 외부 문제로 진행 불가
- `Needs Review`: 검토 필요
- `Rework Required`: 수정 또는 재작업 필요
- `Cancelled`: 작업 취소

일부만 완료된 작업을 `Completed`로 표시하지 않는다.

---

## 8. Writing Standards

### Basic Style

- 한국어 작성을 기본으로 한다.
- 기술명, 장비명, 소프트웨어명은 필요한 경우 영어 원문을 함께 적는다.
- 간결한 사실 중심 문장을 사용한다.
- 결과만 적지 않고 수행 과정과 판단 근거를 함께 적는다.
- 과도한 수식어, 자기평가, 홍보성 표현을 사용하지 않는다.
- 실제로 수행하지 않은 활동을 추가하지 않는다.
- 미완료 작업을 완료된 것처럼 작성하지 않는다.
- 다른 구성원의 활동을 추측해서 대신 기록하지 않는다.

### Fact and Interpretation

확인된 사실과 작성자의 해석을 구분한다.

```text
확인된 결과:
측정값은 3회 모두 기준값보다 높게 나타났다.

해석:
시료 준비 과정의 오차가 영향을 주었을 가능성이 있다.
```

근거가 충분하지 않을 때는 다음과 같이 표시한다.

- 추가 확인 필요
- 현재 자료만으로 판단하기 어려움
- 임시 가설
- 재현 실험 필요
- 미검증

---

## 9. AI Usage Rules

두 구성원은 활동 기록 정리와 문서 작성에 AI를 사용할 수 있다. 다만 AI는 **기록 보조 도구**이며, 실제 활동이나 결과를 만들어내는 도구가 아니다.

### Allowed

- 본인이 작성한 메모 정리
- 문장 교정과 표현 통일
- 긴 내용을 공통 양식에 맞게 재구성
- 자료 요약 초안 작성
- 표와 목록 변환
- 누락 항목 점검
- 회의 메모 정리
- 코드 설명과 오류 기록 정리

### Prohibited

- 수행하지 않은 활동 생성
- 확인하지 않은 결과·수치·날짜·조건 생성
- 존재하지 않는 논문이나 참고자료 작성
- 실제 회의에서 논의하지 않은 내용 추가
- AI의 추측을 검증 없이 사실로 기록
- 다른 구성원의 활동을 임의로 작성
- 성과를 과장하거나 실패 과정을 삭제

### Verification

AI가 작성한 내용은 커밋 전에 작성자가 직접 확인한다.

- 실제 수행 내용과 일치하는가
- 날짜와 작성자가 정확한가
- 수치와 단위가 정확한가
- 파일명과 경로가 정확한가
- 참고자료가 실제로 존재하는가
- 사실과 해석이 구분되어 있는가
- 미완료 상태가 정확하게 표시되어 있는가

AI가 기술자료 요약, 코드 생성·수정, 데이터 해석 또는 의사결정 지원에 직접 사용됐다면 사용 목적과 검증 방법을 기록한다.

```text
사용한 AI: ChatGPT
사용 목적: 조사 메모의 구조화와 문장 정리
검증 방법: 원문 및 실제 활동 메모와 대조
```

---

## 10. Evidence and Reference Rules

중요한 결과에는 가능한 한 근거 파일을 연결한다.

- 원본 데이터
- 분석 파일
- 그래프
- 실험 사진
- 장비 화면 캡처
- 코드
- 발표 자료
- 공식 문서
- 논문
- 회의록

레포 내부 파일은 상대경로로 연결한다. 모든 수치에는 단위를 함께 작성한다.

참고자료에는 가능한 한 다음 정보를 포함한다.

```text
- 제목:
- 저자 또는 기관:
- 발행 연도:
- 링크 또는 식별 정보:
- 프로젝트에서 참고한 내용:
- 확인일:
```

AI가 제안한 논문이나 자료는 실제 존재 여부와 원문 내용을 확인한 뒤 기록한다.

---

## 11. Asset Naming Rules

이미지, 그래프, 데이터 파일은 다음 형식을 권장한다.

```text
YYYY-MM-DD-content-keyword.ext
```

예시:

```text
2026-07-20-device-structure.png
2026-07-20-measurement-result.csv
2026-07-20-simulation-error.png
```

- 파일명에는 공백을 사용하지 않는다.
- 가능한 경우 영문 소문자와 하이픈을 사용한다.
- 가공 파일과 원본 파일을 구분한다.
- 가공 결과를 만들었다고 해서 원본 데이터를 삭제하지 않는다.
- 이미지에는 무엇을 보여주는지 설명을 함께 작성한다.

---

## 12. Meeting and Decision Records

### Meeting

공동 회의는 아래 경로에 작성한다.

```text
shared/meetings/YYYY-MM-DD-meeting.md
```

회의록에는 회의 목적, 참석자, 논의 내용, 결정 사항, 역할 분담, 기한, 추가 확인 사항을 포함한다. 논의 중인 내용을 확정된 결정처럼 작성하지 않는다.

### Decision

프로젝트 방향에 영향을 주는 결정은 아래 형식으로 별도 기록한다.

```text
shared/decisions/DEC-001-topic.md
```

결정 기록에는 배경, 검토한 선택지, 최종 결정, 결정 이유, 예상 영향, 추가 검토 사항을 포함한다. 기존 결정을 변경하더라도 과거 파일을 삭제하지 않고 새로운 결정 기록에서 변경 관계를 명시한다.

---

## 13. Collaboration Rules

1. 각 구성원은 원칙적으로 자신의 `members/<GitHub-ID>/` 폴더를 수정한다.
2. 다른 구성원의 기록에서 오류를 발견하면 먼저 해당 구성원에게 알린다.
3. `README.md`, `shared/`, `templates/` 변경은 상대 구성원에게 공유한다.
4. 다른 구성원의 파일을 임의로 삭제하거나 덮어쓰지 않는다.
5. 대규모 폴더 이동이나 이름 변경은 먼저 협의한다.
6. 중요한 원본 데이터는 덮어쓰기보다 새 버전으로 저장한다.
7. 병합 충돌이 발생하면 한쪽 기록을 임의로 삭제하지 않는다.
8. `main` 브랜치에 강제 푸시하지 않는다.

---

## 14. Commit Rules

커밋 메시지는 아래 형식을 사용한다.

```text
type: 작업 내용
```

### Type

- `log`: 개인 활동 기록
- `docs`: README, 회의록, 규칙 및 문서
- `data`: 실험·분석 데이터
- `asset`: 이미지·그래프·첨부자료
- `fix`: 잘못된 기록이나 파일 수정
- `refactor`: 폴더 또는 문서 구조 정리
- `chore`: 기타 관리 작업

### Examples

```text
log: add activity record for 2026-07-20
docs: define repository documentation rules
data: add initial measurement results
asset: add device structure image
fix: correct voltage value in 2026-07-20 record
```

`update`, `수정`, `완료`, `test`처럼 변경 내용을 알 수 없는 메시지는 사용하지 않는다. 서로 관련 없는 변경은 가능한 한 별도 커밋으로 나눈다.

---

## 15. Security and Privacy

다음 정보는 업로드하지 않는다.

- 비밀번호, API Key, Access Token
- 개인 인증 정보와 개인정보
- 학교·기관의 비공개 자료
- 외부 공개가 금지된 실험 데이터
- 라이선스상 재배포가 금지된 자료
- 타인의 개인정보
- AI 서비스 로그인 정보

`.env`, `credentials.json`, `*.key`, `*.pem` 등 민감정보가 포함될 수 있는 파일은 커밋 전에 반드시 확인한다.

---

## 16. Pre-Commit Checklist

- [ ] 실제 활동일과 작성자를 적었는가
- [ ] 활동 목표와 실제 수행 내용을 적었는가
- [ ] 결과와 해석을 구분했는가
- [ ] 수치에 단위를 적었는가
- [ ] 중요한 결과에 근거 자료를 연결했는가
- [ ] 문제점과 미완료 작업을 숨기지 않았는가
- [ ] 다음 작업이 구체적인가
- [ ] AI가 생성한 정보를 직접 검증했는가
- [ ] 참고자료의 존재와 내용을 확인했는가
- [ ] 개인정보와 비공개 정보가 포함되지 않았는가
- [ ] 다른 구성원의 활동을 추측하여 작성하지 않았는가

---

## 17. Core Principle

이 레포에서 가장 중요한 기준은 글의 화려함이 아니라 **기록의 정확성, 추적 가능성, 재사용 가능성**이다.

AI를 사용하더라도 최종 기록의 정확성에 대한 책임은 해당 내용을 작성하고 커밋한 구성원에게 있다.
