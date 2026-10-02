from pathlib import Path
from html.parser import HTMLParser
import gzip
r=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.sections=[];self.projects=[];self.features=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.sections.append(a['id'])
  if 'data-category' in a:self.projects.append(a['data-category'])
  if 'data-featured' in a:self.features.append(a['data-featured'])
p=Page();p.feed((r/'index.html').read_text())
assert 'selected-work' in p.sections, 'Selected stories are missing'
import json
catalog=json.loads((r/'content/projects.json').read_text())
overviews={x['parent'] for x in catalog if x.get('parent')}
listed=[x for x in catalog if x['id'] not in overviews]
assert overviews=={'fiftyflowers'}, 'Only FiftyFlowers has an overview page above its products'
assert len(p.projects)==len(listed)==21, 'The directory lists every product once; a company overview is not repeated as a card'
assert p.features==['fiftyflowers','till','create-spaces','engineering-platform'], 'Featured work must remain separate from the complete directory'
assert (r/'dist/assets/js/motion.js').exists(), 'Release must include motion module'
assert len(gzip.compress((r/'dist/assets/js/motion.js').read_bytes()))<=35000, 'Motion exceeds transfer budget'
assert (r/'dist/assets/css/refinement.css').exists(), 'Release must include refinement styles'
# One mixed collection: no company headings, the overview is told in the featured story, and companies are interleaved.
home=(r/'index.html').read_text()
import re
cards=re.findall(r'<article class="project-card" data-category="([a-z]+)">.*?<h3><a href="/([a-z0-9-]+)/">',home,re.S)
assert [c[1] for c in cards]==[x['id'] for x in listed], 'Directory order differs from the catalog'
assert [c[0] for c in cards]==[x['category'] for x in listed] and set(p.projects)<={'companies','products','earlier'}, 'Unknown directory kind'
assert 'class="directory-group"' not in home and 'by company' not in home, 'The directory is one mixed collection'
assert home.count('href="/fiftyflowers/"')>=1, 'The company overview stays reachable from the featured story'
# The collection runs loosely in order of creation, newest first, and the games close it.
months=lambda x:int(x['created'][:4])*12+int(x['created'][5:7])
games=[x for x in listed if x.get('game')]; rest=[x for x in listed if not x.get('game')]
assert listed==rest+games and [x['id'] for x in games]==['ai-arena','lunar-base','pacman'], 'The games close the collection'
assert all(months(b)-months(a)<=3 for i,a in enumerate(rest) for b in rest[i+1:]), 'A card sits ahead of one that is more than three months newer'
assert all(months(a)>=months(b) for a,b in zip(games,games[1:])), 'The games run newest first'
company=lambda x:x.get('parent') or x['id']
assert sum(company(a)==company(b) for a,b in zip(rest,rest[1:]))<=2, 'Products of one company stack up in the collection'
assert not any(company(a)==company(b)==company(c) for a,b,c in zip(rest,rest[1:],rest[2:])), 'Three products of one company sit in a row'
assert len({company(x) for x in rest[:3]})==3, 'The collection must open on three different places'
assert 'sitesift' not in p.features, 'A product in development is not featured'
print('PASS: selected stories, a collection in loose order of creation with the games last, and release motion budget')

import json
from PIL import Image
for item in json.loads((r/'content/projects.json').read_text()):
 if item.get('image'):
  with Image.open(r/item['image']) as image:
   assert image.size==(item['imageWidth'],item['imageHeight']), item['id']
print('PASS: source image dimensions match generated aspect ratios')

# Real brand art must retain an intrinsic ratio and appear in the directory and story.
from html.parser import HTMLParser
class BrandImages(HTMLParser):
 def __init__(self,html):
  super().__init__(); self.images=[]; self.feed(html)
 def handle_starttag(self,tag,attrs):
  if tag=='img':self.images.append(dict(attrs))
items=json.loads((r/'content/projects.json').read_text())
for pid in ['fiftyflowers','till','create-spaces','axiom','sitesift','ai-media-manager']:
 item=next(p for p in items if p['id']==pid)
 assert item.get('logo'), f'{pid}: real brand art is missing'
 assert item.get('logoWidth',0)>0 and item.get('logoHeight',0)>0, f'{pid}: missing intrinsic logo dimensions'
 path=r/item['logo']
 if path.suffix=='.svg':
  import xml.etree.ElementTree as ET
  svg=ET.fromstring(path.read_text())
  actual=tuple(map(float,svg.attrib['viewBox'].split()[2:]))
  for node in svg.iter():
   assert node.tag.split('}')[-1] not in ['script','foreignObject','image'], f'{pid}: unsafe SVG content'
   assert all(not key.lower().startswith('on') and key.split('}')[-1] not in ['href','src'] for key in node.attrib), f'{pid}: active or external SVG content'
 else:
  with Image.open(path) as image:actual=image.size
 assert actual==(item['logoWidth'],item['logoHeight']), f'{pid}: dimensions differ from original art'
 for page in ['index.html',pid+'.html']:
  matches=[im for im in BrandImages((r/page).read_text()).images if im.get('src','').lstrip('/')==item['logo']]
  assert matches, f'{page}: missing {pid} brand art'
  assert all(im.get('width')==str(item['logoWidth']) and im.get('height')==str(item['logoHeight']) for im in matches), f'{page}: brand ratio not reserved'
for pid in ['till','create-spaces','engineering-platform']:
 item=next(p for p in items if p['id']==pid)
 assert item.get('image','').startswith('images/product-screens/'), f'{pid}: selected story should show the reviewed interface'
 assert item['imageCaption'], f'{pid}: interface evidence requires its caption'
 assert item['imageCaption'] in (r/(pid+'.html')).read_text(), f'{pid}: caption was lost'
