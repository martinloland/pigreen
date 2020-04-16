import json

def get_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def write_config(options):
    d = get_config()
    with open('config.json', 'w') as f:
        json.dump({**d, **options}, f)
