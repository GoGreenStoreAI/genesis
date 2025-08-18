from pathlib import Path
from dotenv import load_dotenv
import os, json

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

def env(name, default=""):
    return os.getenv(name, default).strip()

AFFILIATE_TAG = env("AFFILIATE_TAG", "gogreenstore-21")
UPI_ID = env("UPI_ID", "919209705081@sbi")
UPI_NAME = env("UPI_NAME", "Gaurav%20Lasaria")
UPI_NOTE = env("UPI_NOTE", "Genesis%20Lab%20Support")

TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = env("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = env("OPENAI_API_KEY")

PUBLISH_TARGETS = [t.strip().lower() for t in env("PUBLISH_TARGETS", "wordpress,blogger").split(",") if t.strip()]

WORDPRESS_URL = env("WORDPRESS_URL")
WP_USER = env("WP_USER")
WP_APP_PASSWORD = env("WP_APP_PASSWORD")

BLOGGER_BLOG_ID = env("BLOGGER_BLOG_ID")
GOOGLE_CLIENT_SECRET_JSON = env("GOOGLE_CLIENT_SECRET_JSON", str(ROOT / "secrets" / "client_secret.json"))

DIR = {
    "ROOT": ROOT,
    "LOGS": ROOT / "logs",
    "UPLOADS": ROOT / "uploads",
    "SITE": ROOT / "site",
    "DATA": ROOT / "data",
    "SECRETS": ROOT / "secrets",
}
for p in DIR.values():
    Path(p).mkdir(parents=True, exist_ok=True)

STATE_FILE = DIR["DATA"] / "state.json"
if not STATE_FILE.exists():
    STATE_FILE.write_text(json.dumps({"posts_total": 0, "donations_total_inr": 0.0, "affiliate_earnings_inr": 0.0}, ensure_ascii=False), encoding="utf-8")
