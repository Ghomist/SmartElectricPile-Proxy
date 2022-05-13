import paho.mqtt.client as mqtt
from threading import Thread

from raspberrypie.database import *
from config import *
import utils.logger as logger
from utils.mqtt_util import on_rc


class LocalClient:
    def __init__(self, client_id="mqtt_proxy", log_all=False):
        self.log = log_all

        # Client id, protocol version
        self.client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)

        # Client id, username
        # self.client.username_pw_set(username, password)

        # Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.message_callback_add(local_topics['all'], self.on_message)
        self.client.message_callback_add(local_topics['data'], self.on_data)
        self.client.message_callback_add(local_topics['report'], self.report)
        self.client.message_callback_add(local_topics['login'], self.on_login)

        self.devices_databass = DeviceDatabass(history_shape=(2000, 3))

        try:
            self.client.connect(local_url, port=local_port)
            self.client.subscribe([
                (local_topics['data'], 0),
                (local_topics['login'], 0)
            ])
        except ConnectionRefusedError:
            print("No local broker found. Try with 'mosquitto'.")
            exit()

    def start(self):
        Thread(target=self.client.loop_forever).start()

    def stop(self):
        # self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        log = f'Connect with return code: {str(rc)} ({on_rc(rc)})'
        logger.log('local', log)

    def on_login(self, client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
        id = message.payload.decode('utf-8')
        if self.devices_databass.check_id(id):
            logger.log('local', f'<{id}> has already in, skip to add')
        else:
            self.devices_databass.add(id)
            logger.log('local', f'<{id}> has logged in')

    def on_data(self, client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
        # Decode
        try:
            payload = message.payload.replace(b"'", b"\"")
            data = json.loads(payload)
        except json.JSONDecodeError:
            logger.log("local", "Decode Error!")
            return

        id = data['id']
        if not self.devices_databass.check_id(id):
            logger.log('local', f'<{id}> has not logged in but is sending msg')
            return

        data_list = data['voltage'], data['current'], data['capacity']
        self.devices_databass.store(id, data_list)

    def report(self, client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
        # TODO
        pass
        # upload payload
        # return
        # upload = {
        #     "services": [
        #         {
        #             "service_id": "CapacitanceTouch",
        #             "properties": {
        #                 "touched": touched
        #             }
        #         },
        #         {
        #             "service_id": "LightState",
        #             "properties": {
        #                 "state": light_on
        #             }
        #         }
        #     ]
        # }
        # # publish
        # cloud.get_cloud_client().publish(cloud_topics['up'], payload=json.dumps(upload))

    def on_disconnect(self, client, userdata, rc):
        logger.log('local', f"Disconnet(rc: {str(rc)})")

    def on_message(self, client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
        if self.log:
            payload = message.payload.decode('utf-8')
            logger.log('local-msg', payload)


def get_local_client():
    return client
