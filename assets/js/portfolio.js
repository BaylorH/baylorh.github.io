// Content and navigation work without JavaScript; this layer adds filtering and image inspection.
const filters = document.querySelector(".filters");
if (filters) {
  filters.hidden = false;
  const cards = [...document.querySelectorAll("[data-category]")];
  const count = document.querySelector(".project-count");
  filters.addEventListener("click", (event) => {
    const button = event.target.closest("[data-filter]");
    if (!button) return;
    filters
      .querySelectorAll("button")
      .forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
    const motionAllowed = event.detail > 0 && !matchMedia('(prefers-reduced-motion: reduce)').matches;
    const previous = new Map(cards.filter(card => !card.hidden).map(card => [card, card.getBoundingClientRect()]));
    cards.forEach(card => card.getAnimations().forEach(animation => animation.cancel()));
    cards.forEach((card) => {
      card.hidden =
        button.dataset.filter !== "all" &&
        card.dataset.category !== button.dataset.filter;
    });
    if (motionAllowed) cards.filter(card => !card.hidden).forEach(card => {
      const before = previous.get(card);
      const after = card.getBoundingClientRect();
      card.animate(before ? [
        { transform: `translate(${before.left-after.left}px,${before.top-after.top}px)` },
        { transform: 'translate(0,0)' }
      ] : [{ opacity: .35, transform: 'translateY(8px)' }, { opacity: 1, transform: 'translateY(0)' }],
      { duration: 250, easing: 'cubic-bezier(.22,1,.36,1)' });
    });
    const visible = cards.filter((card) => !card.hidden).length;
    count.textContent = `${visible} ${visible === 1 ? "project" : "projects"}`;
  });
}
const viewer = document.querySelector("#image-viewer");
if (viewer && typeof viewer.showModal === "function") {
  let trigger;
  document.querySelectorAll(".legacy-content img, .case-visual .image-visual img, .product-screens img").forEach((image) => {
    if (image.closest("a")) return;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "image-expand";
    button.setAttribute("aria-label", `Expand ${image.alt || "project image"}`);
    image.replaceWith(button);
    button.append(image);
    button.addEventListener("click", () => {
      trigger = button;
      viewer.querySelector("img").src = image.src;
      viewer.querySelector("img").alt = image.alt;
      const caption = image.closest("figure")?.querySelector("figcaption")
        || image.closest(".case-visual")?.querySelector(".image-caption");
      viewer.querySelector("p").textContent = caption?.textContent?.trim() || image.alt;
      viewer.showModal();
    });
  });
  viewer
    .querySelector("button")
    .addEventListener("click", () => viewer.close());
  viewer.addEventListener("click", (event) => {
    if (event.target === viewer) viewer.close();
  });
  viewer.addEventListener("close", () => trigger?.focus());
}

// Keep the contents index useful while reading; do not move focus on scroll.
const contentsLinks = [...document.querySelectorAll('.case-aside > a[href^="#"]')];
const sections = contentsLinks.map(link => document.getElementById(link.hash.slice(1))).filter(Boolean);
if (sections.length) {
  let queued = false;
  const update = () => {
    queued = false;
    const active = [...sections].reverse().find(section => section.getBoundingClientRect().top <= 150) || sections[0];
    contentsLinks.forEach(link => {
      if (link.hash === `#${active.id}`) link.setAttribute('aria-current','location');
      else link.removeAttribute('aria-current');
    });
  };
  window.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(update); } }, { passive: true });
  update();
}

// Play historical previews only in view; preserve explicit pause and reduced-motion choices.
for (const root of document.querySelectorAll('[data-video-preview]')) {
  const frame = root.querySelector('iframe');
  const button = root.querySelector('.video-toggle');
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const base = new URL(frame.src);
  let visible = false;
  let paused = preference.matches;
  let playing = false;
  function update() {
    const shouldPlay = visible && !paused && !document.hidden;
    if (shouldPlay !== playing) {
      playing = shouldPlay;
      frame.hidden = !playing;
      if (playing) {
        const url = new URL(base); url.searchParams.set('autoplay', '1');
        frame.src = url.href;
      } else frame.removeAttribute('src');
    }
    button.textContent = paused ? 'Play preview' : 'Pause preview';
    button.setAttribute('aria-label', `${paused ? 'Play' : 'Pause'} ALPHA SEO preview`);
  }
  frame.removeAttribute('src'); frame.hidden = true; button.hidden = false;
  button.addEventListener('click', () => { paused = !paused; update(); });
  preference.addEventListener('change', () => { paused = preference.matches; update(); });
  document.addEventListener('visibilitychange', update);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => { visible = entries[0].isIntersecting; update(); }, { threshold: .15 }).observe(root);
  } else { visible = true; update(); }
}
