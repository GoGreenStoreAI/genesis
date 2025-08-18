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
