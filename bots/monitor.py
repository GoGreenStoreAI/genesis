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
