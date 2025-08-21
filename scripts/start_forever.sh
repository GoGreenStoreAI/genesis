#!/bin/bash
set -e
cd ~/godai-genesis || exit 1

# create tmux sessions if not exist
new_if_absent () {
  local name="$1" cmd="$2"
  tmux has-session -t "$name" 2>/dev/null || tmux new-session -d -s "$name" "$cmd"
}

# continuous sync every 5 min
new_if_absent godai-sync 'while true; do ~/godai-genesis/scripts/auto_sync.sh; sleep 300; done'

# hourly heartbeat (via loop to avoid relying on cron alone)
new_if_absent godai-heart 'while true; do python3 ~/godai-genesis/scripts/heartbeat.py; sleep 3600; done'

# log pusher every 2h
new_if_absent godai-logs 'while true; do ~/godai-genesis/scripts/push_logs.sh; sleep 7200; done'
