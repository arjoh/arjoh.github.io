"""Regression checks for AJH content, routes, branding and local theme assets."""
import base64
import json
import re
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
import sys
import xml.etree.ElementTree as ET

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
DOMAIN = 'https://www.ajh-consultancy.nl'
POSTS = (
    '2015-01-04-first-post', '2015-01-15-pirates', '2015-01-19-soccer',
    '2015-01-27-dear-diary', '2015-02-13-hamlet-monologue',
    '2015-02-26-flake-it-till-you-make-it', '2015-02-28-test-markdown',
)

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.preview_count = 0
        self.elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        self.links.extend(attrs[k] for k in ('href', 'src') if k in attrs)
        self.preview_count += 'post-preview' in attrs.get('class', '').split()


def read(path):
    file = ROOT / path
    assert file.is_file(), f'Missing output: {path}'
    return file.read_text()


for route in ('index.html', 'contact/index.html', 'aboutme/index.html',
              'blog/index.html', 'blog/page2/index.html', 'tags/index.html',
              '404.html', *(f'{post}/index.html' for post in POSTS)):
    read(route)

assert not (ROOT / 'vendor').exists(), 'Bundled gems must not enter the website'
home = read('index.html')
contact = read('contact/index.html')
assert '<title>AJH Consultancy - Deze website is in aanbouw</title>' in home
assert 'Welkom op de website van AJH Consultancy.' in home
contact_page = Page(contact)
contact_elements = {attrs.get('id'): attrs for _, attrs in contact_page.elements if attrs.get('id')}
encoded = contact_elements['contactgegevens']['data-contact']
details = json.loads(bytes(b ^ 93 for b in base64.b64decode(encoded)))
assert contact_elements['show-contact-details']['aria-expanded'] == 'false'
assert contact_elements['show-contact-details']['type'] == 'button'
assert 'hidden' in contact_elements['contact-details']
assert 'Contactgegevens tonen' in contact
assert '/assets/js/contact-details.js' in contact_page.links

# None of the built text files may expose the protected values before a click.
protected = [details['email'], details['phone'], *details['address'][1:]]
for file in ROOT.rglob('*'):
    if not file.is_file():
        continue
    try:
        text = file.read_text()
    except UnicodeDecodeError:
        continue
    for value in protected:
        assert value.casefold() not in text.casefold(), f'Contact detail leaked in {file}'
    phone_digits = re.sub(r'\D', '', details['phone'])
    assert phone_digits not in re.sub(r'\D', '', text), f'Phone digits leaked in {file}'
assert '77102673' in contact and 'NL003148326B03' in contact
for html in (home, contact, read('blog/index.html')):
    assert 'Beautiful Jekyll 6.0.1' in html
    assert '/contact/#contactgegevens' in Page(html).links
    assert not any(link.startswith(('mailto:', 'tel:')) for link in Page(html).links)
    for removed in ('https://github.com/arjoh', 'https://linkedin.com/in/arjohooimeijer'):
        assert removed not in Page(html).links
    assert '/assets/css/ajh-custom.css' in Page(html).links
    assert '/assets/img/avatar-icon.png' in html

assert Page(read('blog/index.html')).preview_count == 5
assert Page(read('blog/page2/index.html')).preview_count == 2
feed = ET.fromstring(read('feed.xml'))
assert {item.findtext('link') for item in feed.findall('./channel/item')} == {
    f'{DOMAIN}/{post}/' for post in POSTS
}
ET.fromstring(read('sitemap.xml'))
css = read('assets/css/beautifuljekyll.css')
for value in ('--page-col: #fdf6e3', '--text-col: #657b83',
              '--link-col: #2aa198', '--navbar-border-col: #eee8d5'):
    assert value in css, f'Missing Solarized setting: {value}'
assert '#586e75' in read('assets/css/ajh-custom.css')
assert sha256((ROOT / 'assets/img/avatar-icon.png').read_bytes()).digest() == sha256(
    Path('img/avatar-icon.png').read_bytes()).digest(), 'Avatar was changed'

# Follow every local link and asset reference in all generated HTML.
for file in ROOT.rglob('*.html'):
    html = file.read_text()
    for link in Page(html).links:
        url = urlparse(urljoin(f'{DOMAIN}/{file.relative_to(ROOT)}', link))
        if url.netloc != urlparse(DOMAIN).netloc:
            continue
        target = ROOT / unquote(url.path.lstrip('/'))
        assert target.is_file() or (target / 'index.html').is_file(), (
            f'Broken local link in {file}: {link}'
        )
print('Passed: original pages, 7 posts, pagination, contact privacy, RSS, '
      'sitemap, Solarized colours, avatar, and all local HTML links/assets.')
