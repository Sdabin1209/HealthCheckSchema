import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import data from '../src/lib/data.js';

const resultDir = fileURLToPath(new URL('../test-results/', import.meta.url));
await mkdir(resultDir, { recursive: true });
const browser = await chromium.launch({ headless: true, ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH } : {}), args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1440, height: 1050 }, acceptDownloads: true });
const errors = [], external = [], checks = [];
page.on('pageerror', e => errors.push(e.message));
page.on('request', r => { if (/^https?:/.test(r.url())) external.push(r.url()); });
async function check(name, fn) { await fn(); checks.push(name); console.log('PASS ' + name); }
const fileUrl = new URL('../dist/index.html', import.meta.url).href;
try {
  await page.goto(fileUrl);
  await check('offline mount and component map', async () => {
    await page.getByRole('heading', { name: '어디서 받아, 무엇을 넘기는가' }).waitFor();
    assert.equal(await page.locator('.map-node').count(), data.components.length);
    assert.equal(await page.locator('.version').textContent(), '계약 v' + data.version);
  });
  await page.screenshot({ path: resultDir + 'desktop-map.png', fullPage: true });
  await check('component and declared connection selection', async () => {
    await page.locator('.map-node').filter({ hasText: 'Answer Normalizer' }).click();
    await page.locator('.connection-list button').first().click();
    await page.locator('.relation-table tbody tr').first().waitFor();
  });
  await check('type search, rationale and reference navigation', async () => {
    await page.getByRole('button', { name: /계약·타입/ }).click();
    await page.getByRole('button', { name: '전체 타입', exact: true }).click();
    await page.getByPlaceholder('ValueMetadata, 근거, LoRA…').fill('ValueMetadata');
    await page.locator('.catalog-list button').first().click();
    await page.getByRole('heading', { name: 'ValueMetadata', exact: true }).waitFor();
    await page.locator('.rationale summary').first().click();
    await page.getByRole('button', { name: 'T1', exact: true }).first().waitFor({ state: 'visible' });
    await page.getByRole('button', { name: 'Precision ↗', exact: true }).click();
    await page.getByRole('heading', { name: 'Precision', exact: true }).waitFor();
    await page.goBack();
    await page.getByRole('heading', { name: 'ValueMetadata', exact: true }).waitFor();
  });
  await page.screenshot({ path: resultDir + 'desktop-contract.png', fullPage: true });
  await check('standalone schema download', async () => {
    const waiting = page.waitForEvent('download');
    await page.getByRole('button', { name: '참조 포함 Schema 저장 ↓', exact: true }).click();
    const download = await waiting;
    const schema = JSON.parse(await readFile(await download.path(), 'utf8'));
    assert.equal(download.suggestedFilename(), 'ValueMetadata.json');
    assert.ok(schema.$defs.ValueMetadata && schema.$defs.Evidence && schema.$defs.TextSpan);
  });
  await check('rationale case link and specimen filters', async () => {
    await page.getByRole('button', { name: 'T1', exact: true }).first().click();
    await page.getByRole('heading', { name: /^T1 ·/ }).waitFor();
    await page.locator('.specimen-controls select').first().selectOption('NormalizerOutput');
    await page.getByRole('heading', { name: 'NormalizerOutput', exact: true }).waitFor();
    assert.match(await page.locator('.json-block pre').last().textContent(), /approximate/);
    await page.getByPlaceholder('B1, 정정, approximate…').fill('B1');
    await page.locator('.catalog-list button').filter({ has: page.getByText('B1', { exact: true }) }).click();
    await page.getByRole('heading', { name: /^B1 ·/ }).waitFor();
    await page.locator('.specimen-controls select').first().selectOption('SessionStore');
    assert.equal(await page.locator('.specimen-controls select').last().locator('option').count(), 3);
  });
  await page.screenshot({ path: resultDir + 'desktop-case.png', fullPage: true });
  await check('file deep link survives reload', async () => {
    await page.reload();
    await page.getByRole('heading', { name: /^B1 ·/ }).waitFor();
  });
  await check('proposal label, pending scope and dark theme', async () => {
    await page.goto(fileUrl + '#view=contracts&item=SessionCommitResult');
    await page.getByRole('heading', { name: 'SessionCommitResult', exact: true }).waitFor();
    assert.equal(await page.locator('.status').textContent(), '저장 API 초안');
    await page.getByRole('button', { name: /계약 제안/ }).click();
    assert.equal(await page.locator('.pending-card').count(), data.proposals.length);
    await page.getByRole('button', { name: '어두운 화면으로 변경', exact: true }).click();
    assert.equal(await page.locator('html').getAttribute('data-theme'), 'dark');
  });
  await check('mobile screens have no document overflow', async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    for (const name of ['구조 지도', '계약·타입', '정적 예시', '계약 제안']) {
      await page.getByRole('button', { name: new RegExp(name) }).click();
      const size = await page.evaluate(() => ({ document: document.documentElement.scrollWidth, viewport: innerWidth }));
      assert.ok(size.document <= size.viewport, name + ': ' + JSON.stringify(size));
    }
    await page.getByRole('button', { name: /구조 지도/ }).click();
    await page.screenshot({ path: resultDir + 'mobile-map.png', fullPage: true });
  });
  await check('no runtime errors or external network requests', async () => {
    assert.deepEqual(errors, []); assert.deepEqual(external, []);
  });
  await writeFile(resultDir + 'browser-report.json', JSON.stringify({ browser: browser.version(), checks, failures: [], scope: 'presentation_ui_only', component_execution: false }, null, 2));
} catch (e) {
  await page.screenshot({ path: resultDir + 'failure.png', fullPage: true });
  throw e;
} finally { await browser.close(); }
