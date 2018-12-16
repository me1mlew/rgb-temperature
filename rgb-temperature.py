import paho.mqtt.client as mqtt
import time

#app parameters
SAMPLE_RATE = 30
TOPIC = "sensors/temp"

#MQTT setup and subscription
client = mqtt.Client('rgb-bulb-controller')
client.connect("raspberrypi")
client.subscribe("sensors/temp")

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

client.on_message=on_message
client.loop_start()
#end

while True:
    #send a messagee to all temperature sensors
    client.publish(TOPIC,"publish")
    time.sleep(SAMPLE_RATE)