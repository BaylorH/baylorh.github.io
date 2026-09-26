// Native document scrolling drives visible product scenes. Text is never faded out.
export function mountSectionMotion({animate, scroll, root = document, desktop = true, viewportHeight = innerHeight}) {
  const disposers = [];
  function bind(element, frames, target, offset) {
    const animation = animate(element, {transform: frames}, {ease: 'linear'});
    const stop = scroll(animation, {target, offset});
    disposers.push(() => { stop(); animation.cancel(); element.style.removeProperty('transform'); });
  }
  const selected = root.querySelector('.selected-work');
  const stories = [...root.querySelectorAll('.featured-story')];
  const keyboardFocused = !!root.querySelector('.selected-work :focus-visible');
  if (selected && desktop && !keyboardFocused) selected.classList.add('has-scroll-scenes');
  // A panel that is taller than its viewport must never be trapped beneath the next.
  const fits = desktop && !keyboardFocused && stories.length > 1 && stories.every(panel => panel.offsetHeight <= viewportHeight - 96);
  if (!fits) selected?.classList.remove('has-scroll-scenes');
  if (selected) {
    const onKeyboardFocus = event => {
      if (event.target.matches(':focus-visible')) selected.classList.remove('has-scroll-scenes');
    };
    selected.addEventListener('focusin', onKeyboardFocus);
    disposers.push(() => {
      selected.classList.remove('has-scroll-scenes');
      selected.removeEventListener('focusin', onKeyboardFocus);
    });
  }
  stories.forEach((story, index) => {
    const next = stories[index + 1];
    if (fits && next) {
      story.style.transformOrigin = '50% 0%';
      bind(story, ['scale(1)', 'scale(.92)'], next, ['start end', 'start 64px']);
      disposers.push(() => story.style.removeProperty('transform-origin'));
    }
    const media = story.querySelector('.featured-media');
    if (media) bind(media,
      [desktop ? 'perspective(1100px) translateY(100px) rotateX(12deg) scale(.88)' : 'translateY(56px) scale(.94)', 'perspective(1100px) translateY(0px) rotateX(0deg) scale(1)'],
      story, ['start 95%', 'start 30%']);
  });
  // The directory is most of the page: give each image a visible, reversible arrival.
  root.querySelectorAll('.project-card').forEach((card, index) => {
    const media = card.querySelector('.visual-link');
    if (media) bind(media,
      [desktop ? `translateY(90px) rotate(${index % 2 ? 3 : -3}deg) scale(.88)` : 'translateY(48px) scale(.94)', 'translateY(0px) rotate(0deg) scale(1)'],
      card, ['start 98%', 'start 45%']);
  });
  root.querySelectorAll('[data-section-reveal], .case-visual').forEach(section => {
    bind(section, [desktop ? 'translateY(100px) scale(.86)' : 'translateY(40px) scale(.96)', 'translateY(0px) scale(1)'], section, ['start end', 'start 20%']);
  });
  const toolkit = root.querySelector('.toolkit');
  if (toolkit && desktop) root.querySelectorAll('.tool-layer').forEach((layer, index) => {
    const angle = [-3, 2, -1][index] ?? 0;
    bind(layer, [`translateY(${55 + index * 30}px) rotate(${angle * 4}deg)`, `translateY(0px) rotate(${angle}deg)`], toolkit, ['start 95%', 'center 55%']);
  });
  let disposed = false;
  return () => { if (disposed) return; disposed = true; disposers.forEach(dispose => dispose()); };
}
