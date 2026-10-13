<!-- 생성물. 직접 고치지 말 것: python3 work/tools/build.py -->

# 테스트케이스에서 출발하는 스키마 계약

요구사항은 `testcases/cases/`, 값의 구조는 `contracts/`, 업무 규칙의 참고 명세는 `rules/`다.
이 프로젝트는 필요한 값을 표현할 수 있는지 검사하며 업무 동작을 구현·평가하지 않는다. [구조와 책임](../docs/architecture.md), [검증 방법](../docs/validation.md), [계약 원본](contracts/README.md)을 함께 읽는다.

| 컴포넌트 | 책임 | 입출력 원본 | 중첩 필드 |
|---|---|---|---|
| Frontend | 사용자 말을 STT로 글자로 바꿔 보내고, 응답 문장을 TTS로 읽어 준다. | [input](contracts/components/frontend/input.schema.json), [output](contracts/components/frontend/output.schema.json) | [상세](out/components/frontend.md) |
| Staff Console | 직원·의료진에게 알림을 보여 주고, 그들의 결정(재개·종료)을 보낸다. | [input](contracts/components/staff_console/input.schema.json), [output](contracts/components/staff_console/output.schema.json) | [상세](out/components/staff_console.md) |
| Orchestrator | 한 턴의 순서대로 컴포넌트를 부르고, 저장소에서 정해진 범위를 가져와 건네고, 쓰기를 저장소에 전달한다. | [input](contracts/components/orchestrator/input.schema.json), [output](contracts/components/orchestrator/output.schema.json), [trace](contracts/types/TurnTrace.schema.json) | [상세](out/components/orchestrator.md) |
| Utterance Parser | 사용자 발화를 (대상, 값, 원문, 의도) 항목들로 바꾼다. | [input](contracts/components/utterance_parser/input.schema.json), [output](contracts/components/utterance_parser/output.schema.json) | [상세](out/components/utterance_parser.md) |
| Answer Normalizer | 항목 값을 표준 형태로 바꾸고, 규칙 위반·기존 값과의 같음/다름·빠진 필수 슬롯·선행 조건을 사실로 표시한다. | [input](contracts/components/answer_normalizer/input.schema.json), [output](contracts/components/answer_normalizer/output.schema.json) | [상세](out/components/answer_normalizer.md) |
| Answer Judge | 이번 발화가 각 대상에 대해 무엇을 뜻하는지(정상·정정·충돌·누락 등) 판정한다. | [input](contracts/components/answer_judge/input.schema.json), [output](contracts/components/answer_judge/output.schema.json) | [상세](out/components/answer_judge.md) |
| Record Writer | 판정을 응답 기록에 어떻게 반영할지 슬롯별로 정한다. | [input](contracts/components/record_writer/input.schema.json), [output](contracts/components/record_writer/output.schema.json) | [상세](out/components/record_writer.md) |
| Dialogue Planner | 다음에 무엇을 말할지 정하고, 그 말에 필요한 값과 문장 재료를 담은 응답 지시를 만든다. | [input](contracts/components/dialogue_planner/input.schema.json), [output](contracts/components/dialogue_planner/output.schema.json) | [상세](out/components/dialogue_planner.md) |
| Response Generator | 응답 지시를 사용자 발화에 맞춰 받아 주며 자연스러운 문장으로 바꾼다. | [input](contracts/components/response_generator/input.schema.json), [output](contracts/components/response_generator/output.schema.json) | [상세](out/components/response_generator.md) |
| Result Dispatcher | 확정된 문진 결과를 시스템 밖으로 넘긴다. | [input](contracts/components/result_dispatcher/input.schema.json), [output](contracts/components/result_dispatcher/output.schema.json) | [상세](out/components/result_dispatcher.md) |
| Question Bank | 문진 설계자가 등록한 문항 정의를 버전별로 읽기 전용으로 보관한다. | [state](contracts/components/question_bank/state.schema.json) | [상세](out/components/question_bank.md) |
| Session Store | 세션별 응답 기록·진행 기록·Plan 기록·세션 정보·로그를 보관하고, 받은 쓰기를 정해진 효과대로 반영한다. | [state](contracts/components/session_store/state.schema.json), [load_request](contracts/types/SessionLoadRequest.schema.json), [load_result](contracts/types/SessionLoadResult.schema.json), [commit_request](contracts/types/SessionCommitRequest.schema.json), [commit_result](contracts/types/SessionCommitResult.schema.json) | [상세](out/components/session_store.md) |

정형 예시의 표현 가능 여부는 `../generated/representation_report.json`에 기록한다.

[전체 필드 연결](out/connections.md)에서 출력 소비와 저장 목적을 추적한다. 에이전트 탐색은 [안내](../docs/agent-guide.md)를 따른다.
