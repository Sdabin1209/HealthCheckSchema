"""Validate authored transfer examples, never execute an adapter or selection policy."""
from pathlib import Path
import json,sys
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import spec_sources as S

def non_null(node):
    for key in ('anyOf','oneOf'):
        if key in node:
            branches=[b for b in node[key] if b.get('type')!='null']
            if len(branches)==1:return non_null(branches[0])
    return node


def named_shape(node):
    node=non_null(node)
    if '$ref' in node:return node['$ref'].split('/')[-1]
    if node.get('type')=='array':return 'array<'+named_shape(node['items'])+'>'
    return None


def output_binding_errors(binding,defs):
    try:
        source=non_null(S.field_schema(binding['source_contract'],binding['source_field'],defs))
        target=non_null(S.field_schema(binding['target_contract'],binding['target_field'],defs))
        mode=binding['mode']
        if mode=='append_record':
            if target.get('type')!='array' or source!=non_null(target['items']):raise ValueError('append payload differs from target array item type')
        elif mode=='create_record':
            if source!=target:raise ValueError('create payload differs from target record type')
        elif mode=='write_update':
            if source!=target and (named_shape(source),named_shape(target))!=('ProgressRecordUpdate','ProgressRecord'):raise ValueError('undeclared update payload/state relation')
        elif mode=='write_decisions':
            if (named_shape(source),named_shape(target))!=('array<StoreDecision>','array<SlotRecord>'):raise ValueError('undeclared decision payload/state relation')
        else:raise ValueError('unknown output transfer mode')
    except (KeyError,TypeError,ValueError) as error:return [str(error)]
    return []


def check():
    defs=S.definitions();bindings=S.read_yaml(S.WORK/'contracts/bindings.yaml')['inputs'];failures=[]
    modes={'copy','project','lookup','join','variant_field','lookup_metadata'}
    count=0
    for name,entry in bindings.items():
        for field,b in entry['fields'].items():
            count+=1;t=b.get('transfer',{})
            if t.get('mode') not in modes or not t.get('description'):failures.append(f'{name}.{field}: missing transfer contract')
    outputs=S.read_yaml(S.WORK/'contracts/output_bindings.yaml')['bindings']
    for b in outputs:
        failures.extend('output binding: '+e for e in output_binding_errors(b,defs))
        try:
            for direction in ('source','target'):
                if b[direction+'_field'] not in defs[b[direction+'_contract']]['properties']:raise ValueError('unknown field')
            evidence,pointer=b['evidence'].split('#',1)
            if not S.at_pointer(S.read_yaml(ROOT/evidence),pointer).get('meaning'):raise ValueError('missing field meaning')
        except Exception as error:failures.append('output binding: '+str(error))
    examples=json.loads((S.WORK/'testcases/handoff_examples.json').read_text())['examples']
    for e in examples:
        try:
            if e['scope']!='static_payload_transfer' or e['component_execution'] is not False:raise ValueError('incorrect scope')
            b=bindings[e['target_contract']]['fields'][e['target_field']]
            if e['source_contract'] not in {s['contract'] for s in b['sources']}:raise ValueError('unbound source')
            for direction in ('source','target'):
                name=e[direction+'_contract'];Draft202012Validator({**defs[name],'$defs':defs}).validate(e[direction])
            for mapping in e['mappings']:
                if not mapping['target_pointer'].startswith('/'+e['target_field']+'/') and mapping['target_pointer']!='/'+e['target_field']:raise ValueError('mapping outside target field')
                a=S.at_pointer(e['source'],mapping['source_pointer']);b=S.at_pointer(e['target'],mapping['target_pointer'])
                if a!=b:raise ValueError('declared payload was not preserved')
        except Exception as error:failures.append(e['id']+': '+str(error)[:200])
    report={'scope':'static_schema_handoffs','component_execution':False,'binding_fields':count,'output_destination_fields':len(outputs),'complete_transfer_examples':len(examples),'failures':failures}
    (ROOT/'generated/handoff_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False));return report
if __name__=='__main__':raise SystemExit(bool(check()['failures']))
