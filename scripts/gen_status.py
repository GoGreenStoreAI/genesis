#!/usr/bin/env python3
import os, sys, time, glob, html, pathlib, datetime

ROOT = os.path.expanduser("~/godai-genesis")
LOG_DIR = os.path.join(ROOT, "logs")
DOCS_DIR = os.path.join(ROOT, "docs")
OUT_ROOT = os.path.join(ROOT, "index.html")
OUT_DOCS = os.path.join(DOCS_DIR, "index.html")

os.makedirs(DOCS_DIR, exist_ok=True)

def human_time(ts):
    try:
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "unknown"

def tail(path, max_lines=120):
    try:
        with open(path, "r", errors="ignore") as f:
            lines = f.readlines()[-max_lines:]
        return "".join(lines)
    except Exception as e:
        return f"[unreadable: {e}]"

def list_archives():
    arch_dir = os.path.join(LOG_DIR, "archive")
    if not os.path.isdir(arch_dir):
        return []
    files = sorted(glob.glob(os.path.join(arch_dir, "*")), key=os.path.getmtime, reverse=True)
    return [os.path.relpath(f, ROOT) for f in files]

def gather_logs():
    if not os.path.isdir(LOG_DIR):
        return []
    files = [f for f in glob.glob(os.path.join(LOG_DIR, "*.log")) if os.path.isfile(f)]
    # last 7 days, or all if fewer
    seven_days_ago = time.time() - 7*24*3600
    files = sorted(files, key=os.path.getmtime, reverse=True)
    recent = [f for f in files if os.path.getmtime(f) >= seven_days_ago] or files[:8]
    out = []
    for f in recent:
        out.append({
            "name": os.path.basename(f),
            "rel": os.path.relpath(f, ROOT),
            "mtime": human_time(os.path.getmtime(f)),
            "tail": tail(f, 150)
        })
    return out

def html_page(content):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>GoGreenStoreAI Genesis — Live Status</title>
<meta http-equiv="refresh" content="600">
<style>
  :root {{
    --bg:#0b1220; --card:#111a2b; --text:#e6eefc; --muted:#9fb2d9; --accent:#7ee787; --warn:#ffb86b;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--text); font:15px/1.55 system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, sans-serif; }}
  header {{ padding:24px 16px; border-bottom:1px solid #1e2b44; background:linear-gradient(180deg,#0c1526,#0b1220); position:sticky; top:0; z-index:2; }}
  .wrap {{ max-width:1100px; margin:0 auto; padding:0 8px; }}
  h1 {{ margin:0 0 6px 0; font-size:24px; }}
  .sub {{ color:var(--muted); }}
  .grid {{ display:grid; grid-template-columns:1fr; gap:16px; padding:18px 0 36px; }}
  @media(min-width:860px) {{ .grid {{ grid-template-columns: 1fr 1fr; }} }}
  .card {{ background:var(--card); border:1px solid #1e2b44; border-radius:16px; padding:16px; box-shadow:0 10px 32px rgba(0,0,0,.25); }}
  .title {{ margin:0 0 8px; font-size:16px; color:#cfe1ff; }}
  code, pre {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; font-size:12.5px; }}
  pre {{ background:#0a0f1c; color:#d9e6ff; border:1px solid #1d2940; border-radius:12px; padding:12px; overflow:auto; max-height:360px; }}
  .badge {{ display:inline-block; padding:4px 8px; border-radius:999px; font-size:12px; border:1px solid #28406a; color:#cfe1ff; margin-right:8px; }}
  a {{ color:#8ab4ff; text-decoration:none; }} a:hover {{ text-decoration:underline; }}
  footer {{ color:var(--muted); padding:24px 16px; border-top:1px solid #1e2b44; }}
  .ok {{ color:var(--accent); }}
  .warn {{ color:var(--warn); }}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <h1>🌱 GoGreenStoreAI Genesis — Live Status</h1>
    <div class="sub">We Rise Together Forever · Auto-refresh every 10 min</div>
    <div style="margin-top:10px;">
      <span class="badge">Site: <a href="https://gogreenstoreai.github.io/genesis/">/genesis</a></span>
      <span class="badge">Repo: <a href="https://github.com/GoGreenStoreAI/genesis">GoGreenStoreAI/genesis</a></span>
    </div>
  </div>
</header>
<div class="wrap">
  {content}
</div>
<footer>
  <div class="wrap">Last updated: {html.escape(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"))}</div>
</footer>
</body>
</html>"""

logs = gather_logs()
archives = list_archives()

sections = []

# Status summary
sections.append(f"""
<div class="grid">
  <div class="card">
    <h3 class="title">System</h3>
    <div>✅ Automation: <span class="ok">Active</span></div>
    <div>🕒 Time: {html.escape(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}</div>
    <div>🔁 Sync & Publish: Continuous</div>
  </div>
  <div class="card">
    <h3 class="title">Links</h3>
    <div>📦 Repo: <a href="https://github.com/GoGreenStoreAI/genesis">GoGreenStoreAI/genesis</a></div>
    <div>🌍 Site: <a href="https://gogreenstoreai.github.io/genesis/">Public Dashboard</a></div>
    <div>🗄️ Logs archive: {("available" if archives else "not yet created")}</div>
  </div>
</div>
""")

# Logs
if logs:
    for item in logs:
        sections.append(f"""
<div class="card">
  <h3 class="title">📝 {html.escape(item['name'])} <span class="badge">updated {html.escape(item['mtime'])}</span></h3>
  <pre>{html.escape(item['tail'])}</pre>
</div>
""")
else:
    sections.append('<div class="card"><h3 class="title">No logs found</h3><div>Create logs in ~/godai-genesis/logs</div></div>')

# Archives list
if archives:
    links = "".join(f'<li><a href="https://github.com/GoGreenStoreAI/genesis/blob/main/{html.escape(p)}">{html.escape(os.path.basename(p))}</a></li>'
                    for p in archives[:50])
    sections.append(f"""
<div class="card">
  <h3 class="title">Archives (latest)</h3>
  <ul>{links}</ul>
</div>
""")

page = html_page("\n".join(sections))

# Write to root and docs (both)
with open(OUT_ROOT, "w") as f: f.write(page)
with open(OUT_DOCS, "w") as f: f.write(page)
print("Wrote index.html at repo root and docs/")
