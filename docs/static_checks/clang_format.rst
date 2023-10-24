############
clang-format
############

This tool uses clang-format and the script clang-format-diff.py provided
in the clang tools to apply style checking on all staged files. You can
use it before committing to check for any style that does not comply
with the TF-M coding guidelines.

*************
How to use it
*************

Using the configuration script
==============================

    - Install clang-format on your system, the tool is available as part of the
      clang suite, but can also be installed standalone from a packet manager.
    - After that the only thing the user needs to do is run the
      run-clang-format.sh script while in the TF-M root folder. If any
      dependency is missing, it will call the setup script to install it.

Without using the configuration script
======================================

    - Make sure clang-format is installed in your system
    - Copy the .clang-format file to the root of the tf-m directory -
    - Download clang-format-diff from the llvm `github repository`_
    - Run

.. code-block:: bash

    git diff -U0 --no-color HEAD^ | <path/to/clang-format-diff.py> -p1 -style file> <out_file>

If clang-format makes any correction, a diff file will be created in the tfm
root directory, simply run ``git apply -p0 <diff_file>`` to apply them. The
generated diff is a unified diff, whose format is slightly different that the
git diff format, hence the -p0 option so that git can correctly interpret the
file.

.. _github repository: https://github.com/llvm/llvm-project/blob/main/clang/tools/clang-format/clang-format-diff.py

*Copyright (c) 2021, Arm Limited. All rights reserved.*
*SPDX-License-Identifier: BSD-3-Clause*
