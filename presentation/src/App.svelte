<script>
  import { setContext, onMount } from 'svelte';
  import data from './lib/data.js';
  import { Explorer } from './lib/explorer.svelte.js';
  import StructureMap from './components/StructureMap.svelte';
  import ContractExplorer from './components/ContractExplorer.svelte';
  import CaseExplorer from './components/CaseExplorer.svelte';
  import ProposalsView from './components/ProposalsView.svelte';
  const explorer = new Explorer();
  const buildCommit = import.meta.env.VITE_BUILD_COMMIT || '';
  setContext('explorer', explorer);
  const tabs = [{id: 'map', label: '구조 지도', number: '01'}, {id: 'contracts', label: '계약·타입', number: '02'}, {id: 'cases', label: '정적 예시', number: '03'}, {id: 'proposals', label: '계약 제안', number: '04'}];
  const boundaries = new Set(data.components.flatMap(c => Object.values(c.contracts)));
  const proposals = Object.values(data.entries).filter(e => e.status === 'proposal').length;
  onMount(() => {
    explorer.restore();
    const listener = () => explorer.restore();
    window.addEventListener('hashchange', listener);
    window.addEventListener('popstate', listener);
    return () => { window.removeEventListener('hashchange', listener); window.removeEventListener('popstate', listener); };
  });
  $effect(() => { document.documentElement.dataset.theme = explorer.dark ? 'dark' : 'light'; });
</script>
<header class="site-header"><a class="brand" href="#view=map" onclick={() => explorer.go('map')}><span class="brand-mark">HC</span><span>HEALTH CHECK <small>DATA CONTRACTS</small></span></a><div class="header-right"><span class="version">계약 v{data.version}</span><button class="theme-button" aria-label={explorer.dark ? '밝은 화면으로 변경' : '어두운 화면으로 변경'} onclick={() => explorer.dark = !explorer.dark}>{explorer.dark ? '☀ 밝게' : '◐ 어둡게'}</button></div></header>
<main><section class="intro"><div><div class="eyebrow">SCHEMA EXPLORER</div><h1>문진 데이터가<br/><span>지나가는 길을 봅니다.</span></h1><p>컴포넌트의 역할부터 필드 하나의 근거까지.<br/>현재 계약 원본과 정적 예시를 함께 탐색합니다.</p></div><div class="stats"><div><strong>{data.components.length}</strong><span>컴포넌트</span></div><div><strong>{boundaries.size - proposals}<small> + {proposals}</small></strong><span>현행 경계 + 저장 API 초안</span></div><div><strong>{Object.keys(data.definitions).length}</strong><span>전체 정의</span></div><div><strong>{data.cases.length}</strong><span>요구사항 케이스</span></div></div></section>
<nav class="main-tabs" aria-label="탐색 화면">{#each tabs as tab}<button aria-current={explorer.tab === tab.id ? 'page' : undefined} class:active={explorer.tab === tab.id} onclick={() => explorer.go(tab.id)}><small>{tab.number}</small>{tab.label}</button>{/each}</nav>
{#if explorer.tab === 'map'}<StructureMap/>{:else if explorer.tab === 'contracts'}<ContractExplorer/>{:else if explorer.tab === 'cases'}<CaseExplorer/>{:else}<ProposalsView/>{/if}
<footer><span>계약 v{data.version} · 작성된 예시를 탐색하는 정적 웹</span><details><summary>원본 식별 정보</summary><code>{data.sourceDigest}</code>{#if buildCommit}<p>빌드 기준 커밋: <code>{buildCommit}</code></p>{/if}<p>work/contracts/ · work/testcases/에서 생성. 구조·설명·예시는 각 원본 파일에서 수정합니다.</p></details></footer></main>
