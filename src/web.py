import subprocess
from werkzeug.utils import safe_join
from flask import Flask, jsonify, abort
from flask.helpers import send_file
import json
import os
import logging
import logging.handlers

from config import PORT, PLATFORM, INTEGRATED_SERVER_DEBUG, get_web_config
app = Flask(__name__, static_folder='web/static')
null_handler = logging.FileHandler(os.devnull)
f_handler = logging.FileHandler("web.py.log")



def get_file_from_theme(theme, fileName):
    # Load from default directory
    try:
        return send_file(safe_join('web', 'themes', theme, fileName))
    except FileNotFoundError:
        # Attempt to load from custom themes directory
        try:
            return send_file(safe_join('custom_themes', theme, fileName))
        except FileNotFoundError:
            # Yeah, nothing here either!
            abort(404)


@app.route('/config')
def config():
    return jsonify(get_web_config())


@app.route('/song')
def song():
    with open('web/song.json', 'r') as f:
        return jsonify(json.loads(f.read()))


@app.route('/themes/<theme>/<fileName>')
def theme_file(theme, fileName):
    app.logger.warning("{} - {}".format(theme, fileName))
    return get_file_from_theme(theme, fileName)


@app.route('/')
def index():
    with open('web/index.html', 'r') as f:
        return f.read()


@app.route('/<fileName>')
def fileName(fileName):
    """
    Serve arbitrary files from the web directory not covered by other routes.
    """
    app.logger.warning(
        "Serving arbitrary file: {} - please setup explicit route!".format(fileName))
    try:
        return send_file(safe_join('web', fileName))
    except FileNotFoundError:
        abort(404)


def start_server():
    app.config['ENV'] = 'integratedServer'
    if INTEGRATED_SERVER_DEBUG:
        logging.getLogger('werkzeug').addHandler(f_handler)
        app.logger.addHandler(f_handler)
        app.logger.setLevel("ERROR")
        logging.getLogger('werkzeug').handlers = [null_handler]
        app.logger.handlers = [null_handler]
        print('Integrated server debug mode enabled - logging to web.py.log')
    else:
        # TODO: Log errors to server when not in debug mode, so we can at least get crash reports from users
        logging.getLogger('werkzeug').handlers = [null_handler]
        app.logger.handlers = [null_handler]
    app.run(host='127.0.0.1', port=PORT)


if __name__ == '__main__':
    start_server()
