# ALPHA SEO preview reliability

Deliverable: code. Local fix; public publishing remains pending.

## Reproduction

The homepage card displayed the illustration and “Pause preview” while the iframe had an empty body. The old controller removed and reassigned `src` on viewport/tab changes and treated requested playback as actual playback. A regression test observed four source changes during initialization and one leave/return cycle. Returning browser sessions also served the old controller after an ordinary reload.

## Change

- Keep the original YouTube video and iframe alive; use the official IFrame API after `onReady` to mute, play and pause.
- Set the embedding origin for the current host, including local preview. In-app playback remained blank without it during this session; subsequent origin-bearing loads played successfully. This is observed behavior, not proof of the browser's internal failure cause.
- Keep explicit pause and reduced-motion behavior; synchronize YouTube's own Play/Pause with the custom control.
- Show a direct original-video link if player initialization fails or exceeds 15 seconds; retain native controls.
- Version the controller URL from its contents so returning visitors receive the matching behavior.

## Verification

- Failing tests first: iframe reset count; stale script URL; native pause intent; unavailable-embed fallback. All subsequently pass.
- Full build and existing portfolio tests pass, including all 16 generated pages, 13 projects, historical sources, privacy boundaries, gallery dimensions/order and analytics gating.
- Chrome: case-study playback, reload and directory playback verified with actual advancing video time and muted audio.
- Codex in-app browser: case-study reload and repeated homepage reloads play the original video. Final run observed 0.032 seconds playing, 0.060 seconds paused offscreen, then 0.384 seconds playing on return without resetting the source.
- Explicit Pause survives leaving/returning to the card (paused at 7.585 seconds). Native YouTube pause and Play update the custom label and resume video.
- Reduced motion, delayed readiness, tab visibility, autoplay rejection/manual retry and player-error fallback are covered by the deterministic controller test.
- Focused code review identified native-control intent drift; fixed and regression-covered.

Reference: https://developers.google.com/youtube/iframe_api_reference

External video availability and browser autoplay policy remain dependencies. Manual playback/fallback is available when autoplay is unavailable. No public deployment, sharing or product data changes occurred.

## Follow-up: silent playback recovery

A ready player can fail to emit either PLAYING or an autoplay-blocked event. The new watchdog retries once after four seconds, then exposes manual Play after another four seconds instead of retaining Loading indefinitely. Tests cover this silent path, cancellation offscreen and native Play without a PAUSED acknowledgment. Fresh in-app reloads reached playback. See MOTION-POLISH-VERIFICATION.md for the accompanying UI pass.
