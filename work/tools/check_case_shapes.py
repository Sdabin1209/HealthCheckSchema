"""Check case-by-case static representation, never actual component behavior."""
from pathlib import Path
import hashlib
import json
import sys
from collections import Counter
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import spec_sources as S
from work.tools.declared_notation import value_preserved


def leaves(value,pointer):
    if isinstance(value,dict) and value:
        for key,child in value.items():
            token=str(key).replace('~','~0').replace('/','~1')
            yield from leaves(child,pointer+'/'+token)
    elif isinstance(value,list) and value:
        for index,child in enumerate(value):yield from leaves(child,pointer+'/'+str(index))
    else:yield pointer,value


def required_leaves(case):
    rows=[]
    for key in ('given','input','expect','성질'):
        if key in case:rows.extend(leaves(case[key],'/'+key))
    for index,step in enumerate(case.get('steps') or []):
        for key in ('given','input','expect'):
            if key in step:rows.extend(leaves(step[key],f'/steps/{index}/{key}'))
    return dict(rows)


def case_digest(case):
    return hashlib.sha256(json.dumps(case,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


KINDS={'literal','content_constraint','presence_constraint','relation_constraint',
       'routing_constraint','identity_constraint','fixture_context','collection_constraint'}


def carrier_node(defs, contract, data, pointer):
    """Resolve the actual payload field; a claim cannot point to an unrelated type."""
    name=contract; node=defs[name]; schema_pointer=''; current=data
    tokens=[t.replace('~1','/').replace('~0','~') for t in pointer.split('/')[1:]]
    for token in [*tokens, None]:
        if token is None:
            return name, schema_pointer, node
        while True:
            if '$ref' in node:
                name=node['$ref'].split('/')[-1];node=defs[name];schema_pointer='';continue
            branches=[]
            for op in ('oneOf','anyOf'):
                for i, branch in enumerate(node.get(op, [])):
                    if Draft202012Validator({**branch,'$defs':defs}).is_valid(current):
                        branches.append((op,i,branch))
            if branches:
                op,i,node=branches[0];schema_pointer+=f'/{op}/{i}';continue
            break
        if isinstance(current,list):
            node=node['items'];schema_pointer+='/items';current=current[int(token)]
        else:
            node=node['properties'][token]
            schema_pointer+='/properties/'+token.replace('~','~0').replace('/','~1')
            current=current[token]


def check(directory=None):
    directory=Path(directory) if directory else S.WORK/'testcases/case_shapes'
    defs=S.definitions();cases={c['id']:c for c in S.cases()['cases']}
    validators={name:Draft202012Validator({**node,'$defs':defs}) for name,node in defs.items()}
    notation=S.read_yaml(S.WORK/'contracts/case_notation.yaml')
    cached={};failures=[];rows=[];kinds=Counter();specimen_count=0;leaf_count=0
    paths={p.stem:p for p in directory.glob('*.json')}
    missing=sorted(set(cases)-set(paths));extra=sorted(set(paths)-set(cases))
    if missing:failures.append({'case':'index','reason':'missing case witnesses','details':missing})
    if extra:failures.append({'case':'index','reason':'unknown case witnesses','details':extra})
    for cid,case in cases.items():
        if cid not in paths:continue
        witness=json.loads(paths[cid].read_text());before=len(failures)
        def bad(reason,details=None):failures.append({'case':cid,'reason':reason,'details':details})
        if witness.get('case')!=cid:bad('case identity differs')
        if witness.get('case_sha256')!=case_digest(case):bad('requirement changed; static witness must be reviewed')
        if witness.get('scope')!='static_schema_representation' or witness.get('component_execution') is not False:
            bad('incorrect verification scope')
        specs=witness.get('specimens',[]);index={s['id']:s for s in specs}
        if len(index)!=len(specs):bad('duplicate specimen id')
        for sample in specs:
            specimen_count+=1
            name=sample['contract']
            if name not in validators:bad('unknown contract',name);continue
            key=(name,json.dumps(sample['data'],ensure_ascii=False,sort_keys=True))
            if key not in cached:
                cached[key]=[str(list(e.absolute_path))+': '+e.message[:180] for e in validators[name].iter_errors(sample['data'])]
            if cached[key]:bad('complete specimen violates schema',{'specimen':sample['id'],'errors':cached[key][:5]})
        need=required_leaves(case);covered=set();leaf_count+=len(need)
        for claim in witness.get('requirements',[]):
            try:
                source=claim['source_pointer'];declared=S.at_pointer(case,source)
                if declared!=claim['source_value']:bad('source requirement changed',source)
                claim_leaves=set(p for p,_ in leaves(declared,source))
                if not claim_leaves <= set(need):bad('claim points outside case facts/requirements',source)
                covered.update(claim_leaves)
                kind=claim['kind'];kinds[kind]+=1
                if kind not in KINDS:bad('unknown requirement kind',kind)
                if not claim.get('meaning'):bad('missing representation rationale',source)
                sample=index[claim['specimen']]
                payload=S.at_pointer(sample['data'],claim['data_pointer'])
                node=S.at_pointer(defs[claim['definition']],claim['schema_pointer'])
                actual_name,actual_pointer,actual_node=carrier_node(defs,sample['contract'],sample['data'],claim['data_pointer'])
                if (claim['definition'],claim['schema_pointer'])!=(actual_name,actual_pointer):
                    bad('schema reference does not describe payload field',source)
                if kind=='presence_constraint':
                    wanted=declared not in ('없음',False)
                    if (payload is not None)!=wanted:bad('static specimen does not preserve declared presence',source)
                if kind=='collection_constraint' and declared=={}:
                    if any(row.get('pending') is not None for row in payload):
                        bad('static specimen does not represent empty pending collection',source)
                if kind=='content_constraint' and declared=='없음' and claim['data_pointer']=='/log_entry':
                    if payload is not None:bad('static specimen does not represent absent log',source)
                for support in claim.get('supporting_fields',[]):
                    supporting=index[support['specimen']]
                    supporting_value=S.at_pointer(supporting['data'],support['data_pointer'])
                    if 'equals_payload' in support and supporting_value!=payload:
                        bad('static identity reference is inconsistent',source)
                    if 'encoded_value' in support:
                        if supporting_value!=support['encoded_value']:
                            bad('supporting field does not carry declared information',source)
                        if kind=='identity_constraint':
                            sn,sp,ss=carrier_node(defs,supporting['contract'],supporting['data'],support['data_pointer'])
                            if not value_preserved(declared,support['encoded_value'],ss,sn,sp,source,defs,notation):
                                bad('static identity carrier loses declared target',source)
                if kind in ('identity_constraint','routing_constraint') and not claim.get('supporting_fields'):
                    bad('missing static identity/routing carrier',source)
                if kind=='literal':
                    if not value_preserved(declared,claim['encoded_value'],node,claim['definition'],
                                           claim['schema_pointer'],source,defs,notation):
                        bad('authored encoding does not preserve declared information',source)
                    if payload!=claim['encoded_value']:bad('authored value is missing from complete specimen',source)
                    errors=[e.message for e in Draft202012Validator({**node,'$defs':defs}).iter_errors(claim['encoded_value'])]
                    if errors:bad('declared value cannot be represented at field',{'source':source,'errors':errors[:3]})
                # Prose and transition requirements are linked to the carrier;
                # their truth is deliberately not evaluated here.
            except (KeyError,IndexError,ValueError,TypeError) as error:bad('invalid requirement/field reference',str(error))
        uncovered=sorted(set(need)-covered)
        if uncovered:bad('unmapped required information',uncovered)
        for obligation in witness.get('structural_obligations',[]):
            try:
                S.at_pointer(case,obligation['source_pointer'])
                if obligation['kind']=='same_payload_definition':
                    node=defs[obligation['destination_contract']]['properties'][obligation['destination_field']]
                    refs=set(S.refs(node))
                    if '#/$defs/'+obligation['payload_definition'] not in refs:
                        bad('destination cannot carry original payload definition',obligation)
                elif obligation['kind']=='required_variants':
                    values=S.at_pointer(index[obligation['specimen']]['data'],obligation['data_pointer'])
                    represented={v[obligation['discriminator']] for v in values}
                    absent=set(obligation['required_values'])-represented
                    if absent:bad('required variants missing from complete specimen',sorted(absent))
                else:bad('unknown structural obligation',obligation['kind'])
            except (KeyError,IndexError,ValueError,TypeError) as error:bad('invalid structural obligation',str(error))
        rows.append({'case':cid,'turns':len(case.get('steps') or [case]) if '성질' not in case else 0,
                     'required_information_leaves':len(need),'mapped_leaves':len(set(need)&covered),
                     'complete_specimens':len(specs),'failures':len(failures)-before})
    report={'scope':'case_by_case_static_schema_representation','component_execution':False,
            'correct_answer_selection_checked':False,'cases':len(cases),'cases_with_witnesses':len(set(cases)&set(paths)),
            'case_turns':sum(r['turns'] for r in rows),'required_information_leaves':leaf_count,
            'complete_specimens':specimen_count,'requirement_kinds':dict(kinds),'rows':rows,'failures':failures}
    target=ROOT/'generated/case_representation_report.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    overview=['# 케이스별 표현 가능성 검사', '',
              '정형 요구값은 계약 필드와 완전한 정적 예시에 연결한다. 컴포넌트를 실행하거나 입력의 정답을 결정하지 않는다.', '',
              '내용·상태 전이 요구는 정보를 담을 계약을 확인하며, 실제 의미 준수·전이 동작은 판정하지 않는다.', '',
              '| 케이스 | 턴 | 정보 항목 | 연결 항목 | 완전한 예시 | 오류 | 근거 |',
              '|---|---:|---:|---:|---:|---:|---|']
    for row in rows:
        cid=row['case']
        overview.append(f"| {cid} | {row['turns']} | {row['required_information_leaves']} | {row['mapped_leaves']} | {row['complete_specimens']} | {row['failures']} | [필드·예시 연결](../work/testcases/case_shapes/{cid}.json) |")
    (ROOT/'generated/case_representation_report.md').write_text('\n'.join(overview)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='rows' and k!='failures'},ensure_ascii=False))
    print('failures',len(failures))
    for failure in failures[:20]:print(json.dumps(failure,ensure_ascii=False)[:500])
    return report


if __name__=='__main__':raise SystemExit(bool(check()['failures']))
