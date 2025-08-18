import os, subprocess, time, json

BOTS = [
    "logger.py",
    # add more bots here (autoblogger.py, updater.py, etc.)
]

while True:
    for bot in BOTS:
        try:
            # Check if bot is already running
            result = subprocess.run(
                f"ps -ef | grep {bot} | grep -v grep",
                shell=True, capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"[Genesis] Restarting {bot}...")
                subprocess.Popen(f"nohup python3 ~/godai-genesis/bots/{bot} &", shell=True)
        except Exception as e:
            print(f"[Genesis][Error] {e}")
    time.sleep(10)
