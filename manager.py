import datetime as dt
import time
from util import get_config, write_config

while True:
    now = dt.datetime.now()
    config = get_config()
    l_start = [int(v) for v in config["light_start"].split(":")]
    l_end = [int(v) for v in config["light_end"].split(":")]
    light_start = dt.datetime.now().replace(
        hour=l_start[0], minute=l_start[1], second=0, microsecond=0
    )
    light_end = dt.datetime.now().replace(
        hour=l_end[0], minute=l_end[1], second=0, microsecond=0
    )
    if light_start <= now <= light_end:
        light = True
    else:
        light = False
    write_config({"light": light})
    time.sleep(4)