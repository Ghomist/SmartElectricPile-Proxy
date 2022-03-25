import paho.mqtt.client as mqtt
import json

import raspberrypie.client as local
import utils.logger as logger
from utils.mqtt_util import on_rc


def on_command_down(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    payload = json.loads(msg.payload)
    # Down command
    if payload['service_id'] == "SwitchLight":
        cmd = {
            "cmd": payload['command_name']
        }
        local.get_local_client().publish(
            "dev/01/down/cmd",
            payload=json.dumps(cmd),
            qos=1
        )


def on_connect(client: mqtt.Client, userdata, flags, rc):
    log = f'Connect with return code: {str(rc)} ({on_rc(rc)})'
    logger.log('cloud', log)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    payload = msg.payload.decode('utf-8')
    logger.log('cloud', payload)

    return

    payload = json.loads(msg.payload)
    # Down command
    if payload['service_id'] == "SwitchLight":
        cmd = {
            "cmd": payload['command_name']
        }
        local.get_local_client().publish(
            "dev/01/down/cmd",
            payload=json.dumps(cmd),
            qos=1
        )
