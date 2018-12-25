import json
import pprint

def getConfig(file):
    with open(file, 'r') as f:
        config = json.load(f)
    return config


if __name__ == "__main__":
    config = getConfig('../resource/config-prd.json')
    pprint.pprint(config)