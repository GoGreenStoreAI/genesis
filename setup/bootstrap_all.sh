#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "[Genesis] Preparing folders..."
mkdir -p "$HOME/godai-genesis/bots"
mkdir -p "$HOME/godai-genesis/logs"
mkdir -p "$HOME/godai-genesis/output/posts"
mkdir -p "$HOME/godai-genesis/content"
mkdir -p "/sdcard/GodAI-Genesis/updates"

# ---------- utils.py ----------
cat > "$HOME/godai-genesis/bots/utils.py" <<'PY'
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
PY

# ---------- logger.py ----------
cat > "$HOME/godai-genesis/bots/logger.py" <<'PY'
import os, time, telebot, datetime, json
from utils import send_telegram, log_to

SECRETS = os.path.expanduser("~/godai-genesis/secrets/telegram.json")
with open(SECRETS, "r") as f:
    cfg = json.load(f)

BOT_TOKEN = cfg["bot_token"]
CHAT_ID = cfg["chat_id"]

bot = telebot.TeleBot(BOT_TOKEN)

def log(message): 
    log_to("logger.log", message)

@bot.message_handler(commands=["start","alive","ping"])
def send_alive(message):
    msg = "🤖 GodAI Logger is alive and running."
    bot.reply_to(message, msg)
    log(msg)

log("✅ Logger started successfully.")
send_telegram("🚀 Logger started successfully!")

while True:
    try:
        bot.polling(none_stop=True, interval=2, timeout=20)
    except Exception as e:
        log(f"⚠️ Logger error: {e}")
        time.sleep(5)
PY

# ---------- autoblogger.py ----------
cat > "$HOME/godai-genesis/bots/autoblogger.py" <<'PY'
import os, datetime, random, textwrap
from utils import OUTDIR, log_to, send_telegram

AFFILIATE_ID = "gogreenstore-21"  # Amazon.in
TOPICS = [
    ("Solar Home Kits", "B0B3S7HXXZ"),
    ("Energy-Efficient LED Bulbs", "B07WHSJY4C"),
    ("Water Purifier Cartridges", "B07N1YF9X9"),
    ("Smart Plugs for Appliances", "B07GP59V9M"),
    ("Ergonomic Chairs", "B08W8N6D4S"),
]

def mk_post():
    dt = datetime.datetime.now()
    title, asin = random.choice(TOPICS)
    slug = f"{dt.strftime('%Y%m%d-%H%M%S')}-{title.lower().replace(' ','-')}"
    url = f"https://www.amazon.in/dp/{asin}?tag={AFFILIATE_ID}"

    body = textwrap.dedent(f"""
    # {title}: Why it’s worth it in 2025

    If you’re upgrading your setup, **{title}** is one of the simplest ways to
    save time, energy, and money. We’ve seen great results at Genesis Lab (Akurdi),
    and this is our top pick today.

    👉 Quick link: {url}

    ## What to look for
    - Build quality & durability  
    - Real-world efficiency  
    - Ease of installation

    ## How we choose
    We prioritise products with consistent customer support, strong warranties,
    and credible specs.

    *Affiliate note:* When you buy using our link, we earn a small commission at no extra cost to you.
    It directly supports the Earth Node at Genesis Lab.
    """).strip()

    path = os.path.join(OUTDIR, f"{slug}.md")
    with open(path, "w") as f:
        f.write(body + "\n")

    log_to("autoblogger.log", f"📝 Created post: {path}")
    send_telegram(f"📝 AutoBlogger posted: {title}")
    return path

if __name__ == "__main__":
    mk_post()
PY

# ---------- scheduler.py ----------
cat > "$HOME/godai-genesis/bots/scheduler.py" <<'PY'
import time, datetime, subprocess
from utils import log_to, send_telegram

# Schedule:
# - 09:30 daily: create 1 blog post
# - 21:30 daily: create 1 blog post

RUN_AT = {"09:30": "autoblogger.py", "21:30": "autoblogger.py"}
LAST_RUN = set()

def already_ran_today(tag):
    today = datetime.date.today().isoformat()
    token = f"{today}:{tag}"
    if token in LAST_RUN: 
        return True
    LAST_RUN.add(token)
    return False

def run_bot(pyfile):
    cmd = f"nohup python3 ~/godai-genesis/bots/{pyfile} >> ~/godai-genesis/logs/{pyfile}.run.log 2>&1 &"
    subprocess.Popen(cmd, shell=True)
    log_to("scheduler.log", f"▶️ Launched {pyfile}")
    send_telegram(f"▶️ Scheduler launched {pyfile}")

if __name__ == "__main__":
    send_telegram("⏰ Scheduler started")
    log_to("scheduler.log", "⏰ Scheduler started")
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now in RUN_AT and not already_ran_today(now):
            run_bot(RUN_AT[now])
        if datetime.datetime.now().strftime("%H:%M") == "00:00":
            LAST_RUN.clear()
        time.sleep(20)
PY

# ---------- monitor.py ----------
cat > "$HOME/godai-genesis/bots/monitor.py" <<'PY'
import subprocess, time
from utils import log_to

WATCH = ["logger.py", "scheduler.py", "autoblogger.py"]

def is_running(name):
    p = subprocess.run(f"ps -ef | grep {name} | grep -v grep", shell=True)
    return p.returncode == 0

