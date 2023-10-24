################################
Profiler tool and TF-M Profiling
################################

The profiler is a tool for profiling and benchmarking programs. The developer can
leverage it to get the interested data of runtime.

Initially, the profiler supports only count logging. You can add "checkpoint"
in the program. The timer count or CPU cycle count of this checkpoint can be
saved at runtime and be analysed in the future.

*********************************
TF-M Profiling Build Instructions
*********************************

TF-M has integrated some built-in profiling cases. There are two configurations
for profiling:

* ``CONFIG_TFM_ENABLE_PROFILING``: Enable profiling building in TF-M SPE and NSPE.
  It cannot be enabled together with any regression test configs, for example ``TEST_NS``.
* ``TFM_TOOLS_PATH``: Path of tf-m-tools repo. The default value is ``DOWNLOAD``
  to fetch the remote source.

The section `TF-M Profiling Cases`_  introduces the profiling cases in TF-M.
To enable the built-in profiling cases in TF-M, run:

.. code-block:: console

  cd <path to tf-m-tools>/profiling/profiling_cases/tfm_profiling
  mkdir build

  # Build SPE
  cmake -S <path to tf-m> -B build/spe -DTFM_PLATFORM=arm/mps2/an521 \
        -DCONFIG_TFM_ENABLE_PROFILING=ON -DCMAKE_BUILD_TYPE=Release \
        -DTFM_EXTRA_PARTITION_PATHS=${PWD}/../prof_psa_client_api/partitions/prof_server_partition;${PWD}/../prof_psa_client_api/partitions/prof_client_partition \
        -DTFM_EXTRA_MANIFEST_LIST_FILES=${PWD}/../prof_psa_client_api/partitions/prof_psa_client_api_manifest_list.yaml \
        -DTFM_PARTITION_LOG_LEVEL=TFM_PARTITION_LOG_LEVEL_INFO

  # Another simple way to configure SPE:
  cmake -S <path to tf-m> -B build/spe -DTFM_PLATFORM=arm/mps2/an521 \
        -DTFM_EXTRA_CONFIG_PATH=${PWD}/../prof_psa_client_api/partitions/config_spe.cmake
  cmake --build build/spe -- install -j

  # Build NSPE
  cmake -S . -B build/nspe -DCONFIG_SPE_PATH=build/spe/api_ns \
        -DTFM_TOOLCHAIN_FILE=build/spe/api_ns/cmake/toolchain_ns_GNUARM.cmake
  cmake --build build/nspe -- -j

******************************
Profiler Integration Reference
******************************

`profiler/profiler.c` is the main source file to be complied with the tagert program.

Initialization
==============

``PROFILING_INIT()`` defined in `profiling/export/prof_intf_s.h` shall be called
on the secure side before calling any other API of the profiler. It initializes the
HAL and the backend database which can be customized by users.

Implement the HAL
-----------------

`export/prof_hal.h` defines the HAL that should be implemented by the platform.

* ``prof_hal_init()``: Initialize the counter hardware.

* ``prof_hal_get_count()``: Get current counter value.

Users shall implement platform-specific hardware support in ``prof_hal_init()``
and ``prof_hal_get_count()`` under `export/platform`.

Take `export/platform/tfm_hal_dwt_prof.c` as an example, it uses Data Watchpoint
and Trace unit (DWT) to count the CPU cycles which can be a reference for
performance.

Setup Database
--------------

The size of the database is determined by ``PROF_DB_MAX`` defined in
`export/prof_common.h`.

The developer can override the size by redefining ``PROF_DB_MAX``.

Add Checkpoints
===============

The developer should identify the places in the source code for adding the
checkpoints. The count value of the timer or CPU cycle will be saved into the
database for the checkpoints. The interface APIs are defined in `export/prof_intf_s.h` for the secure side.

It's also supported to add checkpoints on the non-secure side.
Add `export/ns/prof_intf_ns.c` to the source file list of the non-secure side.
The interface APIs for the non-secure side are defined in `export/ns/prof_intf_ns.h`.

The counter logging related APIs are defined in macros to keep the interface
consistent between the secure and non-secure sides.

Users can call macro ``PROF_TIMING_LOG()`` logs the counter value.

.. code-block:: c
  PROF_TIMING_LOG(topic_id, cp_id);

+------------+--------------------------------------------------------------+
| Parameters | Description                                                  |
+============+==============================================================+
| topic_id   | Topic is used to gather a group of checkpoints.              |
|            | It's useful when you have many checkpoints for different     |
|            | purposes. Topic can help to organize them and filter the     |
|            | related information out. It's an 8-bit unsigned value.       |
+------------+--------------------------------------------------------------+
| cp_id      | Checkpoint ID. Different topics can have same cp_id.         |
|            | It's a 16-bit unsigned value.                                |
+------------+--------------------------------------------------------------+

Collect Data
============

After successfully running the program, the data should be saved into the database.
The developer can dump the data through the interface defined in the header
files mentioned above.

For the same consistent reason as counter logging, the same macros are defined as
the interfaces for both secure and non-secure sides.

