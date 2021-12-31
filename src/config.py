import json
import sys
from datetime import datetime, timedelta


lastConfigRead = timedelta(minutes=1)
interval = 1

j = None

def write_config(j):
    with open('config.json', 'w') as f:
        f.write(json.dumps(j, indent=4))

def reload_config():
    global j
    global lastConfigRead
    try:
        with open('config.json', 'r') as f:
            j = json.loads(f.read())
    except FileNotFoundError:
        with open('config.example.json', 'r') as f:
            j = json.loads(f.read())
            write_config(j)
            return reload_config()
    if j.get('WEB_CONFIG') is None:
        j['WEB_CONFIG'] = {
            "animationDuration": 6000,
            "doHide": True,
            "theme": "minecraft"
        }
        write_config(j)
    with open('web/config.json', 'w') as f:
        f.write(json.dumps(j['WEB_CONFIG'], indent=4))
    lastConfigRead = datetime.now()


reload_config()

try:
    PORT = j['PORT']
    PLATFORM = j['PLATFORM']
except FileNotFoundError:
    print("Your config file is invalid, or cannot be found. Please make sure it's saved at 'config.json'. Thanks!")
    sys.exit(1)

web_debug = j.get('WEB_DEBUG', False)


def get_spotify_config():
    if datetime.now() - lastConfigRead > timedelta(seconds=5):
        reload_config()
    SPOTIFY_BG_COLOR = j.get('SPOTIFY_CODE_BG_COLOR', "f0f0f0")
    SPOTIFY_DARK = j.get('SPOTIFY_DARK', True)
    if SPOTIFY_DARK:
        SPOTIFY_COLOR_SCHEME = 'black'
    else:
        SPOTIFY_COLOR_SCHEME = 'white'
    return SPOTIFY_BG_COLOR, SPOTIFY_COLOR_SCHEME
