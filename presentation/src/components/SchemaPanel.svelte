<script>
  import data, { proposed, standalone, download, contractOwner } from '../lib/data.js';
  import SchemaNode from './SchemaNode.svelte';
  import JsonBlock from './JsonBlock.svelte';
  let { name } = $props();
  let raw = $state(false);
  const entry = $derived(data.entries[name]);
  const node = $derived(data.definitions[name]);
</script>
{#if node}
  <div class="panel-heading"><div><div class="eyebrow">{contractOwner[name]?.title || '공통 타입'}</div><h2>{name}</h2></div><span class:proposal={proposed(name)} class="status">{proposed(name) ? '저장 API 초안' : '현행 정의'}</span></div>
  {#if proposed(name)}<p class="notice">데이터 계약 초안입니다. 실제 저장 API로 채택되었다는 뜻은 아닙니다.</p>{/if}
  <div class="actions"><button class:active={raw} onclick={() => raw = !raw}>{raw ? '필드 설명 보기' : '원본 구조 보기'}</button><button onclick={() => download(name + '.json', standalone(name))}>참조 포함 Schema 저장 ↓</button></div>
  <div class="source-path"><span>구조 원본</span><code>work/contracts/{entry.schema}</code><span>의미·근거 원본</span><code>work/contracts/{entry.semantics}</code></div>
  {#if raw}<JsonBlock value={standalone(name)} filename={name + '.json'} label="JSON Schema · Draft 2020-12"/>{:else}{#key name}<SchemaNode {node}/>{/key}{/if}
{/if}
