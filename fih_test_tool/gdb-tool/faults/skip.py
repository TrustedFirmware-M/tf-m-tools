# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import gdb
import random

class skip_fault():
    def __init__(self, size=None):
        if size is None:
            self.size = random.randint(1, 6) * 2
        else:
            self.size = size

    def execute(self):
        gdb.execute('set $pc += {}'.format(self.size))

    def __repr__(self):
        return "Skip Fault: pc += {}".format(self.size)

    def as_json(self):
        return {
                'type': 'skip',
                'size': self.size,
                }
