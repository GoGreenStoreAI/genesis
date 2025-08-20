import time, subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

WATCH_DIRS = [
    os.path.expanduser("~/godai/uploads"),
    os.path.expanduser("~/godai-genesis/content")
]

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        try:
            print(f"[Watcher] Change detected: {event.src_path}")
            subprocess.run(["python", "scripts/gen_posts.py"], check=True)
            subprocess.run(["python", "scripts/gen_uploads.py"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(
                ["git", "commit", "-m", "Auto-update Genesis Hub (watcher)"],
                check=False
            )
            subprocess.run(["git", "pull", "--rebase"], check=False)
            subprocess.run(["git", "push"], check=False)
        except Exception as e:
            print("[Watcher ERROR]", e)

if __name__ == "__main__":
    event_handler = Handler()
    observer = Observer()
    for d in WATCH_DIRS:
        os.makedirs(d, exist_ok=True)
        observer.schedule(event_handler, d, recursive=True)
    observer.start()
    print("[Watcher] Genesis Hub real-time sync started forever...")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
