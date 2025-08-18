from pathlib import Path
from .config import DIR, PUBLISH_TARGETS
from .logger import log, log_exception
from .content import compose_post_from_text
from .publishers import wordpress as wp
from .publishers import blogger as bl

SUPPORTED_TEXT = (".md", ".markdown", ".txt", ".html", ".htm")

def scan_uploads():
    up = Path(DIR["UPLOADS"])
    files = sorted([p for p in up.glob("**/*") if p.is_file() and p.suffix.lower() in SUPPORTED_TEXT])
    return files

def publish_post(post: dict):
    results = {}
    for target in PUBLISH_TARGETS:
        if target == "wordpress":
            results["wordpress"] = wp.publish(post)
        elif target == "blogger":
            results["blogger"] = bl.publish(post)
        else:
            log("publish_unknown_target", {"target": target})
    return results

def process_once():
    files = scan_uploads()
    if not files:
        return False
    f = files[0]
    try:
        post = compose_post_from_text(f)
        log("post_composed", {"file": f.name, "title": post["title"]})
        res = publish_post(post)
        # Always write rendered version to site/drafts for backup
        out = DIR["SITE"] / "drafts"
        out.mkdir(parents=True, exist_ok=True)
        (out / (f.stem + ".md")).write_text(post["content_md"], encoding="utf-8")
        # Move original to /uploads/processed/
        done = DIR["UPLOADS"] / "processed"
        done.mkdir(parents=True, exist_ok=True)
        f.rename(done / f.name)
        log("post_processed", {"file": f.name, "results": res})
        return True
    except Exception as e:
        log_exception("post_error", e)
        # Move to /uploads/error/
        errd = DIR["UPLOADS"] / "error"
        errd.mkdir(parents=True, exist_ok=True)
        f.rename(errd / f.name)
        return False
