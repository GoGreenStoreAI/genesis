import time, datetime, subprocess
from utils import log_to, send_telegram

# Schedule (24h IST): create post morning, report at night, then sync
RUN_AT = {
    "07:10": "daily_post.py",
    "22:05": "income_report.py",
    "22:10": "__sync__",   # special: run sync_site.sh
}

LAST_RUN = set()

def already_ran_today(tag):
    today = datetime.date.today().isoformat()
    token = f"{today}:{tag}"
    if token in LAST_RUN: return True
    LAST_RUN.add(token); return False

def run_bot(pyfile):
    cmd = f"nohup python3 ~/godai-genesis/bots/{pyfile} >> ~/godai-genesis/logs/{pyfile}.run.log 2>&1 &"
    subprocess.Popen(cmd, shell=True)
    msg = f"▶️ Launched {pyfile}"
    log_to("scheduler.log", msg); send_telegram(msg)

def run_sync():
    cmd = "nohup bash ~/godai-genesis/sync_site.sh >> ~/godai-genesis/logs/sync_site.log 2>&1 &"
    subprocess.Popen(cmd, shell=True)
    msg = "🌐 Site sync triggered"
    log_to("scheduler.log", msg); send_telegram(msg)

if __name__ == "__main__":
    send_telegram("⏰ Scheduler started (auto-posts, reports, sync)")
    log_to("scheduler.log", "⏰ Scheduler started")
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now in RUN_AT and not already_ran_today(now):
            task = RUN_AT[now]
            if task == "__sync__":
                run_sync()
            else:
                run_bot(task)
        # reset flags at midnight
        if datetime.datetime.now().strftime("%H:%M") == "00:00":
            LAST_RUN.clear()
        time.sleep(20)
