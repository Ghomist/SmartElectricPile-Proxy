import paho.mqtt.client as mqtt

import huaweicloud.client_id_generator as generator
import huaweicloud.events as events


def init(device_id, secret):
    # Client id, username, password
    client_id, username, password = generator.generate(
        device_id, secret)

    # Client id, protocol version
    global client
    client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)

    # Client id, username
    client.username_pw_set(username, password)

    # Set callback functions
    client.on_connect = events.on_connect
    client.on_message = events.on_message


def get_cloud_client():
    return client
