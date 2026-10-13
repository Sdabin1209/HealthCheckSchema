<!-- 생성물. 직접 고치지 말 것: python3 work/tools/build.py -->

# Record Writer (저장 판단)

판정을 응답 기록에 어떻게 반영할지 슬롯별로 정한다.

이 문서는 현재 계약 원본에서 생성한 필드 안내다. 업무 실행·정답 판정의 검증 결과가 아니다. 전체 역할은 [구조 설명](../../../docs/architecture.md), 검사 범위는 [검증 방법](../../../docs/validation.md)에 있다.

## input: RecordWriterInput

계약 상태: current. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.

원본: [Schema](../../contracts/components/record_writer/input.schema.json), [의미·근거](../../contracts/components/record_writer/input.fields.yaml)

| 필드·분기 경로 | 필수 여부 | 값 제약·참조 | 무슨 값인가 | 왜 필요한가 | 근거 요구사항 |
|---|---|---|---|---|---|
| RecordWriterInput |  | object; additionalProperties=False | 판정·무효화 대상 문항·슬롯 목록·기록 대상 슬롯의 응답 기록. | 판정을 슬롯별 저장 결정으로 바꾸려면 첫 저장인지(현재값), 받아들일 값(확인 대기)이 무엇인지 알아야 한다. | B1, C1, C2 |
| RecordWriterInput.judgments | 필수 | array | 상태 판정 · 판정. | 판정마다 슬롯별 저장 결정(첫 저장, 새 revision, 확인 대기 등)을 만든다. | B1, C1, C3 |
| RecordWriterInput.judgments[] | 배열 항목 | → Judgment |  |  |  |
| RecordWriterInput.judgments[] → Judgment | 배열 항목 | object; additionalProperties=False; allOf(1분기) | 대상 하나에 대해 이번 발화가 뜻하는 것. | 저장 판단은 정정(새 revision)과 충돌(기존 값 유지)을 구분해야 하므로 판정이 저장보다 먼저 있어야 한다. | A2, B2, C3 |
| RecordWriterInput.judgments[] → Judgment.target | 필수 | → Target | 판정의 대상. 문항 전체 가능. | 문항 전체 모름·거절이 있다(B7). | A2, B1, S3b |
| RecordWriterInput.judgments[] → Judgment.target → Target | 필수 | oneOf(2분기) | 슬롯 하나 또는 문항 전체. | 항목·판정·응답 지시가 슬롯과 문항 전체를 같은 자리에서 가리켜야 한다. | A2, R11, S3b |
| RecordWriterInput.judgments[] → Judgment.target → Target [oneOf:0] | 해당 분기 | → SlotRef |  |  |  |
| RecordWriterInput.judgments[] → Judgment.target → Target [oneOf:0] → SlotRef | 해당 분기 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| RecordWriterInput.judgments[] → Judgment.target → Target [oneOf:0] → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| RecordWriterInput.judgments[] → Judgment.target → Target [oneOf:0] → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| RecordWriterInput.judgments[] → Judgment.target → Target [oneOf:0] → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| RecordWriterInput.judgments[] → Judgment.target → Target [oneOf:0] → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| RecordWriterInput.judgments[] → Judgment.target → Target [oneOf:1] | 해당 분기 | → WholeQuestion |  |  |  |
| RecordWriterInput.judgments[] → Judgment.target → Target [oneOf:1] → WholeQuestion | 해당 분기 | object; additionalProperties=False | 문항의 모든 슬롯을 한꺼번에 가리킴. | "술은 잘 모르겠어요"처럼 문항 전체에 대한 모름·거절과, 문항에 대한 안내·나중에가 있다(B7, D3, E1). 저장은 항상 슬롯 단위라 저장 판단이 펼친다. | R11, S3b, N17 |
| RecordWriterInput.judgments[] → Judgment.target → Target [oneOf:1] → WholeQuestion.question_id | 필수 | → QuestionId | 가리키는 문항. | 문항 전체에 대한 말("술은 잘 모르겠어요")은 그 문항의 모든 칸에 펼쳐 기록해야 하므로 어느 문항인지 있어야 한다. | R11, S3b, N17 |
| RecordWriterInput.judgments[] → Judgment.target → Target [oneOf:1] → WholeQuestion.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| RecordWriterInput.judgments[] → Judgment.target → Target [oneOf:1] → WholeQuestion.whole_question | 필수 | const=true | 항상 true. | 슬롯 대상과 모양으로 구분하기 위해. | R11, S3b, N17 |
| RecordWriterInput.judgments[] → Judgment.status | 필수 | anyOf(2분기) | 공유 어휘 상태. 확인-긍정·부정만으로 확인 대기를 받아들이거나 버리는 판정은 없음. | "네"는 새 값을 말한 것이 아니라 상태가 없다. 받아들임·버림은 확인 대기 처리로 나타낸다(C4). | A2, B2, C3 |
| RecordWriterInput.judgments[] → Judgment.status [anyOf:0] | 해당 분기 | → JudgmentStatus |  |  |  |
| RecordWriterInput.judgments[] → Judgment.status [anyOf:0] → JudgmentStatus | 해당 분기 | oneOf(8분기) | 상태 판정이 대상마다 내린 판정. | 저장 판단과 다음 행동 결정이 대상 슬롯의 상태를 같은 코드로 해석해야 한다. 발화 전체의 무관 여부는 UtteranceJudgment, 세션 완료 여부는 SessionStatus로 구분하여 슬롯 판정과 혼동하지 않는다. | A2, B2, B3a, C1, C3 |
| RecordWriterInput.judgments[] → Judgment.status [anyOf:0] → JudgmentStatus [oneOf:0] | 해당 분기 | const="ANSWERED" | 쓸 수 있는 값(첫 답이거나 기존과 같음) | 쓸 수 있는 값이라 첫 답이면 저장하고, 기존과 같으면 바꿀 것이 없다(남은 확인 대기만 버린다). | A2, B1, C4b |
| RecordWriterInput.judgments[] → Judgment.status [anyOf:0] → JudgmentStatus [oneOf:1] | 해당 분기 | const="MISSING" | 같은 문항의 필수 슬롯이 빠짐 | 같은 문항에서 받은 값은 저장하고 빠진 칸만 다시 묻기 위해 빠진 칸을 따로 판정한다(B2). | B2, E3b, R1 |
| RecordWriterInput.judgments[] → Judgment.status [anyOf:0] → JudgmentStatus [oneOf:2] | 해당 분기 | const="UNCLEAR" | 값에 문제가 있음 | 저장하지 않고 구체화를 묻는다(UNCLEAR, B3, B4) | B3a, B4, B10 |
| RecordWriterInput.judgments[] → Judgment.status [anyOf:0] → JudgmentStatus [oneOf:3] | 해당 분기 | const="CONFLICT" | 표지 없이 기존 답과 다른 값 | 기존 값을 지키고 확인을 묻는다(CONFLICT, C3) | C3, N6, N13 |
| RecordWriterInput.judgments[] → Judgment.status [anyOf:0] → JudgmentStatus [oneOf:4] | 해당 분기 | const="CORRECTION" | 고친 값이 확정됨 | 새 revision으로 저장한다(CORRECTION, C1) | C1, C2, N3b |
| RecordWriterInput.judgments[] → Judgment.status [anyOf:0] → JudgmentStatus [oneOf:5] | 해당 분기 | const="UNKNOWN" | 모름 | 모름도 하나의 응답이라 기록해야 정책대로 다시 묻거나 넘어간다(B7). | B7a, R11, X1 |
| RecordWriterInput.judgments[] → Judgment.status [anyOf:0] → JudgmentStatus [oneOf:6] | 해당 분기 | const="REJECTED" | 거절 | 거절도 하나의 응답이라 기록해야 정책대로 설명하거나 넘어간다(B8). | B8a, S3a, S3b |
| RecordWriterInput.judgments[] → Judgment.status [anyOf:0] → JudgmentStatus [oneOf:7] | 해당 분기 | const="PREREQUISITE_UNMET" | 선행 조건이 정해지지 않았거나 맞지 않는 후속 문항에 대한 말 | 후속 답은 선행 답이 정해진 뒤에만 기록한다. 버리지 않고 판정으로 내는 이유는, 버리면 사용자가 맞게 답해도 응답이 없는 것으로 보여 같은 질문이 끝없이 반복되기 때문이다(B4, C2) | S1a, S2a, S8a |
| RecordWriterInput.judgments[] → Judgment.status [anyOf:1] | 해당 분기 | null | 없음 | 확인-긍정·부정만으로 확인 대기를 받아들이거나 버리는 판정이다(C4a, G10 둘째 턴). 6절 표가 이 판정을 {대상, 상태 없음, 받아들임·버림}으로 내므로, 없음이 "값에 대한 판정이 아님"을 뜻한다. | C4a, X6, G10 |
| RecordWriterInput.judgments[] → Judgment.reasons | 필수 | array | 애매·누락일 때 되물을 이유. | LoRA-B가 무엇을 다시 말해 달라는지 말해야 한다(B2, B3). | B2, B3a, B4 |
| RecordWriterInput.judgments[] → Judgment.reasons[] | 배열 항목 | → Reason |  |  |  |
| RecordWriterInput.judgments[] → Judgment.reasons[] → Reason | 배열 항목 | oneOf(6분기) | 되물을 때 사용자에게 짚어 줄 이유. | LoRA-B가 왜 다시 묻는지 말해야 사용자가 무엇을 고쳐 말할지 안다(B2, B3, I1). | B2, B3a, I1a |
| RecordWriterInput.judgments[] → Judgment.reasons[] → Reason [oneOf:0] | 해당 분기 | const="NO_UNIT" | 단위를 말해 달라 | 단위를 말해 달라고 해야 사용자가 무엇을 덧붙일지 안다("두 번" → "일주일에 두 번"). | B3b |
| RecordWriterInput.judgments[] → Judgment.reasons[] → Reason [oneOf:1] | 해당 분기 | const="OUT_OF_RANGE" | 값이 가능한 범위를 벗어났다 | 가능한 범위를 벗어났다고 알려야 사용자가 잘못 말했는지 다시 본다("서른 시간"). | B3a, S3d |
| RecordWriterInput.judgments[] → Judgment.reasons[] → Reason [oneOf:2] | 해당 분기 | const="AMBIGUOUS" | 하나로 말해 달라 | 하나로 말해 달라고 해야 범위 값을 하나의 값으로 고쳐 말한다("두세 병"). | B10, C8a, N10, S7b |
| RecordWriterInput.judgments[] → Judgment.reasons[] → Reason [oneOf:3] | 해당 분기 | const="MISMATCH" | 앞 답과 맞지 않는다 | 앞 답과 맞지 않는다고 알려야 사용자가 둘 중 어느 쪽을 고칠지 안다(B4). | B4, S2b, S6a, S7c |
| RecordWriterInput.judgments[] → Judgment.reasons[] → Reason [oneOf:4] | 해당 분기 | const="UNRECOGNIZED" | 알아듣지 못했다 | 알아듣지 못했다고 해야 사용자가 같은 말을 다시 한다(구체화와 하는 말이 다르다, I1). | I1a, I1b, J7a, N14, R12 |
| RecordWriterInput.judgments[] → Judgment.reasons[] → Reason [oneOf:5] | 해당 분기 | const="MISSING_SLOT" | 빠진 부분이 있다 | 빠진 부분이 있다고 해야 이미 말한 것을 다시 말하지 않고 빠진 것만 답한다(B2). | B2, E3b, R1, S8b |
| RecordWriterInput.judgments[] → Judgment.value_now | 필수 | anyOf(2분기) | 정상·정정·충돌일 때 표준 값. | 정상·정정이면 저장할 값, 충돌이면 확인 대기에 둘 값이다. 판정에 있어야 저장 판단이 값 규칙을 몰라도 쓴다. | A2, B1, C1 |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:0] | 해당 분기 | → Value |  |  |  |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:0] → Value | 해당 분기 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:0] → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:0] → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:0] → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:0] → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:0] → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:0] → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:0] → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:0] → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:0] → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| RecordWriterInput.judgments[] → Judgment.value_now [anyOf:1] | 해당 분기 | null | 없음 | 정상·정정·충돌이 아니어서 저장할 표준 값이 없는 판정이다(B7a 모름, B3a 애매, C4a 확인 응답만). 7절 1이 값을 쓰는 동작을 이 값이 있을 때만 낸다. | B7a, B3a, C4a |
| RecordWriterInput.judgments[] → Judgment.said_value | 필수 | anyOf(2분기) | 애매일 때 항목의 원문 값. 같은 슬롯의 다른 값 여럿이면 " / "로 잇는다. | 되물을 때 사용자가 한 말을 그대로 짚는다(B3 "두세 병이라고 하셨는데"). | B3a, B10, N10 |
| RecordWriterInput.judgments[] → Judgment.said_value [anyOf:0] | 해당 분기 | string; minLength=1 |  |  |  |
| RecordWriterInput.judgments[] → Judgment.said_value [anyOf:1] | 해당 분기 | null | 없음 | 애매가 아닌 판정이다(B1 정상, B7a 모름). 8-2절 11이 구체화 요청에만 이 값을 말할 값으로 쓰므로, 없음이면 되물을 때 짚을 원문이 없다. | B1, B7a |
| RecordWriterInput.judgments[] → Judgment.pending_handling | 필수 | oneOf(4분기) | 이 판정이 그 슬롯 확인 대기에 하는 일. | 확인 대기를 둘지, 받아들일지, 버릴지를 저장 판단에 알린다. | C3, C4a, C4b |
| RecordWriterInput.judgments[] → Judgment.pending_handling [oneOf:0] | 해당 분기 | const="CREATE" | 새 충돌 값을 확인 대기에 둔다(있던 것은 대체) | 표지 없이 다른 값을 말했으므로 기존 값을 지키고 새 값을 확인 대기에 둔다. 있던 확인 대기는 새 값으로 바뀐다. | C3, N6, N13 |
| RecordWriterInput.judgments[] → Judgment.pending_handling [oneOf:1] | 해당 분기 | const="ACCEPT" | 확인 대기 값을 현재값으로 | 확인 대기 값이 맞다는 응답이므로 그 값을 현재값으로 올리게 한다. | C4a, N3b, S2e |
| RecordWriterInput.judgments[] → Judgment.pending_handling [oneOf:2] | 해당 분기 | const="DROP" | 확인 대기를 지운다 | 기존 답이 맞다는 응답("아니요", 기존 값을 다시 말함)이거나 정정·모름·거절로 확인이 필요 없어졌으므로 확인 대기를 지우게 한다. | C4b, N3a, R9 |
| RecordWriterInput.judgments[] → Judgment.pending_handling [oneOf:3] | 해당 분기 | const="NONE" | 확인 대기에 손대지 않음 | 확인 대기가 없거나 이 판정(애매·누락 등)이 확인 대기를 건드리지 않음을 분명히 해 저장 판단이 손대지 않게 한다. | A2, B1, B3a |
| RecordWriterInput.judgments[] → Judgment.target_pending_ids | 필수 | array | 받아들임·버림일 때 그 확인 대기 ID. 문항 전체 모름·거절이 여럿을 버리면 여럿. | 받아들이거나 버릴 확인 대기를 ID로 가리켜야, 그 사이 같은 슬롯에 생긴 다른 확인 대기를 잘못 처리하지 않는다. | C4a, N17, X2 |
| RecordWriterInput.judgments[] → Judgment.target_pending_ids[] | 배열 항목 | → PendingId |  |  |  |
| RecordWriterInput.judgments[] → Judgment.target_pending_ids[] → PendingId | 배열 항목 | string; minLength=1 | 저장 판단이 확인 대기를 둘 때 새로 만드는, 세션 안에서 겹치지 않는 값(예: UUID). | "네"가 어느 확인 대기에 대한 답인지 상태 판정이 이 ID로 잇는다. 같은 슬롯에 새 충돌 값이 와서 확인 대기가 바뀌면 이전 확인에 대한 "네"가 새 값을 받아들이지 않게 한다(C4). | C3, C4a, N13 |
| RecordWriterInput.judgments[] → Judgment.mismatched_slots | 필수 | array | 사유에 "다른 답과 맞지 않음"이 있을 때 상대 슬롯. | Plan이 상대 값을 말할 값에 담아 두 값을 함께 짚게 한다(B4). | B4, S2b, S6a |
| RecordWriterInput.judgments[] → Judgment.mismatched_slots[] | 배열 항목 | → SlotRef |  |  |  |
| RecordWriterInput.judgments[] → Judgment.mismatched_slots[] → SlotRef | 배열 항목 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| RecordWriterInput.judgments[] → Judgment.mismatched_slots[] → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| RecordWriterInput.judgments[] → Judgment.mismatched_slots[] → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| RecordWriterInput.judgments[] → Judgment.mismatched_slots[] → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| RecordWriterInput.judgments[] → Judgment.mismatched_slots[] → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| RecordWriterInput.judgments[] → Judgment.risk_rule | 필수 | anyOf(2분기) | 이번 값이 있을 때 정규화·검증의 표시를 옮긴다. | Plan이 즉시 위험이면 멈추고, 저장 판단이 위험 표시를 남긴다(G3, G4). | G3, G4 |
| RecordWriterInput.judgments[] → Judgment.risk_rule [anyOf:0] | 해당 분기 | → RiskResponse |  |  |  |
| RecordWriterInput.judgments[] → Judgment.risk_rule [anyOf:0] → RiskResponse | 해당 분기 | oneOf(2분기) | 위험 기준에 해당하는 답에 할 일. | 바로 멈춰야 하는 답과 결과에만 표시할 답을 나눈다(G3, G4). | G3, G4, G6b |
| RecordWriterInput.judgments[] → Judgment.risk_rule [anyOf:0] → RiskResponse [oneOf:0] | 해당 분기 | const="IMMEDIATE" | 바로 멈추고 직원을 부름 | 그 답 자체가 위급하면(죽고 싶은 생각 = 예) 바로 멈추고 직원을 불러야 한다. | G3, G6b |
| RecordWriterInput.judgments[] → Judgment.risk_rule [anyOf:0] → RiskResponse [oneOf:1] | 해당 분기 | const="ON_RESULT" | 계속하고 결과에 표시 | 위험하지만 지금 멈출 정도는 아닌 답(높은 혈압)은 문진을 이어 가고 결과에 표시해 의료진이 본다. | G4 |
| RecordWriterInput.judgments[] → Judgment.risk_rule [anyOf:1] | 해당 분기 | null | 없음 | 이번 값이 없거나 그 값이 위험 기준에 걸리지 않은 판정이다(B1, B7a). 8-1 규칙 1이 즉시 위험 기준이 있을 때만 멈추므로, 없음이 "이 판정으로는 멈추지 않음"이다. | B1, B7a |
| RecordWriterInput.judgments[] → Judgment.value_metadata | 선택 | → ValueMetadata | 해당 값의 정밀도와 근거. 생략은 미수집이며 exact로 간주하지 않는다. | 정규화·판정·저장·확인 후보·응답 재료에서 정밀도와 근거가 사라지지 않아야 한다. | T1, T2 |
| RecordWriterInput.judgments[] → Judgment.value_metadata → ValueMetadata | 선택 | object; additionalProperties=False | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | T1, T2 |
| RecordWriterInput.judgments[] → Judgment.value_metadata → ValueMetadata.precision | 필수 | → Precision | 값이 exact(단일 확정 표현), approximate(근사 표현), unspecified(정밀도 미확보)인지 전달한다. 범위 중간값의 저장 허용 여부는 결정하지 않는다. | 같은 숫자라도 단일 확정 표현과 근사 표현을 구별하여 저장·재질문·응답 재료에서 정보가 사라지지 않아야 한다. | T1, T2 |
| RecordWriterInput.judgments[] → Judgment.value_metadata → ValueMetadata.precision → Precision | 필수 | string; enum=["exact", "approximate", "unspecified"] | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | T1 |
| RecordWriterInput.judgments[] → Judgment.value_metadata → ValueMetadata.evidence | 필수 | array | 원문 근거 목록. 빈 목록은 근거가 확보되지 않았음을 뜻하며 근거가 없다는 업무 판정을 뜻하지 않는다. | 복수 구절의 합산·정정·비교는 근거 하나로 축약하면 정보가 사라진다. | T1, T2 |
| RecordWriterInput.judgments[] → Judgment.value_metadata → ValueMetadata.evidence[] | 배열 항목 | → Evidence |  |  |  |
| RecordWriterInput.judgments[] → Judgment.value_metadata → ValueMetadata.evidence[] → Evidence | 배열 항목 | object; additionalProperties=False | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| RecordWriterInput.judgments[] → Judgment.value_metadata → ValueMetadata.evidence[] → Evidence.turn_index | 필수 | integer; minimum=0 | 세션 내 원문 발화의 턴 순번. Framework가 부여하며 0/1 시작 기준은 세션에서 일관되게 적용한다. | 현재 발화와 과거 발화의 근거를 혼동하지 않아야 한다. | T1, T2 |
| RecordWriterInput.judgments[] → Judgment.value_metadata → ValueMetadata.evidence[] → Evidence.start | 필수 | integer; minimum=0 | 원문에서 근거가 시작하는 포함 위치. 위치 단위는 offset_unit으로 명시한다. | 같은 구절이 원문에 반복되어도 어느 부분을 사용했는지 식별해야 한다. | T1, T2 |
| RecordWriterInput.judgments[] → Judgment.value_metadata → ValueMetadata.evidence[] → Evidence.end | 필수 | integer; minimum=0 | 원문에서 근거가 끝나는 제외 위치. start 이상이어야 한다. 순서와 text 길이의 일관성은 정적 자료 무결성 검사로 확인한다. | 원문 근거의 정확한 범위를 복원할 수 있어야 한다. | T1, T2 |
| RecordWriterInput.judgments[] → Judgment.value_metadata → ValueMetadata.evidence[] → Evidence.offset_unit | 필수 | string; enum=["unicode_code_point", "utf16_code_unit", "utf8_byte"] | 위치 단위: unicode_code_point, utf16_code_unit, utf8_byte. 서로 다른 런타임의 위치를 조용히 혼용하지 않는다. | Unicode 문자, UTF-16 코드 단위, UTF-8 바이트 위치는 같은 숫자가 아닐 수 있다. | T1, T2 |
| RecordWriterInput.judgments[] → Judgment.value_metadata → ValueMetadata.evidence[] → Evidence.text | 필수 | string; minLength=1 | 근거 구절 자체. 원문 일치 여부는 원문을 가진 담당자가 확인한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| RecordWriterInput.judgments[] → Judgment.problem_details | 선택 | array | 판정과 연관된 세부 문제 코드·대상. 생략은 세부 설명 미수집이다. | 판정 경계를 통과할 때 정형 검사에서 발견한 사유 정보를 잃지 않아야 한다. | T9 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] | 배열 항목 | → ProblemDetail |  |  |  |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail | 배열 항목 | object; additionalProperties=False | 문제의 넓은 분류를 유지하면서 세부 사유 코드와 관련 슬롯을 보존한다. 세부 코드는 등록된 문제 코드표로 합의하며 이 자료형만으로 업무 판정을 수행하지 않는다. | 문제의 넓은 분류를 유지하면서 세부 사유 코드와 관련 슬롯을 보존한다. 세부 코드는 등록된 문제 코드표로 합의하며 이 자료형만으로 업무 판정을 수행하지 않는다. | T9 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.category | 필수 | → Problem | 기존의 넓은 문제 분류. 세부 code와 구분한다. | 문제의 넓은 분류를 유지하면서 세부 사유 코드와 관련 슬롯을 보존한다. 세부 코드는 등록된 문제 코드표로 합의하며 이 자료형만으로 업무 판정을 수행하지 않는다. | T9 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.category → Problem | 필수 | oneOf(5분기) | 정규화·검증이 항목 값에서 찾은 문제. | 값을 저장할 수 없는 이유를 상태 판정에 사실로 넘겨, 판정이 값 규칙을 다시 알 필요가 없게 한다. | B3a, B3b, B4, R16 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.category → Problem [oneOf:0] | 해당 분기 | const="NO_UNIT" | 단위가 둘 이상인 슬롯에 단위 없이 숫자만 말함 | 어느 단위인지 정할 수 없어 되묻는다(B3 "두 번이요") | B3b |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.category → Problem [oneOf:1] | 해당 분기 | const="OUT_OF_RANGE" | 그 단위의 범위(단위 정의의 범위)를 벗어난 값 | 잘못 듣거나 잘못 말한 값을 저장하지 않는다(B3 "서른 시간") | B3a, S3d |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.category → Problem [oneOf:2] | 해당 분기 | const="AMBIGUOUS" | 범위 값이나 여러 값 | "두세 병"처럼 값이 하나로 정해지지 않으면 저장할 수 없어 되물어야 한다(B3). | B10, C8a, R10, S7b |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.category → Problem [oneOf:3] | 해당 분기 | const="MISMATCH" | 선행 조건으로 이어진 다른 답과 모순 | 선행 조건으로 이어진 두 답이 모순이면("안 마셔요" + "소주 두 병") 어느 쪽도 저장할 수 없어 둘 다 짚어 되묻는다(B4). | B4, S2b, S6a, S7c |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.category → Problem [oneOf:4] | 해당 분기 | const="UNKNOWN_TARGET" | 문항 정의에 없는 문항·슬롯을 가리킴 | 답 계열 항목은 저장할 곳이 없어 무관으로 다루고, 요청·위험 신호는 대상만 없는 것으로 보고 그 의도대로 다룬다(K9, 6절 규칙 8). | R16, X8, X9 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T9 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.refs | 필수 | array | 문제와 관련된 구조화된 슬롯 목록. 반복 행과 필드까지 식별한다. | 같은 문항의 여러 반복 행 중 실제 문제 대상을 구별해야 한다. | T9 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.refs[] | 배열 항목 | → SlotRef |  |  |  |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.refs[] → SlotRef | 배열 항목 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.refs[] → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.refs[] → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.refs[] → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.refs[] → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.message | 필수 | anyOf(2분기) | 사람의 진단을 위한 보조 설명. 제어 코드나 사용자에게 그대로 읽을 문장이 아니다. | 문제의 넓은 분류를 유지하면서 세부 사유 코드와 관련 슬롯을 보존한다. 세부 코드는 등록된 문제 코드표로 합의하며 이 자료형만으로 업무 판정을 수행하지 않는다. | T9 |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.message [anyOf:0] | 해당 분기 | string; minLength=1 |  |  |  |
| RecordWriterInput.judgments[] → Judgment.problem_details[] → ProblemDetail.message [anyOf:1] | 해당 분기 | null | 해당 payload 미확보 또는 이 결과에서 해당 없음. 생략과는 구별한다. | 문제의 넓은 분류를 유지하면서 세부 사유 코드와 관련 슬롯을 보존한다. 세부 코드는 등록된 문제 코드표로 합의하며 이 자료형만으로 업무 판정을 수행하지 않는다. | T9 |
| RecordWriterInput.judgments[] → Judgment [allOf:0] | 해당 분기 | if; then |  |  |  |
| RecordWriterInput.judgments[] → Judgment [allOf:0] [if] | 조건 |  |  |  |  |
| RecordWriterInput.judgments[] → Judgment [allOf:0] [if].value_metadata | 필수 |  | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| RecordWriterInput.judgments[] → Judgment [allOf:0] [if].value_metadata.precision | 선택 | enum=["exact", "approximate"] | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| RecordWriterInput.judgments[] → Judgment [allOf:0] [then] | 조건 |  |  |  |  |
| RecordWriterInput.judgments[] → Judgment [allOf:0] [then].value_now | 선택 |  | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| RecordWriterInput.invalidated_questions | 필수 | array | 상태 판정 · 무효화 대상 문항. | 선행 답이 바뀐 문항의 후속 기록을 지우는 저장 결정(무효화)을 내야 한다. | C2, S6c |
| RecordWriterInput.invalidated_questions[] | 배열 항목 | → QuestionId |  |  |  |
| RecordWriterInput.invalidated_questions[] → QuestionId | 배열 항목 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| RecordWriterInput.question_slots | 필수 | array | 문항 정의 저장소 · 문항 전체 판정의 문항과 무효화 대상 문항의 슬롯 전부. | 응답 기록은 슬롯 단위라 문항 전체 판정과 무효화 대상 문항을 슬롯으로 펼쳐야 저장 결정을 낼 수 있다. | B7a, C2 |
| RecordWriterInput.question_slots[] | 배열 항목 | object; additionalProperties=False | 문항과 슬롯 ID들. | 문항마다 칸이 달라 문항 단위 판정과 무효화를 칸으로 펼친다. | B7a, C2 |
| RecordWriterInput.question_slots[].question_id | 필수 | → QuestionId | 문항. | 문항 단위 판정을 칸 단위 저장 결정으로 펼치려면 문항과 칸 목록이 짝지어 있어야 한다. | B7a, C2 |
| RecordWriterInput.question_slots[].question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| RecordWriterInput.question_slots[].slot_ids | 필수 | array; minItems=1 | 슬롯들. | 펼칠 칸 목록이다. 응답 기록은 칸 단위다. | B7a, C2 |
| RecordWriterInput.question_slots[].slot_ids[] | 배열 항목 | string; minLength=1 | 대상 문항에 등록된 슬롯 식별자 하나. | 문항 전체 판정과 무효화를 슬롯별 저장 결정으로 펼친다. | B7a, C2 |
| RecordWriterInput.target_records | 필수 | array | 기록 저장소 · 기록 대상 슬롯마다 현재값과 확인 대기(턴 시작). 기록이 없으면 현재값 없음, 확인 대기 없음. | 첫 저장인지 새 revision인지, 지울 기록이 있는지, 받아들일 값과 위험 표시. | C1, B1, C4a |
| RecordWriterInput.target_records[] | 배열 항목 | object; additionalProperties=False | 슬롯·현재값·확인 대기. | 슬롯마다 기록이 다르다. 기록 대상 슬롯만 받아 필요 없는 기록에 의존하지 않는다. | C1, C2, B1, C4a, S8b |
| RecordWriterInput.target_records[].slot | 필수 | → SlotRef | 저장 판단이 current_value·pending을 읽고 쓰기 결정을 적용할 대상 슬롯 식별자. | 어느 칸의 기록인지 있어야 그 칸의 판정과 맞춰 첫 저장인지 새 revision인지 정한다. | C1, C2 |
| RecordWriterInput.target_records[].slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| RecordWriterInput.target_records[].slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| RecordWriterInput.target_records[].slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| RecordWriterInput.target_records[].slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| RecordWriterInput.target_records[].slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| RecordWriterInput.target_records[].current_value | 필수 | → CurrentValue | 현재값. | 첫 저장인지 새 revision인지, 지울 기록이 있는지. | C1, B1, C2 |
| RecordWriterInput.target_records[].current_value → CurrentValue | 필수 | oneOf(4분기) | 슬롯의 지금 기록: 답(값) / 모름 / 거절 / 없음. | 모름·거절은 빈 칸과 다르다(다시 묻지 않거나 정책대로 묻는다, B7, B8). | B1, B7b, C2 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0] | 해당 분기 | object; additionalProperties=False | 확정한 답을 answer 필드로 감싼 기록. 모름·거절 표지와 구별되는 값 분기다. | 답을 받은 칸이다. 이 값이 결과로 넘어가고 같음·다름 비교의 기준이 된다. | B1, C1 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0].answer | 필수 | → Value | 이 슬롯에 확정된 답. 선택지 문자열 또는 수·단위 객체이며 상세 제약은 해당 문항 정의로 검사한다. | 답 값을 모름·거절·없음과 모양으로 구분한다. | B1, C1 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0].answer → Value | 필수 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:1] | 해당 분기 | const="UNKNOWN_RECORD" | 모름. | 모른다고 한 칸이다. 빈 칸과 달리 정책대로만 다시 묻는다. | B7b, C8c, X7 |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:2] | 해당 분기 | const="REFUSAL_RECORD" | 거절. | 답하지 않겠다고 한 칸이다. 빈 칸과 달리 정책대로만 다시 묻는다. | B8b, N8a |
| RecordWriterInput.target_records[].current_value → CurrentValue [oneOf:3] | 해당 분기 | const="NONE" | 아직 없음. | 아직 답이 없는 칸은 열린 문항 계산에서 물을 대상이 된다. | C2, S1c, S6a |
| RecordWriterInput.target_records[].pending | 필수 | anyOf(2분기) | 확인 대기. | 받아들임이면 이 확인 대기의 값과 위험 표시를 현재값으로 옮기고, 버림이면 지울 것이 있는지 안다. | C4a, S8b |
| RecordWriterInput.target_records[].pending [anyOf:0] | 해당 분기 | → PendingRecord |  |  |  |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord | 해당 분기 | object; additionalProperties=False | 확인을 기다리는 새 값. | 충돌 값을 바로 저장하지 않고 확인을 받는다(C3). | C4a, C3 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.pending_id | 필수 | → PendingId | 이 슬롯의 현재 확인 대기를 식별하는 ID. 확인 응답을 특정 대기 값과 연결한다. | 다음 턴의 "네"가 이 확인 대기에 대한 것인지 맞춰 본다. | C4a, X6, C3 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.pending_id → PendingId | 필수 | string; minLength=1 | 저장 판단이 확인 대기를 둘 때 새로 만드는, 세션 안에서 겹치지 않는 값(예: UUID). | "네"가 어느 확인 대기에 대한 답인지 상태 판정이 이 ID로 잇는다. 같은 슬롯에 새 충돌 값이 와서 확인 대기가 바뀌면 이전 확인에 대한 "네"가 새 값을 받아들이지 않게 한다(C4). | C3, C4a, N13 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value | 필수 | → Value | 새 값. | 받아들이면 이 값이 현재값이 되고, 끝까지 안 풀리면 결과에 "풀리지 않은 답"으로 넘어간다. | C4a, C3, S8b |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value → Value | 필수 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.risk_mark | 필수 | anyOf(2분기) | 그 값의 위험 기준. | 받아들일 때 이 위험 표시가 현재값의 위험 표시로 그대로 옮겨진다. | G10 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.risk_mark [anyOf:0] | 해당 분기 | → RiskResponse |  |  |  |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.risk_mark [anyOf:0] → RiskResponse | 해당 분기 | oneOf(2분기) | 위험 기준에 해당하는 답에 할 일. | 바로 멈춰야 하는 답과 결과에만 표시할 답을 나눈다(G3, G4). | G3, G4, G6b |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.risk_mark [anyOf:0] → RiskResponse [oneOf:0] | 해당 분기 | const="IMMEDIATE" | 바로 멈추고 직원을 부름 | 그 답 자체가 위급하면(죽고 싶은 생각 = 예) 바로 멈추고 직원을 불러야 한다. | G3, G6b |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.risk_mark [anyOf:0] → RiskResponse [oneOf:1] | 해당 분기 | const="ON_RESULT" | 계속하고 결과에 표시 | 위험하지만 지금 멈출 정도는 아닌 답(높은 혈압)은 문진을 이어 가고 결과에 표시해 의료진이 본다. | G4 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.risk_mark [anyOf:1] | 해당 분기 | null | 없음 | 위험 기준이 없는 슬롯의 확인 대기다(C3·C4a의 Q2.개비). 9-2절 표가 받아들일 때 이 표시를 현재값의 위험 표시로 옮기므로, 없음이 "받아들여도 위험 표시가 생기지 않음"이다(G10과 대비). | C3, C4a |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata | 선택 | → ValueMetadata | 해당 값의 정밀도와 근거. 생략은 미수집이며 exact로 간주하지 않는다. | 정규화·판정·저장·확인 후보·응답 재료에서 정밀도와 근거가 사라지지 않아야 한다. | T1, T2 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata | 선택 | object; additionalProperties=False | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | T1, T2 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.precision | 필수 | → Precision | 값이 exact(단일 확정 표현), approximate(근사 표현), unspecified(정밀도 미확보)인지 전달한다. 범위 중간값의 저장 허용 여부는 결정하지 않는다. | 같은 숫자라도 단일 확정 표현과 근사 표현을 구별하여 저장·재질문·응답 재료에서 정보가 사라지지 않아야 한다. | T1, T2 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.precision → Precision | 필수 | string; enum=["exact", "approximate", "unspecified"] | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | T1 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence | 필수 | array | 원문 근거 목록. 빈 목록은 근거가 확보되지 않았음을 뜻하며 근거가 없다는 업무 판정을 뜻하지 않는다. | 복수 구절의 합산·정정·비교는 근거 하나로 축약하면 정보가 사라진다. | T1, T2 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] | 배열 항목 | → Evidence |  |  |  |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence | 배열 항목 | object; additionalProperties=False | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence.turn_index | 필수 | integer; minimum=0 | 세션 내 원문 발화의 턴 순번. Framework가 부여하며 0/1 시작 기준은 세션에서 일관되게 적용한다. | 현재 발화와 과거 발화의 근거를 혼동하지 않아야 한다. | T1, T2 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence.start | 필수 | integer; minimum=0 | 원문에서 근거가 시작하는 포함 위치. 위치 단위는 offset_unit으로 명시한다. | 같은 구절이 원문에 반복되어도 어느 부분을 사용했는지 식별해야 한다. | T1, T2 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence.end | 필수 | integer; minimum=0 | 원문에서 근거가 끝나는 제외 위치. start 이상이어야 한다. 순서와 text 길이의 일관성은 정적 자료 무결성 검사로 확인한다. | 원문 근거의 정확한 범위를 복원할 수 있어야 한다. | T1, T2 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence.offset_unit | 필수 | string; enum=["unicode_code_point", "utf16_code_unit", "utf8_byte"] | 위치 단위: unicode_code_point, utf16_code_unit, utf8_byte. 서로 다른 런타임의 위치를 조용히 혼용하지 않는다. | Unicode 문자, UTF-16 코드 단위, UTF-8 바이트 위치는 같은 숫자가 아닐 수 있다. | T1, T2 |
| RecordWriterInput.target_records[].pending [anyOf:0] → PendingRecord.value_metadata → ValueMetadata.evidence[] → Evidence.text | 필수 | string; minLength=1 | 근거 구절 자체. 원문 일치 여부는 원문을 가진 담당자가 확인한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| RecordWriterInput.target_records[].pending [anyOf:1] | 해당 분기 | null | 없음 | 확인 대기가 없는 기록 대상 슬롯이다(B1 첫 저장, C1 새 revision). 7절 1의 두 동작은 확인 대기를 보지 않는다. | B1, C1 |

