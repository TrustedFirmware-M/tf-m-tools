#!/bin/bash
# Copyright (c) 2020, Arm Limited. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# Setup MPS2 TF-M Platform for building CMSIS-Pack

# TF-M root directory
TFM_ROOT=./trusted-firmware-m

# MCUboot root directory
MCUBOOT_ROOT=./mcuboot

# Source and destination root directory
SRC_ROOT=./trusted-firmware-m/platform/ext/target/mps2/an521
DST_ROOT=./tf-m-platform-mps2/mps2/an521

# Copy TF-M Platform files
mkdir -p ${DST_ROOT}
mkdir -p ${DST_ROOT}/native_drivers
mkdir -p ${DST_ROOT}/partition
mkdir -p ${DST_ROOT}/services/src
cp -v  ${SRC_ROOT}/boot_hal.c ${DST_ROOT}/
cp -v  ${SRC_ROOT}/plat_test.c ${DST_ROOT}/
cp -v  ${SRC_ROOT}/spm_hal.c ${DST_ROOT}/
cp -v  ${SRC_ROOT}/target_cfg.c ${DST_ROOT}/
cp -v  ${SRC_ROOT}/target_cfg.h ${DST_ROOT}/
cp -v  ${SRC_ROOT}/tfm_hal_isolation.c ${DST_ROOT}/
cp -v  ${SRC_ROOT}/tfm_peripherals_def.h ${DST_ROOT}/
cp -v  ${SRC_ROOT}/native_drivers/mpu_armv8m_drv.c ${DST_ROOT}/native_drivers/
cp -v  ${SRC_ROOT}/native_drivers/mpu_armv8m_drv.h ${DST_ROOT}/native_drivers/
cp -v  ${SRC_ROOT}/partition/flash_layout.h ${DST_ROOT}/partition/
cp -v  ${SRC_ROOT}/partition/region_defs.h ${DST_ROOT}/partition/
cp -v  ${SRC_ROOT}/services/src/tfm_platform_system.c ${DST_ROOT}/services/src/

# Copy TF-M Platform device files (temporary directory before patching)
mkdir -p ${DST_ROOT}/device
mkdir -p ${DST_ROOT}/device/bl2
mkdir -p ${DST_ROOT}/device/secure
mkdir -p ${DST_ROOT}/device/non_secure
cp -v  ${SRC_ROOT}/cmsis_driver_config.h ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/device_cfg.h ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/RTE_Device.h ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/armclang/startup_cmsdk_mps2_an521_bl2.s ${DST_ROOT}/device/bl2/
cp -v  ${SRC_ROOT}/armclang/startup_cmsdk_mps2_an521_s.s ${DST_ROOT}/device/secure/
cp -v  ${SRC_ROOT}/armclang/startup_cmsdk_mps2_an521_ns.s ${DST_ROOT}/device/non_secure/
cp -v  ${SRC_ROOT}/armclang/mps2_an521_bl2.sct ${DST_ROOT}/device/bl2/
cp -v  ${SRC_ROOT}/armclang/mps2_an521_ns.sct ${DST_ROOT}/device/non_secure/
cp -v  ${SRC_ROOT}/cmsis_core/cmsis.h ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/cmsis_core/cmsis_cpu.h ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/cmsis_core/mps2_an521.h ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/cmsis_core/platform_irq.h ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/cmsis_core/platform_regs.h ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/cmsis_core/system_cmsdk_mps2_an521.c ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/cmsis_core/system_cmsdk_mps2_an521.h ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/retarget/platform_retarget.h ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/retarget/platform_retarget_dev.c ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/retarget/platform_retarget_dev.h ${DST_ROOT}/device/
cp -v  ${SRC_ROOT}/retarget/platform_retarget_pins.h ${DST_ROOT}/device/
cp -v  ${DST_ROOT}/target_cfg.h ${DST_ROOT}/device/
cp -v  ${DST_ROOT}/target_cfg.c ${DST_ROOT}/device/secure/
cp -v  ${DST_ROOT}/spm_hal.c ${DST_ROOT}/device/secure/
cp -v  ${DST_ROOT}/tfm_peripherals_def.h ${DST_ROOT}/device/secure/

