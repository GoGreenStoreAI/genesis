#!/bin/bash
tmux kill-session -t genesis-watcher 2>/dev/null
tmux new-session -d -s genesis-watcher "cd ~/godai-genesis && python scripts/watcher.py"
echo "[Genesis] Watcher started in tmux session 'genesis-watcher'"
