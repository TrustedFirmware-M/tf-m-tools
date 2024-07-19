#######################################
TF-Fuzz (Trusted-Firmware Fuzzer) guide
#######################################

************
Introduction
************

TF-Fuzz is a TF-M fuzzing tool, at the PSA-call level.  At the time of writing
this at least, presentations available at:

- https://www.trustedfirmware.org/docs/TF-M_Fuzzing_Tool_TFOrg.pdf
- https://zoom.us/rec/share/1dxZcZit111IadadyFqFU7IoP5X5aaa8gXUdr_UInxmMbyLzEqEmXQdx79-IWQ9p

(These presentation materials may not all be viewable by all parties.)

A suite generator tool is also provided to make tests output by TF-Fuzz
runnable as a test suite in the regression tester.


*******************************
Building and Installing TF-Fuzz
*******************************

.. Note::

    These instructions assume the use of Ubuntu Linux.


The following dependencies are required to build TF-Fuzz:

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install build-essential bison flex


To build TF-Fuzz, simply type ``make`` in this directory.  The executable,
called ``tfz``, is placed in the ``bin/`` directory.

======================================
Installing the TF-Fuzz suite generator
======================================

**Requirements:** Python 3.8 or later; a built ``tfz`` binary.


The suite generator is installable as a Python package through ``pip``:

.. code-block:: bash

   cd <path/to/tf-tools>/tf_fuzz
   pip3 install tfz-suitegen

Once installed, ``tfz-suitegen`` can be ran by typing ``python3 -m tfz-suitegen``.


******************************************
Generating and running tests using TF-Fuzz
******************************************

**Full usage information can be found by running** ``./bin/tfz`` **and** ``python3 -m tfz-suitegen --help`` **.**

The ``demo`` folder contains some example test specifications. The below steps
describe how to build and run these with the TF-M regression tester.

#. Turn the test specifications into a test suite:

   .. code-block:: bash

        python3 -m tfz-suitegen <path/to/tf_fuzz> <path/to/tf_fuzz>/demo build_suite

   This creates an :external:ref:`out-of-tree test suite
   <tfm_test_suites_addition:out-of-tree regression test suites>` containing
   all the tests in the ``demo`` folder.

   .. note::
      Only files with the ``.test`` extension are included in the test suite.

#. Build the regression tests as normal, adding the following CMake flag to the SPE build:

   .. code-block:: bash

       -DEXTRA_NS_TEST_SUITE_PATH=<absolute_path_to>/build_suite

   For full instructions on how to build and run tests see
   :external:doc:`building/tests_build_instruction` and
   :external:ref:`building/run_tfm_examples_on_arm_platforms:run tf-m tests and
   applications on arm platforms`.

.. warning::

   Some of the provided demos are expected to fail.


************************************
Running the TF-Fuzz regression tests
************************************

To run the regression test suite:

.. code-block:: bash

   cd <path/to/tf-tools>/tf_fuzz/tfz-cpp
   make
   cd regression
   bash regress


For more details, see :doc:`source_structure/regression_dir`.


.. toctree::
    :caption: Table of Contents
    :maxdepth: 1

    Source Structure <source_structure/index>

--------------

*Copyright (c) 2020-2024, Arm Limited. All rights reserved.*
