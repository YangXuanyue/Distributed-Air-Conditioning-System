import flask
import threading
import subprocess
from simulate import *
import data
import json
import os

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

host = get_ip()
port = '5000'

@app.route("/")
def index():
    global host, port
    return flask.render_template("index.html", host=host, port=port)


@app.route("/get_init", methods=['POST'])
def get_init():
    return json.dumps(
        {
            "mode": data.mode,
            "lowTemp": data.min_temp,
            "highTemp": data.max_temp,
            "defaultTemp": data.dflt_temp,
            "lowSpeed": .75,
            "midSpeed": 1.,
            "highSpeed": 1.25,
            "pricePerMin": 1.
        }
    )


@app.route("/set_price", methods=['POST'])
def set_price():
    return "OK"


@app.route("/set_temperature", methods=['POST'])
def set_temperature():
    pkt = flask.request.get_json(force=True)
    data.mode = pkt["mode"]
    data.min_temp = pkt["lowTemp"]
    data.max_temp = pkt["highTemp"]
    data.dflt_temp = pkt["defaultTemp"]
    return "OK"


@app.route("/set_speed", methods=['POST'])
def set_speed():
    return "OK"


@app.route("/valid", methods=['POST'])
def valid():
    return json.dumps(
        {
            "valid": True
        }
    )


@app.route("/create_admin", methods=['POST'])
def create_admin():
    return "OK"


@app.route("/turnon", methods=['POST'])
def turn_on():
    pkt = flask.request.get_json(force=True)
    data.rooms[pkt["roomId"]].val.check_in()
    return "OK"


@app.route("/turnoff", methods=['POST'])
def turn_off():
    pkt = flask.request.get_json(force=True)
    data.rooms[pkt["roomId"]].val.check_out()
    return "OK"


@app.route("/cur_state", methods=['POST'])
def get_curr_state():
    room_id = flask.request.get_json(force=True)["roomId"]
    data.rooms[room_id].lock.acquire()
    room = data.rooms[room_id].val
    res = json.dumps(
        {
            "curTemp": room.curr_temp,
            "curPrice": room.fee,
            "curMode": data.mode
        }
    )
    data.rooms[room_id].lock.release()
    return res


'''
return $http.post('/get_rooms', {
            }).then(handleSuccess, handleError('Error getRooms'));
            // rooms[4];
            // { room.curState :
            //   room.curTemp :
            //   room.aimTemp :
            //   room.curSpeed : 
            // }
'''


status_to_str = [
    "IDLE", "RUNNING", "SUSPENDED", "DISCONNECTED"
]

speed_to_str = [
    "LOW", "MEDIUM", "HIGH"
]


@app.route("/get_rooms", methods=['POST'])
def get_rooms():
    # print("get")
    for room in data.rooms:
        room.lock.acquire()

    # print("get rooms")

    res = json.dumps(
        [
            {
                "roomId": id + 1,
                "curState": status_to_str[room.val.status],
                "curTemp": room.val.curr_temp,
                "aimTemp": room.val.targ_temp,
                "curSpeed": speed_to_str[room.val.speed]
            } for id, room in enumerate(data.rooms)
        ]
    )

    # print(res)

    for room in data.rooms:
        room.lock.release()
    return res


@app.route("/show_log", methods=['POST'])
def show_log():
    log_file = open("log.txt", 'w')
    for room_id in range(data.ROOM_NUM):
        print(f"Room {room_id + 1}", file=log_file)
        data.logs[room_id].lock.acquire()
        for log in data.logs[room_id].val:
            print(log, file=log_file)
            data.logs[room_id].lock.release()
        print("", file=log_file)
    for room_id in range(data.ROOM_NUM):
        data.rooms[room_id].lock.acquire()
        print(f"Total Fee of Room {room_id + 1}: {data.rooms[room_id].val.fee}",
              file=log_file)
        data.rooms[room_id].lock.release()
    os.system("gedit log.txt")
    return "OK"


def wrap_pkt(type, pkt):
    return json.dumps(
        {
            "type": type,
            "content": json.dumps(pkt)
        }
    )


def add_header(func):
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        res = flask.Response(data)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    return wrapper


@app.route("/client-api", methods=['POST'])
@add_header
def handle():
    wrapped_pkt = flask.request.get_json(force=True)
    print(wrapped_pkt)
    # print(type(wrapped_pkt))
    try:
        pkt = json.loads(wrapped_pkt["content"])
    except:
        pkt = wrapped_pkt["content"]
    pkt_type = wrapped_pkt["type"]
    if pkt_type == "connect":
        print("connect")
        room_id = pkt["room_id"]
        data.rooms[room_id].lock.acquire()
        room = data.rooms[room_id].val
        print(room)
        if room.is_checked_in:
            print("connected")
            room.connect(pkt["init_temp"])
            print(pkt["init_temp"])
            connected = {
                "status": room.status,
                "curr_temp": room.curr_temp,
                "targ_temp": data.dflt_temp,
                "speed": room.speed,
                "fee": room.fee,
                "max_temp": data.max_temp,
                "min_temp": data.min_temp,
                "mode": data.mode
            }
            data.rooms[room_id].lock.release()
            print(connected)
            return wrap_pkt("connected", connected)
        else:
            print("reject")
            return wrap_pkt("reject", {"err_msg": "room_not_checked_in"})
    elif pkt_type == "poll":
        print("poll")
        room_id = pkt["room_id"]
        data.rooms[room_id].lock.acquire()
        room = data.rooms[room_id].val
        if pkt["type"] == 1:  # INFORM
            room.curr_temp = pkt["curr_temp"]
        poll_res = {
            "status": room.status,
            "curr_temp": room.curr_temp,
            "targ_temp": room.targ_temp,
            "speed": room.speed,
            "fee": room.fee,
            "mode": data.mode
        }
        data.rooms[room_id].lock.release()
        print("poll_res")
        print(poll_res)
        return wrap_pkt("poll_res", poll_res)
    elif pkt_type == "tune_temp":
        print("tune_temp")
        # print()
        data.inst_queue.lock.acquire()
        data.inst_queue.val.put(
            data.Inst(room_id=pkt["room_id"], is_tuning_temp=True, targ_temp=pkt["targ_temp"])
        )
        data.inst_queue.lock.release()
        return "OK"
    elif pkt_type == "tune_speed":
        print("tune_speed")
        data.inst_queue.lock.acquire()
        data.inst_queue.val.put(
            data.Inst(room_id=pkt["room_id"], is_tuning_speed=True, speed=pkt["speed"])
        )
        data.inst_queue.lock.release()
        return "OK"
    elif pkt_type == "disconnect":
        print("disconnected")
        room_id = pkt["room_id"]
        data.rooms[room_id].lock.acquire()
        data.rooms[room_id].val.disconnect()
        data.rooms[room_id].lock.release()
        return "BYE"

if __name__ == '__main__':
    simulate = threading.Thread(
        target=simulate,
        name="simulate"
    ).start()

    app.run(host=host, port=port)