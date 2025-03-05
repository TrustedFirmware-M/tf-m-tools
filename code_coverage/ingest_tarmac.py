#!/usr/bin/python3
# -----------------------------------------------------------------------------
# Copyright (c) 2024-2025, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import argparse
import logging
import re
import elftools
from itertools import islice

def parse_line_fvp(line: str) -> str:
    split = line.split(" ")
    try:
        addr = split[5]
        size = len(split[6]) // 2
        logging.debug("Instruction at {} of size {}".format(addr, size))
    except Exception as e:
        print("Parse error {} for line {}".format(e,line))
        raise Exception
    return (addr, size)

def parse_line_rtl(line: str) -> str:
    try:
        split = line.split(" ")[1].replace("(", "").replace(")", "").split(":")
        addr = split[0]
        size = len(split[1]) // 2
        logging.debug("Instruction at {} of size {}".format(addr, size))
    except Exception as e:
        print("Parse error {} for line {}".format(e,line))
        raise Exception
    return (addr, size)

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="tarmac file to input", required=True)
parser.add_argument("--log_level", help="Log level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="ERROR")
parser.add_argument("--output_file", help="output file, in qa-tools format", required=True)
args = parser.parse_args()

# logging setup
logging.basicConfig(level=args.log_level)

instructions = []
parse_function = parse_line_fvp
hit_counts = {}

with open(args.input_file, "rt") as input_file:
    while(lines := list(islice(input_file, 100000))):
        lines = ''.join(lines)
        chunk_instructions = re.findall(r'[0-9]* [a-z]{3} [a-z\.]* IT .*', lines)

        if len(chunk_instructions) == 0:
            chunk_instructions = re.findall(r'[0-9]* clk ES (.*:.*).*', lines)
            if len(chunk_instructions) != 0:
                parse_function = parse_line_rtl

        for i in chunk_instructions:
            addr = parse_function(i)
            if addr in hit_counts.keys():
                hit_counts[addr] += 1
            else:
                hit_counts[addr] = 1

with open(args.output_file, "w+") as output_file:
    output_file.writelines(["{} {} {}\n".format(x[0], hit_counts[x], x[1]) for x in hit_counts.keys()])
