# Portfolio refresh · September 24, 2026

Deliverable: code and a verified design/content finding.

## Direction
A personal engineering studio portfolio, using warm paper, charcoal typography, a restrained clay accent and visual system maps. The first screen explains what Baylor builds and gives direct access to projects. Business readers get outcomes first; technical readers can open capability and implementation details.

A cosmetic reskin would leave the missing work unresolved. An effects-heavy immersive site would obscure the work and add a maintenance burden. The selected direction is an editorial, responsive static portfolio with useful diagrams and restrained interaction.

## Implementation sequence
- Preserve the six existing project bodies and all source media under content/legacy; keep their original URLs.
- Store project descriptions and feature groups in content/projects.json; generate static HTML with tools/build.py. No browser-side dependency is needed for content.
- Build a shared header/footer, responsive project directory, working category filters, role/approach sections and clear contact routes.
- Add seven current case studies: FiftyFlowers, Till, Create Spaces, Axiom, SiteSift, AI Development Platform and AI Media Manager. Use the reviewed LinkedIn baseline; label visual maps as explanations, not application screenshots.
- Refresh existing case-study layouts while retaining prose, images, video and code examples. Mark historical snippets as historical references.
- Keep the résumé and recommendation downloads. Clearly date the old résumé instead of presenting it as current.
- Verify generated local links, image paths, original content retention, no-JavaScript content, keyboard filters/details, mobile layout and reduced motion. Commit locally and record evidence in the Portfolio Record.

## Acceptance and publication
All 13 project pages must be reachable from the homepage; all six historical URLs and their media must remain. Current descriptions must distinguish contribution, production use, MVP/beta, prototype and remaining work. No authenticated client data, credentials or private Record URLs enter the public-site candidate. No external form submissions. Public push and deployment require Baylor’s explicit approval of the finished preview; the agent can perform the technical release after that approval.

## Review result
- The generated site contains all 13 projects and preserves the original six URLs and active media. Original implementation is recoverable from the pre-refresh Git commit, not exposed as a new walkthrough.
- Automated checks cover 16 pages, media paths, fragment links, one main heading per page, archive recovery, and prohibited implementation content.
- Browser checks covered desktop and 390px phone layouts, all category filters, keyboard activation, feature disclosures, image expansion, Escape, focus restoration, and retained document links.
- Code review found standalone Pacman code blocks, source-archive publication risk and nested 404 URL resolution; all were corrected. The archive returns 404 from the packaged preview server.
- Mobile visual overlap was corrected. Reduced-motion styling and no-JavaScript content are included; no artificial loading transition blocks the content.
- Public deployment is still awaiting Baylor’s approval. The old résumé is deliberately marked May 2025, not rewritten during this website pass.
