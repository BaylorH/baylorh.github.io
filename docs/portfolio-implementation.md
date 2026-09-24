# Complete portfolio refinement implementation plan

Deliverable: both. Execute inline in the existing isolated worktree; September 24 user approval covers the whole local build. Deployment remains a separate approval.

- [x] Homepage: extract the focused homepage template into tools/homepage.py; replace decorative orbit with three layered surfaces; create selected-work stories and retain full directory.
- [x] Motion: bundle only Motion animate/scroll into a local module. Hero entrance/pointer depth, short featured-visual scroll expansion; respond to reduced-motion preference changes and clean up listeners.
- [x] Browsing: interruptible directory reflow, instant keyboard filtering, active case-study contents, image inspection for actual case-study captures.
- [x] Styling: add scoped refinement stylesheet. Preserve typography legibility, media aspect ratios, mobile reading order and restrained brand colors. Avoid uniform effects on every block.
- [x] Analytics: optional configuration with production-domain gate, disabled by default until a verified measurement ID and consent choice. Document activation checks instead of pretending collection is active.
- [x] Verification: retained-route checker, selected-work/complete-directory invariants, motion bundle budget, desktop/phone screenshots, keyboard filtering, reverse scroll, dialogs and console errors; independent code review.
- [x] Record: verified evidence/results, local commit, completion status; open preview for full review.

Acceptance follows docs/portfolio-second-pass.md. Source edits rebuild generated HTML via tools/build.py; release packaging must include local motion bundle, new stylesheet and third-party license. No remote component runtime or private Record bundle shipped.


Review corrections:

| Before | After | Why |
| --- | --- | --- |
| Assumed dimensions for historical images | Source dimensions recorded for every image | Prevents image-load shifts |
| Low-contrast small captions | Darker meaningful labels | Keeps small text readable |
| Cancel then measure during filter reflow | Measure displayed positions before cancellation | Repeated clicks remain continuous |
| Array-based analytics command queue | Standard Arguments-based Google tag queue | Commands match the documented tag contract |
| Unspecified automatic analytics collection | Activation gate requires Enhanced Measurement review | Prevents automatic data collection exceeding the intended scope |

The analytics property itself is not configured and tracking remains inactive. Deployment is outside this local execution milestone. Final evidence and test results are recorded in The Record.
