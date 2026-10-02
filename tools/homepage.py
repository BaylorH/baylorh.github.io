"""Editorial homepage composition; existing case-study content stays in the shared builder."""
from html import escape as e
from atmosphere import stream
from editorial import closing_sections, capability_strip

def homepage(projects, visual, card, brand_art):
 hero='''<section class="studio-hero"><div class="studio-intro"><p class="studio-byline">Baylor Harrison · Manifold Engineering</p><h1>Useful AI.<br>Thoughtfully engineered.</h1><p class="studio-deck">I turn business information, everyday workflows and ambitious ideas into software people can actually use.</p><div class="hero-actions"><a class="button dark" href="#selected-work">Explore selected work <span aria-hidden="true">↓</span></a><a class="text-link" href="#about">Meet the engineer</a></div><p class="studio-location">Engineer & founder <span>Based in Arizona</span></p></div>'''+stream(projects)+'</section>'+capability_strip()
 stories={
 'fiftyflowers':('One workspace. More ways to help.','AI for customer service, product image editing and company knowledge—all in one workspace.', [('AI customer service','In production since January 2026'),('AI image editing','Reusable presets & content workflows')]),
 'till':('Lower costs. Clearer lending decisions.','Machine-learning loan scoring, paired with a dashboard for understanding lending performance.', [('Machine-learning API','Est. $24K saved a year · my estimate'),('Lending dashboard','5 connected views')]),
 'create-spaces':('Every booking since 2009. Verified to the cent.','A company’s booking history, verified to the cent in its own cloud storage, with a dashboard live behind a company sign-in and a daily AI export and ChatGPT connection being switched on step by step.', [('Booking history','2009 to September 2026 · checked to the cent'),('Stage','Dashboard live · rollout continuing')]),
 'engineering-platform':('Know what’s built. Know what’s next.','A shared view of project progress, with engineering knowledge that carries into the next session.', [('The Record','Scope, progress & evidence'),('Brain + Jarvis OS','Engineering memory · agent orchestration')])}
 featured='<section id="selected-work" class="selected-work"><div class="selected-heading"><p class="studio-byline">Selected work</p><h2 data-reveal-heading>Built around<br>the real problem.</h2><p>A few ways that takes shape.</p></div>'
 for pid,(title,desc,outcomes) in stories.items():
  p=next(p for p in projects if p['id']==pid)
  mark=brand_art(p,"featured-brand") or f'<span class="featured-name">{e(p["name"])}</span>'
  results=''.join(f'<div class="featured-result"><span>{e(label)}</span><strong>{e(result)}</strong></div>' for label,result in outcomes)
  featured+=f'''<article class="featured-story" data-featured="{pid}"><div class="featured-copy">{mark}<p class="featured-sector">{e(p['sector'])}</p><h3>{e(title)}</h3><p>{e(desc)}</p><div class="featured-outcomes">{results}</div><a class="text-link" href="{pid}.html">Explore {e(p['name'])} <span aria-hidden="true">↗</span></a></div><div class="featured-stage"><div class="featured-media">{visual(p,layered=True)}</div></div></article>'''
 featured+='</section>'
 # One mixed collection. A company overview that has its own product pages is told above, not repeated as a card.
 overviews={p['parent'] for p in projects if p.get('parent')}
 listed=[p for p in projects if p['id'] not in overviews]
 kinds=[('companies','Companies & clients'),('products','Own products'),('earlier','Earlier work')]
 size=lambda k:sum(1 for p in listed if p['category']==k)
 buttons='<button type="button" data-filter="all" aria-pressed="true">All work <span>'+str(len(listed))+'</span></button>'+''.join(f'<button type="button" data-filter="{k}" aria-pressed="false">{e(label)} <span>{size(k)}</span></button>' for k,label in kinds)
 grid=''.join(card(p,n) for n,p in enumerate(listed,1))
 directory='''<section class="work-section directory-section" id="work"><div class="section-heading"><div><p class="studio-byline">The complete collection</p><h2>Everything, in one place.</h2></div><p>Every product has its own page,<br>with its real screens and its stage.</p></div><div class="work-toolbar"><div class="filters" role="group" aria-label="Filter projects" hidden>'''+buttons+'''</div><span class="project-count" role="status" aria-live="polite">'''+str(len(listed))+''' projects</span></div><p class="stage-legend" aria-label="What the stage marks mean"><span class="status" data-stage="production"><i></i>In production</span><span class="status" data-stage="rollout"><i></i>Live, still rolling out</span><span class="status" data-stage="own"><i></i>In my own daily use</span><span class="status" data-stage="built"><i></i>Built or delivered, not active</span><span class="status" data-stage="development"><i></i>Paused or prototype</span><span class="status" data-stage="earlier"><i></i>Earlier work</span></p><div class="project-grid">'''+grid+'</div></section>'
 about=closing_sections()
 return hero+featured+directory+about
