#-------------------------------------------------------------------------------
# Copyright (c) 2023, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

add_library(prof_log STATIC)

target_sources(prof_log
    PUBLIC
        prof_log_raw.c
)

target_include_directories(prof_log
    PUBLIC
        .
)

target_link_libraries(prof_log
    PUBLIC
        platform_ns
)
