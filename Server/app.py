import flask
import threading
import subprocess
from simulate import *

app = flask.Flask(__name__)


def get_ip():
    return subprocess.Popen(
            "ifconfig"
            " | grep 'inet addr'"
            " | grep -v 127.0.0.1"
            " | sed 's/:/ : /g'"
            " | awk '{print $4}'",
        shell=True,
        stdout=subprocess.PIPE
    ).stdout.read().strip().decode('utf8')


@app.route("/")
def index():
    return "hello"



if __name__ == '__main__':
    simulate = threading.Thread(
        target=simulate,
        name="simulate"
    ).start()

    app.run(host=get_ip(), port='5000')