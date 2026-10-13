<!-- 생성물. 직접 고치지 말 것: python3 work/tools/build.py -->

# Question Bank (문항 정의 저장소)

문진 설계자가 등록한 문항 정의를 버전별로 읽기 전용으로 보관한다.

이 문서는 현재 계약 원본에서 생성한 필드 안내다. 업무 실행·정답 판정의 검증 결과가 아니다. 전체 역할은 [구조 설명](../../../docs/architecture.md), 검사 범위는 [검증 방법](../../../docs/validation.md)에 있다.

## state: QuestionBank

계약 상태: current. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.

원본: [Schema](../../contracts/components/question_bank/state.schema.json), [의미·근거](../../contracts/components/question_bank/state.fields.yaml)

| 필드·분기 경로 | 필수 여부 | 값 제약·참조 | 무슨 값인가 | 왜 필요한가 | 근거 요구사항 |
|---|---|---|---|---|---|
| QuestionBank |  | object; additionalProperties=False | 한 버전의 문항 정의 전체. 운영 중 바뀌지 않는다. | 진행 중인 세션은 처음 버전으로 끝난다(J1). | A1, J1 |
| QuestionBank.version | 필수 | integer; minimum=0 | 버전 번호. | 세션을 만들 때 이 번호로 버전을 고정해, 운영 중 문항이 바뀌어도 진행 중인 세션은 처음 버전으로 끝난다. | J1 |
| QuestionBank.questions | 필수 | array; minItems=1 | 문항들. 동일 문항 정의 저장소 안의 question_id는 유일하다. | 문진할 문항이 적어도 하나 있어야 세션이 시작된다. ID로 문항을 조회할 때 하나의 정의로 결정되어야 한다. | A1, B1 |
| QuestionBank.questions[] | 배열 항목 | → QuestionDef |  |  |  |
| QuestionBank.questions[] → QuestionDef | 배열 항목 | object; additionalProperties=False | 문항 하나. | 문항에 대해 컴포넌트들이 알아야 하는 것(이름, 순서, 선행 조건, 문장, 정책, 칸)을 한곳에서 정한다. 문진 설계자만 써서 코드를 바꾸지 않고 문항을 바꾼다. | A1, B1 |
| QuestionBank.questions[] → QuestionDef.question_id | 필수 | → QuestionId | 식별자. | 모든 컴포넌트가 이 문항을 같은 이름으로 가리킨다. | A1, B1, E1a |
| QuestionBank.questions[] → QuestionDef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| QuestionBank.questions[] → QuestionDef.name | 필수 | string; minLength=1 | 말할 때 쓰는 이름. | LoRA-A가 "담배 답"이 어느 문항인지 알고, LoRA-B가 이름으로 말한다. | G3, C6a, C7a |
| QuestionBank.questions[] → QuestionDef.order | 필수 | integer; minimum=0 | 묻는 순서. | 열린 문항을 이 순서로 묻는다. | B1, A2, B6 |
| QuestionBank.questions[] → QuestionDef.prerequisite | 필수 | anyOf(2분기) | 없으면 항상 묻는다. | 앞 답에 따라 물을 필요가 없는 문항이 있다(안 마시는 사람에게 음주량). 조건이 정의에 있어야 묻지 않는다. | A2, S1a, S2d |
| QuestionBank.questions[] → QuestionDef.prerequisite [anyOf:0] | 해당 분기 | → Prerequisite |  |  |  |
| QuestionBank.questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite | 해당 분기 | object; additionalProperties=False | 이 문항을 묻는 조건: 다른 슬롯의 답이 이 선택지일 때만. | "술 안 마셔요"라고 한 사람에게 술 종류를 묻지 않는다. 선행 답이 모름·거절·없음이면 묻지 않는다(선행 답이 정해진 뒤에 묻는다, 엄격 원칙). | A2, S2d, B4 |
| QuestionBank.questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot | 필수 | → SlotRef | 선행 슬롯. | 어느 칸의 답에 따라 이 문항을 물을지 정해지는지 알아야 한다. | A2, S1a, S2d |
| QuestionBank.questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| QuestionBank.questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| QuestionBank.questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| QuestionBank.questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| QuestionBank.questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| QuestionBank.questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.value | 필수 | string; minLength=1 | 이 선택지일 때만 묻는다. | 선행 답이 이 선택지일 때만 묻는다. 예를 들어 음주 상세는 음주 여부가 마심일 때만 묻는다. | A2, S1a, B4 |
| QuestionBank.questions[] → QuestionDef.prerequisite [anyOf:1] | 해당 분기 | null | 없음 | 선행 조건 없이 항상 묻는 문항이다(Q1, Q5, Q6, Q7, Q8). 8-1 규칙 17의 열린 문항 계산에서 조건을 따지지 않으므로, A1의 첫 질문이 Q1이 되는 근거가 이 없음이다. | A1, B1 |
| QuestionBank.questions[] → QuestionDef.question_sentence | 필수 | string; minLength=1 | 물을 때의 문장. | 다음 문항 묻기에서 LoRA-B가 바탕으로 쓰고, 실패하면 그대로 읽는 문장이다. | J7c, E4, K1 |
| QuestionBank.questions[] → QuestionDef.refusal_explanation | 필수 | string; minLength=1 | 왜 묻는지 설명하는 문장. | 거절한 사람에게 왜 묻는지 검토된 문장으로 설명해야 한다. | B8a |
| QuestionBank.questions[] → QuestionDef.guide_sentences | 필수 | array | 문항별 안내 항목마다 하나(등록 규칙: 모든 문항에 있어야 등록). | "이게 뭐예요?"의 답은 문항마다 달라 문항마다 문장이 있어야 한다. | E1a, E1b |
| QuestionBank.questions[] → QuestionDef.guide_sentences[] | 배열 항목 | → QuestionGuideSentence |  |  |  |
| QuestionBank.questions[] → QuestionDef.guide_sentences[] → QuestionGuideSentence | 배열 항목 | object; additionalProperties=False | 문항별 안내 항목의 이 문항 문장. | "폭음이 뭐예요?"의 답은 문항마다 다르다(E1). | E1a, E1b |
| QuestionBank.questions[] → QuestionDef.guide_sentences[] → QuestionGuideSentence.guide_id | 필수 | string; minLength=1 | 안내 목록의 문항별 항목. | 문항별 안내 항목이 여럿일 수 있어(뜻, 목적) 문장마다 어느 항목 것인지 있어야 한다. | E1a, E1b |
| QuestionBank.questions[] → QuestionDef.guide_sentences[] → QuestionGuideSentence.sentence | 필수 | string; minLength=1 | 등록 문장. | "폭음이 뭐예요?"에 이 문항에 맞게 검토된 문장으로 답한다. | E1a, E1b |
| QuestionBank.questions[] → QuestionDef.affected_followups | 필수 | array | 이 문항 답이 바뀌면 무효가 되는 후속 문항. | 이 문항 답이 바뀌면 지워야 할 후속 문항을 알아야 모순된 답이 남지 않는다. | C2, S6a, S6c |
| QuestionBank.questions[] → QuestionDef.affected_followups[] | 배열 항목 | → QuestionId |  |  |  |
| QuestionBank.questions[] → QuestionDef.affected_followups[] → QuestionId | 배열 항목 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| QuestionBank.questions[] → QuestionDef.policy | 필수 | → Policy | 문항 정책. | 몇 번까지 묻고 언제 넘어갈지가 문항마다 달라야 한다. | B7a, B8a, B10 |
| QuestionBank.questions[] → QuestionDef.policy → Policy | 필수 | object; additionalProperties=False | 문항마다 몇 번까지 묻는지. | 문항별 질문·모름·거절·확인 횟수 기준을 데이터로 전달해야 한다. 횟수 기준을 공통 스키마에 고정하면 문항이나 서비스의 기준이 바뀔 때 계약까지 변경해야 한다. | B7a, B8a, B10 |
| QuestionBank.questions[] → QuestionDef.policy → Policy.question_limit | 필수 | integer; minimum=1 | 쓸 수 있는 답 없이 이 문항을 물을 수 있는 최대 횟수. | 쓸 수 있는 답이 계속 오지 않을 때 이 횟수에 닿으면 건너뛰어 문진이 끝나게 한다. | B10, R1, R18, S8e |
| QuestionBank.questions[] → QuestionDef.policy → Policy.unknown_accept_after | 필수 | integer; minimum=1 | 몇 번째 모름에서 받아들이고 넘어가는지(1이면 첫 모름에 넘어감). | 모름에 한 번 더 기회를 줄 문항과 바로 넘어갈 문항이 다르다. | B7a, B7b, S8d |
| QuestionBank.questions[] → QuestionDef.policy → Policy.refusal_accept_after | 필수 | integer; minimum=1 | 몇 번째 거절에서 받아들이고 넘어가는지. | 거절에 설명하고 다시 물을 문항(자해 질문 등)과 바로 넘어갈 문항이 다르다. | B8a, B8b |
| QuestionBank.questions[] → QuestionDef.repeat_keys | 필수 | array | 이 문항이 줄마다 반복되면 쓸 수 있는 반복 키들. 반복하지 않으면 빈 목록. | 줄이 몇 개까지 생길 수 있는지는 문진 설계자가 정한다. 목록에 없는 키는 정규화가 받지 않는다(V2). | V3, V1 |
| QuestionBank.questions[] → QuestionDef.repeat_keys[] | 배열 항목 | string; minLength=1 | 이 문항에서 허용되는 반복 행 식별자 하나. | 같은 문항의 서로 다른 행에 대한 답을 분리한다. | V3, V1 |
| QuestionBank.questions[] → QuestionDef.slots | 필수 | array; minItems=1 | 답 칸들. 동일 문항 안의 slot_id는 유일하다. 다른 문항은 같은 slot_id를 사용할 수 있다. | 답을 칸 단위로 받으므로 문항마다 적어도 한 칸이 있어야 한다. 문항 ID와 슬롯 ID로 답 칸을 모호함 없이 식별해야 한다. | B1, B2 |
| QuestionBank.questions[] → QuestionDef.slots[] | 배열 항목 | → SlotDef |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef | 배열 항목 | object; additionalProperties=False; allOf(1분기) | 문항의 답 칸 하나. | 칸마다 받을 수 있는 값(단위·선택지), 필수 여부, 위험 기준이 정해져 있어야 정규화가 검사하고 Plan이 묻는다. | B1, B2 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 모든 컴포넌트가 문항 ID와 함께 이 칸을 같은 이름으로 가리킨다. | B1, B2, B6 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units | 필수 | array | 단위 슬롯의 단위들. 선택지 슬롯이면 빈 목록. | 단위 없는 숫자를 그 단위로 볼지(단위가 하나), 단위를 되물을지(둘 이상) 정하고 환산한다. | B3b, C1, B3a |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] | 배열 항목 | → UnitDef |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef | 배열 항목 | object; additionalProperties=False | 슬롯이 받는 단위 하나. | 정규화가 "한 갑" → 20개비, "두 번"(단위 하나) → 주 2회처럼 표준화하려면 단위와 다른 이름·환산이 정의에 있어야 한다(B3, 정규화 규칙 1). | C1, B3a |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.name | 필수 | string; minLength=1 | 단위 이름. 표준 값의 단위로 쓴다. | 표준 값과 범위가 이 이름의 단위로 정해진다. | C1, B3b, B1 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.synonyms | 필수 | array | 같은 단위를 가리키는 말(개 = 개비). | 다른 이름은 다른 단위가 아니므로 "단위 없음"을 만들지 않는다. | C1, C3, C4b |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.synonyms[] | 배열 항목 | string; minLength=1 |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.range | 필수 | anyOf(2분기) | 이 단위로 센 값의 가능한 범위 [최소, 최대]. 환산이 있는 단위면 없음(환산한 단위의 범위를 쓴다). | 잘못 들었거나 잘못 말한 값을 저장하지 않는다(B3 "서른 시간"). 서로 환산되지 않는 단위는 범위가 달라 단위마다 둔다. | B3a |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.range [anyOf:0] | 해당 분기 | array; minItems=2; maxItems=2 |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.range [anyOf:0][] | 배열 항목 | number |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.range [anyOf:1] | 해당 분기 | null | 없음 | 환산이 있는 단위다(문항 정의의 Q2 "갑" → 개비 20배). 5절 1이 환산한 단위의 값으로 표준화하므로 범위도 그 단위 쪽에만 둔다. 여기 범위를 두면 같은 제약이 두 곳에 생긴다. | C3, C1 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to | 필수 | anyOf(2분기) | 다른 단위로 바꿀 수 있으면 그 단위와 배수(갑 → 개비 20). 없으면 없음. | 환산되는 값은 한 단위로 저장해야 같음·다름과 범위를 비교할 수 있다. | C1 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to [anyOf:0] | 해당 분기 | object; additionalProperties=False | 단위와 배수. | 환산은 바꿀 단위와 배수 두 값이 있어야 계산된다. | C1 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to [anyOf:0].unit | 필수 | string; minLength=1 | 바꿀 단위 이름. | 환산한 값이 어느 단위가 되는지 있어야 저장 값의 단위가 정해진다(갑 → 개비). | C1 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to [anyOf:0].factor | 필수 | number | 이 단위 1이 그 단위 몇인지. | 이 단위 하나가 바꿀 단위로 얼마인지 있어야 수를 바꾼다(한 갑 = 20개비). | C1 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to [anyOf:0].unit_code | 선택 | string; minLength=1 | 환산 대상 단위의 등록 코드. unit은 표시 이름이다. | 환산 대상의 표시 이름과 식별 코드를 따로 전달해야 한다. | T3 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to [anyOf:1] | 해당 분기 | null | 없음 | 다른 단위로 바꿀 수 없는 단위다(Q5 "시간", Q3b "주 n회"·"월 n회"). 서로 환산되지 않는 단위가 있어서 없음이 필요하다. | B1, B3a |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.code | 선택 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 단위 이름을 변경해도 단위의 식별 코드가 유지되어야 한다. | T3 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.choices | 필수 | array | 선택지 슬롯의 선택지. 단위 슬롯이면 빈 목록. | 답을 정해진 말로 표준화한다(B1). | B1, C8a, S7b |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.choices[] | 배열 항목 | string; minLength=1 |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.yes_no_map | 필수 | anyOf(2분기) | "네"·"아니요"가 이 슬롯의 어떤 선택지인지. 예/아니요로 답할 수 있는 선택 슬롯만. | "폭음 하세요?"에 "네"는 값이다(B9). 이 정의가 없으면 "네"를 확인 응답과 구분할 수 없다. | B9, S4d, N16 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.yes_no_map [anyOf:0] | 해당 분기 | object; additionalProperties=False | 두 선택지. | "네"와 "아니요"가 각각 어느 선택지인지 둘 다 있어야 한다. | B9, S4d, N16 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.yes_no_map [anyOf:0].yes | 필수 | string; minLength=1 | "네"에 해당하는 선택지. | "폭음 하세요?" "네" → 예(B9). | B9, S4d |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.yes_no_map [anyOf:0].no | 필수 | string; minLength=1 | "아니요"에 해당하는 선택지. | "술 드세요?" "아니요" → 안 마심. | N16 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.yes_no_map [anyOf:1] | 해당 분기 | null | 없음 | 예·아니요로 답할 수 없는 슬롯이다(Q2.개비, Q5.시간). 4절 3이 이 대응이 있는 슬롯에서만 단독 "네"를 값으로 보므로, 없음이 C4a의 확인 응답 "네"와 B9의 답 "네"를 가른다. | C3, B1 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.required | 필수 | boolean | 꼭 받아야 하는 칸인지. | 열린 문항과 빠진 슬롯을 정한다(B2). 다른 답에 따라 필요 여부가 바뀌는 칸은 같은 문항에 두지 않는다(등록 규칙). | B2, H1 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.reask_sentence | 필수 | string; minLength=1 | 이 칸만 다시 물을 때의 문장. | 빠진 칸이나 애매한 칸만 다시 물을 때 쓸 검토된 문장이 칸마다 있어야 한다. | B2 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule | 필수 | anyOf(2분기) | 있으면 그 조건과 대응. 없으면 없음. | 답에 따라 바로 멈추거나 결과에 표시해야 하는 칸이 있다. 기준이 정의에 있어야 정규화가 판단한다. | G3, G4 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] | 해당 분기 | → RiskRule |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule | 해당 분기 | object; additionalProperties=False | 답이 위험한 조건과 대응. | 죽고 싶은 생각 "예"는 바로 멈추고, 혈압 190은 결과에 표시한다(G3, G4). 조건을 문장으로 두면 정규화가 기계적으로 판단할 수 없어 비교 연산과 값으로 둔다. | G3, G4 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.operator | 필수 | oneOf(2분기) | 비교 방법. | 선택지는 같음, 수치는 크기 비교로 위험을 판단한다(G3 "예", G4 혈압 이상). | G3, G4 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.operator [oneOf:0] | 해당 분기 | const="=" | 같음 | 선택지 슬롯은 특정 선택지(예: 죽고 싶은 생각 = 예)일 때만 위험하다. | G3 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.operator [oneOf:1] | 해당 분기 | const=">=" | 이상 | 수치 슬롯은 기준 이상(예: 수축기 180 이상)일 때 위험하다. | G4 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value | 필수 | → Value | 비교할 값(선택지 또는 단위 값). | 답과 같은 모양이어야 바로 비교한다. | G3, G4 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value | 필수 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.response | 필수 | → RiskResponse | 해당하면 할 일. | 같은 위험이라도 바로 멈출지 결과에만 표시할지는 문항마다 의료진이 정해야 한다. | G3, G4, G6b |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.response → RiskResponse | 필수 | oneOf(2분기) | 위험 기준에 해당하는 답에 할 일. | 바로 멈춰야 하는 답과 결과에만 표시할 답을 나눈다(G3, G4). | G3, G4, G6b |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.response → RiskResponse [oneOf:0] | 해당 분기 | const="IMMEDIATE" | 바로 멈추고 직원을 부름 | 그 답 자체가 위급하면(죽고 싶은 생각 = 예) 바로 멈추고 직원을 불러야 한다. | G3, G6b |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.response → RiskResponse [oneOf:1] | 해당 분기 | const="ON_RESULT" | 계속하고 결과에 표시 | 위험하지만 지금 멈출 정도는 아닌 답(높은 혈압)은 문진을 이어 가고 결과에 표시해 의료진이 본다. | G4 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:1] | 해당 분기 | null | 없음 | 위험 기준이 없는 슬롯이다(Q5.시간, Q2.개비). 기준이 있는 것은 Q6.여부(즉시)와 Q7의 두 칸(결과 표시)뿐이라(G3, G4), 없음이 보통 칸임을 뜻한다. | B1, C3 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.choice_catalog | 선택 | array; minItems=1 | 등록된 선택지 코드·표시 이름·표현 목록. 사용하면 choices는 빈 목록이고 yes_no_map은 등록 코드를 참조한다. | 선택지 이름과 안정적인 코드를 따로 정의하고 두 선택지 목록의 우선순위를 모호하게 두지 않아야 한다. | T3 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] | 배열 항목 | → ChoiceDef |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] → ChoiceDef | 배열 항목 | object; additionalProperties=False | 선택지의 안정적인 코드와 표시 이름·등록 표현을 분리한다. 실제 코드표의 예시는 공식 문항 코드가 아니다. | 선택지의 안정적인 코드와 표시 이름·등록 표현을 분리한다. 실제 코드표의 예시는 공식 문항 코드가 아니다. | T3 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] → ChoiceDef.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T3 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] → ChoiceDef.label | 필수 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T3 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] → ChoiceDef.synonyms | 필수 | array | 표시 이름 외의 등록된 표현 목록. 별도 임의 해석 정책을 정의하지 않는다. | 선택지의 안정적인 코드와 표시 이름·등록 표현을 분리한다. 실제 코드표의 예시는 공식 문항 코드가 아니다. | T3 |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] → ChoiceDef.synonyms[] | 배열 항목 | string; minLength=1 |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef [allOf:0] | 해당 분기 | if; then |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef [allOf:0] [if] | 조건 |  |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef [allOf:0] [then] | 조건 |  |  |  |  |
| QuestionBank.questions[] → QuestionDef.slots[] → SlotDef [allOf:0] [then].choices | 선택 | maxItems=0 | choice_catalog 사용 시 문자열 선택지 목록은 비워 한 정의만 사용한다. | 두 목록이 동시에 선택지 정의의 원본이 되지 않아야 한다. | T3 |
| QuestionBank.session_settings | 필수 | → SessionSettings | 설정. | 위험 표현·상한·고정 문장·안내 목록을 기관이 코드 밖에서 정한다. | G2, C8a, E1a |
| QuestionBank.session_settings → SessionSettings | 필수 | object; additionalProperties=False | 문항과 상관없는 설정. | 기관마다 다르게 정할 값을 코드 밖에 둔다. | G2, C8a, F3 |
| QuestionBank.session_settings → SessionSettings.risk_phrases | 필수 | array | 원문에 들어 있으면 위험 신호로 보는 표현. | 모델이 놓친 위급한 말을 잡는다(G2). 의료진이 관리한다. | G2, G9, S3c |
| QuestionBank.session_settings → SessionSettings.risk_phrases[] | 배열 항목 | string; minLength=1 |  |  |  |
| QuestionBank.session_settings → SessionSettings.confirm_limit | 필수 | integer; minimum=1 | 같은 확인 대기를 물을 수 있는 최대 횟수. | 확인 질문에 계속 다른 값을 대도 이 횟수에서 확인을 그만두어 문진이 끝나게 한다. | C8a, C8b, N6, S8e |
| QuestionBank.session_settings → SessionSettings.unrecognized_streak_limit | 필수 | integer; minimum=1 | 이만큼 이어지면 도움 요청. | 알아듣지 못한 턴이 이만큼 이어지면 직원을 부른다. 기관마다 정할 값이다. | F3, R12 |
| QuestionBank.session_settings → SessionSettings.ask_limit | 필수 | integer; minimum=1 | 같은 대상을 풀리지 않은 채 물을 수 있는 최대 횟수. | 정정 요청·미룸·종료 확인·중단 확인처럼 문항 정책이 없는 물음도 같은 것을 끝없이 묻지 않게 하는 상한이다(8-4절 7). | H1, C8d |
| QuestionBank.session_settings → SessionSettings.fixed_sentences | 필수 | array | 행동·알릴 것 종류마다 하나. 의료진이 검토해 등록한다. | 행동·알릴 것마다 쓰는 검토된 문장을 코드 밖에 두어, 문장을 바꿔도 코드가 바뀌지 않게 한다. | G1 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] | 배열 항목 | → FixedSentence |  |  |  |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence | 배열 항목 | object; additionalProperties=False | 종류와 문장. | 의료진·설계자가 검토한 문장을 행동·알릴 것 종류마다 하나씩 코드 밖에 등록해, 문장을 바꿔도 코드가 바뀌지 않게 한다. | G1 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key | 필수 | → FixedSentenceKey | 고정 문장 종류. | Plan이 이번 행동·알릴 것에 맞는 문장을 이 종류로 찾아 문장 재료에 담는다. | G1 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey | 필수 | oneOf(14분기) | 세션 설정에 등록하는 고정 문장의 종류. 실제 문장 선택·생성은 담당 컴포넌트의 책임이다. | 모델이 지어내면 안 되는 문장(위험 안내 등)과 모델이 실패할 때 그대로 읽을 문장이 필요하다(G1, J7). | G1, J3 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:0] | 해당 분기 | const="ASK_REPEAT" | 다시 말씀 요청 때 쓰는 문장 | 알아듣지 못했을 때 할 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, I1a, J7a |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:1] | 해당 분기 | const="OOS_NOTICE" | 문진 밖 발화에 대응하기 위한 등록 문장의 종류. 적절한 수용·지원 불가 표현의 선택은 응답 담당 컴포넌트의 책임이다. | 문진과 상관없는 말을 받을 때의 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, E4, K1 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:2] | 해당 분기 | const="CALL_STAFF" | 도움 요청 때 쓰는 문장 | 직원을 부른다고 알리는 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, F3 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:3] | 해당 분기 | const="FAREWELL" | 종료 인사 때 쓰는 문장 | 마칠 때의 인사을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, H2, F4 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:4] | 해당 분기 | const="ASK_CONFIRM" | 확인 대기 확인 때 쓰는 문장 | 어느 답이 맞는지 확인하는 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, C3, J7d |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:5] | 해당 분기 | const="ASK_CORRECTION_TARGET" | 정정 구체화 때 쓰는 문장 | 무엇을, 어떤 값으로 고칠지 묻는 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, C5, C6a |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:6] | 해당 분기 | const="ASK_FINISH" | 종료 확인 때 쓰는 문장 | 마칠지 묻는 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, H1 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:7] | 해당 분기 | const="RISK_NOTICE" | 위험 안내 때 쓰는 문장 | G1, 의료진 검토 문장만 쓴다 | G1, J3, J9, J8g |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:8] | 해당 분기 | const="RESUME" | 재개 때 쓰는 문장 | 다시 이어 간다는 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, G6a |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:9] | 해당 분기 | const="SURVEY_STOPPED" | 문진 중단 때 쓰는 문장 | 여기서 그만둔다는 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, D5a, F4 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:10] | 해당 분기 | const="WAIT_NOTICE" | 대기 안내 때 쓰는 문장 | 기다리겠다는 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, D2 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:11] | 해당 분기 | const="ASK_STOP" | 중단 확인 때 쓰는 문장 | 정말 그만둘지 묻는 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, D4 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:12] | 해당 분기 | const="STAFF_NOTICE" | 사람 연결 안내 때 쓰는 문장 | 직원을 불렀다는 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, F1 |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.key → FixedSentenceKey [oneOf:13] | 해당 분기 | const="DEFERRED" | 미룸 때 쓰는 문장 | 나중에 묻겠다는 말을 검토된 문장으로 등록해 두어야, LoRA-B가 이를 바탕으로 말하고 실패하면 그대로 읽을 수 있다. | J9, D3a, J7e |
| QuestionBank.session_settings → SessionSettings.fixed_sentences[] → FixedSentence.sentence | 필수 | string; minLength=1 | 검토된 문장. | 위험 안내처럼 지어내면 안 되는 말을 검토된 문장으로 고정한다. | G1 |
| QuestionBank.session_settings → SessionSettings.guide_list | 필수 | array | 안내 항목들. | 사용자가 물을 수 있는 것과 답을 등록해 두어야 정해진 안내만 하고 나머지는 무관으로 다룬다. | E1a, E2, E3a |
| QuestionBank.session_settings → SessionSettings.guide_list[] | 배열 항목 | → GuideItem |  |  |  |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem | 배열 항목 | object; additionalProperties=False | 사용자가 물을 수 있는 것과 그 답. | 목록에 있는 물음만 안내하고 나머지는 무관이다(E1~E4). 항목을 더해도 컴포넌트 입출력은 바뀌지 않는다. | E1a, E2, E3a |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem.guide_id | 필수 | string; minLength=1 | 식별자. | LoRA-A가 이 ID를 골라 내고, Plan이 이 ID로 문장을 찾는다. | E1a, E2, E3a, E3b |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem.selection_criterion | 필수 | string; minLength=1 | LoRA-A가 볼 설명. | LoRA-A가 사용자 물음이 이 항목인지 판단할 기준. 목록에 없으면 무관이다. | E1a, E3a, E3b |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem.per_question | 필수 | boolean | 참이면 문장은 각 문항의 안내 문장에 있다. | 뜻·목적 안내는 문항마다 다르다. | N12, E1b, E2 |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem.sentence | 필수 | anyOf(2분기) | 문항별이 아니면 문장. 문항별이면 없음. | 문항과 상관없는 안내(개인정보 등)는 문장이 하나라 여기에 둔다. | E2, E3a |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem.sentence [anyOf:0] | 해당 분기 | string; minLength=1 |  |  |  |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem.sentence [anyOf:1] | 해당 분기 | null | 없음 | 문항별 안내라 문장이 문항 정의 쪽(QuestionDef.guide_sentences)에 있다(E1a 설명, E1b 목적). 여기에도 문장을 두면 같은 안내의 문장이 두 곳에 생긴다. | E1a, E1b |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem.fill_value | 필수 | anyOf(2분기) | 문장에 넣을 계산 값. 없으면 없음. | 남은 문항 수처럼 세션마다 다른 값을 문장에 넣어야 하는 안내가 있다. | E2, R11 |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem.fill_value [anyOf:0] | 해당 분기 | → FillValue |  |  |  |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem.fill_value [anyOf:0] → FillValue | 해당 분기 | oneOf(1분기) | 안내 문장에 넣을 계산 값의 종류. | "얼마나 남았어요?"의 답은 고정 문장이 아니라 세션마다 계산해야 한다(E2). | E2, R11 |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem.fill_value [anyOf:0] → FillValue [oneOf:0] | 해당 분기 | const="REMAINING_COUNT" | 이번 턴 반영 뒤에 열려 있는 문항의 수. 미룬 문항은 세고, 건너뛴 문항(모름 수용·거절 수용·시도 초과)과 선행 조건이 맞지 않는 문항은 세지 않는다 | "얼마나 남았어요?"의 답은 세션마다 다른 수라 문장에 고정할 수 없고 Plan이 계산해 넣어야 한다. | E2, R11 |
| QuestionBank.session_settings → SessionSettings.guide_list[] → GuideItem.fill_value [anyOf:1] | 해당 분기 | null | 없음 | 세션마다 달라지는 값을 넣지 않는 안내다(E3a 개인정보, E1a 설명). 채울 값이 있는 것은 E2의 "진행"(남은 문항 수)뿐이다. | E3a, E1a |

