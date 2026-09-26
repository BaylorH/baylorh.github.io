import { animate, scroll, stagger } from 'motion';
import './ambient.js';
import { mountSectionMotion } from './section-motion.js';
const preference = matchMedia('(prefers-reduced-motion: reduce)');
const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
let cleanup = () => {};
function mount() {
  cleanup();
  if (preference.matches) return;
  const disposers = [];
  disposers.push(mountSectionMotion({animate, scroll, desktop:matchMedia('(min-width: 851px)').matches}));
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
  cleanup = () => disposers.forEach(dispose=>dispose());
}
mount();
preference.addEventListener('change',mount);
finePointer.addEventListener('change',mount);
const desktop=matchMedia('(min-width: 851px)');desktop.addEventListener('change',mount);
window.addEventListener('pagehide',()=>cleanup());
window.addEventListener('pageshow',event=>{if(event.persisted)mount();});
