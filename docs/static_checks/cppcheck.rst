########
Cppcheck
########
cppcheck is a tool used to check a number of checks on the codebase. The list
of all the checks is available at :
https://sourceforge.net/p/cppcheck/wiki/ListOfChecks/

******************
tool configuration
******************

This tool is using the pre-existing cppcheck configurations
(arm-cortex-m.cfg/tfm-suppress-list.txt), implementing the developer's
guidelines, as used by the TF-M CI.

The suppression list contains:

    - Files that are not guaranteed to comply with the TF-M rules.
    - Files under directories that correspond to external libraries.

The files utils.sh, arm-cortex-cfg.cfg and tfm-suppress-list.txt were copied
from the CI scripts repo :
https://review.trustedfirmware.org/admin/repos/ci/tf-m-ci-scripts

***************
Using this tool
***************

This script must be launched from the TFM repo and the reports will be stored
under checks_reports if the xml option is selected. The possible parameters are
the following:

    - '-h' display the help for this tool
    - '-r' select the raw output option. If this parameter is selected, the
      output will be displayed in the console instead of stored in an xml file



--------------

*Copyright (c) 2021, Arm Limited. All rights reserved.*
*SPDX-License-Identifier: BSD-3-Clause*
