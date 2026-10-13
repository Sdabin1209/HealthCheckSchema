<script>
  import { getContext } from 'svelte';
  import data, { componentById, contractLabels, proposed } from '../lib/data.js';
  import { boxes, canvas, routePoints, pathD, placeLabels, connectionKind } from '../lib/map-layout.js';
  import JsonBlock from './JsonBlock.svelte';
  const explorer = getContext('explorer');
  let direction = $state('both');
  const visibleEdges = data.edges.filter(e => e.from && e.to && e.from !== e.to && !proposed(e.source) && !proposed(e.target));
  const geometry = Object.fromEntries(visibleEdges.map(e => { const points = routePoints(e); return [e.id, { d: pathD(points), points }]; }));
  const current = $derived(componentById[explorer.component]);
  const incoming = $derived(visibleEdges.filter(e => e.to === explorer.component));
  const outgoing = $derived(visibleEdges.filter(e => e.from === explorer.component));
  const related = $derived((direction === 'input' ? incoming : direction === 'output' ? outgoing : [...incoming, ...outgoing]));
  const arrowGroups = $derived.by(() => {
    const groups = new Map();
    for (const edge of visibleEdges) { const key=[edge.from,edge.to,connectionKind(edge)].join('|'); if(!groups.has(key))groups.set(key,[]);groups.get(key).push(edge); }
    return [...groups.values()];
  });
  const labels = $derived(placeLabels(visibleEdges, geometry));
  const selectedEdge = $derived(data.edges.find(e => e.id === explorer.edge));
  function select(id) { explorer.component = explorer.component === id ? '' : id; explorer.edge = ''; explorer.sync(); }
  function chooseEdge(id) { explorer.edge = id; }
  function clearSelection() { explorer.component = ''; explorer.edge = ''; direction = 'both'; explorer.sync(); }
  function dim(group) { return explorer.edge ? !group.some(e => e.id === explorer.edge) : explorer.component ? !group.some(e => related.some(r => r.id === e.id)) : false; }
  const edgeClass = e => e.kind === 'write' ? 'write' : e.from === explorer.component ? 'outgoing' : 'incoming';
