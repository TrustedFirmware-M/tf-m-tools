###############################
TF-M Example Partition - Readme
###############################
The TF-M example partition is a simple secure partition implementation provided
to aid development of new secure partitions. It implements one RoT Service and
one interrupt handler.

********************************
How to run the example partition
********************************
#. Copy the ``example_partition`` directory to the ``secure_fw/partitions``
   directory of the TF-M repo.
#. Add the following entry to ``tools/tfm_manifest_list.yaml``::

    {
      "name": "TF-M Example Partition",
      "short_name": "TFM_SP_EXAMPLE",
      "manifest": "secure_fw/partitions/example_partition/tfm_example_partition.yaml",
      "tfm_partition_ipc": true,
      "conditional": "TFM_PARTITION_EXAMPLE",
      "version_major": 0,
      "version_minor": 1,
      "pid": 270,
      "linker_pattern": {
        "library_list": [
           "*tfm_partition_example.*"
        ]
      }
    }

#. Build TF-M in the usual way, but provide ``-DTFM_PARTITION_EXAMPLE=ON`` as a
   parameter to the CMake command.

--------------

*Copyright (c) 2020, Arm Limited. All rights reserved.*
