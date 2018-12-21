import paho.mqtt.client as mqtt
import time
import yeelight as yee
import json
import os
import random
import math
script_dir = os.path.dirname(__file__)

#app parameters
SAMPLE_RATE = 5
TOPIC = "sensors/temp"
LOCATION = "FRONT_BEDROOM"

TARGET_TEMP = 21
MIN_TEMP = 19.5
MAX_TEMP = 22.5

#MQTT setup and subscription
client = mqtt.Client('rgb-bulb-controller')
client.connect("raspberrypi")
client.subscribe("sensors/temp")

with open(os.path.join(script_dir, 'bulb-locations.json')) as f:
    bulb_locations = json.loads(f.read())

with open(os.path.join(script_dir, 'sensor-locations.json')) as f:
    sensor_locations = json.loads(f.read())

for bulb_location in bulb_locations:
    if bulb_location['location'] == LOCATION:
        bulb_id = bulb_location['id']
        print(bulb_id)

for sensor_location in sensor_locations:
    if sensor_location['location'] == LOCATION:
        sensor_id = sensor_location['id']

#bulb discovery
def getBulb():
    print(yee.discover_bulbs())
    for bulb_meta in yee.discover_bulbs():
        if bulb_meta['capabilities']['id'] == bulb_id:
           return yee.Bulb(bulb_meta['ip'])

def on_message(client, userdata, message):
    tempProbe = json.loads(str(message.payload.decode("utf-8")))

    print(tempProbe['temp'])

    if (tempProbe['id']==sensor_id):
        setBulbColour(tempProbe['temp'])
    
def setBulbColour(temp):
    if (temp>MAX_TEMP):
        print("Too Warm!")
        tone = getPercentage(MAX_TEMP,temp)
        bulb.set_rgb(255,tone,tone)
    elif (temp<MIN_TEMP):
        print("Too cold!")
        tone = getPercentage(MIN_TEMP,temp)
        print("tone:{}".format(str(tone)))
        bulb.set_rgb(tone,tone,255)
    else:
        print("Perfect!")
        bulb.set_rgb(255,160,160)   

     

def getPercentage(target,actual):
    difference = math.fabs(float(target)-float(actual))
    print("difference:{}".format(str(difference)))
    multi = difference/1.5
    print("multi:{}".format(str(multi)))
    return int(math.floor(255-(multi * 255)))

client.on_message=on_message
client.loop_start()

bulb = getBulb()
bulb.set_brightness(5)
#end

while True:
    #send a messagee to all temperature sensors asking them to publish
    client.publish(TOPIC,"publish")
    time.sleep(SAMPLE_RATE)