</script>
<div class="map-layout">
  <section class="panel map-panel"><div class="map-caption"><div><div class="eyebrow">PROCESS · CONTROL · STORAGE</div><h2>어디서 받아, 무엇을 넘기는가</h2></div><span class="tag">12개 컴포넌트</span></div><p class="muted">위쪽은 문항 정의, 아래쪽은 기록 저장소이며 LangGraph가 처리 컴포넌트의 왼쪽에서 흐름을 연결합니다.</p>
  <div class="map-controls segmented" aria-label="지도 연결 방향">{#each [['both','입력 + 출력'],['input','입력만'],['output','출력만']] as [value,label]}<button disabled={!current} class:active={direction === value} aria-pressed={direction === value} onclick={() => { direction = value; explorer.edge = ''; }}>{label}</button>{/each}<button onclick={clearSelection}>선택 해제</button></div>
  <div class="map-scroll"><svg viewBox={`0 0 ${canvas.width} ${canvas.height}`} role="img" aria-label="처리 흐름·제어·저장소·외부 접점을 구분한 데이터 계약 지도">
    <defs>{#each ['incoming','outgoing','write','main'] as kind}<marker id={`arrow-${kind}`} class={`marker-${kind}`} markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z"/></marker>{/each}</defs>
    {#each data.components as c}{@const b = boxes[c.id]}<foreignObject x={b.x} y={b.y} width={b.w} height={b.h}><button xmlns="http://www.w3.org/1999/xhtml" class="map-node" class:selected={explorer.component === c.id} class:model={c.kind === '모델'} class:store={c.kind === '저장소'} onclick={() => select(c.id)}><span class="node-kind">{b.stage ? b.stage + ' · ' : ''}{c.kind}</span><strong>{c.title}</strong><small>{c.name}</small></button></foreignObject>{/each}
    <g class="active-connections">{#each arrowGroups as group,i}{@const edge = group.find(e => e.id === explorer.edge) || group[0]}{@const g = geometry[edge.id]}{@const kind = edgeClass(edge)}<g class={`map-edge ${kind}`} class:selected={explorer.edge === edge.id} class:dim={dim(group)} role="button" tabindex="0" aria-label={`${edge.source}에서 ${edge.target}로 ${edge.kind === 'write' ? '쓰기 자료 전달' : '데이터 전달'}`} onclick={() => chooseEdge(edge.id)} onkeydown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); chooseEdge(edge.id); } }}><path d={g.d} class="edge-hit"/><path d={g.d} class="edge-line" marker-end={`url(#arrow-${kind})`}/><circle cx={labels[edge.id][0]} cy={labels[edge.id][1]} r="11" class="edge-number-bg"/><text x={labels[edge.id][0]} y={labels[edge.id][1]} class="edge-number">{i+1}</text><title>{group.map(e => e.source + ' → ' + e.target).join(' / ')}</title></g>{/each}</g>
  </svg></div><div class="map-legend"><span><i class="legend-dot incoming"></i>입력</span><span><i class="legend-dot outgoing"></i>출력 소비</span><span><i class="legend-dot store"></i>저장 쓰기 자료</span><span>선택 시 나머지 연결은 흐리게 표시</span></div>
  </section>
  <section class="panel map-detail">{#if current}<div class="eyebrow">{current.kind}</div><h2>{current.title}</h2><p class="lead">{current.responsibility}</p><div class="why-box"><h3>이 역할이 필요한 이유</h3><p>{current.why}</p></div><h3>계약</h3><div class="contract-buttons">{#each Object.entries(current.contracts) as [role,name]}<button onclick={() => explorer.go('contracts', name)}><span class="muted">{contractLabels[role] || role}</span><strong>{name} ↗</strong>{#if current.contract_status?.[role] === 'proposal'}<span class="tag proposal">초안</span>{/if}</button>{/each}</div>
  {#each [['input','받는 데이터',incoming],['output','내보내는 데이터',outgoing]] as [dir,title,edges]}<h3>{title} <span class="count">{edges.length}</span></h3><div class="connection-list" data-direction={dir}>{#each edges as edge}<button class:selected={explorer.edge === edge.id} onclick={() => { direction = 'both'; chooseEdge(edge.id); }}><small>{#if related.some(e => e.id === edge.id)}<b>{arrowGroups.findIndex(group => group.some(e => e.id === edge.id))+1} · </b>{/if}{componentById[edge.from].title} → {componentById[edge.to].title}{edge.kind === 'write' ? ' · 저장 쓰기 자료' : ''}</small><span>{edge.source} → {edge.target}</span><small>{edge.fields.length}개 전달 필드</small></button>{/each}{#if !edges.length}<p class="muted">현재 원본에 선언된 {dir === 'input' ? '입력 출처' : '출력 소비·저장 목적'} 연결이 없습니다.</p>{/if}</div>{/each}
  {:else}<div class="eyebrow">전체 연결</div><h2>컴포넌트나 화살표를 선택하세요</h2><p class="muted">전체 입력·출력 연결이 표시됩니다. 선택하면 관련 연결만 강조되며, 선택 해제로 전체 보기로 돌아갑니다.</p>{/if}</section>
</div>
{#if selectedEdge}<section class="panel relation-panel"><div class="panel-heading"><div><div class="eyebrow">원본: work/contracts/{selectedEdge.kind === 'write' ? 'output_bindings.yaml' : 'bindings.yaml'}</div><h2>{selectedEdge.source} → {selectedEdge.target}</h2></div><button onclick={() => explorer.edge = ''}>닫기 ×</button></div><p class="muted">{selectedEdge.kind === 'write' ? '저장 상태에 반영할 자료의 전달 목적입니다. 실제 저장 효과를 실행하거나 값의 직접 복사를 주장하지 않습니다.' : '원천 출력·상태와 이를 소비하는 입력의 연결입니다. 실제 호출 성공을 나타내지 않습니다.'}</p><div class="relation-table"><table><thead><tr><th>보내는 필드</th><th>받는 필드·시점</th><th>전달 방식과 설명</th></tr></thead><tbody>{#each selectedEdge.fields as info}<tr><td><button class="type-link" onclick={() => explorer.go('contracts', selectedEdge.source)}>{info.source.field_path || '(계약 전체)'}</button></td><td><button class="type-link" onclick={() => explorer.go('contracts', selectedEdge.target)}>{info.field}</button><small>{info.snapshot}</small></td><td><span class="tag">{info.transfer?.mode || '선언된 출처'}</span><p>{info.transfer?.description || info.assembly}</p>{#if info.evidence}<small>근거: {info.evidence}</small>{/if}</td></tr>{/each}</tbody></table></div>
  {#each data.handoffs.filter(e => e.source_contract === selectedEdge.source && e.target_contract === selectedEdge.target) as example}<details><summary>정적 전달 예시 · {example.target_field}</summary><div class="handoff-pair"><JsonBlock value={example.source} label={example.source_contract + ' · 원천 값'} filename={example.id + '-source.json'}/><JsonBlock value={example.target} label={example.target_contract + ' · 목적 값'} filename={example.id + '-target.json'}/></div></details>{/each}
</section>{/if}
