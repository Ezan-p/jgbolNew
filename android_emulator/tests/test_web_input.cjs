// Run with: node android_emulator/tests/test_web_input.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const elements = new Map(), listeners = {}, scheduled = new Map(), sent = [];
let nextId = 0;
const element = id => {
 if (!elements.has(id)) elements.set(id, {
  width:960,height:540,getContext:()=>({}),setPointerCapture:()=>{},
  getBoundingClientRect:()=>({left:0,top:0,width:960,height:540}),
 });
 return elements.get(id);
};
const sandbox = {
 document:{getElementById:element,querySelectorAll:()=>[]},
 window:{addEventListener:(name,fn)=>listeners[name]=fn},
 performance:{now:()=>0},setInterval:()=>{},fetch:()=>new Promise(()=>{}),
 WebSocket:{OPEN:1},requestAnimationFrame:fn=>{scheduled.set(++nextId,fn);return nextId;},
 cancelAnimationFrame:id=>scheduled.delete(id), sent,
};
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync('android_emulator/web/app.js','utf8'),sandbox);
vm.runInContext('ws={readyState:1,send:s=>sent.push(JSON.parse(s))}',sandbox);
const canvas=element('screen');
const event=x=>({pointerId:1,clientX:x,clientY:100,preventDefault:()=>{}});
canvas.onpointerdown(event(10));
for(let i=20;i<100;i++)canvas.onpointermove(event(i));
assert.equal(sent.length,1); // Moves have not flooded the socket.
assert.equal(scheduled.size,1);
const flush=()=>{const callbacks=[...scheduled.values()];scheduled.clear();callbacks.forEach(fn=>fn());};
flush();
assert.equal(sent.length,2);
assert.equal(sent[1].x,99/960); // Latest position wins.
canvas.onpointermove(event(200));
canvas.onpointerup(event(220));
flush();
assert.equal(sent.length,3); // No stale move resurrects a released finger.
assert.equal(sent[2].down,false);
canvas.onpointerdown(event(10));canvas.onpointermove(event(20));listeners.blur();flush();
assert.equal(sent.at(-1).down,false);
assert.equal(sent.length,5);
console.log('Touch coalescing, release ordering, and blur cleanup passed');
