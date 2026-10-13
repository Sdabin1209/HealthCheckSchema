# 요구사항과 정적 표현 예시

이 디렉터리는 필요한 정보와 그 정보를 표현하는 예시를 보관한다. 케이스의 expect는 요구 결과이고, 이 프로젝트가 실행한 컴포넌트의 출력이 아니다.

| 위치 | 용도 |
|---|---|
| `cases/`, `manifest.yaml` | 상황별 요구사항 케이스와 파일 목록 |
| `situations.yaml`, `fixtures/` | 상황 설명과 예시 문항 정의 |
| `format.schema.json` | 요구사항 케이스의 작성 형식 |
| `value_requirements.yaml` | 선언한 정형 값과 담당 필드 연결 |
| `case_shapes/` | 케이스 정보별 원본 포인터·Schema 포인터·완전한 정적 예시 |
| `schema_examples/` | 각 경계의 전체 정형 데이터 예시 |
| `contract_cases.yaml` | 구조적으로 허용·거부할 조합 |
| `handoff_examples.json` | 완전한 원천·목적 데이터와 비교할 필드 연결 |

`valid`는 해당 데이터의 구조적 유효성을 뜻한다. 업무 정답 여부를 뜻하지 않는다. `origin.correctness_claim: false`와 `component_execution: false`가 있는 자료는 실제 실행 결과로 발표하거나 모델 성능의 근거로 사용하지 않는다.

case_shapes의 서로 다른 시점과 계약 예시는 각각 읽는다. processing_state를 저장 후 상태로 단정하거나 예시를 이어 붙인 것만으로 E2E 검증 완료라고 판단하지 않는다. 상세 해석은 [검증 방법](../../docs/validation.md)에 있다.

케이스의 이유는 필요한 정보와 확인하려는 상황을 설명한다. 컴포넌트의 역할은 [구조와 책임](../../docs/architecture.md), [역할 대응](../rules/mapping.md), 계약 원본으로 확인한다. 규칙 절 번호의 대응은 [표기 안내](notation.md#규칙-절-참조)에 있다.

새 요구는 필요한 값·중첩 구조·구조적 조건을 명시하고 계약과 정적 예시를 함께 수정한다. 내용 의미와 실제 상태 전이를 판정하는 구현은 여기 작성하지 않는다.

T1~T10은 정밀도·복수 근거·코드·세부 문제·저장 프로토콜 정보를 표현하는 정적 요구다. 정보별 필요 이유는 `references/metadata_requirements.md`에 설명한다. 저장 포트 자료형의 검증은 실제 API 채택이나 동작 검증을 뜻하지 않는다.

## 테스트 데이터와 스키마의 구분

fixtures의 문항·선택지·단위와 case_shapes의 값은 자료형을 검증하는 재료다. 특정 문항 개수나 코드표는 스키마 완성의 필수 조건이 아니다. 같은 자료형으로 표현되는 문항·코드가 늘어나도 Schema를 바꾸지 않는다. 기존 타입으로 표현하지 못하는 새 정보 요구가 발견될 때 계약 변경을 검토한다. 현재 예시 문항은 10개이며 특정 운영 설문의 전체 목록을 나타내지 않는다.

## 현재 계약 버전을 사용하는 생성 예시

`schema_example_templates/TurnTrace.json`은 현재 계약 예시의 원본 템플릿이며 `schema_examples/TurnTrace.json`은 manifest의 계약 버전을 넣은 생성물이다. 버전 자리표시가 있는 템플릿을 실제 계약 JSON으로 사용하지 않는다. 생성은 `python3 verify.py`의 build 단계에서 수행한다. 실제 Trace·과거 기록에는 이 치환을 적용하지 않는다. 자세한 기준은 [버전 관리](../../docs/versioning.md)에 있다.
