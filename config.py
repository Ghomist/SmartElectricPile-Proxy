import json


def _init():
    global config
    config = {}
    # Init config
    with open('DEVICES-KEY.bib') as f:
        config.update(json.load(f))
    with open('config.json') as f:
        config.update(json.load(f))
        # Update device id into config
        for k, topic in config['cloud']['topics'].items():
            config['cloud']['topics'][k] = topic.format(config['device_id'])


_init()
