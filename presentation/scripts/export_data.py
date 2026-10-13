"""Generate presentation data from authoritative contracts. No business execution."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import spec_sources as S


def export():
    S.require_verification()
    manifest = S.manifest()
    defs = S.definitions(documented=True)
    components = S.components()
    owner = {name: c['id'] for c in components for name in c['contracts'].values()}
    bindings = S.read_yaml(S.WORK / 'contracts/bindings.yaml')['inputs']
    edges = {}
    for target, binding in bindings.items():
        for field, info in binding['fields'].items():
            for source in info.get('sources', []):
                key = (source['contract'], target)
                edge = edges.setdefault(key, {'id': '|'.join(key), 'source': key[0], 'target': target,
                                               'from': owner.get(key[0]), 'to': owner.get(target), 'kind': 'input', 'fields': []})
                edge['fields'].append({'field': field, **info, 'source': source})
    for binding in S.read_yaml(S.WORK / 'contracts/output_bindings.yaml')['bindings']:
        source, target = binding['source_contract'], binding['target_contract']
        key = ('write', source, target)
        edge = edges.setdefault(key, {'id': '|'.join(key), 'source': source, 'target': target,
                                    'from': owner[source], 'to': owner[target], 'kind': 'write', 'fields': []})
        edge['fields'].append({'field': binding['target_field'], 'source': {'contract': source, 'field_path': binding['source_field']},
                               'snapshot': 'write_payload', 'transfer': {'mode': binding['mode'], 'description': binding['description']},
                               'evidence': binding['evidence']})
    values = []
    value_index = {}
    cases = []
    for case in S.cases()['cases']:
        shape = json.loads((S.WORK / 'testcases/case_shapes' / (case['id'] + '.json')).read_text())
        specimens = []
        for specimen in shape['specimens']:
            value = specimen['data']
            raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
            digest = hashlib.sha256(raw.encode()).hexdigest()
            if digest not in value_index:
                value_index[digest] = len(values)
                values.append(value)
            specimens.append({k: v for k, v in specimen.items() if k != 'data'} | {'valueIndex': value_index[digest]})
        cases.append({'id': case['id'], 'requirement': case, 'specimens': specimens,
                      'source': 'work/testcases/case_shapes/' + case['id'] + '.json'})
    report_names = ['case_representation_report', 'handoff_report', 'information_integrity_report']
    reports = {n: {k: v for k, v in json.loads((ROOT / 'generated' / (n + '.json')).read_text()).items() if k != 'rows'} for n in report_names}
    generated_manifest = json.loads((ROOT / 'generated/source_manifest.json').read_text())
    if generated_manifest['source_sha256'] != S.source_digest():
        raise ValueError('Schema sources changed. Run python3 verify.py before building the presentation.')
    # Results are tied to source files, not claimed as execution results.
    payload = {'version': manifest['version'], 'sourceDigest': S.source_digest(),
               'components': components, 'definitions': defs, 'entries': manifest['definitions'],
               'edges': list(edges.values()), 'cases': cases, 'values': values,
               'proposals': S.read_yaml(S.WORK / 'contracts/proposals.yaml')['proposals'],
               'reports': reports,
               'handoffs': json.loads((S.WORK / 'testcases/handoff_examples.json').read_text())['examples']}
    output = ROOT / 'presentation/src/lib/generated-data.json'
    output.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(json.dumps({'version': payload['version'], 'definitions': len(defs), 'cases': len(cases),
                      'specimens': sum(len(c['specimens']) for c in cases), 'data_bytes': output.stat().st_size}))


if __name__ == '__main__':
    export()
