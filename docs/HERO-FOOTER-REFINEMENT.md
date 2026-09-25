# Hero, footer and contact privacy — September 25, 2026

Deliverable: code. Implemented and verified locally; public release remains pending.

## Scope and design

- Use the supplied perspective image-stream reference across the viewport, framing centered introductory copy. Keep real reviewed project screenshots and existing stories.
- Replace the oversized contact section and animated wordmark with a compact email/navigation footer.
- Remove personal telephone details from generated pages, the downloadable résumé and its preview.

## Implementation and evidence

The native CSS corridor uses perspective projection, geometric scale progression and mirrored rails. The central reading area stays stationary. Motion can be paused; the controller stops it offscreen, in background tabs and for reduced-motion preferences. No additional runtime dependency was introduced.

The shared footer is about 185px high at desktop size. Browser checks covered 1440×900, 1280×720 and 390×844, including no horizontal overflow and functional Pause control. The mobile hero occupies the first viewport beneath navigation. The existing automated suite passed across 16 generated pages, 13 projects, link/media integrity, playback, galleries, analytics gating and ambient motion behavior.

Phone rows were destructively redacted from the PDF, and its PNG preview regenerated and visually checked. Generated HTML has no telephone links. No public deployment occurred, so this does not claim removal from the existing live site or past repository history.

Evidence screenshots are attached to the Portfolio Record milestone “A full-screen hero and a quieter footer.”

## Next

Review the localhost preview. Publish the prepared release through the owner-run public release process, then verify the live hero/footer and directly fetch the résumé and preview to confirm the privacy changes are served.

## Follow-up: let the screenshots breathe

The hero now animates image elements directly at their native proportions, without a painted card, border, letterboxing or shadow. Seven screenshots are divided between the two rails instead of duplicating all seven on both sides. The cycle increased from 22 to 36 seconds; narrower images and a slightly tighter rail spread provide a longer interval where a whole screenshot fits on screen. This change applies only to the hero animation. Existing page galleries retain their layout.

## Follow-up: proportional, taller images

The previous Y-axis tilt combined with forward perspective widened projected screenshots near the viewport edges, even though their underlying layout ratios were correct. Removed the tilt so depth scaling remains uniform. Images are now sized from the hero height (60% desktop, 48% mobile before perspective), with a capped scale and an outward exit trajectory. The hero uses the existing taller SiteSift settings screenshot instead of its panoramic cover; galleries are unchanged. Browser measurements at 1440×900 and 390×844 matched source aspect ratios within 0.00002 and showed no horizontal overflow. The 36-second cycle, motion controls and frameless presentation remain.
