from flask import Flask
from .util import get_config, write_config
app = Flask(__name__)

@app.route('/')
def index():
    return str(get_config())

@app.route('/set/<component>/<int:setting>')
def setter(component, setting):
    write_config({component:bool(setting)})
    return '{} turned to {}'.format(component, setting)