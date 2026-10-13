import reference from './reference-layout.json' with { type: 'json' };

export const canvas = { width: 1540, height: 830 };
export const boxes = Object.fromEntries(Object.entries(reference.boxes).map(([id,[x,y,w,h]])=>[id,{x,y,w,h}]));
export const processingOrder=['utterance_parser','answer_normalizer','answer_judge','record_writer','dialogue_planner','response_generator'];
const additions = {
  'session_store|staff_console|read': [[250,770],[250,730],[195,730],[195,210],[105,210]],
  'orchestrator|answer_normalizer|data': [[360,270],[610,270],[610,210],[630,210]],
  'frontend|answer_judge|data': [[180,555],[195,555],[195,85],[830,85],[830,210],[850,210]],
  'frontend|response_generator|data': [[180,565],[195,565],[195,685],[990,685],[990,510]],
};
export function connectionKind(edge){return edge.kind==='write'?'write':['session_store','question_bank'].includes(edge.from)?'read':'data';}
export function routePoints(edge){
  const kind=connectionKind(edge);
  const original=reference.connections.find(c=>c.from===edge.from&&c.to===edge.to&&c.kind===kind);
  if(original?.id==='P4')return [[180,525],[205,525],[205,100],[450,100],[450,150]];
  if(original)return reference.routes[original.id];
  const key=[edge.from,edge.to,kind].join('|');
  if(additions[key])return additions[key];
  throw new Error('Explicit route required for '+key);
}
export function pathD(points,r=9){
  let d='M '+points[0].join(' ');
  for(let i=1;i<points.length-1;i++){
    const a=points[i-1],b=points[i],c=points[i+1];
    const l1=Math.hypot(b[0]-a[0],b[1]-a[1]),l2=Math.hypot(c[0]-b[0],c[1]-b[1]),rr=Math.min(r,l1/2,l2/2);
    d+=' L '+[b[0]-(b[0]-a[0])/l1*rr,b[1]-(b[1]-a[1])/l1*rr].join(' ')+' Q '+b.join(' ')+' '+[b[0]+(c[0]-b[0])/l2*rr,b[1]+(c[1]-b[1])/l2*rr].join(' ');
  }
  return d+' L '+points.at(-1).join(' ');
}
export function segmentHitsBox(a,z,b){
  if(a[0]===z[0])return a[0]>b.x&&a[0]<b.x+b.w&&Math.max(a[1],z[1])>b.y&&Math.min(a[1],z[1])<b.y+b.h;
  return a[1]>b.y&&a[1]<b.y+b.h&&Math.max(a[0],z[0])>b.x&&Math.min(a[0],z[0])<b.x+b.w;
}
// Multiple contracts on the same physical connection share one arrow.
export function placeLabels(edges,geometry){
 const groups=new Map(), result={};
 for(const e of edges){const key=[e.from,e.to,connectionKind(e)].join('|');if(!groups.has(key))groups.set(key,[]);groups.get(key).push(e);}
 const placed=[];
 for(const group of groups.values()){
  const points=geometry[group[0].id].points;
  const segments=points.slice(1).map((b,i)=>({a:points[i],b,l:Math.hypot(b[0]-points[i][0],b[1]-points[i][1])})).sort((a,b)=>b.l-a.l);
  const candidates=segments.flatMap(s=>[.5,.3,.7,.2,.8].map(t=>[s.a[0]+(s.b[0]-s.a[0])*t,s.a[1]+(s.b[1]-s.a[1])*t]));
  const chosen=candidates.find(p=>placed.every(a=>Math.hypot(p[0]-a[0],p[1]-a[1])>=26)&&!Object.values(boxes).some(b=>p[0]>b.x-11&&p[0]<b.x+b.w+11&&p[1]>b.y-11&&p[1]<b.y+b.h+11))||candidates[0];
  for(const e of group)result[e.id]=chosen;placed.push(chosen);
 }
 return result;
}
