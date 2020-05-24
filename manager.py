import datetime as dt
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
            **get_environment(),
            "last_loop": str(now)
        })
        print(get_config())
        time.sleep(10)


def get_environment():
    humidity, temperature = Adafruit_DHT.read_retry(
        sensor=Adafruit_DHT.AM2302,
        pin=4
    )
    return {
        "humidity": round(humidity, 3),
        "temperature": round(temperature, 3),
    }


def get_pump(config, now):
    d = {}
    if config["pump_setting"] == 'auto':
        interval = dt.timedelta(minutes=int(config["pump_interval"]))
        length = dt.timedelta(minutes=int(config["pump_length"]))
        last_on = dt.datetime.fromtimestamp(config["pump_last_on"])
        on = config["pump"]
        if all([last_on + interval <= now, not on]):
            # print("on", str(now))
            d.update({
                "pump": True, "pump_last_on": now.timestamp()
            })
        elif all([now - last_on > length, on]):
            # print("off", str(now))
            d.update({
                "pump": False
            })
    elif config["pump_setting"] == 'on':
        d["pump"] = True
    elif config["pump_setting"] == 'off':
        d["pump"] = False

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