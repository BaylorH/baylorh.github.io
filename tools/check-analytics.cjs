const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const file='assets/js/analytics.js';
assert.ok(fs.existsSync(file),'Optional analytics loader has not been implemented');
const source=fs.readFileSync(file,'utf8');
function run(host,id,choice){
 const appended=[];const listeners={};
 const document={querySelector:s=>s==='meta[name="analytics-id"]'?{content:id}:null,createElement:tag=>({tag,className:'',setAttribute(){},append(){},addEventListener(){}}),head:{append:e=>appended.push(e)},body:{append:e=>appended.push(e)},addEventListener:(type,fn)=>listeners[type]=fn,title:'Portfolio'};
 const context={document,location:{hostname:host,origin:'https://'+host,pathname:'/',href:'https://'+host+'/?private=secret'},localStorage:{getItem:()=>choice,setItem(){}},URL,window:null};context.window=context;vm.runInNewContext(source,context);return{context,appended,listeners};
}
assert.equal(run('127.0.0.1','G-TEST123','granted').appended.length,0);
assert.equal(run('baylor-harrison.com','','granted').appended.length,0);
const denied=run('baylor-harrison.com','G-TEST123','denied');assert.ok(!denied.appended.some(x=>x.tag==='script'));
const allowed=run('baylor-harrison.com','G-TEST123','granted');assert.equal(allowed.appended.filter(x=>x.tag==='script').length,1);assert.ok(!JSON.stringify(allowed.context.dataLayer).includes('private=secret'));
console.log('PASS: analytics disabled on previews/unconfigured sites, consent gate and sanitized page event');

assert.ok(allowed.context.dataLayer.every(command=>Object.prototype.toString.call(command)==='[object Arguments]'));
