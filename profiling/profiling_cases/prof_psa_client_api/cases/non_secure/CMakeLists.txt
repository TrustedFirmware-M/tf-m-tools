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
        ${TFM_PROF_PATH}/export/ns/prof_intf_ns.c
)

target_include_directories(non_secure_prof_psa_client_api
    INTERFACE
        ${PROF_PSA_CLIENT_API_CASE_PATH}/non_secure
        ${PROF_PSA_CLIENT_API_CASE_PATH}/
        ${TFM_PROF_PATH}/profiler
        ${TFM_PROF_PATH}/export/ns
        ${TFM_PROF_PATH}/export
)

target_link_libraries(non_secure_prof_psa_client_api
    INTERFACE
        tfm_log
)

target_compile_definitions(non_secure_prof_psa_client_api
    INTERFACE
        CONFIG_TFM_ENALBE_PROFILING
)
