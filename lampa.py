#!/usr/bin/python


#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep
import logger

logger.start_log()

class Button:
    def __init__(self, pin_btn=18):
        self.pin_btn = pin_btn
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_btn, GPIO.IN)
        GPIO.add_event_detect(self.pin_btn, GPIO.RISING, self.ext_button, bouncetime=300)

    def ext_button(self, pin_btn):
        if GPIO.input(self.pin_btn):
            print("Button press... detected pin#: " + str(self.pin_btn))


class Lampa(mqtt.Client):

    def init(self, name, pin, pin_btn):
        self.name = name
        self.pin = pin
        self.pin_btn = pin_btn
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 0)
        self.status = False
        GPIO.setup(self.pin_btn, GPIO.IN)
        GPIO.add_event_detect(self.pin_btn, GPIO.RISING, self.ext_button, bouncetime=300)

    def get_status(self):
        print(self.status)

    def on(self):
        GPIO.output(self.pin, 1)
        self.status = True
        print(self.name + " is on")

    def off(self):
        GPIO.output(self.pin, 0)
        self.status = False
        print(self.name + " is off")

    def ext_button(self, pin_btn):
        if GPIO.input(self.pin_btn):
            print("Button press... detected pin#: " + str(self.pin_btn))
            if self.status:
                self.off()
            else:
                self.on()
                #            client.publish("led/" + self.name + "/sub", int(self.status))
            sleep(0.1)

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        try:
            p = msg.payload.decode()
            print(msg.topic)
            if int(p) > 0:
                self.on()
                mqttc.publish("led/" + self.name + "/sub", p)
            elif int(p) == 0:
                self.off()
                mqttc.publish("led/" + self.name + "/sub", p)
        except (TypeError, ValueError) as err:
            print("error in on_message: ", err)

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def connect_subscribe(self):
        self.connect("10.0.0.200", 1883, 60)
        self.subscribe("led/" + self.name + "/pub", 0)


#btn = Button()

items_base = {'1': ['lampa1', 3, 18], '2': ['lampa2', 5, 22]}

leds = {}
for id, data in items_base.items():
    leds[id] = Lampa()
    leds[id].init(data[0], data[1], data[2])
    leds[id].connect_subscribe()

try:
    print("Press CTRL+C to exit")
    run = True
    while run:
        for id, data in leds.items():
            leds[id].loop_start()
except KeyboardInterrupt:
    print("\n\rGoodbye.")
finally:  # this block will run no matter how the try block exits
    GPIO.cleanup()  # clean up after yourself
