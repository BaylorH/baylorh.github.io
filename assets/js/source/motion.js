import { animate, scroll, stagger, inView } from 'motion';
import './ambient.js';
const preference = matchMedia('(prefers-reduced-motion: reduce)');
const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
let cleanup = () => {};
function mount() {
  cleanup();
  if (preference.matches) return;
  const disposers = [];
  // Split only display headings; normal paragraphs remain untouched and readable.
  document.querySelectorAll('[data-reveal-heading]').forEach(heading => {
    if (!heading.querySelector('.reveal-word')) {
      [...heading.childNodes].filter(node => node.nodeType === Node.TEXT_NODE).forEach(node => {
        const fragment = document.createDocumentFragment();
        node.textContent.split(/(\s+)/).forEach(word => {
          if (!word.trim()) fragment.append(document.createTextNode(word));
          else { const span = document.createElement('span'); span.className = 'reveal-word'; span.textContent = word; fragment.append(span); }
        });
        node.replaceWith(fragment);
      });
    }
    const words = [...heading.querySelectorAll('.reveal-word')];
    const controls = animate(words, {opacity:[.5,1], y:[12,0]}, {delay:stagger(.055), ease:'linear'});
    const stop = scroll(controls, {target:heading, offset:['start 94%','end 72%']});
    disposers.push(() => { stop(); controls.cancel(); words.forEach(word => {word.style.removeProperty('opacity');word.style.removeProperty('transform');}); });
  });
  const stopCards = inView('.project-card, .approach-grid article', element => {
    const controls = animate(element, {opacity:[.65,1], y:[20,0]}, {duration:.5, ease:[.22,1,.36,1]});
    disposers.push(() => {controls.cancel();element.style.removeProperty('opacity');element.style.removeProperty('transform');});
  }, {margin:'0px 0px -30px 0px'});
  disposers.push(stopCards);
  if (matchMedia('(min-width: 761px)').matches) {
    document.querySelectorAll('.featured-media').forEach(media => {
      const controls=animate(media,{scale:[.94,1],y:[24,0]},{ease:'linear'});
      const stop=scroll(controls,{target:media.parentElement,offset:['start end','center center']});
      disposers.push(()=>{stop();controls.cancel();media.style.removeProperty('transform');});
    });
  }
  cleanup = () => disposers.forEach(dispose=>dispose());
}
mount();
preference.addEventListener('change',mount);
finePointer.addEventListener('change',mount);
const desktop=matchMedia('(min-width: 761px)');desktop.addEventListener('change',mount);
window.addEventListener('pagehide',()=>cleanup());
window.addEventListener('pageshow',event=>{if(event.persisted)mount();});
