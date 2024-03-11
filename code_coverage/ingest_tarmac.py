#!/usr/bin/python3
# -----------------------------------------------------------------------------
# Copyright (c) 2024, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import argparse
import logging
import re
import elftools

def parse_line(line: str) -> str:
    split = line.split(" ")
    addr = split[5]
    size = len(split[6]) // 2
    logging.debug("Instruction at {} of size {}".format(addr, size))
    return (addr, size)

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="tarmac file to input", required=True)
parser.add_argument("--log_level", help="Log level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="ERROR")
parser.add_argument("--output_file", help="output file, in qa-tools format", required=True)
args = parser.parse_args()

# logging setup
logging.basicConfig(level=args.log_level)

with open(args.input_file, "rt") as input_file:
    trace = input_file.read()

instructions = re.findall("[0-9]* [a-z]{2} [a-z\.]* IT .*", trace)

hit_counts = {}

for i in instructions:
    addr = parse_line(i)
    if addr in hit_counts.keys():
        hit_counts[addr] += 1
    else:
        hit_counts[addr] = 1

with open(args.output_file, "w+") as output_file:
    output_file.writelines(["{} {} {}\n".format(x[0], hit_counts[x], x[1]) for x in hit_counts.keys()])
