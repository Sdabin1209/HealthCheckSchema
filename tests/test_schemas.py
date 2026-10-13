"""Schema representation and structural rejection checks; no component execution."""
from pathlib import Path
import json
import sys
import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import spec_sources as S

@pytest.fixture(scope='module')
def source_registry():
    return Registry().with_resources((
        (str((S.WORK/'contracts'/entry['schema']).resolve().as_uri()),
         Resource.from_contents(json.loads((S.WORK/'contracts'/entry['schema']).read_text())))
        for entry in S.manifest()['definitions'].values()))

@pytest.fixture
def parser_validator(source_registry):
    uri=(S.WORK/'contracts/components/utterance_parser/output.schema.json').resolve().as_uri()
    return Draft202012Validator({'$ref':uri},registry=source_registry)

@pytest.fixture
def parser_item():
    return {'item_no':0,'target':{'question_id':'Q3b','repeat_key':'','slot_id':'1회양'},
            'value':'한 병','source_text':'한 병','intent':'ANSWERED_INTENT','progress_op':None,'guide_id':None}

def test_native_split_schema_resolves_without_markdown(parser_validator,parser_item):
    parser_validator.validate({'items':[parser_item]})

@pytest.mark.parametrize('intent',['UNKNOWN_RECORD','UNKNOWN','모름'])
def test_record_and_judgment_codes_are_not_parser_intents(parser_validator,parser_item,intent):
    parser_item['intent']=intent
    assert list(parser_validator.iter_errors({'items':[parser_item]}))

def test_nested_target_requires_repeat_key(parser_validator,parser_item):
    del parser_item['target']['repeat_key']
    assert list(parser_validator.iter_errors({'items':[parser_item]}))

def test_raw_parser_value_is_not_normalized_value(parser_validator,parser_item):
    parser_item['value']={'amount':1,'unit':'병'}
    assert list(parser_validator.iter_errors({'items':[parser_item]}))

def test_whole_question_and_slot_are_distinct_branches(parser_validator,parser_item):
    parser_item['target']={'question_id':'Q3b','whole_question':True}
    parser_validator.validate({'items':[parser_item]})
    parser_item['target']['slot_id']='1회양'
    assert list(parser_validator.iter_errors({'items':[parser_item]}))

def test_source_schemas_contain_no_behavioral_annotations():
    defs=S.definitions()
    def walk(n):
        if isinstance(n,dict):
            assert not {'title','description','x-why','x-cases'} & set(n)
            for v in n.values():walk(v)
        elif isinstance(n,list):
            for v in n:walk(v)
    walk(defs)

@pytest.mark.parametrize('case',S.read_yaml(S.WORK/'testcases/contract_cases.yaml')['cases'],ids=lambda c:c['id'])
def test_cross_field_relations(source_registry,case):
    entry=S.manifest()['definitions'][case['contract']]
    uri=(S.WORK/'contracts'/entry['schema']).resolve().as_uri()
    validator=Draft202012Validator({'$ref':uri},registry=source_registry)
    assert validator.is_valid(case['input']) == case['valid'], case['why']


@pytest.mark.parametrize('status',['ANSWERED','UNKNOWN'])
def test_schema_accepts_both_representable_judgment_codes(status):
    # The schema cannot choose which code is correct for a user's utterance.
    defs=S.definitions()
    Draft202012Validator({**defs['JudgmentStatus'],'$defs':defs}).validate(status)


@pytest.mark.parametrize('text',['많이 힘드시겠어요.','그건 제가 도와드리기 어렵습니다.'])
def test_schema_checks_response_shape_without_grading_meaning(text):
    defs=S.definitions()
    Draft202012Validator({**defs['GeneratorOutput'],'$defs':defs}).validate(
        {'response_text':text,'is_fallback':False})


