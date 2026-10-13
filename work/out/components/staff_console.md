<!-- 생성물. 직접 고치지 말 것: python3 work/tools/build.py -->

# Staff Console (사람 개입)

직원·의료진에게 알림을 보여 주고, 그들의 결정(재개·종료)을 보낸다.

이 문서는 현재 계약 원본에서 생성한 필드 안내다. 업무 실행·정답 판정의 검증 결과가 아니다. 전체 역할은 [구조 설명](../../../docs/architecture.md), 검사 범위는 [검증 방법](../../../docs/validation.md)에 있다.

## input: StaffConsoleInput

계약 상태: current. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.

원본: [Schema](../../contracts/components/staff_console/input.schema.json), [의미·근거](../../contracts/components/staff_console/input.fields.yaml)

| 필드·분기 경로 | 필수 여부 | 값 제약·참조 | 무슨 값인가 | 왜 필요한가 | 근거 요구사항 |
|---|---|---|---|---|---|
| StaffConsoleInput |  | object; additionalProperties=False | 직원 알림(세션 식별 포함), 턴 실패 신호, 개입 결정 결과. | 직원 화면이 보여 줄 알림·실패·결정 결과를 한 모양으로 받아, 화면이 컴포넌트 안쪽을 몰라도 되게 한다. | J2, J3, J4a |
| StaffConsoleInput.staff_alert | 필수 | anyOf(2분기) | 세션 식별과 함께. 없으면 없음. | 어느 키오스크로 가야 하는지 알아야 한다. | J3, F1, G1 |
| StaffConsoleInput.staff_alert [anyOf:0] | 해당 분기 | object; additionalProperties=False | 세션과 알림. | 직원 화면은 여러 키오스크의 알림을 받는다. 어느 세션인지 함께 와야 한다. | F1, G1, J3 |
| StaffConsoleInput.staff_alert [anyOf:0].session_id | 필수 | → SessionId | 어느 세션의 값인지. | 직원이 알림을 받고 실제로 걸어가야 하므로, 어느 키오스크로 갈지가 알림에 붙어 있어야 한다(F1, G1). | F1, G1 |
| StaffConsoleInput.staff_alert [anyOf:0].session_id → SessionId | 필수 | string; minLength=1 | 프론트가 정한 세션 식별자. 발급·인증은 API·인증 영역의 일. | 같은 키오스크의 다음 사람과 세션을 나누고, 재접속 때 이어 가기 위해(A3, A5). | A3, A5 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert | 필수 | → StaffAlert | Plan의 직원 알림. | 직원이 무엇 때문에 와야 하는지 알고 온다. | J3, F1, G1 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert | 필수 | object; additionalProperties=False | 직원을 부르는 알림. | 위험·도움 요청·사람 요청에 사람이 와야 한다(G1, F1, F3). | F1, F3, G1, J3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.kind | 필수 | → AlertKind | 알림 종류. | 직원이 위험(바로 가야 함), 도움 요청, 사람 요청 중 무엇인지 보고 우선순위를 정한다. | F1, F3, G1 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.kind → AlertKind | 필수 | oneOf(3분기) | 직원 알림의 까닭. | 직원이 왜 와야 하는지 바로 알게 한다. | F1, F3, G1 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.kind → AlertKind [oneOf:0] | 해당 분기 | const="RISK" | 위험 신호나 즉시 위험 기준 | 직원이 가장 먼저 가야 하는 알림이다. | G1, G2, G3, J3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.kind → AlertKind [oneOf:1] | 해당 분기 | const="CALL_STAFF" | 알아듣지 못함이 이어짐 | 시스템이 사용자를 알아듣지 못해 사람이 도와야 하는 알림이다. | F3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.kind → AlertKind [oneOf:2] | 해당 분기 | const="USER_CALLED_STAFF" | 사용자가 직원을 찾음 | 사용자가 직원을 원한 알림이다. 무엇을 원하는지 근거가 함께 간다. | F1, F2, X8 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons | 필수 | array | 이유들. 도움 요청이면 빈 목록. 위험 신호와 위험 기준이 함께면 둘 다. | 직원이 무엇 때문에 와야 하는지 알고 온다(G1, G3, F1). | F1, F3, G1, G3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] | 배열 항목 | → StaffAlertReason |  |  |  |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason | 배열 항목 | oneOf(3분기) | 직원 알림의 이유 하나. | 직원이 무엇 때문에 와야 하는지 알고 온다. 사람 개입은 문항 정의를 받지 않으므로 이름과 값을 담는다. | G1, G3, F1 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:0] | 해당 분기 | object; additionalProperties=False | 위험한 말. | 위험한 말 때문에 부른 경우 원문을 함께 보내야 직원이 상황을 알고 온다. | G1, G2, G9, J3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:0].kind | 필수 | const="RISK_SIGNAL" | 위험 신호. | 직원이 보는 알림에서 위급한 말로 불린 것인지를 가린다. 이 갈래만 사용자가 한 말 그대로를 근거로 담으므로, 직원이 상황을 말로 먼저 안다(G1, G2). | G1, G2, G9, J3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:0].evidence | 필수 | array; minItems=1 | 원문 표현. | 직원이 사용자가 한 위급한 말을 원문으로 보고 대처한다. | G1, G2, G9, J3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:0].evidence[] | 배열 항목 | → SourceText |  |  |  |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:0].evidence[] → SourceText | 배열 항목 | string; minLength=1 | 사용자 발화에서 그대로 옮긴 부분. | 판정 근거를 사람이 확인하고, 애매한 값을 사용자 말 그대로 짚어 되묻기 위해(B3, G1). | F1, G1, G8a |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1] | 해당 분기 | object; additionalProperties=False | 위험한 답. | G3. 직원이 "죽고 싶은 생각: 예"처럼 무슨 답인지 안다. | G3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].kind | 필수 | const="RISK_RULE" | 위험 기준. | 답 자체가 위험 기준에 걸려 불린 것인지를 가린다. 이 갈래만 슬롯·문항 이름·값을 담아 직원이 "죽고 싶은 생각: 예"처럼 무슨 답인지 읽는다(G3). | G3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target | 필수 | array; minItems=1 | 해당 답들. | 직원이 어떤 답 때문에 불렸는지 보고 대처한다. | G3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[] | 배열 항목 | object; additionalProperties=False | 슬롯·이름·값. | 직원이 "죽고 싶은 생각: 예"처럼 무슨 답인지 읽는다(G3). | G3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].slot | 필수 | → SlotRef | 위험 기준을 충족한 값이 저장된 문항·반복 행·슬롯의 식별자. | 어느 문항의 어느 칸 답인지 직원 기록과 맞출 수 있게 ID를 함께 둔다. | G3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].question_name | 필수 | string; minLength=1 | 이름. | 사람 개입은 문항 정의를 받지 않으므로 직원이 읽을 문항 이름을 담아 보낸다. | G3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].value | 필수 | → Value | 판정의 이번 값. | 직원이 "죽고 싶은 생각: 예"처럼 무슨 답인지 바로 읽는다. | G3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].value → Value | 필수 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].value → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].value → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].value → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].value → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].value → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].value → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].value → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].value → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:1].target[].value → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:2] | 해당 분기 | object; additionalProperties=False | 직원 요청. | F1, F2. 직원이 무엇을 원하는지 알고 온다("처음부터 다시 할래요"). | F1, F2, R3, X8 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:2].kind | 필수 | const="USER_CALLED_STAFF" | 사람 요청. | 사용자가 직원을 찾아 불린 것인지를 가린다. 위험으로 불린 알림과 달라야 직원이 급한 정도를 판단하고 문진이 멈췄는지 아닌지를 안다(F1, F2). | F1, F2, R3, X8 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:2].evidence | 필수 | array; minItems=1 | 요청의 원문 표현. | 직원이 사용자가 무엇을 원하는지("처음부터 다시 할래요") 알고 온다. | F1, F2, R3 |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:2].evidence[] | 배열 항목 | → SourceText |  |  |  |
| StaffConsoleInput.staff_alert [anyOf:0].staff_alert → StaffAlert.reasons[] → StaffAlertReason [oneOf:2].evidence[] → SourceText | 배열 항목 | string; minLength=1 | 사용자 발화에서 그대로 옮긴 부분. | 판정 근거를 사람이 확인하고, 애매한 값을 사용자 말 그대로 짚어 되묻기 위해(B3, G1). | F1, G1, G8a |
| StaffConsoleInput.staff_alert [anyOf:1] | 해당 분기 | null | 없음 | 보낼 직원 알림이 없는 턴이다(J2, J8b). 알림 없이 턴 실패 신호만 가는 경우가 있어 세 칸이 따로 비워진다. | J2, J8b |
| StaffConsoleInput.turn_failure_signal | 필수 | anyOf(2분기) | 어느 세션이든 턴이 실패하면. | 위험 신호가 들어온 턴이 실패해도 직원이 볼 수 있게(J2). | J2, J3, J4a |
| StaffConsoleInput.turn_failure_signal [anyOf:0] | 해당 분기 | → TurnFailureSignal |  |  |  |
| StaffConsoleInput.turn_failure_signal [anyOf:0] → TurnFailureSignal | 해당 분기 | object; additionalProperties=False | 처리하기로 한 턴이 실패했을 때. | 응답이 나가지 못하거나 직원 호출이 실패하면 프론트와 직원이 알고 대처해야 한다(J2, J3). | J2, J3, J4a |
| StaffConsoleInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.session_id | 필수 | → SessionId | 어느 세션의 값인지. | 프론트와 직원 화면이 여러 세션을 함께 받으므로, 어느 자리의 턴이 실패해 응답이 오지 않는지 가려야 그 자리에만 대처한다(J2, J3). | J2, J4a |
| StaffConsoleInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.session_id → SessionId | 필수 | string; minLength=1 | 프론트가 정한 세션 식별자. 발급·인증은 API·인증 영역의 일. | 같은 키오스크의 다음 사람과 세션을 나누고, 재접속 때 이어 가기 위해(A3, A5). | A3, A5 |
| StaffConsoleInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.write_committed | 필수 | oneOf(2분기) | 이번 턴의 쓰기가 확정됐는지. | 됨이면 기록은 반영됐고 응답만 못 나간 것이다. 다시 말하게 할지 정한다(J2). | J2, J3, J4a |
| StaffConsoleInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.write_committed [oneOf:0] | 해당 분기 | const="COMMITTED" | 기록은 반영됨 | 기록은 반영됐고 응답만 못 나갔으므로 "다시 말씀해 주세요"(반복 요청)로 같은 말을 다시 들을 수 있다. | J3 |
| StaffConsoleInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.write_committed [oneOf:1] | 해당 분기 | const="NOT_COMMITTED" | 아무것도 반영 안 됨 | 아무것도 반영되지 않았으므로 사용자가 같은 말을 다시 하면 처음처럼 처리된다. | J2, J4a |
| StaffConsoleInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.staff_alert | 필수 | oneOf(3분기) | 직원 알림 전달 결과. | 직원이 오지 않는다는 것을 프론트가 알아야 한다(J3). | J2, J3, J4a |
| StaffConsoleInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.staff_alert [oneOf:0] | 해당 분기 | const="NONE" | 보낼 알림이 없었음 | 보낼 알림이 없었던 실패를 알림 실패와 구분해 프론트가 직원을 따로 부르지 않게 한다. | J2, J4a |
| StaffConsoleInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.staff_alert [oneOf:1] | 해당 분기 | const="DELIVERED" | 보냄 | 응답은 실패했어도 직원은 오고 있다는 것을 프론트가 안다. | J8g |
| StaffConsoleInput.turn_failure_signal [anyOf:0] → TurnFailureSignal.staff_alert [oneOf:2] | 해당 분기 | const="DELIVERY_FAILED" | 못 보냄 | 직원 알림이 가지 못했으므로 프론트가 사용자에게 직원을 직접 찾게 하는 등 대처해야 한다. | J3 |
| StaffConsoleInput.turn_failure_signal [anyOf:1] | 해당 분기 | null | 없음 | 실패하지 않은 턴의 직원 알림이다(F1 직원을 찾음, G1 위급한 말). 알림은 가지만 실패 신호는 보낼 것이 없다. | F1, G1 |
| StaffConsoleInput.intervention_result | 필수 | anyOf(2분기) | 보낸 결정의 결과. | 보낸 결정이 반영됐는지 알아야 직원이 다시 보내거나 직접 대처한다. | J4a, J4b, F4 |
| StaffConsoleInput.intervention_result [anyOf:0] | 해당 분기 | → InterventionResult |  |  |  |
| StaffConsoleInput.intervention_result [anyOf:0] → InterventionResult | 해당 분기 | object; additionalProperties=False | 보낸 결정이 반영됐는지. | 반영 안 됐으면 직원이 다시 보내거나 직접 대처한다(J4). | F4, G6a, J4a, J4b |
| StaffConsoleInput.intervention_result [anyOf:0] → InterventionResult.session_id | 필수 | → SessionId | 어느 세션의 값인지. | 직원이 결정을 여러 자리에 보낼 수 있어, 반영됐다는 답이 어느 자리 것인지 알아야 다시 보낼 자리를 고른다(J4). | J4a, J4b, F4 |
| StaffConsoleInput.intervention_result [anyOf:0] → InterventionResult.session_id → SessionId | 필수 | string; minLength=1 | 프론트가 정한 세션 식별자. 발급·인증은 API·인증 영역의 일. | 같은 키오스크의 다음 사람과 세션을 나누고, 재접속 때 이어 가기 위해(A3, A5). | A3, A5 |
| StaffConsoleInput.intervention_result [anyOf:0] → InterventionResult.result | 필수 | oneOf(3분기) | 반영 여부. | 직원이 결정이 반영됐는지 알아야 다시 보내거나 직접 대처한다(J4). | F4, J4a, J4b |
| StaffConsoleInput.intervention_result [anyOf:0] → InterventionResult.result [oneOf:0] | 해당 분기 | const="APPLIED" | 쓰기 확정 | 보낸 결정이 세션에 반영됐으므로 직원이 더 할 일이 없다. | F4, G6a, G7 |
| StaffConsoleInput.intervention_result [anyOf:0] → InterventionResult.result [oneOf:1] | 해당 분기 | const="IGNORED" | 세션 상태상 처리하지 않음 | 세션 상태상 처리할 수 없는 결정(이미 끝난 세션에 종료 등)이었다는 것을 직원이 알아야 다시 보내지 않는다. | J4b |
| StaffConsoleInput.intervention_result [anyOf:0] → InterventionResult.result [oneOf:2] | 해당 분기 | const="FAILED" | 처리 중 실패 | 처리 중 실패했으니 직원이 같은 결정을 다시 보내거나 직접 대처해야 한다. | J4a |
| StaffConsoleInput.intervention_result [anyOf:1] | 해당 분기 | null | 없음 | 직원이 결정을 보내지 않은 턴이다(F1, G1). 개입 결정이 들어온 턴에만 결과가 간다(F4, J4a, J4b). | F1, G1 |

