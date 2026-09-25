"""Native, progressively enhanced treatments inspired by the supplied image corridor."""
from html import escape as e

def stream(projects):
 selected=['fiftyflowers','till','engineering-platform','create-spaces','axiom','sitesift','ai-media-manager']
 images=[next(p for p in projects if p['id']==pid)['image'] for pid in selected]
 keys=[];cards=[]
 for direction,name in [(1,'stream-right'),(-1,'stream-left')]:
  stops=[]
  for n in range(41):
   u=n/40;scale=(2.6/16.25)*(46/2.6)**u;z=30*(1-1/scale)
   rail=44-(44+11)*(1-u)**3.3;turn=6+22*u
   stops.append(f'{u*100:.1f}%{{transform:translate3d({direction*rail:.3f}cqw,0,{z:.3f}cqw) rotateY({-direction*turn:.2f}deg)}}')
  keys.append('@keyframes '+name+'{'+''.join(stops)+'}')
  for i,src in enumerate(images):
   cards.append(f'<div class="stream-card" style="animation-name:{name};animation-delay:-{i*22/7}s"><img src="{e(src)}" width="1440" height="900" alt="" decoding="async" draggable="false"></div>')
 return '<div class="product-stream" data-image-stream>'+'<style>'+''.join(keys)+'</style><div aria-hidden="true" class="stream-world"><div class="stream-rails">'+''.join(cards)+'</div></div><div class="stream-bottom"><span>Real products. Thoughtfully built.</span><button class="ambient-toggle" type="button" hidden>Pause motion</button></div></div>'

def footer(email):
 return f'''<footer class="site-footer studio-footer"><div class="contact-stage"><div class="footer-contact"><div><p class="eyebrow">Have something in mind?</p><a class="footer-email" href="mailto:{email}">{email}<span aria-hidden="true">↗</span></a></div><nav aria-label="Elsewhere"><a href="https://www.linkedin.com/in/baylor-harrison">LinkedIn ↗</a><a href="https://github.com/BaylorH">GitHub ↗</a><a href="resume.html">Background ↗</a></nav></div><div class="footer-colophon"><span>© 2026 Baylor Harrison <i>·</i> Manifold Engineering</span><a href="index.html#work">Explore the work ↑</a></div></div></footer>'''
