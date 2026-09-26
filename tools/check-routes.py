"""Verify real static clean routes, local references, and legacy redirects.

Run after build.py; pass --root dist to validate the release directory too.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import argparse
import json
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://baylor-harrison.com'


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.references = []
        self.ids = set()
        self.canonical = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        for key in ('href', 'src', 'poster'):
            if attrs.get(key):
                self.references.append(attrs[key])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs['href']


def assert_redirect(text, pathname, destination):
    scripts = re.findall(r'<script data-clean-route>(.*?)</script>', text, re.S)
    assert len(scripts) == 1, f'{pathname}: expected one compatibility redirect'
    # Execute the exact generated JavaScript. Query/hash may contain encoded data.
    location = dict(pathname=pathname, search='?from=archive%20link&x=1', hash='#product')
    harness = 'const location = ' + json.dumps(location) + ';\n'
    harness += 'let result=null;location.replace=value=>{result=value;};\n'
    harness += scripts[0] + '\nconsole.log(JSON.stringify(result));'
    output = subprocess.check_output(['node', '-e', harness], text=True)
    expected = destination + location['search'] + location['hash'] if destination else None
    assert json.loads(output) == expected, f'{pathname}: wrong redirect {output}'


def check_site(root, names):
    documents = {}
    for name in names:
        path = root / ('index.html' if name == 'index' else f'{name}/index.html')
        assert path.is_file(), f'Missing real route file: {path}'
        text = path.read_text()
        url = '/' if name == 'index' else f'/{name}/'
        document = Document(text)
        documents[url] = document
        assert document.canonical == SITE + url, f'{url}: incorrect canonical'
        assert '<h1' in text, f'{url}: missing substantive content'
        assert_redirect(text, url, None)
        assert_redirect(text, url + 'index.html', url)
        legacy = (root / f'{name}.html').read_text()
        assert_redirect(legacy, f'/{name}.html', url)
        assert '<h1' in legacy, f'{name}.html: no usable no-JavaScript fallback'
    documents['/404.html'] = Document((root / '404.html').read_text())
    assert 'data-clean-route' not in (root / '404.html').read_text(), '404 must not redirect'
    for url, document in documents.items():
        for reference in document.references:
            parsed = urlsplit(urljoin(SITE + url, reference))
            if parsed.netloc != urlsplit(SITE).netloc or parsed.scheme not in ('http', 'https'):
                continue
            assert reference.startswith('#') or not parsed.path.endswith('.html'), f'{url}: old link {reference}'
            target = root / unquote(parsed.path).lstrip('/')
            if target.is_dir():
                target /= 'index.html'
            assert target.is_file(), f'{url}: missing target {reference}'
            if parsed.fragment and parsed.path in documents:
                assert unquote(parsed.fragment) in documents[parsed.path].ids, f'{url}: missing anchor {reference}'
    sitemap = (root / 'sitemap.xml').read_text()
    assert '.html' not in sitemap, 'Sitemap contains legacy URLs'
    for url in documents:
        if url != '/404.html':
            assert f'<loc>{SITE}{url}</loc>' in sitemap, f'Sitemap missing {url}'


def check_transform():
    assert (ROOT / 'tools/routes.py').is_file(), 'Clean-route generator has not been implemented'
    from routes import build_clean_routes
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        names = ['index', 'example', 'resume']
        for name in [*names, '404']:
            root.joinpath(f'{name}.html').write_text(
                '<!doctype html><html><head><meta charset="utf-8">'
                f'<link rel="canonical" href="{SITE}/{name}.html">'
                f'<meta property="og:url" content="{SITE}/{name}.html">'
                '</head><body><h1>Page</h1><main id="product">'
                '<a href="example.html?from=home&amp;x=1#product">Project</a>'
                '<a href="index.html#product">Home</a><a href="#product">This page</a>'
                '<img src="images/test.svg"><script src="assets/test.js?v=1"></script>'
                '<a href="https://elsewhere.example/example.html">External</a>'
                '<a href="mailto:test@example.invalid">Email</a></main></body></html>'
            )
        for asset in ('images/test.svg', 'assets/test.js'):
            path = root / asset
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('fixture')
        root.joinpath('sitemap.xml').write_text('<urlset>' + ''.join(
            f'<url><loc>{SITE}/{name}.html</loc></url>' for name in names
        ) + '</urlset>')
        build_clean_routes(root, names, SITE)
        check_site(root, names)
        text = root.joinpath('example/index.html').read_text()
        assert 'href="/example/?from=home&amp;x=1#product"' in text
        assert 'https://elsewhere.example/example.html' in text
        assert f'content="{SITE}/example/"' in text
        # A repeated build must not grow redirects or change the route documents.
        before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        build_clean_routes(root, names, SITE)
        after = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        assert before == after, 'Route transformation is not idempotent'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--unit-only', action='store_true')
    args = parser.parse_args()
    check_transform()
    if not args.unit_only:
        names = ['index', 'resume'] + [p['id'] for p in json.loads((ROOT / 'content/projects.json').read_text())]
        check_site(args.root.resolve(), names)
    print('PASS: clean routes, canonical/sitemap URLs, local media and anchors, query/hash redirects, and repeatable generation.')
