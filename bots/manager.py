import subprocess, time
from utils import log_to, send_telegram

BOTS = [
    "logger.py",
    "scheduler.py",
    "updater.py",   # cloud auto-updater
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
