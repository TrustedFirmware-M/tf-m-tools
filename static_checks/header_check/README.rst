#######################
Copyright header checks
#######################

This script checks that all text files staged for commit (new and
modified) have the correct license header. It returns the list of files
whose header is missing or not updated. To use it, make sure you have jinja2
installed (if you are on linux you can run the setup.sh script to install it),
then run the python script from the tfm repository with the name of the
organization, for example: ``python3 run_header_check.py Arm`` To get the list
of known organizations, run ``python3 run_header_check.py --help``.

The list is stored in a python file called "orgs\_list.py", stored in the
same directory as the script. To add a new organization, add a generic
name and the official denomination used in the copyright header to this
file.

The copyright header must have the following structure:
Copyright (c) <year>, <organisation>. (optional)All rights reserved.

--------------

*Copyright (c) 2021, Arm Limited. All rights reserved.*
*SPDX-License-Identifier: BSD-3-Clause*
