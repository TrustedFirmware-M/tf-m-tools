# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import subprocess
import os
import gdb

backend_has_saveload = True

qemu_mon_in_file  = None
qemu_mon_out_file = None

qemu_pid = None

def backend_start_and_reset_and_connect():
    global qemu_mon_in_file
    global qemu_mon_out_file
    global qemu_pid

    print("(Re)Starting QEMU")
    p = subprocess.run(os.path.dirname(os.path.realpath(__file__)) + "/../../fih_test_exec_qemu.sh")
    p = subprocess.run(["pgrep", "qemu-system-arm"], capture_output=True)
    qemu_pid = p.stdout.decode('utf-8').rstrip()

    try:
        gdb.execute('detach')
    except gdb.error:
        # We were probably not attached in the first place - this was post-crash
        # or first run.
        pass
    gdb.execute('target extended-remote localhost:1234')

    if qemu_mon_in_file is not None:
        qemu_mon_in_file.close()
    if qemu_mon_out_file is not None:
        qemu_mon_out_file.close()

    qemu_mon_in_file   = open("qemu_mon.in", 'w')
    qemu_mon_out_file  = open("qemu_mon.out", 'r')

def backend_reset():
    gdb.execute('detach')
    _kill_qemu()
    backend_start_and_reset_and_connect()
    print("Reset QEMU")

####################### Save / Loading #########################################

def backend_save_state(id):
    print("Saving state: {} at PC {}".format(str(id),
                                             hex(gdb.selected_frame().pc())))
    _write_fifo(qemu_mon_in_file, 'savevm {}'.format(str(id)))

def backend_load_state(id):
    _write_fifo(qemu_mon_in_file, 'loadvm {}'.format(str(id)))
    # Disconnect and reconnect to reset gdb's internal state
    gdb.execute('detach')
    gdb.execute('target extended-remote localhost:1234')
    print("Loaded state: " + str(id))

######################## Internal ##############################################

def _write_fifo(fifo, msg):
    fifo.write(msg + '\n')
    fifo.flush()

def _kill_qemu():
    global qemu_pid
    if qemu_pid is None:
        return
    p = subprocess.run(["kill", qemu_pid, "-9"])
    qemu_pid = None
