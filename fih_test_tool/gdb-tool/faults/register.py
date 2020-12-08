# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import gdb
import random

class register_fault():
    def __init__(self, reg=None,
                       val=None):
        if reg is None:
            self.reg = "r" + str(random.randint(0, 16))
        else:
            self.reg = reg

        if val is None:
            self.val = random.randint(0, 0xFFFFFFFF - 1)
        else:
            self.val = val

    def execute(self):
        gdb.execute('set ${} = {}'.format(self.reg, self.val))

    def __repr__(self):
        return "Register Fault: set {} to {}".format(self.reg, hex(self.val))

    def as_json(self):
        return {
                'type': 'register',
                'reg': self.reg,
                'val': hex(self.val),
                }
