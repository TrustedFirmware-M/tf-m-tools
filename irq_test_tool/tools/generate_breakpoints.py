#-------------------------------------------------------------------------------
# Copyright (c) 2020, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

"""Script for scanning the source after breakpoints

This script scans a source code, and finds patterns that sign a location to be
used as a breakpoint.
TODO: Describe format
"""

import os
import sys
import json
import re
import argparse

MACRO_PATTERN = re.compile(r'^\s*IRQ_TEST_TOOL_([0-9a-zA-Z_]*)\s*\(([^\)]*)\)\s*')

def process_line(filename, line, line_num, breakpoints):
    m = MACRO_PATTERN.match(line)
    if m:

        macro_type = m.group(1)
        parameters = m.group(2).split(',')

        print ("Macro " + macro_type + ", parameters: " + str(parameters))

        if (macro_type == 'SYMBOL'):
            if (len(parameters) != 2):
                print ("Invalid macro at " + filename + ":" + str(line_num))
                print ("Expected number of parameters for *SYMBOL is 2")
                exit(1)
            bp = {}
            bp["symbol"] = parameters[1].strip()
            breakpoints[parameters[0].strip()] = bp
            return

        if (macro_type == 'CODE_LOCATION'):
            if (len(parameters) != 1):
                print ("Invalid macro at " + filename + ":" + str(line_num))
                print ("Expected number of parameters for *CODE_LOCATION is 1")
                exit(1)
            bp = {}
            bp["file"] = filename
            bp["line"] = line_num
            breakpoints[parameters[0].strip()] = bp
            return

        if (macro_type == 'SYMBOL_OFFSET'):
            if (len(parameters) != 3):
                print ("Invalid macro at " + filename + ":" + str(line_num))
                print ("Expected number of parameters for *SYMBOL_OFFSET is 3")
                exit(1)
            bp = {}
            bp["symbol"] = parameters[1].strip()
            bp["offset"] = parameters[2].strip()
            breakpoints[parameters[0].strip()] = bp
            return

        print ("invalid macro *" + macro_type + "at " + filename + ":" + str(line_num))
        exit(1)


def process_file(file_path, filename, breakpoints):
    with open(file_path, 'r', encoding='latin_1') as f:
        content = f.readlines()
        for num, line in enumerate(content):
            line_num = num+1
            process_line(filename, line, line_num, breakpoints)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tfm_source", help="path to the TF-M source code")
    parser.add_argument("outfile", help="The output json file with the breakpoints")
    args = parser.parse_args()

    tfm_source_dir = args.tfm_source

    breakpoints = {}

    for root, subdirs, files in os.walk(tfm_source_dir):
        for filename in files:
            # Scan other files as well?
            if not filename.endswith('.c'):
                continue
            file_path = os.path.join(root, filename)
            process_file(file_path, filename, breakpoints)


    breakpoints = {"breakpoints":breakpoints}

    with open(args.outfile, 'w') as outfile:
        json.dump(breakpoints, outfile,
                sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    main()
