"""Validate declared values and static examples; never execute components."""
from pathlib import Path
import json
import sys
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import spec_sources as S


def schema_field(defs,contract,path):
    def dereference(node):
        while '$ref' in node:node=defs[node['$ref'].split('/')[-1]]
        return node
    def visit(node,tokens):
        node=dereference(node)
        if not tokens:return node
        token=tokens[0];name=token.removesuffix('[]')
        if name in node.get('properties',{}):
            child=node['properties'][name]
            if token.endswith('[]'):child=dereference(child)['items']
            return visit(child,tokens[1:])
        branches=[]
        for op in ('oneOf','anyOf','allOf'):
            for branch in node.get(op,[]):
                try:branches.append(visit(branch,tokens))
                except KeyError:pass
        if not branches:raise KeyError(path)
        return branches[0] if len(branches)==1 else {'anyOf':branches}
    return visit(defs[contract],path.split('.') if path else [])


def check():
    defs=S.definitions();failures=[];rows=[]
    cases={c['id']:c for c in S.cases()['cases']}
    notation=S.read_yaml(S.WORK/'contracts/case_notation.yaml')
    vocab=notation['vocabularies'];field_encodings=notation.get('field_encodings',{})
    entries=S.read_yaml(S.WORK/'testcases/value_requirements.yaml')['requirements']
    for entry in entries:
        try:
            case=cases[entry['case']];steps=case.get('steps') or [case]
            if entry['turn']<1:raise ValueError('invalid turn')
            declared=S.at_pointer(steps[entry['turn']-1]['expect'],entry['expect_pointer'])
            encoding=field_encodings.get(entry['contract'],{}).get(entry['field_path'],{})
            encoded=encoding.get(declared,vocab.get(entry['vocabulary'],{}).get(declared,declared))
            if declared!=entry['declared_value'] or encoded!=entry['value']:
                raise ValueError('declared requirement changed; update representation example')
            field=schema_field(defs,entry['contract'],entry['field_path'])
            validator=Draft202012Validator({**field,'$defs':defs})
            errors=[e.message for e in validator.iter_errors(entry['value'])]
            if errors:failures.append({'id':entry['id'],'errors':errors})
            rows.append({'id':entry['id'],'kind':'declared_value','representable':not errors})
        except (KeyError,IndexError,ValueError,TypeError) as error:
            failures.append({'id':entry['id'],'errors':[str(error)]})
    examples=[json.loads(p.read_text()) for p in sorted((S.WORK/'testcases/schema_examples').glob('*.json'))]
    examples+=S.read_yaml(S.WORK/'testcases/contract_cases.yaml')['cases']
    validators={name:Draft202012Validator({**node,'$defs':defs}) for name,node in defs.items()}
    positives=set()
    for example in examples:
        valid=validators[example['contract']].is_valid(example['input'])
        matches=valid==example['valid']
        if not matches:failures.append({'id':example['id'],'errors':['schema acceptance differs from declared valid/invalid shape']})
        if example['valid'] and matches:positives.add(example['contract'])
        rows.append({'id':example['id'],'kind':'structural_example','accepted':valid,'expected_valid':example['valid'],'matches':matches})
    boundaries={n for c in S.components() for n in c['contracts'].values()}
    missing=sorted(boundaries-positives)
    if missing:failures.append({'id':'boundary-coverage','errors':missing})
    report={'scope':'schema_representation_only','component_execution':False,'correct_answer_selection_checked':False,
            'proposed_boundary_contracts':sum(v=='proposal' for c in S.components() for v in c.get('contract_status',{}).values()),'required_values':len(entries),'structural_examples':len(examples),'boundary_contracts':len(boundaries),
            'boundaries_with_valid_examples':len(boundaries & positives),'rows':rows,'failures':failures}
    target=ROOT/'generated/representation_report.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='rows'},ensure_ascii=False))
    return report


if __name__=='__main__':raise SystemExit(bool(check()['failures']))
