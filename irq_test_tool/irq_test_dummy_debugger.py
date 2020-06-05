#-------------------------------------------------------------------------------
# Copyright (c) 2020, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

""" This module contains a dummy implementation of the debugger control interface
"""

import logging
from irq_test_abstract_debugger import AbstractDebugger

class DummyDebugger(AbstractDebugger):
    """A dummy implementation of the debugger control interface

    This class can be used for rapidly testing the testcase execution algorithm.

    Breakpoint names are put in a list to keep track of them. Interrupts are not
    emulated in any way, the 'trigger_interrupt' function returns without doing
    anything. 'continue_execution' returns immediately as well, and
    'get_triggered_breakpoint' returns the breakpoint added the earliest.
    """
    def __init__(self, use_sw_breakpoints):
        super(DummyDebugger, self).__init__()
        self.breakpoints = []
        self.use_sw_breakpoints = use_sw_breakpoints

    def set_breakpoint(self, name, location):
        if (self.use_sw_breakpoints):
            breakpoint_type = "sw"
        else:
            breakpoint_type = "hw"
        logging.info("debugger: set %s breakpoint %s", breakpoint_type, name)
        self.breakpoints.append(name)

    def trigger_interrupt(self, interrupt_line):
        logging.info("debugger: triggering interrupt line for %s", str(interrupt_line))

    def continue_execution(self):
        logging.info("debugger: continue")

    def clear_breakpoints(self):
        logging.info("debugger: clearing breakpoints")
        self.breakpoints = []

    def get_triggered_breakpoint(self):
        if self.breakpoints:
            return self.breakpoints[0]
        return None
