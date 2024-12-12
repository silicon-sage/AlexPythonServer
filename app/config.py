import json

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            "config.json not found. Please create a config file with Redis connection details."
        )
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in config.json")