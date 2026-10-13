"""Check source integrity, required field semantics and traceability claims."""
from pathlib import Path
from collections import Counter
import json
import sys
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import spec_sources as S

def check():
    problems = []
    def bad(message): problems.append(message)
    defs = S.definitions()
    tc = S.cases()
    case_schema=json.loads((S.WORK/'testcases/format.schema.json').read_text())
    for e in Draft202012Validator(case_schema).iter_errors({'cases':tc['cases']}):
        bad(f'case format {list(e.absolute_path)}: {e.message[:150]}')
    ids = [c['id'] for c in tc['cases']]
    for cid,n in Counter(ids).items():
        if n != 1: bad(f'duplicate case: {cid}')
    case_ids = set(ids)
    situation_ids = {s['id'] for s in tc['상황목록']}
    for c in tc['cases']:
        if not c.get('왜'): bad(f'{c["id"]}: missing purpose')
        for sid in c['상황']:
            if sid not in situation_ids: bad(f'{c["id"]}: missing situation {sid}')
        for i,st in enumerate(c.get('steps') or [c],1):
            comp = st.get('comparison',{})
            if comp and comp.get('mode') != 'declared_fields': bad(f'{c["id"]}:{i}: unsupported comparison mode')
            if not st.get('input') and '성질' not in c: bad(f'{c["id"]}:{i}: missing input')
    aggregate = {'$schema':S.SCHEMA_URI, '$defs':defs}
    try: Draft202012Validator.check_schema(aggregate)
    except Exception as e: bad(f'metaschema: {e}')
    covered = set()
    for c in S.components():
        for name in c['contracts'].values():
            try: covered.update(S.dependencies(name,defs))
            except ValueError as e: bad(str(e))
    for n in set(defs)-covered: bad(f'unused definition: {n}')
    annotated = 0
    for name,node in defs.items():
        notes = S.semantics(name)
        for pointer,note in notes.items():
            annotated += 1
            try: S.at_pointer(node,pointer)
            except (KeyError,IndexError,ValueError,TypeError): bad(f'{name}{pointer}: dangling semantic pointer')
            if not note.get('meaning') or not note.get('why'): bad(f'{name}{pointer}: missing meaning/why')
            if not note.get('case_refs'):bad(f'{name}{pointer}: missing case reference')
            for cid in note.get('case_refs',[]):
                if cid not in case_ids: bad(f'{name}{pointer}: missing case {cid}')
            status = note.get('evidence_status')
            if status not in ('requirement_reference',): bad(f'{name}{pointer}: unknown evidence status')
            for assertion in note.get('assertions',[]):
                case=next((c for c in tc['cases'] if c['id']==assertion.get('case')),None)
                if not case:bad(f'{name}{pointer}: missing referenced requirement');continue
                try:
                    step=(case.get('steps') or [case])[assertion['turn']-1]
                    if assertion['turn']<1:raise ValueError('invalid turn')
                    S.at_pointer(step['expect'],assertion['expect_pointer'])
                except (KeyError,IndexError,ValueError,TypeError):bad(f'{name}{pointer}: invalid requirement locator')
        def walk(n,p=''):
            if isinstance(n,dict):
                # The format vocabulary may grow, but annotation-driven runtime is forbidden.
                for key in ('title','description','x-why','x-cases'):
                    if key in n: bad(f'{name}{p}: annotation in wire schema: {key}')
                if p == '' or '/properties/' in p and p.split('/')[-2] == 'properties' or 'const' in n or n.get('type')=='null':
                    if p not in notes: bad(f'{name}{p}: field/branch has no semantics')
                for k,v in n.items():walk(v,p+'/'+k.replace('~','~0').replace('/','~1'))
            elif isinstance(n,list):
                for i,v in enumerate(n):walk(v,p+'/'+str(i))
        walk(node)
    bindings = S.read_yaml(S.WORK/'contracts/bindings.yaml')['inputs']
    for c in S.components():
        name = c['contracts'].get('input')
        if not name: continue
        fields=defs[name].get('properties',{})
        b=bindings.get(name,{}).get('fields',{})
        if set(fields)!=set(b): bad(f'{name}: input bindings differ from field list')
        for field,entry in b.items():
            if not entry['sources']: bad(f'{name}.{field}: no source contract')
            for source in entry['sources']:
                try: S.field_schema(source['contract'],source['field_path'],defs)
                except (KeyError,TypeError):bad(f'{name}.{field}: unknown source field {source}')
                if 'schema_pointer' in source:
                    try: S.at_pointer(defs[source['contract']],source['schema_pointer'])
                    except (KeyError,IndexError,ValueError,TypeError):bad(f'{name}.{field}: unknown source branch {source}')
            if entry['snapshot'] not in ('turn_start','session_lookup','post_store_write','post_turn_write','current_turn'):bad(f'{name}.{field}: invalid snapshot')
            if entry['meaning_pointer'] not in S.semantics(name):bad(f'{name}.{field}: missing source description')
    # Request contracts are operation-specific ports, not additional business components.
    checked={c['contracts'].get('input') for c in S.components()}
    for name,entry in bindings.items():
        if name in checked:continue
        fields=defs[name].get('properties',{})
        b=entry['fields']
        if set(fields)!=set(b):bad(f'{name}: request bindings differ from field list')
        for field,item in b.items():
            if item['meaning_pointer'] not in S.semantics(name):bad(f'{name}.{field}: missing request source description')
            for source in item['sources']:
                try:
                    S.field_schema(source['contract'],source['field_path'],defs)
                    if 'schema_pointer' in source:S.at_pointer(defs[source['contract']],source['schema_pointer'])
                except (KeyError,IndexError,ValueError,TypeError):bad(f'{name}.{field}: invalid request source')
    expectations=S.read_yaml(S.WORK/'contracts/expectations.yaml')['expectations']
    for c in tc['cases']:
        for i,st in enumerate(c.get('steps') or [c],1):
            for key in st.get('expect',{}):
                if key not in expectations:bad(f'{c["id"]}:{i}: expectation has no responsible contract: {key}')
    for key,e in expectations.items():
        try:S.field_schema(e['contract'],e['field_path'],defs)
        except (KeyError,TypeError):bad(f'{key}: invalid expected contract field')
    result={'definitions':len(defs),'cases':len(ids),'semantic_nodes':annotated,'requirement_references_only':True,'component_correctness_checked':False,'failures':problems}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result

if __name__ == '__main__':
    raise SystemExit(bool(check()['failures']))
