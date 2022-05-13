import paho.mqtt.client as mqtt
import json
from threading import Thread

from config import *
from raspberrypie.client import LocalClient
# from huaweicloud.client import CloudClient
from utils import logger


def main():
    # huawei cloud
    # cloud_client = CloudClient(device_id, secret)
    # cloud_client.start()

    # raspberry pie
    local_client = LocalClient(log_all=True)
    local_client.start()

    while True:
        cmd = input()
        if cmd == 'stop':
            local_client.stop()
            # cloud_client.stop()
            logger.log('cmd', 'Exiting')
            exit()
        else:
            logger.log('cmd', 'No such command')


if __name__ == "__main__":
    main()
