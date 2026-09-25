"""Native, progressively enhanced treatments inspired by the supplied image corridor."""
from html import escape as e

def contour():
 paths=''.join(f'<path d="M -100 {100+i*19} C 200 {-100+i*11}, 350 {520+i*6}, 690 {225+i*12} S 1050 {90+i*17}, 1500 {380+i*8}"/>' for i in range(16))
 return f'<svg class="contour-field" viewBox="0 0 1400 650" preserveAspectRatio="xMidYMid slice" aria-hidden="true" fill="none"><g stroke="currentColor" stroke-width=".8">{paths}</g></svg>'

def stream(projects):
 selected=['fiftyflowers','till','engineering-platform','create-spaces','axiom','sitesift','ai-media-manager']
 images=[next(p for p in projects if p['id']==pid)['image'] for pid in selected]
 keys=[];cards=[]
 for direction,name in [(1,'stream-right'),(-1,'stream-left')]:
  stops=[]
  for n in range(41):
   u=n/40;scale=(5/26)*(100/5)**u;z=55*(1-1/scale)
   rail=38-(38+8)*(1-u)**2.8;turn=6+19*u
   stops.append(f'{u*100:.1f}%{{transform:translate3d({direction*rail:.3f}cqw,0,{z:.3f}cqw) rotateY({-direction*turn:.2f}deg)}}')
  keys.append('@keyframes '+name+'{'+''.join(stops)+'}')
  for i,src in enumerate(images):
   cards.append(f'<div class="stream-card" style="animation-name:{name};animation-delay:-{i*28/7}s"><img src="{e(src)}" width="1440" height="900" alt="" decoding="async" draggable="false"></div>')
 return '<div class="studio-scene product-stream" data-image-stream>'+contour()+'<div class="stream-topline"><span>Selected interfaces</span><span>01 — 07</span></div><style>'+''.join(keys)+'</style><div aria-hidden="true" class="stream-world"><div class="stream-rails">'+''.join(cards)+'</div></div><div class="stream-bottom"><span>Real products. Different possibilities.</span><button class="ambient-toggle" type="button" hidden>Pause motion</button></div></div>'

def footer(email):
 return f'''<footer class="site-footer studio-footer"><div class="contact-stage">{contour()}<div class="footer-topline"><span>Baylor Harrison <i>·</i> Manifold Engineering</span><span>Independent engineer / Arizona</span></div><div class="contact-layout"><div><p class="eyebrow">A useful next conversation</p><h2 data-reveal-heading>What could<br>work better?</h2></div><div class="contact-invite"><p>A workflow worth improving.<br>An idea ready to become real.<br>Let’s find the useful next step.</p><a class="contact-orbit" href="mailto:{email}"><span>Let’s talk</span><b aria-hidden="true">↗</b></a></div></div><div class="footer-directory"><a class="footer-email" href="mailto:{email}">{email}<span aria-hidden="true">↗</span></a><nav aria-label="Explore the portfolio"><a href="index.html#work">The work</a><a href="index.html#approach">The approach</a><a href="resume.html">Background</a></nav><nav aria-label="Elsewhere"><a href="https://www.linkedin.com/in/baylor-harrison">LinkedIn ↗</a><a href="https://github.com/BaylorH">GitHub ↗</a><a href="tel:+12089991801">Call ↗</a></nav></div><div class="footer-signature" aria-hidden="true">MANIFOLD<span>ENGINEERING</span></div><div class="footer-colophon"><span>© 2026 Baylor Harrison</span><span>Thoughtfully engineered.</span><button class="ambient-toggle" type="button" hidden>Pause motion</button></div></div></footer>'''
