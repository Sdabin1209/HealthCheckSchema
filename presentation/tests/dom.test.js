import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { Window } from 'happy-dom';
import data from '../src/lib/data.js';

const html = readFileSync(new URL('../dist/index.html', import.meta.url), 'utf8');
const checks = [];

test('compiled single-file application mounts and supports navigation in a DOM emulator', async t => {
  const window = new Window({ url: 'http://localhost/', settings: { enableJavaScriptEvaluation: true } });
  const document = window.document;
  document.write(html);
  const script = document.querySelector('script[type="module"]');
  assert.ok(script, 'inline compiled module must exist');
  window.eval(script.textContent);
  const settle = async () => { await new Promise(r => setTimeout(r, 10)); };
  const button = text => [...document.querySelectorAll('button')].find(e => e.textContent.trim() === text);
  const click = async e => { assert.ok(e, 'target must exist'); e.dispatchEvent(new window.MouseEvent('click', { bubbles: true })); await settle(); };
  const heading = () => document.querySelector('.detail-panel h2')?.textContent;
  const check = async (name, fn) => { await t.test(name, fn); checks.push(name); };
  await settle();
  await check('mounts version and every component without a server', () => {
    assert.equal(document.querySelectorAll('.map-node').length, data.components.length);
    assert.equal(document.querySelector('.version').textContent, '계약 v' + data.version);
    assert.equal(document.querySelectorAll('script[src], link[rel="stylesheet"]').length, 0);
  });
  await check('overview, focus dimming and deselection preserve all arrows', async () => {
    const count=document.querySelectorAll('.map-edge').length;
    assert.ok(count>0);assert.equal(document.querySelectorAll('.map-edge.dim').length,0);
    await click([...document.querySelectorAll('.map-node')].find(e=>e.textContent.includes('Orchestrator')));
    assert.equal(document.querySelectorAll('.map-edge').length,count);assert.ok(document.querySelectorAll('.map-edge.dim').length>0);
    await click(button('선택 해제'));
    assert.equal(document.querySelectorAll('.map-edge.dim').length,0);
    await click(document.querySelector('.map-edge'));
    assert.equal(document.querySelectorAll('.map-edge:not(.dim)').length,1);
    await click(button('선택 해제'));
  });
  await check('component and connection clicks reveal declared fields', async () => {
    await click([...document.querySelectorAll('.map-node')].find(e => e.textContent.includes('Answer Normalizer')));
    assert.equal(document.querySelector('.map-detail h2').textContent, '정규화·검증');
    await click(document.querySelector('.connection-list button'));
    assert.ok(document.querySelectorAll('.relation-table tbody tr').length);
  });
  await check('output destinations and direction controls', async () => {
    await click([...document.querySelectorAll('.map-node')].find(e => e.textContent.includes('Record Writer')));
    const output = [...document.querySelectorAll('.connection-list[data-direction=output] button')].find(e => e.textContent.includes('SessionStore'));
    await click(output);
    assert.match(document.querySelector('.relation-panel').textContent, /store_decisions/);
    await click(button('입력만'));
    assert.equal(document.querySelectorAll('.active-connections .outgoing:not(.dim),.active-connections .write:not(.dim)').length, 0);
    await click(button('출력만'));
    assert.equal(document.querySelectorAll('.active-connections .incoming:not(.dim)').length, 0);
    assert.equal(document.querySelector('.map-scroll svg').lastElementChild.getAttribute('class'), 'active-connections');
  });
  await check('type catalog search and schema rationale', async () => {
    await click(button('02계약·타입'));
    await click(button('전체 타입'));
    const input = document.querySelector('input');
    input.value = 'ValueMetadata'; input.dispatchEvent(new window.Event('input', { bubbles: true })); await settle();
    assert.equal(document.querySelectorAll('.catalog-list button').length, 1);
    await click(document.querySelector('.catalog-list button'));
    assert.equal(heading(), 'ValueMetadata');
    assert.ok(document.querySelector('.rationale p').textContent);
  });
  await check('reference links and raw schema toggle', async () => {
    await click(button('Precision ↗'));
    assert.equal(heading(), 'Precision');
    await click(document.querySelector('.actions button'));
    assert.match(document.querySelector('.json-block pre').textContent, /\$defs/);
    await click(document.querySelector('.actions button'));
  });
  await check('case link, contract filter and authored metadata example', async () => {
    await click(button('T1'));
    assert.match(heading(), /^T1 ·/);
    const select = document.querySelector('.specimen-controls select');
    select.value = 'NormalizerOutput'; select.dispatchEvent(new window.Event('change', { bubbles: true })); await settle();
    assert.equal(document.querySelector('.detail-panel h3').textContent, 'NormalizerOutput');
    assert.match([...document.querySelectorAll('.json-block pre')].at(-1).textContent, /approximate/);
  });
  await check('URL restoration selects a proposed storage contract', async () => {
    window.location.hash = '#view=contracts&item=SessionCommitResult';
    window.dispatchEvent(new window.HashChangeEvent('hashchange')); await settle();
    assert.equal(heading(), 'SessionCommitResult');
    assert.equal(document.querySelector('.status').textContent, '저장 API 초안');
  });
  await check('contract proposals and theme toggle', async () => {
    await click(button('04계약 제안'));
    assert.equal(document.querySelectorAll('.pending-card').length, data.proposals.length);
    await click(document.querySelector('.theme-button'));
    assert.equal(document.documentElement.dataset.theme, 'dark');
  });
  writeFileSync(new URL('../test-results/dom-report.json', import.meta.url), JSON.stringify({ scope: 'DOM_emulator_not_a_real_browser', checks, component_execution: false }, null, 2));
  await window.happyDOM.abort();
});
mkdirSync(new URL('../test-results/', import.meta.url), { recursive: true });
