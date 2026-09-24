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
