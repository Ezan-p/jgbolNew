// Exercise real page handlers without requiring Android to verify cancellation races.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('network_redirect/login.html', 'utf8').split('<script>')[1].split('</script>')[0];
function page(remembered) {
  const elements = {}, requests = [], completed = [], timers = new Map();
  let next = 0;
  const context = {document: {getElementById(id) {return elements[id] ||= {style:{}, value:'', checked:false};}},
    window: {LocalGame:true}, LocalGame:{complete(token){completed.push(token);}},
    location:{search:'?switch=1'},
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
console.log('6 login page scenarios passed');
