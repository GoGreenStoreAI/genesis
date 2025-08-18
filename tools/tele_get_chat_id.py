import os, httpx, json
from dotenv import load_dotenv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
token = os.getenv("TELEGRAM_BOT_TOKEN","").strip()
if not token:
    print("Set TELEGRAM_BOT_TOKEN in .env first."); raise SystemExit(1)
with httpx.Client(timeout=30) as c:
    r = c.get(f"https://api.telegram.org/bot{token}/getUpdates"); r.raise_for_status()
print(json.dumps(r.json(), indent=2))
