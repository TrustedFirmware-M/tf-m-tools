#!/usr/bin/python3
# -----------------------------------------------------------------------------
# Copyright (c) 2024, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import argparse
import logging
import json
from os import listdir
from os.path import join, isfile, relpath
import subprocess

class Source:
    def __init__(self, location : str):
        self.type = "git"
        self.location = location
        self.refspec = ""

        with open(join(location, ".git", "config"), "rt") as git_config_file:
            url_line = [x for x in git_config_file.readlines() if "url" in x][0]
            self.url = url_line.rstrip().replace("\turl = ", "").rstrip()

        with open(join(location, ".git", "HEAD"), "rt") as git_HEAD_file:
            self.commit = git_HEAD_file.read().rstrip()

        self.location = relpath(location, args.source_dir)

def get_tfm_dependencies(build_dir : str) -> [Source]:
    dependencies = []

    with open(join(build_dir, "CMakeCache.txt"), "rt") as cmakecache_file:
        cmakecache = cmakecache_file.readlines()
    variables = [x.rstrip().split("=") for x in cmakecache if "=" in x]
    path_variables = [x for x in variables if "PATH" in x[0]]

    for _,p in path_variables:
        try:
            dependencies.append(Source(p))
        except (FileNotFoundError, NotADirectoryError):
            continue

    return dependencies

parser = argparse.ArgumentParser()
parser.add_argument("--build_dir", help="TF-M build directory", required=True)
parser.add_argument("--source_dir", help="TF-M source directory", required=True)
parser.add_argument("--tools_binary_dir", help="Binary dir in which objdump etc reside", required=False)
parser.add_argument("--log_level", help="Log level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="ERROR")
parser.add_argument("--output_config_file", help="output JSON file", required=True)
parser.add_argument("--output_intermediate_file", help="output intermediate file", required=True)
parser.add_argument("trace_file", nargs="+", help="input trace log files")
args = parser.parse_args()

# logging setup
logging.basicConfig(level=args.log_level)

configuration = {
        "remove_workspace": True,
        "include_assembly": True,
}

if (args.tools_binary_dir):
    tools_prefix = args.tools_binary_dir
else:
    tools_prefix = ""

tfm_source = Source(args.source_dir)
dependencies = get_tfm_dependencies(args.build_dir)

parameters = {
    "objdump" : join(tools_prefix, "arm-none-eabi-objdump"),
    "readelf" : join(tools_prefix, "arm-none-eabi-readelf"),
    "sources" : [
        {
            "type" : x.type,
            "URL": x.url,
            "COMMIT" : x.commit,
            "REFSPEC" : x.refspec,
            "LOCATION" : x.location,
        } for x in [tfm_source] + dependencies],
    "workspace": args.source_dir,
    "output_file": args.output_intermediate_file,
}

bin_dir = join(args.build_dir, "bin")
elf_files = [join(bin_dir, x) for x in listdir(bin_dir) if isfile(join(bin_dir, x)) and "elf" in x]

elfs = [
    {
        "name": x,
        "traces": args.trace_file,
    } for x in elf_files]

output = {
    "configuration": configuration,
    "parameters": parameters,
    "elfs": elfs,
}

with open(args.output_config_file, "w+") as output_file:
    json.dump(output, output_file)
