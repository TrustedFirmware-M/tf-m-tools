#!/usr/bin/env bash
# Copyright (c) 2021-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

set_default BUILD_TYPE Debug
set_default COMPILER GNUARM
set_default FIH_PROFILE OFF
set_default TFM_LEVEL 2

set_default BUILD_DIR ${TEST_DIR}/build_${COMPILER}_${BUILD_TYPE}_${FIH_PROFILE}_${TFM_LEVEL}

set -e

mkdir -p ${BUILD_DIR}
pushd ${SOURCE_DIR}
cmake -S . -B ${BUILD_DIR} \
    -DCMAKE_BUILD_TYPE=${BUILD_TYPE} \
    -DTFM_TOOLCHAIN_FILE=toolchain_${COMPILER}.cmake \
    -DTFM_PLATFORM=mps2/an521 \
    -DDEBUG_AUTHENTICATION=FULL \
    -DTFM_ISOLATION_LEVEL=${TFM_LEVEL} \
    -DTFM_FIH_PROFILE=${FIH_PROFILE}
popd

pushd ${BUILD_DIR}
make clean
make -j install
popd

set +e
