# Portfolio second pass: interaction and visual direction

September 24, 2026. **This plan's deliverable: finding.** Research and design only; the existing local candidate remains unchanged. The subsequent implementation milestone delivers code and verified visual evidence. Production still requires explicit approval.

## Brief

- Preserve the clear positioning, all 13 project stories, the six original routes and their media.
- Make the opening and project browsing feel authored, dimensional and interactive.
- Serve prospective clients and recruiters first: purpose, contribution, outcome and maturity must remain immediately readable.
- Use contemporary libraries and component references selectively; keep implementation detail and private client information out of the public site.

## Audit and direction

The existing candidate establishes a useful content baseline but gives every project nearly equal weight. Its opening illustration is decorative rather than explanatory. The repeated cards, rules, small uppercase labels and warm accent create an overly familiar template rhythm. Adding entrance effects to every card would preserve these weaknesses.

Recommended direction: **an interactive engineering studio**. Keep the spacious light canvas and readable typography. Give one tangible composition in the opening the strongest motion; let the work that follows supply the variety. The headline should remain readable from first paint, without typewriter, blur or scrambled-text effects.

| Before | After | Why |
| --- | --- | --- |
| Three static notes in a decorative orbit | Layered input, application and outcome surfaces connect and settle into alignment during a short entrance; modest depth follows deliberate pointer movement | Demonstrates the business idea of connecting information to useful software |
| Thirteen similarly weighted cards immediately after the hero | Three larger featured stories, then the complete filterable directory | Provides a guided first impression while retaining breadth |
| Repeated small diagrams dominate every story | Different visual treatment appropriate to each story: public-safe product crop, clearly labeled illustration, or evidence figure | Makes the portfolio about actual work rather than a component kit |
| Filters appear/disappear abruptly | Brief position and opacity transitions; results remain immediately operable | Helps visitors understand what changed without delaying browsing |
| Case-study pages have the same static entrance | Wider visual opening, compact summary and desktop section index; image inspection preserves context | Supports both quick scanning and deeper reading |
| Many decorative labels and rules | Fewer labels, stronger spacing and explicit stage/contribution captions | Reduces visual noise without losing meaning |

## Alternatives considered

1. **Add motion to the current gallery.** Low effort, but insufficient hierarchy change; rejected as the main direction.
2. **Interactive studio with selected stories. Recommended.** One signature opening, useful image expansion, then familiar browsing. Fits the audience and existing static delivery.
3. **Full-screen 3D / horizontal scroll narrative.** More theatrical, but makes comparing work and finding contact harder. Reserve a standalone interactive demo for a future project where the interaction itself is evidence.

## Page storyboard

1. **Arrival:** identity and headline visible immediately. On capable devices the hero's three surfaces settle over approximately 600 ms, with overlapping timing. No overlay or loading delay. Faces show “Information”, “Applications”, “Better decisions”; connections are illustrative, not a private architecture diagram.
2. **First scroll:** the hero's depth gently flattens while the first featured visual opens toward its final width. Use a short viewport-relative range, not multiple screenfuls of pinned scrolling. Copy stays outside moving/cropped media.
3. **Selected work:** FiftyFlowers (breadth of business applications), Till (decision support and the strongest reviewed outcome), and the AI Development Platform (engineering practice). Each has one purpose sentence, contribution, accurate stage, visual and case-study link. These are selections, not chronological steps. Keep the platform story public-facing and high level.
4. **Explore:** the full 13-project directory remains reachable directly from the top navigation. Use compact filters and measured reflow. Case-study links remain ordinary links, with browser history and open-in-new-tab behavior intact.
5. **Understand / contact:** the existing approach, background and contact flow stays quiet. On long case studies, a sticky desktop index helps readers jump between purpose, contribution, evidence and stage; on phones use a compact in-flow contents list.

## Visual system

Retain paper #F5F3ED, ink #252922 and white #FFFFFF. Use muted slate #607482 for dimensional surfaces and soft sage #D8DDCE for secondary surfaces. Reduce clay #B8482B to small identity accents rather than emphasizing headline words. These are proposed refinements, not a mandatory wholesale recolor.

Keep DM Sans for reading and navigation. Use DM Serif Display only where it creates a clear typographic role; avoid the default italic last word of a headline. Limit IBM Plex Mono to genuine figure/data labels. Body lines should generally stay around 60–75 characters. Align text left; vary visual widths and whitespace according to hierarchy.

Use layered HTML/CSS surfaces with perspective, soft shadows and restrained highlights for the hero. Real 3D is not necessary to create the proposed shallow depth. Pointer tilt max roughly 3 degrees and 6 px travel; no custom cursor, magnetic button that moves away, or interaction required to reveal text.

## Research and implementation choice

