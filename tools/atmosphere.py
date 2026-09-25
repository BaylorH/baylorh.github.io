"""Native, progressively enhanced treatments inspired by the supplied image corridor."""
from html import escape as e

def stream(projects):
 selected=['fiftyflowers','till','engineering-platform','create-spaces','axiom','sitesift','ai-media-manager']
 images=[next(p for p in projects if p['id']==pid) for pid in selected]
 duration=36
 keys=[];cards=[]
 for direction,name,rail_images in [(1,'stream-right',images[::2]),(-1,'stream-left',images[1::2])]:
  stops=[]
  for n in range(41):
   u=n/40;scale=(2.6/16.25)*(46/2.6)**u;z=30*(1-1/scale)
   rail=38-(38+11)*(1-u)**3.3;turn=6+22*u
   stops.append(f'{u*100:.1f}%{{transform:translate3d({direction*rail:.3f}cqw,0,{z:.3f}cqw) rotateY({-direction*turn:.2f}deg)}}')
  keys.append('@keyframes '+name+'{'+''.join(stops)+'}')
  for i,project in enumerate(rail_images):
   width,height=project['imageWidth'],project['imageHeight']
   offset=(i+.25)*duration/len(rail_images)
   cards.append(f'<img class="stream-card" style="--screen-ratio:{width/height:.6f};animation-name:{name};animation-delay:-{offset:.3f}s" src="{e(project["image"])}" width="{width}" height="{height}" alt="" decoding="async" draggable="false">')
 return '<div class="product-stream" data-image-stream>'+'<style>'+''.join(keys)+'</style><div aria-hidden="true" class="stream-world"><div class="stream-rails">'+''.join(cards)+'</div></div><div class="stream-bottom"><span>Real products. Thoughtfully built.</span><button class="ambient-toggle" type="button" hidden>Pause motion</button></div></div>'

def footer(email):
 return f'''<footer class="site-footer studio-footer"><div class="contact-stage"><div class="footer-contact"><div><p class="eyebrow">Have something in mind?</p><a class="footer-email" href="mailto:{email}">{email}<span aria-hidden="true">↗</span></a></div><nav aria-label="Elsewhere"><a href="https://www.linkedin.com/in/baylor-harrison">LinkedIn ↗</a><a href="https://github.com/BaylorH">GitHub ↗</a><a href="resume.html">Background ↗</a></nav></div><div class="footer-colophon"><span>© 2026 Baylor Harrison <i>·</i> Manifold Engineering</span><a href="index.html#work">Explore the work ↑</a></div></div></footer>'''
