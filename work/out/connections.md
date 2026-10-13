<!-- 생성물. 직접 고치지 말 것: python3 work/tools/build.py -->

# 컴포넌트와 필드의 전달 연결

원본은 `../contracts/bindings.yaml`과 `../contracts/output_bindings.yaml`이다. 생산·소비 관계를 추적하는 인덱스이며 실제 호출·조회·입력 조립·전달은 Orchestrator의 책임이다. 전송 구현이나 동작 성공을 나타내지 않는다. proposal은 현행 계약과 별도로 제안된 자료형이다.

## 출력·상태에서 입력으로

| 원천 컴포넌트 | 원천 계약·필드 | 목적 컴포넌트 | 목적 계약·필드 | 시점 | 전달 방식 | 상태 | 전달 설명 |
|---|---|---|---|---|---|---|---|
| Response Generator | GeneratorOutput.response_text | Frontend | FrontendInput.response_text | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Orchestrator | OrchestratorOutput.turn_failure_signal | Frontend | FrontendInput.turn_failure_signal | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Dialogue Planner | PlannerOutput.staff_alert | Staff Console | StaffConsoleInput.staff_alert | current_turn | join | current | PlannerOutput.staff_alert의 알림 내용과 SessionStore.session_info.session_id를 결합한다. 알림이 없으면 null이다. |
| Session Store | SessionStore.session_info.session_id | Staff Console | StaffConsoleInput.staff_alert | current_turn | join | current | PlannerOutput.staff_alert의 알림 내용과 SessionStore.session_info.session_id를 결합한다. 알림이 없으면 null이다. |
| Orchestrator | OrchestratorOutput.turn_failure_signal | Staff Console | StaffConsoleInput.turn_failure_signal | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Orchestrator | OrchestratorOutput.intervention_result | Staff Console | StaffConsoleInput.intervention_result | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Frontend | FrontendMessage.(전체) | Orchestrator | OrchestratorInput.frontend_input | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Staff Console | InterventionDecision.(전체) | Orchestrator | OrchestratorInput.intervention_decision | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.session_info.session_id | Orchestrator | OrchestratorInput.session_found | session_lookup | lookup_metadata | current | 세션 조회 결과의 존재 여부이다. 세션 데이터 문자열을 boolean으로 변환하는 필드가 아니다. |
| Session Store | SessionStore.session_info.question_bank_version | Orchestrator | OrchestratorInput.session_question_bank_version | turn_start | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.progress_record.session_status | Orchestrator | OrchestratorInput.session_status | turn_start | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Question Bank | QuestionBank.version | Orchestrator | OrchestratorInput.latest_question_bank_version | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Frontend | FrontendMessage.(전체) [Schema /oneOf/1/properties/utterance] | Utterance Parser | UtteranceParserInput.utterance | current_turn | variant_field | current | FrontendMessage의 UTTERANCE 분기 utterance를 제공한다. 발화가 없는 입력에서 null을 허용하는 목적 계약이면 null을 제공한다. |
| Session Store | SessionStore.progress_record.last_directive | Utterance Parser | UtteranceParserInput.last_directive | turn_start | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Question Bank | QuestionBank.questions | Utterance Parser | UtteranceParserInput.awaiting_questions | current_turn | lookup | current | 직전 지시 awaiting.targets가 참조하는 문항 정의를 중복 없이 제공한다. 범위 밖 확장 여부는 별도 정책이다. |
| Question Bank | QuestionBank.questions | Utterance Parser | UtteranceParserInput.question_names | current_turn | project | current | questions[]에서 question_id, name, slots[].slot_id를 각각 question_id, name, slots[]로 투영한다. |
| Session Store | SessionStore.answer_records | Utterance Parser | UtteranceParserInput.answered_slots | turn_start | project | current | answer_records[] 중 current_value가 {answer: Value}인 행을 slot 및 value=current_value.answer로 투영한다. 후보 행의 선정은 입력 조립 구현의 책임이며 전달 자료형과 구분한다. 원천 값의 value_metadata가 수집되어 있으면 함께 전달하며, 없으면 정확도나 근거를 임의 생성하지 않는다. |
| Question Bank | QuestionBank.session_settings.guide_list | Utterance Parser | UtteranceParserInput.guide_list | current_turn | project | current | guide_list[]에서 guide_id, selection_criterion만 투영하며 안내 문장은 제공하지 않는다. |
| Utterance Parser | ParserOutput.items | Answer Normalizer | AnswerNormalizerInput.items | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Question Bank | QuestionBank.questions | Answer Normalizer | AnswerNormalizerInput.related_questions | current_turn | lookup | current | 항목 대상·기다리는 답·직접 선행 조건이 참조하는 문항 정의를 중복 없이 제공한다. |
| Session Store | SessionStore.answer_records | Answer Normalizer | AnswerNormalizerInput.current_values | turn_start | project | current | 선택한 answer_records[]에서 slot 및 current_value를 투영한다. 원천 값의 value_metadata가 수집되어 있으면 함께 전달하며, 없으면 정확도나 근거를 임의 생성하지 않는다. |
| Session Store | SessionStore.answer_records | Answer Normalizer | AnswerNormalizerInput.pendings | turn_start | project | current | 확인 대기가 있는 선택 행에서 slot, pending.pending_id, pending.value만 slot, pending_id, value로 투영한다. risk_mark는 이 입력에 넣지 않는다. 원천 값의 value_metadata가 수집되어 있으면 함께 전달하며, 없으면 정확도나 근거를 임의 생성하지 않는다. |
| Session Store | SessionStore.progress_record.last_directive | Answer Normalizer | AnswerNormalizerInput.awaiting | turn_start | project | current | last_directive가 null이면 null, 아니면 last_directive.awaiting을 제공한다. |
| Orchestrator | TurnTrace.turn_index | Answer Normalizer | AnswerNormalizerInput.turn_index | current_turn | copy | current | 호출 문맥의 순번과 Trace에 기록할 순번을 동일하게 제공한다. 순번을 모델이 추정하지 않는다. |
| Utterance Parser | ParserOutput.items | Answer Judge | AnswerJudgeInput.items | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Answer Normalizer | NormalizerOutput.item_checks | Answer Judge | AnswerJudgeInput.item_checks | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Answer Normalizer | NormalizerOutput.missing_required_slots | Answer Judge | AnswerJudgeInput.missing_required_slots | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Frontend | FrontendMessage.(전체) [Schema /oneOf/1/properties/utterance] | Answer Judge | AnswerJudgeInput.utterance | current_turn | variant_field | current | FrontendMessage의 UTTERANCE 분기 utterance를 제공한다. 발화가 없는 입력에서 null을 허용하는 목적 계약이면 null을 제공한다. |
| Question Bank | QuestionBank.session_settings.risk_phrases | Answer Judge | AnswerJudgeInput.risk_phrases | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.progress_record.last_directive | Answer Judge | AnswerJudgeInput.last_directive | turn_start | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.answer_records | Answer Judge | AnswerJudgeInput.pendings | turn_start | project | current | 확인 대기가 있는 선택 행에서 slot, pending.pending_id만 slot, pending_id로 투영한다. value와 risk_mark는 이 입력에 넣지 않는다. |
| Question Bank | QuestionBank.questions | Answer Judge | AnswerJudgeInput.affected_followups | current_turn | project | current | questions[]의 question_id와 affected_followups를 각각 question_id와 followups로 투영한다. |
| Question Bank | QuestionBank.questions | Answer Judge | AnswerJudgeInput.question_slots | current_turn | project | current | questions[]에서 question_id 및 slots[].slot_id를 slot_ids[]로 투영한다. |
| Answer Judge | JudgeOutput.judgments | Record Writer | RecordWriterInput.judgments | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Answer Judge | JudgeOutput.invalidated_questions | Record Writer | RecordWriterInput.invalidated_questions | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Question Bank | QuestionBank.questions | Record Writer | RecordWriterInput.question_slots | current_turn | project | current | questions[]에서 question_id 및 slots[].slot_id를 slot_ids[]로 투영한다. |
| Session Store | SessionStore.answer_records | Record Writer | RecordWriterInput.target_records | turn_start | lookup | current | judgments의 대상 또는 invalidated_questions에 해당하는 슬롯 기록을 제공한다. |
| Orchestrator | OrchestratorOutput.turn_kind | Dialogue Planner | DialoguePlannerInput.turn_kind | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Answer Judge | JudgeOutput.utterance_judgment | Dialogue Planner | DialoguePlannerInput.utterance_judgment | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Answer Judge | JudgeOutput.judgments | Dialogue Planner | DialoguePlannerInput.judgments | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Record Writer | StoreResult.store_summary | Dialogue Planner | DialoguePlannerInput.store_summary | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.answer_records | Dialogue Planner | DialoguePlannerInput.answer_records | post_store_write | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.progress_record.last_directive | Dialogue Planner | DialoguePlannerInput.last_directive | turn_start | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.progress_record.skipped | Dialogue Planner | DialoguePlannerInput.skipped | turn_start | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.progress_record.confirm_stopped | Dialogue Planner | DialoguePlannerInput.confirm_stopped | turn_start | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.progress_record.open_requests | Dialogue Planner | DialoguePlannerInput.open_requests | turn_start | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.planner_record | Dialogue Planner | DialoguePlannerInput.planner_record | turn_start | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Question Bank | QuestionBank.(전체) | Dialogue Planner | DialoguePlannerInput.question_bank | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Dialogue Planner | PlannerOutput.directive | Response Generator | ResponseGeneratorInput.directive | current_turn | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Frontend | FrontendMessage.(전체) [Schema /oneOf/1/properties/utterance] | Response Generator | ResponseGeneratorInput.utterance | current_turn | variant_field | current | FrontendMessage의 UTTERANCE 분기 utterance를 제공한다. 발화가 없는 입력에서 null을 허용하는 목적 계약이면 null을 제공한다. |
| Session Store | SessionStore.session_info | Result Dispatcher | DispatchInput.session_info | post_turn_write | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.answer_records | Result Dispatcher | DispatchInput.answer_records | post_turn_write | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.progress_record.skipped | Result Dispatcher | DispatchInput.skipped | post_turn_write | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.progress_record.confirm_stopped | Result Dispatcher | DispatchInput.confirm_stopped | post_turn_write | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.progress_record.session_status | Result Dispatcher | DispatchInput.session_status | post_turn_write | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Session Store | SessionStore.progress_record.pause_history | Result Dispatcher | DispatchInput.pause_history | post_turn_write | copy | current | 지정 원천 필드의 payload를 목적 필드로 제공한다. 구조 변환은 없다. 원천 미확보 시 null 허용 여부는 목적 Schema에 따른다. |
| Frontend | FrontendMessage.(전체) [Schema /oneOf/1/properties/session_id] | Session Store | SessionLoadRequest.session_id | current_turn | variant_field | proposal | 현재 입력의 세션 식별자를 조회 요청에 전달한다. |
| Staff Console | InterventionDecision.session_id | Session Store | SessionLoadRequest.session_id | current_turn | variant_field | proposal | 현재 입력의 세션 식별자를 조회 요청에 전달한다. |
| Frontend | FrontendMessage.(전체) [Schema /oneOf/1/properties/session_id] | Session Store | SessionCommitRequest.session_id | current_turn | variant_field | proposal | 현재 입력의 세션 식별자를 저장 요청에 전달한다. |
| Staff Console | InterventionDecision.session_id | Session Store | SessionCommitRequest.session_id | current_turn | variant_field | proposal | 현재 입력의 세션 식별자를 저장 요청에 전달한다. |
| Session Store | SessionLoadResult.revision | Session Store | SessionCommitRequest.expected_revision | current_turn | copy | proposal | 조회 성공으로 확보한 상태 버전 토큰을 제공한다. 최초 저장과 결과 불명 시 정책은 미합의다. |
| Record Writer | StoreResult.(전체) | Session Store | SessionCommitRequest.writes | current_turn | join | proposal | 답 변경·진행 갱신·계획 기록을 TurnWriteSet의 명시적 세 필드로 결합한다. |
| Dialogue Planner | PlannerOutput.progress_record_update | Session Store | SessionCommitRequest.writes | current_turn | join | proposal | 답 변경·진행 갱신·계획 기록을 TurnWriteSet의 명시적 세 필드로 결합한다. |
| Dialogue Planner | PlannerOutput.planner_record_update | Session Store | SessionCommitRequest.writes | current_turn | join | proposal | 답 변경·진행 갱신·계획 기록을 TurnWriteSet의 명시적 세 필드로 결합한다. |

