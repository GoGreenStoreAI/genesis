#!/usr/bin/env python3
import json, os, time
status = {
  "heartbeat": int(time.time()*1000),
  "mirrors": {
    "github":  {"ok": True, "msg":"live", "url":"https://gogreenstoreai.github.io/genesis/"},
    "gitlab":  {"ok": False, "msg":"skipped", "url": os.getenv("GENESIS_MIRROR_GITLAB","__PLACEHOLDER__")},
    "netlify": {"ok": False, "msg":"skipped", "url": os.getenv("GENESIS_MIRROR_NETLIFY","__PLACEHOLDER__")},
    "vercel":  {"ok": False, "msg":"skipped", "url": os.getenv("GENESIS_MIRROR_VERCEL","__PLACEHOLDER__")}
  }
}
with open(os.path.expanduser("~/godai-genesis/docs/status.json"),"w") as f:
  json.dump(status,f)
print("Wrote docs/status.json")
