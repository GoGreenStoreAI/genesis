import os, json, urllib.parse, urllib.request, datetime, pathlib

ROOT = os.path.expanduser("~/godai-genesis")
LOGDIR = os.path.join(ROOT, "logs")
OUTDIR = os.path.join(ROOT, "output", "posts")
SECRETS = os.path.join(ROOT, "secrets", "telegram.json")

pathlib.Path(LOGDIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(OUTDIR).mkdir(parents=True, exist_ok=True)

def _cfg():
    with open(SECRETS, "r") as f: 
        return json.load(f)

def send_telegram(text: str):
    """Best-effort Telegram send (no crash if offline)."""
    try:
        c = _cfg()
        token = c["bot_token"]; chat = c["chat_id"]
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
        urllib.request.urlopen(url, data=data, timeout=15)
    except Exception as e:
        try:
            with open(os.path.join(LOGDIR, "telegram_errors.log"), "a") as fh:
                fh.write(f"{datetime.datetime.now()} - {e}\n")
        except:
            pass

def log_to(file_name: str, message: str):
    p = os.path.join(LOGDIR, file_name)
    with open(p, "a") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")
