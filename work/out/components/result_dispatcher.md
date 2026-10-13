<!-- 생성물. 직접 고치지 말 것: python3 work/tools/build.py -->

# Result Dispatcher (결과 전달)

확정된 문진 결과를 시스템 밖으로 넘긴다.

이 문서는 현재 계약 원본에서 생성한 필드 안내다. 업무 실행·정답 판정의 검증 결과가 아니다. 전체 역할은 [구조 설명](../../../docs/architecture.md), 검사 범위는 [검증 방법](../../../docs/validation.md)에 있다.

## input: DispatchInput

계약 상태: current. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.

원본: [Schema](../../contracts/components/result_dispatcher/input.schema.json), [의미·근거](../../contracts/components/result_dispatcher/input.fields.yaml)

| 필드·분기 경로 | 필수 여부 | 값 제약·참조 | 무슨 값인가 | 왜 필요한가 | 근거 요구사항 |
|---|---|---|---|---|---|
| DispatchInput |  | object; additionalProperties=False | 세션 정보·응답 기록·건너뜀·확인 중단·세션 상태·중지 이력·문항 정의(턴 쓰기 반영 뒤). | 넘길 결과 전부: 답, 수정 이력, 풀리지 않은 답, 위험 답, 받지 못한 문항과 사유, 완료 여부, 멈춘 적(A4, C8, G4, G7). | G7 |
| DispatchInput.session_info | 필수 | → SessionInfo | 기록 저장소 · 세션 정보. | 어느 세션의 결과인지, 어느 문항 정의 버전으로 받은 답인지 받는 쪽이 알아야 한다. | H2, H4 |
| DispatchInput.session_info → SessionInfo | 필수 | object; additionalProperties=False | 세션 식별과 문항 정의 버전. | 세션을 찾고(A3) 버전을 고정한다(J1). | J1, A1 |
| DispatchInput.session_info → SessionInfo.session_id | 필수 | → SessionId | 어느 세션의 값인지. | 응답 기록·진행 기록·Plan 기록·로그가 모두 이 식별로 한 세션에 묶인다. 세션 정보를 만들 때 정해져 끝까지 바뀌지 않는다(9-2절 2). | A3, A1, A2 |
| DispatchInput.session_info → SessionInfo.session_id → SessionId | 필수 | string; minLength=1 | 프론트가 정한 세션 식별자. 발급·인증은 API·인증 영역의 일. | 같은 키오스크의 다음 사람과 세션을 나누고, 재접속 때 이어 가기 위해(A3, A5). | A3, A5 |
| DispatchInput.session_info → SessionInfo.question_bank_version | 필수 | integer; minimum=0 | 세션을 만들 때의 최신 버전. | 운영 중 새 문항 정의가 등록돼도 진행 중인 세션은 처음 버전으로 끝나야 답과 문항이 어긋나지 않는다. | J1 |
| DispatchInput.answer_records | 필수 | array | 기록 저장소 · 모든 슬롯. | 넘길 답(현재값), 수정 이력, 풀리지 않은 확인 대기, 위험 표시가 모두 여기 있다. | H2, H4, A4a |
| DispatchInput.answer_records[] | 배열 항목 | → SlotRecord |  |  |  |
| DispatchInput.answer_records[] → SlotRecord | 배열 항목 | object; additionalProperties=False; allOf(1분기) | 슬롯 하나의 응답 기록. 저장 판단만 쓴다. | 슬롯마다 지금 답, 이전 답, 확인을 기다리는 새 답, 위험 표시를 한곳에 두어야 저장 판단과 결과 전달이 같은 기록을 본다. | B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.slot | 필수 | → SlotRef | 이 답 기록이 속한 문항·반복 행·슬롯의 식별자. | 응답 기록이 슬롯 단위라 기록마다 어느 칸인지 있어야 한다. | B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| DispatchInput.answer_records[] → SlotRecord.slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| DispatchInput.answer_records[] → SlotRecord.slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| DispatchInput.answer_records[] → SlotRecord.slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| DispatchInput.answer_records[] → SlotRecord.slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| DispatchInput.answer_records[] → SlotRecord.current_value | 필수 | → CurrentValue | 지금 기록. | 결과의 본체이자 열린 문항 계산의 근거. | B1, C1, C2 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue | 필수 | oneOf(4분기) | 슬롯의 지금 기록: 답(값) / 모름 / 거절 / 없음. | 모름·거절은 빈 칸과 다르다(다시 묻지 않거나 정책대로 묻는다, B7, B8). | B1, B7b, C2 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0] | 해당 분기 | object; additionalProperties=False | 확정한 답을 answer 필드로 감싼 기록. 모름·거절 표지와 구별되는 값 분기다. | 답을 받은 칸이다. 이 값이 결과로 넘어가고 같음·다름 비교의 기준이 된다. | B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0].answer | 필수 | → Value | 이 슬롯에 확정된 답. 선택지 문자열 또는 수·단위 객체이며 상세 제약은 해당 문항 정의로 검사한다. | 답 값을 모름·거절·없음과 모양으로 구분한다. | B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0].answer → Value | 필수 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0].answer → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:1] | 해당 분기 | const="UNKNOWN_RECORD" | 모름. | 모른다고 한 칸이다. 빈 칸과 달리 정책대로만 다시 묻는다. | B7b, C8c, X7 |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:2] | 해당 분기 | const="REFUSAL_RECORD" | 거절. | 답하지 않겠다고 한 칸이다. 빈 칸과 달리 정책대로만 다시 묻는다. | B8b, N8a |
| DispatchInput.answer_records[] → SlotRecord.current_value → CurrentValue [oneOf:3] | 해당 분기 | const="NONE" | 아직 없음. | 아직 답이 없는 칸은 열린 문항 계산에서 물을 대상이 된다. | C2, S1c, S6a |
| DispatchInput.answer_records[] → SlotRecord.risk_mark | 필수 | anyOf(2분기) | 현재값의 위험 기준. | 결과 전달용(G4). Plan은 다시 보지 않는다(재개 뒤 같은 답으로 다시 멈추지 않게, G6). | G6b, G3, G4 |
| DispatchInput.answer_records[] → SlotRecord.risk_mark [anyOf:0] | 해당 분기 | → RiskResponse |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.risk_mark [anyOf:0] → RiskResponse | 해당 분기 | oneOf(2분기) | 위험 기준에 해당하는 답에 할 일. | 바로 멈춰야 하는 답과 결과에만 표시할 답을 나눈다(G3, G4). | G3, G4, G6b |
| DispatchInput.answer_records[] → SlotRecord.risk_mark [anyOf:0] → RiskResponse [oneOf:0] | 해당 분기 | const="IMMEDIATE" | 바로 멈추고 직원을 부름 | 그 답 자체가 위급하면(죽고 싶은 생각 = 예) 바로 멈추고 직원을 불러야 한다. | G3, G6b |
| DispatchInput.answer_records[] → SlotRecord.risk_mark [anyOf:0] → RiskResponse [oneOf:1] | 해당 분기 | const="ON_RESULT" | 계속하고 결과에 표시 | 위험하지만 지금 멈출 정도는 아닌 답(높은 혈압)은 문진을 이어 가고 결과에 표시해 의료진이 본다. | G4 |
| DispatchInput.answer_records[] → SlotRecord.risk_mark [anyOf:1] | 해당 분기 | null | 없음 | 위험 기준에 걸리지 않는 현재값이다(B1 Q5.시간 7, C1 Q2.개비 20). 결과 전달이 이 표시로 위험한 답을 가리므로(G4, H4), 없음이 "결과에 표시할 것 없음"이다. | B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.history | 필수 | array | 오래된 순서의 이전 답 값. 메타데이터를 확보한 이력은 {value, value_metadata}, 미확보 이력은 값만 기록한다. | 수정 이력을 결과로 넘긴다(C1). | C1, C2, C4a |
| DispatchInput.answer_records[] → SlotRecord.history[] | 배열 항목 | → HistoryEntry |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry | 배열 항목 | oneOf(2분기) | 이전 값만 있는 이력과 이전 값의 정밀도·근거까지 있는 이력을 구별한다. 정보가 있는 경우에만 메타데이터를 함께 기록한다. | 이전 값만 있는 이력과 이전 값의 정밀도·근거까지 있는 이력을 구별한다. 정보가 있는 경우에만 메타데이터를 함께 기록한다. | T2 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:0] | 해당 분기 | → Value |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:0] → Value | 해당 분기 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:0] → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:0] → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:0] → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:0] → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:0] → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:0] → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:0] → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:0] → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:0] → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1] | 해당 분기 | object; additionalProperties=False |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value | 필수 | → Value | 이 항목의 값. 정밀도와 근거는 value_metadata에 별도로 기록한다. | 이전 값만 있는 이력과 이전 값의 정밀도·근거까지 있는 이력을 구별한다. 정보가 있는 경우에만 메타데이터를 함께 기록한다. | T2 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value → Value | 필수 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata | 필수 | → ValueMetadata | 해당 값의 정밀도와 근거. 생략은 미수집이며 exact로 간주하지 않는다. | 이전 값만 있는 이력과 이전 값의 정밀도·근거까지 있는 이력을 구별한다. 정보가 있는 경우에만 메타데이터를 함께 기록한다. | T2 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata → ValueMetadata | 필수 | object; additionalProperties=False | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata → ValueMetadata.precision | 필수 | → Precision | 값이 exact(단일 확정 표현), approximate(근사 표현), unspecified(정밀도 미확보)인지 전달한다. 범위 중간값의 저장 허용 여부는 결정하지 않는다. | 같은 숫자라도 단일 확정 표현과 근사 표현을 구별하여 저장·재질문·응답 재료에서 정보가 사라지지 않아야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata → ValueMetadata.precision → Precision | 필수 | string; enum=["exact", "approximate", "unspecified"] | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | T1 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata → ValueMetadata.evidence | 필수 | array | 원문 근거 목록. 빈 목록은 근거가 확보되지 않았음을 뜻하며 근거가 없다는 업무 판정을 뜻하지 않는다. | 복수 구절의 합산·정정·비교는 근거 하나로 축약하면 정보가 사라진다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata → ValueMetadata.evidence[] | 배열 항목 | → Evidence |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata → ValueMetadata.evidence[] → Evidence | 배열 항목 | object; additionalProperties=False | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata → ValueMetadata.evidence[] → Evidence.turn_index | 필수 | integer; minimum=0 | 세션 내 원문 발화의 턴 순번. Framework가 부여하며 0/1 시작 기준은 세션에서 일관되게 적용한다. | 현재 발화와 과거 발화의 근거를 혼동하지 않아야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata → ValueMetadata.evidence[] → Evidence.start | 필수 | integer; minimum=0 | 원문에서 근거가 시작하는 포함 위치. 위치 단위는 offset_unit으로 명시한다. | 같은 구절이 원문에 반복되어도 어느 부분을 사용했는지 식별해야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata → ValueMetadata.evidence[] → Evidence.end | 필수 | integer; minimum=0 | 원문에서 근거가 끝나는 제외 위치. start 이상이어야 한다. 순서와 text 길이의 일관성은 정적 자료 무결성 검사로 확인한다. | 원문 근거의 정확한 범위를 복원할 수 있어야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata → ValueMetadata.evidence[] → Evidence.offset_unit | 필수 | string; enum=["unicode_code_point", "utf16_code_unit", "utf8_byte"] | 위치 단위: unicode_code_point, utf16_code_unit, utf8_byte. 서로 다른 런타임의 위치를 조용히 혼용하지 않는다. | Unicode 문자, UTF-16 코드 단위, UTF-8 바이트 위치는 같은 숫자가 아닐 수 있다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.history[] → HistoryEntry [oneOf:1].value_metadata → ValueMetadata.evidence[] → Evidence.text | 필수 | string; minLength=1 | 근거 구절 자체. 원문 일치 여부는 원문을 가진 담당자가 확인한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.pending | 필수 | anyOf(2분기) | 있으면 하나. 한 슬롯에 최대 하나(모양으로 보장). | 충돌한 새 값을 확인을 받을 때까지 현재값과 따로 둔다. 끝까지 안 풀리면 결과에 풀리지 않은 답으로 넘어간다. | C4a, C3, C8d |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] | 해당 분기 | → PendingRecord |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord | 해당 분기 | object; additionalProperties=False | 확인을 기다리는 새 값. | 충돌 값을 바로 저장하지 않고 확인을 받는다(C3). | C4a, C3 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.pending_id | 필수 | → PendingId | 이 슬롯의 현재 확인 대기를 식별하는 ID. 확인 응답을 특정 대기 값과 연결한다. | 다음 턴의 "네"가 이 확인 대기에 대한 것인지 맞춰 본다. | C4a, X6, C3 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.pending_id → PendingId | 필수 | string; minLength=1 | 저장 판단이 확인 대기를 둘 때 새로 만드는, 세션 안에서 겹치지 않는 값(예: UUID). | "네"가 어느 확인 대기에 대한 답인지 상태 판정이 이 ID로 잇는다. 같은 슬롯에 새 충돌 값이 와서 확인 대기가 바뀌면 이전 확인에 대한 "네"가 새 값을 받아들이지 않게 한다(C4). | C3, C4a, N13 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value | 필수 | → Value | 새 값. | 받아들이면 이 값이 현재값이 되고, 끝까지 안 풀리면 결과에 "풀리지 않은 답"으로 넘어간다. | C4a, C3, S8b |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value → Value | 필수 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.risk_mark | 필수 | anyOf(2분기) | 그 값의 위험 기준. | 받아들일 때 이 위험 표시가 현재값의 위험 표시로 그대로 옮겨진다. | G10 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.risk_mark [anyOf:0] | 해당 분기 | → RiskResponse |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.risk_mark [anyOf:0] → RiskResponse | 해당 분기 | oneOf(2분기) | 위험 기준에 해당하는 답에 할 일. | 바로 멈춰야 하는 답과 결과에만 표시할 답을 나눈다(G3, G4). | G3, G4, G6b |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.risk_mark [anyOf:0] → RiskResponse [oneOf:0] | 해당 분기 | const="IMMEDIATE" | 바로 멈추고 직원을 부름 | 그 답 자체가 위급하면(죽고 싶은 생각 = 예) 바로 멈추고 직원을 불러야 한다. | G3, G6b |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.risk_mark [anyOf:0] → RiskResponse [oneOf:1] | 해당 분기 | const="ON_RESULT" | 계속하고 결과에 표시 | 위험하지만 지금 멈출 정도는 아닌 답(높은 혈압)은 문진을 이어 가고 결과에 표시해 의료진이 본다. | G4 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.risk_mark [anyOf:1] | 해당 분기 | null | 없음 | 위험 기준이 없는 슬롯의 확인 대기다(C3·C4a의 Q2.개비). 9-2절 표가 받아들일 때 이 표시를 현재값의 위험 표시로 옮기므로, 없음이 "받아들여도 위험 표시가 생기지 않음"이다(G10과 대비). | C3, C4a |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata | 선택 | → ValueMetadata | 해당 값의 정밀도와 근거. 생략은 미수집이며 exact로 간주하지 않는다. | 정규화·판정·저장·확인 후보·응답 재료에서 정밀도와 근거가 사라지지 않아야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata | 선택 | object; additionalProperties=False | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.precision | 필수 | → Precision | 값이 exact(단일 확정 표현), approximate(근사 표현), unspecified(정밀도 미확보)인지 전달한다. 범위 중간값의 저장 허용 여부는 결정하지 않는다. | 같은 숫자라도 단일 확정 표현과 근사 표현을 구별하여 저장·재질문·응답 재료에서 정보가 사라지지 않아야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.precision → Precision | 필수 | string; enum=["exact", "approximate", "unspecified"] | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | T1 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence | 필수 | array | 원문 근거 목록. 빈 목록은 근거가 확보되지 않았음을 뜻하며 근거가 없다는 업무 판정을 뜻하지 않는다. | 복수 구절의 합산·정정·비교는 근거 하나로 축약하면 정보가 사라진다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] | 배열 항목 | → Evidence |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence | 배열 항목 | object; additionalProperties=False | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence.turn_index | 필수 | integer; minimum=0 | 세션 내 원문 발화의 턴 순번. Framework가 부여하며 0/1 시작 기준은 세션에서 일관되게 적용한다. | 현재 발화와 과거 발화의 근거를 혼동하지 않아야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence.start | 필수 | integer; minimum=0 | 원문에서 근거가 시작하는 포함 위치. 위치 단위는 offset_unit으로 명시한다. | 같은 구절이 원문에 반복되어도 어느 부분을 사용했는지 식별해야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence.end | 필수 | integer; minimum=0 | 원문에서 근거가 끝나는 제외 위치. start 이상이어야 한다. 순서와 text 길이의 일관성은 정적 자료 무결성 검사로 확인한다. | 원문 근거의 정확한 범위를 복원할 수 있어야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence.offset_unit | 필수 | string; enum=["unicode_code_point", "utf16_code_unit", "utf8_byte"] | 위치 단위: unicode_code_point, utf16_code_unit, utf8_byte. 서로 다른 런타임의 위치를 조용히 혼용하지 않는다. | Unicode 문자, UTF-16 코드 단위, UTF-8 바이트 위치는 같은 숫자가 아닐 수 있다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence.text | 필수 | string; minLength=1 | 근거 구절 자체. 원문 일치 여부는 원문을 가진 담당자가 확인한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.pending [anyOf:1] | 해당 분기 | null | 없음 | 확인 대기가 없는 슬롯이다(B1, C1). 8-1 규칙 16이 남은 확인 대기를 찾을 때 이 없음이 "물을 것 없음"이 되고, 결과 전달에도 풀리지 않은 답으로 넘어가지 않는다. | B1, C1 |
| DispatchInput.answer_records[] → SlotRecord.value_metadata | 선택 | → ValueMetadata | 해당 값의 정밀도와 근거. 생략은 미수집이며 exact로 간주하지 않는다. | 정규화·판정·저장·확인 후보·응답 재료에서 정밀도와 근거가 사라지지 않아야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.value_metadata → ValueMetadata | 선택 | object; additionalProperties=False | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.value_metadata → ValueMetadata.precision | 필수 | → Precision | 값이 exact(단일 확정 표현), approximate(근사 표현), unspecified(정밀도 미확보)인지 전달한다. 범위 중간값의 저장 허용 여부는 결정하지 않는다. | 같은 숫자라도 단일 확정 표현과 근사 표현을 구별하여 저장·재질문·응답 재료에서 정보가 사라지지 않아야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.value_metadata → ValueMetadata.precision → Precision | 필수 | string; enum=["exact", "approximate", "unspecified"] | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | T1 |
| DispatchInput.answer_records[] → SlotRecord.value_metadata → ValueMetadata.evidence | 필수 | array | 원문 근거 목록. 빈 목록은 근거가 확보되지 않았음을 뜻하며 근거가 없다는 업무 판정을 뜻하지 않는다. | 복수 구절의 합산·정정·비교는 근거 하나로 축약하면 정보가 사라진다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.value_metadata → ValueMetadata.evidence[] | 배열 항목 | → Evidence |  |  |  |
| DispatchInput.answer_records[] → SlotRecord.value_metadata → ValueMetadata.evidence[] → Evidence | 배열 항목 | object; additionalProperties=False | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.value_metadata → ValueMetadata.evidence[] → Evidence.turn_index | 필수 | integer; minimum=0 | 세션 내 원문 발화의 턴 순번. Framework가 부여하며 0/1 시작 기준은 세션에서 일관되게 적용한다. | 현재 발화와 과거 발화의 근거를 혼동하지 않아야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.value_metadata → ValueMetadata.evidence[] → Evidence.start | 필수 | integer; minimum=0 | 원문에서 근거가 시작하는 포함 위치. 위치 단위는 offset_unit으로 명시한다. | 같은 구절이 원문에 반복되어도 어느 부분을 사용했는지 식별해야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.value_metadata → ValueMetadata.evidence[] → Evidence.end | 필수 | integer; minimum=0 | 원문에서 근거가 끝나는 제외 위치. start 이상이어야 한다. 순서와 text 길이의 일관성은 정적 자료 무결성 검사로 확인한다. | 원문 근거의 정확한 범위를 복원할 수 있어야 한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.value_metadata → ValueMetadata.evidence[] → Evidence.offset_unit | 필수 | string; enum=["unicode_code_point", "utf16_code_unit", "utf8_byte"] | 위치 단위: unicode_code_point, utf16_code_unit, utf8_byte. 서로 다른 런타임의 위치를 조용히 혼용하지 않는다. | Unicode 문자, UTF-16 코드 단위, UTF-8 바이트 위치는 같은 숫자가 아닐 수 있다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord.value_metadata → ValueMetadata.evidence[] → Evidence.text | 필수 | string; minLength=1 | 근거 구절 자체. 원문 일치 여부는 원문을 가진 담당자가 확인한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| DispatchInput.answer_records[] → SlotRecord [allOf:0] | 해당 분기 | if; then |  |  |  |
| DispatchInput.answer_records[] → SlotRecord [allOf:0] [if] | 조건 |  |  |  |  |
| DispatchInput.answer_records[] → SlotRecord [allOf:0] [if].value_metadata | 필수 |  | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| DispatchInput.answer_records[] → SlotRecord [allOf:0] [if].value_metadata.precision | 선택 | enum=["exact", "approximate"] | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| DispatchInput.answer_records[] → SlotRecord [allOf:0] [then] | 조건 |  |  |  |  |
| DispatchInput.answer_records[] → SlotRecord [allOf:0] [then].current_value | 선택 | object | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| DispatchInput.skipped | 필수 | array | 기록 저장소 · 진행 기록.건너뜀. | 받지 못한 문항과 그 까닭을 결과에 함께 넘긴다. | H4 |
| DispatchInput.skipped[] | 배열 항목 | → SkipEntry |  |  |  |
| DispatchInput.skipped[] → SkipEntry | 배열 항목 | object; additionalProperties=False | 더 묻지 않기로 한 문항과 사유. | 결과에 왜 답이 없는지 남기고, 다시 묻지 않는다(B7, B8, B10). | B10, B8b, X7 |
| DispatchInput.skipped[] → SkipEntry.question_id | 필수 | → QuestionId | 문항. | 어느 문항을 더 묻지 않는지 알아야 열린 문항에서 빼고 결과에 남긴다. | B10, B8b, X7 |
| DispatchInput.skipped[] → SkipEntry.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| DispatchInput.skipped[] → SkipEntry.reason | 필수 | → SkipReason | 건너뜀 사유. | 결과를 받는 의료진이 답이 없는 까닭(모름·거절·시도 초과)을 구분해 본다. | B10, B8b, X7 |
| DispatchInput.skipped[] → SkipEntry.reason → SkipReason | 필수 | oneOf(3분기) | 문항을 더 묻지 않기로 한 까닭. | 답이 없는 문항에서 모름 수용·거절 수용·질문 횟수 초과 등의 건너뜀 이유를 구분하여 결과 수신처가 미응답 상태를 해석할 수 있어야 한다(B10). | B7b, B8b, B10 |
| DispatchInput.skipped[] → SkipEntry.reason → SkipReason [oneOf:0] | 해당 분기 | const="UNKNOWN_ACCEPTED" | 모름을 받아들임 | 모름을 받아들여 더 묻지 않았다는 것을 결과에 남겨, 받는 쪽이 빈 답의 까닭을 안다. | B7b, C8c, R11, X7 |
| DispatchInput.skipped[] → SkipEntry.reason → SkipReason [oneOf:1] | 해당 분기 | const="REFUSAL_ACCEPTED" | 거절을 받아들임 | 거절을 받아들여 더 묻지 않았다는 것을 결과에 남겨, 받는 쪽이 빈 답의 까닭을 안다. | B8b, S3b |
| DispatchInput.skipped[] → SkipEntry.reason → SkipReason [oneOf:2] | 해당 분기 | const="ATTEMPTS_EXCEEDED" | 질문 상한만큼 물어도 쓸 수 있는 답이 없음 | 질문 상한까지 물어도 쓸 수 있는 답이 없어 넘어갔다는 것을 남긴다. 사용자가 모른다고 한 것과는 다르다. | B10, R1, R18, S3d |
| DispatchInput.confirm_stopped | 필수 | array | 기록 저장소 · 진행 기록.확인 중단. | 확인을 그만둔 확인 대기는 결과에 '풀리지 않은 답'(서로 다른 두 답)으로 넘겨야 의료진이 판단한다. | H4, C8d |
| DispatchInput.confirm_stopped[] | 배열 항목 | → SlotRef |  |  |  |
| DispatchInput.confirm_stopped[] → SlotRef | 배열 항목 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| DispatchInput.confirm_stopped[] → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| DispatchInput.confirm_stopped[] → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| DispatchInput.confirm_stopped[] → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| DispatchInput.confirm_stopped[] → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| DispatchInput.session_status | 필수 | → SessionStatus | 기록 저장소 · 진행 기록.세션 상태. | 완료인지, 미완료면 왜(개입 종료·이탈·사용자 중단)인지 결과에 넘긴다. | A4a, F4, H2 |
| DispatchInput.session_status → SessionStatus | 필수 | oneOf(6분기) | 세션이 어디에 있는지. | LangGraph가 입력을 처리할지(처리 표)와, 결과를 받는 쪽이 완료·미완료와 그 사유를 아는 데 쓴다(A4, A5, G5, H2). | G1, H2, A4a, G6a |
| DispatchInput.session_status → SessionStatus [oneOf:0] | 해당 분기 | const="IN_PROGRESS" | 문진 중 | 이 상태에서만 사용자 발화를 처리한다. 멈춤·종료와 구분해야 처리 표가 입력을 받을지 정한다. | G6a, G6b, H3d |
| DispatchInput.session_status → SessionStatus [oneOf:1] | 해당 분기 | const="PAUSED_RISK" | 위험으로 멈춤. 사용자 발화는 처리하지 않음 | 위험으로 멈춘 동안에는 사용자 말을 처리하지 않고 직원의 재개·종료만 받아야 한다. | G1, G5, J4a |
| DispatchInput.session_status → SessionStatus [oneOf:2] | 해당 분기 | const="ENDED_COMPLETE" | 마침 | 사용자가 마치기로 확인한 정상 종료다. 결과를 받는 쪽이 완료된 결과로 다룬다. | H2, J5, A5 |
| DispatchInput.session_status → SessionStatus [oneOf:3] | 해당 분기 | const="ENDED_STAFF" | 직원이 끝냄 | 직원이 끝낸 미완료다. 받는 쪽이 이탈·사용자 중단과 구분해 사유를 안다. | F4, G7 |
| DispatchInput.session_status → SessionStatus [oneOf:4] | 해당 분기 | const="ENDED_LEFT" | 사용자가 떠남 | 사용자가 떠난 미완료다. 받는 쪽이 사유를 구분한다. | A4a, A4b |
| DispatchInput.session_status → SessionStatus [oneOf:5] | 해당 분기 | const="ENDED_USER_STOP" | 사용자가 그만둠 | 사용자가 그만두기로 확인한 미완료다. 받는 쪽이 사유를 구분한다. | D5a |
| DispatchInput.pause_history | 필수 | array | 기록 저장소 · 진행 기록.중지 이력. | 문진 중 위험으로 멈춘 적이 있는지 결과에 넘긴다. | G7 |
| DispatchInput.pause_history[] | 배열 항목 | → PauseEntry |  |  |  |
| DispatchInput.pause_history[] → PauseEntry | 배열 항목 | object; additionalProperties=False | 일시 중지 또는 재개 한 건. | 결과에 멈춘 적과 이유를 남긴다(G7). | G1, G6a, G7 |
| DispatchInput.pause_history[] → PauseEntry.kind | 필수 | → PauseKind | 중지 이력 종류. | 결과에 멈춘 시점과 다시 이어 간 시점이 둘 다 남아야 문진 경과를 안다. | G1, G6a, G7 |
| DispatchInput.pause_history[] → PauseEntry.kind → PauseKind | 필수 | oneOf(2분기) | 중지 이력 항목의 종류. | 결과에 문진 중 멈춘 적이 있는지와 언제 다시 이어졌는지 남긴다(G7). | G1, G6a, G7 |
| DispatchInput.pause_history[] → PauseEntry.kind → PauseKind [oneOf:0] | 해당 분기 | const="PAUSE" | 위험으로 멈춤 | 언제 무엇 때문에 멈췄는지 결과에 남긴다. | G1, G3, G7 |
| DispatchInput.pause_history[] → PauseEntry.kind → PauseKind [oneOf:1] | 해당 분기 | const="RESUME" | 직원이 이어 가게 함 | 멈춘 뒤 다시 이어 갔다는 것을 남겨, 그 뒤의 답이 재개 후의 답임을 안다. | G6a, G6b, H3d |
| DispatchInput.pause_history[] → PauseEntry.reasons | 필수 | array | 일시 중지의 이유. 재개는 빈 목록. | 결과를 받는 의료진이 왜 멈췄는지 확인한다. | G1, G3, G7 |
| DispatchInput.pause_history[] → PauseEntry.reasons[] | 배열 항목 | → PauseReason |  |  |  |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason | 배열 항목 | oneOf(2분기) | 일시 중지의 이유 하나. | 결과를 받는 쪽이 왜 멈췄는지 안다(G7). | G1, G3, G7 |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:0] | 해당 분기 | object; additionalProperties=False | 위험한 말. | 위험한 말 때문에 멈췄다면 그 원문을 남겨야 의료진이 결과에서 무슨 말이었는지 확인한다. | G1, G2, G9, X9, S3c |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:0].kind | 필수 | const="RISK_SIGNAL" | 위험 신호. | 멈춘 까닭이 위험 신호면 근거(원문)를, 위험 기준이면 대상(슬롯)을 담는다. 담는 칸이 서로 달라 이 값으로 가르지 않으면 중지 이력을 읽는 쪽이 어느 칸을 봐야 할지 모른다(G1, G3). | G1, G2, G9, X9 |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:0].evidence | 필수 | array; minItems=1 | 원문 표현. | 결과를 받는 의료진이 어떤 말 때문에 멈췄는지 원문으로 확인한다. | G1, G2, G9, S3c |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:0].evidence[] | 배열 항목 | → SourceText |  |  |  |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:0].evidence[] → SourceText | 배열 항목 | string; minLength=1 | 사용자 발화에서 그대로 옮긴 부분. | 판정 근거를 사람이 확인하고, 애매한 값을 사용자 말 그대로 짚어 되묻기 위해(B3, G1). | F1, G1, G8a |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:1] | 해당 분기 | object; additionalProperties=False | 위험한 답. | 위험한 답 때문에 멈췄다면 어느 칸의 답인지 남겨야 의료진이 결과에서 그 답을 찾아 본다. | G3 |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:1].kind | 필수 | const="RISK_RULE" | 위험 기준. | 위험 기준으로 멈춘 이력은 어느 슬롯의 답 때문인지를 남긴다. 위험 신호 이유와 모양이 달라, 이 값이 있어야 결과 전달이 중지 이력을 원문과 슬롯 중 무엇으로 읽을지 정한다(G3, G6b). | G3 |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:1].target | 필수 | array; minItems=1 | 위험 기준에 해당한 슬롯. | 어느 답 때문에 멈췄는지 결과에 남긴다. | G3 |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:1].target[] | 배열 항목 | → SlotRef |  |  |  |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:1].target[] → SlotRef | 배열 항목 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:1].target[] → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:1].target[] → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:1].target[] → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| DispatchInput.pause_history[] → PauseEntry.reasons[] → PauseReason [oneOf:1].target[] → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |

