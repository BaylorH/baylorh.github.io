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
