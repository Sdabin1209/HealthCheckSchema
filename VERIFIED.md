# 스키마 검증 결과

검증 명령은 프로젝트 루트의 `python3 verify.py`다. 대상 계약 버전과 원본 해시는 `generated/source_manifest.json`에 기록한다. 이 문서는 정적 계약 검사 결과 요약이며 변경 기록이나 구현 명세가 아니다.

| 항목 | 결과 |
|---|---|
| 계약 정의 / 컴포넌트 | 110개 / 12개 |
| 현재 배포 경계 / 제안 경계 | 23개 / 4개 |
| 요구사항 케이스 | 226개 |
| 케이스별 정보 항목 | 5513개, 미연결 0 |
| 완전한 케이스 예시 | 4553개, Schema 위반 0 |
| 정형 요구값 / 구조 예시 | 50개 / 39개, 선언 결과와 일치 |
| 전달 설명 / 완전한 전달 예시 | 59개 필드 / 17개, 오류 0 |
| 자료 무결성 검사 | 전체 4584개 예시 / 중복 제외 2655개 payload, 오류 0 |
| 구조 회귀 검사 | 61개 통과 |
| 원본·생성물·참조 정합성 | 통과 |

## 근거

- `generated/representation_report.json`: 정형 값·경계 예시 검사.
- `generated/case_representation_report.json` 및 `.md`: 케이스별 정보 연결과 예시 검사.
- `generated/handoff_report.json`: 입력 출처·정적 필드 전달 검사.
- `generated/information_integrity_report.json`: 근거 위치·등록 코드·문제 분류·조회 revision의 내부 관계 검사.
- `generated/verification.log`: 전체 실행 로그.

## 적용 범위

모델·업무 컴포넌트·DB 서버는 실행하지 않았다. 입력의 정답 코드, 공감·진단 등 자연어 의미, 원문 근거의 실제 판단 타당성, 전체 상태 전이, 저장·재시도·전달 동작은 검증하지 않았다. 모든 값 조합·미래 문항·필드의 최소성을 증명하지 않는다.

메타데이터 검사 중 JSON Schema 단독으로 검사할 수 없는 위치 길이·코드 참조·revision 관계는 출력 내부의 정적 자료 무결성으로 구분한다. 실제 입력에 올바른 답이나 사유를 선택했는지는 판단하지 않는다.

저장 포트 4개는 API 채택 합의 전 데이터 계약 초안이다. 현재 배포 계약과 별도 proposals 디렉터리에 있으며, 정적 예시 통과는 API 확정이나 저장 동작 성공을 뜻하지 않는다. 현재 포함된 실제 문항 예시는 10개이며 DEMO.* 코드는 설명용이다. 문항·코드는 검증 재료이며 데이터의 개수나 특정 목록을 범용 Schema의 완성 조건으로 삼지 않는다. 저장 자료형의 추가 제안은 `work/contracts/proposals.yaml`에 구분한다.

상세 해석은 [검증 방법](docs/validation.md)과 [정보 계약](docs/information.md)을 참고한다.

검증 완료 정보는 `generated/verification_result.json`이다. 현재 원본·검사기·생성물과의 일치는 `python3 verify.py --check`로 확인한다. 정보 항목의 필요 이유와 검사 범위는 [정적 무결성 검사](docs/static-integrity.md)에 있다.
