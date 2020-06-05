#-------------------------------------------------------------------------------
# Copyright (c) 2020, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

""" This module implements the debugger control interface for the GDB debugger
"""

import traceback
import logging
import re
# pylint: disable=import-error
import gdb
# pylint: enable=import-error

from irq_test_abstract_debugger import AbstractDebugger
from irq_test_executor import TestExecutor

class Breakpoint:
    def __init__(self, number, hit_count):
        self.number = number
        self.hit_count = hit_count

    def __str__(self):
        return "(#" + str(self.number) + ": hit_count=" + str(self.hit_count) + ")"

class GDBDebugger(AbstractDebugger):
    """This class is the implementation for the debugger control interface for GDB
    """
    def __init__(self, use_sw_breakpoints):
        super(GDBDebugger, self).__init__()
        self.last_breakpoint_list = []
        self.breakpoint_names = {}
        self.use_sw_breakpoints = use_sw_breakpoints
        self.last_breakpoint_num = 0
        self.execute_output = None

    def parse_breakpoint_line(self, lines):

        number = 0
        hit_count = 0

        # look for a first line: starts with a number
        m = re.match(r'^\s*(\d+)\s+', lines[0])
        if m:
            number = int(m.group(1))
            lines.pop(0)

        else:
            logging.error('unexpected line in "info breakpoints": %s', lines[0])
            exit (0)

        # look for additional lines
        if lines:
            m = re.match(r'^\s*stop only', lines[0])
            if m:
                lines.pop(0)

        if lines:
            m = re.match(r'^\s*breakpoint already hit (\d+) time', lines[0])
            if m:
                hit_count = int(m.group(1))
                lines.pop(0)

        return Breakpoint(number, hit_count)

    #TODO: remove this as it is unnecessary
    def get_list_of_breakpoints(self):
        breakpoints_output = gdb.execute('info breakpoints', to_string=True)

        if breakpoints_output.find("No breakpoints or watchpoints.") == 0:
            return []

        breakpoints = []

        m = re.match(r'^Num\s+Type\s+Disp\s+Enb\s+Address\s+What', breakpoints_output)
        if m:
            lines = breakpoints_output.splitlines()
            lines.pop(0) # skip the header

            while lines:
                breakpoints.append(self.parse_breakpoint_line(lines))

            return breakpoints

        logging.error('unexpected output from "info breakpoints"')
        exit(0)

    def set_breakpoint(self, name, location):
        # Using the gdb.Breakpoint class available in the gdb scripting
        # environment is not used here, as it looks like the python API has no
        # knowledge of the Hardware breakpoints.
        # This means that the Breakpoint.__init__() be called with
        # gdb.BP_HARDWARE_BREAKPOINT as nothing similar exists. Also the
        # gdb.breakpoints() function seems to be returning the list of software
        # breakpoints only (i.e. only breakpoints created with the 'break'
        # command are returned, while breakpoints created with 'hbreak' command
        # are not)
        # So instead of using the python API for manipulating breakpoints,
        # 'gdb.execute' is used to issue 'break', 'hbreak' and
        # 'info breakpoints' commands, and the output is parsed.
        logging.info("Add breakpoint for location '%s'", str(location))

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("List the breakpoints BEFORE adding")
            #gdb.execute("info breakpoints")
            for b in self.get_list_of_breakpoints():
                logging.debug("  " + str(b))
            logging.debug("End of breakpoint list")

        if self.use_sw_breakpoints:
            keyword = "break"
        else:
            keyword = "hbreak"

        if location.symbol:
             if (location.offset != 0):
                 argument = '*(((unsigned char*)' + location.symbol + ') + ' + location.offset + ')'
             else:
                 argument = location.symbol
        else:
             argument = location.filename + ":" + str(location.line)

        command = keyword + " " + argument
        logging.debug("Setting breakpoint with command '" + command + "'")

        add_breakpoint_output = gdb.execute(command, to_string=True)

        print add_breakpoint_output
        m = re.search(r'reakpoint\s+(\d+)\s+at', str(add_breakpoint_output))
        if (m):
            self.last_breakpoint_num = int(m.group(1))
        else:
            logging.error("matching breakpoint command's output failed")
            exit(1)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("List the breakpoints AFTER adding")
            #gdb.execute("info breakpoints")
            for b in self.get_list_of_breakpoints():
                logging.debug("  " + str(b))
            logging.debug("End of breakpoint list")

        self.breakpoint_names[self.last_breakpoint_num] = name

    def __triger_interrupt_using_STIR_address(self, line):
        logging.debug("writing to STIR address %s", hex(line))

        command = "set *((unsigned int *) " + hex(0xE000EF00) + ") = " + str(line)
        logging.debug("calling '%s'", command)
        gdb.execute(command)

    def __triger_interrupt_using_NVIC_ISPR_address(self, line):
             # write ISPR register directly
        register_id = line//32

        # straight
        #register_offset = line%32
        # reversed endianness
        register_offset = ((3-(line%32)/8)*8)+(line%8)

        # TODO: remove magic numbers
        NVIC_ISPR_address = 0xE000E200
        NVIC_ISPR_n_address = NVIC_ISPR_address + register_id * 4

        value = 1 << register_offset # 0 bits are ignored on write

        logging.debug("Writing to address 0x{:08x} register 0x{:08x}".
                      format(NVIC_ISPR_n_address, value))

        command = "set *((unsigned int *) " + hex(NVIC_ISPR_n_address) + ") = " + hex(value)
        logging.debug("calling '%s'", command)
        gdb.execute(command)

    def trigger_interrupt(self, interrupt_line):
        logging.info("triggering interrupt for line %s", str(interrupt_line))

        line = int(interrupt_line)

        # self.__triger_interrupt_using_NVIC_ISPR_address(line)
        self.__triger_interrupt_using_STIR_address(line)

    def continue_execution(self):
        logging.info("Continuing execution ")
        # save the list of breakpoints before continuing
        # self.last_breakpoint_list = gdb.breakpoints()
        self.execute_output = gdb.execute("continue", to_string=True)

    def clear_breakpoints(self):
        logging.info("Remove all breakpoints")
        gdb.execute("delete breakpoint")

    def get_triggered_breakpoint(self):
        logging.info("getting the triggered breakpoints")

        if not self.execute_output:
            logging.error("Execute was not called yet.")
            exit(1)

        m = re.search(r'Breakpoint\s+(\d+)\s*,', self.execute_output)
        if m:
            print "self.breakpoint_names: " + str(self.breakpoint_names)
            return self.breakpoint_names[int(m.group(1))]
        else:
            logging.error("Unexpected output from execution.")
            exit(1)

class TestIRQsCommand(gdb.Command):
    """This class represents the new command to be registered in GDB
    """
    def __init__(self, arg_parser):
        # This registers our class as "test_irqs"
        super(TestIRQsCommand, self).__init__("test_irqs", gdb.COMMAND_DATA)
        self.arg_parser = arg_parser

    def print_usage(self):
        """Print usage of the custom command
        """
        print self.arg_parser.print_help()

    def invoke(self, arg, from_tty):
        """This is the entry point of the command

        This function is called by GDB when the command is called from the debugger
        """
        args = self.arg_parser.parse_args(arg.split())

        debugger = GDBDebugger(args.sw_break)
        test_executor = TestExecutor(debugger)

        try:
            test_executor.execute(args.irqs, args.breakpoints, args.testcase)
        except:
            pass

        traceback.print_exc()
