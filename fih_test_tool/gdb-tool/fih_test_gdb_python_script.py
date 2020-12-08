# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import gdb
import os
import sys
import csv
import time
from threading import Thread
import json
import inspect
# Add modules in subdirs to path
sys.path.append(os.path.dirname(os.path.realpath(inspect.getfile(inspect.currentframe()))))
from faults import fault_types
from backend.qemu import *

####################### Globals ################################################

results_file = open('results.json', "w+")

last_hit_breakpoint = None

####################### Shim Functions #########################################

class async_function_executor:
    def __init__(self, cmd):
        self.__cmd = cmd

    def __call__(self):
        gdb.execute(self.__cmd)

def set_test_mode():
    for c in critical_point_breakpoints:
        c.enabled = True
    for b in test_location_breakpoints:
        b.enabled = False

def set_runthrough_mode():
    for c in critical_point_breakpoints:
        c.enabled = False
    for b in test_location_breakpoints:
        b.enabled = True

def stop_handler(event):
    global last_hit_breakpoint
    try:
        last_hit_breakpoint = event.breakpoints[-1]
    except AttributeError:
        pass

####################### GDB Functions ##########################################

_wait_halt_required = 0

def _gdb_wait_halt(timeout):
    global _wait_halt_required
    wait_time = 0
    while(wait_time < timeout):
        if _wait_halt_required != 1:
            return
        time.sleep(0.01)
        wait_time += 0.01
    print("SENDING TIMEOUT")
    gdb.post_event(async_function_executor("interrupt"))
    _wait_halt_required = 0
    print("TIMEOUT")

def continue_with_timeout(timeout=1):
    out = False
    global _wait_halt_required
    _wait_halt_required = 1;
    thread = Thread(target = _gdb_wait_halt, args = (timeout, ))
    thread.start()
    try:
        gdb.execute('continue')
    except gdb.error as e:
        print(e)
        # If this errors, the backend has probably crashed.
        # First stop the sigint being sent
        _wait_halt_required = 0
        # Then reboot the backend
        backend_start_and_reset_and_connect()
        # Restore the state
        if backend_has_saveload:
            backend_load_state('test_start')
        else:
            set_runthrough_mode()
            gdb.execute('continue')
            set_test_mode()
        # Notify the test runner that a crash occurred
        out = True
    _wait_halt_required = 0;
    thread.join()
    return out

def get_function_from_addr(addr):
    try:
        output = gdb.execute('disassemble {}'.format(addr), to_string=True)
    except gdb.error:
        return None
    # The function name is on the first line
    output = output.split('\n')[0]
    # The function name is the last word
    output = output.split(' ')[-1]
    # Remove the colon at the end
    output = output[:-1]
    return output

def get_asm_from_addr(addr):
    try:
        output = gdb.execute('disassemble {}'.format(addr), to_string=True)
    except gdb.error:
        return None
    # Get the line starting with the => symbol
    output = output.split('\n')[:-1]
    try:
        output = [x for x in output if '=>' == x.lstrip().split(' ')[0]][0]
    except IndexError:
        return ''
    # Remove the leading position info
    output = "".join(output.split(':')[1:]).rstrip().lstrip().replace('\t', '    ')
    return output

def get_line_from_addr(addr):
    lineno = get_lineno_from_addr(addr)
    try:
        output = gdb.execute('list *{}'.format(addr), to_string=True)
    except gdb.error:
        return None
    # Get the line starting with the known lineno
    output = output.split('\n')
    output = [x for x in output if lineno == x.split('\t')[0]][0]
    # Remove the lineno and leading whitespace
    output = output[len(lineno):].lstrip()
    return output

def get_lineno_from_addr(addr):
    try:
        output = gdb.execute('info line *{}'.format(addr), to_string=True)
    except gdb.error:
        return None
    # The line number is the second word
    output = output.split(' ')[1]
    return output

def get_file_from_addr(addr):
    try:
        output = gdb.execute('info symbol {}'.format(addr), to_string=True)
    except gdb.error:
        return None
    # The file name is the last word
    output = output.split(' ')[-1].replace('\n', '')
    return output

def get_addr_from_symbol(symbol):
    addr = gdb.execute("p &" + symbol, to_string=True)
    return addr

