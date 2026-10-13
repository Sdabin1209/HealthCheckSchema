import data from './generated-data.json' with { type: 'json' };

export default data;
export const contractLabels = { input: '입력', output: '출력', state: '저장 상태', trace: '턴 기록', load_request: '조회 요청', load_result: '조회 결과', commit_request: '저장 요청', commit_result: '저장 결과' };
export const roleLabels = { input: '입력', output: '출력', representation: '표현 예시', configuration: '설정', initial_state: '턴 시작 상태', processing_state: '처리 시점 상태', final_state: '작성된 최종 상태' };
export const componentById = Object.fromEntries(data.components.map(c => [c.id, c]));
export const contractOwner = Object.fromEntries(data.components.flatMap(c => Object.values(c.contracts).map(n => [n, c])));
export const proposed = name => data.entries[name]?.status === 'proposal';
export const json = value => JSON.stringify(value, null, 2);
export const caseTitle = c => c.requirement['설명'] || c.requirement.name || c.requirement.title || c.requirement.description || c.id;
export function download(name, value) {
  const url = URL.createObjectURL(new Blob([json(value)], { type: 'application/json;charset=utf-8' }));
  const a = document.createElement('a'); a.href = url; a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export function standalone(name) {
  const found = new Set();
  function scan(n) {
    if (!n || typeof n !== 'object') return;
    if (n.$ref) {
      const ref = n.$ref.split('/').at(-1);
      if (!found.has(ref)) { found.add(ref); scan(data.definitions[ref]); }
    }
    Object.values(n).forEach(scan);
  }
  found.add(name); scan(data.definitions[name]);
  return { $schema: 'https://json-schema.org/draft/2020-12/schema', $ref: `#/$defs/${name}`, $defs: Object.fromEntries([...found].sort().map(n => [n, data.definitions[n]])) };
}
