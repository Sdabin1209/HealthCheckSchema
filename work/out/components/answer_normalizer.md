<!-- 생성물. 직접 고치지 말 것: python3 work/tools/build.py -->

# Answer Normalizer (정규화·검증)

항목 값을 표준 형태로 바꾸고, 규칙 위반·기존 값과의 같음/다름·빠진 필수 슬롯·선행 조건을 사실로 표시한다.

이 문서는 현재 계약 원본에서 생성한 필드 안내다. 업무 실행·정답 판정의 검증 결과가 아니다. 전체 역할은 [구조 설명](../../../docs/architecture.md), 검사 범위는 [검증 방법](../../../docs/validation.md)에 있다.

## input: AnswerNormalizerInput

계약 상태: current. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.

원본: [Schema](../../contracts/components/answer_normalizer/input.schema.json), [의미·근거](../../contracts/components/answer_normalizer/input.fields.yaml)

| 필드·분기 경로 | 필수 여부 | 값 제약·참조 | 무슨 값인가 | 왜 필요한가 | 근거 요구사항 |
|---|---|---|---|---|---|
| AnswerNormalizerInput |  | object; additionalProperties=False | 항목 목록과 관련 문항의 규칙·현재값·확인 대기·기다리는 답. | 값 규칙을 적용하려면 규칙과 비교할 기존 값이 필요하다. | B1, B3a |
| AnswerNormalizerInput.items | 필수 | array | LoRA-A · 항목 목록. | 표준화하고 검사할 값이 이 항목들에 있다. | B1, B3a |
| AnswerNormalizerInput.items[] | 배열 항목 | → Item |  |  |  |
| AnswerNormalizerInput.items[] → Item | 배열 항목 | object; additionalProperties=False; allOf(1분기) | 발화에서 뽑은 (대상, 값, 원문, 의도) 하나. | 한 발화에 답과 요청이 함께 포함되어도 각각 처리할 수 있도록, 추출한 사실과 의도를 항목 단위로 전달해야 한다. | A2, B1, G8a |
| AnswerNormalizerInput.items[] → Item.item_no | 필수 | integer; minimum=0 | 이번 턴 안에서 항목마다 붙이는 번호(0부터). | 정규화·검증과 상태 판정의 항목별 결과를 원래 항목과 잇는다. 턴을 넘어 쓰지 않는다. | B1, B4, N13 |
| AnswerNormalizerInput.items[] → Item.target | 필수 | anyOf(2분기) | 무엇에 대한 말인지. 정정 의도인데 무엇을 고칠지 모르면 없음. 확인-긍정·부정·위험 신호는 없어도 된다. | 값을 어느 슬롯에 넣을지 정한다. 대상 없이 온 확인 응답은 상태 판정이 직전 응답 지시로 잇는다(C4). | A2, B1, C5 |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] | 해당 분기 | → Target |  |  |  |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target | 해당 분기 | oneOf(2분기) | 슬롯 하나 또는 문항 전체. | 항목·판정·응답 지시가 슬롯과 문항 전체를 같은 자리에서 가리켜야 한다. | A2, R11, S3b |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target [oneOf:0] | 해당 분기 | → SlotRef |  |  |  |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target [oneOf:0] → SlotRef | 해당 분기 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target [oneOf:0] → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target [oneOf:0] → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target [oneOf:0] → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target [oneOf:0] → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target [oneOf:1] | 해당 분기 | → WholeQuestion |  |  |  |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target [oneOf:1] → WholeQuestion | 해당 분기 | object; additionalProperties=False | 문항의 모든 슬롯을 한꺼번에 가리킴. | "술은 잘 모르겠어요"처럼 문항 전체에 대한 모름·거절과, 문항에 대한 안내·나중에가 있다(B7, D3, E1). 저장은 항상 슬롯 단위라 저장 판단이 펼친다. | R11, S3b, N17 |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target [oneOf:1] → WholeQuestion.question_id | 필수 | → QuestionId | 가리키는 문항. | 문항 전체에 대한 말("술은 잘 모르겠어요")은 그 문항의 모든 칸에 펼쳐 기록해야 하므로 어느 문항인지 있어야 한다. | R11, S3b, N17 |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target [oneOf:1] → WholeQuestion.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| AnswerNormalizerInput.items[] → Item.target [anyOf:0] → Target [oneOf:1] → WholeQuestion.whole_question | 필수 | const=true | 항상 true. | 슬롯 대상과 모양으로 구분하기 위해. | R11, S3b, N17 |
| AnswerNormalizerInput.items[] → Item.target [anyOf:1] | 해당 분기 | null | 없음 | 무엇을 고칠지 모르는 정정(C5), 인식불가(I1a), 무관(K1), 위험 신호(G1)에는 값을 넣을 슬롯이 없다. 4절 1이 답함·모름·거절에만 대상을 요구하므로, 없음이 "저장할 곳이 없는 말"을 뜻한다. | C5, I1a, K1, G1 |
| AnswerNormalizerInput.items[] → Item.value | 필수 | anyOf(2분기) | 원문에서 뽑은 값 문자열. 표준화하지 않는다. | 표준화(단위 환산·범위 검사)는 정규화·검증 한 곳에서만 한다. 애매하면 이 문자열 그대로 짚어 되묻는다(B3). | A2, B1, B3a |
| AnswerNormalizerInput.items[] → Item.value [anyOf:0] | 해당 분기 | string; minLength=1 |  |  |  |
| AnswerNormalizerInput.items[] → Item.value [anyOf:1] | 해당 분기 | null | 없음 | 뽑을 값이 없는 항목이다: 값 없는 정정(C6a), 모름(B7a), 나중에(D3a), 사람 요청(F1). 값 없음과 빈 문자열이 같으면 "값을 말하지 않은 정정"을 가려낼 수 없어 C6a가 C1과 섞인다. | C6a, B7a, D3a, F1 |
| AnswerNormalizerInput.items[] → Item.source_text | 필수 | → SourceText | 이 항목에 해당하는 발화 부분. | 애매한 값을 사용자 말 그대로 짚어 되묻고, 판정 근거를 사람이 확인한다(B3). | G8a, G8b, R3 |
| AnswerNormalizerInput.items[] → Item.source_text → SourceText | 필수 | string; minLength=1 | 사용자 발화에서 그대로 옮긴 부분. | 판정 근거를 사람이 확인하고, 애매한 값을 사용자 말 그대로 짚어 되묻기 위해(B3, G1). | F1, G1, G8a |
| AnswerNormalizerInput.items[] → Item.intent | 필수 | → Intent | 공유 어휘 의도 중 하나. | 하려는 일에 따라 처리 경로가 갈린다. | A2, B7a, D1a |
| AnswerNormalizerInput.items[] → Item.intent → Intent | 필수 | oneOf(12분기) | LoRA-A가 항목마다 붙이는, 사용자가 그 말로 하려는 일. | 같은 말도 하려는 일에 따라 저장·되묻기·요청 처리로 갈린다. 하려는 일을 모델이 한 번 정해 두면 뒤의 코드 컴포넌트는 말의 뜻을 다시 해석하지 않는다. | A2, B7a, F1, G1, K1 |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:0] | 해당 분기 | const="ANSWERED_INTENT" | 묻는 문항(또는 다른 문항)에 값을 말함 | 말한 값을 그 슬롯의 답으로 저장하는 경로다. 이 의도가 없으면 답과 요청·잡담을 구분할 수 없다(B1). | A2, B1, B9 |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:1] | 해당 분기 | const="CORRECTION_MARKED" | 앞서 한 답을 고친다는 표지와 함께 말함 | 표지가 있으면 새 값을 확인 없이 고치고, 없으면 확인을 묻는다(C1과 C3을 가르는 유일한 근거) | C1, C2, C5 |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:2] | 해당 분기 | const="CONFIRM_YES" | 확인 질문에 "네" | 확인 대기를 받아들이거나 종료·중단·정정 구체화에 승낙한다(C4, H2, D5) | C4a, D5a, H2 |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:3] | 해당 분기 | const="CONFIRM_NO" | 확인 질문에 "아니요" | 확인 대기를 버리거나 종료·중단·정정 구체화를 거부한다(C4, C9, D5) | C4b, C9a, D5b |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:4] | 해당 분기 | const="SAYS_UNKNOWN" | 모른다고 함 | 모름은 빈 칸과 다르다. 기록해 두어야 정책대로 한 번 더 묻거나 넘어가고, 결과에도 '모름'으로 남는다(B7). | B7a, B7b, R11 |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:5] | 해당 분기 | const="SAYS_REFUSAL" | 답하지 않겠다고 함 | 거절은 모름과 정책이 다르다(왜 묻는지 설명한 뒤 다시 묻는다). 구분하지 않으면 거절한 사람에게 모르냐고 다시 묻게 된다(B8). | B8a, B8b, S3a |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:6] | 해당 분기 | const="PROGRESS_OP" | 반복·대기·나중에·중단 요청 | 답이 아니라 진행에 대한 요청이라 저장하지 않고 응답만 바꾼다(D1~D5) | D1a, D2, D3a, D4 |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:7] | 해당 분기 | const="GUIDE_REQUEST" | 안내 목록에 있는 물음(뜻, 남은 수 등) | 안내 목록에 있는 물음은 검토된 문장으로만 답해야 하므로 무관과 구분해 안내 항목을 골라야 한다(E1~E3). | E1a, E2, E3a |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:8] | 해당 분기 | const="USER_CALLED_STAFF" | 직원을 찾거나 시스템이 할 수 없는 요청 | 직원이 필요한 말을 무관으로 두면 요청이 아무에게도 가지 않는다(F1, F2). | F1, F2, X8 |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:9] | 해당 분기 | const="OUT_OF_SCOPE" | 문진·안내 목록과 상관없는 말 | 저장도 요청도 아니므로 받아 주고 하던 질문을 잇는다(E4, K1~K9) | E4, K1, K9a |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:10] | 해당 분기 | const="UNRECOGNIZED" | 무슨 말인지 알 수 없음 | 다시 말해 달라고 하고, 이어지면 직원을 부른다(I1, F3) | I1a, F3, J7b |
| AnswerNormalizerInput.items[] → Item.intent → Intent [oneOf:11] | 해당 분기 | const="RISK_SIGNAL" | 지금 위급하다는 말 | 위급한 말은 문진보다 먼저 멈추고 직원을 불러야 하므로 다른 의도와 따로 표시한다(G1). | G1, G8a, J3 |
| AnswerNormalizerInput.items[] → Item.progress_op | 필수 | anyOf(2분기) | 의도가 진행 조작일 때만. 나중에는 대상(문항 전체)이 있을 수 있다. | 반복·대기·나중에·중단은 응답이 서로 다르다(D1~D4). | D1a, D2, D3a, D4 |
| AnswerNormalizerInput.items[] → Item.progress_op [anyOf:0] | 해당 분기 | → ProgressOp |  |  |  |
| AnswerNormalizerInput.items[] → Item.progress_op [anyOf:0] → ProgressOp | 해당 분기 | oneOf(4분기) | 진행에 대한 요청의 종류. | 반복은 직전 말을 다시, 대기는 기다림, 나중에는 미룸, 중단은 확인으로 응답이 서로 달라서 어떤 요청인지 구분해야 한다. | D1a, D2, D3a, D4 |
| AnswerNormalizerInput.items[] → Item.progress_op [anyOf:0] → ProgressOp [oneOf:0] | 해당 분기 | const="REPEAT" | 다시 말해 달라 | 직전 말을 다시 들으려는 요청이다. 새로 묻지 않고 같은 말을 되풀이해야 한다. | D1a, D1b, R8 |
| AnswerNormalizerInput.items[] → Item.progress_op [anyOf:0] → ProgressOp [oneOf:1] | 해당 분기 | const="WAIT" | 기다려 달라 | 잠깐 기다려 달라는 요청이다. 다음 질문으로 재촉하지 않아야 한다. | D2, R2, X5 |
| AnswerNormalizerInput.items[] → Item.progress_op [anyOf:0] → ProgressOp [oneOf:2] | 해당 분기 | const="LATER" | 이 문항은 나중에 | 지금 문항을 나중에 하겠다는 요청이다. 다른 것을 먼저 묻고 맨 뒤에 다시 묻는다. | D3a, D3c, N7a |
| AnswerNormalizerInput.items[] → Item.progress_op [anyOf:0] → ProgressOp [oneOf:3] | 해당 분기 | const="STOP" | 그만하겠다 | 그만하겠다는 요청이다. 잘못 들었을 수 있어 바로 끝내지 않고 확인한다. | D4, R4, S5a |
| AnswerNormalizerInput.items[] → Item.progress_op [anyOf:1] | 해당 분기 | null | 없음 | 진행 조작 의도가 아닌 항목이다(B1 답함, B7a 모름). 4절 대체 출력이 "의도가 진행 조작인데 진행 조작이 없으면 인식불가로"를 적용하려면 없음이 값으로 있어야 한다. | B1, B7a |
| AnswerNormalizerInput.items[] → Item.guide_id | 필수 | anyOf(2분기) | 의도가 안내 요청일 때만. 받은 안내 목록 안의 값. | 어느 안내 문장으로 답할지 정한다. 문항에 대한 안내("폭음이 뭐예요?")면 대상(문항 전체)도 채운다(E1). | E1a, E2, E3a |
| AnswerNormalizerInput.items[] → Item.guide_id [anyOf:0] | 해당 분기 | string; minLength=1 | 안내 목록에 등록된 안내 항목 식별자. | 안내 요청을 등록된 안내 문장과 연결한다. | E1a, E2, E3a |
| AnswerNormalizerInput.items[] → Item.guide_id [anyOf:1] | 해당 분기 | null | 없음 | 고른 안내가 없는 항목이다(B1 답함, E4 안내 목록에 없는 물음). 4절 대체 출력이 "의도가 안내 요청인데 ID가 없으면 무관으로"를 판단하는 조건이 이 없음이다. | B1, E4 |
| AnswerNormalizerInput.items[] → Item.evidence | 선택 | array | 현재 발화의 원문 구절과 위치 목록. 턴 번호는 모델이 아니라 Framework가 부여한다. | 같은 원문에서 여러 구절의 합산·정정 근거를 하나로 축약하지 않아야 한다. | T2 |
| AnswerNormalizerInput.items[] → Item.evidence[] | 배열 항목 | → TextSpan |  |  |  |
| AnswerNormalizerInput.items[] → Item.evidence[] → TextSpan | 배열 항목 | object; additionalProperties=False | 모델이 읽은 현재 원문의 구절·위치를 표현한다. 턴 번호는 모델이 만들어 낼 필요가 없다. | 모델이 읽은 현재 원문의 구절·위치를 표현한다. 턴 번호는 모델이 만들어 낼 필요가 없다. | T2 |
| AnswerNormalizerInput.items[] → Item.evidence[] → TextSpan.start | 필수 | integer; minimum=0 | 원문에서 근거가 시작하는 포함 위치. 위치 단위는 offset_unit으로 명시한다. | 같은 구절이 원문에 반복되어도 어느 부분을 사용했는지 식별해야 한다. | T2 |
| AnswerNormalizerInput.items[] → Item.evidence[] → TextSpan.end | 필수 | integer; minimum=0 | 원문에서 근거가 끝나는 제외 위치. start 이상이어야 한다. 순서와 text 길이의 일관성은 정적 자료 무결성 검사로 확인한다. | 원문 근거의 정확한 범위를 복원할 수 있어야 한다. | T2 |
| AnswerNormalizerInput.items[] → Item.evidence[] → TextSpan.offset_unit | 필수 | string; enum=["unicode_code_point", "utf16_code_unit", "utf8_byte"] | 위치 단위: unicode_code_point, utf16_code_unit, utf8_byte. 서로 다른 런타임의 위치를 조용히 혼용하지 않는다. | Unicode 문자, UTF-16 코드 단위, UTF-8 바이트 위치는 같은 숫자가 아닐 수 있다. | T2 |
| AnswerNormalizerInput.items[] → Item.evidence[] → TextSpan.text | 필수 | string; minLength=1 | 근거 구절 자체. 원문 일치 여부는 원문을 가진 담당자가 확인한다. | 모델이 읽은 현재 원문의 구절·위치를 표현한다. 턴 번호는 모델이 만들어 낼 필요가 없다. | T2 |
| AnswerNormalizerInput.items[] → Item [allOf:0] | 해당 분기 | if; then |  |  |  |
| AnswerNormalizerInput.items[] → Item [allOf:0] [if] | 조건 |  |  |  |  |
| AnswerNormalizerInput.items[] → Item [allOf:0] [if].intent | 선택 | enum=["ANSWERED_INTENT"] | 답함 의도에는 대상과 값이 함께 존재해야 한다. Parser 보정 이후 출력과 외부 스키마 검증에서 같은 조건을 강제한다. | 잘못된 조합을 경계 스키마에서 거부하기 위해 필요하다. tests/test_schemas.py의 관계 거부 회귀 테스트로 확인한다. | B1 |
| AnswerNormalizerInput.items[] → Item [allOf:0] [then] | 조건 |  |  |  |  |
| AnswerNormalizerInput.items[] → Item [allOf:0] [then].target | 선택 |  | 답함 의도에는 대상과 값이 함께 존재해야 한다. Parser 보정 이후 출력과 외부 스키마 검증에서 같은 조건을 강제한다. | 잘못된 조합을 경계 스키마에서 거부하기 위해 필요하다. tests/test_schemas.py의 관계 거부 회귀 테스트로 확인한다. | B1 |
| AnswerNormalizerInput.items[] → Item [allOf:0] [then].value | 선택 |  | 답함 의도에는 대상과 값이 함께 존재해야 한다. Parser 보정 이후 출력과 외부 스키마 검증에서 같은 조건을 강제한다. | 잘못된 조합을 경계 스키마에서 거부하기 위해 필요하다. tests/test_schemas.py의 관계 거부 회귀 테스트로 확인한다. | B1 |
| AnswerNormalizerInput.related_questions | 필수 | array | 문항 정의 저장소 · 항목이 가리킨 문항, 기다리는 답의 대상 슬롯이 속한 문항, 그리고 그것들의 선행 조건이 가리키는 문항의 정의. 정의에 없는 문항은 넣지 않는다(정의에 없는 대상 검사에 쓰인다). | 표준화·범위·네아니요·위험 기준·선행 조건 검사(B3, B4, B9, G3). 기다리는 답의 대상 문항까지 와야 5절 4의 "기다리는 답이 확인 대기 확인이고 그 슬롯의 문항이 선행 불충족 조건이면"을 판정할 수 있다(S6c). | B3a, S2d, B4 |
| AnswerNormalizerInput.related_questions[] | 배열 항목 | → QuestionDef |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef | 배열 항목 | object; additionalProperties=False | 문항 하나. | 문항에 대해 컴포넌트들이 알아야 하는 것(이름, 순서, 선행 조건, 문장, 정책, 칸)을 한곳에서 정한다. 문진 설계자만 써서 코드를 바꾸지 않고 문항을 바꾼다. | A1, B1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.question_id | 필수 | → QuestionId | 식별자. | 모든 컴포넌트가 이 문항을 같은 이름으로 가리킨다. | A1, B1, E1a |
| AnswerNormalizerInput.related_questions[] → QuestionDef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| AnswerNormalizerInput.related_questions[] → QuestionDef.name | 필수 | string; minLength=1 | 말할 때 쓰는 이름. | LoRA-A가 "담배 답"이 어느 문항인지 알고, LoRA-B가 이름으로 말한다. | G3, C6a, C7a |
| AnswerNormalizerInput.related_questions[] → QuestionDef.order | 필수 | integer; minimum=0 | 묻는 순서. | 열린 문항을 이 순서로 묻는다. | B1, A2, B6 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.prerequisite | 필수 | anyOf(2분기) | 없으면 항상 묻는다. | 앞 답에 따라 물을 필요가 없는 문항이 있다(안 마시는 사람에게 음주량). 조건이 정의에 있어야 묻지 않는다. | A2, S1a, S2d |
| AnswerNormalizerInput.related_questions[] → QuestionDef.prerequisite [anyOf:0] | 해당 분기 | → Prerequisite |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite | 해당 분기 | object; additionalProperties=False | 이 문항을 묻는 조건: 다른 슬롯의 답이 이 선택지일 때만. | "술 안 마셔요"라고 한 사람에게 술 종류를 묻지 않는다. 선행 답이 모름·거절·없음이면 묻지 않는다(선행 답이 정해진 뒤에 묻는다, 엄격 원칙). | A2, S2d, B4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot | 필수 | → SlotRef | 선행 슬롯. | 어느 칸의 답에 따라 이 문항을 물을지 정해지는지 알아야 한다. | A2, S1a, S2d |
| AnswerNormalizerInput.related_questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| AnswerNormalizerInput.related_questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.prerequisite [anyOf:0] → Prerequisite.value | 필수 | string; minLength=1 | 이 선택지일 때만 묻는다. | 선행 답이 이 선택지일 때만 묻는다. 예를 들어 음주 상세는 음주 여부가 마심일 때만 묻는다. | A2, S1a, B4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.prerequisite [anyOf:1] | 해당 분기 | null | 없음 | 선행 조건 없이 항상 묻는 문항이다(Q1, Q5, Q6, Q7, Q8). 8-1 규칙 17의 열린 문항 계산에서 조건을 따지지 않으므로, A1의 첫 질문이 Q1이 되는 근거가 이 없음이다. | A1, B1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.question_sentence | 필수 | string; minLength=1 | 물을 때의 문장. | 다음 문항 묻기에서 LoRA-B가 바탕으로 쓰고, 실패하면 그대로 읽는 문장이다. | J7c, E4, K1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.refusal_explanation | 필수 | string; minLength=1 | 왜 묻는지 설명하는 문장. | 거절한 사람에게 왜 묻는지 검토된 문장으로 설명해야 한다. | B8a |
| AnswerNormalizerInput.related_questions[] → QuestionDef.guide_sentences | 필수 | array | 문항별 안내 항목마다 하나(등록 규칙: 모든 문항에 있어야 등록). | "이게 뭐예요?"의 답은 문항마다 달라 문항마다 문장이 있어야 한다. | E1a, E1b |
| AnswerNormalizerInput.related_questions[] → QuestionDef.guide_sentences[] | 배열 항목 | → QuestionGuideSentence |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.guide_sentences[] → QuestionGuideSentence | 배열 항목 | object; additionalProperties=False | 문항별 안내 항목의 이 문항 문장. | "폭음이 뭐예요?"의 답은 문항마다 다르다(E1). | E1a, E1b |
| AnswerNormalizerInput.related_questions[] → QuestionDef.guide_sentences[] → QuestionGuideSentence.guide_id | 필수 | string; minLength=1 | 안내 목록의 문항별 항목. | 문항별 안내 항목이 여럿일 수 있어(뜻, 목적) 문장마다 어느 항목 것인지 있어야 한다. | E1a, E1b |
| AnswerNormalizerInput.related_questions[] → QuestionDef.guide_sentences[] → QuestionGuideSentence.sentence | 필수 | string; minLength=1 | 등록 문장. | "폭음이 뭐예요?"에 이 문항에 맞게 검토된 문장으로 답한다. | E1a, E1b |
| AnswerNormalizerInput.related_questions[] → QuestionDef.affected_followups | 필수 | array | 이 문항 답이 바뀌면 무효가 되는 후속 문항. | 이 문항 답이 바뀌면 지워야 할 후속 문항을 알아야 모순된 답이 남지 않는다. | C2, S6a, S6c |
| AnswerNormalizerInput.related_questions[] → QuestionDef.affected_followups[] | 배열 항목 | → QuestionId |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.affected_followups[] → QuestionId | 배열 항목 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| AnswerNormalizerInput.related_questions[] → QuestionDef.policy | 필수 | → Policy | 문항 정책. | 몇 번까지 묻고 언제 넘어갈지가 문항마다 달라야 한다. | B7a, B8a, B10 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.policy → Policy | 필수 | object; additionalProperties=False | 문항마다 몇 번까지 묻는지. | 문항별 질문·모름·거절·확인 횟수 기준을 데이터로 전달해야 한다. 횟수 기준을 공통 스키마에 고정하면 문항이나 서비스의 기준이 바뀔 때 계약까지 변경해야 한다. | B7a, B8a, B10 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.policy → Policy.question_limit | 필수 | integer; minimum=1 | 쓸 수 있는 답 없이 이 문항을 물을 수 있는 최대 횟수. | 쓸 수 있는 답이 계속 오지 않을 때 이 횟수에 닿으면 건너뛰어 문진이 끝나게 한다. | B10, R1, R18, S8e |
| AnswerNormalizerInput.related_questions[] → QuestionDef.policy → Policy.unknown_accept_after | 필수 | integer; minimum=1 | 몇 번째 모름에서 받아들이고 넘어가는지(1이면 첫 모름에 넘어감). | 모름에 한 번 더 기회를 줄 문항과 바로 넘어갈 문항이 다르다. | B7a, B7b, S8d |
| AnswerNormalizerInput.related_questions[] → QuestionDef.policy → Policy.refusal_accept_after | 필수 | integer; minimum=1 | 몇 번째 거절에서 받아들이고 넘어가는지. | 거절에 설명하고 다시 물을 문항(자해 질문 등)과 바로 넘어갈 문항이 다르다. | B8a, B8b |
| AnswerNormalizerInput.related_questions[] → QuestionDef.repeat_keys | 필수 | array | 이 문항이 줄마다 반복되면 쓸 수 있는 반복 키들. 반복하지 않으면 빈 목록. | 줄이 몇 개까지 생길 수 있는지는 문진 설계자가 정한다. 목록에 없는 키는 정규화가 받지 않는다(V2). | V3, V1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.repeat_keys[] | 배열 항목 | string; minLength=1 | 이 문항에서 허용되는 반복 행 식별자 하나. | 같은 문항의 서로 다른 행에 대한 답을 분리한다. | V3, V1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots | 필수 | array; minItems=1 | 답 칸들. 동일 문항 안의 slot_id는 유일하다. 다른 문항은 같은 slot_id를 사용할 수 있다. | 답을 칸 단위로 받으므로 문항마다 적어도 한 칸이 있어야 한다. 문항 ID와 슬롯 ID로 답 칸을 모호함 없이 식별해야 한다. | B1, B2 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] | 배열 항목 | → SlotDef |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef | 배열 항목 | object; additionalProperties=False; allOf(1분기) | 문항의 답 칸 하나. | 칸마다 받을 수 있는 값(단위·선택지), 필수 여부, 위험 기준이 정해져 있어야 정규화가 검사하고 Plan이 묻는다. | B1, B2 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 모든 컴포넌트가 문항 ID와 함께 이 칸을 같은 이름으로 가리킨다. | B1, B2, B6 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units | 필수 | array | 단위 슬롯의 단위들. 선택지 슬롯이면 빈 목록. | 단위 없는 숫자를 그 단위로 볼지(단위가 하나), 단위를 되물을지(둘 이상) 정하고 환산한다. | B3b, C1, B3a |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] | 배열 항목 | → UnitDef |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef | 배열 항목 | object; additionalProperties=False | 슬롯이 받는 단위 하나. | 정규화가 "한 갑" → 20개비, "두 번"(단위 하나) → 주 2회처럼 표준화하려면 단위와 다른 이름·환산이 정의에 있어야 한다(B3, 정규화 규칙 1). | C1, B3a |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.name | 필수 | string; minLength=1 | 단위 이름. 표준 값의 단위로 쓴다. | 표준 값과 범위가 이 이름의 단위로 정해진다. | C1, B3b, B1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.synonyms | 필수 | array | 같은 단위를 가리키는 말(개 = 개비). | 다른 이름은 다른 단위가 아니므로 "단위 없음"을 만들지 않는다. | C1, C3, C4b |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.synonyms[] | 배열 항목 | string; minLength=1 |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.range | 필수 | anyOf(2분기) | 이 단위로 센 값의 가능한 범위 [최소, 최대]. 환산이 있는 단위면 없음(환산한 단위의 범위를 쓴다). | 잘못 들었거나 잘못 말한 값을 저장하지 않는다(B3 "서른 시간"). 서로 환산되지 않는 단위는 범위가 달라 단위마다 둔다. | B3a |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.range [anyOf:0] | 해당 분기 | array; minItems=2; maxItems=2 |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.range [anyOf:0][] | 배열 항목 | number |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.range [anyOf:1] | 해당 분기 | null | 없음 | 환산이 있는 단위다(문항 정의의 Q2 "갑" → 개비 20배). 5절 1이 환산한 단위의 값으로 표준화하므로 범위도 그 단위 쪽에만 둔다. 여기 범위를 두면 같은 제약이 두 곳에 생긴다. | C3, C1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to | 필수 | anyOf(2분기) | 다른 단위로 바꿀 수 있으면 그 단위와 배수(갑 → 개비 20). 없으면 없음. | 환산되는 값은 한 단위로 저장해야 같음·다름과 범위를 비교할 수 있다. | C1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to [anyOf:0] | 해당 분기 | object; additionalProperties=False | 단위와 배수. | 환산은 바꿀 단위와 배수 두 값이 있어야 계산된다. | C1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to [anyOf:0].unit | 필수 | string; minLength=1 | 바꿀 단위 이름. | 환산한 값이 어느 단위가 되는지 있어야 저장 값의 단위가 정해진다(갑 → 개비). | C1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to [anyOf:0].factor | 필수 | number | 이 단위 1이 그 단위 몇인지. | 이 단위 하나가 바꿀 단위로 얼마인지 있어야 수를 바꾼다(한 갑 = 20개비). | C1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to [anyOf:0].unit_code | 선택 | string; minLength=1 | 환산 대상 단위의 등록 코드. unit은 표시 이름이다. | 환산 대상의 표시 이름과 식별 코드를 따로 전달해야 한다. | T3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.convert_to [anyOf:1] | 해당 분기 | null | 없음 | 다른 단위로 바꿀 수 없는 단위다(Q5 "시간", Q3b "주 n회"·"월 n회"). 서로 환산되지 않는 단위가 있어서 없음이 필요하다. | B1, B3a |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.units[] → UnitDef.code | 선택 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 단위 이름을 변경해도 단위의 식별 코드가 유지되어야 한다. | T3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.choices | 필수 | array | 선택지 슬롯의 선택지. 단위 슬롯이면 빈 목록. | 답을 정해진 말로 표준화한다(B1). | B1, C8a, S7b |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.choices[] | 배열 항목 | string; minLength=1 |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.yes_no_map | 필수 | anyOf(2분기) | "네"·"아니요"가 이 슬롯의 어떤 선택지인지. 예/아니요로 답할 수 있는 선택 슬롯만. | "폭음 하세요?"에 "네"는 값이다(B9). 이 정의가 없으면 "네"를 확인 응답과 구분할 수 없다. | B9, S4d, N16 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.yes_no_map [anyOf:0] | 해당 분기 | object; additionalProperties=False | 두 선택지. | "네"와 "아니요"가 각각 어느 선택지인지 둘 다 있어야 한다. | B9, S4d, N16 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.yes_no_map [anyOf:0].yes | 필수 | string; minLength=1 | "네"에 해당하는 선택지. | "폭음 하세요?" "네" → 예(B9). | B9, S4d |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.yes_no_map [anyOf:0].no | 필수 | string; minLength=1 | "아니요"에 해당하는 선택지. | "술 드세요?" "아니요" → 안 마심. | N16 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.yes_no_map [anyOf:1] | 해당 분기 | null | 없음 | 예·아니요로 답할 수 없는 슬롯이다(Q2.개비, Q5.시간). 4절 3이 이 대응이 있는 슬롯에서만 단독 "네"를 값으로 보므로, 없음이 C4a의 확인 응답 "네"와 B9의 답 "네"를 가른다. | C3, B1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.required | 필수 | boolean | 꼭 받아야 하는 칸인지. | 열린 문항과 빠진 슬롯을 정한다(B2). 다른 답에 따라 필요 여부가 바뀌는 칸은 같은 문항에 두지 않는다(등록 규칙). | B2, H1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.reask_sentence | 필수 | string; minLength=1 | 이 칸만 다시 물을 때의 문장. | 빠진 칸이나 애매한 칸만 다시 물을 때 쓸 검토된 문장이 칸마다 있어야 한다. | B2 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule | 필수 | anyOf(2분기) | 있으면 그 조건과 대응. 없으면 없음. | 답에 따라 바로 멈추거나 결과에 표시해야 하는 칸이 있다. 기준이 정의에 있어야 정규화가 판단한다. | G3, G4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] | 해당 분기 | → RiskRule |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule | 해당 분기 | object; additionalProperties=False | 답이 위험한 조건과 대응. | 죽고 싶은 생각 "예"는 바로 멈추고, 혈압 190은 결과에 표시한다(G3, G4). 조건을 문장으로 두면 정규화가 기계적으로 판단할 수 없어 비교 연산과 값으로 둔다. | G3, G4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.operator | 필수 | oneOf(2분기) | 비교 방법. | 선택지는 같음, 수치는 크기 비교로 위험을 판단한다(G3 "예", G4 혈압 이상). | G3, G4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.operator [oneOf:0] | 해당 분기 | const="=" | 같음 | 선택지 슬롯은 특정 선택지(예: 죽고 싶은 생각 = 예)일 때만 위험하다. | G3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.operator [oneOf:1] | 해당 분기 | const=">=" | 이상 | 수치 슬롯은 기준 이상(예: 수축기 180 이상)일 때 위험하다. | G4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value | 필수 | → Value | 비교할 값(선택지 또는 단위 값). | 답과 같은 모양이어야 바로 비교한다. | G3, G4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value | 필수 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.value → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.response | 필수 | → RiskResponse | 해당하면 할 일. | 같은 위험이라도 바로 멈출지 결과에만 표시할지는 문항마다 의료진이 정해야 한다. | G3, G4, G6b |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.response → RiskResponse | 필수 | oneOf(2분기) | 위험 기준에 해당하는 답에 할 일. | 바로 멈춰야 하는 답과 결과에만 표시할 답을 나눈다(G3, G4). | G3, G4, G6b |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.response → RiskResponse [oneOf:0] | 해당 분기 | const="IMMEDIATE" | 바로 멈추고 직원을 부름 | 그 답 자체가 위급하면(죽고 싶은 생각 = 예) 바로 멈추고 직원을 불러야 한다. | G3, G6b |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:0] → RiskRule.response → RiskResponse [oneOf:1] | 해당 분기 | const="ON_RESULT" | 계속하고 결과에 표시 | 위험하지만 지금 멈출 정도는 아닌 답(높은 혈압)은 문진을 이어 가고 결과에 표시해 의료진이 본다. | G4 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.risk_rule [anyOf:1] | 해당 분기 | null | 없음 | 위험 기준이 없는 슬롯이다(Q5.시간, Q2.개비). 기준이 있는 것은 Q6.여부(즉시)와 Q7의 두 칸(결과 표시)뿐이라(G3, G4), 없음이 보통 칸임을 뜻한다. | B1, C3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.choice_catalog | 선택 | array; minItems=1 | 등록된 선택지 코드·표시 이름·표현 목록. 사용하면 choices는 빈 목록이고 yes_no_map은 등록 코드를 참조한다. | 선택지 이름과 안정적인 코드를 따로 정의하고 두 선택지 목록의 우선순위를 모호하게 두지 않아야 한다. | T3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] | 배열 항목 | → ChoiceDef |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] → ChoiceDef | 배열 항목 | object; additionalProperties=False | 선택지의 안정적인 코드와 표시 이름·등록 표현을 분리한다. 실제 코드표의 예시는 공식 문항 코드가 아니다. | 선택지의 안정적인 코드와 표시 이름·등록 표현을 분리한다. 실제 코드표의 예시는 공식 문항 코드가 아니다. | T3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] → ChoiceDef.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] → ChoiceDef.label | 필수 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] → ChoiceDef.synonyms | 필수 | array | 표시 이름 외의 등록된 표현 목록. 별도 임의 해석 정책을 정의하지 않는다. | 선택지의 안정적인 코드와 표시 이름·등록 표현을 분리한다. 실제 코드표의 예시는 공식 문항 코드가 아니다. | T3 |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef.choice_catalog[] → ChoiceDef.synonyms[] | 배열 항목 | string; minLength=1 |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef [allOf:0] | 해당 분기 | if; then |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef [allOf:0] [if] | 조건 |  |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef [allOf:0] [then] | 조건 |  |  |  |  |
| AnswerNormalizerInput.related_questions[] → QuestionDef.slots[] → SlotDef [allOf:0] [then].choices | 선택 | maxItems=0 | choice_catalog 사용 시 문자열 선택지 목록은 비워 한 정의만 사용한다. | 두 목록이 동시에 선택지 정의의 원본이 되지 않아야 한다. | T3 |
| AnswerNormalizerInput.current_values | 필수 | array | 기록 저장소 · 관련 슬롯의 현재값(턴 시작). | 기존 답과 같은지, 선행 답이 무엇인지, 필수 슬롯이 비었는지(C3, B2). | C3, B2, S2d |
| AnswerNormalizerInput.current_values[] | 배열 항목 | object; additionalProperties=False | 슬롯과 현재값. | 칸마다 현재값이 달라 칸별로 비교해야 한다. | C3, B2, X2, S2d |
| AnswerNormalizerInput.current_values[].slot | 필수 | → SlotRef | 이 current_value와 비교할 이번 턴의 대상 슬롯 식별자. | 어느 칸의 현재값인지 있어야 같은 칸의 새 값과 비교한다. | C3, B2 |
| AnswerNormalizerInput.current_values[].slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| AnswerNormalizerInput.current_values[].slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| AnswerNormalizerInput.current_values[].slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| AnswerNormalizerInput.current_values[].slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| AnswerNormalizerInput.current_values[].slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| AnswerNormalizerInput.current_values[].current_value | 필수 | → CurrentValue | 현재값. | 같음·다름 비교와 선행 답 판단의 기준. | C3, X2, S2d |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue | 필수 | oneOf(4분기) | 슬롯의 지금 기록: 답(값) / 모름 / 거절 / 없음. | 모름·거절은 빈 칸과 다르다(다시 묻지 않거나 정책대로 묻는다, B7, B8). | B1, B7b, C2 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0] | 해당 분기 | object; additionalProperties=False | 확정한 답을 answer 필드로 감싼 기록. 모름·거절 표지와 구별되는 값 분기다. | 답을 받은 칸이다. 이 값이 결과로 넘어가고 같음·다름 비교의 기준이 된다. | B1, C1 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0].answer | 필수 | → Value | 이 슬롯에 확정된 답. 선택지 문자열 또는 수·단위 객체이며 상세 제약은 해당 문항 정의로 검사한다. | 답 값을 모름·거절·없음과 모양으로 구분한다. | B1, C1 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0].answer → Value | 필수 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:0].answer → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:1] | 해당 분기 | const="UNKNOWN_RECORD" | 모름. | 모른다고 한 칸이다. 빈 칸과 달리 정책대로만 다시 묻는다. | B7b, C8c, X7 |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:2] | 해당 분기 | const="REFUSAL_RECORD" | 거절. | 답하지 않겠다고 한 칸이다. 빈 칸과 달리 정책대로만 다시 묻는다. | B8b, N8a |
| AnswerNormalizerInput.current_values[].current_value → CurrentValue [oneOf:3] | 해당 분기 | const="NONE" | 아직 없음. | 아직 답이 없는 칸은 열린 문항 계산에서 물을 대상이 된다. | C2, S1c, S6a |
| AnswerNormalizerInput.current_values[].value_metadata | 선택 | → ValueMetadata | 해당 값의 정밀도와 근거. 생략은 미수집이며 exact로 간주하지 않는다. | 현재 답과 확인 대기 후보를 비교하는 입력에서도 정밀도와 근거를 보존할 수 있어야 한다. | T1, T2 |
| AnswerNormalizerInput.current_values[].value_metadata → ValueMetadata | 선택 | object; additionalProperties=False | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | T1, T2 |
| AnswerNormalizerInput.current_values[].value_metadata → ValueMetadata.precision | 필수 | → Precision | 값이 exact(단일 확정 표현), approximate(근사 표현), unspecified(정밀도 미확보)인지 전달한다. 범위 중간값의 저장 허용 여부는 결정하지 않는다. | 같은 숫자라도 단일 확정 표현과 근사 표현을 구별하여 저장·재질문·응답 재료에서 정보가 사라지지 않아야 한다. | T1, T2 |
| AnswerNormalizerInput.current_values[].value_metadata → ValueMetadata.precision → Precision | 필수 | string; enum=["exact", "approximate", "unspecified"] | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | T1 |
| AnswerNormalizerInput.current_values[].value_metadata → ValueMetadata.evidence | 필수 | array | 원문 근거 목록. 빈 목록은 근거가 확보되지 않았음을 뜻하며 근거가 없다는 업무 판정을 뜻하지 않는다. | 복수 구절의 합산·정정·비교는 근거 하나로 축약하면 정보가 사라진다. | T1, T2 |
| AnswerNormalizerInput.current_values[].value_metadata → ValueMetadata.evidence[] | 배열 항목 | → Evidence |  |  |  |
| AnswerNormalizerInput.current_values[].value_metadata → ValueMetadata.evidence[] → Evidence | 배열 항목 | object; additionalProperties=False | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| AnswerNormalizerInput.current_values[].value_metadata → ValueMetadata.evidence[] → Evidence.turn_index | 필수 | integer; minimum=0 | 세션 내 원문 발화의 턴 순번. Framework가 부여하며 0/1 시작 기준은 세션에서 일관되게 적용한다. | 현재 발화와 과거 발화의 근거를 혼동하지 않아야 한다. | T1, T2 |
| AnswerNormalizerInput.current_values[].value_metadata → ValueMetadata.evidence[] → Evidence.start | 필수 | integer; minimum=0 | 원문에서 근거가 시작하는 포함 위치. 위치 단위는 offset_unit으로 명시한다. | 같은 구절이 원문에 반복되어도 어느 부분을 사용했는지 식별해야 한다. | T1, T2 |
| AnswerNormalizerInput.current_values[].value_metadata → ValueMetadata.evidence[] → Evidence.end | 필수 | integer; minimum=0 | 원문에서 근거가 끝나는 제외 위치. start 이상이어야 한다. 순서와 text 길이의 일관성은 정적 자료 무결성 검사로 확인한다. | 원문 근거의 정확한 범위를 복원할 수 있어야 한다. | T1, T2 |
| AnswerNormalizerInput.current_values[].value_metadata → ValueMetadata.evidence[] → Evidence.offset_unit | 필수 | string; enum=["unicode_code_point", "utf16_code_unit", "utf8_byte"] | 위치 단위: unicode_code_point, utf16_code_unit, utf8_byte. 서로 다른 런타임의 위치를 조용히 혼용하지 않는다. | Unicode 문자, UTF-16 코드 단위, UTF-8 바이트 위치는 같은 숫자가 아닐 수 있다. | T1, T2 |
| AnswerNormalizerInput.current_values[].value_metadata → ValueMetadata.evidence[] → Evidence.text | 필수 | string; minLength=1 | 근거 구절 자체. 원문 일치 여부는 원문을 가진 담당자가 확인한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| AnswerNormalizerInput.pendings | 필수 | array | 기록 저장소 · 관련 슬롯과 기다리는 답 대상 슬롯 중 확인 대기가 있는 것(턴 시작). | 이번 값이 확인 대기 값과 같은지, "네"가 받아들일 선행 슬롯 값(C4, 정규화 규칙 3). | S8b, S6a, C4b |
| AnswerNormalizerInput.pendings[] | 배열 항목 | object; additionalProperties=False | ID·슬롯·값. | 값을 비교하고, 받아들일 확인 대기를 ID로 가리킨다. | S8b, S6a, C4b |
| AnswerNormalizerInput.pendings[].pending_id | 필수 | → PendingId | 값 비교·확인 수락의 대상으로 사용되는 현재 확인 대기의 ID. | 확인-긍정이 받아들일 확인 대기를 기다리는 답의 ID와 맞춰 본다. | S8b, S6a |
| AnswerNormalizerInput.pendings[].pending_id → PendingId | 필수 | string; minLength=1 | 저장 판단이 확인 대기를 둘 때 새로 만드는, 세션 안에서 겹치지 않는 값(예: UUID). | "네"가 어느 확인 대기에 대한 답인지 상태 판정이 이 ID로 잇는다. 같은 슬롯에 새 충돌 값이 와서 확인 대기가 바뀌면 이전 확인에 대한 "네"가 새 값을 받아들이지 않게 한다(C4). | C3, C4a, N13 |
| AnswerNormalizerInput.pendings[].slot | 필수 | → SlotRef | 이 확인 대기 값이 속한 문항·반복 행·슬롯의 식별자. | 어느 칸의 확인 대기 값인지 있어야 같은 칸의 새 값과 비교한다. | S8b, S6a, C4b |
| AnswerNormalizerInput.pendings[].slot → SlotRef | 필수 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| AnswerNormalizerInput.pendings[].slot → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| AnswerNormalizerInput.pendings[].slot → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| AnswerNormalizerInput.pendings[].slot → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| AnswerNormalizerInput.pendings[].slot → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| AnswerNormalizerInput.pendings[].value | 필수 | → Value | 확인 대기 값. | 이번 값이 확인 대기 값과 같은지(받아들임) 비교하고, "네"면 선행 슬롯 값으로 쓴다. | S8b, S6a, C4b |
| AnswerNormalizerInput.pendings[].value → Value | 필수 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| AnswerNormalizerInput.pendings[].value → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| AnswerNormalizerInput.pendings[].value → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| AnswerNormalizerInput.pendings[].value → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| AnswerNormalizerInput.pendings[].value → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| AnswerNormalizerInput.pendings[].value → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| AnswerNormalizerInput.pendings[].value → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| AnswerNormalizerInput.pendings[].value → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| AnswerNormalizerInput.pendings[].value → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| AnswerNormalizerInput.pendings[].value → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| AnswerNormalizerInput.pendings[].value_metadata | 선택 | → ValueMetadata | 해당 값의 정밀도와 근거. 생략은 미수집이며 exact로 간주하지 않는다. | 현재 답과 확인 대기 후보를 비교하는 입력에서도 정밀도와 근거를 보존할 수 있어야 한다. | T1, T2 |
| AnswerNormalizerInput.pendings[].value_metadata → ValueMetadata | 선택 | object; additionalProperties=False | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | T1, T2 |
| AnswerNormalizerInput.pendings[].value_metadata → ValueMetadata.precision | 필수 | → Precision | 값이 exact(단일 확정 표현), approximate(근사 표현), unspecified(정밀도 미확보)인지 전달한다. 범위 중간값의 저장 허용 여부는 결정하지 않는다. | 같은 숫자라도 단일 확정 표현과 근사 표현을 구별하여 저장·재질문·응답 재료에서 정보가 사라지지 않아야 한다. | T1, T2 |
| AnswerNormalizerInput.pendings[].value_metadata → ValueMetadata.precision → Precision | 필수 | string; enum=["exact", "approximate", "unspecified"] | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | T1 |
| AnswerNormalizerInput.pendings[].value_metadata → ValueMetadata.evidence | 필수 | array | 원문 근거 목록. 빈 목록은 근거가 확보되지 않았음을 뜻하며 근거가 없다는 업무 판정을 뜻하지 않는다. | 복수 구절의 합산·정정·비교는 근거 하나로 축약하면 정보가 사라진다. | T1, T2 |
| AnswerNormalizerInput.pendings[].value_metadata → ValueMetadata.evidence[] | 배열 항목 | → Evidence |  |  |  |
| AnswerNormalizerInput.pendings[].value_metadata → ValueMetadata.evidence[] → Evidence | 배열 항목 | object; additionalProperties=False | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| AnswerNormalizerInput.pendings[].value_metadata → ValueMetadata.evidence[] → Evidence.turn_index | 필수 | integer; minimum=0 | 세션 내 원문 발화의 턴 순번. Framework가 부여하며 0/1 시작 기준은 세션에서 일관되게 적용한다. | 현재 발화와 과거 발화의 근거를 혼동하지 않아야 한다. | T1, T2 |
| AnswerNormalizerInput.pendings[].value_metadata → ValueMetadata.evidence[] → Evidence.start | 필수 | integer; minimum=0 | 원문에서 근거가 시작하는 포함 위치. 위치 단위는 offset_unit으로 명시한다. | 같은 구절이 원문에 반복되어도 어느 부분을 사용했는지 식별해야 한다. | T1, T2 |
| AnswerNormalizerInput.pendings[].value_metadata → ValueMetadata.evidence[] → Evidence.end | 필수 | integer; minimum=0 | 원문에서 근거가 끝나는 제외 위치. start 이상이어야 한다. 순서와 text 길이의 일관성은 정적 자료 무결성 검사로 확인한다. | 원문 근거의 정확한 범위를 복원할 수 있어야 한다. | T1, T2 |
| AnswerNormalizerInput.pendings[].value_metadata → ValueMetadata.evidence[] → Evidence.offset_unit | 필수 | string; enum=["unicode_code_point", "utf16_code_unit", "utf8_byte"] | 위치 단위: unicode_code_point, utf16_code_unit, utf8_byte. 서로 다른 런타임의 위치를 조용히 혼용하지 않는다. | Unicode 문자, UTF-16 코드 단위, UTF-8 바이트 위치는 같은 숫자가 아닐 수 있다. | T1, T2 |
| AnswerNormalizerInput.pendings[].value_metadata → ValueMetadata.evidence[] → Evidence.text | 필수 | string; minLength=1 | 근거 구절 자체. 원문 일치 여부는 원문을 가진 담당자가 확인한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| AnswerNormalizerInput.awaiting | 필수 | anyOf(2분기) | 기록 저장소 · 직전 응답 지시의 기다리는 답 중 행동·대상 목록·대상 확인 대기 ID(턴 시작). | "네"가 어느 확인 대기를 받아들이는지 알아야 선행 슬롯 값을 정한다(정규화 규칙 3). | S8b, S6a, S6b |
| AnswerNormalizerInput.awaiting [anyOf:0] | 해당 분기 | object; additionalProperties=False | 행동·대상·확인 대기 ID. | 기다리는 답 전체가 아니라 확인 대기를 가리키는 데 필요한 부분만 받아, 응답 지시 모양이 바뀌어도 정규화가 바뀌지 않게 한다. | S8b, S6a |
| AnswerNormalizerInput.awaiting [anyOf:0].action | 필수 | → AskAction | 묻기 행동. | 확인 대기 확인을 기다릴 때만 "네"가 확인 대기 값을 받아들인다. | S8b, S6a |
| AnswerNormalizerInput.awaiting [anyOf:0].action → AskAction | 필수 | oneOf(9분기) | 사용자에게 답을 기다리는 행동. | 기다리는 답에는 이 행동만 들어갈 수 있다. 다음 턴의 짧은 답("네", "두 병이요")이 무엇에 대한 답인지 알려면 묻는 행동이어야 하기 때문이다(B5). | D2, G1, H3e, R6 |
| AnswerNormalizerInput.awaiting [anyOf:0].action → AskAction [oneOf:0] | 해당 분기 | const="ASK_NEXT" | 열린 문항을 묻는다 | 열린 문항을 차례로 물어 문진을 진행한다. | A1, D2, G1 |
| AnswerNormalizerInput.awaiting [anyOf:0].action → AskAction [oneOf:1] | 해당 분기 | const="ASK_MISSING" | 같은 문항의 빠진 필수 슬롯만 묻는다 | 같은 문항에서 받은 값은 다시 묻지 않고 빠진 칸만 묻는다. | B2, B3b, E1c |
| AnswerNormalizerInput.awaiting [anyOf:0].action → AskAction [oneOf:2] | 해당 분기 | const="ASK_CLARIFY" | 애매한 값을 짚어 다시 묻는다 | 애매한 값을 사용자가 한 말 그대로 짚어 하나로 다시 말하게 한다. | B5, B3a, B10 |
| AnswerNormalizerInput.awaiting [anyOf:0].action → AskAction [oneOf:3] | 해당 분기 | const="ASK_CONFIRM" | 기존 답과 새 답 중 어느 것이 맞는지 묻는다 | 표지 없이 다른 값을 말했을 때 잘못 들었을 수 있으므로 기존 답과 새 답 중 어느 것이 맞는지 확인한다. | H3e, R7, C4a |
| AnswerNormalizerInput.awaiting [anyOf:0].action → AskAction [oneOf:4] | 해당 분기 | const="ASK_AFTER_UNKNOWN" | 모름에 한 번 더 묻는다 | 모름에 한 번 더 기회를 주는 문항이 있다(정책). | B7a, B7b, S8i |
| AnswerNormalizerInput.awaiting [anyOf:0].action → AskAction [oneOf:5] | 해당 분기 | const="ASK_AFTER_REFUSAL" | 왜 묻는지 설명하고 다시 묻는다 | 거절한 사람에게 왜 묻는지 설명하면 답할 수 있다(정책). | S3c, B8a, B8b |
| AnswerNormalizerInput.awaiting [anyOf:0].action → AskAction [oneOf:6] | 해당 분기 | const="ASK_CORRECTION_TARGET" | 무엇을, 어떤 값으로 고칠지 묻는다 | 값 없이 고치겠다는 말을 버리면 사용자의 정정 의사가 사라진다(C5, C6) | R6, X5, X3 |
| AnswerNormalizerInput.awaiting [anyOf:0].action → AskAction [oneOf:7] | 해당 분기 | const="ASK_FINISH" | 마칠지 묻는다 | 마친 뒤에는 고칠 수 없으므로 한 번 묻는다(H1, A6) | H3d, N12, H1 |
| AnswerNormalizerInput.awaiting [anyOf:0].action → AskAction [oneOf:8] | 해당 분기 | const="ASK_STOP" | 정말 그만둘지 묻는다 | 잘못 알아들은 "그만"으로 문진이 끝나지 않게(D4) | G8b, N9, S5a |
| AnswerNormalizerInput.awaiting [anyOf:0].targets | 필수 | array | 현재 기다리는 응답이 가리키는 슬롯 또는 문항 전체 대상의 목록. | 확인 대기 확인의 대상 칸이 선행 슬롯이면 "네"로 받아들일 값이 후속 문항의 선행 값이 된다. | S8b, S6a |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] | 배열 항목 | → Target |  |  |  |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target | 배열 항목 | oneOf(2분기) | 슬롯 하나 또는 문항 전체. | 항목·판정·응답 지시가 슬롯과 문항 전체를 같은 자리에서 가리켜야 한다. | A2, R11, S3b |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target [oneOf:0] | 해당 분기 | → SlotRef |  |  |  |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target [oneOf:0] → SlotRef | 해당 분기 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target [oneOf:0] → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target [oneOf:0] → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target [oneOf:0] → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target [oneOf:0] → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target [oneOf:1] | 해당 분기 | → WholeQuestion |  |  |  |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target [oneOf:1] → WholeQuestion | 해당 분기 | object; additionalProperties=False | 문항의 모든 슬롯을 한꺼번에 가리킴. | "술은 잘 모르겠어요"처럼 문항 전체에 대한 모름·거절과, 문항에 대한 안내·나중에가 있다(B7, D3, E1). 저장은 항상 슬롯 단위라 저장 판단이 펼친다. | R11, S3b, N17 |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target [oneOf:1] → WholeQuestion.question_id | 필수 | → QuestionId | 가리키는 문항. | 문항 전체에 대한 말("술은 잘 모르겠어요")은 그 문항의 모든 칸에 펼쳐 기록해야 하므로 어느 문항인지 있어야 한다. | R11, S3b, N17 |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target [oneOf:1] → WholeQuestion.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| AnswerNormalizerInput.awaiting [anyOf:0].targets[] → Target [oneOf:1] → WholeQuestion.whole_question | 필수 | const=true | 항상 true. | 슬롯 대상과 모양으로 구분하기 위해. | R11, S3b, N17 |
| AnswerNormalizerInput.awaiting [anyOf:0].target_pending_id | 필수 | anyOf(2분기) | 기다리는 응답이 특정 확인 대기에 대한 것이면 그 ID, 아니면 null. | "네"가 받아들일 확인 대기를 ID로 정해야 그 값을 선행 슬롯 값으로 쓸지 정한다. | S8b, S6a |
| AnswerNormalizerInput.awaiting [anyOf:0].target_pending_id [anyOf:0] | 해당 분기 | → PendingId |  |  |  |
| AnswerNormalizerInput.awaiting [anyOf:0].target_pending_id [anyOf:0] → PendingId | 해당 분기 | string; minLength=1 | 저장 판단이 확인 대기를 둘 때 새로 만드는, 세션 안에서 겹치지 않는 값(예: UUID). | "네"가 어느 확인 대기에 대한 답인지 상태 판정이 이 ID로 잇는다. 같은 슬롯에 새 충돌 값이 와서 확인 대기가 바뀌면 이전 확인에 대한 "네"가 새 값을 받아들이지 않게 한다(C4). | C3, C4a, N13 |
| AnswerNormalizerInput.awaiting [anyOf:0].target_pending_id [anyOf:1] | 해당 분기 | null | 없음 | 기다리는 답이 확인 대기 확인이 아니다(B1 다음 문항 묻기, B2 빠진 슬롯 되묻기). 5절 3이 이 ID가 있을 때만 "네"를 선행 슬롯 값으로 바꾸므로, 없음이 그 길을 막는다. | B1, B2 |
| AnswerNormalizerInput.awaiting [anyOf:1] | 해당 분기 | null | 없음 | 기다리는 답 자체가 없는 턴이다(A2 첫 입력이 말, N1c 첫 입력을 알아듣지 못함). 직전 응답 지시가 없으면 건넬 기다리는 답도 없다. | A2, N1c |
| AnswerNormalizerInput.turn_index | 선택 | integer; minimum=0 | 세션 내 원문 발화의 턴 순번. Framework가 부여하며 0/1 시작 기준은 세션에서 일관되게 적용한다. | 모델의 원문 위치 근거에 Framework가 부여한 턴 순번을 결합할 수 있어야 한다. | T2 |

