import arrow
from flask import Flask, redirect, url_for, render_template, request
from .util import get_config, write_config
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', config=get_config())

@app.route('/config')
def config():
    return render_template('config.html', config=get_config())

@app.route('/set/<component>/<setting>/<type_>')
def setter(component, setting, type_):
    parser = {
        'int': int, 
        'float': float, 
        'bool': lambda v: bool(int(v))
    }.get(type_, str)
    write_config({component: parser(setting)})
    return redirect(url_for('index'), code=302)

@app.route('/post', methods=["GET", "POST"])
def post():
    data = {k: v for k, v in request.form.items()}
    write_config(data)
    return redirect(url_for('index'), code=302)

@app.template_filter('arrow')
def reverse_filter(s):
    return arrow.get(s).humanize()

if __name__ == '__main__':
    port = 80
    app.run(host='0.0.0.0', port=port)