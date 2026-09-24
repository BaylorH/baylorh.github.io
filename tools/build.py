"""Generate the portfolio as portable, crawlable static HTML."""
from pathlib import Path
from html import escape as e
import json, re, subprocess
ROOT = Path(__file__).resolve().parents[1]
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

def header(active=''):
 return f'''<a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="index.html" aria-label="Baylor Harrison home"><span class="brand-mark">bh<span>·</span></span><span>Baylor Harrison<small>Engineer & builder</small></span></a><nav aria-label="Main navigation"><a href="index.html#work" {'aria-current="page"' if active=='work' else ''}>Work</a><a href="index.html#approach">Approach</a><a href="resume.html" {'aria-current="page"' if active=='resume' else ''}>Background</a><a class="contact-link" href="mailto:{EMAIL}">Let’s talk <span aria-hidden="true">↗</span></a></nav></header>'''

def footer():
 return f'''<footer class="site-footer"><div class="footer-top"><div><p class="eyebrow">A useful next conversation</p><h2>What could work<br><em>better?</em></h2></div><div class="footer-contact"><p>Have a workflow, a product idea, or a team<br>that could use a different perspective?</p><a class="button dark" href="mailto:{EMAIL}">Let’s talk <span aria-hidden="true">↗</span></a></div></div><div class="footer-bottom"><span>© 2026 Baylor Harrison</span><div><a href="https://www.linkedin.com/in/baylor-harrison">LinkedIn ↗</a><a href="https://github.com/BaylorH">GitHub ↗</a><a href="tel:+12089991801">Call ↗</a></div><span>Built with care. Designed to be useful.</span></div></footer>'''

def page(title,description,body,path,active=''):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f5f3ed"><title>{e(title)} · Baylor Harrison</title><meta name="description" content="{e(description)}"><link rel="canonical" href="{SITE}/{path}"><meta property="og:title" content="{e(title)} · Baylor Harrison"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE}/{path}"><meta property="og:image" content="{SITE}/images/portfolio-social.png"><link rel="icon" type="image/svg+xml" href="images/portfolio-mark.svg"><link rel="stylesheet" href="assets/css/portfolio.css"><script defer src="assets/js/portfolio.js"></script></head><body>{header(active)}<main id="main">{body}</main>{footer()}<dialog id="image-viewer" aria-label="Expanded project image"><button type="button" class="viewer-close" aria-label="Close image">Close ×</button><img alt=""><p></p></dialog></body></html>'''

def visual(p,large=False):
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

def card(p,n):
 return f'''<article class="project-card" data-category="{p['category']}"><a class="visual-link" href="{p['id']}.html" aria-label="Explore {e(p['name'])}">{visual(p)}</a><div class="card-meta"><span>{e(p['sector'])}</span><span>{n:02d}</span></div><h3><a href="{p['id']}.html">{e(p['name'])}<span aria-hidden="true">↗</span></a></h3><p>{e(p['short'])}</p><span class="status"><i></i>{e(p['status'])}</span></article>'''

def home():
 body='''<section class="hero"><div class="hero-copy"><p class="eyebrow"><span class="tiny-cross">+</span> Independent thinking. Connected systems.</p><h1>Useful AI.<br>Thoughtfully<br><em>engineered.</em></h1><p class="hero-description">I’m Baylor. I build applications that connect business information, automate everyday work, and help people make better decisions.</p><div class="hero-actions"><a class="button dark" href="#work">Explore the work <span aria-hidden="true">↓</span></a><a class="text-link" href="#about">A little about me ↗</a></div></div><div class="hero-canvas" aria-label="A simple illustration of connected business software"><div class="canvas-caption"><span>AN ENGINEER’S VIEW</span><span>FIG. 01</span></div><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><div class="system-center"><span class="center-spark">✳</span></div><div class="system-node node-data"><span>01 / CONNECT</span><b>The right information</b><small>Data · tools · context</small></div><div class="system-node node-work"><span>02 / BUILD</span><b>Useful applications</b><small>Interfaces · automation · cloud</small></div><div class="system-node node-people"><span>03 / MAKE IT MATTER</span><b>People in control</b><small>Visibility · decisions · outcomes</small></div><div class="canvas-note">The technology is the means.<br>The useful part is what it makes possible.</div></div></section><div class="intro-strip"><span>Founder, <strong>Manifold Engineering</strong></span><span>AI applications / Full-stack engineering / Cloud systems</span><span>Based in Arizona <span aria-hidden="true">↗</span></span></div>
