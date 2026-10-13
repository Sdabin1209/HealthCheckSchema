<!-- 생성물. 직접 고치지 말 것: python3 work/tools/build.py -->

# Frontend (프론트)

사용자 말을 STT로 글자로 바꿔 보내고, 응답 문장을 TTS로 읽어 준다.

이 문서는 현재 계약 원본에서 생성한 필드 안내다. 업무 실행·정답 판정의 검증 결과가 아니다. 전체 역할은 [구조 설명](../../../docs/architecture.md), 검사 범위는 [검증 방법](../../../docs/validation.md)에 있다.

## input: FrontendInput

계약 상태: current. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.

원본: [Schema](../../contracts/components/frontend/input.schema.json), [의미·근거](../../contracts/components/frontend/input.fields.yaml)

| 필드·분기 경로 | 필수 여부 | 값 제약·참조 | 무슨 값인가 | 왜 필요한가 | 근거 요구사항 |
|---|---|---|---|---|---|
| FrontendInput |  | object; additionalProperties=False | 응답 문장과 턴 실패 신호. | 프론트가 읽어 줄 말과, 실패했을 때 대처할 신호를 받는다. | J2, J3, A5 |
| FrontendInput.response_text | 필수 | anyOf(2분기) | LoRA-B의 응답 문장. 실패했으면 없음. | 프론트가 TTS로 읽을 말. 실패한 턴에는 없고 턴 실패 신호가 온다. | J3, A5, G5 |
| FrontendInput.response_text [anyOf:0] | 해당 분기 | string; minLength=1 |  |  |  |
| FrontendInput.response_text [anyOf:1] | 해당 분기 | null | 없음 | 턴이 실패해 응답 문장이 만들어지지 않았다(J2 Plan 결정에서 실패, J8b LoRA-A에서 실패). 이때 턴 실패 신호가 대신 간다. | J2, J8b |
| FrontendInput.turn_failure_signal | 필수 | anyOf(2분기) | 실패했을 때. | 응답이 오지 않은 까닭과 직원 알림 전달 여부를 알아야 프론트가 사용자에게 대처한다. | J2, J3, J4a |
| FrontendInput.turn_failure_signal [anyOf:0] | 해당 분기 | → TurnFailureSignal |  |  |  |
| FrontendInput.turn_failure_signal [anyOf:0] → TurnFailureSignal | 해당 분기 | object; additionalProperties=False | 처리하기로 한 턴이 실패했을 때. | 응답이 나가지 못하거나 직원 호출이 실패하면 프론트와 직원이 알고 대처해야 한다(J2, J3). | J2, J3, J4a |
| FrontendInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.session_id | 필수 | → SessionId | 어느 세션의 값인지. | 프론트와 직원 화면이 여러 세션을 함께 받으므로, 어느 자리의 턴이 실패해 응답이 오지 않는지 가려야 그 자리에만 대처한다(J2, J3). | J2, J4a |
| FrontendInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.session_id → SessionId | 필수 | string; minLength=1 | 프론트가 정한 세션 식별자. 발급·인증은 API·인증 영역의 일. | 같은 키오스크의 다음 사람과 세션을 나누고, 재접속 때 이어 가기 위해(A3, A5). | A3, A5 |
| FrontendInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.write_committed | 필수 | oneOf(2분기) | 이번 턴의 쓰기가 확정됐는지. | 됨이면 기록은 반영됐고 응답만 못 나간 것이다. 다시 말하게 할지 정한다(J2). | J2, J3, J4a |
| FrontendInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.write_committed [oneOf:0] | 해당 분기 | const="COMMITTED" | 기록은 반영됨 | 기록은 반영됐고 응답만 못 나갔으므로 "다시 말씀해 주세요"(반복 요청)로 같은 말을 다시 들을 수 있다. | J3 |
| FrontendInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.write_committed [oneOf:1] | 해당 분기 | const="NOT_COMMITTED" | 아무것도 반영 안 됨 | 아무것도 반영되지 않았으므로 사용자가 같은 말을 다시 하면 처음처럼 처리된다. | J2, J4a |
| FrontendInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.staff_alert | 필수 | oneOf(3분기) | 직원 알림 전달 결과. | 직원이 오지 않는다는 것을 프론트가 알아야 한다(J3). | J2, J3, J4a |
| FrontendInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.staff_alert [oneOf:0] | 해당 분기 | const="NONE" | 보낼 알림이 없었음 | 보낼 알림이 없었던 실패를 알림 실패와 구분해 프론트가 직원을 따로 부르지 않게 한다. | J2, J4a |
| FrontendInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.staff_alert [oneOf:1] | 해당 분기 | const="DELIVERED" | 보냄 | 응답은 실패했어도 직원은 오고 있다는 것을 프론트가 안다. | J8g |
| FrontendInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.staff_alert [oneOf:2] | 해당 분기 | const="DELIVERY_FAILED" | 못 보냄 | 직원 알림이 가지 못했으므로 프론트가 사용자에게 직원을 직접 찾게 하는 등 대처해야 한다. | J3 |
| FrontendInput.turn_failure_signal [anyOf:1] | 해당 분기 | null | 없음 | 실패 없이 끝난 턴이다(B1, C1). 응답 문장과 턴 실패 신호 중 하나만 차므로, 없음이 "정상으로 끝나 응답을 읽으면 된다"를 뜻한다. | B1, C1 |

