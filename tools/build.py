"""Generate the portfolio as portable, crawlable static HTML."""
from pathlib import Path
from html import escape as e
import json, re, subprocess, os, hashlib
from screen_gallery import preview_screens, screen_gallery
ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_HASH = hashlib.sha256((ROOT/'assets/js/portfolio.js').read_bytes()).hexdigest()[:12]
PROJECTS = json.loads((ROOT/'content/projects.json').read_text())
# Original source is recoverable from the committed baseline; local copies never ship.
legacy_dir=ROOT/'content/legacy'
legacy_dir.mkdir(exist_ok=True)
for legacy_name in [p['id'] for p in PROJECTS if p.get('legacy')]+['resume']:
 target=legacy_dir/f'{legacy_name}.html'
 if not target.exists():
  source=subprocess.check_output(['git','show',f'b5e19c2:{legacy_name}.html'],cwd=ROOT,text=True)
  target.write_text(re.search(r'<section class="post">(.*?)</section>',source,re.S).group(1))
SITE = 'https://baylor-harrison.com'
EMAIL = 'baylor@manifoldengineering.ai'
ANALYTICS_ID = os.environ.get('PORTFOLIO_ANALYTICS_ID', '')
if ANALYTICS_ID and os.environ.get('PORTFOLIO_ANALYTICS_REVIEWED') != 'true':
 raise ValueError('Review the analytics property and disable Enhanced Measurement before activation')
if ANALYTICS_ID and not re.fullmatch(r'G-[A-Z0-9]+', ANALYTICS_ID):
 raise ValueError('PORTFOLIO_ANALYTICS_ID must be a valid GA4 measurement ID')

def header(active=''):
 return f'''<a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="index.html" aria-label="Baylor Harrison home"><span class="brand-mark">bh<span>·</span></span><span>Baylor Harrison<small>Engineer & builder</small></span></a><nav aria-label="Main navigation"><a href="index.html#work" {'aria-current="page"' if active=='work' else ''}>Work</a><a href="index.html#approach">Approach</a><a href="resume.html" {'aria-current="page"' if active=='resume' else ''}>Background</a><a class="contact-link" href="mailto:{EMAIL}">Let’s talk <span aria-hidden="true">↗</span></a></nav></header>'''

def footer():
 from atmosphere import footer as contact_footer
 return contact_footer(EMAIL)

