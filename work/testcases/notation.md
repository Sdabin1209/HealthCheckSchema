# 요구사항 케이스의 표기

이 문서는 케이스의 축약 표기와 기대 결과를 읽는 방법을 설명한다. `given`은 예시의 전제 상태, `input`은 예시 입력, `expect`는 요구하는 결과다. `주입`은 장애·대체 출력 상황을 표현하기 위해 가정한 경계값이다. 실제 컴포넌트를 실행한 기록이나 이 저장소가 제공하는 실행 검사기의 사용법이 아니다.

케이스의 정보는 `case_shapes/<ID>.json`에서 Schema 필드와 완전한 정적 예시로 연결한다. 상황 목록은 `situations.yaml`이며, 상황의 필요 이유와 케이스가 확인할 정보는 해당 자료에 설명한다. 검사 범위는 [검증 방법](../../docs/validation.md)을 따른다.

## 비교 표기의 의미

- 엄격 필드: 판정, 저장, Plan(행동·대상·알릴것·세션상태·흐름·직원알림·건너뜀추가·건너뜀해제·확인중단추가·확인중단해제·중지이력추가).
발화 턴에서 적지 않았으면 "없음 / 비어 있음 / 그대로"와 비교한다.
- 그 밖(LoRA-A, 정규화, 발화판정, 말할값, 기다리는답, LangGraph, 뒤, LoRA-B조건)은 적은 것만 비교한다.
- "범위"가 있는 케이스는 그 칸들만 비교한다(컴포넌트 하나만 떼어 보는 케이스). 엄격 필드 기본값은 범위 밖에는 걸리지 않는다.
- 기다리는답을 적지 않으면 응답 지시 자신(묻기 행동)이거나 Dialogue Planner 요구의 8-2절의 "지금 물을 것"이다.

표기
- 슬롯: 문항ID.슬롯ID (예: Q2.개비). 문항 전체: Q3b.*
- 값: 선택지 값은 그대로. 단위 값은 "수 단위"를 붙여 쓴다(주 2회 = {수: 2, 단위: 주 n회}, 1병 = {수: 1, 단위: 병}).
단위가 하나뿐인 슬롯은 수만 쓴다(Q5 7 = {수: 7, 단위: 시간}, Q2 20 = {수: 20, 단위: 개비}, Q7 190 = {수: 190, 단위: mmHg}).
- given.답: 응답 기록.현재값. given.확인대기: {슬롯: {ID, 값}}. given.직전: 진행 기록.직전 응답 지시.
given.기다리는답이 없으면 직전 자신이 기다리는 답이다.
- given.열린요청 / given.건너뜀 / given.확인중단: 진행 기록의 사실. 적지 않으면 비어 있다(중단요청은 아니요).
- given.Plan기록: 시도횟수 {문항: 수}, 확인횟수 {슬롯: 수}, 모름횟수, 거절횟수, 알아듣지못한연속, 물은횟수. 적지 않은 값은 0이고,
확인횟수만은 직전 행동이 그 슬롯의 확인 대기 확인이면 1이다(이미 한 번 물었으므로).
- given.세션: 진행 중(기본) / 없음 / 일시 중지(위험) / 종료(완료)
- 기본 상태: given.세션이 없음·종료가 아니고 "기본: 없음"도 없으면, 적지 않은 Q1~Q4는 아래 값으로 본다.
Q1.상태 = 현재 피움, Q2.개비 = 10, Q3a.여부 = 마심, Q3b = {빈도: 주 2회, 종류: 소주, 1회양: 1병}, Q4.여부 = 예
given.답에 적은 값이 앞선다. Q5 이후는 적은 것만 답이 있다.
- "H1 뒤 상태": 기본 없음, 답 {Q1.상태: 안 피움, Q3a.여부: 안 마심, Q5.시간: 7, Q6.여부: 아니요, Q7.수축기: 120, Q7.이완기: 80, Q8.횟수: 주 3회}

## 스키마 표현 검사에서의 표기
`JudgeOutput.judgments[].status`에 대응하는 “상태: 없음”은 코드 문자열이 아닌 JSON null을 뜻한다. 이 필드별 변환은 `work/contracts/case_notation.yaml`의 field_encodings에 명시한다. 입력의 정답 여부를 계산하는 규칙은 아니다.

## 규칙 절 참조

케이스의 이유에 적힌 절 번호는 이 저장소에 포함된 업무 요구 문서의 제목 번호다. 기대 결과를 읽기 위한 내부 참조이며 이 프로젝트가 해당 동작을 실행했다는 뜻은 아니다.

| 절 | 문서 |
|---|---|
| 0 | [원칙](../rules/principles.md) |
| 0-1 | [전제 조건](../rules/preconditions.md) |
| 0-2 | [상태 조회 시점](../rules/timing.md) |
| 1 | [역할과 계약](../rules/mapping.md) |
| 9-2 | [Session Store](../rules/session_store.md) |
| 4 | [Utterance Parser](../rules/utterance_parser.md) |
| 5 | [Answer Normalizer](../rules/answer_normalizer.md) |
| 6 | [Answer Judge](../rules/answer_judge.md) |
| 7 | [Record Writer](../rules/record_writer.md) |
| 8-1~8-4 | [Dialogue Planner](../rules/dialogue_planner.md) |
| 9 | [Response Generator](../rules/response_generator.md) |
| 9-1 | [Orchestrator](../rules/orchestrator.md) |
| 자료형 이름·필드 경로 | [계약 인덱스](../schema.md)와 해당 계약 원본 |

전체 목록은 [업무 요구 manifest](../rules/manifest.yaml)에 있다.
