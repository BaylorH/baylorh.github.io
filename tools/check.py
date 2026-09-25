"""Check the generated portfolio's reachable pages, media, and content preservation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json,re,subprocess
root=Path(__file__).resolve().parents[1]
projects=json.loads((root/'content/projects.json').read_text())
pages=['index.html','resume.html','404.html']+[p['id']+'.html' for p in projects]
errors=[]
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.links=[];self.ids=[];self.h1=0;self.images=[];self.feed(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  for key in ('href','src'):
   if key in a:self.links.append(a[key])
  if tag=='img':self.images.append(a)
parsed={name:Page((root/name).read_text()) for name in pages}
for name,page in parsed.items():
 if page.h1!=1:errors.append(f'{name}: expected one h1, found {page.h1}')
 if len(set(page.ids))!=len(page.ids):errors.append(f'{name}: duplicate IDs')
 for image in page.images:
  if 'alt'not in image:errors.append(f'{name}: image without alt')
 for url in page.links:
  u=urlsplit(url)
  if u.scheme or u.netloc:continue
  target=unquote(u.path) or name
  target=target.lstrip('/')
  if not (root/target).exists():errors.append(f'{name}: missing {url}')
  if u.fragment and target in parsed and u.fragment not in parsed[target].ids:errors.append(f'{name}: missing fragment {url}')
 text=(root/name).read_text()
 for bad in ['clientPassword','apiKey','sk-proj-','/Users/','jarvis-os-frontend.firebaseapp.com/p/']:
  if bad in text:errors.append(f'{name}: source/private detail found: {bad}')
 if re.search(r'<(?:pre|code)\b',text):errors.append(f'{name}: implementation recipe remains exposed')
for p in projects:
 if p.get('legacy'):
  source=subprocess.check_output(['git','show',f'b5e19c2:{p["id"]}.html'],cwd=root,text=True)
  old=re.search(r'<section class="post">(.*?)</section>',source,re.S).group(1)
  saved=(root/'content/legacy'/f'{p["id"]}.html').read_text()
  if old!=saved:errors.append(f'{p["id"]}: original source not preserved')
  active=re.sub(r'<!--.*?-->','',old,flags=re.S)
  for src in re.findall(r'<img[^>]+src="([^"]+)"',active):
   if src not in p.get('excludedLegacyImages',[]) and src not in (root/f'{p["id"]}.html').read_text():errors.append(f'{p["id"]}: lost original media {src}')
 if f'{p["id"]}.html' not in (root/'index.html').read_text():errors.append(f'{p["id"]}: absent from gallery')
assert len(projects)==13
assert 'href="/index.html"' in (root/'404.html').read_text()
assert '<base' not in (root/'404.html').read_text()
config=(root/'_config.yml').read_text()
for excluded in ['content','tools','docs','dist']:
 if f'  - {excluded}' not in config:errors.append(f'Public hosting does not exclude {excluded}')
if (root/'dist').exists():
 for excluded in ['content','tools','docs','generic.html','elements.html']:
  if (root/'dist'/excluded).exists():errors.append(f'Release contains {excluded}')
 for file in (root/'dist').glob('*.html'):
  if re.search(r'<(?:pre|code)\b',file.read_text()):errors.append(f'Release code exposure: {file.name}')
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; internal links, fragments, media, headings, public-content boundaries, and all six original project sources.')
