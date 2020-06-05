#-------------------------------------------------------------------------------
# Copyright (c) 2020, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

""" This module implements the debugger control interface for the Arm
    Developement Studio
"""

import logging
import re
# pylint: disable=import-error
from arm_ds.debugger_v1 import Debugger
from arm_ds.debugger_v1 import DebugException
# pylint: enable=import-error
from irq_test_abstract_debugger import AbstractDebugger

class ArmDSDebugger(AbstractDebugger):
    """ This class is the implementation of the control interface for the Arm
        Developement Studio
    """

    def __init__(self, use_sw_breakpoints):
        super(ArmDSDebugger, self).__init__()
        debugger = Debugger()
        self.debugger = debugger
        self.breakpoints = {} # map breakpoint IDs to names
        self.use_sw_breakpoints = use_sw_breakpoints

        if debugger.isRunning():
            logging.info("debugger is running, stop it")
            debugger.stop()
            try:
                timeout = 180*1000 # TODO: configureble timeout value?
                debugger.waitForStop(timeout)
            except DebugException as debug_exception:
                logging.error("debugger wait timed out: %s", str(debug_exception))

    def set_breakpoint(self, name, location):
        logging.info("Add breakpoint for location %s:'%s'", name, str(location))

        ec = self.debugger.getCurrentExecutionContext()
        bps = ec.getBreakpointService()

        try:
            if location.symbol:
                if location.offset != 0:
                    spec = '(((unsigned char*)' + location.symbol + ') + ' + location.offset + ')'
                    bps.setBreakpoint(spec, hw=(not self.use_sw_breakpoints))
                else:
                    bps.setBreakpoint(location.symbol, hw=(not self.use_sw_breakpoints))
            else:
                bps.setBreakpoint(location.filename, location.line, hw=(not self.use_sw_breakpoints))
        except DebugException as ex:
            logging.error("Failed to set breakpoint for %s", str(location))
            logging.error(str(ex))
            # TODO: Remove exit (from all over the script), and drop custom
            # exception that is handled in main.
            exit(2)

        # Add the new breakpoint to the list.
        # Assume that the last breakpoint is the newly added one
        breakpoint = bps.getBreakpoint(bps.getBreakpointCount()-1)

        self.breakpoints[breakpoint.getId()] = name

    def __triger_interrupt_using_STIR_address(self, line):
        logging.debug("writing to STIR address %s", hex(line))
        ec = self.debugger.getCurrentExecutionContext()
        memory_service = ec.getMemoryService()
        mem_params = {'width': 8, 'verify': 0, 'use_image': 0}
        memory_service.writeMemory32(hex(0xE000EF00), line, mem_params)

    def __triger_interrupt_using_STIR_register(self, line):
        logging.debug("writing to STIR register %s", hex(line))
        register_name = "STIR"
        ec = self.debugger.getCurrentExecutionContext()
        ec.getRegisterService().setValue(register_name, line)

    def __triger_interrupt_using_NVIC_ISPR_register(self, line):
         # write ISPR register directly
        register_id = line//32
        register_offset = line%32
        register_name = "NVIC_ISPR" + str(register_id)

        ec = self.debugger.getCurrentExecutionContext()
        value = ec.getRegisterService().getValue(register_name)
        value |= 1 << register_offset

        logging.debug("Writing to {:s} register 0x{:08x}".
                      format(register_name, value))

        ec.getRegisterService().setValue(register_name, hex(value))

    def __triger_interrupt_using_NVIC_ISPR_address(self, line):
        # write ISPR register directly
        register_id = line//32
        register_offset = line%32
        # TODO: remove magic numbers
        NVIC_ISPR_address = 0xE000E200
        NVIC_ISPR_n_address = NVIC_ISPR_address + register_id * 4

        ec = self.debugger.getCurrentExecutionContext()
        memory_service = ec.getMemoryService()
        mem_params = {'width': 8, 'verify': 0, 'use_image': 0}

        value = 1 << register_offset # 0 bits are ignored on write

        logging.debug("Writing to address 0x{:08x} register 0x{:08x}".
                      format(NVIC_ISPR_n_address, value))

        memory_service.writeMemory32(NVIC_ISPR_n_address, value, mem_params)

    def trigger_interrupt(self, interrupt_line):
        logging.info("triggering interrupt for line %s", str(interrupt_line))

        line = int(interrupt_line)

        if line >= 0:
            #self.__triger_interrupt_using_STIR_address(line)
            #self.__triger_interrupt_using_STIR_register(line)
            #self.__triger_interrupt_using_NVIC_ISPR_register(line) # seems to have bugs?
            self.__triger_interrupt_using_NVIC_ISPR_address(line)
        else:
            logging.error("Invalid  interrupt line value {:d}".format(line))
            exit(0)

    def continue_execution(self):
        logging.info("Continuing execution ")
        ec = self.debugger.getCurrentExecutionContext()
        ec.executeDSCommand("info breakpoints")
        self.debugger.run()

        try:
            timeout = 180*1000 # TODO: configureble timeout value?
            self.debugger.waitForStop(timeout)
        except DebugException as debug_exception:
            logging.error("debugger wait timed out %s", str(debug_exception))
            exit(0)


    def clear_breakpoints(self):
        logging.info("Remove all breakpoints")
        self.debugger.removeAllBreakpoints()
        self.breakpoints = {}

    def get_triggered_breakpoint(self):
        ec = self.debugger.getCurrentExecutionContext()
        bps = ec.getBreakpointService()
        breakpoint = bps.getHitBreakpoint()
        id = breakpoint.getId()
        logging.info("getting the triggered breakpoints, ID = {:d}".format(id))
        return self.breakpoints[id]
