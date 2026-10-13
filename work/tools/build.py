"""Build disposable runtime bundles and readable views from reviewed sources."""
from pathlib import Path
import json
import shutil
import sys
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import spec_sources as S

HEAD = '<!-- 생성물. 직접 고치지 말 것: python3 work/tools/build.py -->\n\n'

def write(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding='utf-8')

def wire_shape(node):
    bits = []
    if '$ref' in node: bits.append('→ ' + node['$ref'].split('/')[-1])
    if 'type' in node: bits.append(str(node['type']))
    if 'const' in node: bits.append('const=' + json.dumps(node['const'], ensure_ascii=False))
    for k in ('pattern','format','minimum','maximum','minLength','maxLength','minItems','maxItems','additionalProperties'):
        if k in node: bits.append(f'{k}={node[k]}')
    if 'enum' in node: bits.append('enum=' + json.dumps(node['enum'], ensure_ascii=False))
    for k in ('oneOf','anyOf','allOf'):
        if k in node: bits.append(f'{k}({len(node[k])}분기)')
    for k in ('if','then','else'):
        if k in node:bits.append(k)
    return '; '.join(bits)

def field_rows(name, defs):
    rows = []
    notes = {n:S.semantics(n) for n in S.dependencies(name, defs)}
    def walk(n, path, source_name, ptr, required='', stack=()):
        note = notes[source_name].get(ptr, {})
        rows.append((path, required, wire_shape(n), note.get('meaning',''), note.get('why',''), ', '.join(note.get('case_refs',[]))))
        if '$ref' in n:
            target = n['$ref'].split('/')[-1]
            if target not in stack:
                walk(defs[target], path + f' → {target}', target, '', required, (*stack, target))
        for key, value in n.get('properties', {}).items():
            escaped = key.replace('~','~0').replace('/','~1')
            walk(value, path + '.' + key, source_name, ptr + '/properties/' + escaped,
                 '필수' if key in n.get('required',[]) else '선택', stack)
        if 'items' in n and isinstance(n['items'], dict):
            walk(n['items'], path + '[]', source_name, ptr + '/items', '배열 항목', stack)
        for op in ('oneOf','anyOf','allOf'):
            for i, branch in enumerate(n.get(op,[])):
                walk(branch, path + f' [{op}:{i}]', source_name, ptr + f'/{op}/{i}', '해당 분기', stack)
        for keyword in ('if','then','else'):
            if keyword in n:
                walk(n[keyword],path+' ['+keyword+']',source_name,ptr+'/'+keyword,'조건',stack)
    walk(defs[name], name, name, '', '', (name,))
    return rows

def table(head, rows):
    result = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    for row in rows:
        result.append('| ' + ' | '.join(str(x).replace('|','\\|').replace('\n',' ') for x in row) + ' |')
    return '\n'.join(result) + '\n'

def render_current_example(template, version):
    import copy
    result=copy.deepcopy(template)
    meta=result['generation']
    if meta.get('template') is not True:raise ValueError('Not a current-contract example template')
    for pointer in meta['version_fields']:
        parent,_,token=pointer.rpartition('/')
        node=S.at_pointer(result,parent)
        if node[token]!='__CURRENT_CONTRACT_VERSION__':raise ValueError('Missing explicit version placeholder')
        node[token]=version
    meta['template']=False
    meta['generated']=True
    return result


def generate_current_examples():
    version=S.manifest()['version']
    for path in sorted((S.WORK/'testcases/schema_example_templates').glob('*.json')):
        template=json.loads(path.read_text())
        result=render_current_example(template,version)
        result['generation']['template_source']='work/testcases/schema_example_templates/'+path.name
        write(S.WORK/'testcases/schema_examples'/path.name,json.dumps(result,ensure_ascii=False,indent=2)+'\n')


