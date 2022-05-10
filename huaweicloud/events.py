import paho.mqtt.client as mqtt
import json

import utils.logger as logger
from utils.mqtt_util import on_rc
from config import config


def on_command_down(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    # Exclude respone messages
    if "response" in msg.topic:
        return

    payload = json.loads(msg.payload)
    # Down command
    if payload['service_id'] == "LightService" and payload['command_name'] == "SwitchLight":
        get_server().send_to(payload['paras']['state'])
        # cmd = {
        #     "cmd": payload['command_name']
        # }
        # local.get_local_client().publish(
        #     config['local']['topics']['down'],
        #     payload=json.dumps(cmd),
        #     qos=1
        # )

    # Respone
    resp_topic = "commands/response/".join(msg.topic.split('commands/'))
    resp_payload = {"result_code": 0}  # default: true
    client.publish(topic=resp_topic, payload=json.dumps(resp_payload))


def on_connect(client: mqtt.Client, userdata, flags, rc):
    log = f'Connect with return code: {str(rc)} ({on_rc(rc)})'
    logger.log('cloud', log)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    payload = msg.payload.decode('utf-8')
    logger.log('cloud', payload)


def on_disconnect(client, userdata, rc):
    logger.log('cloud', f"Disconnet(rc: {str(rc)})")
