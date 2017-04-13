import threading
import time

MINOR_TIME_SLOT = 0.02

open_flags = [True, True, True, True]
runnings = [0, 1, 3]
waitings = [2]

def simulate():

    while True:
        if count_open_client(open_flags) > 3:
            runnings = dispatch(runnings, status)
            waitings = get_waiting(runnings, clients)
        insts = fetch_insts(runnings, insts_queue)
        update_hang_queue(hang_queue, waiting, insts_queue)
        for inst in insts:
            exec_inst(inst, status)
        time.sleep(MINOR_TIME_SLOT)