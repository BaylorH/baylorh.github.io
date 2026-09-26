const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');
const source = fs.readFileSync('assets/js/source/section-motion.js','utf8').replace('export function','function');
function element(height=540){return {offsetHeight:height, style:{removed:[],removeProperty(key){this.removed.push(key);}},querySelector(){return null;}};}
function fixture(height=540,keyboardFocused=false){
 const stories=[element(height),element(height),element(height)],media=stories.map(()=>element()),cards=[element(),element()];
 stories.forEach((e,i)=>e.querySelector=()=>media[i]);
 cards.forEach(e=>e.querySelector=()=>element());
 const classes=new Set(),listeners={};
 const selected={classList:{add:c=>classes.add(c),remove:c=>classes.delete(c),contains:c=>classes.has(c)},addEventListener:(e,f)=>listeners[e]=f,removeEventListener:e=>delete listeners[e]};
 const root={querySelector:s=>s==='.selected-work'?selected:s==='.selected-work :focus-visible'&&keyboardFocused?{}:null,querySelectorAll:s=>s==='.featured-story'?stories:s==='.project-card'?cards:[]};
 const animations=[],bindings=[];let stopped=0,cancelled=0;
 const animate=(el,frames)=>{assert.ok(!('opacity' in frames),'Text must not be hidden while waiting for scroll');const a={el,frames,cancel(){cancelled++;}};animations.push(a);return a;};
 const scroll=(animation,options)=>{bindings.push({animation,options});return()=>stopped++;};
 const ctx={document:root,innerHeight:900};vm.createContext(ctx);vm.runInContext(source,ctx);
 return {stories,root,classes,listeners,animations,bindings,getStopped:()=>stopped,getCancelled:()=>cancelled,mount:o=>ctx.mountSectionMotion({animate,scroll,root,viewportHeight:900,...o})};
}
let f=fixture();let dispose=f.mount({desktop:true});
assert.ok(f.classes.has('has-scroll-scenes'),'Fitting desktop panels must actually pin, not just translate a few pixels');
assert.ok(f.bindings.some(b=>b.animation.el===f.stories[0]&&b.options.target===f.stories[1]),'A departing panel must respond to the arriving panel');
assert.ok(f.animations.length>3,'Directory media must also participate');
const n=f.animations.length;dispose();dispose();assert.equal(f.getStopped(),n);assert.equal(f.getCancelled(),n);assert.ok(!f.classes.has('has-scroll-scenes'));assert.equal(Object.keys(f.listeners).length,0);
f=fixture(1000);dispose=f.mount({desktop:true});assert.ok(!f.classes.has('has-scroll-scenes'),'Tall content must remain readable in normal document flow');dispose();
f=fixture();dispose=f.mount({desktop:false});assert.ok(!f.classes.has('has-scroll-scenes'),'Mobile stays in document flow');dispose();
f=fixture();dispose=f.mount({desktop:true});f.listeners.focusin({target:{matches:()=>true}});assert.ok(!f.classes.has('has-scroll-scenes'),'Keyboard navigation must not leave focused links beneath overlapping panels');dispose();
f=fixture(540,true);dispose=f.mount({desktop:true});assert.ok(!f.classes.has('has-scroll-scenes'),'Remount must preserve an existing keyboard focus fallback');dispose();
console.log('PASS: fitted sticky scenes, next-panel-linked motion, directory coverage, tall/mobile fallbacks, keyboard escape and complete disposal');
