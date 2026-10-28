// Exercise real page handlers without requiring Android to verify cancellation races.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('network_redirect/login.html', 'utf8').split('<script>')[1].split('</script>')[0];
function page(remembered, search='') {
  const elements = {}, requests = [], completed = [], timers = new Map();
  let next = 0;
  const context = {document: {getElementById(id) {return elements[id] ||= {style:{}, value:'', checked:false};}},
    window: {LocalGame:true}, LocalGame:{complete(token){completed.push(token);}},
    location:{search},
    setTimeout(fn){timers.set(++next,fn);return next;}, clearTimeout(id){timers.delete(id);},
    XMLHttpRequest: function(){this.open=()=>{};this.setRequestHeader=()=>{};this.send=body=>requests.push({xhr:this,body:JSON.parse(body)});}};
  vm.runInNewContext(source.replace('__AUTO_LOGIN__', String(remembered)),context);
  return {elements, requests, completed, tick(){for(const fn of [...timers.values()])fn();timers.clear();}, reply(result){const req=requests.at(-1);req.xhr.responseText=JSON.stringify(result);req.xhr.onload();}};
}
let p=page(false);p.tick();assert.equal(p.requests.length,0);
p=page(true);p.tick();assert.equal(p.requests[0].body.action,'resume');p.reply({ok:true,token:'session'});assert.deepEqual(p.completed,['session']);
p=page(true);p.elements.change.onclick();p.tick();assert.equal(p.requests.length,1);assert.equal(p.requests[0].body.action,'forget');
p=page(true);p.tick();p.elements.change.onclick();p.reply({ok:true,token:'must-not-enter'});assert.equal(p.requests[1].body.action,'forget');p.reply({ok:true});assert.deepEqual(p.completed,[]);
p=page(true);p.elements.username.onfocus();p.tick();assert.equal(p.requests.length,0);
p=page(true);p.tick();p.reply({ok:false,error:'expired'});assert.deepEqual(p.completed,[]);assert.equal(p.elements.submit.disabled,false);
// Native account switching must revoke credentials before enabling password login.
for (const remembered of [true, false]) {
  p=page(remembered, '?switch=1');p.tick();
  assert.equal(p.requests.length,1);assert.equal(p.requests[0].body.action,'forget');
  assert.equal(p.elements.submit.disabled,true);p.reply({ok:true});
  assert.equal(p.elements.submit.disabled,false);assert.deepEqual(p.completed,[]);
  p.tick();assert.equal(p.requests.length,1);
}
p=page(true,'?switch=10');p.tick();assert.equal(p.requests[0].body.action,'resume');
// Switching while a password login is pending must not enter the old account.
p=page(false);p.elements.username.value='alice';p.elements.password.value='test-pass-123';
p.elements.form.onsubmit({preventDefault(){}});p.elements.change.onclick();
assert.equal(p.elements.password.value,'');p.reply({ok:true,token:'old-account'});
assert.equal(p.requests[1].body.action,'forget');p.reply({ok:true});assert.deepEqual(p.completed,[]);
// A timed-out resume may still have issued a cookie: always follow with forget.
p=page(true);p.tick();p.elements.change.onclick();p.requests[0].xhr.ontimeout();
assert.equal(p.requests[1].body.action,'forget');p.reply({ok:true});assert.deepEqual(p.completed,[]);
// Failed revocation stays locked until an explicit retry succeeds.
p=page(true,'?switch=1');p.requests[0].xhr.onerror();
assert.equal(p.elements.submit.disabled,true);p.elements.form.onsubmit({preventDefault(){}});
assert.equal(p.requests.length,1);p.elements.change.onclick();p.reply({ok:true});
assert.equal(p.elements.submit.disabled,false);
console.log('12 login page scenarios passed');
