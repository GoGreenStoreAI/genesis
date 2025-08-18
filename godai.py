from godai.scheduler import run_forever
from godai.logger import log
if __name__ == "__main__":
    log("godai_boot", {"msg": "Genesis online"})
    run_forever()
