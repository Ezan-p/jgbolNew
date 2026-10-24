'use strict';
const $=id=>document.getElementById(id),canvas=$('screen'),ctx=canvas.getContext('2d',{alpha:false});
let ws,audioSession=null,audioAvailable=false,frameCount=0,frameStart=performance.now();const fingers=new Map();
function note(s){$('notice').textContent=s;}
function send(d){if(ws?.readyState===WebSocket.OPEN)ws.send(JSON.stringify(d));}
function socket(path){return new WebSocket(`${location.protocol==='https:'?'wss':'ws'}://${location.host}${path}`);}
let statusPending=false;
async function status(){
 if(statusPending)return;statusPending=true;
 try{
  const r=await fetch('/api/status'),s=await r.json();
  if(s.ui){$('edition').textContent=s.ui.edition;$('game-help').textContent=s.ui.help;}
  $('status').textContent=s.emulator?'● 安卓设备已连接':'○ 等待安卓设备';
  $('launch').disabled=!s.emulator||!s.device?.booted||!s.device?.compatible;
  audioAvailable=Boolean(s.audio&&s.emulator);
  if(!audioAvailable)stopAudio();
  $('sound').disabled=!audioAvailable;
  if(!s.audio)$('sound').textContent=s.mode==='adb'?'声音由安卓设备播放':'声音不可用';
  else if(!audioSession)$('sound').textContent='♬ 开启声音';
  $('compatibility').textContent=s.emulator
   ?(s.device.issue||(s.mode==='adb'?'设备支持本游戏 · ADB 模式：单指操作，声音由设备播放':s.runtime_profile.startsWith('arm32-')?'32 位安卓环境已就绪 · 软件仿真，启动和加载较慢':'设备支持本游戏 · 内置模拟器模式'))
   :(s.message||'请启动安卓环境，再重新连接。');
 }catch{
  $('status').textContent='服务连接中断';$('launch').disabled=true;
  $('compatibility').textContent='无法读取设备状态，请检查本机游戏台服务。';
 }finally{statusPending=false;}
}
setInterval(status,5000);status();
$('connect').onclick=()=>{
 if(ws){ws.close();return;}
 const connection=socket('/ws/screen?format=rgba');ws=connection;let frameInfo=null;ws.binaryType='arraybuffer';$('connect').textContent='连接中…';
 ws.onopen=()=>{$('connect').textContent='断开画面';note('已连接。点击画面操作游戏。');$('stage').focus();};
 ws.onmessage=async e=>{
  if(typeof e.data==='string'){const d=JSON.parse(e.data);if(d.type==='frame')frameInfo=d;if(d.type==='error')note(d.message);if(d.type==='action_result')note(d.ok?'操作已发送':d.error);return;}
  try{
   if(ws!==connection)return;
   if(frameInfo?.encoding==='rgba'){
    const {width,height}=frameInfo;
    if(e.data.byteLength!==width*height*4)throw new Error('Invalid RGBA frame size');
    if(canvas.width!==width||canvas.height!==height){canvas.width=width;canvas.height=height;}
    ctx.putImageData(new ImageData(new Uint8ClampedArray(e.data),width,height),0,0);
   }else{
    const image=await createImageBitmap(new Blob([e.data],{type:'image/png'}));
    try{if(ws!==connection)return;if(canvas.width!==image.width||canvas.height!==image.height){canvas.width=image.width;canvas.height=image.height;}ctx.drawImage(image,0,0);}finally{image.close();}
   }
   $('empty').hidden=true;frameCount++;const now=performance.now();if(now-frameStart>1000){$('fps').textContent=`${(frameCount*1000/(now-frameStart)).toFixed(1)} FPS · ${canvas.width} × ${canvas.height}`;frameCount=0;frameStart=now;}
  }catch(err){note('画面解码失败：'+err.message);}finally{if(connection.readyState===WebSocket.OPEN)connection.send(JSON.stringify({type:'ack'}));}
 };
 ws.onerror=()=>note('无法连接画面。请确认模拟器已启动，且没有其他窗口正在控制。');
 ws.onclose=()=>{if(ws!==connection)return;ws=null;clearMoves();fingers.clear();$('connect').textContent='连接画面';$('fps').textContent='已断开';};
};
async function action(name){if(ws?.readyState===WebSocket.OPEN){send({type:'action',action:name});return;}try{const r=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:name})});const d=await r.json();note(d.ok?'操作已发送':d.error);}catch(e){note('操作失败：'+e.message);}}
$('launch').onclick=()=>action('launch');document.querySelectorAll('[data-action]').forEach(b=>b.onclick=()=>action(b.dataset.action));
function coords(e){const r=canvas.getBoundingClientRect(),scale=Math.min(r.width/canvas.width,r.height/canvas.height),w=canvas.width*scale,h=canvas.height*scale;return {x:Math.max(0,Math.min(1,(e.clientX-r.left-(r.width-w)/2)/w)),y:Math.max(0,Math.min(1,(e.clientY-r.top-(r.height-h)/2)/h))};}
canvas.onpointerdown=e=>{if(!ws||fingers.size>=10)return;e.preventDefault();canvas.setPointerCapture(e.pointerId);const p=coords(e);fingers.set(e.pointerId,p);send({type:'touch',id:e.pointerId,...p,down:true});};
const pendingMoves=new Map();let moveFrame=null;
function clearMoves(){if(moveFrame!==null)cancelAnimationFrame(moveFrame);moveFrame=null;pendingMoves.clear();}
canvas.onpointermove=e=>{
 if(!fingers.has(e.pointerId))return;
 const p=coords(e);fingers.set(e.pointerId,p);pendingMoves.set(e.pointerId,p);
 if(moveFrame===null)moveFrame=requestAnimationFrame(()=>{
  moveFrame=null;for(const [id,p]of pendingMoves)send({type:'touch',id,...p,down:true});pendingMoves.clear();
 });
};
function release(e){if(!fingers.has(e.pointerId))return;pendingMoves.delete(e.pointerId);send({type:'touch',id:e.pointerId,...coords(e),down:false});fingers.delete(e.pointerId);}
canvas.onpointerup=release;canvas.onpointercancel=release;canvas.onlostpointercapture=release;
window.addEventListener('blur',()=>{clearMoves();for(const [id,p]of fingers)send({type:'touch',id,...p,down:false});fingers.clear();});
$('stage').onkeydown=e=>{if(e.metaKey||e.ctrlKey||e.altKey)return;if(e.key==='Escape'){action('back');e.preventDefault();}else if(e.key.length===1||['Enter','Backspace','Tab','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)){send({type:'key',key:e.key});e.preventDefault();}};
$('fullscreen').onclick=()=>document.fullscreenElement?document.exitFullscreen():$('stage').requestFullscreen();
function stopAudio(session=audioSession){
 if(!session)return;
 if(audioSession===session){audioSession=null;$('sound').textContent='♬ 开启声音';}
 session.socket?.close();
 for(const source of session.sources){try{source.stop();}catch{}}
 session.sources.clear();
 if(session.context.state!=='closed')session.context.close().catch(()=>{});
}
$('sound').onclick=async()=>{
 if(audioSession){stopAudio();return;}
 if(!audioAvailable)return;
 let session;
 try{
  const context=new AudioContext({sampleRate:44100});
  session={context,socket:null,scheduled:0,sources:new Set()};audioSession=session;
  $('sound').textContent='♬ 连接声音中…';
  await context.resume();
  if(audioSession!==session)return;
  const connection=socket('/ws/audio');session.socket=connection;connection.binaryType='arraybuffer';
  connection.onopen=()=>{if(audioSession===session)$('sound').textContent='♬ 关闭声音';};
  connection.onmessage=e=>{
   if(audioSession!==session)return;
   if(typeof e.data==='string'){try{const d=JSON.parse(e.data);if(d.type==='error')note(d.message);}catch{}return;}
   if(context.state!=='running')return;
   const pcm=new DataView(e.data),n=Math.floor(pcm.byteLength/4);if(!n)return;
   const now=context.currentTime;if(session.scheduled>now+.35)return;
   const b=context.createBuffer(2,n,44100);
   for(let ch=0;ch<2;ch++){const out=b.getChannelData(ch);for(let i=0;i<n;i++)out[i]=pcm.getInt16(i*4+ch*2,true)/32768;}
   if(session.scheduled<now)session.scheduled=now+.04;
   const source=context.createBufferSource();source.buffer=b;source.connect(context.destination);
   session.sources.add(source);source.onended=()=>{session.sources.delete(source);source.disconnect();};
   source.start(session.scheduled);session.scheduled+=n/44100;
  };
  connection.onerror=()=>{if(audioSession===session)note('音频连接失败，请检查模拟器音频服务或关闭其他窗口的声音。');};
  connection.onclose=()=>stopAudio(session);
 }catch(e){stopAudio(session);note('无法开启声音：'+e.message);}
};
window.addEventListener('pagehide',()=>stopAudio());
