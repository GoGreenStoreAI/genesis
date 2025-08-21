#!/bin/bash
while true; do
  # Core GodAI
  tmux has-session -t godai 2>/dev/null || tmux new-session -d -s godai "python ~/godai-genesis/main.py"

  # Tunnel
  tmux has-session -t godai-tunnel 2>/dev/null || tmux new-session -d -s godai-tunnel "~/godai-genesis/scripts/tunnel.sh"

  # Sync
  tmux has-session -t godai-sync 2>/dev/null || tmux new-session -d -s godai-sync "while true; do ~/godai-genesis/scripts/auto_sync.sh; sleep 300; done"

  # Logs
  tmux has-session -t godai-logs 2>/dev/null || tmux new-session -d -s godai-logs "while true; do ~/godai-genesis/scripts/push_logs.sh; sleep 600; done"

  # Watcher
  tmux has-session -t genesis-watcher 2>/dev/null || tmux new-session -d -s genesis-watcher "~/godai-genesis/scripts/watcher.sh"

  sleep 60
done