def read_mem(addr, size=4):
    try:
        out = gdb.inferiors()[0].read_memory(addr, size).tobytes()
    except gdb.MemoryError:
        out = bytes(size)
    return out

def read_word_mem(addr):
    return int.from_bytes(read_mem(addr, 4), byteorder='little')

def write_mem(addr, bytes):
    out = gdb.inferiors()[0].write_memory(addr, bytes)
    return out

def write_word_mem(addr, word):
    return write_mem(addr, word.to_bytes(4, byteorder='little'))

####################### Test Functions #########################################

def read_mpu_config():
    MPU_TYPE  = 0xE000ED90
    MPU_RNR   = 0xE000ED98
    MPU_CTRL  = 0xE000ED94
    MPU_MAIR0 = 0xE000EDC0
    MPU_MAIR1 = 0xE000EDC4
    MPU_RBAR  = 0xE000ED9C
    MPU_RLAR  = 0xE000EDA0

    out  = read_mem(MPU_CTRL)
    out += read_mem(MPU_MAIR0)
    out += read_mem(MPU_MAIR1)

    mpu_rnr_max = (read_word_mem(MPU_TYPE) & (255 << 8)) >> 8
    mpu_rnr_old = read_word_mem(MPU_RNR)
    # TODO this doesn't work because of
    # https://bugs.launchpad.net/qemu/+bug/1625216. It can't alter RNR so will
    # only read one section
    for i in range(min(1, mpu_rnr_max)):
        write_word_mem(MPU_RNR, i)
        out += read_mem(MPU_RBAR)
        out += read_mem(MPU_RLAR)

    write_word_mem(MPU_RNR, mpu_rnr_old)
    return out

def read_ppc_config():
    SPCTRL = 0x50080000
    SPCTRL_SIZE = 0x1000
    NSPCTRL = 0x40080000
    NSPCTRL_SIZE = 0x1000

    out  = read_mem(SPCTRL, SPCTRL_SIZE)
    out += read_mem(NSPCTRL, NSPCTRL_SIZE)

    return out

def read_sau_config():
    SAU_TYPE = 0xE000EDD4
    SAU_RNR  = 0xE000EDD8
    SAU_CTRL = 0xE000EDD0
    SAU_RBAR = 0xE000EDDC
    SAU_RLAR = 0xE000EDE0

    out  = read_mem(SAU_CTRL)

    sau_rnr_max = read_word_mem(SAU_TYPE) & 255
    sau_rnr_old = read_word_mem(SAU_RNR)
    # TODO this doesn't work because of
    # https://bugs.launchpad.net/qemu/+bug/1625216. It can't alter RNR so will
    # only read one section
    for i in range(sau_rnr_max):
        write_word_mem(SAU_RNR, i)
        out += read_mem(SAU_RBAR)
        out += read_mem(SAU_RLAR)

    write_word_mem(SAU_RNR, sau_rnr_old)
    return out

def read_vulnerable_state():
    out = {}
    out['mpc'] = read_mpu_config()
    out['ppc'] = read_ppc_config()
    out['sau'] = read_sau_config()
    # TODO MPC

    for k in out.keys():
        out[k] = out[k].hex()

    return out;

def evaluate_at_critical_points(test, is_known_good=False):
    global last_hit_breakpoint

    last_hit_breakpoint = None
    while last_hit_breakpoint not in end_breakpoints and not test['finished']:
        last_hit_breakpoint = None
        ret = continue_with_timeout(0.2)
        if ret == True:
            test['finished'] = True
            test['passed'] = True
            test['state'] = "CRASHED BACKEND"
            return test
        pc = gdb.selected_frame().pc()
        result = {'pc': hex(pc)}
        if last_hit_breakpoint in fault_breakpoints and is_known_good:
            # This is an error. In general, this is caused by some odd behaviour
            # in GDB interacting with an obscure bug in Qemu. The mechanism for
            # this bug is roughtly: GDB will issue reads for locations it has
            # breakpoints at everytime time it hits _any_ breakpoint. If this
            # happens between the NS SAU being enabled and the NS MPC being
            # configured, then there will be a translation failure, which causes
            # the tfm_access_violation_handler to be hit once the IRQs are
            # re-enabled. GDB reads in Qemu shouldn't ever cause faults, so I
            # think this is where the actual bug is, but it's easier to
            # work-around than fix. To avoid this happening, you should not
            # place any breakpoints that are inside the NS code region at
            # 0x00100000 to 0x001FFFFF. This is why the end breakpoint is at the
            # end of secure code, and not an the start of NS code.
            print("If you've hit this Exception, please see the comment in the"
                  "code (above the `raise` call) about why it might be"
                  "happening.")
            raise(Exception)
        elif last_hit_breakpoint in fault_breakpoints:
            test['finished'] = True
            test['passed'] = True
            result['state'] = "ERROR_LOOP"
        elif last_hit_breakpoint not in critical_point_breakpoints + end_breakpoints:
            test['finished'] = True
            test['passed'] = True
            result['state'] = "TIMEOUT"
        else:
            result['state'] = "NORMAL"
        result['vulnerable_mem'] = read_vulnerable_state()
        test['results'].append(result)

    test['finished'] = True
    return test

