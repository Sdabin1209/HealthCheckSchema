"""Identity of successfully checked inputs and generated artifacts; no component execution."""
from pathlib import Path
import hashlib,json,os
from datetime import datetime, timezone

RESULT='verification_result.json'

def _digest(paths,base):
    h=hashlib.sha256()
    for p in sorted(paths):
        h.update(str(p.relative_to(base)).encode());h.update(b'\0');h.update(p.read_bytes())
    return h.hexdigest()

def source_digest(root):
    work=Path(root)/'work'
    return _digest([p for folder in ('contracts','testcases','rules') for p in (work/folder).rglob('*') if p.is_file()],work)

def checker_digest(root):
    root=Path(root)
    paths=[root/n for n in ('spec_sources.py','verification_state.py','verify.py','requirements.txt')]
    paths += list((root/'work/tools').glob('*.py'))+list((root/'tests').glob('*.py'))
    return _digest([p for p in paths if p.is_file()],root)

def artifact_digest(root):
    root=Path(root)
    paths=[p for p in (root/'generated').rglob('*') if p.is_file() and p.name not in (RESULT,'verification.log') and not p.name.endswith('.tmp')]
    paths += [root/'work/schema.md']+list((root/'work/out').rglob('*.md'))
    return _digest([p for p in paths if p.is_file()],root)

def invalidate(root):
    (Path(root)/'generated'/RESULT).unlink(missing_ok=True)

def publish(root,version,source,checker):
    root=Path(root)
    if source_digest(root)!=source or checker_digest(root)!=checker:raise ValueError('Verification inputs changed during the run')
    value={'status':'passed','contract_version':version,'source_sha256':source,'checker_sha256':checker,'artifacts_sha256':artifact_digest(root),'completed_at':datetime.now(timezone.utc).isoformat()}
    target=root/'generated'/RESULT;target.parent.mkdir(exist_ok=True)
    temp=target.with_suffix('.json.tmp');temp.write_text(json.dumps(value,indent=2)+'\n');os.replace(temp,target)
    return value

def require_valid(root,version):
    root=Path(root);target=root/'generated'/RESULT
    if not target.exists():raise ValueError('No successful verification record. Run python3 verify.py')
    result=json.loads(target.read_text())
    expected={'status':'passed','contract_version':version,'source_sha256':source_digest(root),'checker_sha256':checker_digest(root),'artifacts_sha256':artifact_digest(root)}
    for key,value in expected.items():
        if result.get(key)!=value:raise ValueError('Verification is stale: '+key+'. Run python3 verify.py')
    return result
