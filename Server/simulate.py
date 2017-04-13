import threading
import time

MINOR_TIME_SLOT = 0.02

open_flags = [True, True, True, True]
runnings = [0, 1, 3]
waitings = [2]
insts_queue = []
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

def trans_status(room):
    if room.status = 'free':
        # free -> running
        if count_run_status < 3:
            room.status = 'running'
        # free -> hang
        else:
            dispatch(room)
    elif room.status = 'hang':
        # hang -> hang
        dispatch(room)
    else:
        # running -> running
        # running -> hang
        dispatch(room)


def is_same_tmp(tmp1, tmp2):
    if abs(tmp1 - tmp2) < 1e-4:
        return True
    return False


def simulate():
    while True:

        # step1 : get insts and orders

        insts = fetch_insts(insts_queue)
        for inst in insts:
            exec_inst(inst, rooms)
        order = get_order()

        # step2 : translate the status

        for r in order:
            trans_status(r)

        # step3 : if it can be sim-ed, if it can turn to status 'free'

        for room in rooms:
            if room.status = 'running':
                room.sim()
            if is_same_tmp(room.target_tmp, room.cur_tmp):
                room.status = 'free'
        time.sleep(MINOR_TIME_SLOT)
