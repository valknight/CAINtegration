import json
import sys
from datetime import datetime, timedelta
from typing import Literal

lastConfigRead = timedelta(minutes=1)
interval = 1

j = None


def reload_config():
    global j
    global lastConfigRead
    with open('config.json', 'r') as f:
        j = json.loads(f.read())
    lastConfigRead = datetime.now()


reload_config()

try:
    PORT = j['PORT']
    PLATFORM = j['PLATFORM']
except FileNotFoundError:
    print("Your config file is invalid, or cannot be found. Please make sure it's saved at 'config.json'. Thanks!")
    sys.exit(1)

debug = j.get('DEBUG', False)


def get_spotify_config() -> tuple[str, Literal["black", "white"]]:
    if datetime.now() - lastConfigRead > timedelta(seconds=5):
        reload_config()
    SPOTIFY_BG_COLOR = j.get('SPOTIFY_CODE_BG_COLOR', "f0f0f0")
    SPOTIFY_DARK = j.get('SPOTIFY_DARK', True)
    if SPOTIFY_DARK:
        SPOTIFY_COLOR_SCHEME = 'black'
    else:
        SPOTIFY_COLOR_SCHEME = 'white'
    return SPOTIFY_BG_COLOR, SPOTIFY_COLOR_SCHEME
