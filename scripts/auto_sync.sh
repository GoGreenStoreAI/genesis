#!/bin/bash
set -e
cd ~/godai-genesis || exit 1

# 1) Build dashboard (never fail the pipeline if Python fails)
python3 scripts/gen_status.py || echo "[warn] gen_status.py failed, continuing"

# 2) Stage everything (including updated index.html)
git add -A

# 3) Commit with timestamp (ignore no-change error)
git commit -m "Auto-update Genesis Hub $(date '+%Y-%m-%d %H:%M:%S %Z')" || echo "No changes to commit"

# 4) Ensure tracking
git branch --set-upstream-to=origin/main main 2>/dev/null || true

# 5) Pull safely
git pull --rebase || echo "[warn] rebase failed, continuing"

# 6) Push
git push || echo "[warn] push failed (will retry next loop)"
