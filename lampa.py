#!/usr/bin/python3
#import context
import paho.mqtt.client as mqtt
#import OPi.GPIO as GPIO
import RPi.GPIO as GPIO
from time import sleep


import logging
import logging.handlers
import argparse
import sys
#import time  # this is only being used as part of the example

# Deafults
LOG_FILENAME = "/home/pi/lampa/logs/log.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="lampa Python service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
        LOG_FILENAME = args.log

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

i = 0


class Lampa(mqtt.Client):
    def __init__(self,name="lampa", pin=3, pin_btn=None,clientid=None):
        self.name = name
        self.pin = pin
        self.pin_btn = pin_btn
        self._mqttc = mqtt.Client(clientid)
        self._mqttc.on_message = self.mqtt_on_message
        self._mqttc.on_connect = self.mqtt_on_connect
        self._mqttc.on_publish = self.mqtt_on_publish
        self._mqttc.on_subscribe = self.mqtt_on_subscribe
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 0)
        self.status = False
        GPIO.setup(self.pin_btn, GPIO.IN)
        GPIO.add_event_detect(self.pin_btn, GPIO.RISING, callback=self.ext_button, bouncetime=300)


    def init(self):
        pass

    def get_status(self):
        print(self.status)

    def on(self):
        GPIO.output(self.pin, 1)
        self.status = True
        print("lampa "+ self.name +" on")

    def off(self):
        GPIO.output(self.pin, 0)
        self.status = False
        print("lampa "+ self.name +" off")

    def ext_button(self, pin_btn):
        if GPIO.input(self.pin_btn):
            print("Button press... detected pin#: " + str(self.pin_btn))
            if self.status:
                self.off()
            else:
                self.on()
            #client.publish("led/" + self.name + "/sub", int(self.status))
            sleep(0.1)

    def mqtt_on_connect(self, mqttc, obj, flags, rc):
        print("rc: " + str(rc))

    # def mqtt_on_message(self, mqttc, obj, msg):
    #     print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def mqtt_on_publish(self, mqttc, obj, mid):
        print("on_publish mid: " + str(mid))

    def mqtt_on_message(self, client, userdata, msg):
        #print("on_message")
        try:
            p = msg.payload.decode()
            print(msg.topic)
            if int(p) > 0:
                self.on()
                client.publish("led/" + self.name + "/sub", p)
            elif int(p) == 0:
                self.off()
                client.publish("led/" + self.name + "/sub", p)
        except (TypeError, ValueError) as err:
            print("error in on_message: ", err)

    def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: " + self.name + " " + str(mid) + " " + str(granted_qos))

    def mqtt_on_log(self, mqttc, obj, level, string):
        print(string)

    def run(self):
        self._mqttc.connect("127.0.0.1", 1883, 60)
        self._mqttc.subscribe("led/" + self.name + "/pub" , 0)
        return "led/" + self.name + "/pub"


led1 = Lampa(name="lampa1", pin=3, pin_btn=18)
led2 = Lampa(name="lampa2", pin=5, pin_btn=22)

rc = led1.run()
rc2 = led2.run()
print("rc: "+str(rc))
print("rc2: "+str(rc2))

try:
    print("Press CTRL+C to exit")
    run = True
    while run:
        led1._mqttc.loop_start()
        led2._mqttc.loop_start()
except KeyboardInterrupt:
    print ("\n\rGoodbye.")
finally:  # this block will run no matter how the try block exits
    GPIO.cleanup()  # clean up after yourself
