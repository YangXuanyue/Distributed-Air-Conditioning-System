import threading
import time

MINOR_TIME_SLOT = 0.02

insts_queue = []
insts = []
rooms = []

# room_id is to be dispatched, the others are running

def dispatch(room_id, rooms):
    pass
    return

def fetch_insts(inst_queue):
    pass
    return insts, hangs

def exec_inst(inst, rooms):
    pass
    return

def trans_status(room):
    if room.status = 'free':
        # free -> running
        if count_run_status() < 3:
            room.status = 'running'
        # free -> hang
        else:
            dispatch(room)
    elif room.status = 'hang':
        # hang -> hang
        dispatch(room)
    else:
        # running -> hang
        if count_run_status() > 3:
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
                find_hang_room().set(status='running')
        time.sleep(MINOR_TIME_SLOT)