def build():
    from verification_state import invalidate
    invalidate(ROOT)
    generate_current_examples()
    defs=S.definitions();comps=S.components();tc=S.cases()
    base=ROOT/'generated';schemas=base/'schemas'
    if schemas.exists():shutil.rmtree(schemas)
    schemas.mkdir(parents=True)
    bundle={'$schema':S.SCHEMA_URI,'$id':'all.json','$defs':defs}
    write(schemas/'all.json',json.dumps(bundle,ensure_ascii=False,indent=2)+'\n')
    boundaries={n for c in comps for n in c['contracts'].values()}
    proposed={n for c in comps for role,n in c['contracts'].items() if c.get('contract_status',{}).get(role)=='proposal'}
    for name in defs:
        write(schemas/f'{name}.json',json.dumps({'$schema':S.SCHEMA_URI,'$id':f'{name}.json','$ref':f'all.json#/$defs/{name}'},ensure_ascii=False,indent=2)+'\n')
    for name in sorted(boundaries):
        folder='proposals' if name in proposed else 'standalone'
        doc={'$schema':S.SCHEMA_URI,'$id':f'{folder}/{name}.json','$ref':f'#/$defs/{name}','$defs':{n:defs[n] for n in sorted(S.dependencies(name,defs))}}
        write(schemas/folder/f'{name}.json',json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    write(schemas/'INDEX.md',HEAD+'# 전달용 Schema\n\n원본은 `../../work/contracts/`, 탐색은 `../../work/schema.md`.\n\n'+table(['컴포넌트','방향','계약','상태'],[(c['name'],role,n,c.get('contract_status',{}).get(role,'current')) for c in comps for role,n in c['contracts'].items()]))
    write(base/'requirements_cases.yaml','# 요구사항 참고 자료. 컴포넌트를 실행하거나 정답을 판정하지 않는다.\n'+yaml.safe_dump(tc,allow_unicode=True,sort_keys=False,width=110))
    index=HEAD+'# 테스트케이스에서 출발하는 스키마 계약\n\n요구사항은 `testcases/cases/`, 값의 구조는 `contracts/`, 업무 규칙의 참고 명세는 `rules/`다.\n'
    index+='이 프로젝트는 필요한 값을 표현할 수 있는지 검사하며 업무 동작을 구현·평가하지 않는다. [구조와 책임](../docs/architecture.md), [검증 방법](../docs/validation.md), [계약 원본](contracts/README.md)을 함께 읽는다.\n\n'
    index+=table(['컴포넌트','책임','입출력 원본','중첩 필드'],[(c['name'],c['responsibility'],', '.join(f'[{role}](contracts/{S.manifest()["definitions"][n]["schema"]})' for role,n in c['contracts'].items()),f'[상세](out/components/{c["id"]}.md)') for c in comps])
    index+='\n정형 예시의 표현 가능 여부는 `../generated/representation_report.json`에 기록한다.\n'
    index+='\n[전체 필드 연결](out/connections.md)에서 출력 소비와 저장 목적을 추적한다. 에이전트 탐색은 [안내](../docs/agent-guide.md)를 따른다.\n'
    write(S.WORK/'schema.md',index)
    owners={n:c['name'] for c in comps for n in c['contracts'].values()}
    connections=[]
    for target,binding in S.read_yaml(S.WORK/'contracts/bindings.yaml')['inputs'].items():
        for field,info in binding['fields'].items():
            for source in info['sources']:
                name=source['contract'];status='proposal' if name in proposed or target in proposed else 'current'
                path=source.get('field_path') or '(전체)'
                if source.get('schema_pointer'):path+=' [Schema '+source['schema_pointer']+']'
                connections.append((owners[name],name+'.'+path,owners[target],target+'.'+field,info['snapshot'],info['transfer']['mode'],status,info['transfer']['description']))
    writes=[]
    for b in S.read_yaml(S.WORK/'contracts/output_bindings.yaml')['bindings']:
        a,z=b['source_contract'],b['target_contract']
        writes.append((owners[a],a+'.'+b['source_field'],owners[z],z+'.'+b['target_field'],b['mode'],b['description'],b['evidence']))
    connection_doc=HEAD+'# 컴포넌트와 필드의 전달 연결\n\n원본은 `../contracts/bindings.yaml`과 `../contracts/output_bindings.yaml`이다. 생산·소비 관계를 추적하는 인덱스이며 실제 호출·조회·입력 조립·전달은 Orchestrator의 책임이다. 전송 구현이나 동작 성공을 나타내지 않는다. proposal은 현행 계약과 별도로 제안된 자료형이다.\n\n## 출력·상태에서 입력으로\n\n'
    connection_doc+=table(['원천 컴포넌트','원천 계약·필드','목적 컴포넌트','목적 계약·필드','시점','전달 방식','상태','전달 설명'],connections)
    connection_doc+='\n## 출력에서 저장 상태로 전달되는 쓰기 자료\n\n아래 자료는 반영할 결정·갱신·기록이다. 원천과 저장 상태의 값이 같다는 직접 복사나 실제 반영 성공을 뜻하지 않는다.\n\n'
    connection_doc+=table(['생산 컴포넌트','출력 계약·필드','저장소','목적 계약·필드','자료 방식','목적 설명','원본 근거'],writes)
    write(S.WORK/'out/connections.md',connection_doc)
    for c in comps:
        body=HEAD+f'# {c["name"]} ({c["title"]})\n\n{c["responsibility"]}\n\n이 문서는 현재 계약 원본에서 생성한 필드 안내다. 업무 실행·정답 판정의 검증 결과가 아니다. 전체 역할은 [구조 설명](../../../docs/architecture.md), 검사 범위는 [검증 방법](../../../docs/validation.md)에 있다.\n\n'
        for role,name in c['contracts'].items():
            entry=S.manifest()['definitions'][name]
            body+=f'## {role}: {name}\n\n계약 상태: {c.get("contract_status",{}).get(role,"current")}. proposal은 실제 API 채택 합의를 기다리는 데이터 계약 초안이다.\n\n원본: [Schema](../../contracts/{entry["schema"]}), [의미·근거](../../contracts/{entry["semantics"]})\n\n'
            body+=table(['필드·분기 경로','필수 여부','값 제약·참조','무슨 값인가','왜 필요한가','근거 요구사항'],field_rows(name,defs))+'\n'
        write(S.WORK/'out/components'/f'{c["id"]}.md',body)
    mapping=S.read_yaml(S.WORK/'contracts/expectations.yaml')['expectations'];rows=[]
    for case in tc['cases']:
        for turn,step in enumerate(case.get('steps') or [case],1):
            for key in step.get('expect',{}):
                entry=mapping[key];rows.append((case['id'],turn,'expect.'+key,entry['contract'],entry['field_path'] or '(전체 경계)'))
    write(S.WORK/'out/requirements.md',HEAD+'# 요구 결과를 표현할 계약 위치\n\n이 연결표는 요구의 표현 위치를 보여준다. 입력에 대한 실제 정답을 판정하지 않는다.\n\n'+table(['케이스','턴','요구 결과','계약','필드'],rows))
    result={'contract_version':S.manifest()['version'],'source_sha256':S.source_digest(),'definitions':len(defs),'components':len(comps),'requirement_cases':len(tc['cases']),'standalone':len(boundaries-proposed),'proposed_boundaries':len(proposed)}
    write(base/'source_manifest.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result

if __name__=='__main__':print(json.dumps(build(),ensure_ascii=False))