## output: InterventionDecision

계약 상태: current. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.

원본: [Schema](../../contracts/components/staff_console/output.schema.json), [의미·근거](../../contracts/components/staff_console/output.fields.yaml)

| 필드·분기 경로 | 필수 여부 | 값 제약·참조 | 무슨 값인가 | 왜 필요한가 | 근거 요구사항 |
|---|---|---|---|---|---|
| InterventionDecision |  | object; additionalProperties=False | 직원·의료진의 재개·종료. | 위험으로 멈춘 문진은 사람만 이어 가거나 끝낼 수 있다(G6, G7, F4). | F4, G6a, G7, J4b |
| InterventionDecision.session_id | 필수 | → SessionId | 어느 세션의 값인지. | 직원이 여러 키오스크를 보며 재개·종료를 보내므로, 어느 세션에 대한 결정인지 있어야 9-1절 처리 표가 그 세션의 상태로 판단한다(F4, G6). | G6a, J4b, F4 |
| InterventionDecision.session_id → SessionId | 필수 | string; minLength=1 | 프론트가 정한 세션 식별자. 발급·인증은 API·인증 영역의 일. | 같은 키오스크의 다음 사람과 세션을 나누고, 재접속 때 이어 가기 위해(A3, A5). | A3, A5 |
| InterventionDecision.decision | 필수 | → Decision | 재개 또는 종료. | 직원이 이어 갈지 끝낼지 정한다(G6, G7). | F4, G6a, G7, J4a |
| InterventionDecision.decision → Decision | 필수 | oneOf(2분기) | 직원의 재개 또는 종료. | 위험으로 멈춘 문진은 사람만 이어 가거나 끝낼 수 있다(G6, G7, F4). | G6a, F4, J4a |
| InterventionDecision.decision → Decision [oneOf:0] | 해당 분기 | const="RESUME" | 이어 감 | 위험이 지나갔다고 직원이 판단하면 멈춘 곳부터 이어 간다. | G6a, G6b, H3d, J4a |
| InterventionDecision.decision → Decision [oneOf:1] | 해당 분기 | const="END" | 끝냄 | 직원이 문진을 더 하지 않기로 하면 미완료로 마치고 결과를 넘긴다. | F4, G7, J4b |

