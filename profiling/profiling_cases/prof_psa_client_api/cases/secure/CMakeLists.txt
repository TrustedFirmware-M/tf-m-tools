#-------------------------------------------------------------------------------
# Copyright (c) 2023, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

cmake_policy(SET CMP0079 NEW)

add_library(secure_prof_psa_client_api INTERFACE)

target_sources(secure_prof_psa_client_api
    INTERFACE
        secure_prof_psa_client_api.c
        ${TFM_PROF_PATH}/profiler/profiler.c
        ${TFM_PROF_PATH}/export/platform/tfm_hal_dwt_prof.c
)

target_include_directories(secure_prof_psa_client_api
    INTERFACE
        ${PROF_PSA_CLIENT_API_CASE_PATH}/secure
        ${PROF_PSA_CLIENT_API_CASE_PATH}/
        ${TFM_PROF_PATH}/export
        ${TFM_PROF_PATH}/profiler
)

target_link_libraries(secure_prof_psa_client_api
    INTERFACE
        tfm_sprt
)

target_compile_definitions(secure_prof_psa_client_api
    INTERFACE
        CONFIG_TFM_ENALBE_PROFILING
)
