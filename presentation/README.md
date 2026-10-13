# 사람에게 보여주는 스키마 웹

이 디렉토리는 문진 데이터 계약을 탐색하는 Svelte 5 웹의 소스와 빌드 결과만 보관한다. 계약 원본은 상위 프로젝트의 `work/contracts/`, 요구사항·정적 예시는 `work/testcases/`에 있다. 웹의 문구·배치·상호작용은 계약을 정의하거나 변경하지 않는다.

## 화면

- 구조 지도: 12개 컴포넌트의 역할·이유·계약, `bindings.yaml`의 입력 출처·출력 소비와 `output_bindings.yaml`의 저장 목적. 입력·출력 필터와 상세 표로 양쪽 필드를 확인한다.
- 계약·타입: 경계 계약과 공통 타입의 구조, 필수 여부, 제약, 의미, 필요한 이유, 근거 요구사항. 참조 타입과 케이스로 이동한다.
- 정적 예시: 모든 요구사항의 작성된 JSON을 턴·계약·시점별로 확인한다. 예시를 실행하거나 DB 상태를 계산하지 않는다.
- 계약 제안: 현행 계약과 별도로 추가하는 자료형의 목적과 생성 시점의 정적 검사 보고서 요약.

지도는 선언된 입력 출처·출력 소비·저장 목적을 표시하며 실행 순서도나 DB 쓰기 실행 결과가 아니다. 저장 API 초안은 현행 계약과 구분한다. 전체 문항·공식 코드표가 확보되었다는 뜻도 아니다.

## 빌드와 실행

Node.js 22.12 이상과 Python 3.10 이상을 사용한다. 최초 준비는 프로젝트 루트에서 한다.

```sh
python3 -m pip install -r requirements.txt
python3 verify.py
cd presentation
npm ci
npm run data
npm run check
npm run test
npm run build
npm run test:dom
```

`dist/index.html` 하나를 브라우저에서 연다. JavaScript·CSS·데이터가 모두 들어 있어 서버나 인터넷 연결이 필요 없다. 생성 시각 대신 계약 버전과 원본 해시로 기준을 식별한다. 예시 전체를 포함하므로 파일 크기는 수 MB다. 최근 Chrome·Edge·Firefox·Safari를 대상으로 한다.

개발 화면은 `npm run dev`로 실행한다. 화면 변경은 Vite가 갱신한다. 개발 서버 실행 중 계약·예시 원본을 바꿨다면 루트의 `python3 verify.py`를 실행한 뒤 `npm run data`로 웹 데이터를 다시 생성한다.

`npm run build`는 데이터 생성기를 먼저 실행한다. `generated/verification_result.json`의 성공 결과가 없거나 현재 계약·검사 코드·생성물의 해시와 다르면 중단한다. 먼저 루트에서 `python3 verify.py`로 검증과 생성물을 갱신해야 한다. `verify.py`는 웹 빌드를 실행하지 않으므로 스키마만 사용하는 사람에게 Node.js를 요구하지 않는다.

## GitHub Pages 배포

공개 주소는 https://sdabin1209.github.io/HealthCheckSchema/ 이다. 저장소 관리자는 최초 한 번 Settings → Pages → Build and deployment → Source에서 GitHub Actions를 선택한다. 최초 배포 전에는 이 주소에 웹이 없으며, 설정 전에 배포 작업이 실패했다면 설정 후 Actions에서 `Schema viewer Pages` → Run workflow → `main`으로 다시 실행한다.

`.github/workflows/pages.yml`은 `main` push, `main` 대상 PR, 수동 실행을 받는다. Python 계약·정적 예시 검증, 웹 데이터 생성, Svelte 검사, 웹 데이터 테스트, 빌드, DOM 에뮬레이터 검사를 모두 통과해야 배포 산출물을 만든다. 이 검사는 실제 브라우저의 시각적 배치나 업무 컴포넌트 동작을 보증하지 않는다. PR과 `main` 이외 브랜치의 수동 실행은 검사·빌드만 수행한다. 배포 권한은 별도 배포 job에만 부여한다.

평소에는 계약·예시 원본 또는 웹 소스를 수정하고 `main`에 push한다. 웹은 같은 공개 주소에서 갱신된다. 변경 없이 재배포하려면 Actions의 Run workflow를 사용한다. 실행 결과와 실패 단계는 해당 워크플로 실행에서 확인한다. 실패하거나 실행이 취소되면 새 배포가 완료되지 않을 수 있으므로 기존 웹을 최신 원본으로 간주하지 않는다.

빌드는 `dist/`를 비우고 새 결과를 만들며 `presentation/dist/`의 내용만 Pages에 전달한다. 소스, 계약 문서, `node_modules/`는 게시 대상에 넣지 않는다. `dist/`와 웹용 생성 데이터는 Git 추적에서 제외하고 별도 `gh-pages` 브랜치는 사용하지 않는다. 현재 산출물은 JS·CSS·데이터를 포함한 `index.html` 하나다. 나중에 별도 파일을 쓰더라도 상대 경로 기준(`base: './'`)을 유지한다.

