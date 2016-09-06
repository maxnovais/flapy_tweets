# coding: utf-8
from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello word!'


@app.route('/hi')
def hi():
    return '<h1>Hi Human!</h1>'


@app.route('/hi/<name>')
def hi_name(name):
    return '<h1>Hi Human, your name is {}?'.format(name)


if __name__ == '__main__':
    app.run()