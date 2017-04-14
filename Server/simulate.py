import threading
import time
import data

# room_id is to be dispatched, the others are running


def fetch_insts():
    insts = []

    data.insts_queue.lock.acquire()

    flags = [False for i in range(4)]
    while not data.insts_queue.val.emtpy():
        inst = data.insts_queue.val.get()
        if flags[inst.room_id]:
            continue
        insts.append(inst)

    data.insts_queue.lock.release()

    insts = insts[::-1]
    return insts


def exec_inst(inst):

    # inst for tmp
    if inst.val.op == 0:
        data.rooms[inst.val.room_id].val.target_tmp = inst.val.tmp
    # inst for speed
    elif inst.val.op == 1:
        data.rooms[inst.val.room_id].val.speed = inst.val.speed
    # error
    else:
        print('Unknown instruction.')


def count_run_status():
    count = 0
    for room in data.rooms:
        if room.val.status == 'running':
            count += 1
    return count


def dispatch():
    # debug
    statuss = [room.val.status for room in data.rooms]
    print(statuss)

    # need to be debugged !!!
    # priority : low -> high
    sorted(data.rooms,
           key=lambda d: (d.val.speed, -d.val.srv_time, -d.val.id)
           )

    for i in range(4):
        if i == 0:
            data.rooms[i].val.status = 'hang'
        else:
            data.rooms[i].val.status = 'running'


def trans_status(room):
    if room.status == 'free':
        # free -> running
        if count_run_status() < 3:
            room.status = 'running'
        # free -> hang
        else:
            dispatch()
    elif room.status == 'hang':
        # hang -> hang
        dispatch()
    else:
        # running -> hang
        if count_run_status() > 3:
            dispatch()


def is_same_tmp(tmp1, tmp2):
    if abs(tmp1 - tmp2) < 1e-2:
        return True
    return False


def start_a_hang_room(rooms):
    for room in rooms:
        if room.val.status == 'hang':
            room.val.status = 'running'


def simulate():
    while True:
        for room in data.rooms:
            room.lock.acquire()

        # step1 : get insts and orders

        insts = fetch_insts()
        for inst in insts:
            exec_inst(inst)

        # step2 : translate the status

        for inst in insts:
            trans_status(data.rooms[inst.val.room_id])

        # step3 : if it can be sim-ed, if it can turn to status 'free'

        for room in data.rooms:
            if room.val.status == 'running':
                room.sim()
            if is_same_tmp(room.val.target_tmp, room.val.cur_tmp):
                room.val.status = 'free'
                start_a_hang_room()
        time.sleep(data.MINOR_TIME_SLOT)

        for room in data.rooms:
            room.lock.release()