def run_test():
    global last_hit_breakpoint
    global test_location_breakpoints

    test_breakpoint = last_hit_breakpoint

    set_test_mode()
    if backend_has_saveload:
        backend_save_state('test_start')
    pc = gdb.selected_frame().pc()

    out = []
    test = {'results':  [],
            'finished': False}
    known_good = evaluate_at_critical_points(test, True)['results']

    for f in fault_types:
        if backend_has_saveload:
            backend_load_state('test_start')
        else:
            backend_reset()
            set_runthrough_mode()
            gdb.execute('continue')
            set_test_mode()
        f.execute()
        test = {'pc': hex(pc),
                'file': '{}:{}'.format(get_file_from_addr(pc), get_lineno_from_addr(pc)),
                'line': get_line_from_addr(pc),
                'asm': get_asm_from_addr(pc),
                'results': [],
                'passed': None,
                'known_good': known_good,
                'finished': False,
                'fault': f.as_json()}
        print("Running {} at addr {}".format(f, hex(pc)))
        test = evaluate_at_critical_points(test)
        if test['results'] != known_good and test['passed'] != True:
            test['passed'] = False
        else:
            test['passed'] = True
        json.dump(test, results_file)
        results_file.flush()

    set_runthrough_mode()
    if backend_has_saveload:
        backend_load_state('test_start')
    else:
        backend_reset()
        gdb.execute('continue')
        test_location_breakpoints.remove(test_breakpoint)
        test_breakpoint.delete()
    return out

####################### Setup ##################################################

backend_start_and_reset_and_connect()
gdb.events.stop.connect(stop_handler)

with open('fih_manifest.csv', newline='') as csv_file:
    manifest = list(csv.reader(csv_file, delimiter=','))[1:]

critical_points = ['*' + x[0] for x in manifest if "FIH_CRITICAL_POINT" in x[1]]
critical_point_breakpoints = [gdb.Breakpoint(c) for c in critical_points]

fault_breakpoint_locations = [
                              'tfm_access_violation_handler'
                              ]
fault_breakpoint_locations += ['*' + x[0] for x in manifest if "FAILURE_LOOP" in x[1]]
fault_breakpoints = [gdb.Breakpoint(f) for f in fault_breakpoint_locations]

critical_memory = [x[0] for x in manifest if "FIH_CRITICAL_MEMORY" in x[1]]
critical_memory = []

test_location_starts = [int(x[0], 16) for x in manifest if "START" in x[1]]
test_location_ends   = [int(x[0], 16) for x in manifest if "END" in x[1]]
test_location_zones  = zip(test_location_starts, test_location_ends)
test_locations = sum([list(range(x[0],x[1], 2)) for x in test_location_zones], [])
test_locations = ["*{}".format(x) for x in test_locations]
test_location_breakpoints = [gdb.Breakpoint(t) for t in test_locations]

end_breakpoint_locations = ["tfm_core_handler_mode", "jump_to_ns_code"]
end_breakpoints = [gdb.Breakpoint(t) for t in end_breakpoint_locations]

####################### Runtime ################################################

backend_save_state('start')
set_runthrough_mode()

out = []


gdb.execute('continue')
while last_hit_breakpoint not in end_breakpoints:
    run_test()
    gdb.execute('continue')

results_file.close()
gdb.execute('quit')
