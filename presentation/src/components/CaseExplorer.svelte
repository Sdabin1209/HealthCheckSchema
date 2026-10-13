<script>
  import { getContext } from 'svelte';
  import data, { roleLabels, caseTitle } from '../lib/data.js';
  import JsonBlock from './JsonBlock.svelte';
  const explorer = getContext('explorer');
  let contractFilter = $state('');
  const cases = $derived(data.cases.filter(c => `${c.id} ${JSON.stringify(c.requirement)}`.toLowerCase().includes(explorer.query.toLowerCase())));
  const current = $derived(data.cases.find(c => c.id === explorer.caseId) || data.cases[0]);
  const specimens = $derived(current.specimens.filter(s => !contractFilter || s.contract === contractFilter));
  const specimen = $derived(specimens.find(s => s.id === explorer.specimen) || specimens[0]);
  const contracts = $derived([...new Set(current.specimens.map(s => s.contract))].sort());
  function selectCase(id) { explorer.caseId = id; explorer.specimen = ''; contractFilter = ''; explorer.sync(); }
</script>
<div class="explorer-layout">
  <aside class="catalog panel"><div class="catalog-top"><h2>정적 예시 <span class="count">{data.cases.length}</span></h2><label class="search-label">케이스·발화·필드 검색<input placeholder="B1, 정정, approximate…" bind:value={explorer.query}/></label><small>{cases.length}개 표시</small></div><div class="catalog-list">{#each cases as c}<button class:selected={current.id === c.id} onclick={() => selectCase(c.id)}><span>{c.id}</span><small>{caseTitle(c)}</small></button>{/each}{#if !cases.length}<p class="empty">검색 결과가 없습니다.</p>{/if}</div></aside>
  <section class="panel detail-panel"><div class="eyebrow">요구사항에서 작성한 JSON</div><h2>{current.id} · {caseTitle(current)}</h2><p class="notice">실제 컴포넌트를 실행한 결과가 아닙니다. 케이스별로 작성된 값의 구조와 표현 위치를 탐색합니다.</p><div class="source-path"><span>예시 원본</span><code>{current.source}</code></div><details class="requirement"><summary>요구사항 보기</summary><JsonBlock value={current.requirement} filename={current.id + '-requirement.json'}/></details>
  <div class="specimen-controls"><label>계약 필터<select value={contractFilter} onchange={e => { contractFilter = e.currentTarget.value; explorer.specimen = ''; }}><option value="">전체 계약</option>{#each contracts as n}<option value={n}>{n}</option>{/each}</select></label><label>턴·시점별 값<select value={specimen?.id || ''} onchange={e => explorer.specimen = e.currentTarget.value}>{#each specimens as s}<option value={s.id}>{s.turn}턴 · {s.contract} · {roleLabels[s.role] || s.role}</option>{/each}</select></label></div>
  {#if specimen}<div class="panel-heading"><div><h3>{specimen.contract}</h3><span class="muted">{specimen.turn}턴 · {roleLabels[specimen.role] || specimen.role}</span></div><button onclick={() => explorer.go('contracts', specimen.contract)}>계약 확인 ↗</button></div><JsonBlock value={data.values[specimen.valueIndex]} filename={current.id + '-' + specimen.id + '.json'} label={specimen.id}/>{:else}<p class="empty">이 계약의 예시가 없습니다.</p>{/if}
  </section>
</div>
