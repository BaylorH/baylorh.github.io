"""Editorial homepage composition; existing case-study content stays in the shared builder."""
from html import escape as e
from atmosphere import stream
from editorial import closing_sections

def homepage(projects, visual, card, brand_art):
 hero='''<section class="studio-hero"><div class="studio-intro"><p class="studio-byline">Baylor Harrison · Manifold Engineering</p><h1>Useful AI.<br>Thoughtfully engineered.</h1><p class="studio-deck">I turn business information, everyday workflows and ambitious ideas into software people can actually use.</p><div class="hero-actions"><a class="button dark" href="#selected-work">Explore selected work <span aria-hidden="true">↓</span></a><a class="text-link" href="#about">Meet the engineer</a></div><p class="studio-location">Independent engineer & founder <span>Based in Arizona</span></p></div>'''+stream(projects)+'''</section><div class="studio-disciplines"><span>AI applications</span><span>Full-stack products</span><span>Cloud integrations</span><span>Engineering tools</span></div>'''
 stories={
 'fiftyflowers':('One workspace. More ways to help.','Connected tools for customer support, product imagery and company knowledge.', [('Customer support','4 connected applications'),('Marketing','Reusable image & content workflows')]),
 'till':('Lower costs. Clearer lending decisions.','Scoring built into the lending workflow, with a separate dashboard for tracking performance.', [('Scoring API','$24K annualized savings'),('Lending dashboard','5 connected views')]),
 'engineering-platform':('Know what’s built. Know what’s next.','A shared view of project progress, with engineering knowledge that carries into the next session.', [('The Record','Scope, progress & evidence'),('Brain + Jarvis OS','Working memory · orchestration prototype')])}
 featured='<section id="selected-work" class="selected-work"><div class="selected-heading"><p class="studio-byline">Selected work</p><h2 data-reveal-heading>Built around<br>the real problem.</h2><p>A few ways that takes shape.</p></div>'
 for pid,(title,desc,outcomes) in stories.items():
  p=next(p for p in projects if p['id']==pid)
  mark=brand_art(p,"featured-brand") or f'<span class="featured-name">{e(p["name"])}</span>'
  results=''.join(f'<div class="featured-result"><span>{e(label)}</span><strong>{e(result)}</strong></div>' for label,result in outcomes)
  featured+=f'''<article class="featured-story" data-featured="{pid}"><div class="featured-copy">{mark}<p class="featured-sector">{e(p['sector'])}</p><h3>{e(title)}</h3><p>{e(desc)}</p><div class="featured-outcomes">{results}</div><a class="text-link" href="{pid}.html">Explore {e(p['name'])} <span aria-hidden="true">↗</span></a></div><div class="featured-stage"><div class="featured-media">{visual(p,layered=True)}</div></div></article>'''
 featured+='</section>'
 directory='''<section class="work-section directory-section" id="work"><div class="section-heading"><div><p class="studio-byline">The complete collection</p><h2>More to explore.</h2></div><p>Client products, engineering tools<br>and the projects that came before.</p></div><div class="work-toolbar"><div class="filters" role="group" aria-label="Filter projects" hidden><button type="button" data-filter="all" aria-pressed="true">All work <span>13</span></button><button type="button" data-filter="business" aria-pressed="false">Business systems</button><button type="button" data-filter="engineering" aria-pressed="false">Developer & research tools</button><button type="button" data-filter="earlier" aria-pressed="false">Earlier work</button></div><span class="project-count" role="status" aria-live="polite">13 projects</span></div><div class="project-grid">'''+''.join(card(p,n) for n,p in enumerate(projects,1))+'</div></section>'
 about=closing_sections()
 return hero+featured+directory+about
