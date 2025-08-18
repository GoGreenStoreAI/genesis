import schedule, time
from .heartbeat import heartbeat
from .logger import log, log_exception
from .autoblogger import process_once
from .dashboard import render, update_totals

def run_forever():
    # Frequent jobs
    schedule.every(5).minutes.do(heartbeat)
    schedule.every(5).minutes.do(lambda: process_once() and update_totals(posts_inc=1))
    schedule.every(30).minutes.do(render)

    # Daily summary (IST-friendly hour; adjust if needed)
    schedule.every().day.at("21:30").do(lambda: log("daily_summary", {}))

    log("scheduler_started", {"jobs": ["heartbeat@5m","autoblogger@5m","dashboard@30m","daily@21:30"]})
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            log_exception("scheduler_error", e)
        time.sleep(1)
