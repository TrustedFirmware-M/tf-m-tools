#-------------------------------------------------------------------------------
# Copyright (c) 2023, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

cmake_policy(SET CMP0079 NEW)

add_library(non_secure_prof_psa_client_api INTERFACE)

target_sources(non_secure_prof_psa_client_api
    INTERFACE
        non_secure_prof_psa_client_api.c
        ${TFM_PROFILING_PATH}/export/ns/prof_intf_ns.c
)

target_include_directories(non_secure_prof_psa_client_api
    INTERFACE
        ${PROF_PSA_CLIENT_API_CASE_PATH}/non_secure
        ${PROF_PSA_CLIENT_API_CASE_PATH}/
        ${TFM_PROFILING_PATH}/profiler
        ${TFM_PROFILING_PATH}/export/ns
        ${TFM_PROFILING_PATH}/export
)

target_link_libraries(non_secure_prof_psa_client_api
    INTERFACE
        tfm_log
)

###################### TF-M Non-secure Profiling ###############################

target_link_libraries(tfm_ns_profiling
    INTERFACE
        non_secure_prof_psa_client_api
)
