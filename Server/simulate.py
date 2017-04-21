import time
import data

# room_id is to be dispatched, the others are running


def fetch_insts():
    insts = []
    data.inst_queue.lock.acquire()
    idxes = [-1] * data.ROOM_NUM
    idx = 0
    while not data.inst_queue.val.empty():
        inst = data.inst_queue.val.get()
        if idxes[inst.room_id] != -1:
            if inst.is_tuning_temp:
                if not insts[idxes[inst.room_id]].is_tuning_temp:
                    insts[idxes[inst.room_id]].is_tuning_temp = True
                    insts[idxes[inst.room_id]].targ_temp = inst.targ_temp
            else:
                assert(inst.is_tuning_speed)
                if not insts[idxes[inst.room_id]].is_tuning_speed:
                    insts[idxes[inst.room_id]].is_tuning_speed = True
                    insts[idxes[inst.room_id]].speed = inst.speed
        else:
            insts.append(inst)
            idxes[inst.room_id] = idx
            idx += 1
    data.inst_queue.lock.release()
    insts = insts[::-1]
    return insts


def exec_inst(inst):
    # print(inst)
    if inst.is_tuning_temp:
        data.rooms[inst.room_id].val.targ_temp = inst.targ_temp
        # print(data.rooms[inst.room_id].val.targ_temp)
    if inst.is_tuning_speed:
        data.rooms[inst.room_id].val.speed = inst.speed


def count_running_status():
    count = 0
    for room in data.rooms:
        if room.val.status == data.Room.RUNNING:
            count += 1
    return count


def dispatch():
    to_sort = [(room.val.speed, -room.val.srv_time, -room_id)
               for room_id, room in enumerate(data.rooms)]

    for i, x in enumerate(sorted(to_sort)):
        if i == 0:
            data.rooms[-x[2]].val.set_status(data.Room.SUSPENDED)
        else:
            data.rooms[-x[2]].val.set_status(data.Room.RUNNING)


def trans_status(room):
    if room.status == data.Room.IDLE:
        # free -> running
        if count_running_status() < 3:
            room.set_status(data.Room.RUNNING)
        # free -> hang
        else:
            dispatch()
    elif room.status == data.Room.SUSPENDED:
        # hang -> hang
        if count_running_status() < 3:
            room.set_status(data.Room.RUNNING)
        else:
            dispatch()
    '''elif room.status == data.Room.RUNNING:
        # running -> hang
        if count_running_status() > 3:
            dispatch()'''


def run_a_suspended_room(rooms):
    for room in rooms:
        if room.val.status == data.Room.SUSPENDED:
            room.val.set_status(data.Room.RUNNING)
            return

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
            trans_status(data.rooms[inst.room_id].val)

        # step3 : if it can be sim-ed, if it can turn to status 'free'

        for room in data.rooms:
            if room.val.status == data.Room.RUNNING:
                room.val.update()
            if (room.val.status == data.Room.RUNNING
                or room.val.status == data.Room.SUSPENDED) \
                    and room.val.is_targ_temp_reached():
                room.val.set_status(data.Room.IDLE)
                run_a_suspended_room(data.rooms)

        for room in data.rooms:
            room.lock.release()

        time.sleep(data.TIME_SLOT)
