#-------------------------------------------------------------------------------
# Copyright (c) 2022-2023, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------
cmake_minimum_required(VERSION 3.21)

project(prof_self_test VERSION 1.0 DESCRIPTION "Profiler self-test" LANGUAGES C)

add_executable(prof_self_test prof_self_test.c ../profiler/profiler.c)

target_include_directories(prof_self_test
    PUBLIC
        ../profiler
        ../export
)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DPROF_SELF_TEST")
