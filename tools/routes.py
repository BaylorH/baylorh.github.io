"""Materialize directory routes for a static website served at a domain root.

Call build_clean_routes after generating the root HTML. Publish both the new
directories and the original HTML files, which remain readable compatibility
pages and immediately navigate to the canonical routes when JavaScript runs.
"""
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
import json
import re

REDIRECT = re.compile(r'<script data-clean-route>.*?</script>', re.S)
ATTRIBUTE = re.compile(r'''(?P<prefix>\b(?:href|src|poster|content)\s*=\s*)(?P<quote>["'])(?P<value>.*?)(?P=quote)''', re.S | re.I)


def build_clean_routes(root: Path, page_names, site: str):
    """Turn root pages (stems including index) into /stem/ static routes.

    All source pages must have been generated first. Assets and navigation use
    absolute root paths so direct loads, nested routes and the custom 404 work.
    The function can safely be called again on already transformed output.
    """
    root = Path(root)
    names = list(page_names)
    paths = {f'/{name}.html': '/' if name == 'index' else f'/{name}/' for name in names}
    origin = urlsplit(site)

    def rewrite_url(value):
        value = unescape(value)
        if not value or value.startswith('#'):
            return value
        parsed = urlsplit(value)
        if parsed.scheme and parsed.scheme not in ('http', 'https'):
            return value
        if parsed.netloc and parsed.netloc != origin.netloc:
            return value
        absolute = bool(parsed.scheme or parsed.netloc)
        path = urlsplit(urljoin(site.rstrip('/') + '/', value)).path
        path = paths.get(path, path)
        return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment)) if absolute else urlunsplit(('', '', path, parsed.query, parsed.fragment))

    class Rewriter(HTMLParser):
        def __init__(self, text, error_page=False):
            super().__init__(convert_charrefs=False)
            self.text = text
            self.error_page = error_page
            self.edits = []
            self.offsets = [0]
            for line in text.splitlines(keepends=True):
                self.offsets.append(self.offsets[-1] + len(line))
            self.feed(text)

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            raw = self.get_starttag_text()
            line, column = self.getpos()
            start = self.offsets[line - 1] + column
            if self.error_page and ((tag == 'link' and attrs.get('rel') == 'canonical') or (tag == 'meta' and attrs.get('property') == 'og:url')):
                updated = ''
            else:
                def attribute(match):
                    key = match['prefix'].split('=')[0].strip().lower()
                    if key == 'content' and not (tag == 'meta' and attrs.get('property') in ('og:url', 'og:image')):
                        return match[0]
                    return match['prefix'] + match['quote'] + escape(rewrite_url(match['value']), quote=True) + match['quote']
                updated = ATTRIBUTE.sub(attribute, raw)
            if updated != raw:
                self.edits.append((start, start + len(raw), updated))

        handle_startendtag = handle_starttag

        def result(self):
            result = self.text
            for start, end, updated in reversed(self.edits):
                result = result[:start] + updated + result[end:]
            return result

    for name in names:
        original = root / f'{name}.html'
        text = Rewriter(REDIRECT.sub('', original.read_text())).result()
        target = paths[f'/{name}.html']
        # A real navigation preserves bookmarks and replaces only the obsolete
        # history entry. Never rewrite the address without loading that route.
        aliases = [f'/{name}.html', target + 'index.html']
        script = '<script data-clean-route>if(' + json.dumps(aliases) + '.includes(location.pathname)){location.replace(' + json.dumps(target) + '+location.search+location.hash);}</script>'
        text = text.replace('<head>', '<head>' + script, 1)
        original.write_text(text)
        if name != 'index':
            directory = root / name
            directory.mkdir(exist_ok=True)
            (directory / 'index.html').write_text(text)

    error = root / '404.html'
    if error.exists():
        error.write_text(Rewriter(REDIRECT.sub('', error.read_text()), error_page=True).result())
    sitemap = root / 'sitemap.xml'
    if sitemap.exists():
        sitemap.write_text(re.sub(r'<loc>(.*?)</loc>', lambda match: '<loc>' + escape(rewrite_url(match[1]), quote=False) + '</loc>', sitemap.read_text()))
