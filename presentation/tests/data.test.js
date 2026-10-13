import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import data, { standalone } from '../src/lib/data.js';

const root = fileURLToPath(new URL('../../', import.meta.url));
const read = path => JSON.parse(readFileSync(root + path, 'utf8'));
const annotationKeys = new Set(['title', 'description', 'x-why', 'x-cases']);
function constraints(value) {
  if (Array.isArray(value)) return value.map(constraints);
  if (!value || typeof value !== 'object') return value;
  return Object.fromEntries(Object.entries(value).filter(([k]) => !annotationKeys.has(k)).map(([k, v]) => [k, constraints(v)]));
}

test('presentation preserves every canonical schema constraint and source identity', () => {
  const source = read('generated/source_manifest.json');
  assert.equal(data.version, source.contract_version);
  assert.equal(data.sourceDigest, source.source_sha256);
  assert.deepEqual(constraints(data.definitions), constraints(read('generated/schemas/all.json').$defs));
});

test('all authored specimen values survive deduplication unchanged', () => {
  for (const c of data.cases) {
    const source = read(c.source);
    assert.equal(c.specimens.length, source.specimens.length);
    c.specimens.forEach((specimen, i) => {
      assert.deepEqual(data.values[specimen.valueIndex], source.specimens[i].data, c.id + '/' + specimen.id);
      assert.ok(data.definitions[specimen.contract], specimen.contract);
    });
  }
});

test('every downloadable contract contains the full reference closure', () => {
  for (const name of Object.keys(data.definitions)) {
    const schema = standalone(name);
    function walk(value) {
      if (!value || typeof value !== 'object') return;
      if (value.$ref) assert.ok(schema.$defs[value.$ref.split('/').at(-1)], name + ': ' + value.$ref);
      Object.values(value).forEach(walk);
    }
    walk(schema);
  }
});

test('proposed storage ports remain distinct from current contracts', () => {
  for (const component of data.components) {
    for (const [role, name] of Object.entries(component.contracts)) {
      assert.equal(data.entries[name].status === 'proposal', component.contract_status?.[role] === 'proposal');
    }
  }
});

test('every displayed arrow avoids all component interiors', async () => {
  const { boxes, routePoints, segmentHitsBox } = await import('../src/lib/map-layout.js');
  for (const edge of data.edges.filter(e => e.from && e.to && e.from !== e.to && data.entries[e.source]?.status !== 'proposal' && data.entries[e.target]?.status !== 'proposal')) {
    const points = routePoints(edge);
    assert.ok(points.length >= 2, edge.id);
    for (let i=1; i<points.length; i++) {
      for (const [id,box] of Object.entries(boxes)) assert.equal(segmentHitsBox(points[i-1],points[i],box), false, edge.id + ' crosses ' + id);
    }
  }
});

test('focused connection numbers remain separate and outside component boxes', async () => {
  const {routePoints,placeLabels,boxes}=await import('../src/lib/map-layout.js');
  const edges=data.edges.filter(e=>e.from&&e.to&&e.from!==e.to&&data.entries[e.source]?.status!=='proposal'&&data.entries[e.target]?.status!=='proposal');
  const geometry=Object.fromEntries(edges.map(e=>[e.id,{points:routePoints(e)}]));
  for(const component of data.components){
    const related=edges.filter(e=>e.from===component.id||e.to===component.id);
    const labels=[...new Map(Object.values(placeLabels(related,geometry)).map(p=>[p.join(','),p])).values()];
    labels.forEach((a,i)=>labels.slice(i+1).forEach(b=>assert.ok(Math.hypot(a[0]-b[0],a[1]-b[1])>=26)));
    for(const p of labels)for(const b of Object.values(boxes))assert.ok(!(p[0]>b.x-12&&p[0]<b.x+b.w+12&&p[1]>b.y-12&&p[1]<b.y+b.h+12));
  }
});

test('all component positions preserve the repository HTML layout',async()=>{
 const ref=JSON.parse(readFileSync(new URL('../src/lib/reference-layout.json',import.meta.url),'utf8'));
 const {boxes}=await import('../src/lib/map-layout.js');
 for(const [id,[x,y,w,h]] of Object.entries(ref.boxes))assert.deepEqual(boxes[id],{x,y,w,h});
});
