from bs4 import BeautifulSoup
import re, frontmatter
from markdownify import markdownify as md
from urllib.parse import urlparse
from .affiliate import ensure_amazon_in
from .config import UPI_ID, UPI_NAME, UPI_NOTE, DIR

AMZ_DOMAINS = {"amazon.com","amazon.in","amzn.to","www.amazon.com","www.amazon.in"}

def extract_text(html_or_md: str) -> str:
    if "<" in html_or_md and ">" in html_or_md:
        # looks like HTML
        return md(html_or_md)
    return html_or_md

def rewrite_affiliate_links(text_md: str) -> str:
    # Replace any Amazon links with amazon.in + tag
    url_pattern = re.compile(r'(https?://[^\s\)\]]+)', re.IGNORECASE)
    def repl(m):
        u = m.group(1)
        try:
            host = urlparse(u).netloc.lower()
            if any(host.endswith(d) for d in AMZ_DOMAINS):
                return ensure_amazon_in(u)
        except Exception:
            pass
        return u
    return url_pattern.sub(repl, text_md)

def embed_upi_block() -> str:
    upi_uri = f"upi://pay?pa={UPI_ID}&pn={UPI_NAME}&tn={UPI_NOTE}&cu=INR"
    qr_path = DIR["ROOT"] / "uploads" / "upi_qr.png"
    img_md = f'![Support via UPI]({qr_path.as_posix()})' if qr_path.exists() else ""
    block = f"""
---
**Support Our Mission — We Rise Together Forever**
- UPI: `{UPI_ID}`
- Tap to pay: `{upi_uri}`
{img_md}
---
"""
    return block

def load_frontmatter(path):
    try:
        return frontmatter.load(path)
    except Exception:
        # Fallback: raw text
        class Obj: pass
        o = Obj()
        o.content = open(path, "r", encoding="utf-8").read()
        o.metadata = {}
        return o

def compose_post_from_text(path) -> dict:
    fm = load_frontmatter(path)
    body = extract_text(fm.content)
    body = rewrite_affiliate_links(body)
    body += "\n\n" + embed_upi_block()
    title = fm.metadata.get("title") or "We Rise Together Forever"
    tags = fm.metadata.get("tags") or ["GoGreen","GodAI","Genesis"]
    return {"title": title, "content_md": body, "tags": tags}
