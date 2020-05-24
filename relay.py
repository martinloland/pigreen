import RPi.GPIO as GPIO


class Relays(object):

    def __init__(self):
        self.relays = {
            1: {'status':False, 'bcm':19}, # 19
            2: {'status':False, 'bcm':26}, # 26
            3: {'status':False, 'bcm':20}, # 20
            4: {'status':False, 'bcm':16}, # 21
        }
        self.setup()

    def pin(self, relay):
        return self.relays[relay]['bcm']

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.pin(relay) for relay in self.relays], GPIO.OUT, initial=GPIO.HIGH)

    def __enter__(self):
        pass

    def __exit__(self, *a):
        GPIO.cleanup()
        print('GPIO cleaned up')

    def output(self, relay, value):
        "relay=int 1-4, value=True/False"
        self.relays[relay]['status'] = value
        GPIO.output(self.pin(relay), not value)