| Source | Suitable use | Decision / limits |
| --- | --- | --- |
| [Motion JavaScript scroll](https://motion.dev/docs/scroll) | Scroll-linked transforms, short entrance orchestration, interaction feedback | Preferred runtime. Works with the existing JavaScript site; use CSS sticky where needed. Pin the chosen package version and measure the actual shipped bundle. |
| [GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) | Complex synchronized timelines, scrubbing and pinning | Strong alternative if the hero prototype proves Motion insufficient. Do not ship two animation engines to implement the same behavior. |
| [React Bits Scroll Expand](https://reactbits.dev/animations/scroll-expand) | A framed visual expanding as it enters focus | Inspected the live demo before/after scroll. Adapt the framing idea to featured work, with text outside media. The demo's text contrast during motion should not be reproduced. |
| [React Bits Scroll Stack](https://reactbits.dev/components/scroll-stack) | Layered depth between stories | Inspected live initial and stacked states. Borrow limited depth, not the nested scroll container or content occlusion. Keep all three stories independently readable. |
| [21st.dev](https://21st.dev/) | Component discovery and composition references | A catalog of authored components, not one universal runtime. Check source, license and dependencies on the exact selected item. Many expect React/Tailwind; avoid a framework migration solely to copy a treatment. |
| [Origin UI](https://github.com/shadcn/originui) | Navigation, tabs, disclosure and dialog detailing | Likely the “origin kit” reference; exact intended product is unconfirmed. React/Tailwind primitives are useful references, but the current native links/details/dialog remain the starting point. |
| [Lenis](https://github.com/darkroomengineering/lenis) | Optional scroll smoothing and animation synchronization | Defer. Native scrolling first; add only if an actual device comparison shows a benefit. Review anchor, modal and nested-scroll behavior if introduced. |

No new dependency, MCP service, paid generation or global skill was installed during research. Public demo observation does not prove production performance or accessibility.

## Skills reviewed

Existing brainstorming, design-engineering, planning and verification guidance covers this work. Skill discovery also reviewed the [skills leaderboard](https://www.skills.sh/) and the first-party [Anthropic frontend-design source](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md). Its focus on one memorable element, meaningful hierarchy and avoiding default visual tropes directly informs this plan. Discovery popularity is not a quality guarantee.

The [official 21st CLI skill](https://github.com/21st-dev/skill/blob/main/skills/21st-cli-use/SKILL.md) was inspected. It is useful for catalog retrieval when an exact component is selected; it is not an aesthetic decision-maker. It distinguishes metadata discovery, metered source retrieval and separate hosted generation. No credentials or project data were sent to it. Install only when retrieval actually helps implementation, after checking the current contract.

## Bounded implementation sequence

1. Adjust shared template hierarchy and featured-story data in `tools/build.py` and `content/projects.json`. Preserve complete project directory and original URLs.
2. Build the hero and first featured story as the motion reference. Compare a static, native-scroll version against Motion enhancement before extending the treatment. Verify geometry at 1440, 1024 and 390 px.
3. Apply the approved interaction language to the other two selected stories, directory filtering and case-study index. Keep unrelated content and historical media intact.
4. Bundle only required animation APIs into local assets, preserve license notices, and package through the existing static build. Add graceful fallback if the animation code fails to load.
5. Capture desktop and phone evidence, inspect slow scroll, fast scroll, reverse scroll and repeated filtering. Fix visual quality and usability issues before requesting release approval.

## Acceptance and evidence

- Every headline, case-study link and contact path works with JavaScript disabled. No pre-animation CSS leaves essential content hidden on failure.
- Reduced motion uses static final compositions and immediate state changes; no scroll-bound zoom, perspective or parallax. Touch gets a stable layout without hover dependencies.
- Native scroll, keyboard navigation, browser back/forward, anchor jumps and new-tab links work. Image dialogs preserve focus and Escape behavior.
- No layout jumps caused by image loading. Declare media dimensions; avoid upscaling tiny evidence images into full-width heroes.
- Proposed budget: at most 35 KB gzip of additional motion JavaScript, no video auto-download, no continuous offscreen animation and no added animation-driven long tasks in tested interactions. Measure before claiming these targets pass.
- Target 60 fps on the measured desktop/phone environments, while recognizing low-end hardware can differ. Check frame traces, layout shifts and input responsiveness, not merely whether an effect runs.
- Verify 13 stories, all original routes/media, current facts/stages, mobile overflow, broken links and public-content boundaries with the existing checks plus focused interaction tests.
- Record screenshots or short motion evidence, actual device/browser sizes, measurements, remaining issues and the reviewed commit. Distinguish implemented locally from deployed publicly.

## Current checkpoint

Research and second-pass design are complete. Implementation is next; this document does not claim the new interactions exist. First candidate remains at local commit 7fd36bd. Public site unchanged.

## Contact, imagery and measurement amendment

The local candidate now uses the Manifold business email throughout generated contact links and in the retained résumé/PDF preview. The résumé's experience content remains May 2025; only its contact information has been refreshed.

Record evidence reviewed for the next pass includes the current Internal AI support screen and the saved Brain graph. The empty Internal AI form is now used in the homepage directory and FiftyFlowers case study, with an accurate caption. Existing Till and Create Spaces company marks are now displayed on their case studies against a dark background so their white artwork remains legible. The Brain screenshot is not copied into the public package: its internal labels need a separately reviewed presentation first. Avoid exporting whole Record assets merely to obtain a screenshot; preserve source provenance in the authenticated Record and copy only the reviewed image.

Hosting decision: keep GitHub Pages. Visitor analytics does not require Firebase Hosting. [Google's tag supports static HTML sites](https://developers.google.com/analytics/devguides/collection/ga4/tag-options); [Plausible also installs through a site-specific script](https://plausible.io/docs/plausible-script). A migration would add domain/release work without improving the current static portfolio.

Recommended initial analytics scope: GA4 page visits, referral sources, popular case studies, and contact-link/document clicks. The dashboard should distinguish aggregate visits from leads: a contact-link click is not proof of a message or inquiry. No session recordings, form contents, personal identifiers or arbitrary URL query values in custom events. Exclude local previews and avoid duplicate page views. Configure measurement/consent behavior as part of the release setup and validate actual collection on the approved production domain. No analytics property or measurement ID is configured in this candidate yet; tracking is not active. A paid alternative or hosting migration is not needed to complete the design.
