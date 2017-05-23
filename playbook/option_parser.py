import os
import json
import yaml


def options_json(ansible_option):
    if os.path.isfile(str(ansible_option)):
        with open(ansible_option, "r") as f:
            _ansible_option = json.load(f)
        return json.dumps(_ansible_option)
    elif isinstance(ansible_option, dict):
        return json.dumps(ansible_option)
    elif isinstance(ansible_option, str):
        return ansible_option
    else:
        print("Wrong format!")
        return
