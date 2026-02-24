import json
import os

CONFIG_FILE = "config.json"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {
            "database_path": "",
            "destination_path": ""
        }

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)