import json, os, telebot

# Load secrets
with open(os.path.expanduser("~/godai-genesis/secrets/telegram.json")) as f:
    secrets = json.load(f)

BOT_TOKEN = secrets["bot_token"]
CHAT_ID = secrets["chat_id"]

bot = telebot.TeleBot(BOT_TOKEN)

# Send test message
bot.send_message(CHAT_ID, "🚀 PingBot test: I am alive!")
