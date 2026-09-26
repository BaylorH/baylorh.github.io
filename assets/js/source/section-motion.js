// Section choreography preserves native scrolling and never hides readable copy.
// The caller owns reduced-motion/viewport changes and disposes before remounting.
export function mountSectionMotion({animate, scroll, root = document, desktop = true}) {
  const disposers = [];
  function bind(element, frames, target, offset) {
    const animation = animate(element, {transform: frames}, {ease: 'linear'});
    const stop = scroll(animation, {target, offset});
    disposers.push(() => {
      stop();
      animation.cancel();
      element.style.removeProperty('transform');
    });
  }
  root.querySelectorAll('.featured-story, [data-section-reveal], .case-visual').forEach(section => {
    section.style.transformOrigin = '50% 15%';
    bind(section, [desktop ? 'translateY(76px) scale(.95)' : 'translateY(24px)', 'translateY(0px) scale(1)'], section, ['start end', 'start 25%']);
    disposers.push(() => section.style.removeProperty('transform-origin'));
  });
  const toolkit = root.querySelector('.toolkit');
  if (toolkit && desktop) {
    root.querySelectorAll('.tool-layer').forEach((layer, index) => {
      const restingAngles = [-3, 2, -1];
      const angle = restingAngles[index] ?? 0;
      bind(layer, [`translateY(${40 + index * 12}px) rotate(${angle * 3}deg)`, `translateY(0px) rotate(${angle}deg)`], toolkit, ['start 95%', 'center 55%']);
    });
  }
  const diagram = root.querySelector('.system-diagram');
  if (diagram && desktop) {
    root.querySelectorAll('.system-connector i').forEach(line => {
      bind(line, ['scaleX(.15)', 'scaleX(1)'], diagram, ['start 90%', 'center 55%']);
    });
  }
  let disposed = false;
  return () => {
    if (disposed) return;
    disposed = true;
    disposers.forEach(dispose => dispose());
  };
}
