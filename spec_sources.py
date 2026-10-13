"""Read declarative requirements and schemas; no component execution."""
from pathlib import Path
import copy
import hashlib
import json
import yaml

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'
SCHEMA_URI = 'https://json-schema.org/draft/2020-12/schema'

class UniqueKeyLoader(yaml.SafeLoader):
    pass

def _unique_mapping(loader,node,deep=False):
    loader.flatten_mapping(node)
    result={}
    for key_node,value_node in node.value:
        key=loader.construct_object(key_node,deep=deep)
        if key in result:raise ValueError(f'Duplicate YAML key: {key!r} (line {key_node.start_mark.line+1})')
        result[key]=loader.construct_object(value_node,deep=deep)
    return result

UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,_unique_mapping)

def read_yaml(path):
    return yaml.load(Path(path).read_text(encoding='utf-8'),Loader=UniqueKeyLoader)

def manifest():
    return read_yaml(WORK / 'contracts/manifest.yaml')

def components():
    return read_yaml(WORK / 'contracts/components.yaml')['components']

def definitions(documented=False):
    out = {}
    entries = manifest()['definitions']
    by_path = {(WORK / 'contracts' / e['schema']).resolve(): n for n,e in entries.items()}
    for name, entry in entries.items():
        node = json.loads((WORK / 'contracts' / entry['schema']).read_text(encoding='utf-8'))
        node.pop('$schema', None)
        def normalize(n):
            if isinstance(n,dict):
                if '$ref' in n and not n['$ref'].startswith('#/$defs/'):
                    path = (WORK / 'contracts' / entry['schema']).parent / n['$ref']
                    if path.resolve() not in by_path: raise ValueError(f'{name}: unmapped reference {n["$ref"]}')
                    n['$ref'] = '#/$defs/' + by_path[path.resolve()]
                for v in n.values(): normalize(v)
            elif isinstance(n,list):
                for v in n: normalize(v)
        normalize(node)
        if documented:
            for pointer, meta in semantics(name).items():
                target = at_pointer(node, pointer)
                for key, src in (('title', 'title'), ('description', 'meaning'), ('x-why', 'why'), ('x-cases', 'case_refs')):
                    if meta.get(src): target[key] = copy.deepcopy(meta[src])
        out[name] = node
    return out

def at_pointer(node, pointer):
    if pointer and not pointer.startswith('/'):
        raise ValueError(f'Invalid JSON pointer: {pointer}')
    for token in pointer.split('/')[1:]:
        token = token.replace('~1', '/').replace('~0', '~')
        node = node[int(token)] if isinstance(node, list) else node[token]
    return node

def semantics(name):
    entry = manifest()['definitions'][name]
    return read_yaml(WORK / 'contracts' / entry['semantics'])['nodes']

def cases():
    base = WORK / 'testcases'
    result = read_yaml(base / 'metadata.yaml') or {}
    result['문항정의'] = read_yaml(base / 'fixtures/question_bank.yaml')
    result.update(read_yaml(base / 'situations.yaml'))
    result['cases'] = []
    for path in read_yaml(base / 'manifest.yaml')['case_files']:
        result['cases'].extend(read_yaml(base / path)['cases'])
    return result

def rule(name):
    return (WORK / 'rules' / f'{name}.md').read_text(encoding='utf-8')

def refs(node):
    if isinstance(node, dict):
        if '$ref' in node: yield node['$ref']
        for value in node.values(): yield from refs(value)
    elif isinstance(node, list):
        for value in node: yield from refs(value)

def dependencies(name, defs, seen=None):
    seen = set() if seen is None else seen
    if name in seen: return seen
    if name not in defs: raise ValueError(f'Missing definition: {name}')
    seen.add(name)
    for ref in refs(defs[name]):
        if not ref.startswith('#/$defs/'):
            raise ValueError(f'Unsupported named reference: {ref}')
        dependencies(ref[len('#/$defs/'):], defs, seen)
    return seen

def field_schema(name, path, defs):
    node = defs[name]
    for field in path.split('.') if path else []:
        while '$ref' in node: node=defs[node['$ref'].split('/')[-1]]
        node=node['properties'][field]
    return node

def source_digest():
    from verification_state import source_digest as digest
    return digest(ROOT)


def require_verification():
    from verification_state import require_valid
    return require_valid(ROOT,manifest()['version'])
