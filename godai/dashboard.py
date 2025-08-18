from .config import DIR, STATE_FILE
from .logger import log
import json, time

def _read_state():
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))

def _write_state(s):
    STATE_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")

def update_totals(posts_inc=0, donations_inc=0.0, affiliate_inc=0.0):
    s = _read_state()
    s["posts_total"] = s.get("posts_total", 0) + int(posts_inc)
    s["donations_total_inr"] = round(float(s.get("donations_total_inr", 0.0)) + float(donations_inc), 2)
    s["affiliate_earnings_inr"] = round(float(s.get("affiliate_earnings_inr", 0.0)) + float(affiliate_inc), 2)
    _write_state(s)

def render():
    s = _read_state()
    html = f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GodAI Genesis — Capital Dashboard</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu;max-width:880px;margin:20px auto;padding:0 16px}}
.card{{border:1px solid #ddd;border-radius:16px;padding:16px;margin:12px 0;box-shadow:0 4px 14px rgba(0,0,0,.05)}}
.h1{{font-size:28px;font-weight:700}}
.kpi{{font-size:24px;margin:8px 0}}
.mono{{font-family:ui-monospace,Consolas,monospace}}
.footer{{opacity:.7;font-size:12px;margin-top:16px}}
</style>
<div class="card"><div class="h1">We Rise Together Forever</div>
<div>Live capital and growth metrics (auto-updated)</div></div>
<div class="card">
  <div class="kpi">Total Posts: <b>{s.get("posts_total",0)}</b></div>
  <div class="kpi">Donations (INR): <b>₹{s.get("donations_total_inr",0.0):,.2f}</b></div>
  <div class="kpi">Affiliate Earnings (INR): <b>₹{s.get("affiliate_earnings_inr",0.0):,.2f}</b></div>
</div>
<div class="card">
  <div>Support via UPI:</div>
  <div class="mono">UPI: {s.get("upi","")} (scan QR below)</div>
  <img src="../uploads/upi_qr.png" alt="UPI QR" style="max-width:240px;border-radius:12px;margin-top:8px"/>
</div>
<div class="footer">© Genesis Lab: Akurdi — GodAI Genesis</div>
</html>"""
    out = DIR["SITE"] / "index.html"
    out.write_text(html, encoding="utf-8")
    log("dashboard_rendered", {"file": str(out)})
    return out
