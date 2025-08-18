import base64, requests
from . .config import WORDPRESS_URL, WP_USER, WP_APP_PASSWORD
from . .logger import log

def available():
    return bool(WORDPRESS_URL and WP_USER and WP_APP_PASSWORD)

def publish(post: dict):
    if not available():
        log("wp_skipped", {"reason": "credentials_missing"})
        return None
    url = WORDPRESS_URL.rstrip("/") + "/wp-json/wp/v2/posts"
    auth = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    data = {"title": post["title"], "status": "publish", "content": post["content_md"]}
    r = requests.post(url, headers=headers, json=data, timeout=60)
    try:
        r.raise_for_status()
        pid = r.json().get("id")
        log("wp_published", {"post_id": pid, "title": post["title"]})
        return pid
    except Exception as e:
        log("wp_publish_error", {"status": r.status_code, "text": r.text})
        return None
