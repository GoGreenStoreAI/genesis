#!/data/data/com.termux/files/usr/bin/bash
set -e
cd ~/godai-genesis

python3 scripts/gen_status.py || true

git add -A
git commit -m "Auto-update Genesis Hub $(date '+%Y-%m-%d %H:%M:%S %Z')" || echo "[auto_sync] nothing to commit"
git branch --set-upstream-to=origin/main main 2>/dev/null || true
git pull --rebase || echo "[auto_sync] rebase skipped"
git push || { echo "[auto_sync] push failed, retrying in 10s..."; sleep 10; git push || echo "[auto_sync] still failed"; }
