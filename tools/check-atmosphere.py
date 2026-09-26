from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]
p=json.loads((r/'content/projects.json').read_text())
ml=next(x for x in p if x['id']=='machine-learning-visualization')
assert len(ml['screens'])==1, 'ML preview must show the classifier, not the menu'
assert 'MachineLearningVisualizationMenu.png' not in (r/'machine-learning-visualization.html').read_text(), 'ML menu still rendered'
html=(r/'index.html').read_text()
assert 'data-image-stream' in html and 'Pause motion' in html, 'continuous hero motion needs a usable pause control'
assert 'aria-hidden="true" class="stream-world"' in html, 'duplicated decorative screens must not duplicate accessible content'
for page in ['index.html','alpha-seo.html','create-spaces.html']:
 text=(r/page).read_text()
 assert 'class="contact-stage"' in text and 'mailto:baylor@manifoldengineering.ai' in text
 assert 'href="/resume/"' in text and 'href="/#work"' in text
css=(r/'assets/css/atmosphere.css').read_text()
assert 'prefers-reduced-motion:reduce' in css and 'animation-play-state:paused' in css
print('PASS: product-only ML imagery, decorative hero semantics/pause, responsive motion fallback and usable footer navigation')