# Apply patches
cd tf-m-platform-mps2
for f in ../tf-m-platform-mps2_patch/*.patch
  do
    git apply -v $f
done
cd ..

# Update TF-M Platform files (after patching)
cp -vf ${DST_ROOT}/device/target_cfg.h ${DST_ROOT}/
cp -vf ${DST_ROOT}/device/secure/target_cfg.c ${DST_ROOT}/
cp -vf ${DST_ROOT}/device/secure/spm_hal.c ${DST_ROOT}/
cp -vf ${DST_ROOT}/device/secure/tfm_peripherals_def.h ${DST_ROOT}/

# Destination path for projects (bl2+secure)
DST_PATH="
  ${DST_ROOT}/project/fvp/tfm_bl/bl2
  ${DST_ROOT}/project/fvp/tfm_bl/tfm_s
  ${DST_ROOT}/project/fvp/tfm/tfm_s
  ${DST_ROOT}/test/fvp/ipc_l1/tfm_s
  ${DST_ROOT}/test/fvp/ipc_l2/tfm_s
  ${DST_ROOT}/test/fvp/ipc_l3/tfm_s
  ${DST_ROOT}/test/fvp/sfn/tfm_s
"

# Copy TF-M Platform native drivers
FILE_LIST="
  arm_uart_drv.c
  arm_uart_drv.h
  mpc_sie200_drv.c
  mpc_sie200_drv.h
  ppc_sse200_drv.c
  ppc_sse200_drv.h
"
SUB_DIR=native_drivers
for d in ${DST_PATH}
do
  mkdir -p $d/${SUB_DIR}
  for f in ${FILE_LIST}
  do
    cp -v ${SRC_ROOT}/${SUB_DIR}/$f $d/${SUB_DIR}/
  done
done

FILE_LIST="
  timer_cmsdk.c
  timer_cmsdk.h
"
SUB_DIR=native_drivers/timer_cmsdk
for d in ${DST_PATH}
do
  mkdir -p $d/${SUB_DIR}
  for f in ${FILE_LIST}
  do
    cp -v ${SRC_ROOT}/${SUB_DIR}/$f $d/${SUB_DIR}/
  done
done

# Copy TF-M Platform CMSIS drivers
FILE_LIST="
  Driver_Flash.c
  Driver_MPC.c
  Driver_PPC.c
  Driver_USART.c
"
SUB_DIR=cmsis_drivers
for d in ${DST_PATH}
do
  mkdir -p $d/${SUB_DIR}
  for f in ${FILE_LIST}
  do
    cp -v ${SRC_ROOT}/${SUB_DIR}/$f $d/${SUB_DIR}/
  done
done

FILE_LIST="
  Driver_MPC.h
  Driver_PPC.h
"
SRC_DIR=../../../driver
DST_DIR=cmsis_drivers
for d in ${DST_PATH}
do
  mkdir -p $d/${DST_DIR}
  for f in ${FILE_LIST}
  do
    cp -v ${SRC_ROOT}/${SRC_DIR}/$f $d/${DST_DIR}/
  done
done

# Destination directory for device files
DST_DIR=RTE/Device/SMM-SSE-200

# Destination path for projects (bl2+secure+non_secure)
DST_PATH="
  ${DST_ROOT}/project/fvp/tfm_bl/bl2
  ${DST_ROOT}/project/fvp/tfm_bl/tfm_s
  ${DST_ROOT}/project/fvp/tfm_bl/tfm_ns
  ${DST_ROOT}/project/fvp/tfm/tfm_s
  ${DST_ROOT}/project/fvp/tfm/tfm_ns
  ${DST_ROOT}/test/fvp/ipc_l1/tfm_s
  ${DST_ROOT}/test/fvp/ipc_l1/tfm_ns
  ${DST_ROOT}/test/fvp/ipc_l2/tfm_s
  ${DST_ROOT}/test/fvp/ipc_l2/tfm_ns
  ${DST_ROOT}/test/fvp/ipc_l3/tfm_s
  ${DST_ROOT}/test/fvp/ipc_l3/tfm_ns
  ${DST_ROOT}/test/fvp/sfn/tfm_s
  ${DST_ROOT}/test/fvp/sfn/tfm_ns
"

# Copy device files (bl2+secure+non_secure)
for d in ${DST_PATH}
do
  mkdir -p $d/${DST_DIR}
  cp -v ${DST_ROOT}/device/*.* $d/${DST_DIR}/
done

# Destination path for projects (bl2)
DST_PATH="
  ${DST_ROOT}/project/fvp/tfm_bl/bl2
"

# Copy device files (bl2)
for d in ${DST_PATH}
do
  mkdir -p $d/${DST_DIR}
  cp -v ${DST_ROOT}/device/bl2/*.* $d/${DST_DIR}/
done

# Copy TF-M specific files (bl2)
for d in ${DST_PATH}
do
  mkdir -p $d/RTE/TFM
  cp -v ${TFM_ROOT}/bl2/ext/mcuboot/config/mcuboot-mbedtls-cfg.h $d/RTE/TFM/
  sed -i '/#define __MCUBOOT_MBEDTLS_CFG__/a\\n#include "bl2_config.h"' $d/RTE/TFM/mcuboot-mbedtls-cfg.h
  unix2dos -q $d/RTE/TFM/mcuboot-mbedtls-cfg.h
  mkdir -p $d/RTE/TFM_Platform/SMM-SSE-200
  cp -v ${DST_ROOT}/boot_hal.c $d/RTE/TFM_Platform/SMM-SSE-200/
  cp -v ${DST_ROOT}/partition/flash_layout.h $d/RTE/TFM_Platform/SMM-SSE-200/
  cp -v ${DST_ROOT}/partition/region_defs.h $d/RTE/TFM_Platform/SMM-SSE-200/
done

# Destination path for projects (secure)
DST_PATH="
  ${DST_ROOT}/project/fvp/tfm_bl/tfm_s
  ${DST_ROOT}/project/fvp/tfm/tfm_s
  ${DST_ROOT}/test/fvp/ipc_l1/tfm_s
  ${DST_ROOT}/test/fvp/ipc_l2/tfm_s
  ${DST_ROOT}/test/fvp/ipc_l3/tfm_s
  ${DST_ROOT}/test/fvp/sfn/tfm_s
"

# Copy device files (secure)
for d in ${DST_PATH}
do
  mkdir -p $d/${DST_DIR}
  cp -v ${DST_ROOT}/device/secure/*.* $d/${DST_DIR}/
done

# Copy TF-M specific files (secure)
for d in ${DST_PATH}
do
  mkdir -p $d/RTE/TFM
  cp -v ${TFM_ROOT}/platform/ext/common/armclang/tfm_common_s.sct $d/RTE/TFM/
  cp -v ${TFM_ROOT}/platform/ext/common/armclang/tfm_isolation_l3.sct $d/RTE/TFM/
  cp -v ${TFM_ROOT}/lib/ext/mbedcrypto/mbedcrypto_config/tfm_mbedcrypto_config.h $d/RTE/TFM/
  mkdir -p $d/RTE/TFM_Platform
  cp -v ${TFM_ROOT}/platform/ext/common/template/attest_hal.c $d/RTE/TFM_Platform/
  mkdir -p $d/RTE/TFM_Platform/SMM-SSE-200
  cp -v ${DST_ROOT}/partition/flash_layout.h $d/RTE/TFM_Platform/SMM-SSE-200/
  cp -v ${DST_ROOT}/partition/region_defs.h $d/RTE/TFM_Platform/SMM-SSE-200/
  cp -v ${DST_ROOT}/services/src/tfm_platform_system.c $d/RTE/TFM_Platform/SMM-SSE-200/
done

# Destination path for projects (non_secure)
DST_PATH="
  ${DST_ROOT}/project/fvp/tfm_bl/tfm_ns
  ${DST_ROOT}/project/fvp/tfm/tfm_ns
  ${DST_ROOT}/test/fvp/ipc_l1/tfm_ns
  ${DST_ROOT}/test/fvp/ipc_l2/tfm_ns
  ${DST_ROOT}/test/fvp/ipc_l3/tfm_ns
  ${DST_ROOT}/test/fvp/sfn/tfm_ns
"

# Copy device files (non_secure)
for d in ${DST_PATH}
do
  mkdir -p $d/${DST_DIR}
  cp -v ${DST_ROOT}/device/non_secure/* $d/${DST_DIR}/
done

# Adjust memory map of non-secure project when using bootloader
pushd ${DST_ROOT}/project/fvp/tfm_bl/tfm_ns/${DST_DIR}
sed -i 's/NS_CODE_START           (0x00100000)/NS_CODE_START           (0x00100400)/' mps2_an521_ns.sct
sed -i 's/NS_CODE_SIZE            (0x00080000)/NS_CODE_SIZE            (0x0007F800)/' mps2_an521_ns.sct
unix2dos -q mps2_an521_ns.sct
popd

# Remove temporary device files
rm -r  ${DST_ROOT}/device

# Copy root and encryption keys
cp -v  ${TFM_ROOT}/bl2/ext/mcuboot/root-RSA-3072.pem ${DST_ROOT}/project/fvp/tfm_bl/tfm_s/
cp -v  ${TFM_ROOT}/bl2/ext/mcuboot/root-RSA-3072_1.pem ${DST_ROOT}/project/fvp/tfm_bl/tfm_ns/
cp -v  ${MCUBOOT_ROOT}/enc-rsa2048-pub.pem ${DST_ROOT}/project/fvp/tfm_bl/tfm_s/
cp -v  ${MCUBOOT_ROOT}/enc-rsa2048-pub.pem ${DST_ROOT}/project/fvp/tfm_bl/tfm_ns/

# Copy pack addon files
cp -vr ./tf-m-platform-mps2_addon/* ./tf-m-platform-mps2/
