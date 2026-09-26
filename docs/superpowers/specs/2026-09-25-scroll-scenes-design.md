# Visible scroll scenes and protected hero text

Deliverable: both (source-backed findings and code). User chose stacked project panels in this task; Building proceeds here within the ongoing portfolio refinement.

## Reproduced

At an 884px viewport, reduced motion is off and the Motion bundle is active. The first featured story computed scale .986 and translateY 21px while the following stories remained at .95/76px. The effects run but are too small to read as section choreography; the thirteen-project directory has no comparable section animation. Hero paragraph width is 500px while its background protection is an ellipse scaled to the viewport, so dark images remain visible behind the ends of the text.

## Research and options

| Treatment | Mechanism | Fit here |
| --- | --- | --- |
| Entrance/reveal | IntersectionObserver triggers a short animation | Good for directory cards, insufficient as the main section effect |
| Scroll-linked parallax | Transform follows scroll progress | Useful supporting depth; too subtle alone |
| Tilt-to-flat / expanding image | Perspective and scale resolve as image enters | Good for screenshot entrances, while maintaining proportions |
| Stacked/pinned panels | CSS sticky or a pin controller holds one chapter while the next overlaps | Chosen for the three featured projects |
| Horizontal gallery | A pinned viewport translates a wide row with vertical scroll | Noticeable, but adds navigation friction to a scan-first portfolio |
| Text reveal | Words or lines reveal as they enter | Keep body copy immediately readable; not the main event |
| SVG path drawing / timeline | Stroke length tracks progress | Better suited to a true process diagram than unrelated projects |
| WebGL / video scrubbing | Rendered frames track scroll | Higher asset, performance and accessibility costs; not warranted for this correction |

Primary references:
- Motion scroll API: https://motion.dev/docs/scroll — progress-driven animations, offsets and cleanup; already installed in this static site.
- Motion examples: https://motion.dev/examples?category=scroll — parallax, image reveals, horizontal galleries and zoom scenes.
- GSAP ScrollTrigger: https://gsap.com/docs/v3/Plugins/ScrollTrigger/ — pinning, scrubbed timelines, snapping and viewport triggers. Strong alternative for a more complex timeline, but changing engines does not itself fix choreography.
- React Bits Scroll Stack: https://reactbits.dev/components/scroll-stack; reference implementation https://github.com/DavidHDev/react-bits/blob/main/src/content/Components/ScrollStack/ScrollStack.jsx — stack/scale pattern. Adapt the concept to existing vanilla HTML rather than introducing React and a second scroll controller.
- Aceternity Container Scroll: https://ui.aceternity.com/components/container-scroll-animation — perspective-to-flat screen treatment.
- 21st.dev visual browsing: https://21st.dev/community/components/explore/hero-scroll — selectable hero/scroll designs; inspect dependencies and adapt selected source to this site's stack.
- CSS scroll-driven animation guide: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations — native scroll/view timelines, with support/fallback considerations.
- Lenis: https://github.com/darkroomengineering/lenis — scroll smoothing, not a replacement for scene choreography. Keep native input here.
- Origin UI currently redirects to https://coss.com/ui — useful interface primitives, not the strongest source for this animation brief.

## Build

Preserve copy, screenshots, gallery controls and the accepted hero geometry. Protect the paragraph with an opaque paper-colored backing sized to its text box and softly feather its exterior. Use native sticky featured panels only if each fits the available viewport; previous panels recede as the next rises. On smaller/shorter screens retain ordinary document flow with screenshot entrances. Animate directory media and the lower visual chapter over a visible portion of the viewport. Never hide text or delay access to links. Honor reduced motion and clean up every scroll binding on remount. No public deployment.

## Validation

Check actual scroll positions and screenshots, not only presence of animation code. Confirm at least two positions for a pinned story, changing transform as the next approaches, and unobstructed hero text at desktop and narrow width. Check mobile flow, keyboard access, no overflow, gallery controls, cleanups and full build/test suite. Save Record evidence and local commit.

## Verified result

- At 1280×720 the first panel remained at y=48 while scrolling from 1440 to 1692; its scale changed from .960 to .929 as the following panel rose from y=392 to y=140. Screenshot captured the overlap.
- At 884×942 the entire hero paragraph remained legible over a paper-colored backing, including both ends beside dark screenshots.
- At 390×844 panels retained normal document flow with no horizontal overflow.
- Keyboard focus unstacked the panels; resizing with that focus retained the accessible layout. Added and passed a regression test for remounting with existing keyboard focus.
- Production build and all existing checks passed: 16 pages, links/media, privacy boundaries, image dimensions, galleries, analytics consent, video playback fallback, reduced motion and animation cleanup.
- Evidence retained in the private Portfolio Record. Local implementation complete; public release not performed in this pass.
