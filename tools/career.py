"""Career timeline sourced from reviewed LinkedIn roles and the current portfolio."""
from html import escape as e
import json
from pathlib import Path

def career_page(projects,brand_art):
 c=json.loads((Path(__file__).resolve().parents[1]/'content/career.json').read_text());by={p['id']:p for p in projects}
 def bullets(items):return '<ul>'+''.join('<li>'+e(t)+'</li>' for t in items)+'</ul>'
 def role(v):return '<div class="career-role"><div class="career-role-heading"><h3>'+e(v['role'])+'</h3><span>'+e(v['period'])+'</span></div>'+bullets(v['bullets'])+'</div>'
 entries=''
 for i,x in enumerate(c['experience']):
  logo=brand_art(by[x['logo']],'career-company-logo') if x.get('logo') else '<span class="manifold-mark" aria-hidden="true">M<span>·</span></span>'
  entries+=f'<article class="career-entry"><div class="career-date"><span>{e(x["period"])}</span><i aria-hidden="true"></i></div><div class="career-entry-body"><div class="career-company">{logo}<div><h2>{e(x["company"])}</h2><p>{e(x["context"])}</p></div></div>'
  entries+=''.join(role(v) for v in x.get('roles',[x]))
  if x.get('clients'):
   entries+='<div class="career-clients"><p class="eyebrow">Selected client work</p><div class="career-client-grid">'+''.join(f'<a href="{pid}.html" aria-label="Explore {e(by[pid]["name"])}">'+brand_art(by[pid],'career-client-logo',True)+f'<span>{e(by[pid]["name"])}</span></a>' for pid in x['clients'])+'</div></div>'
  if x.get('note'):entries+='<p class="career-note">'+e(x['note'])+'</p>'
  if x.get('earlier'):entries+='<p class="career-note">'+e(x['earlier'])+'</p>'
  entries+='</div></article>'
 ed=c['education']
 entries+=f'<article class="career-entry career-education"><div class="career-date"><span>{e(ed["period"])}</span><i aria-hidden="true"></i></div><div class="career-entry-body"><div class="career-company"><img class="asu-mark" src="images/brands/asu.jpg" width="100" height="100" alt="Arizona State University"><div><h2>{e(ed["school"])}</h2><p>{e(ed["degree"])}</p></div></div><p class="career-degree">Graduated {e(ed["completed"])} · {e(ed["details"])}</p><p class="career-note">{e(ed["project"])}</p><a class="text-link" href="machine-learning-visualization.html">Explore the capstone ↗</a></div></article>'
 return '''<section class="career-hero"><a class="back-link" href="index.html">← Home</a><p class="eyebrow">Background & experience</p><h1>Building useful AI.<br><em>Taking ownership.</em></h1><p class="career-intro">From an independent first build to connected business platforms. Hands-on engineering, product thinking and delivery.</p><div class="career-actions"><a class="button dark" href="files/Baylor-Harrison-Resume.pdf" download>Download résumé <span>PDF ↓</span></a><a class="text-link" href="https://www.linkedin.com/in/baylor-harrison/">LinkedIn ↗</a><span>Updated September 2026</span></div></section><section class="career-timeline" aria-label="Professional experience and education">'''+entries+'''</section><section class="career-skills"><p class="eyebrow">Across the work</p><h2>From the interface to the infrastructure.</h2><div>'''+''.join('<article><h3>'+e(h)+'</h3><p>'+e(t)+'</p></article>' for h,t in c['skills'])+'''</div></section>'''
