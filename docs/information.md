# 값과 원문 근거의 정보 계약

이 문서는 정밀도·원문 근거·코드·세부 문제·저장 요청의 데이터 역할을 설명한다. 필드별 허용 형태는 Schema 원본, 의미와 필요 이유는 fields·semantics 파일이 정한다. 업무 정책이나 실제 실행 결과는 이 문서의 대상이 아니다.

## 값의 정밀도와 근거

값의 경계에는 선택적인 `value_metadata`가 있다. `precision`은 exact, approximate, unspecified 중 하나이며 `evidence`는 원문 근거 목록이다. 메타데이터가 생략된 값은 미수집 상태이고 exact로 간주하지 않는다. exact 또는 approximate는 실제 값이 있을 때만 허용한다. unspecified에는 값 또는 근거가 미확보된 상태를 표현할 수 있다.

메타데이터는 정형 검사 결과, 판정, 저장 결정, 현재 답, 확인 대기 후보, 응답 재료에서 전달할 수 있다. Notice의 value_metadata와 previous_value_metadata는 각각 새 값과 이전 값에 대응한다. 저장 이력은 값만 있는 항목과 `{value, value_metadata}` 항목을 구분한다. 확보한 메타데이터는 해당 값과 함께 보존하며 없던 정보를 임의 생성하지 않는다.

Parser의 `Item.evidence`는 현재 원문의 TextSpan 목록이다. TextSpan은 start·end·text·offset_unit을 포함하며 모델이 턴 순번을 만들어 낼 필요가 없다. Framework는 호출 문맥의 순번을 정규화 입력의 turn_index로 전달할 수 있다. 저장·정형 결과의 Evidence는 turn_index까지 포함해 현재·이전 턴을 구별한다. 순번의 0/1 시작 기준은 서비스에서 일관되게 정한다.

start는 포함, end는 제외 위치다. 위치 단위는 Unicode 코드 포인트, UTF-16 코드 단위, UTF-8 바이트를 명시한다. 빈 근거 목록은 미확보를 뜻한다. JSON Schema는 필드 형태와 자료형을 검사한다. 끝 위치와 시작 위치의 순서 및 구절의 해당 단위 길이는 정적 무결성 검사에서 확인한다. 실제 원문의 그 위치에 같은 text가 있는지, 근거가 답을 뒷받침하는지는 원문과 판단을 가진 담당자의 책임이다.

근사값의 표시를 전달할 수 있다는 사실은 범위의 중간값 저장을 허용한다는 뜻이 아니다. 범위 처리·재질문·저장 여부의 정책은 이 변경으로 바꾸지 않는다.

## 코드와 표시 이름

`SlotDef.choice_catalog`는 code·label·synonyms를 묶은 등록 목록이다. 이 목록을 사용하면 문자열 choices는 빈 목록이어야 하고 yes_no_map은 등록 코드를 가리킨다. 코드 목록이 없는 문항은 문자열 choices를 사용한다. 동일 문항에서 두 선택지 정의를 동시에 사용하지 않는다.

코드 선택지의 값은 CodedValue의 code와 선택적인 label로 전달한다. label은 등록된 표시 이름이며 새로운 선택지를 모델이 생성할 근거가 아니다. 단위 정의의 name과 값의 unit은 표시 이름이고, UnitDef.code와 값의 unit_code는 안정적인 코드다. 환산 대상 코드가 있으면 convert_to.unit_code로 전달한다. 실제 코드 등록·유효성·동일 단위 판단은 문항 정의와 담당 컴포넌트의 책임이다.

예시의 DEMO.*와 bottle은 자료형을 설명하는 코드다. 실제 문항·선택지·단위 목록은 이 구조로 표현할 데이터이며 범용 Schema 완성의 전제 조건이 아니다.

## 구체적인 문제 정보

ItemCheck와 Judgment의 problem_details는 넓은 category, 세부 code, 관련 슬롯 refs, 선택적인 진단 message를 보존한다. ItemCheck에서는 세부 category가 problems 목록에 포함돼야 한다. 기존의 넓은 문제 분류를 없애거나 세부 코드 하나로 턴의 행동을 결정하는 것은 아니다.

refs는 문항·반복키·슬롯을 구별한다. message는 진단용이며 제어 코드나 사용자에게 그대로 읽을 문장으로 쓰지 않는다. 세부 코드 등록과 분류 대응은 담당 모듈의 합의가 필요하다. Schema는 사유 코드 문자열의 형태를 표현하며 그 사유가 실제 입력에 맞는지는 판단하지 않는다.

## 저장 요청과 결과의 초안

SessionLoadRequest/Result와 SessionCommitRequest/Result는 저장 포트의 데이터 계약 초안이다. 생성 파일은 `generated/schemas/proposals/`에 있고 components의 contract_status가 proposal로 표시된다. 실제 함수명·전송 방식·API 채택·최초 저장·revision 토큰 생성·재시도 정책을 확정하지 않는다.

조회 결과는 성공·세션 부재·DB 오류를 구별하고, 성공하면 상태와 revision을 함께 전달한다. 상태에 revision이 들어 있으면 반환 토큰과 같아야 한다. revision은 저장 상태의 버전이며 답의 변경 이력 식별자와 구별한다.

저장 요청은 expected_revision과 TurnWriteSet을 전달한다. TurnWriteSet은 StoreResult, 진행 갱신, 계획 기록을 한 묶음으로 표현한다. 실제 원자적 반영은 DB와 Framework 담당자의 책임이며 이 프로젝트는 실행하거나 증명하지 않는다.

저장 결과는 OK·REVISION_CONFLICT·DB_ERROR와 write_outcome을 구분한다. 성공은 APPLIED, 버전 충돌은 NOT_APPLIED와 반환 revision을 갖는다. DB 오류는 NOT_APPLIED 또는 UNKNOWN을 표현한다. UNKNOWN은 재시도해도 안전하다는 뜻이 아니다. 전송 실패만으로 저장 미반영을 단정하지 않는다.

TurnTrace는 이러한 요청·결과를 별도 경계로 기록할 수 있고, 미수집이면 null이다. Trace 형식에 데이터가 있다는 사실은 실제 API가 채택되었다는 뜻이 아니다.

## 근거와 확인 범위

정보별 필요 이유는 계약의 필드 설명에, 근거 요약은 `work/testcases/references/metadata_requirements.md`에 있다. T1~T10은 정보를 표현하는 정적 요구이고 case_shapes는 완전한 예시와 담당 필드를 연결한다. 실제 입력의 정답이나 팀 구현의 실행 결과를 나타내지 않는다.

`check_information_integrity.py`는 원문 위치 단위·코드 목록·문제 분류·조회 버전의 출력 내부 관계를 정적 자료로 검사한다. JSON Schema 단독으로 보장하지 못하는 관계를 구분하여 설명하고, 업무 정답 판정이나 DB 동작을 구현하지 않는다.
