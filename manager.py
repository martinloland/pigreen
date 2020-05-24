import datetime as dt
from pathlib import Path
import time
import Adafruit_DHT
from util import get_config, write_config


def main():
    while True:
        now = dt.datetime.now()
        config = get_config()
        write_config({
            **get_light(config=config, now=now),
            **get_pump(config=config, now=now),
            **get_fan(config=config, now=now),
            **get_environment(),
            "last_loop": str(now)
        })
        write_log(config=config)
        time.sleep(1)


def get_environment():
    humidity, temperature = Adafruit_DHT.read_retry(
        sensor=Adafruit_DHT.AM2302,
        pin=4
    )
    return {
        "humidity": round(humidity, 3),
        "temperature": round(temperature, 3),
    }


def write_log(config):
    interval = dt.timedelta(minutes=int(config["logging_interval"]))
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


def get_pump(config, now):
    d = {}
    if config["pump_setting"] == 'auto':
        interval = dt.timedelta(minutes=int(config["pump_interval"]))
        length = dt.timedelta(minutes=int(config["pump_length"]))
        last_on = dt.datetime.fromtimestamp(config["pump_last_on"])
        on = config["pump"]
        if all([last_on + interval <= now, not on]):
            d.update({
                "pump": True, "pump_last_on": now.timestamp()
            })
        elif all([now - last_on > length, on]):
            d.update({
                "pump": False
            })
    elif config["pump_setting"] == 'on':
        d["pump"] = True
    elif config["pump_setting"] == 'off':
        d["pump"] = False

    return d


def get_fan(config, now):
    d = {}
    if config["fan_setting"] == 'auto':
        interval = dt.timedelta(minutes=int(config["fan_interval"]))
        length = dt.timedelta(minutes=int(config["fan_length"]))
        last_on = dt.datetime.fromtimestamp(config["fan_last_on"])
        on = config["fan"]
        if all([last_on + interval <= now, not on]):
            d.update({
                "fan": True, "fan_last_on": now.timestamp()
            })
        elif all([now - last_on > length, on]):
            d.update({
                "fan": False
            })
    elif config["fan_setting"] == 'on':
        d["fan"] = True
    elif config["fan_setting"] == 'off':
        d["fan"] = False

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