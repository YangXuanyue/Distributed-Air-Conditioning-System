import threading


class Item:
    val = None
    lock = threading.Lock()

    def __init__(self, val):
        self.val = val


