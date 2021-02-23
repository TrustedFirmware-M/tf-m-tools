#-------------------------------------------------------------------------------
# Copyright (c) 2020, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

from irq_test_abstract_debugger import Location
import logging
import json

def create_locations_from_file(breakpoints_file_name):
    """Internal function to create Location objects of a breakpoints data file
    """
    # Read in the points to break at
    logging.info("Reading breakpoints file '%s'", breakpoints_file_name)
    breakpoints_file = open(breakpoints_file_name)
    breakpoints = json.load(breakpoints_file)
    logging.debug("breakpoints: %s", str(breakpoints))

    #TODO: go over the breakpoints and try to set them as a sanity check

    locations = {}

    for loc_name in breakpoints['breakpoints']:
        bkpt = breakpoints['breakpoints'][loc_name]
        offset = 0

        if 'file' in bkpt:
            filename = bkpt['file']
        else:
            filename = None

        if 'symbol' in bkpt:
            symbol = bkpt['symbol']
            if 'offset' in bkpt:
                offset = bkpt['offset']
            else:
                offset = 0
        else:
            if 'offset' in bkpt:
                logging.error("In location %s offset is included without a"
                              " symbol")
                exit(2)
            symbol = None

        if 'line' in bkpt:
            line = bkpt['line']
            try:
                int(line)
            except ValueError:
                logging.error("In location %s line is not a valid int",
                              loc_name)
                exit(2)
        else:
            line = None

        if symbol:
            if line or filename:
                logging.error("In location %s nor filename nor line should"
                              "be present when symbol is present", loc_name)
                exit(2)

        if (not line and filename) or (line and not filename):
            logging.error("In location %s line and filename have to be "
                          "present the same time", loc_name)
            exit(2)

        if (not symbol) and (not filename):
            logging.error("In location %s no symbol nor code location is "
                          "specified at all", loc_name)
            exit(2)

        loc = Location(symbol=symbol, offset=offset, filename=filename, line=line)

        locations[loc_name] = loc

    return locations

class TestExecutor(object):
    """ This class implements the test logic.

    It reads the input files, and executes the steps of the testcase. It receives an
    AbstractDebugger instance on creation. The test execution is implemented in the
    execute function.
    """

    def __init__(self, debugger):
        self.debugger = debugger

    def execute(self, irqs_filename, breakpoints_filename, testcase_filename):
        """ Execute a testcase

        Execute the testcase defined in 'testcase_filename', using the IRQs and
        breakpoints defined in irqs_filename and breakpoints_filename.
        """
        # Read in the list of IRQs
        logging.info("Reading irqs file '%s'", irqs_filename)
        irqs_file = open(irqs_filename)
        irqs = json.load(irqs_file)
        logging.debug("irqs: %s", str(irqs))

        # read in the test sequence
        logging.info("Reading test sequence file '%s'", testcase_filename)
        test_file = open(testcase_filename)
        test = json.load(test_file)
        logging.debug("testcase: %s", str(test))

        # TODO: crosscheck the tests file against the breakpoints and the irq's
        #       available

        locations = create_locations_from_file(breakpoints_filename)

        self.debugger.clear_breakpoints()

        # execute the test
        steps = test['steps']
        for i, step in enumerate(steps):

            logging.info("---- Step %d ----", i)

            continue_execution = False

            if 'wait_for' in step:
                bp_name = step['wait_for']
                self.debugger.set_breakpoint(bp_name, locations[bp_name])
                next_to_break_at = bp_name
                continue_execution = True
            elif 'expect' in step:
                bp_name = step['expect']
                self.debugger.set_breakpoint(bp_name, locations[bp_name])
                next_to_break_at = bp_name

                # Find the next wait_for in the test sequence, and set a
                # breakpoint for that as well. So that it can be detected if an
                # expected breakpoint is missed.

                wait_for_found = False
                ii = i+1

                while ii < len(steps) and not wait_for_found:
                    next_step = steps[ii]
                    if 'wait_for' in next_step:
                        next_bp_name = next_step['wait_for']
                        self.debugger.set_breakpoint(next_bp_name,
                                                     locations[next_bp_name])
                        wait_for_found = True
                    ii += 1

                continue_execution = True


            if 'trigger' in step:
                irqs_dict = irqs['irqs']
                irq = irqs_dict[step['trigger']]
                line_nu = irq['line_num']
                self.debugger.trigger_interrupt(line_nu)


            if continue_execution:
                self.debugger.continue_execution()

                triggered_breakpoint = self.debugger.get_triggered_breakpoint()

                if triggered_breakpoint is None:
                    logging.error("No breakpoint was hit?????")
                    exit(0)

                if triggered_breakpoint != next_to_break_at:
                    logging.error("execution stopped at '%s' instead of '%s'",
                                triggered_breakpoint, next_to_break_at)
                    exit(0)
            else:
                logging.error("execution stopped as no breakpoint is set")
                exit(1)

            self.debugger.clear_breakpoints()

        logging.info("All the steps in the test file are executed successfully"
                     " with the expected result.")
