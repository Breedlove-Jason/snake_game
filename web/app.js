const $ = id => document.getElementById(id);
const canvas = $('board'), ctx = canvas.getContext('2d');
let engine, game, state, timer, speed = 145, best = 0, loading = false;
try { best = Math.max(0, Math.min(573, Number(localStorage.getItem('jb-snake-best')) || 0)); } catch {}
$('best').textContent = String(best).padStart(2, '0');
const preview = { size:24, snake:[[12,12],[11,12],[10,12]], food:[17,8], score:0, status:'ready' };
function draw(s) {
  const cell = canvas.width / s.size;
  ctx.fillStyle = '#0b1410'; ctx.fillRect(0,0,canvas.width,canvas.height);
  ctx.strokeStyle = '#1c2c21'; ctx.lineWidth = 1;
  for(let i=1;i<s.size;i++){ctx.beginPath();ctx.moveTo(i*cell,0);ctx.lineTo(i*cell,canvas.height);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i*cell);ctx.lineTo(canvas.width,i*cell);ctx.stroke();}
  if(s.food){ctx.fillStyle='#ff7191';ctx.beginPath();ctx.arc((s.food[0]+.5)*cell,(s.food[1]+.5)*cell,cell*.32,0,Math.PI*2);ctx.fill();}
  s.snake.forEach(([x,y],i)=>{ctx.fillStyle=i===0?'#d2ff66':'#5eac80';ctx.fillRect(x*cell+2,y*cell+2,cell-4,cell-4);});
}
function sync() {
  state = JSON.parse(game.snapshot()); draw(state);
  $('score').textContent = String(state.score).padStart(2,'0');
  if(state.score>best){best=state.score;try{localStorage.setItem('jb-snake-best',String(best));}catch{}}
  $('best').textContent=String(best).padStart(2,'0');
  speed=Math.max(65,145-state.score*2);
  $('overlay').hidden=state.status==='running';
  const copy={ready:['YOUR NEXT RUN','Ready to grow?','Start a game, then use arrows, WASD, or touch controls.'],paused:['TAKE YOUR TIME','A little breather.','Resume when you’re ready.'],over:['THAT’S A WRAP','One more turn?','Your next personal best is just a run away.'],won:['ALL FILLED UP','Perfect run.','Every cell. Every turn. You did it.']};
  if(copy[state.status]){const [label,title,text]=copy[state.status];$('overlay-label').textContent=label;$('overlay-title').textContent=title;$('overlay-text').textContent=text;}
  $('pause').disabled=state.status!=='running';
  $('start').disabled=state.status==='running';
  $('start').textContent=state.status==='paused'?'Resume ↗':state.status==='ready'?'Start game ↗':'Play again ↗';
  $('status').textContent=state.status==='running'?'Keep moving. Space pauses the game.':state.status==='paused'?'Paused. Your run is waiting.':state.status==='over'?`Game over. You collected ${state.score} fruit.`:state.status==='won'?'Board complete!': 'Ready. Choose your first move.';
}
function tick(){clearTimeout(timer);if(!game||state.status!=='running')return;game.step();sync();if(state.status==='running')timer=setTimeout(tick,speed);}
function start(){if(!game)return;if(['over','won'].includes(state.status))game.reset();game.start();sync();clearTimeout(timer);timer=setTimeout(tick,speed);canvas.focus({preventScroll:true});}
function pause(){if(!game)return;game.pause();clearTimeout(timer);sync();}
function restart(){if(!game)return;clearTimeout(timer);game.reset();sync();canvas.focus({preventScroll:true});}
function turn(direction){if(game&&state.status==='running')game.turn(direction);}
$('start').addEventListener('click',()=>game?start():load());
$('pause').addEventListener('click',pause);$('restart').addEventListener('click',restart);
const keys={ArrowUp:'up',w:'up',W:'up',ArrowDown:'down',s:'down',S:'down',ArrowLeft:'left',a:'left',A:'left',ArrowRight:'right',d:'right',D:'right'};
canvas.addEventListener('keydown',event=>{if(keys[event.key]){event.preventDefault();turn(keys[event.key]);}else if(event.code==='Space'){event.preventDefault();if(!event.repeat)state?.status==='running'?pause():start();}else if(event.key.toLowerCase()==='r'&&!event.repeat){restart();}});
for(const button of document.querySelectorAll('[data-direction]'))button.addEventListener('click',()=>{turn(button.dataset.direction);canvas.focus({preventScroll:true});});
let touch;
canvas.addEventListener('pointerdown',event=>{touch=[event.clientX,event.clientY];canvas.setPointerCapture(event.pointerId);canvas.focus({preventScroll:true});});
canvas.addEventListener('pointerup',event=>{if(!touch)return;const dx=event.clientX-touch[0],dy=event.clientY-touch[1];touch=null;if(Math.max(Math.abs(dx),Math.abs(dy))<12)return;turn(Math.abs(dx)>Math.abs(dy)?dx>0?'right':'left':dy>0?'down':'up');});
canvas.addEventListener('pointercancel',()=>{touch=null;});
document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
window.addEventListener('blur',pause);
async function load(){
 if(loading)return;loading=true;$('start').disabled=true;$('status').textContent='Loading Python. The first visit may take a moment.';
 try{
   const {loadPyodide}=await import('https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs');
   engine=await loadPyodide();
   const response=await fetch('engine.py');if(!response.ok)throw new Error('Game rules unavailable');
   engine.runPython(await response.text());engine.runPython('game = Game()');game=engine.globals.get('game');
   $('restart').disabled=false;sync();
 }catch(error){console.error(error);$('overlay-title').textContent='Couldn’t load the game.';$('overlay-text').textContent='Check your connection and try again.';$('status').textContent='Python could not load. Select Retry to try again.';$('start').textContent='Retry';$('start').disabled=false;}
 finally{loading=false;}
}
draw(preview);load();
