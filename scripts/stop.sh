#!/data/data/com.termux/files/usr/bin/bash
tmux has-session -t godai-genesis 2>/dev/null && tmux kill-session -t godai-genesis || true
echo "Stopped tmux session 'godai-genesis'."
