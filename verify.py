"""Run static contract checks; publish completion only when every stage succeeds."""
from pathlib import Path
import subprocess,sys,json
import spec_sources as S
import verification_state as V
ROOT=Path(__file__).resolve().parent
STAGES=[('원본 Schema·필드 설명·요구 참조','work/tools/check_contracts.py'),
        ('전달용 Schema·문서 생성','work/tools/build.py'),
        ('원본과 생성물 대조','work/tools/check_emitted.py'),
        ('요구값·정형 예시 표현 가능 여부','work/tools/check_representation.py'),
        ('전체 케이스의 정보·완전한 예시·계약 연결','work/tools/check_case_shapes.py'),
        ('입력 조립 명세·정적 전달 예시','work/tools/check_handoffs.py'),
        ('자료 무결성','work/tools/check_information_integrity.py')]

def run(root=ROOT,runner=subprocess.run):
    root=Path(root);V.invalidate(root);checker=V.checker_digest(root);source=None
    for label,script in STAGES:
        print(label,flush=True);runner([sys.executable,script],cwd=root,check=True)
        if script=='work/tools/build.py':source=V.source_digest(root)
    print('Schema 회귀 검사',flush=True)
    runner([sys.executable,'-m','pytest','tests','-q'],cwd=root,check=True)
    import yaml
    version=yaml.safe_load((root/'work/contracts/manifest.yaml').read_text())['version']
    V.publish(root,version,source,checker)
    print('정적 스키마 검증 통과. 실제 컴포넌트 동작을 실행하지 않았습니다.',flush=True)

if __name__=='__main__':
    if sys.argv[1:]==['--check']:print(json.dumps(V.require_valid(ROOT,S.manifest()['version']),ensure_ascii=False))
    elif sys.argv[1:]:raise SystemExit('usage: python3 verify.py [--check]')
    else:run()
