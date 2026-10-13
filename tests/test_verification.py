"""Regression checks for completion identity and static data integrity, not business behavior."""
import copy,json,subprocess,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import spec_sources as S
import verification_state as V
import verify
from work.tools.check_handoffs import output_binding_errors
from work.tools.check_information_integrity import integrity_errors,check as check_integrity

@pytest.fixture
def minimal_root(tmp_path):
    (tmp_path/'work/contracts').mkdir(parents=True);(tmp_path/'work/contracts/manifest.yaml').write_text('version: 1\n')
    (tmp_path/'generated').mkdir();(tmp_path/'generated/example.json').write_text('{}')
    return tmp_path

def test_completion_is_absent_on_late_failure(minimal_root):
    r=minimal_root;V.publish(r,1,V.source_digest(r),V.checker_digest(r))
    def runner(cmd,**kwargs):
        if 'pytest' in cmd:raise subprocess.CalledProcessError(1,cmd)
    with pytest.raises(subprocess.CalledProcessError):verify.run(r,runner)
    assert not (r/'generated'/V.RESULT).exists()

def test_completion_requires_all_stages_and_unchanged_sources(minimal_root):
    r=minimal_root;calls=[]
    def runner(cmd,**kwargs):calls.append(cmd)
    verify.run(r,runner);assert len(calls)==len(verify.STAGES)+1
    assert V.require_valid(r,1)['status']=='passed'
    def change(cmd,**kwargs):
        if 'pytest' in cmd:(r/'work/contracts/new.yaml').write_text('changed: true')
    with pytest.raises(ValueError,match='changed'):verify.run(r,change)
    assert not (r/'generated'/V.RESULT).exists()

@pytest.mark.parametrize('target',['work/contracts/manifest.yaml','generated/example.json','verify.py'])
def test_completion_detects_changes_to_sources_artifacts_or_checker(minimal_root,target):
    r=minimal_root;V.publish(r,1,V.source_digest(r),V.checker_digest(r));(r/target).write_text('modified')
    with pytest.raises(ValueError,match='stale'):V.require_valid(r,1)

def test_correct_output_bindings_pass_and_wrong_log_type_is_rejected():
    defs=S.definitions();bindings=S.read_yaml(S.WORK/'contracts/output_bindings.yaml')['bindings']
    assert all(not output_binding_errors(b,defs) for b in bindings)
    wrong=copy.deepcopy(next(b for b in bindings if b['target_field']=='dispatch_log'))
    wrong.update(source_contract='OrchestratorOutput',source_field='log_entry')
    assert output_binding_errors(wrong,defs)
    wrong=copy.deepcopy(bindings[0]);wrong['mode']='unrecognized'
    assert output_binding_errors(wrong,defs)

@pytest.mark.parametrize('contract,key',[('QuestionBank','questions'),('SessionStore','answer_records')])
def test_duplicate_identity_keys_are_rejected(contract,key):
    data=json.loads((S.WORK/f'testcases/schema_examples/{contract}.json').read_text())['input']
    data=copy.deepcopy(data);data[key].append(copy.deepcopy(data[key][0]))
    assert any('duplicate' in e for e in integrity_errors(contract,data,S.definitions()))

def test_slot_identity_is_local_to_question_and_record_identity_includes_repeat_key():
    defs=S.definitions();bank=json.loads((S.WORK/'testcases/schema_examples/QuestionBank.json').read_text())['input']
    question=copy.deepcopy(bank['questions'][0]);question['slots'].append(copy.deepcopy(question['slots'][0]))
    assert any('duplicate slot_id' in e for e in integrity_errors('QuestionDef',question,defs))
    store=copy.deepcopy(json.loads((S.WORK/'testcases/schema_examples/SessionStore.json').read_text())['input'])
    row=copy.deepcopy(store['answer_records'][0]);row['slot']['repeat_key']='another-row';store['answer_records'].append(row)
    assert not integrity_errors('SessionStore',store,defs)

def test_bad_span_in_non_T_case_is_checked_by_the_batch(tmp_path,monkeypatch):
    from work.tools import check_information_integrity as M
    work=tmp_path/'work';(work/'testcases/case_shapes').mkdir(parents=True);(work/'testcases/schema_examples').mkdir()
    witness=json.loads((S.WORK/'testcases/case_shapes/B1.json').read_text())
    item=next(s for s in witness['specimens'] if s['contract']=='ParserOutput')
    item['data']['items'][0]['evidence']=[{'start':0,'end':1,'text':'두 번','offset_unit':'unicode_code_point'}]
    (work/'testcases/case_shapes/B1.json').write_text(json.dumps(witness))
    (tmp_path/'generated').mkdir();defs=S.definitions()
    monkeypatch.setattr(M,'ROOT',tmp_path);monkeypatch.setattr(S,'WORK',work);monkeypatch.setattr(S,'definitions',lambda:defs)
    report=check_integrity()
    assert any(f['id'].startswith('B1/') and any('span' in e for e in f['errors']) for f in report['failures'])
