<script>
  import { getContext } from 'svelte';
  import data, { contractOwner, proposed } from '../lib/data.js';
  import SchemaPanel from './SchemaPanel.svelte';
  const explorer = getContext('explorer');
  const names = $derived(Object.keys(data.definitions).filter(n => (explorer.typeScope === 'all' || contractOwner[n]) && `${n} ${data.definitions[n].title || ''} ${contractOwner[n]?.title || ''}`.toLowerCase().includes(explorer.query.toLowerCase())).sort());
</script>
<div class="explorer-layout">
  <aside class="catalog panel"><div class="catalog-top"><h2>계약 탐색</h2><label class="search-label">이름·역할 검색<input placeholder="ValueMetadata, 근거, LoRA…" bind:value={explorer.query}/></label><div class="segmented"><button class:active={explorer.typeScope === 'boundary'} onclick={() => explorer.typeScope = 'boundary'}>경계 계약</button><button class:active={explorer.typeScope === 'all'} onclick={() => explorer.typeScope = 'all'}>전체 타입</button></div><small>{names.length}개 표시</small></div><div class="catalog-list">{#each names as name}<button class:selected={explorer.type === name} onclick={() => { explorer.type = name; explorer.sync(); }}><span>{name}</span><small>{contractOwner[name]?.title || data.definitions[name].title || '공통 타입'}{proposed(name) ? ' · 초안' : ''}</small></button>{/each}{#if !names.length}<p class="empty">검색 결과가 없습니다.</p>{/if}</div></aside>
  <section class="panel detail-panel"><SchemaPanel name={explorer.type}/></section>
</div>
