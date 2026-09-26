# Career, navigation and directory polish

Deliverable: code and verification findings. September 2026.

## Scope
- Replace the outdated background page and downloadable résumé with a dated career timeline and current one-page PDF.
- Show company and education identity without publishing private contact details or old references.
- Preserve old links while making normal navigation use real directory routes.
- Align mixed project-preview types and show the full stacked-screen edges.
- Center the Approach panel when it fits; align its top when taller than the viewport.

## Sources and editorial decisions
The signed-in LinkedIn profile was read to verify dates and titles: Manifold Engineering (August 2024–present), FiftyFlowers (July 2025–present; AI Solutions Engineer from January 2026), WebMarkets (May–August 2024), ASU Computer Science (2021–2025, graduation May 2025). The previous PDF was read and visually reviewed before replacement.

Baylor supplied the FiftyFlowers customer-service annual savings figure of $24,000. This is owner-reported, not independently audited. Till’s existing savings claim is expressed annually throughout. Axiom copy explicitly distinguishes delivery leadership from implementation by collaborating developers. WebMarkets attribution distinguishes the independently built client portal from collaborative ALPHA SEO work.

`content/career.json` supplies both the web timeline and PDF. Generate the PDF with Python plus ReportLab (`tools/build_resume.py`); render and inspect the result after any change. ASU’s logo was obtained from the university’s organization identity shown on LinkedIn; it is used only to identify education.

## Verification
- One-page PDF rendered and inspected for readable text, spacing, clipping and current content.
- Full build and existing checks pass, including local links, privacy boundaries, image dimensions, motion lifecycle, video fallback and consent-gated analytics.
- Clean-route checks pass against both repository output and release output. Old `.html` links retain queries/fragments through compatibility redirects.
- Desktop and tablet directory measurements show equal media heights and matching title offsets (within a pixel of rounding). Mobile checks show no horizontal overflow, working filters and visible stacked-screen edges.
- Desktop and mobile career timeline inspected. Approach navigation handles tall layouts without clipping their top.
- Versioned changed styles and scripts prevent stale cached UI for returning visitors.

No product application data was changed. The old recommendation letter and its preview were removed from the published file set.
