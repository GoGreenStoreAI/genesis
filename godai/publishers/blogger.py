from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pathlib import Path
from . .config import GOOGLE_CLIENT_SECRET_JSON, BLOGGER_BLOG_ID, DIR
from . .logger import log
import json, os

SCOPES = ["https://www.googleapis.com/auth/blogger"]

def token_path():
    return DIR["SECRETS"] / "google_token.json"

def _creds():
    creds = None
    tp = token_path()
    if tp.exists():
        creds = Credentials.from_authorized_user_file(str(tp), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                pass
        else:
            if not Path(GOOGLE_CLIENT_SECRET_JSON).exists():
                log("blogger_skipped", {"reason": "client_secret_missing"})
                return None
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CLIENT_SECRET_JSON, SCOPES)
            # NOTE: First time requires local authorization flow in device browser.
            creds = flow.run_console()
        tp.write_text(creds.to_json(), encoding="utf-8")
    return creds

def available():
    return bool(BLOGGER_BLOG_ID)

def publish(post: dict):
    if not available():
        log("blogger_skipped", {"reason": "blog_id_missing"})
        return None
    creds = _creds()
    if not creds:
        return None
    service = build("blogger", "v3", credentials=creds, cache_discovery=False)
    body = {
        "kind": "blogger#post",
        "title": post["title"],
        "content": post["content_md"],
    }
    try:
        res = service.posts().insert(blogId=BLOGGER_BLOG_ID, body=body, isDraft=False).execute()
        pid = res.get("id")
        log("blogger_published", {"post_id": pid, "title": post["title"]})
        return pid
    except Exception as e:
        log("blogger_publish_error", {"error": str(e)})
        return None
