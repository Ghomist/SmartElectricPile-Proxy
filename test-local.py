import paho.mqtt.client as mqtt
from threading import Thread

from config import config

print(config)
exit()


def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("[TEST] Connected local broker successfully.")
    print('[TEST] Try to publish a message with: mosquitto_pub -t "test" -m "Hello! MQTT!"')


def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    print("[TEST] RECEIVED! "+message.payload.decode('utf-8'))


client = mqtt.Client()

# Set callback functions
client.on_message = on_message
client.on_connect = on_connect

# Connect
client.connect('127.0.0.1', port=1883)

# Subscribe topic
client.subscribe(("test", 0))

# Start
Thread(None, client.loop_forever()).start()
