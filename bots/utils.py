import os, json, urllib.parse, urllib.request, sys

SECRETS = os.path.expanduser("~/godai-genesis/secrets/telegram.json")

def _cfg():
    with open(SECRETS,"r") as f: return json.load(f)

def send_telegram(text:str):
    try:
        c=_cfg(); token=c["bot_token"]; chat=c["chat_id"]
        msg=text[:4000]
        data = urllib.parse.urlencode({"chat_id":chat, "text":msg}).encode()
        url=f"https://api.telegram.org/bot{token}/sendMessage"
        urllib.request.urlopen(url, data=data, timeout=10)
    except Exception as e:
        # last-resort stderr so watchers can see
        print("TG_FAIL:", e, file=sys.stderr)
