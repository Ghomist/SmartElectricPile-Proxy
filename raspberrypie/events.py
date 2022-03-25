import paho.mqtt.client as mqtt
import json

from config import config
import utils.logger as logger
import huaweicloud.client as cloud
from utils.mqtt_util import on_rc


def upload(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    data = json.loads(message.payload)

    # touch
    touched: int
    if data['capacitanceTouch']['value'] < 50:
        touched = 1
    else:
        touched = 0

    # light state
    light_on: int
    if data['light']['value'] == True:
        light_on = 1
    else:
        light_on = 0

    # upload payload
    upload = {
        "services": [
            {
                "service_id": "CapacitanceTouch",
                "properties": {
                    "touched": touched
                }
            },
            {
                "service_id": "LightState",
                "properties": {
                    "state": light_on
                }
            }
        ]
    }

    # publish
    cloud.get_cloud_client().publish(
        config['cloud']['topics']['up'],
        # f'$oc/devices/{config["device_id"]}/sys/properties/report',
        payload=json.dumps(upload)
    )


def on_connect(client: mqtt.Client, userdata, flags, rc):
    log = f'Connect with return code: {str(rc)} ({on_rc(rc)})'
    logger.log('local', log)


def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    payload = message.payload.decode('utf-8')
    logger.log('local', payload)