## output: FrontendMessage

계약 상태: current. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.

원본: [Schema](../../contracts/components/frontend/output.schema.json), [의미·근거](../../contracts/components/frontend/output.fields.yaml)

| 필드·분기 경로 | 필수 여부 | 값 제약·참조 | 무슨 값인가 | 왜 필요한가 | 근거 요구사항 |
|---|---|---|---|---|---|
| FrontendMessage |  | oneOf(3분기) | 프론트가 LangGraph로 보내는 것 하나. | 프론트에서 오는 턴은 이 셋 중 하나로 시작한다(개입 결정은 사람 개입에서 온다). 사용자가 떠났는지는 프론트가 판단한다. | A1, A2, A4a |
| FrontendMessage [oneOf:0] | 해당 분기 | object; additionalProperties=False | 첫 접속·재접속. | 말 없이 세션을 시작하거나 다시 접속하는 신호다. 첫 질문이나 하던 질문을 듣게 된다. | A1, A3 |
| FrontendMessage [oneOf:0].session_id | 필수 | → SessionId | 어느 세션의 값인지. | 키오스크가 여럿이라 어느 자리에서 온 시작 신호인지 있어야 세션을 찾거나 새로 만든다(9-1절 처리 표의 세션 있음, A1, A3). | A1, A3 |
| FrontendMessage [oneOf:0].session_id → SessionId | 필수 | string; minLength=1 | 프론트가 정한 세션 식별자. 발급·인증은 API·인증 영역의 일. | 같은 키오스크의 다음 사람과 세션을 나누고, 재접속 때 이어 가기 위해(A3, A5). | A3, A5 |
| FrontendMessage [oneOf:0].kind | 필수 | const="SESSION_START" | 세션 시작 신호. | 발화가 없는 신호라 LoRA-A를 부르지 않고 Plan부터 돈다. 이 값이 없으면 빈 발화(I1b)와 구분되지 않아 시작 신호가 "알아듣지 못함"이 된다(A1, A3). | A1, A3 |
| FrontendMessage [oneOf:1] | 해당 분기 | object; additionalProperties=False | 사용자 말(STT 결과). 빈 문자열 가능. | B1 등. 빈 발화는 알아듣지 못함이 된다(I1). | A2, A5, G5, B1, G2 |
| FrontendMessage [oneOf:1].session_id | 필수 | → SessionId | 어느 세션의 값인지. | 같은 말이라도 어느 세션의 답인지에 따라 들어갈 기록이 다르다. 끝난 세션 앞에서 다음 사람이 말해도 앞사람 결과에 섞이지 않게 한다(A5). | A2, A5, G5 |
| FrontendMessage [oneOf:1].session_id → SessionId | 필수 | string; minLength=1 | 프론트가 정한 세션 식별자. 발급·인증은 API·인증 영역의 일. | 같은 키오스크의 다음 사람과 세션을 나누고, 재접속 때 이어 가기 위해(A3, A5). | A3, A5 |
| FrontendMessage [oneOf:1].kind | 필수 | const="UTTERANCE" | 발화. | 발화 갈래만 발화 칸을 담는다. 9-1절 처리 표가 입력 종류로 행을 고르므로, 이 값이 전체 흐름을 돌릴지 Plan만 돌릴지를 정한다(A2). | A2, B1 |
| FrontendMessage [oneOf:1].utterance | 필수 | string | STT가 옮긴 글자. | LoRA-A가 항목을 뽑고, 상태 판정이 위험 표현을 대조하고, LoRA-B가 받아 주는 말을 하는 원문이다. | A2, B1, G2 |
| FrontendMessage [oneOf:2] | 해당 분기 | object; additionalProperties=False | 프론트가 세션을 끝냄(떠남). | 사용자가 떠난 것을 프론트만 알 수 있으므로 신호로 받아 미완료로 마치고 결과를 넘긴다. | A4a, A4b |
| FrontendMessage [oneOf:2].session_id | 필수 | → SessionId | 어느 세션의 값인지. | 떠난 사람의 세션만 미완료로 닫아야 한다. 식별이 없으면 옆 자리의 진행 중인 문진까지 끝난다(A4). | A4a, A4b |
| FrontendMessage [oneOf:2].session_id → SessionId | 필수 | string; minLength=1 | 프론트가 정한 세션 식별자. 발급·인증은 API·인증 영역의 일. | 같은 키오스크의 다음 사람과 세션을 나누고, 재접속 때 이어 가기 위해(A3, A5). | A3, A5 |
| FrontendMessage [oneOf:2].kind | 필수 | const="SESSION_END" | 세션 종료 신호. | 사용자가 떠났다는 신호라 확인하지 않고 바로 미완료로 끝낸다(8-3절 4). 발화와 같은 모양으로 오면 떠남이 답으로 해석된다(A4). | A4a, A4b |