if __name__ == "__main__":
    log_to("monitor.log", "👁️ Monitor started")
    while True:
        for n in WATCH:
            if not is_running(n):
                log_to("monitor.log", f"⚠️ {n} not running")
        time.sleep(60)
PY

# ---------- manager.py ----------
cat > "$HOME/godai-genesis/bots/manager.py" <<'PY'
import subprocess, time
from utils import log_to, send_telegram

BOTS = [
    "logger.py",
    "scheduler.py",
    "updater_local.py",   # pulls updates from /sdcard/GodAI-Genesis/updates
]

def is_running(name):
    p = subprocess.run(f"ps -ef | grep {name} | grep -v grep", shell=True)
    return p.returncode == 0

def start(name):
    cmd = f"nohup python3 ~/godai-genesis/bots/{name} >> ~/godai-genesis/logs/{name}.run.log 2>&1 &"
    subprocess.Popen(cmd, shell=True)
    msg = f"♻️ Started {name}"
    log_to("manager.log", msg); send_telegram(msg)

if __name__ == "__main__":
    log_to("manager.log", "🧠 Manager started"); send_telegram("🧠 Manager started")
    while True:
        for b in BOTS:
            if not is_running(b):
                start(b)
        time.sleep(10)
PY

# ---------- updater_local.py ----------
cat > "$HOME/godai-genesis/bots/updater_local.py" <<'PY'
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
PY

# ---------- watchdog.sh ----------
cat > "$HOME/godai-genesis/bots/watchdog.sh" <<'SH'
#!/data/data/com.termux/files/usr/bin/bash
LOGFILE="$HOME/godai-genesis/logs/watchdog.log"
HISTORY="$HOME/godai-genesis/logs/health_history.log"
SECRETS="$HOME/godai-genesis/secrets/telegram.json"

BOT_TOKEN=$(jq -r '.bot_token' "$SECRETS")
CHAT_ID=$(jq -r '.chat_id' "$SECRETS")

send_tg () {
  curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" -d text="$1" >/dev/null 2>&1
}

echo "$(date) - 🛡️ Watchdog started" >> "$LOGFILE"
send_tg "🛡️ Watchdog started"

while true; do
  if ! pgrep -f "logger.py" >/dev/null; then
    echo "$(date) - logger down — restarting" | tee -a "$LOGFILE" "$HISTORY" >/dev/null
    nohup python3 "$HOME/godai-genesis/bots/logger.py" >> "$HOME/godai-genesis/logs/logger_run.log" 2>&1 &
    send_tg "⚠️ Logger crashed and was restarted"
  fi

  # daily 10:00 ping
  T=$(date +%H:%M)
  D=$(date +%Y-%m-%d)
  if [ "$T" = "10:00" ] && [ ! -f "$HOME/godai-genesis/logs/.daily_$D" ]; then
    touch "$HOME/godai-genesis/logs/.daily_$D"
    echo "$(date) - ✅ Daily health: $D" | tee -a "$LOGFILE" "$HISTORY" >/dev/null
    send_tg "✅ Daily health: $D"
  fi

  # weekly Sunday 10:05 summary
  W=$(date +%u)
  if [ "$W" = "7" ] && [ "$T" = "10:05" ] && [ ! -f "$HOME/godai-genesis/logs/.weekly_$D" ]; then
    touch "$HOME/godai-genesis/logs/.weekly_$D"
    summary=$(tail -n 50 "$HISTORY" | sed 's/$/%0A/' | tr -d '\n')
    [ -z "$summary" ] && summary="(no entries yet)"
    send_tg "📊 Weekly Summary (last 50):%0A$summary"
    echo "$(date) - Weekly report sent" >> "$LOGFILE"
  fi
  sleep 60
done
SH
chmod +x "$HOME/godai-genesis/bots/watchdog.sh"

# ---------- restart_all.sh ----------
cat > "$HOME/godai-genesis/bots/restart_all.sh" <<'SH'
#!/data/data/com.termux/files/usr/bin/bash
set -e
echo "[Genesis] stopping old processes..."
pkill -f manager.py >/dev/null 2>&1 || true
pkill -f scheduler.py >/dev/null 2>&1 || true
pkill -f updater_local.py >/dev/null 2>&1 || true
pkill -f logger.py >/dev/null 2>&1 || true
pkill -f watchdog.sh >/dev/null 2>&1 || true

sleep 1
echo "[Genesis] starting watchdog..."
nohup "$HOME/godai-genesis/bots/watchdog.sh" >> "$HOME/godai-genesis/logs/watchdog_run.log" 2>&1 &

echo "[Genesis] starting manager..."
nohup python3 "$HOME/godai-genesis/bots/manager.py" >> "$HOME/godai-genesis/logs/manager_run.log" 2>&1 &

echo "[Genesis] starting scheduler..."
nohup python3 "$HOME/godai-genesis/bots/scheduler.py" >> "$HOME/godai-genesis/logs/scheduler_run.log" 2>&1 &

echo "[Genesis] all systems launched."
SH
chmod +x "$HOME/godai-genesis/bots/restart_all.sh"

echo "[Genesis] Launching all systems..."
"$HOME/godai-genesis/bots/restart_all.sh"

echo
echo "✅ Done. Quick status:"
ps -ef | grep -E "logger.py|manager.py|scheduler.py|updater_local.py|watchdog.sh" | grep -v grep || true
echo "📄 Logs in: $HOME/godai-genesis/logs"
