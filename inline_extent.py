import re
import base64
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

INPUT_HTML = "extent.html"
OUTPUT_HTML = "extent.single.html"
TIMEOUT = 30

session = requests.Session()
session.headers.update({"User-Agent": "singlefile-inliner/1.0"})

def to_data_uri(content: bytes, mime: str) -> str:
    b64 = base64.b64encode(content).decode("ascii")
    return f"data:{mime};base64,{b64}"

def guess_mime(url: str) -> str:
    path = urlparse(url).path.lower()
    if path.endswith(".css"):
        return "text/css"
    if path.endswith(".js"):
        return "application/javascript"
    if path.endswith(".png"):
        return "image/png"
    if path.endswith(".jpg") or path.endswith(".jpeg"):
        return "image/jpeg"
    if path.endswith(".svg"):
        return "image/svg+xml"
    if path.endswith(".woff2"):
        return "font/woff2"
    if path.endswith(".woff"):
        return "font/woff"
    if path.endswith(".ttf"):
        return "font/ttf"
    if path.endswith(".eot"):
        return "application/vnd.ms-fontobject"
    return "application/octet-stream"

def fetch(url: str) -> bytes:
    r = session.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    return r.content

URL_IN_CSS = re.compile(r'url\(\s*(?P<q>[\'"]?)(?P<u>[^\'")]+)(?P=q)\s*\)', re.IGNORECASE)

def inline_urls_in_css(css_text: str, base_url: str) -> str:
    def repl(m):
        u = m.group("u").strip()
        # Skip already-inlined or special cases
        if u.startswith("data:") or u.startswith("#") or u.startswith("about:"):
            return m.group(0)
        abs_u = urljoin(base_url, u)
        try:
            content = fetch(abs_u)
            mime = guess_mime(abs_u)
            return f'url("{to_data_uri(content, mime)}")'
        except Exception as e:
            # Leave as-is if fetch fails
            return m.group(0)

    return URL_IN_CSS.sub(repl, css_text)

with open(INPUT_HTML, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 1) Inline external stylesheets
for link in list(soup.find_all("link", rel=lambda x: x and "stylesheet" in x)):
    href = link.get("href")
    if not href:
        continue
    if href.startswith("http://") or href.startswith("https://"):
        css_bytes = fetch(href)
        css_text = css_bytes.decode("utf-8", errors="replace")
        css_text = inline_urls_in_css(css_text, href)

        style_tag = soup.new_tag("style")
        style_tag.string = css_text
        link.replace_with(style_tag)

# 2) Inline external scripts
for script in list(soup.find_all("script")):
    src = script.get("src")
    if not src:
        continue
    if src.startswith("http://") or src.startswith("https://"):
        js = fetch(src).decode("utf-8", errors="replace")
        script.attrs.pop("src", None)
        script.string = js

# 3) Inline common image references in <link rel=icon ...>, <img src=...>
for tag in soup.find_all(["link", "img"]):
    attr = "href" if tag.name == "link" else "src"
    url = tag.get(attr)
    if not url:
        continue
    if url.startswith("http://") or url.startswith("https://"):
        try:
            content = fetch(url)
            mime = guess_mime(url)
            tag[attr] = to_data_uri(content, mime)
        except Exception:
            pass

# NOTE:
# - If your HTML has other CSS/JS references embedded via inline style blocks that reference http(s),
#   you can extend the script similarly.

out = str(soup)

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(out)

print(f"✅ Wrote single-file report: {OUTPUT_HTML}")