웹의 원본 식별 정보에는 계약 버전·계약 원본 해시와 함께 CI가 `VITE_BUILD_COMMIT`에 전달한 커밋 SHA를 표시한다. 커밋은 UI 변경까지 포함한 배포 기준을 식별하기 위한 웹 빌드 정보이며 계약 필드나 계약 버전이 아니다. 로컬 빌드에서 이 환경 변수가 없으면 커밋 표시는 생략한다. Pages가 공개하는 웹은 마지막 성공 배포이며 저장소의 최신 커밋과 다를 수 있다.

## 파일의 책임

| 위치 | 책임 | 수정 방법 |
|---|---|---|
| `src/components/StructureMap.svelte` | 컴포넌트 지도와 연결 상세 | 표시 방식 변경 시 편집 |
| `src/components/ContractExplorer.svelte`, `SchemaPanel.svelte`, `SchemaNode.svelte` | 계약 목록·구조·의미·참조 탐색 | 화면 변경 시 편집 |
| `src/components/CaseExplorer.svelte` | 요구사항 및 정적 예시 탐색 | 화면 변경 시 편집 |
| `src/components/ProposalsView.svelte` | 추가 자료형 제안과 범위 안내 | 화면 변경 시 편집 |
| `src/components/JsonBlock.svelte` | JSON 표시·파일 저장 | 공통 기능 변경 시 편집 |
| `src/lib/explorer.svelte.js` | 탐색 상태·주소·이동 | 탐색 동작 변경 시 편집 |
| `src/lib/data.js` | 읽기·내보내기 유틸리티 | 표시 데이터 처리 변경 시 편집 |
| `scripts/export_data.py` | 계약·의미·근거·입력 출처·예시를 원본에서 추출 | 원본 구조 변경 시 검토 |
| `src/lib/generated-data.json` | 웹용 생성 데이터 | 직접 편집하지 않음 |
| `src/App.svelte`, `src/style.css` | 화면 조합·공통 스타일·반응형 배치 | UI 변경 시 편집 |
| `dist/index.html` | 독립 실행용 빌드 결과 | 직접 편집하지 않음 |
| `tests/` | 원본 보존 및 웹 동작 검사 | 기능 변경 시 검토 |

컴포넌트는 Svelte 5 runes와 콜백 이벤트를 사용한다. 탐색 상태는 context로 공유하며 계약·업무 정책을 UI 안에 복제하지 않는다. 데이터 생성기는 `spec_sources.py`를 재사용하고 중복 예시 값을 묶어 저장하되 원본 값은 변형하지 않는다. 다운로드 Schema에는 원본 의미·근거가 주석 키로 추가되며 구조 제약은 동일하다.

컴포넌트를 추가하면 계약 원본에서 목록·계약 버튼은 자동 갱신된다. 지도 좌표는 `src/lib/map-layout.js`의 `boxes`에서 역할별로 배치한다. 지도 박스 좌표와 기본 연결 경로는 reference-layout.json에 보관한다. 추가 연결 경로는 map-layout.js에서 정의한다. 같은 컴포넌트 사이의 같은 전달 종류는 화살표 하나로 묶으며 상세 목록에서 개별 계약을 선택한다. 초안 저장 API는 지도에서 실제 채택된 연결처럼 표시하지 않는다. 경로의 박스 내부 통과 여부를 검사한다. 공통 타입·필드·예시를 추가할 때는 화면 파일에 데이터를 추가하지 않고 원본을 수정한다.

## 화면 동작 검사

`npm run test:dom`은 빌드된 HTML을 Happy DOM에서 실행해 화면 생성·지도 선택·참조 이동·필터·주소 복원·테마 전환을 검사한다. 실제 브라우저의 배치·다운로드·접근성·모바일 화면 검증을 대신하지 않는다.

아래 명령은 실제 Chromium 검사에 사용한다.

```sh
npx playwright install chromium
npm run test:browser
```

선택적으로 `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`에 설치된 Chromium 경로를 지정할 수 있다. 검사기는 로컬 `dist/index.html`을 직접 열어 탐색·필터·참조 이동·다운로드·주소 복원·모바일 가로 넘침을 검사한다. 결과는 `test-results/`에 쓴다. 이 검사는 업무 컴포넌트의 동작이나 모델 정답률을 검사하지 않는다.

RAW 데이터 엔드포인트와 서버는 포함하지 않는다. `generated-data.json`은 이 웹을 빌드하기 위한 내부 생성물이므로 별도 외부 API 계약으로 사용하지 않는다.

지도는 처음에 전체 연결을 표시한다. 컴포넌트 선택은 관련 입력·출력을, 화살표 선택은 해당 연결을 강조하고 나머지는 흐리게 표시한다. 연결을 제거하지 않으며 선택 해제로 전체 보기로 복원한다.
