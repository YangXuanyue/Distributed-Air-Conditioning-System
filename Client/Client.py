from flask import Flask
from Client.simulate import *
import Client.data as data


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello what!'


if __name__ == '__main__':
    data.init()
    app.run()
