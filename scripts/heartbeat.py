import os, time, subprocess, datetime
from pathlib import Path
from bots.utils import send_telegram

def git_state():
    try:
        b = subprocess.check_output("git rev-parse --abbrev-ref HEAD", shell=True).decode().strip()
        h = subprocess.check_output("git rev-parse --short HEAD", shell=True).decode().strip()
        return f"{b}@{h}"
    except: return "git:unknown"

def tmux_ls():
    try:
        out = subprocess.check_output("tmux ls", shell=True, stderr=subprocess.STDOUT).decode().strip()
        return out or "(no sessions)"
    except subprocess.CalledProcessError:
        return "(tmux not running)"

def disk_free():
    try:
        out = subprocess.check_output("df -h /data/data/com.termux/files | tail -1", shell=True).decode().split()
        return f"{out[3]} free"
    except: return "unknown"

def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = (
        "💚 Genesis Heartbeat\n"
        f"• Time: {now}\n"
        f"• Repo: {git_state()}\n"
        f"• Disk: {disk_free()}\n"
        f"• Tmux:\n{tmux_ls()}\n"
        "We Rise Together Forever."
    )
    send_telegram(msg)

if __name__ == "__main__":
    main()
