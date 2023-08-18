#-------------------------------------------------------------------------------
# Copyright (c) 2023, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

cmake_policy(SET CMP0079 NEW)

###################### TF-M Non-secure Profiling ###############################

add_library(tfm_ns_profiling INTERFACE)

target_sources(tfm_ns_profiling
    INTERFACE
        tfm_ns_profiling.c
)

target_include_directories(tfm_ns_profiling
    INTERFACE
        .
)

target_compile_definitions(tfm_ns_profiling
    INTERFACE
        CONFIG_TFM_ENALBE_PROFILING
)

###################### TF-M Non-secure Profiling cases #########################

add_subdirectory(${PROF_PSA_CLIENT_API_CASE_PATH}/non_secure
                 ${CMAKE_CURRENT_BINARY_DIR}/prof_psa_client_api/non_secure)
