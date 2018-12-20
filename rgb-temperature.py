import paho.mqtt.client as mqtt
import time
import yeelight as yee
import json
import os
import random

script_dir = os.path.dirname(__file__)

#app parameters
SAMPLE_RATE = 30
TOPIC = "sensors/temp"
BULB_LOCATION="FRONT_BEDROOM"

#MQTT setup and subscription
client = mqtt.Client('rgb-bulb-controll er')
client.connect("raspberrypi")
client.subscribe("sensors/temp")

with open(os.path.join(script_dir, 'bulb-locations.json')) as f:
    bulb_locations = json.loads(f.read())

for bulb_location in bulb_locations:
    if bulb_location['location'] == BULB_LOCATION:
        bulb_id = bulb_location['id']

#bulb discovery
def getBulb():
    for bulb_meta in yee.discover_bulbs():
        if bulb_meta['capabilities']['id'] == bulb_id:
           return yee.Bulb(bulb_meta['ip'])

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

client.on_message=on_message
client.loop_start()

bulb = getBulb()
#end

while True:
    #send a messagee to all temperature sensors
    client.publish(TOPIC,"publish")
    bulb.set_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    time.sleep(SAMPLE_RATE)