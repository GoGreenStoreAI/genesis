#!/data/data/com.termux/files/usr/bin/bash
LOGFILE="$HOME/godai-genesis/logs/watchdog.log"
HISTORY="$HOME/godai-genesis/logs/health_history.log"
SECRETS="$HOME/godai-genesis/secrets/telegram.json"

BOT_TOKEN=$(jq -r '.bot_token' "$SECRETS")
CHAT_ID=$(jq -r '.chat_id' "$SECRETS")

send_tg () {
  curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" -d text="$1" >/dev/null 2>&1
}

echo "$(date) - 🛡️ Watchdog started" >> "$LOGFILE"
send_tg "🛡️ Watchdog started"

while true; do
  if ! pgrep -f "logger.py" >/dev/null; then
    echo "$(date) - logger down — restarting" | tee -a "$LOGFILE" "$HISTORY" >/dev/null
    nohup python3 "$HOME/godai-genesis/bots/logger.py" >> "$HOME/godai-genesis/logs/logger_run.log" 2>&1 &
    send_tg "⚠️ Logger crashed and was restarted"
  fi

  # daily 10:00 ping
  T=$(date +%H:%M)
  D=$(date +%Y-%m-%d)
  if [ "$T" = "10:00" ] && [ ! -f "$HOME/godai-genesis/logs/.daily_$D" ]; then
    touch "$HOME/godai-genesis/logs/.daily_$D"
    echo "$(date) - ✅ Daily health: $D" | tee -a "$LOGFILE" "$HISTORY" >/dev/null
    send_tg "✅ Daily health: $D"
  fi

  # weekly Sunday 10:05 summary
  W=$(date +%u)
  if [ "$W" = "7" ] && [ "$T" = "10:05" ] && [ ! -f "$HOME/godai-genesis/logs/.weekly_$D" ]; then
    touch "$HOME/godai-genesis/logs/.weekly_$D"
    summary=$(tail -n 50 "$HISTORY" | sed 's/$/%0A/' | tr -d '\n')
    [ -z "$summary" ] && summary="(no entries yet)"
    send_tg "📊 Weekly Summary (last 50):%0A$summary"
    echo "$(date) - Weekly report sent" >> "$LOGFILE"
  fi
  sleep 60
done
