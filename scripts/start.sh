#!/data/data/com.termux/files/usr/bin/bash
set -e
cd ~/godai-genesis
. .venv/bin/activate
tmux has-session -t godai-genesis 2>/dev/null && tmux kill-session -t godai-genesis || true
tmux new-session -d -s godai-genesis ". .venv/bin/activate && python godai.py"
echo "Started tmux session 'godai-genesis'."
