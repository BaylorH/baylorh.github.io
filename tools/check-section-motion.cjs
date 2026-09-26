const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');
const source = fs.readFileSync('assets/js/source/section-motion.js','utf8').replace('export function','function');
function element(){return {style:{removed:[],removeProperty(key){this.removed.push(key);}}};}
const sections=[element(),element()],layers=[element(),element(),element()],lines=[element(),element()];
const toolkit={},diagram={};
const root={querySelector:s=>s==='.toolkit'?toolkit:diagram,querySelectorAll:s=>s==='.tool-layer'?layers:s==='.system-connector i'?lines:sections};
let animations=[],stopped=0,cancelled=0;
const context={document:root};vm.createContext(context);vm.runInContext(source,context);
const animate=(el,frames)=>{assert.ok(!('opacity' in frames),'Text must never wait to become visible');animations.push({el,frames});return {cancel(){cancelled++;}}};
const scroll=(animation,options)=>{assert.ok(options.target);assert.ok(options.offset.length===2);return()=>{stopped++;};};
const dispose=context.mountSectionMotion({animate,scroll,root,desktop:true});
assert.equal(animations.length,7);dispose();dispose();assert.equal(stopped,7);assert.equal(cancelled,7);assert.ok([...sections,...layers,...lines].every(e=>e.style.removed.includes('transform')));
animations=[];const disposeMobile=context.mountSectionMotion({animate,scroll,root,desktop:false});assert.equal(animations.length,2,'Mobile omits layered choreography');disposeMobile();
console.log('PASS: section motion preserves readable text, cleans up scroll bindings/styles, supports repeated disposal and limits mobile choreography');