@pytest.fixture
def single_case_witness(tmp_path,monkeypatch):
    import importlib.util
    spec=importlib.util.spec_from_file_location('case_shapes',S.WORK/'tools/check_case_shapes.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    case=next(c for c in S.cases()['cases'] if c['id']=='B1')
    witness=json.loads((S.WORK/'testcases/case_shapes/B1.json').read_text())
    directory=tmp_path/'examples';directory.mkdir()
    monkeypatch.setattr(module,'ROOT',tmp_path)
    monkeypatch.setattr(module.S,'cases',lambda:{'cases':[case]})
    return module,case,witness,directory


def test_case_representation_rejects_unmapped_required_information(single_case_witness):
    module,case,witness,directory=single_case_witness
    witness['requirements']=[r for r in witness['requirements'] if r['source_pointer']!='/input/발화']
    (directory/'B1.json').write_text(json.dumps(witness,ensure_ascii=False))
    report=module.check(directory)
    assert any(r['reason']=='unmapped required information' for r in report['failures'])


def test_case_representation_rejects_invalid_complete_shape(single_case_witness):
    module,case,witness,directory=single_case_witness
    sample=next(s for s in witness['specimens'] if s['contract']=='ParserOutput')
    sample['data']['items'][0]['target']=None
    (directory/'B1.json').write_text(json.dumps(witness,ensure_ascii=False))
    report=module.check(directory)
    assert any(r['reason']=='complete specimen violates schema' for r in report['failures'])


def test_case_representation_requires_review_when_requirement_changes(single_case_witness):
    module,case,witness,directory=single_case_witness
    case['input']['발화']='변경된 요구 입력'
    (directory/'B1.json').write_text(json.dumps(witness,ensure_ascii=False))
    report=module.check(directory)
    assert any(r['reason']=='requirement changed; static witness must be reviewed' for r in report['failures'])


def test_case_representation_does_not_replace_required_code_with_another_valid_code(single_case_witness):
    module,case,witness,directory=single_case_witness
    requirement=next(r for r in witness['requirements'] if r['source_pointer']=='/expect/LoRA-A/0/의도')
    sample=next(s for s in witness['specimens'] if s['id']==requirement['specimen'])
    sample['data']['items'][0]['intent']='SAYS_UNKNOWN'
    requirement['encoded_value']='SAYS_UNKNOWN'
    (directory/'B1.json').write_text(json.dumps(witness,ensure_ascii=False))
    report=module.check(directory)
    assert any(r['reason']=='authored encoding does not preserve declared information' for r in report['failures'])


def test_case_representation_rejects_unrelated_schema_pointer(single_case_witness):
    module,case,witness,directory=single_case_witness
    claim=next(r for r in witness['requirements'] if r['source_pointer']=='/input/발화')
    claim['definition']='GeneratorOutput'
    claim['schema_pointer']='/properties/response_text'
    (directory/'B1.json').write_text(json.dumps(witness,ensure_ascii=False))
    report=module.check(directory)
    assert any(r['reason']=='schema reference does not describe payload field' for r in report['failures'])


def test_case_representation_rejects_missing_declared_payload(single_case_witness):
    module,case,witness,directory=single_case_witness
    claim=next(r for r in witness['requirements'] if r['source_pointer']=='/expect/LangGraph/대화로그/LoRA-A출력')
    sample=next(s for s in witness['specimens'] if s['id']==claim['specimen'])
    sample['data']['log_entry']['parser_output']=None
    (directory/'B1.json').write_text(json.dumps(witness,ensure_ascii=False))
    report=module.check(directory)
    assert any(r['reason']=='static specimen does not preserve declared presence' for r in report['failures'])


def test_trace_accepts_complete_model_inputs_and_outputs():
    defs=S.definitions()
    example=json.loads((S.WORK/'testcases/schema_examples/TurnTrace.json').read_text())['input']
    Draft202012Validator({**defs['TurnTrace'],'$defs':defs}).validate(example)
    assert example['parser_input'] is not None and example['generator_input'] is not None


def test_trace_requires_explicit_absent_payload():
    defs=S.definitions();v=Draft202012Validator({**defs['TurnTrace'],'$defs':defs})
    data=json.loads((S.WORK/'testcases/schema_examples/TurnTrace.json').read_text())['input']
    data['generator_input']=None;data['generator_output']=None
    v.validate(data)
    del data['generator_input']
    assert not v.is_valid(data)


def test_trace_uses_nested_input_contract():
    defs=S.definitions();data=json.loads((S.WORK/'testcases/schema_examples/TurnTrace.json').read_text())['input']
    data['parser_input']['utterance']=42
    assert not Draft202012Validator({**defs['TurnTrace'],'$defs':defs}).is_valid(data)


def test_ungrounded_wire_caps_are_not_enforced():
    defs=S.definitions()
    Draft202012Validator({**defs['GeneratorOutput'],'$defs':defs}).validate({'response_text':'가'*3000,'is_fallback':False})
    Draft202012Validator({**defs['Value'],'$defs':defs}).validate({'amount':1000001,'unit':'단위'})
    Draft202012Validator({**defs['QuestionId'],'$defs':defs}).validate('문항 식별자/'+('Q'*100))


def test_structural_lower_bounds_remain():
    defs=S.definitions()
    assert not Draft202012Validator({**defs['QuestionId'],'$defs':defs}).is_valid('')
    unit={'name':'분','synonyms':[],'range':[0,1,2],'convert_to':None}
    assert not Draft202012Validator({**defs['UnitDef'],'$defs':defs}).is_valid(unit)


def test_static_transfer_checker_rejects_lost_payload(tmp_path,monkeypatch):
    import importlib.util
    spec=importlib.util.spec_from_file_location('handoffs',S.WORK/'tools/check_handoffs.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    examples=json.loads((S.WORK/'testcases/handoff_examples.json').read_text())
    row=next(r for r in examples['examples'] if r['id']=='answered-value-projection')
    row['target']['answered_slots'][0]['value']='정보가 바뀐 예시'
    from unittest.mock import patch
    original=module.json.loads
    def changed(content):
        result=original(content)
        return examples if isinstance(result,dict) and 'examples' in result else result
    (tmp_path/'generated').mkdir();monkeypatch.setattr(module,'ROOT',tmp_path)
    with patch.object(module.json,'loads',side_effect=changed):result=module.check()
    assert any('declared payload was not preserved' in failure for failure in result['failures'])


@pytest.mark.parametrize('precision',['exact','approximate','unspecified'])
def test_precision_values_are_representable(precision):
    defs=S.definitions()
    Draft202012Validator({**defs['ValueMetadata'],'$defs':defs}).validate({'precision':precision,'evidence':[]})


@pytest.mark.parametrize('name,field',[('ItemCheck','standard_value'),('Judgment','value_now'),('StoreDecision','value')])
def test_exact_metadata_cannot_describe_an_absent_value(name,field):
    defs=S.definitions()
    source={'ItemCheck':('NormalizerOutput','item_checks'),'Judgment':('JudgeOutput','judgments'),'StoreDecision':('StoreResult','store_decisions')}[name]
    example=json.loads((S.WORK/'testcases/schema_examples'/f'{source[0]}.json').read_text())['input'][source[1]][0]
    example[field]=None;example['value_metadata']={'precision':'exact','evidence':[]}
    assert not Draft202012Validator({**defs[name],'$defs':defs}).is_valid(example)


def information_module():
    import importlib.util
    spec=importlib.util.spec_from_file_location('integrity',S.WORK/'tools/check_information_integrity.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('unit,end,valid',[('unicode_code_point',1,True),('utf16_code_unit',1,False),('utf16_code_unit',2,True)])
def test_span_position_units_are_not_silently_mixed(unit,end,valid):
    span={'start':0,'end':end,'offset_unit':unit,'text':'😀'}
    errors=information_module().integrity_errors('TextSpan',span,S.definitions())
    assert (not errors)==valid


def test_span_missing_endpoint_is_schema_invalid():
    defs=S.definitions()
    assert not Draft202012Validator({**defs['TextSpan'],'$defs':defs}).is_valid({'start':0,'offset_unit':'unicode_code_point','text':'두 병'})


def test_catalog_and_string_choices_are_distinct_branches():
    defs=S.definitions()
    example=next(c for c in S.cases()['cases'] if c['id']=='T3')['expect']['문항정의']['questions'][0]['slots'][0]
    example['choices']=['중복 정의']
    assert not Draft202012Validator({**defs['SlotDef'],'$defs':defs}).is_valid(example)


def test_catalog_detects_duplicate_codes_and_unknown_yes_no_reference():
    import copy
    defs=S.definitions();example=copy.deepcopy(next(c for c in S.cases()['cases'] if c['id']=='T3')['expect']['문항정의']['questions'][0]['slots'][0])
    example['choice_catalog'].append({**example['choice_catalog'][0],'label':'다른 이름'})
    example['yes_no_map']={'yes':'등록되지 않은 코드','no':example['choice_catalog'][0]['code']}
    errors=information_module().integrity_errors('SlotDef',example,defs)
    assert any('duplicate choice code' in e for e in errors)
    assert any('unknown choice code' in e for e in errors)


@pytest.mark.parametrize('status,outcome',[('OK','NOT_APPLIED'),('REVISION_CONFLICT','APPLIED'),('DB_ERROR','APPLIED')])
def test_commit_result_rejects_output_local_contradictions(status,outcome):
    defs=S.definitions();data={'session_id':'S-TEST','status':status,'write_outcome':outcome,'revision':12,'detail':None}
    assert not Draft202012Validator({**defs['SessionCommitResult'],'$defs':defs}).is_valid(data)


def test_commit_result_can_express_unknown_write_outcome():
    defs=S.definitions()
    Draft202012Validator({**defs['SessionCommitResult'],'$defs':defs}).validate({'session_id':'S-TEST','status':'DB_ERROR','write_outcome':'UNKNOWN','revision':None,'detail':None})


def test_history_metadata_is_preserved_as_structured_information():
    defs=S.definitions();entry={'value':{'amount':1,'unit':'병','unit_code':'bottle'},'value_metadata':{'precision':'approximate','evidence':[]}}
    Draft202012Validator({**defs['HistoryEntry'],'$defs':defs}).validate(entry)
    assert entry['value_metadata']['precision']=='approximate'


def test_current_example_version_is_generated_from_explicit_template():
    from work.tools.build import render_current_example
    template=json.loads((S.WORK/'testcases/schema_example_templates/TurnTrace.json').read_text())
    old=json.loads(json.dumps(template))
    for version in (1,7):
        result=render_current_example(template,version)
        assert result['input']['contract_version']==version
        assert result['input']['orchestrator_input']['session_question_bank_version']==old['input']['orchestrator_input']['session_question_bank_version']
    assert template==old


def test_current_generated_trace_example_uses_manifest_version():
    example=json.loads((S.WORK/'testcases/schema_examples/TurnTrace.json').read_text())
    assert example['input']['contract_version']==S.manifest()['version']
    assert example['generation']['generated'] is True