## output: StoreResult

계약 상태: current. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.

원본: [Schema](../../contracts/components/record_writer/output.schema.json), [의미·근거](../../contracts/components/record_writer/output.fields.yaml)

| 필드·분기 경로 | 필수 여부 | 값 제약·참조 | 무슨 값인가 | 왜 필요한가 | 근거 요구사항 |
|---|---|---|---|---|---|
| StoreResult |  | object; additionalProperties=False | 저장 결정과 저장 결과 요약. | 저장 결정은 기록 저장소가, 요약은 Plan이 받아서 각자 필요한 것만 본다. | A2, C1, C2 |
| StoreResult.store_decisions | 필수 | array | 슬롯별 쓰기. | 기록 저장소가 판단 없이 반영하도록 슬롯별 할 일을 다 정해 보낸다. | A2, C2, C3 |
| StoreResult.store_decisions[] | 배열 항목 | → StoreDecision |  |  |  |
| StoreResult.store_decisions[] → StoreDecision | 배열 항목 | object; additionalProperties=False; allOf(1분기) | 슬롯 하나에 대한 기록 저장소 쓰기. 변경 없는 슬롯은 나오지 않는다. 무효화가 먼저 온다. | 기록 저장소가 판단 없이 그대로 반영하도록, 무엇을 어떤 값으로 할지 슬롯 단위로 다 정해서 보낸다. | A2, C2, C3 |
| StoreResult.store_decisions[] → StoreDecision.slot | 필수 | → SlotRef | 쓸 슬롯. | 응답 기록은 슬롯 단위로 저장되므로 쓰기마다 어느 칸인지 정해져 있어야 한다. | A2, B1, C2 |
| StoreResult.store_decisions[] → StoreDecision.slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| StoreResult.store_decisions[] → StoreDecision.slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| StoreResult.store_decisions[] → StoreDecision.slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| StoreResult.store_decisions[] → StoreDecision.slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| StoreResult.store_decisions[] → StoreDecision.slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| StoreResult.store_decisions[] → StoreDecision.action | 필수 | → StoreAction | 저장 동작. | 저장소는 판단하지 않으므로 이 슬롯에 무엇을 할지(첫 저장, 새 revision, 확인 대기 둠 등)를 받아야 그대로 반영한다. | A2, C2, C3 |
| StoreResult.store_decisions[] → StoreDecision.action → StoreAction | 필수 | oneOf(8분기) | 저장 판단이 슬롯마다 기록 저장소에 시키는 일. | 기록 저장소가 판단 없이 정해진 효과대로만 반영하게 하려면, 무엇을 할지가 동작 하나로 정해져 있어야 한다. | A2, C3, B7a, C2 |
| StoreResult.store_decisions[] → StoreDecision.action → StoreAction [oneOf:0] | 해당 분기 | const="FIRST_WRITE" | 빈 슬롯에 값을 넣음 | 빈 칸에 처음 들어온 답은 이력 없이 현재값만 정한다. | A2, B1, B2 |
| StoreResult.store_decisions[] → StoreDecision.action → StoreAction [oneOf:1] | 해당 분기 | const="NEW_REVISION" | 있던 답을 고침(이전 답은 이력으로) | 고친 답을 저장하되 이전 답을 버리지 않고 이력으로 남겨 결과에 수정 이력이 넘어가게 한다(C1). | C1, C2, H3a |
| StoreResult.store_decisions[] → StoreDecision.action → StoreAction [oneOf:2] | 해당 분기 | const="RECORD_UNKNOWN" | 모름으로 기록 | 모름을 현재값으로 기록해 빈 칸과 구분하고, 그 전 답이 있었으면 이력으로 남긴다. | B7a, R11, S3d |
| StoreResult.store_decisions[] → StoreDecision.action → StoreAction [oneOf:3] | 해당 분기 | const="RECORD_REFUSAL" | 거절로 기록 | 거절을 현재값으로 기록해 모름·빈 칸과 구분하고, 그 전 답이 있었으면 이력으로 남긴다. | B8a, S3a, S3b |
| StoreResult.store_decisions[] → StoreDecision.action → StoreAction [oneOf:4] | 해당 분기 | const="SET_PENDING" | 기존 값은 두고 새 값을 확인 대기에 둠 | 표지 없이 다른 값을 말하면 잘못 들었을 수도 있으므로 기존 값을 지키고 새 값은 확인을 받을 때까지 따로 둔다(C3). | C3, N6, N13 |
| StoreResult.store_decisions[] → StoreDecision.action → StoreAction [oneOf:5] | 해당 분기 | const="ACCEPT_PENDING" | 확인 대기 값을 현재값으로 | 사용자가 새 값이 맞다고 확인했으므로 확인 대기 값을 현재값으로 올리고 옛 답은 이력으로 남긴다. | C4a, N3b, S2e |
| StoreResult.store_decisions[] → StoreDecision.action → StoreAction [oneOf:6] | 해당 분기 | const="DROP_PENDING" | 확인 대기를 지움 | 확인 대기가 더 필요 없어졌을 때(기존 답이 맞다는 응답, 또는 정정·모름·거절로 그 칸이 따로 정해짐) 확인 대기만 지운다. 현재값은 이 동작으로 바뀌지 않는다. | C4b, N3a, R9 |
| StoreResult.store_decisions[] → StoreDecision.action → StoreAction [oneOf:7] | 해당 분기 | const="INVALIDATE" | 선행 답이 바뀌어 후속 답을 지움 | 선행 답이 바뀌어 맞지 않게 된 후속 답을 지우되 이력으로 남긴다. 지우지 않으면 술을 안 마신다는 사람에게 음주량이 남는다. | C2, N15, R5 |
| StoreResult.store_decisions[] → StoreDecision.value | 필수 | anyOf(2분기) | 첫 저장·새 revision·확인 대기 둠·확인 대기 받아들임일 때. | 저장소는 판단하지 않으므로 넣을 값을 받아야 한다. 받아들임이면 확인 대기의 값을 다시 적어 보내 저장소가 찾지 않게 한다. | A2, C1, C3 |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:0] | 해당 분기 | → Value |  |  |  |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:0] → Value | 해당 분기 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:0] → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:0] → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:0] → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:0] → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:0] → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:0] → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:0] → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:0] → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:0] → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| StoreResult.store_decisions[] → StoreDecision.value [anyOf:1] | 해당 분기 | null | 없음 | 넣을 값이 없는 동작이다: 무효화(C2), 확인 대기 버림(C4b), 모름 기록(B7b), 거절 기록(B8b). 9-2절 표가 이 동작들의 현재값을 없음·모름·거절로 정하므로 저장소가 값을 받을 필요가 없다. | C2, C4b, B7b, B8b |
| StoreResult.store_decisions[] → StoreDecision.pending_id | 필수 | anyOf(2분기) | 확인 대기 둠이면 새로 만든 ID, 받아들임·버림이면 그 ID. | 받아들이거나 버릴 때 어느 확인 대기인지 맞춰 보고, 새로 둘 때는 다음 턴의 "네"가 이 ID로 이어진다. | C3, C4a, C4b |
| StoreResult.store_decisions[] → StoreDecision.pending_id [anyOf:0] | 해당 분기 | → PendingId |  |  |  |
| StoreResult.store_decisions[] → StoreDecision.pending_id [anyOf:0] → PendingId | 해당 분기 | string; minLength=1 | 저장 판단이 확인 대기를 둘 때 새로 만드는, 세션 안에서 겹치지 않는 값(예: UUID). | "네"가 어느 확인 대기에 대한 답인지 상태 판정이 이 ID로 잇는다. 같은 슬롯에 새 충돌 값이 와서 확인 대기가 바뀌면 이전 확인에 대한 "네"가 새 값을 받아들이지 않게 한다(C4). | C3, C4a, N13 |
| StoreResult.store_decisions[] → StoreDecision.pending_id [anyOf:1] | 해당 분기 | null | 없음 | 확인 대기를 다루지 않는 동작이다(B1 첫 저장, C1 새 revision). 7절 3이 확인 대기 둠마다 ID를 새로 만들므로, 없음이 "이 쓰기는 확인 대기와 상관없음"이다. | B1, C1 |
| StoreResult.store_decisions[] → StoreDecision.risk_mark | 필수 | anyOf(2분기) | 값을 저장하거나 확인 대기에 두거나 받아들일 때 그 값의 위험 기준(받아들임이면 확인 대기의 위험 표시). | 결과 전달이 위험 답을 표시한다(G4). | G3, G4 |
| StoreResult.store_decisions[] → StoreDecision.risk_mark [anyOf:0] | 해당 분기 | → RiskResponse |  |  |  |
| StoreResult.store_decisions[] → StoreDecision.risk_mark [anyOf:0] → RiskResponse | 해당 분기 | oneOf(2분기) | 위험 기준에 해당하는 답에 할 일. | 바로 멈춰야 하는 답과 결과에만 표시할 답을 나눈다(G3, G4). | G3, G4, G6b |
| StoreResult.store_decisions[] → StoreDecision.risk_mark [anyOf:0] → RiskResponse [oneOf:0] | 해당 분기 | const="IMMEDIATE" | 바로 멈추고 직원을 부름 | 그 답 자체가 위급하면(죽고 싶은 생각 = 예) 바로 멈추고 직원을 불러야 한다. | G3, G6b |
| StoreResult.store_decisions[] → StoreDecision.risk_mark [anyOf:0] → RiskResponse [oneOf:1] | 해당 분기 | const="ON_RESULT" | 계속하고 결과에 표시 | 위험하지만 지금 멈출 정도는 아닌 답(높은 혈압)은 문진을 이어 가고 결과에 표시해 의료진이 본다. | G4 |
| StoreResult.store_decisions[] → StoreDecision.risk_mark [anyOf:1] | 해당 분기 | null | 없음 | 위험 기준에 걸리지 않은 값을 저장하거나 값을 쓰지 않는 동작이다(B1 Q5.시간 7, C2 무효화). 9-2절 표의 "받은 것"이 곧 이 값이라, 없음이 응답 기록의 위험 표시를 비운다. | B1, C2 |
| StoreResult.store_decisions[] → StoreDecision.value_metadata | 선택 | → ValueMetadata | 해당 값의 정밀도와 근거. 생략은 미수집이며 exact로 간주하지 않는다. | 정규화·판정·저장·확인 후보·응답 재료에서 정밀도와 근거가 사라지지 않아야 한다. | T1, T2 |
| StoreResult.store_decisions[] → StoreDecision.value_metadata → ValueMetadata | 선택 | object; additionalProperties=False | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | T1, T2 |
| StoreResult.store_decisions[] → StoreDecision.value_metadata → ValueMetadata.precision | 필수 | → Precision | 값이 exact(단일 확정 표현), approximate(근사 표현), unspecified(정밀도 미확보)인지 전달한다. 범위 중간값의 저장 허용 여부는 결정하지 않는다. | 같은 숫자라도 단일 확정 표현과 근사 표현을 구별하여 저장·재질문·응답 재료에서 정보가 사라지지 않아야 한다. | T1, T2 |
| StoreResult.store_decisions[] → StoreDecision.value_metadata → ValueMetadata.precision → Precision | 필수 | string; enum=["exact", "approximate", "unspecified"] | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | T1 |
| StoreResult.store_decisions[] → StoreDecision.value_metadata → ValueMetadata.evidence | 필수 | array | 원문 근거 목록. 빈 목록은 근거가 확보되지 않았음을 뜻하며 근거가 없다는 업무 판정을 뜻하지 않는다. | 복수 구절의 합산·정정·비교는 근거 하나로 축약하면 정보가 사라진다. | T1, T2 |
| StoreResult.store_decisions[] → StoreDecision.value_metadata → ValueMetadata.evidence[] | 배열 항목 | → Evidence |  |  |  |
| StoreResult.store_decisions[] → StoreDecision.value_metadata → ValueMetadata.evidence[] → Evidence | 배열 항목 | object; additionalProperties=False | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| StoreResult.store_decisions[] → StoreDecision.value_metadata → ValueMetadata.evidence[] → Evidence.turn_index | 필수 | integer; minimum=0 | 세션 내 원문 발화의 턴 순번. Framework가 부여하며 0/1 시작 기준은 세션에서 일관되게 적용한다. | 현재 발화와 과거 발화의 근거를 혼동하지 않아야 한다. | T1, T2 |
| StoreResult.store_decisions[] → StoreDecision.value_metadata → ValueMetadata.evidence[] → Evidence.start | 필수 | integer; minimum=0 | 원문에서 근거가 시작하는 포함 위치. 위치 단위는 offset_unit으로 명시한다. | 같은 구절이 원문에 반복되어도 어느 부분을 사용했는지 식별해야 한다. | T1, T2 |
| StoreResult.store_decisions[] → StoreDecision.value_metadata → ValueMetadata.evidence[] → Evidence.end | 필수 | integer; minimum=0 | 원문에서 근거가 끝나는 제외 위치. start 이상이어야 한다. 순서와 text 길이의 일관성은 정적 자료 무결성 검사로 확인한다. | 원문 근거의 정확한 범위를 복원할 수 있어야 한다. | T1, T2 |
| StoreResult.store_decisions[] → StoreDecision.value_metadata → ValueMetadata.evidence[] → Evidence.offset_unit | 필수 | string; enum=["unicode_code_point", "utf16_code_unit", "utf8_byte"] | 위치 단위: unicode_code_point, utf16_code_unit, utf8_byte. 서로 다른 런타임의 위치를 조용히 혼용하지 않는다. | Unicode 문자, UTF-16 코드 단위, UTF-8 바이트 위치는 같은 숫자가 아닐 수 있다. | T1, T2 |
| StoreResult.store_decisions[] → StoreDecision.value_metadata → ValueMetadata.evidence[] → Evidence.text | 필수 | string; minLength=1 | 근거 구절 자체. 원문 일치 여부는 원문을 가진 담당자가 확인한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| StoreResult.store_decisions[] → StoreDecision [allOf:0] | 해당 분기 | if; then |  |  |  |
| StoreResult.store_decisions[] → StoreDecision [allOf:0] [if] | 조건 |  |  |  |  |
| StoreResult.store_decisions[] → StoreDecision [allOf:0] [if].value_metadata | 필수 |  | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| StoreResult.store_decisions[] → StoreDecision [allOf:0] [if].value_metadata.precision | 선택 | enum=["exact", "approximate"] | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| StoreResult.store_decisions[] → StoreDecision [allOf:0] [then] | 조건 |  |  |  |  |
| StoreResult.store_decisions[] → StoreDecision [allOf:0] [then].value | 선택 |  | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| StoreResult.store_summary | 필수 | → StoreSummary | 바뀐 것. | Plan이 저장 동작을 해석하지 않고도 무엇이 바뀌었는지 알도록 결과만 요약해 넘긴다. | C1, C4b, N15 |
| StoreResult.store_summary → StoreSummary | 필수 | object; additionalProperties=False | 이번 저장 결정으로 무엇이 바뀌었는지. | Plan은 저장 결정을 해석하지 않고 결과만 보고 알릴 것을 정한다. 저장 동작이 바뀌어도 Plan은 바뀌지 않는다. | C1, C4b, N15 |
| StoreResult.store_summary → StoreSummary.changed_slots | 필수 | array | 현재값이 답으로 바뀐 슬롯들. | 답이 새로 들어오거나 바뀐 칸을 알아야 Plan이 "정정 받았음"을 알리고 방금 받은 값을 말한다. | C1, B2, N13 |
| StoreResult.store_summary → StoreSummary.changed_slots[] | 배열 항목 | → ChangedSlot |  |  |  |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot | 배열 항목 | object; additionalProperties=False | 현재값이 답으로 바뀐 슬롯. | Plan이 "정정 받았음"을 알리고 방금 저장한 값을 말한다(C1). | C1, B2, N13 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.slot | 필수 | → SlotRef | 바뀐 슬롯. | Plan이 "정정 받았음"을 알릴 때 어느 문항의 어느 칸이 바뀌었는지 말해야 한다. | C1, C2, N15 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value | 필수 | anyOf(2분기) | 바뀌기 전 답. 없었으면 없음. | "열 개에서 스무 개로"처럼 알린다(C1). | C1, C2, N13 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:0] | 해당 분기 | → Value |  |  |  |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:0] → Value | 해당 분기 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:0] → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:0] → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:0] → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:0] → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:0] → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:0] → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:0] → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:0] → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:0] → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.previous_value [anyOf:1] | 해당 분기 | null | 없음 | 고치기 전 답이 없던 슬롯이다(B1 첫 저장, N11b 정정 표지로 처음 답함). 8-2절 10의 정정 받았음이 "열 개에서 스무 개로"처럼 말하려면 이전 값이 있어야 하고, 없으면 그 말을 하지 않는다. | B1, N11b |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.new_value | 필수 | → Value | 바뀐 뒤 답. | Plan이 방금 저장한 값을 말하고 정정 받았음의 새 값으로 알린다(B2, C1). | C1, B2, E3b |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.new_value → Value | 필수 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.new_value → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.new_value → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.new_value → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.new_value → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.new_value → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.new_value → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.new_value → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.new_value → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.new_value → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.kind | 필수 | oneOf(2분기) | 첫 답인지 고친 것인지. | 첫 답에는 "정정 받았음"을 알리지 않는다. | C1, B2, B1 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.kind [oneOf:0] | 해당 분기 | const="FIRST_ANSWER" | 빈 슬롯에 들어감 | 빈 칸에 들어간 첫 답이다. 고친 것이 아니므로 "정정 받았음"을 알리지 않는다. | B1, B2, A2 |
| StoreResult.store_summary → StoreSummary.changed_slots[] → ChangedSlot.kind [oneOf:1] | 해당 분기 | const="CORRECTION" | 있던 답이 바뀜 | 있던 답이 바뀐 것이다. "이전 값에서 새 값으로 고쳤다"고 알려야 사용자가 확인한다. | C1, C4a, N3b |
| StoreResult.store_summary → StoreSummary.unknown_refused_records | 필수 | array | 모름·거절로 기록된 슬롯들. | Plan이 모름·거절 횟수를 세고 정책대로 묻는다(B7, B8). | S3a, S3b, S3d |
| StoreResult.store_summary → StoreSummary.unknown_refused_records[] | 배열 항목 | object; additionalProperties=False | 슬롯과 기록. | 어느 슬롯이 모름·거절이 됐는지 Plan이 횟수를 센다(B7, B8). | S3a, S3d |
| StoreResult.store_summary → StoreSummary.unknown_refused_records[].slot | 필수 | → SlotRef | 기록된 슬롯. | 모름·거절 횟수는 문항마다 세므로 어느 칸이 모름·거절이 됐는지 알아야 한다. | S3a, S3d |
| StoreResult.store_summary → StoreSummary.unknown_refused_records[].slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| StoreResult.store_summary → StoreSummary.unknown_refused_records[].slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| StoreResult.store_summary → StoreSummary.unknown_refused_records[].slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| StoreResult.store_summary → StoreSummary.unknown_refused_records[].slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| StoreResult.store_summary → StoreSummary.unknown_refused_records[].slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| StoreResult.store_summary → StoreSummary.unknown_refused_records[].record | 필수 | oneOf(2분기) | 모름 또는 거절. | 모름과 거절은 수용 시점과 다시 묻는 말(재질문, 설명 후 재질문)이 달라 구분해야 한다. | S3a, S3d |
| StoreResult.store_summary → StoreSummary.unknown_refused_records[].record [oneOf:0] | 해당 분기 | const="UNKNOWN_RECORD" | 모름 | 모름 수용 시점과 비교할 모름 횟수를 센다. | S3d |
| StoreResult.store_summary → StoreSummary.unknown_refused_records[].record [oneOf:1] | 해당 분기 | const="REFUSAL_RECORD" | 거절 | 거절 수용 시점과 비교할 거절 횟수를 센다. | S3a, S3b |
| StoreResult.store_summary → StoreSummary.created_pendings | 필수 | array | 이번에 생긴 확인 대기들. | Plan이 확인 대기 확인을 묻는다(C3). | C3, N13, H3e |
| StoreResult.store_summary → StoreSummary.created_pendings[] | 배열 항목 | object; additionalProperties=False | 새 확인 대기. | 이번 턴에 생긴 확인 대기를 먼저 묻는다(C3). | C3, N13, H3e |
| StoreResult.store_summary → StoreSummary.created_pendings[].slot | 필수 | → SlotRef | 확인 대기가 생긴 슬롯. | 확인 질문에서 어느 답에 대한 확인인지 말해야 한다. | C3, N13, H3e |
| StoreResult.store_summary → StoreSummary.created_pendings[].slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| StoreResult.store_summary → StoreSummary.created_pendings[].slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| StoreResult.store_summary → StoreSummary.created_pendings[].slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| StoreResult.store_summary → StoreSummary.created_pendings[].slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| StoreResult.store_summary → StoreSummary.created_pendings[].slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| StoreResult.store_summary → StoreSummary.resolved_pendings | 필수 | array | 이번에 없어지거나 바뀐 확인 대기들. | Plan이 "기존 답 유지"를 알리고, 확인 횟수를 이어 셀지 정한다(C4, C8). | C4b, N6, C4a |
| StoreResult.store_summary → StoreSummary.resolved_pendings[] | 배열 항목 | object; additionalProperties=False | 해소된 확인 대기. | 어떻게 풀렸는지에 따라 알릴 것이 다르다(C4). | C4b, R9, N17, C4a, N6 |
| StoreResult.store_summary → StoreSummary.resolved_pendings[].slot | 필수 | → SlotRef | 그 슬롯. | "기존 답 유지"를 알릴 때 어느 칸의 답인지 말해야 한다. | C4b, R9, N17 |
| StoreResult.store_summary → StoreSummary.resolved_pendings[].slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| StoreResult.store_summary → StoreSummary.resolved_pendings[].slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| StoreResult.store_summary → StoreSummary.resolved_pendings[].slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| StoreResult.store_summary → StoreSummary.resolved_pendings[].slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| StoreResult.store_summary → StoreSummary.resolved_pendings[].slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| StoreResult.store_summary → StoreSummary.resolved_pendings[].handling | 필수 | oneOf(3분기) | 어떻게 해소됐는지. | 받아들임은 정정 받았음, 버림은 기존 답 유지를 알리고, 대체는 확인을 이어 묻는다. | C4a, C4b, N6 |
| StoreResult.store_summary → StoreSummary.resolved_pendings[].handling [oneOf:0] | 해당 분기 | const="ACCEPT" | 확인 대기 값이 현재값이 됨 | 새 값이 현재값이 됐으므로 "정정 받았음"을 알린다. | C4a, N3b |
| StoreResult.store_summary → StoreSummary.resolved_pendings[].handling [oneOf:1] | 해당 분기 | const="DROP" | 확인 대기가 지워짐 | 확인 대기가 지워졌다는 사실을 넘긴다. Plan은 현재값이 이번 턴에 바뀌지 않았을 때만 "기존 답 유지"를 알리고, 정정·모름·거절로 버려진 경우는 그 판정대로 알린다. | C4b, R9, C8c |
| StoreResult.store_summary → StoreSummary.resolved_pendings[].handling [oneOf:2] | 해당 분기 | const="REPLACE" | 같은 슬롯의 새 충돌 값으로 바뀜 | 확인 횟수를 이어 센다. 매번 다른 값을 대도 끝없이 묻지 않게(C8) | N6 |
| StoreResult.store_summary → StoreSummary.invalidated_questions | 필수 | array | 이번에 실제로 무효화한 슬롯이 있는 문항. | Plan이 다시 열린 문항을 다룬다(C2). | N15, R5 |
| StoreResult.store_summary → StoreSummary.invalidated_questions[] | 배열 항목 | → QuestionId |  |  |  |
| StoreResult.store_summary → StoreSummary.invalidated_questions[] → QuestionId | 배열 항목 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |

