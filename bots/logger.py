import os, time, telebot, datetime, json
from utils import send_telegram, log_to

SECRETS = os.path.expanduser("~/godai-genesis/secrets/telegram.json")
with open(SECRETS, "r") as f:
    cfg = json.load(f)

BOT_TOKEN = cfg["bot_token"]
CHAT_ID = cfg["chat_id"]

bot = telebot.TeleBot(BOT_TOKEN)

def log(message): 
    log_to("logger.log", message)

@bot.message_handler(commands=["start","alive","ping"])
def send_alive(message):
    msg = "🤖 GodAI Logger is alive and running."
    bot.reply_to(message, msg)
    log(msg)

log("✅ Logger started successfully.")
send_telegram("🚀 Logger started successfully!")

while True:
    try:
        bot.polling(none_stop=True, interval=2, timeout=20)
    except Exception as e:
        log(f"⚠️ Logger error: {e}")
        time.sleep(5)
