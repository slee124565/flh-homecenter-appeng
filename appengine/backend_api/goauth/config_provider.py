
import os
import json


@staticmethod
def get_config():
    config_json_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'config_provider.json'
    )
    if os.path.exists(config_json_file):
        with open(config_json_file) as fh:
            return json.loads(fh.read())
    else:
        return None
