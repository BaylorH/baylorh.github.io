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
assert len(p.projects)==13, 'Full directory must retain all 13 projects'
assert p.features==['fiftyflowers','till','engineering-platform'], 'Featured work must remain separate from the complete directory'
assert (r/'dist/assets/js/motion.js').exists(), 'Release must include motion module'
assert len(gzip.compress((r/'dist/assets/js/motion.js').read_bytes()))<=35000, 'Motion exceeds transfer budget'
assert (r/'dist/assets/css/refinement.css').exists(), 'Release must include refinement styles'
print('PASS: selected stories, complete directory and release motion budget')

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
  matches=[im for im in BrandImages((r/page).read_text()).images if im.get('src')==item['logo']]
  assert matches, f'{page}: missing {pid} brand art'
  assert all(im.get('width')==str(item['logoWidth']) and im.get('height')==str(item['logoHeight']) for im in matches), f'{page}: brand ratio not reserved'
for pid in ['till','engineering-platform']:
 item=next(p for p in items if p['id']==pid)
 assert item.get('image','').startswith('images/product-screens/'), f'{pid}: selected story should show the reviewed interface'
 assert item['imageCaption'], f'{pid}: interface evidence requires its caption'
 assert item['imageCaption'] in (r/(pid+'.html')).read_text(), f'{pid}: caption was lost'
print('PASS: verified brand art and reviewed selected-work screenshots retain dimensions and captions')

# Keep requested editorial order and gallery sources reliable as the collection grows.
expected=['fiftyflowers','till','engineering-platform','create-spaces','axiom','ai-media-manager','sitesift','client-portal','alpha-seo','pacman','machine-learning-visualization','lunar-base','ai-travel-companion']
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
  assert html.count('class="screen-shot ')==len(screens)
  assert html.count('data-screen-index=')==len(screens)
  assert html.count('aria-hidden="true"')==len(screens)-1
  assert 'screen-caption' in html and 'data-caption=' in html
assert next(x for x in items if x['id']=='axiom')['previewMode']=='single'
assert 'object-fit:contain' in (r/'assets/css/refinement.css').read_text()
print('PASS: directory order, unique screen sources, dimensions, keyboard-ready controls and singular Axiom cover')