## output: DispatchOutput

계약 상태: current. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.

원본: [Schema](../../contracts/components/result_dispatcher/output.schema.json), [의미·근거](../../contracts/components/result_dispatcher/output.fields.yaml)

| 필드·분기 경로 | 필수 여부 | 값 제약·참조 | 무슨 값인가 | 왜 필요한가 | 근거 요구사항 |
|---|---|---|---|---|---|
| DispatchOutput |  | object; additionalProperties=False | 전달 기록 한 건. 밖으로 넘기는 문진 결과의 형식은 받는 곳이 정해지면 정한다(이 스키마 밖). | 전달 실패를 남겨 다시 보낼 수 있게(J5). | J5 |
| DispatchOutput.dispatch_record | 필수 | → DispatchRecord | 한 건. | 넘기기가 성공했는지를 남겨야 실패한 전달을 다시 보낼 수 있다(J5). 시각은 어느 케이스도 쓰지 않아 두지 않는다(원칙 5). | J5 |
| DispatchOutput.dispatch_record → DispatchRecord | 필수 | object; additionalProperties=False | 결과 전달 한 건. | 세션 결과를 어느 대상에 전달했는지와 전달 성공·실패를 기록하여, 누락된 결과와 아직 전달되지 않은 결과를 구분해야 한다. | J5 |
| DispatchOutput.dispatch_record → DispatchRecord.succeeded | 필수 | boolean | 성공했는지. | 실패한 전달을 찾아 다시 보내려면 성공 여부가 있어야 한다. | J5 |

