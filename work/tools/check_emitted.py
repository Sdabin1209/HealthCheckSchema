"""Validate generated bundles independently against canonical JSON source."""
from pathlib import Path
import json
import sys
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import spec_sources as S

def check():
    defs=S.definitions()
    base=ROOT/'generated/schemas'
    failures=[]
    actual=json.loads((base/'all.json').read_text())
    if actual.get('$defs')!=defs:failures.append('all.json differs from contract source')
    io={n for c in S.components() for n in c['contracts'].values()}
    proposed={n for c in S.components() for role,n in c['contracts'].items() if c.get('contract_status',{}).get(role)=='proposal'}
    if {p.stem for p in (base/'standalone').glob('*.json')}!=io-proposed:failures.append('standalone contract set differs')
    if {p.stem for p in (base/'proposals').glob('*.json')}!=proposed:failures.append('proposal contract set differs')
    for name in io:
        folder='proposals' if name in proposed else 'standalone'
        doc=json.loads((base/folder/f'{name}.json').read_text())
        try:Draft202012Validator.check_schema(doc)
        except Exception as e:failures.append(f'{name}: {e}')
        expected={n:defs[n] for n in S.dependencies(name,defs)}
        if doc.get('$defs')!=expected:failures.append(f'{name}: stale or incomplete dependencies')
        if doc.get('$ref')!=f'#/$defs/{name}':failures.append(f'{name}: wrong entry reference')
    tc=S.cases()
    if S.read_yaml(ROOT/'generated/requirements_cases.yaml')!=tc:failures.append('stale requirement reference cases')
    meta=json.loads((ROOT/'generated/source_manifest.json').read_text())
    if meta['source_sha256']!=S.source_digest():failures.append('source digest differs')
    print(json.dumps({'standalone':len(io-proposed),'proposals':len(proposed),'failures':failures},ensure_ascii=False))
    return failures

if __name__=='__main__':raise SystemExit(bool(check()))