The data fetching interfaces work in a stream way. ``PROF_FETCH_DATA_START`` and
``PROF_FETCH_DATA_BY_TOPIC_START`` search the data that matches the given pattern
from the beginning of the database. ``PROF_FETCH_DATA_CONTINUE`` and
``PROF_FETCH_DATA_BY_TOPIC_CONTINUE`` search from the next data set of the
previous result.

.. Note::

    All the APIs increase the internal search index, be careful about mixing using them
    for different checkpoints and topics at the same time.

The match condition of a search is controlled by the tag mask. It's ``tag value``
& ``tag_mask`` == ``tag_pattern``. To enumerate the whole database, set
``tag_mask`` and ``tag_pattern`` both to ``0``.

* ``PROF_FETCH_DATA_XXX``: The generic interface for getting data.
* ``PROF_FETCH_DATA_BY_TOPIC_XXX``: Get data for a specific ``topic``.

The APIs return ``false`` if no matching data is found until the end of the database.

Calibration
===========

The profiler itself has the tick or cycle cost. To get more accurate data, a
calibration system is introduced. It's optional.

The counter logging APIs can be called from the secure or non-secure side. And the
cost of calling functions from these two worlds is different. So, secure and
non-secure have different calibration data.

The system performance might float during the initialization, for example, change
CPU frequency, enable cache, etc. So, it's recommended that the calibration is
done just before the first checkpoint.

* ``PROF_DO_CALIBRATE``: Call this macro to get the calibration value. The more ``rounds``
  the more accurate.
* ``PROF_GET_CALI_VALUE_FROM_TAG``: Get the calibration value from the tag.
  The calibrated counter is ``current_counter - previous_counter - current_cali_value``.
  Here ``current_cali_value`` equals ``PROF_GET_CALI_VALUE_FROM_TAG`` (current_tag).

Data Analysis
=============

Data analysis interfaces can be used to do some basic analysis and the data
returned is calibrated already.

``PROF_DATA_DIFF``: Get the counter value difference for the two tags. Returning
``0`` indicates errors.

If the checkpoints are logged by multi-times, you can get the following counter
value differences between two tags:

* ``PROF_DATA_DIFF_MIN``: Get the minimum counter value difference for the two tags.
  Returning ``UINT32_MAX`` indicates errors.
* ``PROF_DATA_DIFF_MAX``: Get the maximum counter value difference for the two tags.
  Returning ``0`` indicates errors.
* ``PROF_DATA_DIFF_AVG``: Get the average counter value difference for the two tags.
  Returning ``0`` indicates errors.

A customized software or tool can be used to generate the analysis report based
on the data.

Profiler Self-test
==================

`profiler_self_test` is a quick test for all interfaces above. To build and run
in the Linux:

.. code-block:: console

  cd profiler_self_test
  mkdir build && cd build
  cmake .. && make
  ./prof_self_test

********************
TF-M Profiling Cases
********************

The profiler tool has already been integrated into TF-M to analyze the program
performance with the built-in profiling cases. Users can also add a new
profiling case to get a specific profiling report. TF-M profiling provides
example profiling cases in `profiling_cases`.

PSA Client API Profiling
========================

This profiling case analyzes the performance of PSA Client APIs called from SPE
and NSPE, including ``psa_connect()``, ``psa_call()``, ``psa_close()`` and ``stateless psa_call()``.
The main structure is:

::

   prof_psa_client_api/
      ├── cases
      │     ├── non_secure
      │     └── secure
      └── partitions
            ├── prof_server_partition
            └── prof_client_partition

* The `cases` folder is the basic SPE and NSPE profiling log and analysis code.
* NSPE can use `prof_log` library to print the analysis result.
* `prof_server_partition` is a dummy secure partition. It immediately returns
  once it receives a PSA client call from a client.
* `prof_client_partition` is the SPE profiling entry to trigger the secure profiling.

To make this profiling report more accurate, It is recommended to disable other
partitions and all irrelevant tests.

Adding New TF-M Profiling Case
==============================

Users can add source folder `<prof_example>` under path `profiling_cases` to
customize performance analysis of target processes, such as the APIs of secure
partitions, the functions in the SPM, or the user's interfaces. The
integration requires these steps:

1. Confirm the target process block to create profiling cases.
2. Enable or create the server partition if necessary. Note that the other
   irrelevant partitions shall be disabled.
3. Find ways to output profiling data.
4. Trigger profiling cases in SPE or NSPE.

   a. For SPE, a secure client partition can be created to trigger the secure profiling.
   b. For NSPE, the profiling case entry can be added to the 'tfm_ns' target under the `tfm_profiling` folder.

.. Note::

   If the profiling case requires extra out-of-tree secure partition build, the
   paths of extra partitions and manifest list file shall be appended in
   ``TFM_EXTRA_PARTITION_PATHS`` and ``TFM_EXTRA_MANIFEST_LIST_FILES``. Refer to
   `Adding Secure Partition`_.

.. _Adding Secure Partition: https://git.trustedfirmware.org/TF-M/trusted-firmware-m.git/tree/docs/integration_guide/services/tfm_secure_partition_addition.rst

--------------

*Copyright (c) 2022-2023, Arm Limited. All rights reserved.*
