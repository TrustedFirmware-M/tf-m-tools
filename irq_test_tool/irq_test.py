#-------------------------------------------------------------------------------
# Copyright (c) 2020, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

""" This module is the entry point of the IRQ testing tool.
"""

import argparse
import json
import logging
import os
import sys

# Workaround for GDB: Add current directory to the module search path
sys.path.insert(0, os.getcwd())
from irq_test_abstract_debugger import Location
from irq_test_dummy_debugger import DummyDebugger
from irq_test_executor import TestExecutor

def create_argparser():
    """ Create an argument parser for the script

    This parser enumerates the arguments that are necessary for all the
    debuggers. Debugger implementations might add other arguments to this
    parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--sw-break",
                        help="use sw breakpoint (the default is HW breakpoint)",
                        action="store_true")
    parser.add_argument("-q", "--irqs",
                        type=str,
                        help="the name of the irqs json",
                        required=True)
    parser.add_argument("-b", "--breakpoints",
                        type=str,
                        help="the name of the breakpoints json",
                        required=True)
    parser.add_argument("-t", "--testcase",
                        type=str,
                        help="The testcase to execute",
                        required=True)
    return parser

def main():
    """ The main function of the script

    Detects the debugger that it is started in, creates the debugger
    implementation instance, and either executes the test, or registers a
    command in the debugger. For details see the README.rst
    """
    try:
        # TODO: evironment checking should be refactored to the debugger
        # implementations
        from arm_ds.debugger_v1 import Debugger
        debugger_type = 'Arm-DS'
    except ImportError:
        logging.debug('Failed to import Arm-DS scripting env, try GDB')
        try:
            # TODO: evironment checking should be refactored to the debugger
            # implementations
            import gdb
            debugger_type = 'GDB'
        except ImportError:
            logging.debug("Failed to import GDB scripting env, fall back do "
                          "dummy")
            debugger_type = 'dummy'

    logging.info("The debugger type selected is: %s", debugger_type)

    # create a debugger controller instance
    if debugger_type == 'Arm-DS':
        from irq_test_Arm_DS_debugger import ArmDSDebugger
        logging.debug("initialising debugger object...")
        arg_parser = create_argparser()
        try:
            args = arg_parser.parse_args()
        except:
            logging.error("Failed to parse command line parameters")
            return
        # TODO: Fail gracefully in case of an argparse error
        debugger = ArmDSDebugger(args.sw_break)
        executor = TestExecutor(debugger)
        executor.execute(args.irqs, args.breakpoints, args.testcase)
    elif debugger_type == 'GDB':
        from irq_test_gdb_debugger import GDBDebugger
        from irq_test_gdb_debugger import TestIRQsCommand
        logging.debug("initialising debugger object...")
        arg_parser = create_argparser()

        # register the 'test_irqs' custom command
        TestIRQsCommand(arg_parser)
        logging.info("Command 'test_irqs' is successfully registered")
    elif debugger_type == 'dummy':
        arg_parser = create_argparser()
        args = arg_parser.parse_args()
        debugger = DummyDebugger(args.sw_break)
        executor = TestExecutor(debugger)
        executor.execute(args.irqs, args.breakpoints, args.testcase)

if __name__ == "__main__":
    logging.basicConfig(format='===== %(levelname)s: %(message)s',
                        level=logging.DEBUG, stream=sys.stdout)
    main()
