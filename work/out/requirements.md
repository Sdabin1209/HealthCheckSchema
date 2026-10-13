<!-- 생성물. 직접 고치지 말 것: python3 work/tools/build.py -->

# 요구 결과를 표현할 계약 위치

이 연결표는 요구의 표현 위치를 보여준다. 입력에 대한 실제 정답을 판정하지 않는다.

| 케이스 | 턴 | 요구 결과 | 계약 | 필드 |
|---|---|---|---|---|
| A1 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| A1 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| A2 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| A2 | 1 | expect.LoRA-A | ParserOutput | items |
| A2 | 1 | expect.판정 | JudgeOutput | judgments |
| A2 | 1 | expect.저장 | StoreResult | store_decisions |
| A2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| A2 | 1 | expect.뒤 | SessionStore | (전체 경계) |
| A3 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| A3 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| A4a | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| A4a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| A4a | 1 | expect.결과전달입력 | DispatchInput | (전체 경계) |
| A4b | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| A4b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| A5 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| A5 | 1 | expect.응답 | FrontendInput | response_text |
| A6 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| A6 | 1 | expect.응답 | FrontendInput | response_text |
| B1 | 1 | expect.LoRA-A | ParserOutput | items |
| B1 | 1 | expect.판정 | JudgeOutput | judgments |
| B1 | 1 | expect.저장 | StoreResult | store_decisions |
| B1 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B1 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| B2 | 1 | expect.LoRA-A | ParserOutput | items |
| B2 | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| B2 | 1 | expect.판정 | JudgeOutput | judgments |
| B2 | 1 | expect.저장 | StoreResult | store_decisions |
| B2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B2 | 1 | expect.문장재료 | Directive | sentence_materials |
| B3a | 1 | expect.LoRA-A | ParserOutput | items |
| B3a | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| B3a | 1 | expect.판정 | JudgeOutput | judgments |
| B3a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B3b | 1 | expect.LoRA-A | ParserOutput | items |
| B3b | 1 | expect.판정 | JudgeOutput | judgments |
| B3b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B4 | 1 | expect.LoRA-A | ParserOutput | items |
| B4 | 1 | expect.판정 | JudgeOutput | judgments |
| B4 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B5 | 1 | expect.LoRA-A | ParserOutput | items |
| B5 | 1 | expect.판정 | JudgeOutput | judgments |
| B5 | 1 | expect.저장 | StoreResult | store_decisions |
| B5 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B6 | 1 | expect.LoRA-A | ParserOutput | items |
| B6 | 1 | expect.판정 | JudgeOutput | judgments |
| B6 | 1 | expect.저장 | StoreResult | store_decisions |
| B6 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B7a | 1 | expect.LoRA-A | ParserOutput | items |
| B7a | 1 | expect.판정 | JudgeOutput | judgments |
| B7a | 1 | expect.저장 | StoreResult | store_decisions |
| B7a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B7b | 1 | expect.LoRA-A | ParserOutput | items |
| B7b | 1 | expect.판정 | JudgeOutput | judgments |
| B7b | 1 | expect.저장 | StoreResult | store_decisions |
| B7b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B8a | 1 | expect.LoRA-A | ParserOutput | items |
| B8a | 1 | expect.판정 | JudgeOutput | judgments |
| B8a | 1 | expect.저장 | StoreResult | store_decisions |
| B8a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B8a | 1 | expect.문장재료 | Directive | sentence_materials |
| B8b | 1 | expect.LoRA-A | ParserOutput | items |
| B8b | 1 | expect.판정 | JudgeOutput | judgments |
| B8b | 1 | expect.저장 | StoreResult | store_decisions |
| B8b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B9 | 1 | expect.LoRA-A | ParserOutput | items |
| B9 | 1 | expect.판정 | JudgeOutput | judgments |
| B9 | 1 | expect.저장 | StoreResult | store_decisions |
| B9 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| B10 | 1 | expect.LoRA-A | ParserOutput | items |
| B10 | 1 | expect.판정 | JudgeOutput | judgments |
| B10 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C1 | 1 | expect.LoRA-A | ParserOutput | items |
| C1 | 1 | expect.판정 | JudgeOutput | judgments |
| C1 | 1 | expect.저장 | StoreResult | store_decisions |
| C1 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C1 | 1 | expect.뒤 | SessionStore | (전체 경계) |
| C2 | 1 | expect.LoRA-A | ParserOutput | items |
| C2 | 1 | expect.판정 | JudgeOutput | judgments |
| C2 | 1 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| C2 | 1 | expect.저장 | StoreResult | store_decisions |
| C2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C2 | 1 | expect.뒤 | SessionStore | (전체 경계) |
| C3 | 1 | expect.LoRA-A | ParserOutput | items |
| C3 | 1 | expect.판정 | JudgeOutput | judgments |
| C3 | 1 | expect.저장 | StoreResult | store_decisions |
| C3 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C4a | 1 | expect.LoRA-A | ParserOutput | items |
| C4a | 1 | expect.판정 | JudgeOutput | judgments |
| C4a | 1 | expect.저장 | StoreResult | store_decisions |
| C4a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C4a | 1 | expect.뒤 | SessionStore | (전체 경계) |
| C4b | 1 | expect.LoRA-A | ParserOutput | items |
| C4b | 1 | expect.판정 | JudgeOutput | judgments |
| C4b | 1 | expect.저장 | StoreResult | store_decisions |
| C4b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C4b | 1 | expect.뒤 | SessionStore | (전체 경계) |
| C5 | 1 | expect.LoRA-A | ParserOutput | items |
| C5 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| C5 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C6a | 1 | expect.LoRA-A | ParserOutput | items |
| C6a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| C6a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C6b | 1 | expect.LoRA-A | ParserOutput | items |
| C6b | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| C6b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C6c | 1 | expect.LoRA-A | ParserOutput | items |
| C6c | 1 | expect.판정 | JudgeOutput | judgments |
| C6c | 1 | expect.저장 | StoreResult | store_decisions |
| C6c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C7a | 1 | expect.LoRA-A | ParserOutput | items |
| C7a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| C7a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C7b | 1 | expect.LoRA-A | ParserOutput | items |
| C7b | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| C7b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C8a | 1 | expect.LoRA-A | ParserOutput | items |
| C8a | 1 | expect.판정 | JudgeOutput | judgments |
| C8a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C8a | 1 | expect.뒤 | SessionStore | (전체 경계) |
| C8b | 1 | expect.LoRA-A | ParserOutput | items |
| C8b | 1 | expect.판정 | JudgeOutput | judgments |
| C8b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C8c | 1 | expect.LoRA-A | ParserOutput | items |
| C8c | 1 | expect.판정 | JudgeOutput | judgments |
| C8c | 1 | expect.저장 | StoreResult | store_decisions |
| C8c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C8c | 1 | expect.뒤 | SessionStore | (전체 경계) |
| C8d | 1 | expect.LoRA-A | ParserOutput | items |
| C8d | 1 | expect.판정 | JudgeOutput | judgments |
| C8d | 1 | expect.저장 | StoreResult | store_decisions |
| C8d | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C9a | 1 | expect.LoRA-A | ParserOutput | items |
| C9a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| C9a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C9b | 1 | expect.LoRA-A | ParserOutput | items |
| C9b | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| C9b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C9c | 1 | expect.LoRA-A | ParserOutput | items |
| C9c | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| C9c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C9d | 1 | expect.LoRA-A | ParserOutput | items |
| C9d | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| C9d | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C10 | 1 | expect.LoRA-A | ParserOutput | items |
| C10 | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| C10 | 1 | expect.판정 | JudgeOutput | judgments |
| C10 | 1 | expect.저장 | StoreResult | store_decisions |
| C10 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C10 | 1 | expect.뒤 | SessionStore | (전체 경계) |
| C11 | 1 | expect.LoRA-A | ParserOutput | items |
| C11 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| C11 | 1 | expect.판정 | JudgeOutput | judgments |
| C11 | 1 | expect.저장 | StoreResult | store_decisions |
| C11 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| C11 | 1 | expect.뒤 | SessionStore | (전체 경계) |
| D1a | 1 | expect.LoRA-A | ParserOutput | items |
| D1a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| D1a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| D1b | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| D1b | 1 | expect.LoRA-A | ParserOutput | items |
| D1b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| D1c | 1 | expect.LoRA-A | ParserOutput | items |
| D1c | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| D1c | 1 | expect.판정 | JudgeOutput | judgments |
| D1c | 1 | expect.저장 | StoreResult | store_decisions |
| D1c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| D2 | 1 | expect.LoRA-A | ParserOutput | items |
| D2 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| D2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| D3a | 1 | expect.LoRA-A | ParserOutput | items |
| D3a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| D3a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| D3b | 1 | expect.LoRA-A | ParserOutput | items |
| D3b | 1 | expect.판정 | JudgeOutput | judgments |
| D3b | 1 | expect.저장 | StoreResult | store_decisions |
| D3b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| D3c | 1 | expect.LoRA-A | ParserOutput | items |
| D3c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| D3c | 1 | expect.LoRA-B조건 | GeneratorOutput | response_text |
| D4 | 1 | expect.LoRA-A | ParserOutput | items |
| D4 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| D4 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| D5a | 1 | expect.LoRA-A | ParserOutput | items |
| D5a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| D5a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| D5a | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| D5b | 1 | expect.LoRA-A | ParserOutput | items |
| D5b | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| D5b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| E1a | 1 | expect.LoRA-A | ParserOutput | items |
| E1a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| E1a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| E1a | 1 | expect.문장재료 | Directive | sentence_materials |
| E1b | 1 | expect.LoRA-A | ParserOutput | items |
| E1b | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| E1b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| E1b | 1 | expect.문장재료 | Directive | sentence_materials |
| E1c | 1 | expect.LoRA-A | ParserOutput | items |
| E1c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| E2 | 1 | expect.LoRA-A | ParserOutput | items |
| E2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| E2 | 1 | expect.문장재료 | Directive | sentence_materials |
| E3a | 1 | expect.LoRA-A | ParserOutput | items |
| E3a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| E3a | 1 | expect.문장재료 | Directive | sentence_materials |
| E3b | 1 | expect.LoRA-A | ParserOutput | items |
| E3b | 1 | expect.판정 | JudgeOutput | judgments |
| E3b | 1 | expect.저장 | StoreResult | store_decisions |
| E3b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| E4 | 1 | expect.LoRA-A | ParserOutput | items |
| E4 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| E4 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| E4 | 1 | expect.LoRA-B조건 | GeneratorOutput | response_text |
| E5a | 1 | expect.LoRA-A | ParserOutput | items |
| E5a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| E5a | 1 | expect.판정 | JudgeOutput | judgments |
| E5a | 1 | expect.저장 | StoreResult | store_decisions |
| E5a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| F1 | 1 | expect.LoRA-A | ParserOutput | items |
| F1 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| F1 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| F1 | 1 | expect.사람개입입력 | StaffConsoleInput | (전체 경계) |
| F2 | 1 | expect.LoRA-A | ParserOutput | items |
| F2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| F3 | 1 | expect.LoRA-A | ParserOutput | items |
| F3 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| F3 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| F4 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| F4 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| F4 | 1 | expect.결과전달입력 | DispatchInput | (전체 경계) |
| G1 | 1 | expect.LoRA-A | ParserOutput | items |
| G1 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| G1 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| G1 | 1 | expect.LoRA-B조건 | GeneratorOutput | response_text |
| G1 | 1 | expect.사람개입입력 | StaffConsoleInput | (전체 경계) |
| G2 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| G2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| G3 | 1 | expect.LoRA-A | ParserOutput | items |
| G3 | 1 | expect.판정 | JudgeOutput | judgments |
| G3 | 1 | expect.저장 | StoreResult | store_decisions |
| G3 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| G4 | 1 | expect.LoRA-A | ParserOutput | items |
| G4 | 1 | expect.판정 | JudgeOutput | judgments |
| G4 | 1 | expect.저장 | StoreResult | store_decisions |
| G4 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| G5 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| G5 | 1 | expect.응답 | FrontendInput | response_text |
| G6a | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| G6a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| G6b | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| G6b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| G7 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| G7 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| G7 | 1 | expect.결과전달입력 | DispatchInput | (전체 경계) |
| G8a | 1 | expect.LoRA-A | ParserOutput | items |
| G8a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| G8b | 1 | expect.LoRA-A | ParserOutput | items |
| G8b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| G8b | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| G9 | 1 | expect.LoRA-A | ParserOutput | items |
| G9 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| G9 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| G10 | 1 | expect.LoRA-A | ParserOutput | items |
| G10 | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| G10 | 1 | expect.판정 | JudgeOutput | judgments |
| G10 | 1 | expect.저장 | StoreResult | store_decisions |
| G10 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| G10 | 1 | expect.뒤 | SessionStore | (전체 경계) |
| G10 | 2 | expect.LoRA-A | ParserOutput | items |
| G10 | 2 | expect.판정 | JudgeOutput | judgments |
| G10 | 2 | expect.저장 | StoreResult | store_decisions |
| G10 | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| G10 | 2 | expect.뒤 | SessionStore | (전체 경계) |
| H1 | 1 | expect.LoRA-A | ParserOutput | items |
| H1 | 1 | expect.판정 | JudgeOutput | judgments |
| H1 | 1 | expect.저장 | StoreResult | store_decisions |
| H1 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| H2 | 1 | expect.LoRA-A | ParserOutput | items |
| H2 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| H2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| H2 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| H2 | 1 | expect.결과전달입력 | DispatchInput | (전체 경계) |
| H3a | 1 | expect.LoRA-A | ParserOutput | items |
| H3a | 1 | expect.판정 | JudgeOutput | judgments |
| H3a | 1 | expect.저장 | StoreResult | store_decisions |
| H3a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| H3b | 1 | expect.LoRA-A | ParserOutput | items |
| H3b | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| H3b | 1 | expect.판정 | JudgeOutput | judgments |
| H3b | 1 | expect.저장 | StoreResult | store_decisions |
| H3b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| H3b | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| H3c | 1 | expect.LoRA-A | ParserOutput | items |
| H3c | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| H3c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| H3c | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| H3d | 1 | expect.LoRA-A | ParserOutput | items |
| H3d | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| H3d | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| H3d | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| H3d | 3 | expect.LoRA-A | ParserOutput | items |
| H3d | 3 | expect.Plan | PlannerOutput | (전체 경계) |
| H3d | 3 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| H3e | 1 | expect.LoRA-A | ParserOutput | items |
| H3e | 1 | expect.판정 | JudgeOutput | judgments |
| H3e | 1 | expect.저장 | StoreResult | store_decisions |
| H3e | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| H3e | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| H4 | 1 | expect.LoRA-A | ParserOutput | items |
| H4 | 1 | expect.판정 | JudgeOutput | judgments |
| H4 | 1 | expect.저장 | StoreResult | store_decisions |
| H4 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| H4 | 1 | expect.뒤 | SessionStore | (전체 경계) |
| H4 | 2 | expect.LoRA-A | ParserOutput | items |
| H4 | 2 | expect.발화판정 | JudgeOutput | utterance_judgment |
| H4 | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| H4 | 2 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| H4 | 2 | expect.결과전달입력 | DispatchInput | (전체 경계) |
| H4 | 2 | expect.전달기록 | DispatchRecord | (전체 경계) |
| H5a | 1 | expect.LoRA-A | ParserOutput | items |
| H5a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| H5a | 1 | expect.판정 | JudgeOutput | judgments |
| H5a | 1 | expect.저장 | StoreResult | store_decisions |
| H5a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| H5a | 1 | expect.Plan기록 | PlannerOutput | planner_record_update |
| H5b | 1 | expect.LoRA-A | ParserOutput | items |
| H5b | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| H5b | 1 | expect.판정 | JudgeOutput | judgments |
| H5b | 1 | expect.저장 | StoreResult | store_decisions |
| H5b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| H5b | 1 | expect.Plan기록 | PlannerOutput | planner_record_update |
| I1a | 1 | expect.LoRA-A | ParserOutput | items |
| I1a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| I1a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| I1b | 1 | expect.LoRA-A | ParserOutput | items |
| I1b | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| I1b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K1 | 1 | expect.LoRA-A | ParserOutput | items |
| K1 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| K1 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K1 | 1 | expect.LoRA-B조건 | GeneratorOutput | response_text |
| K2 | 1 | expect.LoRA-A | ParserOutput | items |
| K2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K2 | 1 | expect.LoRA-B조건 | GeneratorOutput | response_text |
| K3 | 1 | expect.LoRA-A | ParserOutput | items |
| K3 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K4 | 1 | expect.LoRA-A | ParserOutput | items |
| K4 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| K4 | 1 | expect.판정 | JudgeOutput | judgments |
| K4 | 1 | expect.저장 | StoreResult | store_decisions |
| K4 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K4 | 1 | expect.LoRA-B조건 | GeneratorOutput | response_text |
| K5 | 1 | expect.LoRA-A | ParserOutput | items |
| K5 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| K5 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K5 | 1 | expect.LoRA-B조건 | GeneratorOutput | response_text |
| K6 | 1 | expect.LoRA-A | ParserOutput | items |
| K6 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K7 | 1 | expect.LoRA-A | ParserOutput | items |
| K7 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K7 | 1 | expect.LoRA-B조건 | GeneratorOutput | response_text |
| K8 | 1 | expect.LoRA-A | ParserOutput | items |
| K8 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K8 | 1 | expect.LoRA-B조건 | GeneratorOutput | response_text |
| K9a | 1 | expect.LoRA-A | ParserOutput | items |
| K9a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K9b | 1 | expect.LoRA-A | ParserOutput | items |
| K9b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K9c | 1 | expect.LoRA-A | ParserOutput | items |
| K9c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| K9d | 1 | expect.LoRA-A | ParserOutput | items |
| K9d | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J1 | 1 | expect.LoRA-A | ParserOutput | items |
| J1 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J1 | 1 | expect.판정 | JudgeOutput | judgments |
| J1 | 1 | expect.저장 | StoreResult | store_decisions |
| J1 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J2 | 1 | expect.LoRA-A | ParserOutput | items |
| J2 | 1 | expect.판정 | JudgeOutput | judgments |
| J2 | 1 | expect.저장 | StoreResult | store_decisions |
| J2 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J2 | 1 | expect.뒤 | SessionStore | (전체 경계) |
| J3 | 1 | expect.LoRA-A | ParserOutput | items |
| J3 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J3 | 1 | expect.응답 | FrontendInput | response_text |
| J3 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J4a | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J4a | 1 | expect.뒤 | SessionStore | (전체 경계) |
| J4b | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J5 | 1 | expect.LoRA-A | ParserOutput | items |
| J5 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J5 | 1 | expect.전달기록 | DispatchRecord | (전체 경계) |
| J7a | 1 | expect.LoRA-A | ParserOutput | items |
| J7a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| J7a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J7b | 1 | expect.LoRA-A | ParserOutput | items |
| J7b | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| J7b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J7c | 1 | expect.LoRA-A | ParserOutput | items |
| J7c | 1 | expect.판정 | JudgeOutput | judgments |
| J7c | 1 | expect.저장 | StoreResult | store_decisions |
| J7c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J7c | 1 | expect.LoRA-B | GeneratorOutput | (전체 경계) |
| J8a | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J8a | 1 | expect.응답 | FrontendInput | response_text |
| J8a | 1 | expect.뒤 | SessionStore | (전체 경계) |
| J8b | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J8b | 1 | expect.응답 | FrontendInput | response_text |
| J8b | 1 | expect.뒤 | SessionStore | (전체 경계) |
| J8c | 1 | expect.LoRA-A | ParserOutput | items |
| J8c | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J8c | 1 | expect.응답 | FrontendInput | response_text |
| J8c | 1 | expect.뒤 | SessionStore | (전체 경계) |
| J8d | 1 | expect.LoRA-A | ParserOutput | items |
| J8d | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J8d | 1 | expect.응답 | FrontendInput | response_text |
| J8d | 1 | expect.뒤 | SessionStore | (전체 경계) |
| J8e | 1 | expect.LoRA-A | ParserOutput | items |
| J8e | 1 | expect.판정 | JudgeOutput | judgments |
| J8e | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J8e | 1 | expect.응답 | FrontendInput | response_text |
| J8e | 1 | expect.뒤 | SessionStore | (전체 경계) |
| J8f | 1 | expect.LoRA-A | ParserOutput | items |
| J8f | 1 | expect.판정 | JudgeOutput | judgments |
| J8f | 1 | expect.저장 | StoreResult | store_decisions |
| J8f | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J8f | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J8f | 1 | expect.응답 | FrontendInput | response_text |
| J8f | 1 | expect.뒤 | SessionStore | (전체 경계) |
| J8g | 1 | expect.LoRA-A | ParserOutput | items |
| J8g | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J8g | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J8g | 1 | expect.응답 | FrontendInput | response_text |
| J8g | 1 | expect.뒤 | SessionStore | (전체 경계) |
| J8h | 1 | expect.LoRA-A | ParserOutput | items |
| J8h | 1 | expect.판정 | JudgeOutput | judgments |
| J8h | 1 | expect.저장 | StoreResult | store_decisions |
| J8h | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J8h | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| J8h | 1 | expect.뒤 | SessionStore | (전체 경계) |
| J7d | 1 | expect.LoRA-A | ParserOutput | items |
| J7d | 1 | expect.판정 | JudgeOutput | judgments |
| J7d | 1 | expect.저장 | StoreResult | store_decisions |
| J7d | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J7d | 1 | expect.문장재료 | Directive | sentence_materials |
| J7d | 1 | expect.LoRA-B | GeneratorOutput | (전체 경계) |
| J7e | 1 | expect.LoRA-A | ParserOutput | items |
| J7e | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| J7e | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| J7e | 1 | expect.문장재료 | Directive | sentence_materials |
| J7e | 1 | expect.LoRA-B | GeneratorOutput | (전체 경계) |
| X1 | 1 | expect.LoRA-A | ParserOutput | items |
| X1 | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| X1 | 1 | expect.판정 | JudgeOutput | judgments |
| X1 | 1 | expect.저장 | StoreResult | store_decisions |
| X1 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| X2 | 1 | expect.LoRA-A | ParserOutput | items |
| X2 | 1 | expect.판정 | JudgeOutput | judgments |
| X2 | 1 | expect.저장 | StoreResult | store_decisions |
| X2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| X2 | 1 | expect.뒤 | SessionStore | (전체 경계) |
| X3 | 1 | expect.LoRA-A | ParserOutput | items |
| X3 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| X3 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| X4 | 1 | expect.LoRA-A | ParserOutput | items |
| X4 | 1 | expect.판정 | JudgeOutput | judgments |
| X4 | 1 | expect.저장 | StoreResult | store_decisions |
| X4 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| X5 | 1 | expect.LoRA-A | ParserOutput | items |
| X5 | 1 | expect.판정 | JudgeOutput | judgments |
| X5 | 1 | expect.저장 | StoreResult | store_decisions |
| X5 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| X5 | 2 | expect.LoRA-A | ParserOutput | items |
| X5 | 2 | expect.판정 | JudgeOutput | judgments |
| X5 | 2 | expect.저장 | StoreResult | store_decisions |
| X5 | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| X6 | 1 | expect.LoRA-A | ParserOutput | items |
| X6 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| X7 | 1 | expect.LoRA-A | ParserOutput | items |
| X7 | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| X7 | 1 | expect.판정 | JudgeOutput | judgments |
| X7 | 1 | expect.저장 | StoreResult | store_decisions |
| X7 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| X8 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| X8 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| X9 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| X9 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N1a | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| N1a | 1 | expect.LoRA-A | ParserOutput | items |
| N1a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| N1a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N1b | 1 | expect.LoRA-A | ParserOutput | items |
| N1b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N1c | 1 | expect.LoRA-A | ParserOutput | items |
| N1c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N2a | 1 | expect.LoRA-A | ParserOutput | items |
| N2a | 1 | expect.판정 | JudgeOutput | judgments |
| N2a | 1 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| N2a | 1 | expect.저장 | StoreResult | store_decisions |
| N2a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N2b | 1 | expect.LoRA-A | ParserOutput | items |
| N2b | 1 | expect.판정 | JudgeOutput | judgments |
| N2b | 1 | expect.저장 | StoreResult | store_decisions |
| N2b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N3a | 1 | expect.LoRA-A | ParserOutput | items |
| N3a | 1 | expect.판정 | JudgeOutput | judgments |
| N3a | 1 | expect.저장 | StoreResult | store_decisions |
| N3a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N3b | 1 | expect.LoRA-A | ParserOutput | items |
| N3b | 1 | expect.판정 | JudgeOutput | judgments |
| N3b | 1 | expect.저장 | StoreResult | store_decisions |
| N3b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N4 | 1 | expect.LoRA-A | ParserOutput | items |
| N4 | 1 | expect.판정 | JudgeOutput | judgments |
| N4 | 1 | expect.저장 | StoreResult | store_decisions |
| N4 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N5a | 1 | expect.LoRA-A | ParserOutput | items |
| N5a | 1 | expect.판정 | JudgeOutput | judgments |
| N5a | 1 | expect.저장 | StoreResult | store_decisions |
| N5a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N5b | 1 | expect.LoRA-A | ParserOutput | items |
| N5b | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| N5b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N6 | 1 | expect.LoRA-A | ParserOutput | items |
| N6 | 1 | expect.판정 | JudgeOutput | judgments |
| N6 | 1 | expect.저장 | StoreResult | store_decisions |
| N6 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N6 | 1 | expect.뒤 | SessionStore | (전체 경계) |
| N7a | 1 | expect.LoRA-A | ParserOutput | items |
| N7a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| N7a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N7b | 1 | expect.LoRA-A | ParserOutput | items |
| N7b | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| N7b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N7c | 1 | expect.LoRA-A | ParserOutput | items |
| N7c | 1 | expect.판정 | JudgeOutput | judgments |
| N7c | 1 | expect.저장 | StoreResult | store_decisions |
| N7c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N8a | 1 | expect.LoRA-A | ParserOutput | items |
| N8a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| N8a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N8b | 1 | expect.LoRA-A | ParserOutput | items |
| N8b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N8b | 2 | expect.LoRA-A | ParserOutput | items |
| N8b | 2 | expect.발화판정 | JudgeOutput | utterance_judgment |
| N8b | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| N9 | 1 | expect.LoRA-A | ParserOutput | items |
| N9 | 1 | expect.판정 | JudgeOutput | judgments |
| N9 | 1 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| N9 | 1 | expect.저장 | StoreResult | store_decisions |
| N9 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N10 | 1 | expect.LoRA-A | ParserOutput | items |
| N10 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N10 | 2 | expect.LoRA-A | ParserOutput | items |
| N10 | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| N10 | 3 | expect.LoRA-A | ParserOutput | items |
| N10 | 3 | expect.판정 | JudgeOutput | judgments |
| N10 | 3 | expect.Plan | PlannerOutput | (전체 경계) |
| N11a | 1 | expect.LoRA-A | ParserOutput | items |
| N11a | 1 | expect.판정 | JudgeOutput | judgments |
| N11a | 1 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| N11a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N11b | 1 | expect.LoRA-A | ParserOutput | items |
| N11b | 1 | expect.판정 | JudgeOutput | judgments |
| N11b | 1 | expect.저장 | StoreResult | store_decisions |
| N11b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N11c | 1 | expect.LoRA-A | ParserOutput | items |
| N11c | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| N11c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N12 | 1 | expect.LoRA-A | ParserOutput | items |
| N12 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N13 | 1 | expect.LoRA-A | ParserOutput | items |
| N13 | 1 | expect.판정 | JudgeOutput | judgments |
| N13 | 1 | expect.저장 | StoreResult | store_decisions |
| N13 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N13 | 2 | expect.LoRA-A | ParserOutput | items |
| N13 | 2 | expect.판정 | JudgeOutput | judgments |
| N13 | 2 | expect.저장 | StoreResult | store_decisions |
| N13 | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| N14 | 1 | expect.LoRA-A | ParserOutput | items |
| N14 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| N14 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N15 | 1 | expect.LoRA-A | ParserOutput | items |
| N15 | 1 | expect.판정 | JudgeOutput | judgments |
| N15 | 1 | expect.저장 | StoreResult | store_decisions |
| N15 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N15 | 2 | expect.LoRA-A | ParserOutput | items |
| N15 | 2 | expect.판정 | JudgeOutput | judgments |
| N15 | 2 | expect.저장 | StoreResult | store_decisions |
| N15 | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| N16 | 1 | expect.LoRA-A | ParserOutput | items |
| N16 | 1 | expect.판정 | JudgeOutput | judgments |
| N16 | 1 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| N16 | 1 | expect.저장 | StoreResult | store_decisions |
| N16 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| N17 | 1 | expect.LoRA-A | ParserOutput | items |
| N17 | 1 | expect.판정 | JudgeOutput | judgments |
| N17 | 1 | expect.저장 | StoreResult | store_decisions |
| N17 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S1a | 1 | expect.LoRA-A | ParserOutput | items |
| S1a | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| S1a | 1 | expect.판정 | JudgeOutput | judgments |
| S1a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| S1a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S1b | 1 | expect.LoRA-A | ParserOutput | items |
| S1b | 1 | expect.판정 | JudgeOutput | judgments |
| S1b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S1c | 1 | expect.LoRA-A | ParserOutput | items |
| S1c | 1 | expect.판정 | JudgeOutput | judgments |
| S1c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S1c | 1 | expect.뒤 | SessionStore | (전체 경계) |
| S1d | 1 | expect.LoRA-A | ParserOutput | items |
| S1d | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| S1d | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S1e | 1 | expect.LoRA-A | ParserOutput | items |
| S1e | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| S1e | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S2a | 1 | expect.LoRA-A | ParserOutput | items |
| S2a | 1 | expect.판정 | JudgeOutput | judgments |
| S2a | 1 | expect.저장 | StoreResult | store_decisions |
| S2a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S2b | 1 | expect.LoRA-A | ParserOutput | items |
| S2b | 1 | expect.판정 | JudgeOutput | judgments |
| S2b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S2c | 1 | expect.LoRA-A | ParserOutput | items |
| S2c | 1 | expect.판정 | JudgeOutput | judgments |
| S2c | 1 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| S2c | 1 | expect.저장 | StoreResult | store_decisions |
| S2c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S2c | 1 | expect.뒤 | SessionStore | (전체 경계) |
| S2d | 1 | expect.LoRA-A | ParserOutput | items |
| S2d | 1 | expect.판정 | JudgeOutput | judgments |
| S2d | 1 | expect.저장 | StoreResult | store_decisions |
| S2d | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S2e | 1 | expect.LoRA-A | ParserOutput | items |
| S2e | 1 | expect.판정 | JudgeOutput | judgments |
| S2e | 1 | expect.저장 | StoreResult | store_decisions |
| S2e | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S2e | 2 | expect.LoRA-A | ParserOutput | items |
| S2e | 2 | expect.판정 | JudgeOutput | judgments |
| S2e | 2 | expect.저장 | StoreResult | store_decisions |
| S2e | 2 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| S2e | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| S3d | 1 | expect.LoRA-A | ParserOutput | items |
| S3d | 1 | expect.판정 | JudgeOutput | judgments |
| S3d | 1 | expect.저장 | StoreResult | store_decisions |
| S3d | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S3a | 1 | expect.LoRA-A | ParserOutput | items |
| S3a | 1 | expect.판정 | JudgeOutput | judgments |
| S3a | 1 | expect.저장 | StoreResult | store_decisions |
| S3a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S3b | 1 | expect.LoRA-A | ParserOutput | items |
| S3b | 1 | expect.판정 | JudgeOutput | judgments |
| S3b | 1 | expect.저장 | StoreResult | store_decisions |
| S3b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S3c | 1 | expect.LoRA-A | ParserOutput | items |
| S3c | 1 | expect.판정 | JudgeOutput | judgments |
| S3c | 1 | expect.저장 | StoreResult | store_decisions |
| S3c | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| S3c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S4a | 1 | expect.판정 | JudgeOutput | judgments |
| S4a | 1 | expect.저장 | StoreResult | store_decisions |
| S4a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S4b | 1 | expect.LoRA-A | ParserOutput | items |
| S4b | 1 | expect.판정 | JudgeOutput | judgments |
| S4b | 1 | expect.저장 | StoreResult | store_decisions |
| S4b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S4c | 1 | expect.판정 | JudgeOutput | judgments |
| S4c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S4d | 1 | expect.판정 | JudgeOutput | judgments |
| S4d | 1 | expect.저장 | StoreResult | store_decisions |
| S4d | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S4e | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| S4e | 1 | expect.판정 | JudgeOutput | judgments |
| S4e | 1 | expect.저장 | StoreResult | store_decisions |
| S4e | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S4f | 1 | expect.판정 | JudgeOutput | judgments |
| S4f | 1 | expect.저장 | StoreResult | store_decisions |
| S4f | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S5a | 1 | expect.LoRA-A | ParserOutput | items |
| S5a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S5a | 2 | expect.LoRA-A | ParserOutput | items |
| S5a | 2 | expect.판정 | JudgeOutput | judgments |
| S5a | 2 | expect.저장 | StoreResult | store_decisions |
| S5a | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| S5a | 3 | expect.LoRA-A | ParserOutput | items |
| S5a | 3 | expect.Plan | PlannerOutput | (전체 경계) |
| S6a | 1 | expect.LoRA-A | ParserOutput | items |
| S6a | 1 | expect.판정 | JudgeOutput | judgments |
| S6a | 1 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| S6a | 1 | expect.저장 | StoreResult | store_decisions |
| S6a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S6a | 1 | expect.뒤 | SessionStore | (전체 경계) |
| S6b | 1 | expect.LoRA-A | ParserOutput | items |
| S6b | 1 | expect.판정 | JudgeOutput | judgments |
| S6b | 1 | expect.저장 | StoreResult | store_decisions |
| S6b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S6c | 1 | expect.LoRA-A | ParserOutput | items |
| S6c | 1 | expect.판정 | JudgeOutput | judgments |
| S6c | 1 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| S6c | 1 | expect.저장 | StoreResult | store_decisions |
| S6c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S6c | 1 | expect.뒤 | SessionStore | (전체 경계) |
| S7a | 1 | expect.LoRA-A | ParserOutput | items |
| S7a | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| S7a | 1 | expect.판정 | JudgeOutput | judgments |
| S7a | 1 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| S7a | 1 | expect.저장 | StoreResult | store_decisions |
| S7a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S7b | 1 | expect.판정 | JudgeOutput | judgments |
| S7b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S7c | 1 | expect.판정 | JudgeOutput | judgments |
| S7c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S8a | 1 | expect.LoRA-A | ParserOutput | items |
| S8a | 1 | expect.판정 | JudgeOutput | judgments |
| S8a | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| S8a | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S8b | 1 | expect.LoRA-A | ParserOutput | items |
| S8b | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| S8b | 1 | expect.판정 | JudgeOutput | judgments |
| S8b | 1 | expect.저장 | StoreResult | store_decisions |
| S8b | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S8c | 1 | expect.LoRA-A | ParserOutput | items |
| S8c | 1 | expect.판정 | JudgeOutput | judgments |
| S8c | 1 | expect.저장 | StoreResult | store_decisions |
| S8c | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S8d | 1 | expect.LoRA-A | ParserOutput | items |
| S8d | 1 | expect.판정 | JudgeOutput | judgments |
| S8d | 1 | expect.저장 | StoreResult | store_decisions |
| S8d | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S8d | 1 | expect.Plan기록 | PlannerOutput | planner_record_update |
| S8d | 2 | expect.LoRA-A | ParserOutput | items |
| S8d | 2 | expect.판정 | JudgeOutput | judgments |
| S8d | 2 | expect.저장 | StoreResult | store_decisions |
| S8d | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| S8d | 3 | expect.LoRA-A | ParserOutput | items |
| S8d | 3 | expect.판정 | JudgeOutput | judgments |
| S8d | 3 | expect.Plan | PlannerOutput | (전체 경계) |
| S8e | 1 | expect.LoRA-A | ParserOutput | items |
| S8e | 1 | expect.판정 | JudgeOutput | judgments |
| S8e | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S8e | 1 | expect.Plan기록 | PlannerOutput | planner_record_update |
| S8f | 1 | expect.LoRA-A | ParserOutput | items |
| S8f | 1 | expect.판정 | JudgeOutput | judgments |
| S8f | 1 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| S8f | 1 | expect.저장 | StoreResult | store_decisions |
| S8f | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S8g | 1 | expect.LoRA-A | ParserOutput | items |
| S8g | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| S8g | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S8h | 1 | expect.LoRA-A | ParserOutput | items |
| S8h | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| S8h | 2 | expect.LoRA-A | ParserOutput | items |
| S8h | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| S8h | 3 | expect.LoRA-A | ParserOutput | items |
| S8h | 3 | expect.Plan | PlannerOutput | (전체 경계) |
| S8i | 1 | expect.LoRA-A | ParserOutput | items |
| S8i | 1 | expect.판정 | JudgeOutput | judgments |
| S8i | 1 | expect.저장 | StoreResult | store_decisions |
| S8i | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R1 | 1 | expect.LoRA-A | ParserOutput | items |
| R1 | 1 | expect.판정 | JudgeOutput | judgments |
| R1 | 1 | expect.저장 | StoreResult | store_decisions |
| R1 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R2 | 1 | expect.LoRA-A | ParserOutput | items |
| R2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R2 | 2 | expect.LoRA-A | ParserOutput | items |
| R2 | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| R3 | 1 | expect.LoRA-A | ParserOutput | items |
| R3 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R4 | 1 | expect.LoRA-A | ParserOutput | items |
| R4 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R4 | 2 | expect.LoRA-A | ParserOutput | items |
| R4 | 2 | expect.판정 | JudgeOutput | judgments |
| R4 | 2 | expect.저장 | StoreResult | store_decisions |
| R4 | 2 | expect.Plan | PlannerOutput | (전체 경계) |
| R5 | 1 | expect.LoRA-A | ParserOutput | items |
| R5 | 1 | expect.판정 | JudgeOutput | judgments |
| R5 | 1 | expect.무효화대상문항 | JudgeOutput | invalidated_questions |
| R5 | 1 | expect.저장 | StoreResult | store_decisions |
| R5 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R6 | 1 | expect.LoRA-A | ParserOutput | items |
| R6 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R7 | 1 | expect.판정 | JudgeOutput | judgments |
| R7 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| R7 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R8 | 1 | expect.LoRA-A | ParserOutput | items |
| R8 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R8 | 1 | expect.Plan기록 | PlannerOutput | planner_record_update |
| R9 | 1 | expect.LoRA-A | ParserOutput | items |
| R9 | 1 | expect.판정 | JudgeOutput | judgments |
| R9 | 1 | expect.저장 | StoreResult | store_decisions |
| R9 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| R9 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R10 | 1 | expect.LoRA-A | ParserOutput | items |
| R10 | 1 | expect.판정 | JudgeOutput | judgments |
| R10 | 1 | expect.저장 | StoreResult | store_decisions |
| R10 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R11 | 1 | expect.LoRA-A | ParserOutput | items |
| R11 | 1 | expect.판정 | JudgeOutput | judgments |
| R11 | 1 | expect.저장 | StoreResult | store_decisions |
| R11 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R12 | 1 | expect.LoRA-A | ParserOutput | items |
| R12 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R13 | 1 | expect.LoRA-A | ParserOutput | items |
| R13 | 1 | expect.판정 | JudgeOutput | judgments |
| R13 | 1 | expect.저장 | StoreResult | store_decisions |
| R13 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R14 | 1 | expect.LoRA-A | ParserOutput | items |
| R14 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| R14 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R15 | 1 | expect.LoRA-A | ParserOutput | items |
| R15 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R16 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| R16 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R17 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R18 | 1 | expect.LoRA-A | ParserOutput | items |
| R18 | 1 | expect.판정 | JudgeOutput | judgments |
| R18 | 1 | expect.저장 | StoreResult | store_decisions |
| R18 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R19 | 1 | expect.LoRA-A | ParserOutput | items |
| R19 | 1 | expect.판정 | JudgeOutput | judgments |
| R19 | 1 | expect.저장 | StoreResult | store_decisions |
| R19 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R19 | 1 | expect.Plan기록 | PlannerOutput | planner_record_update |
| R20 | 1 | expect.LoRA-A | ParserOutput | items |
| R20 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| R20 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R21 | 1 | expect.LoRA-A | ParserOutput | items |
| R21 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| R21 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| R21 | 1 | expect.LangGraph | OrchestratorOutput | (전체 경계) |
| V1 | 1 | expect.LoRA-A | ParserOutput | items |
| V1 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| V1 | 1 | expect.판정 | JudgeOutput | judgments |
| V1 | 1 | expect.저장 | StoreResult | store_decisions |
| V1 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| V2 | 1 | expect.LoRA-A | ParserOutput | items |
| V2 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| V2 | 1 | expect.판정 | JudgeOutput | judgments |
| V2 | 1 | expect.저장 | StoreResult | store_decisions |
| V2 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| V3 | 1 | expect.LoRA-A | ParserOutput | items |
| V3 | 1 | expect.발화판정 | JudgeOutput | utterance_judgment |
| V3 | 1 | expect.판정 | JudgeOutput | judgments |
| V3 | 1 | expect.저장 | StoreResult | store_decisions |
| V3 | 1 | expect.Plan | PlannerOutput | (전체 경계) |
| T1 | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| T2 | 1 | expect.LoRA-A | ParserOutput | items |
| T2 | 1 | expect.뒤 | SessionStore | (전체 경계) |
| T3 | 1 | expect.문항정의 | QuestionBank | (전체 경계) |
| T4 | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| T5 | 1 | expect.저장요청 | SessionCommitRequest | (전체 경계) |
| T6 | 1 | expect.저장결과 | SessionCommitResult | (전체 경계) |
| T7 | 1 | expect.저장결과 | SessionCommitResult | (전체 경계) |
| T8 | 1 | expect.조회결과 | SessionLoadResult | (전체 경계) |
| T8 | 1 | expect.조회요청 | SessionLoadRequest | (전체 경계) |
| T9 | 1 | expect.정규화 | NormalizerOutput | (전체 경계) |
| T9 | 1 | expect.판정 | JudgeOutput | judgments |
| T10 | 1 | expect.저장결과 | SessionCommitResult | (전체 경계) |
