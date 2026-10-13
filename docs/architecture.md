# 구조와 책임

이 프로젝트의 대상은 사용자의 자유응답을 정형 문진 값으로 표현하고, 정해진 다음 행동을 자연어 응답으로 전달하는 시스템이다. 아래 역할은 데이터의 생산·소비 책임을 설명한다. 실행 코드는 이 프로젝트에 없다.

## 컴포넌트

| 컴포넌트 | 책임 | 주요 계약 |
|---|---|---|
| Frontend | 발화를 받아 보내고 응답과 실패 신호를 표시 | FrontendMessage / FrontendInput |
| Utterance Parser 또는 LoRA-A | 발화의 대상·원문·값·의도를 추출 | UtteranceParserInput / ParserOutput |
| Answer Normalizer | 단위·범위·누락 등 정형 검사 결과를 표현 | AnswerNormalizerInput / NormalizerOutput |
| Answer Judge | 항목별 상태와 발화 전체 판정을 표현 | AnswerJudgeInput / JudgeOutput |
| Record Writer | 판정을 바탕으로 저장할 변경을 표현 | RecordWriterInput / StoreResult |
| Dialogue Planner | 다음 행동과 응답에 필요한 재료를 표현 | DialoguePlannerInput / PlannerOutput |
| Response Generator 또는 LoRA-B | 응답 지시를 자연어로 표현 | ResponseGeneratorInput / GeneratorOutput |
| Orchestrator 또는 LangGraph | 조회·호출·입력 조립·쓰기·전달의 순서를 관리 | OrchestratorInput / OrchestratorOutput |
| Staff Console | 직원·의료진 알림과 개입 결정을 전달 | StaffConsoleInput / InterventionDecision |
| Result Dispatcher | 확정된 문진 결과와 전달 결과를 표현 | DispatchInput / DispatchOutput |
| Question Bank | 문항·슬롯·선택지·단위·기준·세션 설정을 보관 | QuestionBank |
| Session Store | 세션별 답·진행·계획 기록과 로그를 보관 | SessionStore |

발화 턴은 원문 수신, 사실 추출, 정규화, 상태 판정, 저장 판단, 계획 결정, 응답 생성으로 이어진다. 세션 시작·종료·직원 개입·실패 턴은 일부 경계를 사용하지 않을 수 있다. 구체적인 처리 요구는 [Orchestrator 명세](../work/rules/orchestrator.md)와 [시점 정의](../work/rules/timing.md)에 있다.

## 데이터의 구분

`ParserOutput`은 원시 추출 결과이고 저장 결정이 아니다. `NormalizerOutput`은 정형 검사 결과, `JudgeOutput`은 상태 판정, `StoreResult`는 저장할 변경, `PlannerOutput`은 진행 갱신과 응답 지시다. 각각을 같은 의미의 결과로 취급하지 않는다.

`QuestionBank`는 문항의 실제 선택지·단위·범위·선행 조건을 담는다. 범용 값 타입이 Schema를 통과해도 그 문항에서 허용되는 답인지까지 통과했다는 뜻은 아니다. 문항별 판단은 업무 컴포넌트의 책임이다.

`SessionStore.answer_records[].current_value`는 현재 답, `history`는 오래된 순서의 이전 답 값, `pending`은 확인 대기 중인 후보다. 현재 이력 구조는 별도 변경 ID·변경 시각을 정의하지 않는다. 이 정보를 요구하는 새 요구사항이 생기면 일반 계약 변경 절차로 검토한다.

## 입력의 출처와 시점

[bindings.yaml](../work/contracts/bindings.yaml)은 목적 입력 필드마다 원천 계약, 읽는 시점, 전달 방식을 정의한다. 직접 복사, 필드 투영, 참조에 따른 조회, 여러 원천의 결합, 입력 분기별 필드 추출, 조회 메타데이터를 구분한다. 선택 정책의 구현은 Orchestrator 담당자의 책임이다.

`turn_start`는 이번 턴 쓰기 전, `post_store_write`는 저장 결정 반영 후, `post_turn_write`는 턴의 모든 쓰기 반영 후다. 같은 세션의 값이라도 시점이 다르면 달라질 수 있다. LoRA-A에 제공할 기존 답 후보의 선정은 입력 조립 구현의 책임이며 현재 입력 자료형의 미완성 사항이 아니다.

## 업무 로그와 전체 Trace

`LogEntry`는 업무 결과와 경계 출력을 기록하는 로그 항목이다. `TurnTrace`는 세션·턴·계약 버전, 각 컴포넌트의 원본 입력과 출력, 저장 전후 상태를 기록하는 전체 Trace 형식이다. 서로 다른 용도이므로 하나를 다른 하나의 완전한 대체로 취급하지 않는다.

TurnTrace의 각 경계 필드는 해당 계약의 전체 JSON 또는 null이다. null은 payload 미확보를 뜻하며 단계가 실행되지 않았다고 단정하지 않는다. 수집·유일한 턴 ID 생성·보관·실행 성공은 수집 담당자의 책임이다. 정적 Trace 예시는 실제 실행 기록이 아니다.

## 원본과 생성물

Schema는 필수 필드·타입·허용 코드·중첩 구조·출력 자체의 구조적 관계를 정한다. 의미 설명 파일은 각 필드의 뜻과 필요 이유를 정한다. 업무 요구는 그 정보를 사용해야 하는 상황을 설명한다. [계약 원본 안내](../work/contracts/README.md)에 파일별 우선순위와 수정 위치가 있다.

## 값의 부가 정보와 저장 포트

정밀도·복수 원문 근거는 값 메타데이터로, 안정적인 코드와 표시 이름은 등록 목록과 코드 값으로, 세부 문제 사유는 problem_details로 표현한다. 데이터의 뜻과 전달 경로는 [값과 근거의 정보 계약](information.md)에 있다. Session Store의 조회·저장 요청과 결과는 데이터 계약 초안이며 API 합의 상태를 확인해야 한다.

## 출력의 전달 목적

입력 계약의 소비 관계는 bindings.yaml에서 역으로 확인한다. 저장 상태는 입력 계약이 아니므로 output_bindings.yaml에서 생산 출력의 필드와 저장 목적 필드를 별도로 선언한다. 저장 결정·진행 갱신·로그 항목은 반영할 자료이며 현재 상태와 같은 값이라는 직접 복사 주장이 아니다. 선언 근거는 저장 필드의 의미 설명에 있다. 전송·조회·반영 동작을 실행하지 않는다.
