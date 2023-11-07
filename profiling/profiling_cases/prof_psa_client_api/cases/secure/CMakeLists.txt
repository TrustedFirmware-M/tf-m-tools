#-------------------------------------------------------------------------------
# Copyright (c) 2023, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

cmake_policy(SET CMP0079 NEW)

set(TFM_PROFILING_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../../../../)

add_library(secure_prof_psa_client_api INTERFACE)

target_sources(secure_prof_psa_client_api
    INTERFACE
        secure_prof_psa_client_api.c
        ${TFM_PROFILING_PATH}/profiler/profiler.c
        ${TFM_PROFILING_PATH}/export/platform/tfm_hal_dwt_prof.c
)

target_include_directories(secure_prof_psa_client_api
    INTERFACE
        .
        ..
        ${TFM_PROFILING_PATH}/export
        ${TFM_PROFILING_PATH}/profiler
)

target_link_libraries(secure_prof_psa_client_api
    INTERFACE
        tfm_sprt
)

target_compile_definitions(secure_prof_psa_client_api
    INTERFACE
        CONFIG_TFM_ENABLE_PROFILING
)