<section class="work-section" id="work"><div class="section-heading"><div><p class="eyebrow">01 / A selection of the work</p><h2>Different problems.<br><em>The same care.</em></h2></div><p>From everyday business workflows<br>to the tools behind the engineering.</p></div><div class="work-toolbar"><div class="filters" role="group" aria-label="Filter projects" hidden><button type="button" data-filter="all" aria-pressed="true">All work <span>13</span></button><button type="button" data-filter="business" aria-pressed="false">Business systems</button><button type="button" data-filter="engineering" aria-pressed="false">Developer & research tools</button><button type="button" data-filter="earlier" aria-pressed="false">Earlier work</button></div><span class="project-count" role="status" aria-live="polite">13 projects</span></div><div class="project-grid">'''
 body+=''.join(card(p,n) for n,p in enumerate(PROJECTS,1))
 body+='''</div></section><section class="approach-section" id="approach"><div class="section-heading"><div><p class="eyebrow">02 / How I approach the work</p><h2>Make it useful.<br><em>Then make it hold up.</em></h2></div><p>Good software starts with understanding the operation—and stays grounded in the people using it.</p></div><div class="approach-grid"><article><span>01</span><h3>Understand the work.</h3><p>Find the information, decisions and repetitive steps that matter. Shape a focused scope around the actual business need.</p></article><article><span>02</span><h3>Connect the pieces.</h3><p>Bring the interface, existing tools and cloud services together into an application people can use.</p></article><article><span>03</span><h3>Prove the useful part.</h3><p>Test the behavior, make limitations visible and leave clear evidence and handoffs for whatever comes next.</p></article></div></section><section class="about-section" id="about"><div><p class="eyebrow">03 / The person behind the work</p><h2>An engineer’s curiosity.<br><em>A builder’s perspective.</em></h2></div><div class="about-copy"><p>I’m the founder of Manifold Engineering, an AI development studio. My work brings together product thinking, full-stack applications, integrations and cloud infrastructure.</p><p>I’m interested in the space between what a business does today and what better tools could make possible—from a more useful dashboard to a connected workflow that takes repetitive work off someone’s plate.</p><p>I also build tools for AI-assisted engineering itself, so project knowledge, focused assignments and evidence stay connected as the work evolves.</p><div class="about-links"><a class="text-link" href="resume.html">Background & experience ↗</a><a class="text-link" href="https://www.linkedin.com/in/baylor-harrison">LinkedIn ↗</a></div></div></section>'''
 return page('AI applications, built around real work','Baylor Harrison builds AI applications, business automation and cloud systems. Explore client work, developer tools and selected earlier projects.',body,'','work')

def legacy_body(p):
 raw=(ROOT/'content/legacy'/f'{p["id"]}.html').read_text()
 raw=re.sub(r'<!--.*?-->','',raw,flags=re.S)
 raw=re.sub(r'<header class="major">.*?</header>','',raw,count=1,flags=re.S)
 # Keep the original implementation excerpts in source history; the public narrative emphasizes the product.
 raw=re.sub(r'<pre\b[^>]*>.*?</pre>','',raw,flags=re.S)
 raw=re.sub(r'<code\b[^>]*>.*?</code>','',raw,flags=re.S)
 raw=re.sub(r'\sstyle="[^"]*"','',raw)
 raw=raw.replace('src="https://www.youtube.com/embed/rbcvWOjfI3E?autoplay=1&mute=1&loop=1&playlist=rbcvWOjfI3E"','src="https://www.youtube-nocookie.com/embed/rbcvWOjfI3E" title="ALPHA SEO original product demonstration" loading="lazy"')
 raw=raw.replace('alt=""',f'alt="{e(p["name"])} original project image"')
 raw=re.sub(r'<img\s', '<img loading="lazy" ',raw)
 raw=re.sub(r'<a href="alpha-seo.html"[^>]*>(\s*<iframe.*?</iframe>)\s*</a>',r'\1',raw,flags=re.S)
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
 brand=f'<div class="client-brand"><img src="{p["logo"]}" alt="{e(p["name"])}"></div>' if p.get('logo') else ''
 body=f'''<section class="case-hero"><a class="back-link" href="index.html#work">← All work</a><p class="eyebrow">{e(p['sector'])}</p>{brand}<h1>{e(p['title'])}</h1><p class="case-deck">{e(p['short'])}</p><div class="case-meta"><div><span>PROJECT</span><b>{e(p['name'])}</b></div><div><span>MY ROLE</span><b>{e(p['role'])}</b></div><div><span>STAGE</span><b>{e(p['status'])}</b></div></div></section><div class="case-visual">{visual(p,True)}</div><div class="case-body"><aside class="case-aside"><p class="eyebrow">Inside this project</p><a href="#context">The context</a><a href="#contribution">My contribution</a><a href="#product">The product</a><a href="#next">Where it stands</a><div class="tech-tags">{chips}</div></aside><div class="case-story"><section id="context"><p class="eyebrow">The context</p><h2>A problem worth solving.</h2><p>{e(p['problem'])}</p></section><section id="contribution"><p class="eyebrow">My contribution</p><h2>What I brought to the work.</h2><p>{e(p['contribution'])}</p></section><section id="product"><p class="eyebrow">The product</p><h2>What it makes possible.</h2>'''
 if p.get('legacy'):
  body+=legacy_body(p)
 else:
  body+='<div class="feature-groups">'+''.join(f'<details><summary><span>{i:02d}</span>{e(g[0])}<b aria-hidden="true">+</b></summary><p>{e(g[1])}</p></details>' for i,g in enumerate(p['groups'],1))+'</div>'
  body+='<div class="flow-panel"><p class="eyebrow">At a glance / simplified product view</p><ol>'+''.join(f'<li><span>{i:02d}</span>{e(x)}</li>' for i,x in enumerate(p['flow'],1))+'</ol></div>'
 body+='</section><section id="next"><p class="eyebrow">Where it stands</p><h2>The work keeps moving.</h2><p>'+e(p.get('next','This project remains part of the earlier-work collection. The original materials show the implementation at that point in time; they are not a claim about current operation.'))+'</p></section></div></div>'
 nxt=PROJECTS[(n+1)%len(PROJECTS)]
 body+=f'<a class="next-project" href="{nxt["id"]}.html"><span class="eyebrow">Keep exploring / next project</span><strong>{e(nxt["name"])} <span aria-hidden="true">↗</span></strong></a>'
 return page(p['name'],p['short'],body,p['id']+'.html','work')

def resume():
 body='''<section class="case-hero"><a class="back-link" href="index.html">← Home</a><p class="eyebrow">Background & experience</p><h1>A builder, across<br><em>disciplines.</em></h1><p class="case-deck">AI applications, business workflows and the engineering that brings them together.</p></section><section class="background-grid"><div><p class="eyebrow">Experience</p><article class="role"><span>MANIFOLD ENGINEERING</span><h2>Founder & Software Engineer</h2><p>AI development studio. Client software across lending, workplace services, structural engineering and commercial real estate, alongside internal developer tools and research prototypes.</p><a href="index.html#work">Explore the projects ↗</a></article><article class="role"><span>FIFTYFLOWERS</span><h2>AI Solutions Engineer</h2><p>AI applications across customer support, marketing, company knowledge, commerce and product-data operations. Earlier work as AI & Process Innovation Associate established several of the storefront integrations.</p><a href="fiftyflowers.html">Explore FiftyFlowers ↗</a></article><article class="role"><span>WEBMARKETS / 2024 INTERNSHIP</span><h2>Web Developer Intern</h2><p>Built the first client portal and contributed to the ALPHA SEO application with the engineering team.</p><a href="client-portal.html">Explore the Client Portal ↗</a></article><article class="role"><span>EDUCATION</span><h2>Computer Science, B.S.</h2><p>Arizona State University · May 2025</p></article></div><aside class="document-panel"><p class="eyebrow">Documents</p><h2>The full background.</h2><p>The live LinkedIn profile reflects the September 2026 experience update. The résumé retains its May 2025 experience content and does not yet include the newer work. Its contact email was updated in September 2026.</p><a class="button dark" href="https://www.linkedin.com/in/baylor-harrison">Current LinkedIn profile ↗</a><a class="document-link" href="files/Baylor-Harrison-Resume.pdf" download>Résumé <span>PDF · May 2025 ↓</span></a><a class="document-link" href="files/Baylor-Harrison-LOR.pdf" download>Recommendation <span>PDF ↓</span></a><details><summary>View original documents</summary><a href="images/SeniorResume.png"><img src="images/SeniorResume.png" alt="Résumé with May 2025 experience and updated contact email" loading="lazy"></a><a href="images/LOR.png"><img src="images/LOR.png" alt="Existing letter of recommendation" loading="lazy"></a></details></aside></section>'''
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
