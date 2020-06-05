#-------------------------------------------------------------------------------
# Copyright (c) 2020, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

"""Defines the interface that a debugger control class have to implement
"""

class Location(object):
    """A helper class to store the properties of a location where breakpoint
       can be put
    """
    def __init__(self, symbol=None, offset=0, filename=None, line=None):
        self.symbol = symbol
        self.offset = offset
        self.filename = filename
        self.line = line

    def __str__(self):
        ret = ""
        if self.symbol:
            ret += str(self.symbol)

        if self.offset:
            ret += "+" + str(self.offset)

        if self.filename:
            if self.symbol:
                ret += " @ "
            ret += str(self.filename) + ":" + str(self.line)

        return ret

    def __unicode__(self):
        return str(self), "utf-8"

class AbstractDebugger(object):
    """The interface that a debugger control class have to implement
    """
    def __init__(self):
        pass

    def set_breakpoint(self, name, location):
        """Put a breakpoint at a location

        Args:
            name: The name of the location. This name is returned by
                  get_triggered_breakpoint
            location: An instance of a Location class
        """
        raise NotImplementedError('subclasses must override set_breakpoint()!')

    def trigger_interrupt(self, interrupt_line):
        """trigger an interrupt on the interrupt line specified in the parameter

        Args:
            interrupt_line: The number of the interrupt line
        """
        raise NotImplementedError('subclasses must override trigger_interrupt()!')

    def continue_execution(self):
        """Continue the execution
        """
        raise NotImplementedError('subclasses must override continue_execution()!')

    def clear_breakpoints(self):
        """Clear all breakpoints
        """
        raise NotImplementedError('subclasses must override clear_breakpoints()!')

    def get_triggered_breakpoint(self):
        """Get the name of the last triggered breakpoint
        """
        raise NotImplementedError('subclasses must override get_triggered_breakpoint()!')
