<!-- 생성물. 직접 고치지 말 것: python3 work/tools/build.py -->

# 전달용 Schema

원본은 `../../work/contracts/`, 탐색은 `../../work/schema.md`.

| 컴포넌트 | 방향 | 계약 | 상태 |
|---|---|---|---|
| Frontend | input | FrontendInput | current |
| Frontend | output | FrontendMessage | current |
| Staff Console | input | StaffConsoleInput | current |
| Staff Console | output | InterventionDecision | current |
| Orchestrator | input | OrchestratorInput | current |
| Orchestrator | output | OrchestratorOutput | current |
| Orchestrator | trace | TurnTrace | current |
| Utterance Parser | input | UtteranceParserInput | current |
| Utterance Parser | output | ParserOutput | current |
| Answer Normalizer | input | AnswerNormalizerInput | current |
| Answer Normalizer | output | NormalizerOutput | current |
| Answer Judge | input | AnswerJudgeInput | current |
| Answer Judge | output | JudgeOutput | current |
| Record Writer | input | RecordWriterInput | current |
| Record Writer | output | StoreResult | current |
| Dialogue Planner | input | DialoguePlannerInput | current |
| Dialogue Planner | output | PlannerOutput | current |
| Response Generator | input | ResponseGeneratorInput | current |
| Response Generator | output | GeneratorOutput | current |
| Result Dispatcher | input | DispatchInput | current |
| Result Dispatcher | output | DispatchOutput | current |
| Question Bank | state | QuestionBank | current |
| Session Store | state | SessionStore | current |
| Session Store | load_request | SessionLoadRequest | proposal |
| Session Store | load_result | SessionLoadResult | proposal |
| Session Store | commit_request | SessionCommitRequest | proposal |
| Session Store | commit_result | SessionCommitResult | proposal |
