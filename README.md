# 문진 시스템의 데이터 계약

이 프로젝트는 자연어 문진 시스템의 컴포넌트가 주고받는 JSON과 저장하는 상태를 정의한다. 요구사항 케이스에서 필요한 정보를 찾고, 그 정보를 계약으로 표현할 수 있는지 검증한다. 모델·업무 컴포넌트·데이터베이스 서버를 실행하는 구현은 포함하지 않는다.

## 읽는 순서

1. [구조와 책임](docs/architecture.md): 컴포넌트, 처리 순서, 상태와 Trace의 관계.
2. [계약 안내](work/schema.md): 컴포넌트별 Schema 원본과 중첩 필드 설명.
3. [검증 방법](docs/validation.md): 검사하는 것, 검사하지 않는 것, 예시의 해석.
4. [값과 근거의 정보 계약](docs/information.md): 정밀도·근거·코드·문제 정보와 저장 계약 초안.
5. [추가 계약 제안](work/contracts/proposals.yaml): 현행 계약과 별도로 제안된 자료형과 목적.

## 에이전트와 구현 담당자의 시작점

이 저장소를 처음 탐색할 때는 [에이전트 안내](docs/agent-guide.md)와 [AGENTS.md](AGENTS.md)를 먼저 읽는다. 전체 구조는 [구조와 책임](docs/architecture.md), 출력·상태에서 입력·저장 목적으로 이어지는 필드 관계는 [연결 인덱스](work/out/connections.md), 필요한 계약 찾기는 [계약 인덱스](work/schema.md)에서 시작한다. 계약명에서 원본 위치를 찾는 기계 판독용 목록은 `work/contracts/manifest.yaml`이다.

스키마·업무 컴포넌트 작업에서는 `presentation/`을 탐색 대상에서 제외한다. 이 경로는 사람용 웹이며 계약이나 업무 코드의 원본이 아니다. 사용자가 웹 작업을 명시한 경우에만 별도의 웹 안내를 따른다.

계약에 맞는 코드를 작성하는 데 필요한 구조·의미·관계·관련 요구를 찾을 수 있다. 업무 동작의 미정의나 충돌은 임의로 채우지 않으며, 에이전트 안내나 정적 검사 통과가 실제 구현의 정확성을 보증하지 않는다.

## 사용

Python 3.10 이상에서 프로젝트 루트 기준으로 실행한다.

```sh
python3 -m pip install -r requirements.txt
python3 verify.py
python3 verify.py --check
```

구현에 필요한 계약은 `generated/schemas/standalone/<계약명>.json`에서 가져간다. 각 파일은 필요한 참조를 자체 `$defs`에 포함한다. 사용 환경은 JSON Schema Draft 2020-12를 지원해야 한다. 미합의 저장 포트의 초안은 `generated/schemas/proposals/`에 별도로 있으며 실제 API 채택을 뜻하지 않는다. 입력과 출력에 어느 파일을 적용할지는 [컴포넌트 목록](work/contracts/components.yaml)에 명시되어 있다.

## 파일의 역할

| 위치 | 역할 | 편집 여부 |
|---|---|---|
| `work/testcases/cases/` | 표현해야 할 정보를 정의하는 요구사항 케이스 | 요구 변경 시 편집 |
| `work/contracts/` | JSON 구조, 필드 의미, 컴포넌트 책임, 입력 출처의 원본 | 계약 변경 시 편집 |
| `work/testcases/case_shapes/` | 케이스 정보와 계약 필드 및 완전한 정적 예시 연결 | 요구·계약 변경 시 검토 |
| `work/testcases/schema_examples/`, `work/testcases/contract_cases.yaml`, `work/testcases/handoff_examples.json` | 경계 형태·허용과 거부·정보 전달의 정적 예시 | 계약 변경 시 검토 |
| `work/rules/` | 필드가 필요한 이유를 설명하는 업무 요구 명세 | 요구 변경 시 편집 |
| `work/schema.md`, `work/out/`, `generated/schemas/` | 원본에서 생성하는 안내·상세 문서·배포 Schema | 직접 편집하지 않음 |
| `generated/*report*`, `VERIFIED.md` | 검사 결과와 그 결과의 적용 범위 | 검증 후 갱신 |
| `docs/` | 현재 구조·검증·제약의 사용 설명 | 설계 변경 시 편집 |
| `presentation/` | 사람에게 보여주는 Svelte 5 웹 소스·빌드·웹 검사 | UI만 이 디렉토리에서 편집; 계약은 원본에서 변경 |

계약 버전은 `work/contracts/manifest.yaml`에서 확인한다. [버전 관리 원칙](docs/versioning.md)에 증가 기준, 현재 생성물·정적 예시와 실제 Trace의 차이를 설명한다. 현재 허용 구조와 의미는 계약 원본을 기준으로 확인한다.

## 변경 절차

필요 정보를 요구사항 케이스에 명시하고, 해당 계약과 필드 설명 및 정적 예시를 함께 수정한다. `python3 verify.py`로 참조·구조·정보 연결을 검사한 뒤 생성물을 갱신한다. 추가 자료형 제안은 proposals.yaml에 현행 계약과 구분해 기록한다. 테스트 문항·코드 목록의 확보와 구현·운영 정책은 스키마의 미완성 항목으로 관리하지 않는다.

[검증 결과](VERIFIED.md)는 선언한 정적 예시의 표현 가능성을 보여준다. 실제 모델의 정답률, 입력 조립의 선택 정확성, 저장·전달 동작의 성공을 뜻하지 않는다.

## 사람용 웹

[웹뷰어](https://sdabin1209.github.io/HealthCheckSchema/)는 GitHub Pages 배포 주소이며 최초 설정과 배포가 완료된 뒤 이용할 수 있다. `main` 변경 시 검증과 빌드를 통과한 웹을 자동 갱신한다. 배포 방법과 실패 확인은 [웹 유지보수 안내](presentation/README.md#github-pages-배포)를 따른다.

[웹 유지보수 안내](presentation/README.md)에 빌드와 화면 수정 방법이 있다. `presentation/dist/index.html`은 계약·타입·정적 예시를 탐색하는 독립 실행 파일이다. 웹 소스·데이터·검사 결과는 `presentation/`에 분리하며 일반 문서와 계약 원본의 역할을 대신하지 않는다. 스키마 검증에는 웹이나 Node.js가 필요하지 않다.

검증 완료와 생성 기준은 구분한다. 성공 결과의 항목과 무결성 검사 범위는 [정적 무결성 검사](docs/static-integrity.md)에 설명한다.
