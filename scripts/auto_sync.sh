#!/bin/bash
set -e
cd ~/godai-genesis || exit 1

# Stage everything (including newly created files)
git add -A || true

# Commit with timestamp if there are changes
git diff --cached --quiet || git commit -m "Auto-update Genesis Hub $(date +"%Y-%m-%d %H:%M:%S %Z")"

# Ensure we're tracking origin/main
git branch --set-upstream-to=origin/main main 2>/dev/null || true

# Pull safely with rebase, falling back to stash if needed
if ! git pull --rebase; then
  echo "[auto_sync] rebase conflict -> stash"
  git stash push -u -m "autosync-$(date +%s)" || true
  git pull --rebase || true
  git stash pop || true
fi

# Push with two tries
git push || { echo "[auto_sync] first push failed; retrying..."; sleep 5; git push || echo "[auto_sync] push failed, will try next loop"; }