## 출력에서 저장 상태로 전달되는 쓰기 자료

아래 자료는 반영할 결정·갱신·기록이다. 원천과 저장 상태의 값이 같다는 직접 복사나 실제 반영 성공을 뜻하지 않는다.

| 생산 컴포넌트 | 출력 계약·필드 | 저장소 | 목적 계약·필드 | 자료 방식 | 목적 설명 | 원본 근거 |
|---|---|---|---|---|---|---|
| Record Writer | StoreResult.store_decisions | Session Store | SessionStore.answer_records | write_decisions | 슬롯별 저장 결정 자료를 응답 기록 반영의 입력으로 전달한다. 값의 직접 복사 관계가 아니며 이 프로젝트에서 반영 동작을 실행하지 않는다. | work/contracts/components/session_store/state.fields.yaml#/nodes/~1properties~1answer_records |
| Dialogue Planner | PlannerOutput.progress_record_update | Session Store | SessionStore.progress_record | write_update | 진행 기록 갱신 자료를 전달한다. 실제 상태 변경을 계산하지 않는다. | work/contracts/components/session_store/state.fields.yaml#/nodes/~1properties~1progress_record |
| Dialogue Planner | PlannerOutput.planner_record_update | Session Store | SessionStore.planner_record | write_update | 계획 기록 갱신 자료를 전달한다. | work/contracts/components/session_store/state.fields.yaml#/nodes/~1properties~1planner_record |
| Orchestrator | OrchestratorOutput.session_info_created | Session Store | SessionStore.session_info | create_record | 세션 정보 생성 자료를 전달한다. nullable 출력은 생성 자료가 없는 경우를 표현한다. | work/contracts/components/session_store/state.fields.yaml#/nodes/~1properties~1session_info |
| Orchestrator | OrchestratorOutput.log_entry | Session Store | SessionStore.dialogue_log | append_record | 턴 로그 항목을 대화 로그에 기록하기 위한 자료로 전달한다. | work/contracts/components/session_store/state.fields.yaml#/nodes/~1properties~1dialogue_log |
| Result Dispatcher | DispatchOutput.dispatch_record | Session Store | SessionStore.dispatch_log | append_record | 결과 전달 기록 항목을 전달 로그에 기록하기 위한 자료로 전달한다. | work/contracts/components/session_store/state.fields.yaml#/nodes/~1properties~1dispatch_log |
