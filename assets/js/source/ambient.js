// Continuous decoration is optional, viewport-bound, and paused in background tabs.
let ambientPaused = false;
function mountAmbient() {
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const roots = [...document.querySelectorAll('[data-image-stream]')];
  const buttons = [...document.querySelectorAll('.ambient-toggle')];
  const visible = new Set();
  const update = () => {
    roots.forEach(root => root.classList.toggle('is-running', visible.has(root) && !ambientPaused && !preference.matches && !document.hidden));
    buttons.forEach(button => {
      button.hidden = false;
      button.disabled = preference.matches;
      button.textContent = preference.matches ? 'Reduced motion' : ambientPaused ? 'Play motion' : 'Pause motion';
      button.setAttribute('aria-label', `${button.textContent} · decorative animation`);
    });
  };
  const toggle = () => { ambientPaused = !ambientPaused; update(); };
  buttons.forEach(button => button.addEventListener('click', toggle));
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => entry.isIntersecting ? visible.add(entry.target) : visible.delete(entry.target));
    update();
  });
  roots.forEach(root => observer.observe(root));
  document.addEventListener('visibilitychange', update);
  preference.addEventListener('change', update);
  update();
  return () => {
    observer.disconnect();
    roots.forEach(root => root.classList.toggle('is-running', false));
    buttons.forEach(button => button.removeEventListener('click', toggle));
    document.removeEventListener('visibilitychange', update);
    preference.removeEventListener('change', update);
  };
}
let stopAmbient = mountAmbient();
window.addEventListener('pagehide', () => stopAmbient());
window.addEventListener('pageshow', event => { if (event.persisted) stopAmbient = mountAmbient(); });
