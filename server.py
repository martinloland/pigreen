from flask import Flask, redirect, url_for
from .util import get_config, write_config
app = Flask(__name__)

@app.route('/')
def index():
    return str(get_config())

@app.route('/set/<component>/<int:setting>')
def setter(component, setting):
    write_config({component: bool(setting)})
    return redirect(url_for('index'), code=302)

if __name__ == '__main__':
    port = 80
    app.run(host='0.0.0.0', port=port)