print('PASS: verified brand art and reviewed selected-work screenshots retain dimensions and captions')

# Keep requested editorial order and gallery sources reliable as the collection grows.
expected=['fiftyflowers', 'create-spaces', 'fiftyflowers-diy-migration', 'engineering-platform', 'fiftyflowers-second-brain', 'fiftyflowers-content-engine', 'ai-media-manager', 'fiftyflowers-image-studio', 'axiom', 'fiftyflowers-proposal-manager', 'fiftyflowers-support-ai', 'till', 'fiftyflowers-storefront-requests', 'sitesift', 'fiftyflowers-shopping-assistant', 'ai-travel-companion', 'client-portal', 'alpha-seo', 'machine-learning-visualization', 'ai-arena', 'lunar-base', 'pacman']
assert [x['id'] for x in items]==expected, 'Requested directory order changed'
import sys
sys.path.insert(0,str(r/'tools'))
from screen_gallery import screen_gallery,preview_screens
for item in items:
 screens=item.get('screens',[])
 assert len({s['src'] for s in screens})==len(screens), item['id']+' repeated a screen'
 for s in screens:
  with Image.open(r/s['src']) as image:assert image.size==(s['width'],s['height']),s['src']
 if len(preview_screens(item))>1:
  html=screen_gallery(item,layered=True)
  shown=preview_screens(item)
  assert html.count('class="screen-shot ')==len(shown)
  assert html.count('data-screen-index=')==len(shown)
  assert html.count('aria-hidden="true"')==len(shown)-1
  # Earlier-work pages keep their original walkthrough instead of the screen list.
  if not item.get('legacy'):
   page=(r/(item['id']+'.html')).read_text()
   assert all(s['src'] in page for s in screens), item['id']+' product page lost a screen'
  assert 'screen-caption' in html and 'data-caption=' in html
assert next(x for x in items if x['id']=='axiom')['previewMode']=='single'
assert 'object-fit:contain' in (r/'assets/css/refinement.css').read_text()
print('PASS: directory order, unique screen sources, dimensions, keyboard-ready controls and singular Axiom cover')

# Returning visitors must receive the matching controller, not stale cached playback code.
import hashlib
controller_hash=hashlib.sha256((r/'assets/js/portfolio.js').read_bytes()).hexdigest()[:12]
for page in r.glob('*.html'):
 if 'assets/js/portfolio.js' in page.read_text():
  assert f'assets/js/portfolio.js?v={controller_hash}' in page.read_text(), f'{page.name}: stale controller URL'
print('PASS: generated pages version the playback controller by content')

# Chapters: every screen exists at its stated size, appears on its page, and the page's contents list reaches each chapter.
for item in items:
 if not item.get('chapters'): continue
 page=(r/(item['id']+'.html')).read_text(); seen=set()
 for c in item['chapters']:
  assert f'<section id="{c["id"]}" class="chapter">' in page and f'href="#{c["id"]}"' in page, f"{item['id']}: chapter {c['id']} is not reachable"
  for x in c['screens']:
   assert x['src'] not in seen, x['src']+' is used twice'; seen.add(x['src'])
   with Image.open(r/x['src']) as image: assert image.size==(x['width'],x['height']), x['src']
   assert x['src'] in page and x['label'] and x['caption'], x['src']
# The AI Media Manager prototype shows every screen of its three builds, and each chapter says what the pictures are.
aim=next(x for x in items if x['id']=='ai-media-manager')
assert [c['id'] for c in aim['chapters']]==['rebuild','planning-dashboard','first-build'] and sum(len(c['screens']) for c in aim['chapters'])>=30, 'ai-media-manager prototype screens are missing'
assert all(any(k in c['note'] for k in ['sample','placeholder','invented']) for c in aim['chapters']), 'an AI Media Manager chapter does not say its data is sample or placeholder'
assert all(any(k in x['caption'] for k in ['sample','Placeholder','placeholder']) for x in aim['screens']), 'an AI Media Manager card caption does not say its data is sample'
print("PASS: 'ai-media-manager' prototype shows every clicked-through screen of its three builds, each chapter labelled")

# Every "Built with" tag has its mark, the mark file exists and is plain drawing only, and each product page shows them.
from stack_icons import ICONS
import xml.etree.ElementTree as ET
for item in items:
 page=(r/(item['id']+'.html')).read_text()
 assert 'class="tech-label">Built with<' in page, item['id']+': the stack list lost its label'
 for tag in item['stack']:
  assert tag in ICONS, f"{item['id']}: no mark for the tag {tag!r}"
  assert f'<img src="/images/{ICONS[tag]}.svg" alt="" width="18" height="18" loading="lazy">' in page, f"{item['id']}: {tag!r} is missing its mark"
for name in sorted(set(ICONS.values())):
 path=r/'images'/(name+'.svg'); assert path.exists(), f'missing mark {name}'
 for node in ET.fromstring(path.read_text()).iter():
  assert node.tag.split('}')[-1] not in ['script','foreignObject','image','use','a'], f'{name}: unsafe SVG content'
  assert all(not key.lower().startswith('on') and key.split('}')[-1] not in ['href','src'] for key in node.attrib), f'{name}: active or external SVG content'
assert (r/'images/stack/LICENSE.txt').exists(), 'the marks need their licence notice'
print('PASS: every stack tag on every product page carries a safe, licensed mark')
