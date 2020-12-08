#!/usr/bin/env bash
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

set_default MCUBOOT_PATH ${TEST_DIR}/mcuboot
if ! test -f ${MCUBOOT_PATH}/success
then
    mkdir -p ${MCUBOOT_PATH}
    git clone https://github.com/mcu-tools/mcuboot ${MCUBOOT_PATH}
    pushd ${MCUBOOT_PATH}
    git checkout 81d19f0
    popd
    touch ${MCUBOOT_PATH}/success
fi

set_default MBEDCRYPTO_PATH ${TEST_DIR}/mbedtls
if ! test -f ${MBEDCRYPTO_PATH}/success
then
    mkdir -p ${MBEDCRYPTO_PATH}
    git clone https://github.com/ARMmbed/mbedtls -b mbedtls-2.24.0 ${MBEDCRYPTO_PATH}
    pushd ${MBEDCRYPTO_PATH}
    git am ${SOURCE_DIR}/lib/ext/mbedcrypto/*.patch
    popd
    touch ${MBEDCRYPTO_PATH}/success
fi

set_default TFM_TEST_REPO_PATH ${TEST_DIR}/tf-m-tests
if ! test -f ${TFM_TEST_REPO_PATH}/success
then
    mkdir -p ${TFM_TEST_REPO_PATH}
    git clone https://git.trustedfirmware.org/TF-M/tf-m-tests.git ${TFM_TEST_REPO_PATH}
    touch ${TFM_TEST_REPO_PATH}/success
fi

set_default BUILD_TYPE debug
set_default COMPILER GNUARM
set_default FIH_PROFILE OFF
set_default TFM_LEVEL 2

set_default BUILD_DIR ${TEST_DIR}/build_${COMPILER}_${BUILD_TYPE}_${FIH_PROFILE}_${TFM_LEVEL}

set -e

mkdir -p ${BUILD_DIR}
pushd ${SOURCE_DIR}
cmake -B ${BUILD_DIR} \
    -DCMAKE_BUILD_TYPE=${BUILD_TYPE} \
    -DTFM_TOOLCHAIN_FILE=toolchain_${COMPILER}.cmake \
    -DTFM_PLATFORM=mps2/an521 \
    -DTFM_PSA_API=ON \
    -DDEBUG_AUTHENTICATION=FULL \
    -DTFM_ISOLATION_LEVEL=${TFM_LEVEL} \
    -DTFM_FIH_PROFILE=${FIH_PROFILE} \
    -DMCUBOOT_PATH=${MCUBOOT_PATH} \
    -DMBEDCRYPTO_PATH=${MBEDCRYPTO_PATH} \
    -DTFM_TEST_REPO_PATH=${TFM_TEST_REPO_PATH} \
    .
popd

pushd ${BUILD_DIR}
make clean
make -j install
popd

set +e
