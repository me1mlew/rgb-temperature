import paho.mqtt.client as mqtt
import time
import yeelight as yee
import json
import os
import random

script_dir = os.path.dirname(__file__)

#app parameters
SAMPLE_RATE = 5
TOPIC = "sensors/temp"
BULB_LOCATION = "FRONT_BEDROOM"

TARGET_TEMP = 21
MIN_TEMP = 19.5
MAX_TEMP = 22.5

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
    tempProbe = json.loads(str(message.payload.decode("utf-8")))
    print(tempProbe['temp'])
    print(tempProbe['id'])
    
def setBulbColour(temp):
    print("colour")

client.on_message=on_message
client.loop_start()

bulb = getBulb()
#end

while True:
    #send a messagee to all temperature sensors
    client.publish(TOPIC,"publish")
    time.sleep(SAMPLE_RATE)