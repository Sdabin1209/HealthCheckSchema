<script>
  import { getContext } from 'svelte';
  import data from '../lib/data.js';
  import SchemaNode from './SchemaNode.svelte';
  let { node, name = '', required = false, depth = 0 } = $props();
  const explorer = getContext('explorer');
  let open = $state(null);
  const expanded = $derived(open ?? depth < 1);
  const ref = $derived(node.$ref?.split('/').at(-1));
  const children = $derived(Object.entries(node.properties || {}));
  const groups = $derived(['oneOf', 'anyOf', 'allOf', 'if', 'then', 'else'].filter(k => node[k]));
  const hasChildren = $derived(children.length || node.items || groups.length);
  const kind = $derived(ref || (Array.isArray(node.type) ? node.type.join(' | ') : node.type) || (groups.length ? '조건·분기' : 'schema'));
  const limits = $derived(Object.entries(node).filter(([k]) => ['minimum', 'maximum', 'minLength', 'maxLength', 'minItems', 'maxItems', 'pattern', 'format', 'additionalProperties', 'uniqueItems'].includes(k)));
</script>
<div class="schema-node" class:nested={depth > 0}>
  <div class="schema-line">
    {#if hasChildren}<button class="disclosure" aria-expanded={!!expanded} aria-label={`${name || '구조'} ${expanded ? '접기' : '펼치기'}`} onclick={() => open = !expanded}>{expanded ? '−' : '+'}</button>{:else}<span class="disclosure placeholder">·</span>{/if}
    <code class="field-name">{name || '전체 구조'}</code>
    {#if required}<span class="tag required">필수</span>{:else if depth > 0 && !name.startsWith('[')}<span class="tag">선택</span>{/if}
    {#if ref}<button class="type-link" onclick={() => explorer.go('contracts', ref)}>{ref} ↗</button>{:else}<span class="type-name">{kind}</span>{/if}
    {#if node.title}<span class="field-title">{node.title}</span>{/if}
  </div>
  {#if node.description}<p class="field-description">{node.description}</p>{/if}
  {#if node['x-why']}<details class="rationale"><summary>필요한 이유</summary><p>{node['x-why']}</p>{#each node['x-cases'] || [] as id}<button class="case-link" onclick={() => explorer.go('cases', id)}>{id}</button>{/each}</details>{/if}
  {#if node.enum || Object.hasOwn(node, 'const')}<div class="enum-list">{#each node.enum || [node.const] as value}<code class="enum">{JSON.stringify(value)}</code>{/each}</div>{/if}
  {#if limits.length}<div class="limits">{#each limits as [key, value]}<span>{key}: <code>{JSON.stringify(value)}</code></span>{/each}</div>{/if}
  {#if expanded && depth < 16}
    {#each children as [key, child]}<SchemaNode node={child} name={key} required={(node.required || []).includes(key)} depth={depth + 1}/>{/each}
    {#if node.items}<SchemaNode node={node.items} name="[배열 항목]" depth={depth + 1}/>{/if}
    {#each groups as group}{#each Array.isArray(node[group]) ? node[group] : [node[group]] as branch, i}<SchemaNode node={branch} name={`[${group}${Array.isArray(node[group]) ? ': ' + (i + 1) : ''}]`} depth={depth + 1}/>{/each}{/each}
  {/if}
  {#if ref && !data.definitions[ref]}<p>참조를 찾을 수 없습니다.</p>{/if}
</div>
