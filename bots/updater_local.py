import os, time, shutil
from utils import send_telegram, log_to

SRC_DIR = "/sdcard/GodAI-Genesis/updates"
DST_DIR = os.path.expanduser("~/godai-genesis/bots")

log_to("updater_local.log", "🔄 Local updater started")
send_telegram("🔄 Local updater started")

def newer(src, dst):
    if not os.path.exists(dst): 
        return True
    return os.path.getmtime(src) > os.path.getmtime(dst)

while True:
    try:
        if os.path.isdir(SRC_DIR):
            for name in os.listdir(SRC_DIR):
                if not name.endswith(".py"): 
                    continue
                s = os.path.join(SRC_DIR, name)
                d = os.path.join(DST_DIR, name)
                if newer(s, d):
                    shutil.copy2(s, d)
                    m = f"✅ Updated {name} from local updates"
                    log_to("updater_local.log", m); send_telegram(m)
    except Exception as e:
        log_to("updater_local.log", f"⚠️ Updater error: {e}")
    time.sleep(300)
