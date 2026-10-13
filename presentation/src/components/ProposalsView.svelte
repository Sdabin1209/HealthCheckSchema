<script>
  import { getContext } from 'svelte';
  import data from '../lib/data.js';
  import JsonBlock from './JsonBlock.svelte';
  const explorer = getContext('explorer');
</script>
<section class="panel detail-panel"><div class="eyebrow">ADDITIONAL DATA CONTRACTS</div><h2>추가 계약 제안</h2><p class="lead">현행 스키마와 별도로 제안된 자료형입니다. 현행 계약이 미완성이라는 뜻은 아닙니다.</p><div class="source-path"><span>원본</span><code>work/contracts/proposals.yaml</code></div><div class="pending-grid">{#each data.proposals as item}<article class="pending-card"><div class="eyebrow">추가 자료형 · 제안</div><h3>{item.title}</h3><p>{item.purpose}</p><p class="muted">{item.scope}</p><div class="contract-buttons">{#each item.contracts as name}<button onclick={() => explorer.go('contracts', name)}>{name} ↗</button>{/each}</div></article>{/each}</div><div class="scope-note"><h3>테스트 데이터와 스키마</h3><p>문항·선택지·단위 목록은 계약으로 표현할 데이터입니다. 테스트 문항 수나 특정 코드 목록은 스키마의 완성 조건이 아닙니다. 동일한 자료형의 데이터가 늘어나도 Schema를 바꾸지 않습니다.</p></div><details><summary>생성 시점의 정적 검사 보고서</summary><JsonBlock value={data.reports} filename="static-reports.json" label="원본 보고서 요약"/></details></section>
