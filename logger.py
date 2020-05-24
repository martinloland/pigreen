from util import get_config, write_config
from pathlib import Path
import datetime as dt
import time

while True:
    config = get_config()
    interval = dt.timedelta(seconds=int(config["logging_interval"]))
    logging_last = dt.datetime.fromtimestamp(config["logging_last"])
    log = Path("log.txt")
    if not log.is_file():
        with open(log, "w+") as f:
            f.write(", ".join([str(k) for k, v in config.items()]))
            f.write("\n")
    if dt.datetime.now() - logging_last > interval:
        with open(log, 'a+') as f:
            f.write(", ".join([str(v) for k, v in config.items()]))
            f.write('\n')
    time.sleep(2)