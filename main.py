import paho.mqtt.client as mqtt
import json
from threading import Thread

import config
import huaweicloud.client as cloud
from local.local_server import SocketServer


def main():
    cfg = config.config

    # huawei cloud
    cloud.init(cfg['device_id'], cfg['secret'])
    cloud_client = cloud.get_cloud_client()
    try:
        cloud_client.connect(cfg['cloud']['url'], port=cfg['cloud']['port'])
        cloud_client.subscribe((cfg['cloud']['topics']['cmd-down'], 0))
    except ConnectionError:
        print("Failed connecting to cloud.")
        exit()

    # Start
    Thread(None, cloud_client.loop_forever).start()

    global server
    server = SocketServer(8876)
    server.start()

    # print("Connecting finished.")
    # cloud_client.disconnect()
    # local_client.disconnect()


if __name__ == "__main__":
    main()
