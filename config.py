import json


def _init():
    global config
    config = {}
    # Init config
    with open('config.json') as f:
        config = json.loads(f.read())
    with open('DEVICES-KEY.bib') as f:
        device_key = json.loads(f.read())
        config['device_id'] = device_key['device_id']
        config['secret'] = device_key['secret']


def get_cfg():
    return config


_init()
