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
