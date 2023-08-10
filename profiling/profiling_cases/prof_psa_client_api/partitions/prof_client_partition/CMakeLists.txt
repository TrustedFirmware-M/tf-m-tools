#-------------------------------------------------------------------------------
# Copyright (c) 2023, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

cmake_policy(SET CMP0079 NEW)

############################ Secure profiling case #############################

add_subdirectory(${PROF_PSA_CLIENT_API_CASE_PATH}/secure ${CMAKE_CURRENT_BINARY_DIR}/prof_psa_client_api/cases/secure)

############################ Secure profiling client partition #################

add_library(tfm_app_rot_partition_prof_client_partition STATIC)

target_sources(tfm_app_rot_partition_prof_client_partition
    PRIVATE
        prof_client_partition.c
)

# The generated sources
target_sources(tfm_app_rot_partition_prof_client_partition
    PRIVATE
        ${CMAKE_BINARY_DIR}/generated/secure_fw/partitions/prof_client_partition/auto_generated/intermedia_prof_client_partition.c
)

target_sources(tfm_partitions
    INTERFACE
        ${CMAKE_BINARY_DIR}/generated/secure_fw/partitions/prof_client_partition/auto_generated/load_info_prof_client_partition.c
)

# Set include directory
target_include_directories(tfm_app_rot_partition_prof_client_partition
    PRIVATE
        ${CMAKE_BINARY_DIR}/generated/secure_fw/partitions/prof_client_partition
)

target_include_directories(tfm_partitions
    INTERFACE
        ${CMAKE_BINARY_DIR}/generated/secure_fw/partitions/prof_client_partition
)

target_link_libraries(tfm_app_rot_partition_prof_client_partition
    PUBLIC
        secure_prof_psa_client_api
    PRIVATE
        tfm_sprt
)

############################ Partition Defs ####################################

target_link_libraries(tfm_partitions
    INTERFACE
        tfm_app_rot_partition_prof_client_partition
)
