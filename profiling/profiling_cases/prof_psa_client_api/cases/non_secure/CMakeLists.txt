#-------------------------------------------------------------------------------
# Copyright (c) 2023, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

cmake_policy(SET CMP0079 NEW)

set(TFM_PROFILING_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../../../../)

add_subdirectory(${TFM_PROFILING_PATH}/profiling_cases/prof_log ${CMAKE_CURRENT_BINARY_DIR}/prof_log)

add_library(non_secure_prof_psa_client_api INTERFACE)

target_sources(non_secure_prof_psa_client_api
    INTERFACE
        non_secure_prof_psa_client_api.c
        ${TFM_PROFILING_PATH}/export/ns/prof_intf_ns.c
)

target_include_directories(non_secure_prof_psa_client_api
    INTERFACE
        .
        ..
        ${TFM_PROFILING_PATH}/profiler
        ${TFM_PROFILING_PATH}/export/ns
        ${TFM_PROFILING_PATH}/export
)

target_link_libraries(non_secure_prof_psa_client_api
    INTERFACE
        prof_log
)
