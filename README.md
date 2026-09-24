# Baylor Harrison portfolio

A static portfolio with 13 case studies, responsive layouts and a small progressive-enhancement layer. Content is readable without JavaScript. All existing project URLs and images remain available.

## Edit and preview

- Edit project descriptions in `content/projects.json`.
- Edit shared templates in `tools/build.py`, styles in `assets/css/portfolio.css`, and interactions in `assets/js/portfolio.js`.
- Run `python3 tools/build.py` then `python3 tools/check.py`.
- Run `python3 tools/package.py` to build the clean `dist` release.
- Preview with `python3 -m http.server 8908 --bind 127.0.0.1 --directory dist`.

Historical project bodies are retained in baseline commit `b5e19c2`. The build recovers exact local copies under ignored `content/legacy` when needed (use a full-history checkout). Those files include original implementation examples and are not website content. The public presentation keeps the project explanations and media, not those source-code recipes. The packaged release excludes build sources, research notes and archives. `_config.yml` also excludes them from the existing GitHub Pages branch build.

## Release

The currently configured public host is GitHub Pages, main branch, repository root, with `baylor-harrison.com` as the custom domain. Do not push or deploy until Baylor explicitly approves the current candidate. After approval, the agent can perform the technical release, preserve the domain configuration, and verify the deployed result. Never publish the entire working directory to a generic static host; use `dist`.

The retained résumé PDF is dated May 2025 and is visibly labeled accordingly. LinkedIn is the current professional baseline; updating the résumé itself is separate work. Current scope, decisions, verification and release status belong in the Portfolio website Record.

## Content conventions

Start with the business problem, describe the individual contribution, then state the result or maturity. Group related products; distinguish working systems, MVPs, betas and prototypes. Illustrations are labeled as capability overviews, not production screenshots. Keep client records, internal prompts and detailed implementation out of the showcase.


## Refined portfolio build

Install pinned build dependencies with `npm ci`, then run `npm run build` and `npm test`. The generated HTML remains directly readable without JavaScript. Motion is bundled locally; its license file is included in the release. Homepage composition lives in `tools/homepage.py`, styles in `assets/css/refinement.css`, and motion source in `assets/js/source/motion.js`. The original six project routes and historical media remain.

### Optional visitor analytics

Tracking is **off** in the review candidate. Hosting remains GitHub Pages. Before activation, configure a GA4 web stream for the public domain and disable Enhanced Measurement (automatic clicks, site search, downloads and other automatic events). Review the property's data-sharing and retention settings. Set `PORTFOLIO_ANALYTICS_ID` to the verified measurement ID and `PORTFOLIO_ANALYTICS_REVIEWED=true` when building the approved release. These flags do not establish consent by themselves.

On the configured production hostname only, visitors can allow or decline analytics. No Google script is requested before opt-in; the settings button can disable subsequent collection. Local previews and an empty measurement ID stay inactive. Events are limited to page views and project, contact and document clicks, with query strings removed from configured page location and only the referring origin retained. A contact click is not a completed inquiry.

Verify actual outgoing requests after the approved production release, including opt-out behavior and no automatic Enhanced Measurement payloads. Unit checks validate the loader contract, not Google's live property configuration. Add the private analytics dashboard link to the authenticated portfolio Record once the property exists; do not make analytics reports public.
