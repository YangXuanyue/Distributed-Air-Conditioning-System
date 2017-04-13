import threading


class Item:
    val = None
    lock = threading.Lock()

    def __init__(self, val):
        self.val = val

def init():
    global room_id
    room_id = Item(-1)