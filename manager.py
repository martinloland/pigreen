import datetime as dt
from pathlib import Path
import time
import Adafruit_DHT
from util import get_config, write_config, free_drive_space
from relay import Relays


def main():
    relays = Relays()
    with relays:
        while True:
            now = dt.datetime.now()
            config = get_config()
            write_config({
                **get_light(config=config, now=now),
                **get_interval_relay(config=config, now=now, relay="pump"),
                **get_interval_relay(config=config, now=now, relay="fan"),
                **get_interval_relay(config=config, now=now, relay="breeze"),
                **get_environment(),
                **write_log(config=config, now=now),
                "last_loop": now.timestamp(),
                "free_drive_space": free_drive_space(as_string=True)
            })
            set_relay(relays=relays)
            
            time.sleep(1)


def set_relay(relays):
    config = get_config()
    relays.output(
        relay=int(config["channel_light"]), 
        value=config["light"]
    )
    relays.output(
        relay=int(config["channel_pump"]), 
        value=config["pump"]
    )
    relays.output(
        relay=int(config["channel_fan"]), 
        value=config["fan"]
    )
    relays.output(
        relay=int(config["channel_breeze"]), 
        value=config["breeze"]
    )


def get_environment():
    humidity, temperature = Adafruit_DHT.read_retry(
        sensor=Adafruit_DHT.AM2302,
        pin=4,
        retries=5,
    )
    return {
        "humidity": 0 if not humidity else round(humidity, 3),
        "temperature": 0 if not temperature else round(temperature, 3),
    }


def write_log(config, now):
    d = {}
    interval = dt.timedelta(minutes=int(config["logging_interval"]))
    logging_last = dt.datetime.fromtimestamp(config["logging_last"])
    config.update({"time": now.timestamp()})
    log = Path("log.txt")
    if not log.is_file():
        with open(log, "w+") as f:
            f.write(", ".join([str(k) for k, v in config.items()]))
            f.write("\n")
    if dt.datetime.now() - logging_last > interval:
        with open(log, 'a+') as f:
            f.write(", ".join([str(v) for k, v in config.items()]))
            f.write('\n')
        d.update({"logging_last": now.timestamp()})
    return d


def get_interval_relay(config, now, relay):
    d = {}
    if config[f"{relay}_setting"] == 'auto':
        interval = dt.timedelta(minutes=int(config[f"{relay}_interval"]))
        length = dt.timedelta(minutes=int(config[f"{relay}_length"]))
        last_on = dt.datetime.fromtimestamp(config[f"{relay}_last_on"])
        on = config[relay]
        if all([last_on + interval <= now, not on]):
            d.update({
                relay: True, f"{relay}_last_on": now.timestamp()
            })
        elif all([now - last_on > length, on]):
            d.update({
                f"{relay}": False
            })
    elif config[f"{relay}_setting"] == 'on':
        d[relay] = True
    elif config[f"{relay}_setting"] == 'off':
        d[relay] = False

    return d


def get_light(config, now):
    if config["light_setting"] == 'auto':
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
    elif config["light_setting"] == 'on':
        light = True
    elif config["light_setting"] == 'off':
        light = False
    return {"light": light}

if __name__ == "__main__":
    main()