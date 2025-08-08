#!/usr/bin/python3
# -----------------------------------------------------------------------------
# Copyright (c) 2024-2025, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import re
import argparse

import multiprocessing as mp

from itertools import islice
from collections import Counter

MAX_JOBS = 10
CHUNK_SIZE = 100000


def parse_fvp(line: str) -> (str, str):
    """ processes the assembly instructions from the fvp """
    split = line.split(" ")

    #       addr      size
    return (split[5], len(split[6]) // 2)


def parse_rtl(line: str) -> (str, str):
    split = line.split(" ")[1].replace("(", "").replace(")", "").split(":")

    #       addr      size
    return (split[0], len(split[1]) // 2)


def process_trace(function, lines) -> Counter:
    """ function run by each worker
        to process the tarmac trace """

    hit_counts = {}
    for line in lines:

        addr = function(line)

        if addr not in hit_counts: hit_counts[addr]  = 1
        else:                      hit_counts[addr] += 1

    return hit_counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file",
                        help="tarmac file to input", required=True)
    parser.add_argument("--output_file",
                        help="output file, in qa-tools format", required=True)
    parser.add_argument("--log_level",   help="Log level",
                        choices=["DEBUG", "INFO", "WARNING",
                                 "ERROR", "CRITICAL"],
                        default="ERROR")

    args = parser.parse_args()

    # open mp pool
    p = mp.Pool(MAX_JOBS)

    jobs = []
    hit_count = Counter({})
    with open(args.input_file, "rt") as f:
        while (chunk := list(islice(f, CHUNK_SIZE))):
            # when workers are not availible
            j = 0
            while len(jobs) == MAX_JOBS:
                job = jobs[j]

                # next job if this job not finished
                if not job.ready():
                    j += 1
                    j %= MAX_JOBS
                    continue

                # sum when results are availible
                hit_count += job.get()
                # remove completed job from list
                jobs.pop(j)

            # when a worker is available
            chunk = ''.join(chunk)

            chunk = \
                re.findall(r'[0-9]* [a-z]{3} [a-z\.]* IT .*', chunk)

            # if there are any fvp instructions to process
            if len(chunk):
                jobs.append(p.apply_async(process_trace,
                                          args=(parse_fvp, chunk,)))
                continue

            chunk = \
                re.findall(r'[0-9]* clk ES (.*:.*).*', chunk)

            # if there are any rtl instructions to process
            if len(chunk):
                jobs.append(p.apply_async(process_trace,
                                          args=(parse_rtl, chunk,)))
                continue

    # sum any remaining jobs
    for job in jobs:
        job.wait()
        hit_count += job.get()

    # close mp pool
    p.close()

    # write the results
    with open(args.output_file, "w+") as f:
        f.writelines([f"{x[0]} {hit_count[x]} {x[1]}\n"
                      for x in hit_count.keys()])
