import threading
import Client.data as data

MINOR_TIME_SLOT = 0.02

def tmp_simulate():
    while True:
        if room.status != 'running':
            room.sim_tmp()
