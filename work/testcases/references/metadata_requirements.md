# 값과 기록 정보의 필요성

이 문서는 데이터 전달 과정에서 보존해야 할 정보와, 그 정보가 없을 때 구분할 수 없는 상황을 설명한다. 허용 구조와 필드별 의미는 이 저장소의 계약 원본에 정의한다.

| 정보 | 필요한 이유 | 계약과 정적 요구 |
|---|---|---|
| 값의 정밀도 | 같은 숫자라도 확정적으로 말한 값과 근사 표현에서 얻은 값은 다르다. 숫자만 전달하면 그 차이가 저장과 응답 재료에서 사라진다. 미수집 상태도 확정값으로 오인하지 않도록 구분한다. | `ValueMetadata.precision`; T1, T3, T4 |
| 원문 근거 목록 | 합산·정정·비교에 여러 구절이 사용될 수 있으므로 근거 하나로 축약하지 않는다. 각 근거의 턴 순번·위치 단위·범위·구절을 함께 보존해야 여러 턴과 Unicode 문자열에서도 출처를 식별할 수 있다. | `ValueMetadata.evidence[]`, `Evidence`, `TextSpan`; T1, T2, T9 |
| 코드와 표시 이름 | 표시 이름이 달라져도 같은 선택지·단위를 식별할 수 있어야 한다. 안정적인 코드와 사람이 읽는 이름을 구분하고, 선택 가능한 코드 목록도 함께 정의한다. | `ChoiceDef`, `UnitDef`, `SlotDef`, `Value`; T3, T4 |
| 세부 문제 정보 | 단위 문제·범위 문제·조건 불충족을 하나의 포괄 코드로만 표현하면 어느 칸을 어떤 이유로 다시 확인해야 하는지 알 수 없다. 세부 사유와 관련 슬롯을 함께 전달한다. | `ProblemDetail`, `ItemCheck.problem_details`; T3, T4 |
| 상태 버전과 저장 결과 | 조회한 상태와 저장 기준을 연결하고, 성공·동시 수정 충돌·오류를 구분해야 한다. 처리 결과와 반환 revision을 따로 표현하여 서로 다른 시점의 상태를 같은 것으로 취급하지 않는다. | `SessionLoadRequest/Result`, `SessionCommitRequest/Result`; T5~T8 |
| 반영 여부 미확인 | 오류 응답이나 전송 실패만으로 쓰기가 반영되지 않았다고 단정할 수 없다. 반영됨·미반영·확인 불가를 구분하여 저장 결과의 불확실성을 보존한다. | `WriteOutcome`, `SessionCommitResult.write_outcome`; T10 |

공통 타입의 원본은 [계약 manifest](../../contracts/manifest.yaml)에서 찾는다. 필드별 의미와 필요한 이유는 `work/contracts/semantics/` 및 `work/contracts/components/`의 설명 파일에 있고, 전달 관계는 [연결 인덱스](../../out/connections.md)에 있다.

T1~T10의 요구 원본은 [cases/T.yaml](../cases/T.yaml), 완전한 정적 예시는 `work/testcases/case_shapes/T1.json`부터 `T10.json`까지다. 저장 요청·결과는 [추가 계약 제안](../../contracts/proposals.yaml)으로 구분한다. 이 문서는 실제 입력의 정답, 저장 API의 채택, 재시도 정책이나 실행 성공을 정하지 않는다.