def page(title,description,body,path,active=''):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f5f3ed"><meta name="analytics-id" content="{ANALYTICS_ID}"><title>{e(title)} · Baylor Harrison</title><meta name="description" content="{e(description)}"><link rel="canonical" href="{SITE}/{path}"><meta property="og:title" content="{e(title)} · Baylor Harrison"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE}/{path}"><meta property="og:image" content="{SITE}/images/portfolio-social.png"><link rel="icon" type="image/svg+xml" href="images/portfolio-mark.svg"><link rel="stylesheet" href="assets/css/portfolio.css"><link rel="stylesheet" href="assets/css/refinement.css"><link rel="stylesheet" href="assets/css/atmosphere.css?v={hashlib.sha256((ROOT/'assets/css/atmosphere.css').read_bytes()).hexdigest()[:12]}"><script defer src="assets/js/portfolio.js?v={CONTROLLER_HASH}"></script><script defer src="assets/js/analytics.js"></script><script type="module" src="assets/js/motion.js?v={hashlib.sha256((ROOT/'assets/js/motion.js').read_bytes()).hexdigest()[:12]}"></script></head><body>{header(active)}<main id="main">{body}</main>{footer()}<dialog id="image-viewer" aria-label="Expanded project image"><button type="button" class="viewer-close" aria-label="Close image">Close ×</button><img alt=""><p></p></dialog></body></html>'''

def visual(p,large=False,layered=False):
 if not large and not p.get("videoId") and len(preview_screens(p))>1:
  return screen_gallery(p,layered)
 if p.get('videoId'):
  video=e(p['videoId']); fallback=visual({k:v for k,v in p.items() if k!='videoId'},large)
  caption=f'<p class="image-caption">{e(p["videoCaption"])}</p>' if large else ''
  return f'<div class="video-preview" data-video-preview data-video-id="{video}"><div class="video-poster">{fallback}</div><iframe src="https://www.youtube-nocookie.com/embed/{video}?enablejsapi=1&amp;mute=1&amp;loop=1&amp;playlist={video}&amp;playsinline=1" title="{e(p["name"])} original product demonstration" allow="autoplay; encrypted-media; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe><button type="button" class="video-toggle" hidden>Pause preview</button><a class="video-fallback" hidden href="https://www.youtube.com/watch?v={video}" target="_blank" rel="noopener">Watch original video ↗</a></div>'+caption
 if p.get('image'):
  caption = f'<p class="image-caption">{e(p["imageCaption"])}</p>' if large and p.get('imageCaption') else ''
  return f'<div class="project-visual {p["color"]} image-visual"><img src="{p["image"]}" alt="{e(p.get("imageAlt", p["name"] + " — original project screen"))}" loading="lazy" width="{p.get("imageWidth",1200)}" height="{p.get("imageHeight",800)}"></div>'+caption
 v=p.get('visual'); color=p['color']
 if v=='flowers':
  inner='<span class="visual-kicker">FIFTYFLOWERS / INTERNAL AI</span><div class="flower-symbol" aria-hidden="true">✳</div><div class="visual-title">One workspace.<br>Many possibilities.</div><div class="app-chips"><span>Customer support</span><span>Image tools</span><span>Company knowledge</span></div>'
 elif v=='till':
  inner='<span class="visual-kicker">TILL / LENDING INTELLIGENCE</span><div class="score-orbit" aria-hidden="true"><span></span><span></span><span></span><b>till.</b></div><div class="visual-bottom"><span>Applications → Scoring → Insight</span><strong>$24k<small>annualized savings</small></strong></div>'
 elif v=='platform':
  inner='<span class="visual-kicker">THE DEVELOPMENT WORKSPACE</span><div class="platform-stack"><div><span>01</span><b>The Record</b><small>Project management</small></div><div><span>02</span><b>Brain</b><small>Engineering memory</small></div><div><span>03</span><b>Jarvis OS</b><small>Agent orchestration</small></div></div>'
 elif v=='reports':
  inner='<span class="visual-kicker">CREATE SPACES / REPORTING</span><div class="report-art"><div class="paper"><span>BOOKINGS</span><i></i><i></i><i></i><i></i><b>From report</b></div><div class="answer"><span>→</span><b>to understanding.</b><small>Data, ready for a conversation.</small></div></div>'
 elif v=='axiom':
  inner='<span class="visual-kicker">AXIOM / ENGINEERING CONTEXT</span><div class="axiom-art" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div class="visual-bottom"><span>Past projects.<br>Better context.</span><b class="wordmark">axiom</b></div>'
 elif v=='sitesift':
  inner='<span class="visual-kicker">SITESIFT AI / PROPERTY RESEARCH</span><div class="property-grid" aria-hidden="true">'+''.join('<i></i>' for _ in range(18))+'</div><div class="visual-title low">The search,<br>in context.</div>'
 elif v=='media':
  inner='<span class="visual-kicker">AI MEDIA MANAGER / RESEARCH</span><div class="media-art" aria-hidden="true">'+''.join(f'<i class="m{i}"></i>' for i in range(6))+'</div><div class="media-label">Collect. Organize. Explore.</div>'
 else:
  inner='<span class="visual-kicker">ALPHA SEO / DIGITAL AGENCY</span><div class="seo-art" aria-hidden="true"><span>α</span><div><i></i><i></i><i></i><i></i></div></div><div class="visual-bottom">A clearer view of search.</div>'
 return f'<div class="project-visual {color} {"large" if large else ""}" role="img" aria-label="{e(p["name"])} illustrated capability overview">{inner}<span class="map-label">Illustrated overview</span></div>'

def brand_art(p, context, decorative=False):
 if not p.get('logo'):return ''
 kind=p.get('logoKind','wordmark')
 label='' if decorative or kind=='icon' else p['name']
 image=f'<img src="{e(p["logo"])}" alt="{e(label)}" width="{p["logoWidth"]}" height="{p["logoHeight"]}" loading="lazy">'
 # A product icon remains an icon; its readable product name is separate text.
 name=f'<span>{e(p["name"])}</span>' if kind=='icon' and not decorative else ''
 return f'<div class="brand-art brand-art--{kind} {context}"'+(' aria-hidden="true"' if decorative else '')+f'>{image}{name}</div>'

def card(p,n):
 media=visual(p)
 preview=f'<div class="visual-link">{media}</div>' if p.get('videoId') or len(preview_screens(p))>1 else f'<a class="visual-link" href="{p["id"]}.html" aria-label="Explore {e(p["name"])}">{media}</a>'
 return f'''<article class="project-card" data-category="{p['category']}">{preview}<div class="card-meta"><span>{e(p['sector'])}</span><span>{n:02d}</span></div>{brand_art(p,"directory-brand",True)}<h3><a href="{p['id']}.html">{e(p['name'])}<span aria-hidden="true">↗</span></a></h3><p>{e(p['short'])}</p><span class="status"><i></i>{e(p['status'])}</span></article>'''

def home():
 from homepage import homepage
 return page('AI applications, built around real work','Baylor Harrison builds AI applications, business automation and cloud systems. Explore client work, developer tools and selected earlier projects.',homepage(PROJECTS,visual,card,brand_art),'','work')


def legacy_body(p):
 raw=(ROOT/'content/legacy'/f'{p["id"]}.html').read_text()
 raw=re.sub(r'<!--.*?-->','',raw,flags=re.S)
 for excluded in p.get('excludedLegacyImages',[]):
  raw=re.sub(r'<div[^>]*>\s*<img[^>]*src="'+re.escape(excluded)+r'"[^>]*>\s*</div>','',raw)
 raw=re.sub(r'<header class="major">.*?</header>','',raw,count=1,flags=re.S)
 # Keep the original implementation excerpts in source history; the public narrative emphasizes the product.
 raw=re.sub(r'<pre\b[^>]*>.*?</pre>','',raw,flags=re.S)
 raw=re.sub(r'<code\b[^>]*>.*?</code>','',raw,flags=re.S)
 raw=re.sub(r'\sstyle="[^"]*"','',raw)
 raw=raw.replace('src="https://www.youtube.com/embed/rbcvWOjfI3E?autoplay=1&mute=1&loop=1&playlist=rbcvWOjfI3E"','src="https://www.youtube-nocookie.com/embed/rbcvWOjfI3E" title="ALPHA SEO original product demonstration" loading="lazy"')
 raw=raw.replace('alt=""',f'alt="{e(p["name"])} original project image"')
 raw=re.sub(r'<img\s', '<img loading="lazy" ',raw)
 raw=re.sub(r'<a href="alpha-seo.html"[^>]*>(\s*<iframe.*?</iframe>)\s*</a>',r'\1',raw,flags=re.S)
 # The original demonstration now leads the case study; avoid a second simultaneous player.
 if p.get('videoId'):
  raw=re.sub(r'<iframe\b[^>]*>.*?</iframe>','<p>The original demonstration at the top of this page shows the application as it existed during the internship.</p>',raw,flags=re.S)
 # Keep legacy pages readable as product stories, with implementation retained in source history.
 if p['id']=='client-portal':
  captions=[('A shared client workspace','A central interface brings client communication and project information together.'),('Sign-in and notifications','The application connects account access with the relevant client experience and updates.'),('Client onboarding','An onboarding workflow creates a new client portal and its account.'),('Staff visibility','The staff dashboard organizes client portals and their associated information.'),('Profile management','Staff can maintain their profile information within the application.')]
  it=iter(captions)
  def caption(match):
   pair=next(it,None)
   return f'<h3>{pair[0]}</h3><p>{pair[1]}</p>' if pair else match.group(0)
  raw=re.sub(r'<p(?:\s[^>]*)?>.*?</p>',caption,raw,flags=re.S)
 raw=re.sub(r'Here is a snippet.*?(?:coded this:|tracking algorithm:)','',raw,flags=re.S)
 raw=raw.replace('This function is responsible for generating real-time predictions based on user input.','The interactive tool generates predictions from user input.')
 # Modernize prose that referred to now-hidden code without inventing capabilities.
 raw=raw.replace('In this snippet,','In the original implementation,').replace('This snippet shows','The implementation connects').replace('The following snippet demonstrates','The original implementation covers')
 raw=re.sub(r'<p>The following function is how.*?</p>','',raw,flags=re.S)
 raw=re.sub(r'<p>\s*The following.*?code.*?</p>','',raw,flags=re.S)
 return '<section class="legacy-content" aria-label="Original project walkthrough"><p class="eyebrow">Original project / selected screens & walkthrough</p><p class="archive-note">The original project imagery and product explanation are retained here. These are historical project materials; current availability may differ.</p>'+raw+'</section>'

def case(p,n):
 chips=''.join(f'<span>{e(t)}</span>' for t in p['stack'])
 brand=brand_art(p,"client-brand")
 body=f'''<section class="case-hero"><a class="back-link" href="index.html#work">← All work</a><p class="eyebrow">{e(p['sector'])}</p>{brand}<h1>{e(p['title'])}</h1><p class="case-deck">{e(p['short'])}</p><div class="case-meta"><div><span>PROJECT</span><b>{e(p['name'])}</b></div><div><span>MY ROLE</span><b>{e(p['role'])}</b></div><div><span>STAGE</span><b>{e(p['status'])}</b></div></div></section><div class="case-visual">{visual(p,True)}</div><div class="case-body"><aside class="case-aside"><p class="eyebrow">Inside this project</p><a href="#context">The context</a><a href="#contribution">My contribution</a><a href="#product">The product</a><a href="#next">Where it stands</a><div class="tech-tags">{chips}</div></aside><div class="case-story"><section id="context"><p class="eyebrow">The context</p><h2>A problem worth solving.</h2><p>{e(p['problem'])}</p></section><section id="contribution"><p class="eyebrow">My contribution</p><h2>What I brought to the work.</h2><p>{e(p['contribution'])}</p></section><section id="product"><p class="eyebrow">The product</p><h2>What it makes possible.</h2>'''
 if p.get('legacy'):
  body+=legacy_body(p)
 else:
  body+='<div class="feature-groups">'+''.join(f'<details><summary><span>{i:02d}</span>{e(g[0])}<b aria-hidden="true">+</b></summary><p>{e(g[1])}</p></details>' for i,g in enumerate(p['groups'],1))+'</div>'
  body+='<div class="flow-panel"><p class="eyebrow">At a glance / simplified product view</p><ol>'+''.join(f'<li><span>{i:02d}</span>{e(x)}</li>' for i,x in enumerate(p['flow'],1))+'</ol></div>'
 screens=[im for im in p.get('screens',[]) if im['src']!=p.get('image')]
 if screens and not p.get('legacy'):
  body+='<div class="product-screens"><p class="eyebrow">Inside the software</p><h3>See the actual workspace.</h3>'+''.join(f'<figure><img src="{e(im["src"])}" alt="{e(im["alt"])}" width="{im["width"]}" height="{im["height"]}" loading="lazy"><figcaption>{e(im["caption"])}</figcaption></figure>' for im in screens)+'</div>'
 body+='</section><section id="next"><p class="eyebrow">Where it stands</p><h2>The work keeps moving.</h2><p>'+e(p.get('next','This project remains part of the earlier-work collection. The original materials show the implementation at that point in time; they are not a claim about current operation.'))+'</p></section></div></div>'
 nxt=PROJECTS[(n+1)%len(PROJECTS)]
 body+=f'<a class="next-project" href="{nxt["id"]}.html"><span class="eyebrow">Keep exploring</span><strong>{e(nxt["name"])} <span aria-hidden="true">↗</span></strong></a>'
 return page(p['name'],p['short'],body,p['id']+'.html','work')

def resume():
 body='''<section class="case-hero"><a class="back-link" href="index.html">← Home</a><p class="eyebrow">Background & experience</p><h1>A builder, across<br><em>disciplines.</em></h1><p class="case-deck">AI applications, business workflows and the engineering that brings them together.</p></section><section class="background-grid"><div><p class="eyebrow">Experience</p><article class="role"><span>MANIFOLD ENGINEERING</span><h2>Founder & Software Engineer</h2><p>AI development studio. Client software across lending, workplace services, structural engineering and commercial real estate, alongside internal developer tools and research prototypes.</p><a href="index.html#work">Explore the projects ↗</a></article><article class="role"><span>FIFTYFLOWERS</span><h2>AI Solutions Engineer</h2><p>AI applications across customer support, marketing, company knowledge, commerce and product-data operations. Earlier work as AI & Process Innovation Associate established several of the storefront integrations.</p><a href="fiftyflowers.html">Explore FiftyFlowers ↗</a></article><article class="role"><span>WEBMARKETS / 2024 INTERNSHIP</span><h2>Web Developer Intern</h2><p>Built the first client portal and contributed to the ALPHA SEO application with the engineering team.</p><a href="client-portal.html">Explore the Client Portal ↗</a></article><article class="role"><span>EDUCATION</span><h2>Computer Science, B.S.</h2><p>Arizona State University · May 2025</p></article></div><aside class="document-panel"><p class="eyebrow">Documents</p><h2>The full background.</h2><p>The live LinkedIn profile reflects the September 2026 experience update. The résumé retains its May 2025 experience content and does not yet include the newer work. Its public contact details were updated in September 2026.</p><a class="button dark" href="https://www.linkedin.com/in/baylor-harrison">Current LinkedIn profile ↗</a><a class="document-link" href="files/Baylor-Harrison-Resume.pdf" download>Résumé <span>PDF · May 2025 ↓</span></a><a class="document-link" href="files/Baylor-Harrison-LOR.pdf" download>Recommendation <span>PDF ↓</span></a><details><summary>View document previews</summary><a href="images/SeniorResume.png"><img src="images/SeniorResume.png" alt="Résumé with May 2025 experience and updated contact email" loading="lazy"></a><a href="images/LOR.png"><img src="images/LOR.png" alt="Existing letter of recommendation" loading="lazy"></a></details></aside></section>'''
 return page('Background & experience','The background behind Baylor Harrison’s AI and software engineering work.',body,'resume.html','resume')

(ROOT/'index.html').write_text(home())
for n,p in enumerate(PROJECTS): (ROOT/f'{p["id"]}.html').write_text(case(p,n))
(ROOT/'resume.html').write_text(resume())
(ROOT/'404.html').write_text(page('Page not found','Return to the portfolio.', '<section class="case-hero"><p class="eyebrow">404 / A small detour</p><h1>Let’s get you<br>back to the work.</h1><a class="button dark" href="index.html">Explore the portfolio ↗</a></section>','404.html'))
urls=['']+[p['id']+'.html' for p in PROJECTS]+['resume.html']
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{SITE}/{x}</loc></url>' for x in urls)+'</urlset>')
print(f'Generated homepage, {len(PROJECTS)} projects, background, and 404.')

# Root-based assets/navigation keep the error page usable at arbitrary missing paths.
f=ROOT/'404.html'
f.write_text(re.sub(r'((?:href|src)=")(?!(?:[a-z]+:|/|#))',r'\1/',f.read_text()))
for filename in ['index.html','resume.html','404.html']+[p['id']+'.html' for p in PROJECTS]:
 target=ROOT/filename
 target.write_text('\n'.join(line.rstrip() for line in target.read_text().splitlines())+'\n')
