#############
FIH TEST TOOL
#############

This directory contains a tool for testing the fault injection mitigations
implemented by TF-M.

Description
===========

The tool relies on QEMU (simulating the AN521 target), and GDB.

The tool will:
   * first compile a version of TF-M with the given parameters.
   * Then setup some infrastructure used for control of a QEMU session,
     including a Virtual Hard Drive (VHD) to save test state and some FIFOs for
     control.
   * Then run GDB, which then creates a QEMU instance and attaches to it via the
     GDBserver interface and the FIFOs.
   * Run through an example execution of TF-M, conducting fault tests.
   * Output a JSON file with details of which tests where run, and what failed.

The workflow for actually running the test execution is as follows:
   * Perform setup, including starting QEMU.
   * Until the end_breakpoint is hit:
      * Execute through the program until a `test_location` breakpoint is hit.
      * Save the execution state to the QEMU VHD.
      * Enable all the `critical point breakpoints`.
      * Run through until the end_breakpoint to save the "known good" state. The
         state saving is described below.
      * For each of the fault tests specified:
         * Load the test_start state, so that a clean environment is present.
         * Perform the fault.
         * Run through, evaluating any `critical memory` at every
            `critical point breakpoint` and saving this to the test state.
         * Detect any failure loop states, QEMU crashes, or the end breakpoint,
            and end the test.
         * Compare the execution state of the test with the "known good" state.
      * Load the state at the start of the test.
      * Disable all the `critical point breakpoints`.

The output file will be inside the created TFM build directory. It is named
`results.json` The name of the created TFM build dir will be determined by the
build options. For example `build_GNUARM_debug_OFF_2/results.json`

Dependencies
============

 * qemu-system-arm
 * gdb-multiarch (with python3 support)
 * python3.7+
 * python packages detailed in requirements.txt

The version of python packaged with gdb-multiarch can differ from the version of
python that is shipped by the system. The version of python used by
gdb-multiarch can can be tested by running the command:
`gdb-multiarch -batch -ex "python import sys; print(sys.version)"`.
If this version is not greater than or equal to 3.7, then gdb-multiarch may need
to be upgraded. Under some distributions, this might require upgrading to a
later version of the distribution.

Usage of the tool
=================

Options can be determined by using

``./fih_test --help``

In general, executing `fih_test` from a directory inside the TF-M source
directory (`<TFM_DIR>/build`), will automatically set the SOURCE_DIR and
BUILD_DIR variables / arguments correctly.

For example:

.. code-block:: console

  cd <TFM_DIR>
  mkdir build
  cd build
  <Path to>/fih_test -p LOW

  # Test with certain function
  <Path to>/fih_test -p LOW -l 2 -f "tfm_hal_set_up_static_boundaries"

  # Build the AXF file again if the source code has been changed
  <Path to>/fih_test -p LOW -l 2 -r

Fault types
=====================

The types of faults simulated is controlled by ``faults/__init__.py``. This file
should be altered to change the fault simulation parameters. To add new fault
types, new fault files should be added to the ``faults`` directory.

Currently, the implemented fault types are:
 * Setting a single register (from r0 to r15) to a random uint32
 * Setting a single register (from r0 to r15) to zero
 * Skipping between 1 and 7 instructions

All of these will be run at every evaluation point, currently 40 faults per
evaluation point.

Working with results
====================

Results are written as a JSON file, and can be large. As such, it can be useful
to employ dedicated tools to parse the JSON.

The use of `jq <https://stedolan.github.io/jq/>` is highly recommended. Full
documentation of this program is out of scope of this document, but instructions
and reference material can be found at the linked webpage.

For example, to find the amount of passes:

``cat results.json | jq 'select(.passed==true) | .passed' | wc -l``

And the amount of fails:

``cat results.json | jq 'select(.passed==false) | .passed' | wc -l``

To find all the faults that caused failures, and the information about where
they occurred:

``cat results.json | jq 'select(.passed==false) | {pc: .pc, file: .file, line: .line, asm: .asm, fault: .fault}'``

--------------

*Copyright (c) 2021-2022, Arm Limited. All rights reserved.*
