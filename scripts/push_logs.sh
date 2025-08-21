#!/bin/bash
set -e
cd ~/godai-genesis || exit 1
mkdir -p logs/archive
cp logs/*.log logs/archive/ 2>/dev/null || true
git add logs/* || true
git commit -m "Auto-log update $(date +"%Y-%m-%d %H:%M:%S %Z")" || true
git push || echo "[push_logs] push failed"
