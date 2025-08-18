import os, time, json, urllib.request, subprocess
from utils import log_to, send_telegram

REPO = "https://raw.githubusercontent.com/GoGreenStoreAI/genesis/main/bots"
FILES = ["logger.py", "scheduler.py", "manager.py", "utils.py"]

def fetch(url):
    try:
        return urllib.request.urlopen(url, timeout=10).read().decode()
    except: return None

def update_file(name):
    url = f"{REPO}/{name}"
    data = fetch(url)
    if not data: return False
    local = os.path.expanduser(f"~/godai-genesis/bots/{name}")
    with open(local, "w") as f: f.write(data)
    log_to("updater.log", f"⬇️ Updated {name}")
    send_telegram(f"⬇️ Updated {name}")
    return True

if __name__ == "__main__":
    send_telegram("☁️ Cloud Updater running")
    while True:
        for f in FILES:
            update_file(f)
        time.sleep(1800)  # every 30 min
