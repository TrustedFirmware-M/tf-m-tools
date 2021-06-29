##########
Checkpatch
##########

This tool uses the `checkpatch`_ tool, with a prexisting configuration, created
for the TF-M OpenCI, to perform static checking on the developer's machine.

The script is set by default, to mimic the configuratio of `TF-M OpenCI script`_,
but the user can extend it by adding new parameters in the ``checkpatch.conf`` file.

The script is kept simple by design, since it is aimed at be easy to maintain
from a single's user perspective

******
Set-up
******

Setting up this tool, is a simple operation of retrieving the script and its
dependencies and placing them in the `tf-m-tools\static_checks\checkpatch`
directory:

- checkpatch.pl
- const_structs.checkpatch
- spelling.txt

The proccess can be automated, without any special priviledges by invoking the
``tf-m-tools\static_checks\checkpatch\setup.sh`` script.

****************
Using the script
****************

The user can call the ``tf-m-tools\static_checks\checkpatch\run_checkpatch.sh``
script from the ``{$TFM-ROOT}`` directory

.. code-block:: bash

    cd $TFM-ROOT
    # Only need to be run once
    ../tf-m-tools/static_checks/checkpatch/setup.sh
    ../tf-m-tools/static_checks/checkpatch/run_checkpatch.sh

Or as a part of all the tests set in the Static Checking Framework

.. code-block:: bash

    cd $TFM-ROOT
    ../tf-m-tools/static_checks/run_all_checks.sh

.. _checkpatch: https://www.kernel.org/doc/html/latest/dev-tools/checkpatch.html
.. _TF-M OpenCI script: https://git.trustedfirmware.org/next/ci/tf-m-ci-scripts.git/tree/run-checkpatch.sh?h=refs/heads/master

*Copyright (c) 2021, Arm Limited. All rights reserved.*
*SPDX-License-Identifier: BSD-3-Clause*