## output: NormalizerOutput

계약 상태: current. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.

원본: [Schema](../../contracts/components/answer_normalizer/output.schema.json), [의미·근거](../../contracts/components/answer_normalizer/output.fields.yaml)

| 필드·분기 경로 | 필수 여부 | 값 제약·참조 | 무슨 값인가 | 왜 필요한가 | 근거 요구사항 |
|---|---|---|---|---|---|
| NormalizerOutput |  | object; additionalProperties=False | 항목별 검사와 빠진 필수 슬롯. | 값 규칙 쪽 사실을 한 번에 넘겨, 상태 판정이 문항 정의의 규칙을 직접 보지 않게 한다. | B2, B3a, X7 |
| NormalizerOutput.item_checks | 필수 | array | 항목마다 하나. | 상태 판정이 항목 번호로 원래 항목과 이어 판정한다. | B3a, S1a, X7 |
| NormalizerOutput.item_checks[] | 배열 항목 | → ItemCheck |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck | 배열 항목 | object; additionalProperties=False; allOf(1분기) | 항목 하나의 값을 표준화하고 검사한 사실. | 값 규칙(단위·범위·선행 조건)을 아는 곳을 이 컴포넌트 하나로 모은다. 상태 판정은 이 사실만 보고 판정한다(값 규칙과 해석 규칙은 바뀌는 이유가 달라 나눴다). | B3a, S1a, X7 |
| NormalizerOutput.item_checks[] → ItemCheck.item_no | 필수 | integer; minimum=0 | 검사한 항목. | 검사 결과를 상태 판정이 원래 항목(의도·원문)과 다시 이어야 판정할 수 있다. | B1, B4, N13 |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value | 필수 | anyOf(2분기) | 표준화한 값. 문제가 있거나 값 없는 항목이면 없음. | "한 갑"·"스무 개비"처럼 다르게 말한 같은 값을 하나의 형태로 바꿔야 비교하고 저장할 수 있다. | A2, B1, C1 |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:0] | 해당 분기 | → Value |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:0] → Value | 해당 분기 | oneOf(3분기) | 선택지 문자열, 수와 표시 단위·선택적 단위 코드, 또는 선택지 코드 객체. 값의 정밀도·근거는 해당 경계의 value_metadata로 전달한다. | 값 비교(같음·다름, 범위, 위험 기준)는 정규화·검증만 하지만, 단위가 서로 환산되지 않는 슬롯(주 n회와 월 n회)은 수만으로 값을 나타낼 수 없다. 문자열 "주 2회"로 두면 받는 쪽마다 다시 풀어야 하므로 수와 단위를 나눠 둔다. | A2, B1, C1 |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:0] → Value [oneOf:0] | 해당 분기 | string; minLength=1 | 코드 목록이 없는 문항의 선택지 문자열. 코드 목록을 사용하는 문항의 정규화 값은 CodedValue로 표현한다. | 선택지 슬롯의 답은 정해진 말 중 하나여야 결과를 받는 쪽이 집계할 수 있다. | A2, B1, C1 |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:0] → Value [oneOf:1] | 해당 분기 | object; additionalProperties=False | 수와 그 단위. | 단위 슬롯은 같은 수라도 단위가 다르면 다른 답이므로 수와 단위를 함께 둔다. | B1, C1, G4, B3b |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:0] → Value [oneOf:1].amount | 필수 | number | 단위로 센 수. | 범위 밖인지, 위험 기준을 넘는지, 기존 답과 같은지를 수로 비교해야 한다. | B1, C1, G4 |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:0] → Value [oneOf:1].unit | 필수 | string; minLength=1 | 사용자에게 보여 줄 단위 이름. 안정적인 코드가 확보되어 있으면 unit_code를 함께 전달한다. | 같은 수라도 단위가 다르면 다른 값이다. | B1, B3b, C1 |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:0] → Value [oneOf:1].unit_code | 선택 | string; minLength=1 | 정규화된 단위의 등록 코드. unit은 표시 이름이며 코드가 없는 자료는 이 필드를 생략한다. | 저장·비교에 쓰는 단위 코드와 사용자에게 보여 줄 이름을 분리해야 한다. | T1, T3 |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:0] → Value [oneOf:2] | 해당 분기 | → CodedValue |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:0] → Value [oneOf:2] → CodedValue | 해당 분기 | object; additionalProperties=False | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | 선택지 코드를 값으로 전달하고 필요하면 등록된 표시 이름의 스냅샷을 함께 보존한다. | T4 |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:0] → Value [oneOf:2] → CodedValue.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T4 |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:0] → Value [oneOf:2] → CodedValue.label | 선택 | string; minLength=1 | 사람에게 보여 줄 표시 이름. 코드와 같은 문자열일 필요가 없다. | 안정적인 코드를 사용자에게 그대로 읽는 대신 등록된 이름을 사용할 수 있어야 한다. | T4 |
| NormalizerOutput.item_checks[] → ItemCheck.standard_value [anyOf:1] | 해당 분기 | null | 없음 | 표준화하지 못했거나 표준화할 값이 없는 항목이다(B3a 범위 밖, B3b 단위 없음, C6a 값 없는 정정). 5절 6이 이때 "현재 값과·확인 대기 값과"를 해당 없음으로 정하는 조건이 바로 이 없음이다. | B3a, B3b, C6a |
| NormalizerOutput.item_checks[] → ItemCheck.problems | 필수 | array | 찾은 문제들(없으면 빈 목록). | 값을 쓸 수 없는 까닭을 사실로 넘겨야 상태 판정이 애매로 판정하고 Plan이 무엇을 되물을지 안다. | B3a, B3b, B4 |
| NormalizerOutput.item_checks[] → ItemCheck.problems[] | 배열 항목 | → Problem |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck.problems[] → Problem | 배열 항목 | oneOf(5분기) | 정규화·검증이 항목 값에서 찾은 문제. | 값을 저장할 수 없는 이유를 상태 판정에 사실로 넘겨, 판정이 값 규칙을 다시 알 필요가 없게 한다. | B3a, B3b, B4, R16 |
| NormalizerOutput.item_checks[] → ItemCheck.problems[] → Problem [oneOf:0] | 해당 분기 | const="NO_UNIT" | 단위가 둘 이상인 슬롯에 단위 없이 숫자만 말함 | 어느 단위인지 정할 수 없어 되묻는다(B3 "두 번이요") | B3b |
| NormalizerOutput.item_checks[] → ItemCheck.problems[] → Problem [oneOf:1] | 해당 분기 | const="OUT_OF_RANGE" | 그 단위의 범위(단위 정의의 범위)를 벗어난 값 | 잘못 듣거나 잘못 말한 값을 저장하지 않는다(B3 "서른 시간") | B3a, S3d |
| NormalizerOutput.item_checks[] → ItemCheck.problems[] → Problem [oneOf:2] | 해당 분기 | const="AMBIGUOUS" | 범위 값이나 여러 값 | "두세 병"처럼 값이 하나로 정해지지 않으면 저장할 수 없어 되물어야 한다(B3). | B10, C8a, R10, S7b |
| NormalizerOutput.item_checks[] → ItemCheck.problems[] → Problem [oneOf:3] | 해당 분기 | const="MISMATCH" | 선행 조건으로 이어진 다른 답과 모순 | 선행 조건으로 이어진 두 답이 모순이면("안 마셔요" + "소주 두 병") 어느 쪽도 저장할 수 없어 둘 다 짚어 되묻는다(B4). | B4, S2b, S6a, S7c |
| NormalizerOutput.item_checks[] → ItemCheck.problems[] → Problem [oneOf:4] | 해당 분기 | const="UNKNOWN_TARGET" | 문항 정의에 없는 문항·슬롯을 가리킴 | 답 계열 항목은 저장할 곳이 없어 무관으로 다루고, 요청·위험 신호는 대상만 없는 것으로 보고 그 의도대로 다룬다(K9, 6절 규칙 8). | R16, X8, X9 |
| NormalizerOutput.item_checks[] → ItemCheck.mismatched_slots | 필수 | array | 문제에 "다른 답과 맞지 않음"이 있을 때, 어느 슬롯의 값과 맞지 않는지. | 되물을 때 두 값을 함께 짚어야 사용자가 어느 쪽을 고칠지 안다(B4). | B4, S2b, S6a |
| NormalizerOutput.item_checks[] → ItemCheck.mismatched_slots[] | 배열 항목 | → SlotRef |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck.mismatched_slots[] → SlotRef | 배열 항목 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| NormalizerOutput.item_checks[] → ItemCheck.mismatched_slots[] → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| NormalizerOutput.item_checks[] → ItemCheck.mismatched_slots[] → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| NormalizerOutput.item_checks[] → ItemCheck.mismatched_slots[] → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| NormalizerOutput.item_checks[] → ItemCheck.mismatched_slots[] → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| NormalizerOutput.item_checks[] → ItemCheck.vs_current | 필수 | oneOf(4분기) | 표준 값과 현재값의 비교. | 같음은 정상, 다름은 충돌이나 정정을 가른다(C3). | X7, C3, C4b |
| NormalizerOutput.item_checks[] → ItemCheck.vs_current [oneOf:0] | 해당 분기 | const="EQUAL" | 현재값과 같음 | 다시 말한 것이라 바꿀 것이 없다 | C4b |
| NormalizerOutput.item_checks[] → ItemCheck.vs_current [oneOf:1] | 해당 분기 | const="DIFFERENT" | 현재값과 다름 | 기존 답과 다르면 정정 표지에 따라 바로 고치거나(정정) 확인을 묻는다(충돌). | C3, N6, N13 |
| NormalizerOutput.item_checks[] → ItemCheck.vs_current [oneOf:2] | 해당 분기 | const="NO_CURRENT" | 현재값이 없음·모름·거절 | 값을 말하면 충돌이 아니라 새 답이다(B7 뒤의 답) | X7, A2, B1 |
| NormalizerOutput.item_checks[] → ItemCheck.vs_current [oneOf:3] | 해당 분기 | const="NOT_APPLICABLE" | 표준 값이 없음 | 표준 값이 없으면 비교 자체가 불가능하므로 같음·다름과 구분해 둔다. | B3a, B3b |
| NormalizerOutput.item_checks[] → ItemCheck.vs_pending | 필수 | oneOf(4분기) | 표준 값과 그 슬롯 확인 대기 값의 비교. | 확인 대기 값을 다시 말하면 받아들인 것이다(C4). | C4b, N3b, N6 |
| NormalizerOutput.item_checks[] → ItemCheck.vs_pending [oneOf:0] | 해당 분기 | const="EQUAL" | 확인 대기 값과 같음 | 확인 대기 값을 다시 말하면 그 값을 받아들인 것으로 본다. | N3b, N17, S2e |
| NormalizerOutput.item_checks[] → ItemCheck.vs_pending [oneOf:1] | 해당 분기 | const="DIFFERENT" | 확인 대기 값과 다름 | 확인 대기와도 다르면 새 충돌이거나, 기존 값을 다시 말한 경우 확인 대기를 버린다. | C4b, N6 |
| NormalizerOutput.item_checks[] → ItemCheck.vs_pending [oneOf:2] | 해당 분기 | const="NO_PENDING" | 그 슬롯에 확인 대기가 없음 | 확인 대기가 없으면 받아들이거나 버릴 것이 없다는 사실을 따로 알려야 상태 판정이 확인 대기 처리를 내지 않는다. | A2, C3 |
| NormalizerOutput.item_checks[] → ItemCheck.vs_pending [oneOf:3] | 해당 분기 | const="NOT_APPLICABLE" | 표준 값이 없음 | 표준 값이 없으면 비교 자체가 불가능하므로 같음·다름과 구분해 둔다. | C8a, B3a |
| NormalizerOutput.item_checks[] → ItemCheck.risk_rule | 필수 | anyOf(2분기) | 표준 값이 슬롯 위험 기준에 해당하면 그 대응, 아니면 없음. | 값 비교는 이 컴포넌트에서만 하므로, 위험 해당 여부도 여기서 사실로 넘긴다(G3, G4). | G3, G4 |
| NormalizerOutput.item_checks[] → ItemCheck.risk_rule [anyOf:0] | 해당 분기 | → RiskResponse |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck.risk_rule [anyOf:0] → RiskResponse | 해당 분기 | oneOf(2분기) | 위험 기준에 해당하는 답에 할 일. | 바로 멈춰야 하는 답과 결과에만 표시할 답을 나눈다(G3, G4). | G3, G4, G6b |
| NormalizerOutput.item_checks[] → ItemCheck.risk_rule [anyOf:0] → RiskResponse [oneOf:0] | 해당 분기 | const="IMMEDIATE" | 바로 멈추고 직원을 부름 | 그 답 자체가 위급하면(죽고 싶은 생각 = 예) 바로 멈추고 직원을 불러야 한다. | G3, G6b |
| NormalizerOutput.item_checks[] → ItemCheck.risk_rule [anyOf:0] → RiskResponse [oneOf:1] | 해당 분기 | const="ON_RESULT" | 계속하고 결과에 표시 | 위험하지만 지금 멈출 정도는 아닌 답(높은 혈압)은 문진을 이어 가고 결과에 표시해 의료진이 본다. | G4 |
| NormalizerOutput.item_checks[] → ItemCheck.risk_rule [anyOf:1] | 해당 분기 | null | 없음 | 위험 기준이 없는 슬롯이거나 값이 기준에 걸리지 않은 항목이다(B1 Q5.시간 7). G4처럼 걸릴 때만 대응이 담기므로, 없음이 "위험에 해당하지 않음"을 사실로 남긴다. | B1, B3a |
| NormalizerOutput.item_checks[] → ItemCheck.prerequisite_unmet | 필수 | boolean | 후속 문항 항목인데 선행 답이 정해지지 않았거나, 이번 발화에서 충돌이 될 값이거나, 저장할 수 없는 경우. | 후속 답은 선행 답이 정해진 뒤에만 기록한다는 원칙을 값 규칙 쪽에서 판단한다(C2, B4). | S1a, S2a, S8a |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata | 선택 | → ValueMetadata | 해당 값의 정밀도와 근거. 생략은 미수집이며 exact로 간주하지 않는다. | 정규화·판정·저장·확인 후보·응답 재료에서 정밀도와 근거가 사라지지 않아야 한다. | T1, T2 |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata → ValueMetadata | 선택 | object; additionalProperties=False | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | 정밀도와 복수 근거를 값과 분리하여 여러 경계와 저장 상태에서 보존한다. | T1, T2 |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata → ValueMetadata.precision | 필수 | → Precision | 값이 exact(단일 확정 표현), approximate(근사 표현), unspecified(정밀도 미확보)인지 전달한다. 범위 중간값의 저장 허용 여부는 결정하지 않는다. | 같은 숫자라도 단일 확정 표현과 근사 표현을 구별하여 저장·재질문·응답 재료에서 정보가 사라지지 않아야 한다. | T1, T2 |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata → ValueMetadata.precision → Precision | 필수 | string; enum=["exact", "approximate", "unspecified"] | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | 단일 값과 근사 표현의 정밀도를 보존하는 값이다. | T1 |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata → ValueMetadata.evidence | 필수 | array | 원문 근거 목록. 빈 목록은 근거가 확보되지 않았음을 뜻하며 근거가 없다는 업무 판정을 뜻하지 않는다. | 복수 구절의 합산·정정·비교는 근거 하나로 축약하면 정보가 사라진다. | T1, T2 |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata → ValueMetadata.evidence[] | 배열 항목 | → Evidence |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata → ValueMetadata.evidence[] → Evidence | 배열 항목 | object; additionalProperties=False | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata → ValueMetadata.evidence[] → Evidence.turn_index | 필수 | integer; minimum=0 | 세션 내 원문 발화의 턴 순번. Framework가 부여하며 0/1 시작 기준은 세션에서 일관되게 적용한다. | 현재 발화와 과거 발화의 근거를 혼동하지 않아야 한다. | T1, T2 |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata → ValueMetadata.evidence[] → Evidence.start | 필수 | integer; minimum=0 | 원문에서 근거가 시작하는 포함 위치. 위치 단위는 offset_unit으로 명시한다. | 같은 구절이 원문에 반복되어도 어느 부분을 사용했는지 식별해야 한다. | T1, T2 |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata → ValueMetadata.evidence[] → Evidence.end | 필수 | integer; minimum=0 | 원문에서 근거가 끝나는 제외 위치. start 이상이어야 한다. 순서와 text 길이의 일관성은 정적 자료 무결성 검사로 확인한다. | 원문 근거의 정확한 범위를 복원할 수 있어야 한다. | T1, T2 |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata → ValueMetadata.evidence[] → Evidence.offset_unit | 필수 | string; enum=["unicode_code_point", "utf16_code_unit", "utf8_byte"] | 위치 단위: unicode_code_point, utf16_code_unit, utf8_byte. 서로 다른 런타임의 위치를 조용히 혼용하지 않는다. | Unicode 문자, UTF-16 코드 단위, UTF-8 바이트 위치는 같은 숫자가 아닐 수 있다. | T1, T2 |
| NormalizerOutput.item_checks[] → ItemCheck.value_metadata → ValueMetadata.evidence[] → Evidence.text | 필수 | string; minLength=1 | 근거 구절 자체. 원문 일치 여부는 원문을 가진 담당자가 확인한다. | 현재 또는 이전 턴의 원문 근거를 위치 단위와 함께 표현한다. 턴 번호는 Framework가 부여한다. | T1, T2 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details | 선택 | array | problems의 넓은 분류를 보충하는 세부 코드·관련 슬롯·진단 설명. 생략은 세부 설명 미수집이다. | 단위 불명과 모호한 표현 등을 하나의 AMBIGUOUS로 축약해도 원래 사유와 대상은 보존할 수 있어야 한다. | T9 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] | 배열 항목 | → ProblemDetail |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail | 배열 항목 | object; additionalProperties=False | 문제의 넓은 분류를 유지하면서 세부 사유 코드와 관련 슬롯을 보존한다. 세부 코드는 등록된 문제 코드표로 합의하며 이 자료형만으로 업무 판정을 수행하지 않는다. | 문제의 넓은 분류를 유지하면서 세부 사유 코드와 관련 슬롯을 보존한다. 세부 코드는 등록된 문제 코드표로 합의하며 이 자료형만으로 업무 판정을 수행하지 않는다. | T9 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.category | 필수 | → Problem | 기존의 넓은 문제 분류. 세부 code와 구분한다. | 문제의 넓은 분류를 유지하면서 세부 사유 코드와 관련 슬롯을 보존한다. 세부 코드는 등록된 문제 코드표로 합의하며 이 자료형만으로 업무 판정을 수행하지 않는다. | T9 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.category → Problem | 필수 | oneOf(5분기) | 정규화·검증이 항목 값에서 찾은 문제. | 값을 저장할 수 없는 이유를 상태 판정에 사실로 넘겨, 판정이 값 규칙을 다시 알 필요가 없게 한다. | B3a, B3b, B4, R16 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.category → Problem [oneOf:0] | 해당 분기 | const="NO_UNIT" | 단위가 둘 이상인 슬롯에 단위 없이 숫자만 말함 | 어느 단위인지 정할 수 없어 되묻는다(B3 "두 번이요") | B3b |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.category → Problem [oneOf:1] | 해당 분기 | const="OUT_OF_RANGE" | 그 단위의 범위(단위 정의의 범위)를 벗어난 값 | 잘못 듣거나 잘못 말한 값을 저장하지 않는다(B3 "서른 시간") | B3a, S3d |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.category → Problem [oneOf:2] | 해당 분기 | const="AMBIGUOUS" | 범위 값이나 여러 값 | "두세 병"처럼 값이 하나로 정해지지 않으면 저장할 수 없어 되물어야 한다(B3). | B10, C8a, R10, S7b |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.category → Problem [oneOf:3] | 해당 분기 | const="MISMATCH" | 선행 조건으로 이어진 다른 답과 모순 | 선행 조건으로 이어진 두 답이 모순이면("안 마셔요" + "소주 두 병") 어느 쪽도 저장할 수 없어 둘 다 짚어 되묻는다(B4). | B4, S2b, S6a, S7c |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.category → Problem [oneOf:4] | 해당 분기 | const="UNKNOWN_TARGET" | 문항 정의에 없는 문항·슬롯을 가리킴 | 답 계열 항목은 저장할 곳이 없어 무관으로 다루고, 요청·위험 신호는 대상만 없는 것으로 보고 그 의도대로 다룬다(K9, 6절 규칙 8). | R16, X8, X9 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.code | 필수 | string; minLength=1 | 저장·비교에 사용하는 안정적인 식별 코드. 표시 이름으로 임의 생성하지 않는다. | 표시 이름 변경·번역에도 저장 값의 정체성이 유지되어야 한다. | T9 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.refs | 필수 | array | 문제와 관련된 구조화된 슬롯 목록. 반복 행과 필드까지 식별한다. | 같은 문항의 여러 반복 행 중 실제 문제 대상을 구별해야 한다. | T9 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.refs[] | 배열 항목 | → SlotRef |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.refs[] → SlotRef | 배열 항목 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.refs[] → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.refs[] → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.refs[] → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.refs[] → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.message | 필수 | anyOf(2분기) | 사람의 진단을 위한 보조 설명. 제어 코드나 사용자에게 그대로 읽을 문장이 아니다. | 문제의 넓은 분류를 유지하면서 세부 사유 코드와 관련 슬롯을 보존한다. 세부 코드는 등록된 문제 코드표로 합의하며 이 자료형만으로 업무 판정을 수행하지 않는다. | T9 |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.message [anyOf:0] | 해당 분기 | string; minLength=1 |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck.problem_details[] → ProblemDetail.message [anyOf:1] | 해당 분기 | null | 해당 payload 미확보 또는 이 결과에서 해당 없음. 생략과는 구별한다. | 문제의 넓은 분류를 유지하면서 세부 사유 코드와 관련 슬롯을 보존한다. 세부 코드는 등록된 문제 코드표로 합의하며 이 자료형만으로 업무 판정을 수행하지 않는다. | T9 |
| NormalizerOutput.item_checks[] → ItemCheck [allOf:0] | 해당 분기 | if; then |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck [allOf:0] [if] | 조건 |  |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck [allOf:0] [if].value_metadata | 필수 |  | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| NormalizerOutput.item_checks[] → ItemCheck [allOf:0] [if].value_metadata.precision | 선택 | enum=["exact", "approximate"] | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| NormalizerOutput.item_checks[] → ItemCheck [allOf:0] [then] | 조건 |  |  |  |  |
| NormalizerOutput.item_checks[] → ItemCheck [allOf:0] [then].standard_value | 선택 |  | exact·approximate 메타데이터는 실제 값이 있는 경우에만 허용한다. 미확보 값에는 unspecified만 사용한다. | 값이 없는데 확정 또는 근사값이 있다고 표현하는 구조적 모순을 거부한다. 입력의 정답이나 정밀도 분류는 판단하지 않는다. | T1 |
| NormalizerOutput.missing_required_slots | 필수 | array | 이번에 답한 문항에서 이번 값도, 모름·거절도 없고 현재값도 없음인 필수 슬롯. 선행 답이 정해지지 않았거나 선행 조건과 맞지 않는 문항(선행 불충족·다른 답과 맞지 않음인 항목의 문항)은 따지지 않는다. | 일부만 답하면 빠진 것만 되묻는다(B2). 물을 수 없는 후속 문항의 빈칸을 되물으면 모순된 질문이 된다(S2d, S6a). | B2, S8b, S7a, X1 |
| NormalizerOutput.missing_required_slots[] | 배열 항목 | → SlotRef |  |  |  |
| NormalizerOutput.missing_required_slots[] → SlotRef | 배열 항목 | object; additionalProperties=False | 답 칸 하나. 문항 ID·반복 키·슬롯 ID 셋으로 가리킨다. | 한 문항에 답 칸이 여럿일 수 있고(음주 상세의 빈도·양), 한 문항이 줄마다 반복될 수 있다(주종별 음주량). 셋이어야 같은 칸의 다른 줄을 가리킬 수 있다. | A2, B2, C3 |
| NormalizerOutput.missing_required_slots[] → SlotRef.question_id | 필수 | → QuestionId | 그 슬롯이 속한 문항. | 슬롯 ID만으로는 어느 문항의 칸인지 모른다. | A2, B1, B2 |
| NormalizerOutput.missing_required_slots[] → SlotRef.question_id → QuestionId | 필수 | string; minLength=1 | 문진 설계자가 문항 정의 저장소에 정한 문항 식별자. | 모든 컴포넌트가 같은 문항을 같은 이름으로 가리켜야 한다. | A1, A2, D3a |
| NormalizerOutput.missing_required_slots[] → SlotRef.repeat_key | 필수 | string | 반복 문항에서 그 줄의 식별자. 반복하지 않는 문항은 빈 문자열. | 문항·슬롯 쌍만으로는 같은 칸의 두 줄을 가리킬 수 없다. "소주는 2병인데 맥주는 모르겠어요"는 같은 칸에 줄이 둘이고 줄마다 판정이 다르다(V1, V2, V3). 빈 문자열로 두면 반복하지 않는 문항도 같은 모양으로 가리킨다. | V1, V2, V3 |
| NormalizerOutput.missing_required_slots[] → SlotRef.slot_id | 필수 | string; minLength=1 | 문항 안의 칸 식별자. | 한 문항에 칸이 여럿일 수 있어(음주 빈도·양) 문항 ID만으로는 어느 칸인지 모른다. | A2, B1, B2 |

