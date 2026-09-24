import { animate, scroll } from 'motion';
const preference = matchMedia('(prefers-reduced-motion: reduce)');
const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
let cleanup = () => {};
function mount() {
  cleanup();
  if (preference.matches) return;
  const disposers = [];
  const layers = [...document.querySelectorAll('.scene-layer')];
  layers.forEach((layer, i) => {
    const controls = animate(layer, { opacity: [0, 1], y: [22, 0] }, { duration: .65, delay: i * .09, ease: [.22, 1, .36, 1] });
    disposers.push(() => { controls.cancel(); layer.style.removeProperty('opacity'); layer.style.removeProperty('transform'); });
  });
  const scene = document.querySelector('.studio-scene');
  const depth = scene?.querySelector('.scene-depth');
  if (depth && finePointer.matches) {
    const move = event => {
      const bounds = scene.getBoundingClientRect();
      const x = Math.max(-.5, Math.min(.5, (event.clientX-bounds.left)/bounds.width-.5));
      const y = Math.max(-.5, Math.min(.5, (event.clientY-bounds.top)/bounds.height-.5));
      depth.style.transform = `rotateX(${-y*5}deg) rotateY(${x*6}deg) translate3d(${x*5}px,${y*5}px,0)`;
    };
    const reset = () => depth.style.removeProperty('transform');
    scene.addEventListener('pointermove', move); scene.addEventListener('pointerleave', reset);
    disposers.push(() => { scene.removeEventListener('pointermove',move);scene.removeEventListener('pointerleave',reset);reset(); });
  }
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
