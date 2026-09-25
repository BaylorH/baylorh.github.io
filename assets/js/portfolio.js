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

// Retain the embed across scrolling: destroying it can cancel YouTube startup.
// Playback commands wait for the official API's readiness event.
let youtubeAPI;
function loadYouTubeAPI() {
  if (window.YT?.Player) return Promise.resolve(window.YT);
  if (!youtubeAPI) youtubeAPI = new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('Player unavailable')), 15000);
    window.onYouTubeIframeAPIReady = () => { clearTimeout(timeout); resolve(window.YT); };
    const script = document.createElement('script');
    script.src = 'https://www.youtube.com/iframe_api';
    script.onerror = () => { clearTimeout(timeout); reject(new Error('Player unavailable')); };
    document.head.append(script);
  });
  return youtubeAPI;
}
for (const root of document.querySelectorAll('[data-video-preview]')) {
  const frame = root.querySelector('iframe');
  const button = root.querySelector('.video-toggle');
  const fallback = root.querySelector('.video-fallback');
  const embedURL = new URL(frame.src);
  embedURL.searchParams.set('origin', location.origin);
  frame.src = embedURL.href;
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  let visible = false;
  let paused = preference.matches;
  let playing = false;
  let ready = false;
  let playRequested = false;
  let pausing = false;
  let player;
  let playbackTimeout;
  const wantsPlayback = () => visible && !paused && !document.hidden;
  function label() {
    button.textContent = paused ? 'Play preview' : playing ? 'Pause preview' : 'Loading preview…';
    button.setAttribute('aria-label', `${button.textContent} · ALPHA SEO`);
  }
  function stopPlaybackWatch() { clearTimeout(playbackTimeout); playbackTimeout = undefined; }
  function watchPlayback(retried = false) {
    stopPlaybackWatch();
    playbackTimeout = setTimeout(() => {
      playbackTimeout = undefined;
      if (!wantsPlayback() || playing) return;
      if (!retried) { player.mute(); player.playVideo(); watchPlayback(true); }
      else { paused = true; playRequested = false; pausing = false; player.pauseVideo(); label(); }
    }, 4000);
  }
  function update() {
    if (ready) {
      if (wantsPlayback()) { playRequested = true; player.mute(); player.playVideo(); if (!playing && !playbackTimeout) watchPlayback(); }
      else { stopPlaybackWatch(); pausing = playing || playRequested; player.pauseVideo(); }
    }
    label();
  }
  // If the API cannot load, retain YouTube's own play/error controls.
  const nativeFallback = () => { stopPlaybackWatch(); button.hidden = true; frame.hidden = false; fallback.hidden = false; };
  const startupTimeout = setTimeout(nativeFallback, 15000);
  button.hidden = false;
  label();
  button.addEventListener('click', () => { paused = !paused; update(); });
  preference.addEventListener('change', () => { paused = preference.matches; update(); });
  document.addEventListener('visibilitychange', update);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => { visible = entries[0].isIntersecting; update(); }, { threshold: .15 }).observe(root);
  } else { visible = true; update(); }
  loadYouTubeAPI().then(YT => {
    player = new YT.Player(frame, {
      events: {
        onReady() { clearTimeout(startupTimeout); ready = true; button.hidden = false; fallback.hidden = true; update(); },
        onStateChange(event) {
          playing = event.data === 1;
          if (playing) {
            stopPlaybackWatch();
            // Honor native Play as user intent, but finish pending automatic pauses.
            if (!visible || document.hidden || (pausing && paused)) player.pauseVideo();
            else { paused = false; pausing = false; }
          } else if (event.data === 2) {
            stopPlaybackWatch();
            if (!pausing && visible && !document.hidden) paused = true;
            pausing = false; playRequested = false;
          }
          label();
        },
        onAutoplayBlocked() { stopPlaybackWatch(); paused = true; playing = false; label(); },
        onError() { clearTimeout(startupTimeout); nativeFallback(); }
      }
    });
  }).catch(() => { clearTimeout(startupTimeout); nativeFallback(); });
}

// Screen changes are deliberate, scoped to one gallery, and never auto-advance.
for (const gallery of document.querySelectorAll('[data-screen-gallery]')) {
  const shots = [...gallery.querySelectorAll('.screen-shot')];
  const buttons = [...gallery.querySelectorAll('[data-screen-index]')];
  const controls = gallery.querySelector('.screen-controls');
  controls.hidden = false;
  function select(index) {
    shots.forEach((shot, i) => {
      shot.classList.toggle('is-front', i === index);
      shot.classList.toggle('is-back', i === (index + 1) % shots.length);
      shot.classList.toggle('is-third', gallery.classList.contains('is-portrait') && i === (index + 2) % shots.length);
      shot.tabIndex = i === index ? 0 : -1;
      shot.setAttribute('aria-hidden', String(i !== index));
      buttons[i].setAttribute('aria-pressed', String(i === index));
    });
    gallery.querySelector('.screen-count').textContent = `${index + 1} / ${shots.length}`;
    const caption = gallery.querySelector('.screen-caption');
    if (caption) caption.textContent = buttons[index].dataset.caption;
  }
  buttons.forEach((button, index) => {
    button.addEventListener('click', () => select(index));
    button.addEventListener('keydown', event => {
      const offset = event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0;
      if (!offset) return;
      event.preventDefault();
      const next = (index + offset + shots.length) % shots.length;
      select(next); buttons[next].focus();
    });
  });
}
