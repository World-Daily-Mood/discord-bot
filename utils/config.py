import json

config_file = "storage/config.json"

def load_config(config_file):
    with open(config_file, "r") as f:
        return json.load(f)

def get_token():
    return load_config(config_file)["token"]