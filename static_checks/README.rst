#########################
Static Checking Framework
#########################

This tool has been made to provide a framework to check the truster-firmware-m
(TF-M) code base.

************
Instructions
************

This tool should be used from the root of the TF-M repository. launching
run_all_checks.sh will launch the different checkers used :

- Cppcheck
- Copyright header check
- clang-format
- Checkpatch

Both checkpatch and clang-format are use to check the coding style, but they
both cover different cases so together they provide a better coverage.

Each tool will be configured using a setup.sh script located under the tool
directory before being launched. The main script might need to be launched with
root priviledges in order to correctly install the tools on the first time it
is being used.

The tool will return exit code of 0 if everything is compliant, and no
new warnings are generated, and 1 in all other occasions.

Output reports if produced by each corresponding script, will be stored at
`{TFM-Root}/checks_reports``

--------------

*Copyright (c) 2021, Arm Limited. All rights reserved.*
*SPDX-License-Identifier: BSD-3-Clause*
