#!/bin/bash
set -e
cd ~/godai-genesis || exit 1

# Kill existing sessions if any
tmux has-session -t godai-sync 2>/dev/null && tmux kill-session -t godai-sync || true
tmux has-session -t godai-logs 2>/dev/null && tmux kill-session -t godai-logs || true

# Sync loop: regenerate + push every 5 minutes
tmux new-session -d -s godai-sync "while true; do ~/godai-genesis/scripts/auto_sync.sh; sleep 300; done"

# Logs loop: snapshot & push logs every 30 minutes
tmux new-session -d -s godai-logs "while true; do ~/godai-genesis/scripts/push_logs.sh; sleep 1800; done"
