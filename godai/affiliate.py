from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from .config import AFFILIATE_TAG

def ensure_amazon_in(url: str) -> str:
    p = urlparse(url.strip())
    netloc = "www.amazon.in"
    params = dict(parse_qsl(p.query, keep_blank_values=True))
    params["tag"] = AFFILIATE_TAG
    params.pop("linkCode", None)
    new = p._replace(scheme="https", netloc=netloc, query=urlencode(params, doseq=True))
    return urlunparse(new)
