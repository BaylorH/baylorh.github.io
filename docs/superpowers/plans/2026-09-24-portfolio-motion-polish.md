# Portfolio motion and media polish

Deliverable: code. Execute locally in this task under the user's standing instruction to plan in the Record, build, verify and present a finished preview. Public publishing remains pending.

## Intent

Preserve the portfolio's content, professional cream/sage identity, real product screenshots and project hierarchy. Improve the visual opening, scroll rhythm and closing; remove the machine-learning menu image everywhere rendered. Recheck the reported ALPHA startup failure rather than assuming last turn resolved every path.

## Design decision

| Before | After | Why |
| --- | --- | --- |
| Abstract hero software illustration | Slow 3D corridor of reviewed product screenshots beside the existing headline | The supplied Image Stream Hero concept demonstrates real work immediately |
| Flat background and limited scroll cues | Fine contour lines, softly lit cream/sage surfaces and measured text/media reveals | Add depth and pacing without reducing content legibility |
| Generic closing CTA | Dark forest contact section, large type, subtle moving contour and grouped navigation | Make a deliberate final impression and keep contact straightforward |
| ML menu screenshot in preview and legacy article | Only the actual interactive 3D classifier screen | Menus do not demonstrate the product |
| Potential video startup stall | Re-test fresh reload + scroll, add bounded recovery for confirmed startup gaps | Avoid an indefinite placeholder/loading state |

## References and access

- User-supplied 21st Image Stream Hero source: geometric apparent-size corridor, opposing rails, negative animation delays. Adapt geometry to native HTML/CSS and landscape product images; no stock photos and no React/Tailwind migration.
- https://reactbits.dev/text-animations/scroll-reveal — reviewed live demo/controls. Adapt restrained scroll-linked text opacity using the existing Motion runtime; keep readable base opacity, no body-copy blur.
- https://reactbits.dev/backgrounds/silk — reviewed live visual. Borrow soft directional lighting, not its React/Three dependency stack or bright purple palette.
- https://docs.21st.dev/blog/react-footer-design-examples — examined curtain/oversized-type footer patterns. Build an original in-flow reveal so keyboard/touch navigation is reliable.
- https://www.originkit.dev/ and /components/light-curtain — reviewed catalogue and public descriptions. Pro prompt prevented component preview/source access. No premium code copied or access bypass attempted.

## Implementation

1. Add focused build/render checks for removal of ML menu, real hero sources, usable footer links and motion fallback.
2. `tools/atmosphere.py`: generate deterministic corridor keyframes and semantic hero/footer markup. `tools/homepage.py`: use new hero media with existing copy. `tools/build.py`: shared footer and stylesheet, version modified assets, filter excluded ML legacy image without altering archived source.
3. `assets/css/atmosphere.css`: responsive stream composition, cream contour background, dark footer and reduced-motion/static states. Keep imagery legible, no cursor hijacking or scroll locks.
4. `assets/js/source/motion.js`: readable scroll text, staged media arrival and footer reveal. Stop loops offscreen/background; expose Pause motion for continuous decorative animation; respect reduced motion and cleanup.
5. `content/projects.json`: remove ML menu screenshot and explicitly suppress original menu in rendered legacy content; preserve archive/source file.
6. Re-test ALPHA on current version in normal reload/scroll and delayed readiness conditions. Fix proven gaps with regression tests before implementation.
7. Build/check, inspect desktop and phone, exercise controls, reduced-motion lifecycle tests and all 13 project links. Commit source/generated pages; update existing Portfolio Record with evidence and limitations, then open preview.

## Guardrails

No external forms/messages, new audiences, public deployment or product changes. No new runtime dependencies. Retain reviewed redactions and accurate maturity captions. CSS/JS failure leaves content readable; reduced motion produces a finished still. Never hide project content until a scroll event fires.
