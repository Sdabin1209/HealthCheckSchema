"""Check output-local metadata relations in authored fixtures; no business judgment."""
from pathlib import Path
import json,sys
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import spec_sources as S

def integrity_errors(contract,payload,defs):
    errors=[]
    def visit(node,value,name,path):
        if '$ref' in node:
            target=node['$ref'].split('/')[-1]
            visit(defs[target],value,target,path);return
        if node is defs.get(name):
            if name in ('TextSpan','Evidence') and isinstance(value,dict):
                start=value.get('start');end=value.get('end');text=value.get('text');unit=value.get('offset_unit')
                if isinstance(start,int) and isinstance(end,int) and isinstance(text,str):
                    length=len(text.encode('utf8')) if unit=='utf8_byte' else len(text.encode('utf-16-le'))//2 if unit=='utf16_code_unit' else len(text)
                    if end<start or end-start!=length:errors.append(path+': span boundaries and encoded text length disagree')
            if name=='QuestionBank' and isinstance(value,dict):
                ids=[q['question_id'] for q in value['questions']]
                if len(ids)!=len(set(ids)):errors.append(path+': duplicate question_id in question bank')
            if name=='QuestionDef' and isinstance(value,dict):
                ids=[slot['slot_id'] for slot in value['slots']]
                if len(ids)!=len(set(ids)):errors.append(path+': duplicate slot_id within question')
            if name=='SessionStore' and isinstance(value,dict):
                keys=[(r['slot']['question_id'],r['slot']['repeat_key'],r['slot']['slot_id']) for r in value['answer_records']]
                if len(keys)!=len(set(keys)):errors.append(path+': duplicate answer record compound slot key')
            if name=='SlotDef' and isinstance(value,dict) and 'choice_catalog' in value:
                codes=[r['code'] for r in value['choice_catalog']]
                if len(codes)!=len(set(codes)):errors.append(path+': duplicate choice code')
                if value.get('yes_no_map') and not set(value['yes_no_map'].values())<=set(codes):errors.append(path+': yes_no_map refers to an unknown choice code')
            if name=='ItemCheck' and isinstance(value,dict):
                if any(d['category'] not in value['problems'] for d in value.get('problem_details',[])):errors.append(path+': detailed problem category is absent from problems')
            if name=='SessionLoadResult' and isinstance(value,dict) and value.get('status')=='OK':
                state=value.get('state')
                if isinstance(state,dict) and 'revision' in state and state['revision']!=value['revision']:errors.append(path+': state revision differs from load result revision')
        if isinstance(value,dict):
            for key,child in node.get('properties',{}).items():
                if key in value:visit(child,value[key],name,path+'/'+key)
        if isinstance(value,list) and 'items' in node:
            for i,item in enumerate(value):visit(node['items'],item,name,path+'/'+str(i))
        for op in ('oneOf','anyOf'):
            for branch in node.get(op,[]):
                if Draft202012Validator({**branch,'$defs':defs}).is_valid(value):visit(branch,value,name,path)
    visit(defs[contract],payload,contract,'')
    return errors

def check():
    defs=S.definitions();failures=[];samples=[]
    for p in (S.WORK/'testcases/schema_examples').glob('*.json'):
        e=json.loads(p.read_text())
        if e['valid']:samples.append((e['id'],e['contract'],e['input']))
    for p in (S.WORK/'testcases/case_shapes').glob('*.json'):
        w=json.loads(p.read_text())
        for s in w['specimens']:samples.append((w['case']+'/'+s['id'],s['contract'],s['data']))
    cached={}
    validators={n:Draft202012Validator({**d,'$defs':defs}) for n,d in defs.items()}
    for id,name,data in samples:
        key=(name,json.dumps(data,ensure_ascii=False,sort_keys=True))
        if key not in cached:
            cached[key]=integrity_errors(name,data,defs) if validators[name].is_valid(data) else ['schema-invalid specimen']
        errors=cached[key]
        if errors:failures.append({'id':id,'errors':errors})
    result={'scope':'static_output_local_information_integrity','component_execution':False,'specimens':len(samples),'unique_payloads':len(cached),'failures':failures}
    (ROOT/'generated/information_integrity_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False));return result
if __name__=='__main__':raise SystemExit(bool(check()['failures']))
