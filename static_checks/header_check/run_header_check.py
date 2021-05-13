#-------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

import subprocess
from jinja2 import Template
import datetime
import re
import sys
import os
from orgs_list import orgs_list

def print_help():
    print("[SCF Header Check] The following organizations are recognized:")
    for d in orgs_list:
        print(" - {}".format(d['name']))
    print("[SCF Header Check] If your organization is not in the list, please edit the \'orgs_list.py\' file.")

# Retrieve the list of organizations
script_path = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) != 2:
    print("[SCF Header Check: ERROR] Usage: python3 run_header_check.py <org>")
    print("[SCF Header Check] Try python3 run_header_check.py --help")
    sys.exit(1)

if sys.argv[1] == "--help":
    print("[SCF Header Check] Usage: python3 run_header_check.py <org>")
    print_help()
    sys.exit(1)

org_name = sys.argv[1].lower()

org = next((item for item in orgs_list if item["name"].lower() == org_name), None)

if org == None:
    print("[SCF Header Check: ERROR] Unrecognised organization.")
    print_help()
    sys.exit(1)

now = datetime.datetime.now()
year = now.year

# Base template for copyright header
base_header = Template(r"Copyright \(c\) {{ year }}, {{ org }}.( All rights reserved.)?")

# Retrieve the list of new and modified files
# The -M100% argument is there to tell Git to consider moved files as new when
# at least one character has been modified (Otherwise it might not consider
# files that has been moved and modified)
added_files = subprocess.Popen(['git', 'diff', '--name-only',
    '--diff-filter=A', '--cached', '-M100%'], stdout=subprocess.PIPE,
    universal_newlines=True).stdout.read().split()
modified_files = subprocess.Popen(['git', 'diff', '--name-only',
    '--diff-filter=M', '--cached'], stdout=subprocess.PIPE,
    universal_newlines=True).stdout.read().split()

# Remove non text files
added_text_files = []
modified_text_files = []

for f in added_files:
    out = subprocess.Popen(['file', f], stdout=subprocess.PIPE,
            universal_newlines=True).stdout.read()
    if "ASCII" in out:
        added_text_files.append(f)

for f in modified_files:
    out = subprocess.Popen(['file', f], stdout=subprocess.PIPE,
            universal_newlines=True).stdout.read()
    if "ASCII" in out:
        modified_text_files.append(f)

# Check that all files have a correct header
files_without_header = []

year_pattern = str(year)
copyright = base_header.render(year=year_pattern, org=org['header'])
copyright = r'{}'.format(copyright)

for filename in added_text_files:
    with open(filename) as f:
        if not re.search(copyright, f.read()):
            files_without_header.append(filename)

year_pattern = "(\d\d\d\d-)?" + str(year)
copyright = base_header.render(year=year_pattern, org=org['header'])
copyright = r'{}'.format(copyright)

for filename in modified_text_files:
    with open(filename) as f:
        if not re.search(copyright, f.read()):
            files_without_header.append(filename)

if len(files_without_header) != 0:
    print("[SCF Header Check: WARNING] Some files are missing up-to-date {} header:".format(org['name']))
    for f in files_without_header:
        print(" - {}".format(f))
    sys.exit(1)
else:
    print("[SCF Header Check: PASS] All files have a correct header")
    sys.exit(0)

