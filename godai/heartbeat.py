from time import time
from .logger import log
def heartbeat():
    log("heartbeat", {"t": int(time())})
