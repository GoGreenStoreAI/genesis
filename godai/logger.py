from datetime import datetime
from pathlib import Path
import json, traceback, httpx
from rich.console import Console
from .config import DIR, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

console = Console()
LOGFILE = DIR["LOGS"] / "godai.log"

def _write(line: str):
    LOGFILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def _send_telegram(text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        with httpx.Client(timeout=15) as c:
            c.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                   data={"chat_id": TELEGRAM_CHAT_ID, "text": text[:4000], "disable_web_page_preview": True})
    except Exception:
        pass

def log(event: str, data: dict | None = None, level: str = "INFO", tmsg: str | None = None):
    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    obj = {"ts": ts, "level": level, "event": event, "data": data or {}}
    line = json.dumps(obj, ensure_ascii=False)
    console.print(f"[{level}] {event} :: {data or {}}")
    _write(line)
    _send_telegram(tmsg if tmsg else f"🛰️ {event}\n{json.dumps(data or {}, ensure_ascii=False)[:1500]}")

def log_exception(event: str, err: Exception):
    tb = traceback.format_exc(limit=4)
    log(event, {"error": str(err), "trace": tb}, level="ERROR")
