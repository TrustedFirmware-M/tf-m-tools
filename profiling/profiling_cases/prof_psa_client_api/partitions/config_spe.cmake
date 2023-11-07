#-------------------------------------------------------------------------------
# Copyright (c) 2023, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

set(CONFIG_TFM_ENABLE_PROFILING ON CACHE BOOL "Enable profiling for TF-M")
set(CMAKE_BUILD_TYPE Release)

# Secure profiling case runs in secure profiling client partition. The Profiling
# Log api is implemented by secure patition log interfaces in library tfm_sprt.
# As CMAKE_BUILD_TYPE has already determined the secure partition log level and
# the normal build type Release uses SILENCE. Here use 'FORCE' to replace it.
set(TFM_PARTITION_LOG_LEVEL TFM_PARTITION_LOG_LEVEL_INFO CACHE STRING "Set default Secure Partition log level as INFO level" FORCE)

# Out-of-tree partition configurations
list(APPEND TFM_EXTRA_PARTITION_PATHS
    ${CMAKE_CURRENT_LIST_DIR}/prof_server_partition
    ${CMAKE_CURRENT_LIST_DIR}/prof_client_partition
)

list(APPEND TFM_EXTRA_MANIFEST_LIST_FILES
    ${CMAKE_CURRENT_LIST_DIR}/prof_psa_client_api_manifest_list.yaml
)
