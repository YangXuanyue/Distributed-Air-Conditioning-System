import threading
import queue


class Item:
    val = None
    lock = threading.Lock()

    def __init__(self, val):
        self.val = val


class Room:

    def __init__(self,
                 id=-1,  # = 0, 1, 2, 3
                 is_open=False,  # = True, False
                 status='disconnected',  # = 'free', 'running', 'hang', 'disconnected'
                 cur_tmp=-1,  # = float .00
                 target_tmp=-1,  # = float .00
                 speed=-1,  # = 0, 1, 2
                 fee_total=.00,  # = float .00
                 srv_time=.00  # float .00 /s
                 ):
        self.id = id
        self.is_open = is_open
        self.status = status
        self.cur_tmp = cur_tmp
        self.target_tmp = target_tmp
        self.speed = speed
        self.fee_total = fee_total
        self.srv_time = srv_time

        def __delta_tmp(self, speed):
            if speed == 0:
                return MINOR_TIME_SLOT*1000 / (3*6000)
            elif speed == 1:
                return MINOR_TIME_SLOT*1000 / (2*6000)
            elif speed == 2:
                return MINOR_TIME_SLOT*1000 / (1*6000)
            else:
                print('Error speed.')

        def sim(self):
            self.cur_tmp += __delta_tmp(self.speed)
            self.srv_time += MINOR_TIME_SLOT


class Inst:

    def __init__(self,
                 op=-1,  # 0 : tmp, 1 : speed
                 room_id=-1,
                 tmp=-1,
                 speed=-1
                 ):
        self.op = op
        self.room_id = room_id
        self.tmp = tmp
        self.speed = speed


MINOR_TIME_SLOT = 0.02
MODE = -1  # 0 : cooling , 1 : warming
rooms = [Item(Room(id)) for id in range(4)]
insts_queue = Item(queue.LifoQueue())