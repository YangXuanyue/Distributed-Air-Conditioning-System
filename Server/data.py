import threading
import queue
import math
import time


ROOM_NUM = 4
max_temp = 25
min_temp = 18
dflt_temp = 22
TIME_SLOT = 0.02

TEMP_EPS = 1e-4

# mode
COOLING = 0
HEATING = 1
mode = COOLING  # 0 : cooling , 1 : heating


class Item:
    def __init__(self, val):
        self.val = val
        self.lock = threading.Lock()


class Room:
    # status
    IDLE = 0
    RUNNING = 1
    SUSPENDED = 2
    DISCONNECTED = 3

    # speed
    LOW = 0
    MEDIUM = 1
    HIGH = 2

    def __init__(
            self,
            id=-1,  # = 0, 1, 2, 3
            is_checked_in=True,
            is_connected=False,  # = True, False
            # status=,  # IDLE, RUNNING, SUSPENDED, DISCONNECTED
            init_temp=-1,
            curr_temp=-1,  # = float .00
            targ_temp=dflt_temp,  # = float .00
            speed=1,  # = 0, 1, 2
            fee=.00,  # = float .00
            srv_time=.00  # float .00 /s
    ):
        self.id = id
        self.is_checked_in = is_checked_in
        self.is_connected = is_connected
        self.status = Room.DISCONNECTED
        self.init_temp = init_temp
        self.curr_temp = curr_temp
        self.targ_temp = targ_temp
        self.speed = speed
        self.fee_of_a_log = 0.
        self.fee = fee
        self.srv_time = srv_time

    def set_status(self, new_status):
        if self.status != Room.RUNNING and new_status == Room.RUNNING:
            self.fee_of_a_log = 0.
        elif self.status == Room.RUNNING and new_status != Room.RUNNING:
            logs[self.id].lock.acquire()
            log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logs[self.id].val.append(f"{log_time} {self.fee_of_a_log}")
            logs[self.id].lock.release()
        self.status = new_status

    def check_in(self):
        self.is_checked_in = True
        self.fee = 0.

    def connect(self, curr_temp):
        self.is_connected = True
        self.set_status(Room.IDLE)
        if self.init_temp == -1:
            self.init_temp = curr_temp
        self.curr_temp = curr_temp
        self.targ_temp = dflt_temp
        self.speed = Room.MEDIUM
        self.srv_time = 0

    def disconnect(self):
        self.is_connected = False
        self.set_status(Room.DISCONNECTED)

    def check_out(self):
        self.is_checked_in = False

    @staticmethod
    def calc_delta_temp_and_fee(speed):
        if speed == Room.LOW:
            return TIME_SLOT / (3. * 60.), .75 * TIME_SLOT / 60.
        elif speed == Room.MEDIUM:
            return TIME_SLOT / (2. * 60.), 1. * TIME_SLOT / 60.
        elif speed == Room.HIGH:
            return TIME_SLOT / (1. * 60.), 1.25 * TIME_SLOT / 60.

    def update(self):
        if mode == COOLING and self.curr_temp < self.targ_temp:
            return
        if mode == HEATING and self.curr_temp > self.targ_temp:
            return
        delta_temp, delta_fee = self.calc_delta_temp_and_fee(self.speed)
        self.curr_temp += (1. if mode == HEATING else -1.) \
                          * delta_temp
        self.fee += delta_fee
        self.fee_of_a_log += delta_fee
        self.srv_time += TIME_SLOT

    def is_targ_temp_reached(self):
        if mode == COOLING and self.curr_temp < self.targ_temp:
            return True
        if mode == HEATING and self.curr_temp > self.targ_temp:
            return True
        return math.fabs(self.curr_temp - self.targ_temp) < TEMP_EPS


class Inst:
    def __init__(
            self,
            # op=-1,  # 0 : tmp, 1 : speed
            room_id=-1,
            is_tuning_temp=False,
            targ_temp=-1,
            is_tuning_speed=False,
            speed=-1
    ):
        self.room_id = room_id
        self.is_tuning_temp = is_tuning_temp
        self.targ_temp = targ_temp
        self.is_tuning_speed = is_tuning_speed
        self.speed = speed


rooms = [Item(Room(id)) for id in range(ROOM_NUM)]
inst_queue = Item(queue.LifoQueue())
logs = [Item([]) for id in range(ROOM_NUM)]

