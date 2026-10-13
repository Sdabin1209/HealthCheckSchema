# 계약 원본 안내

이 디렉터리는 컴포넌트의 JSON 구조와 그 의미를 정의한다. 실행 코드나 입력의 정답을 고르는 구현은 포함하지 않는다.

| 파일 | 정의하는 내용 |
|---|---|
| `components.yaml` | 컴포넌트 책임과 입력·출력·상태·Trace 계약 |
| `manifest.yaml` | 계약 버전 및 정의 이름에 대응하는 Schema·의미 설명 파일 |
| `components/*/*.schema.json` | 컴포넌트 경계의 구조적 허용 조건 |
| `types/*.schema.json` | 공유·중첩 타입의 구조적 허용 조건 |
| `*.fields.yaml`, `semantics/*.yaml` | JSON 포인터별 의미·필요 이유·근거 요구 연결 |
| `bindings.yaml` | 입력 필드의 원천·시점·전달 형태 |
| `expectations.yaml` | 요구 결과가 표현되는 계약 위치 |
| `case_notation.yaml` | 요구자료의 축약 표기와 전달 값 사이의 대응 |
| `proposals.yaml` | 추가 데이터 계약 제안과 목적; 현행 계약의 미완성 목록이 아님 |
| `output_bindings.yaml` | 출력에서 저장 상태로 전달되는 쓰기 자료와 목적 위치 |

## 우선순위

JSON 구조는 Schema 원본, 의미는 fields·semantics, 생산·소비 책임은 components·bindings를 기준으로 읽는다. `work/out/`의 상세 문서와 배포 Schema는 이 원본의 생성물이다. 둘이 다르면 원본을 수정·검증하고 다시 생성한다. 변경 기록은 현재 계약을 덮어쓰지 않는다.

Schema의 상대 `$ref`는 이 디렉터리의 파일을 참조한다. 외부 구현에는 `generated/schemas/standalone/` 파일을 사용한다. 계약 버전은 `manifest.yaml`에서 확인하며 Trace의 contract_version에는 적용한 버전을 기록한다.

## 필드의 의미와 근거

`evidence_status: requirement_reference`는 요구사항 위치와 연결되었다는 뜻이다. 필드의 최소성, 업무 구현의 정답, 모든 조건 조합을 증명했다는 뜻은 아니다. assertions는 케이스·턴·기대 위치를 명시하고, `case_shapes`는 정적 데이터로 표현 위치를 보여준다.

입력을 정답 코드로 해석하는 것은 업무 컴포넌트의 책임이다. 예를 들어 ANSWERED_INTENT이면 대상·값이 함께 존재해야 한다는 조건은 출력 구조의 일관성이고, 특정 발화가 그 의도인지는 Schema가 판단하지 않는다.

현재 제약 정책은 [구조적 제약과 운영 정책](../../docs/constraints.md), 전체 역할은 [구조와 책임](../../docs/architecture.md)에 있다. proposals.yaml은 추가 데이터 계약 제안만 기록한다. 테스트 자료 확보·운영 정책·구현 방식은 포함하지 않는다.

## 부가 정보와 제안 계약

[값과 근거의 정보 계약](../../docs/information.md)은 추가 타입의 사용과 정보 전달을 설명한다. 필드마다 의미·필요 이유·근거 케이스는 기존 fields·semantics 원본에 기록한다. manifest의 status와 components의 contract_status가 proposal인 저장 포트는 데이터 계약 초안이다. 생성 파일도 proposals 디렉터리에 구분하며 실제 API를 확정하지 않는다.
