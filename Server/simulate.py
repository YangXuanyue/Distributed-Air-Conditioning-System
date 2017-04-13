import threading
import time

MINOR_TIME_SLOT = 0.02

open_flags = [True, True, True, True]
runnings = [0, 1, 3]
waitings = [2]
insts_queue = []
hang_queue = []
insts = []
rooms = []


def dispatch(runnings, status):
    pass
    return runnings, status


def fetch_insts(runnings, waitings, insts_queue):
    pass
    return insts, hangs


def exec_inst(inst, status):
    pass
    return


def simulate():
    while True:
        if sum(open_flags) > 3:
            runnings, waitings = dispatch(runnings, rooms)
        insts, hangs = fetch_insts(runnings, waitings, insts_queue)
        hang_queue.append(hangs)
        for inst in insts:
            exec_inst(inst, rooms)
        for room in rooms:
            room.sim()
        time.sleep(MINOR_TIME_SLOT)
