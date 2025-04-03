#-------------------------------------------------------------------------------
# Copyright (c) 2023, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

cmake_policy(SET CMP0079 NEW)

add_library(tfm_app_rot_partition_prof_server_partition STATIC)

target_sources(tfm_app_rot_partition_prof_server_partition
    PRIVATE
        prof_server_partition.c
)

# The generated sources
target_sources(tfm_app_rot_partition_prof_server_partition
    PRIVATE
        ${CMAKE_BINARY_DIR}/generated/secure_fw/partitions/prof_server_partition/auto_generated/intermedia_prof_server_partition.c
)

target_sources(tfm_partitions
    INTERFACE
        ${CMAKE_BINARY_DIR}/generated/secure_fw/partitions/prof_server_partition/auto_generated/load_info_prof_server_partition.c
)

target_include_directories(tfm_app_rot_partition_prof_server_partition
    PRIVATE
        ${CMAKE_BINARY_DIR}/generated/secure_fw/partitions/prof_server_partition
)

target_include_directories(tfm_partitions
    INTERFACE
        ${CMAKE_BINARY_DIR}/generated/secure_fw/partitions/prof_server_partition
)

target_link_libraries(tfm_app_rot_partition_prof_server_partition
    PRIVATE
        tfm_log_headers
)

############################ Partition Defs ####################################

target_link_libraries(tfm_partitions
    INTERFACE
        tfm_app_rot_partition_prof_server_partition
)
