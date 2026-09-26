"""Create a clean release directory, never the repository root, for website hosting."""
from pathlib import Path
import json,shutil,hashlib
root=Path(__file__).resolve().parents[1]
out=root/'dist'
if out.exists():shutil.rmtree(out)
out.mkdir()
pages=['index.html','resume.html','404.html','sitemap.xml','CNAME','LICENSE.txt']+[p['id']+'.html' for p in json.loads((root/'content/projects.json').read_text())]
for name in pages:shutil.copy2(root/name,out/name)
for directory in ['images','videos','files']:shutil.copytree(root/directory,out/directory,ignore=shutil.ignore_patterns('.DS_Store'))
for name in ['assets/css/portfolio.css','assets/css/refinement.css','assets/css/atmosphere.css','assets/css/editorial.css','assets/js/portfolio.js','assets/js/analytics.js','assets/js/motion.js','assets/js/motion-license.txt']:
 dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/name,dest)
(out/'.nojekyll').write_text('')
assert not (out/'content').exists() and not (out/'tools').exists()
manifest={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}
print(f'Release ready: {out} ({len(manifest)} files; source notes and implementation archives excluded)')
