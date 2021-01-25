#!/bin/bash
# Copyright (c) 2020, Arm Limited. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# Setup TF-M for building CMSIS-Packs

# Install required Python packages
pip install -r requirements.txt

# TF-M repositories
TFM_URL=https://git.trustedfirmware.org/TF-M/trusted-firmware-m.git
TFM_TESTS_URL=https://git.trustedfirmware.org/TF-M/tf-m-tests.git

# TF-M tag
TFM_TAG=TF-Mv1.2.0

# External repositories
MCUBOOT_URL=https://github.com/mcu-tools/mcuboot.git
MCUBOOT_TAG=v1.7.0

# Clone TF-M repository
git clone $TFM_URL --branch $TFM_TAG --single-branch
errorlevel=$?
if [ $errorlevel -gt 0 ]
  then
  echo "Error: Cloning TF-M repository failed"
  echo " "
  exit
fi

# Clone TF-M tests repository
git clone $TFM_TESTS_URL --branch $TFM_TAG --single-branch
errorlevel=$?
if [ $errorlevel -gt 0 ]
  then
  echo "Error: Cloning TF-M tests repository failed"
  echo " "
  exit
fi

# Clone MCUboot repository
git clone $MCUBOOT_URL --branch $MCUBOOT_TAG --single-branch
errorlevel=$?
if [ $errorlevel -gt 0 ]
  then
  echo "Error: Cloning MCUboot repository failed"
  echo " "
  exit
fi

# Copy files from MCUboot to TF-M
mkdir -p ./trusted-firmware-m/lib/ext/mcuboot/boot
cp -vr ./mcuboot/boot/bootutil ./trusted-firmware-m/lib/ext/mcuboot/boot/

# Create MCUboot config file (from template)
pushd ./trusted-firmware-m/bl2/ext/mcuboot/include/mcuboot_config
cp -v  mcuboot_config.h.in mcuboot_config.h
# Remove defines which are already defined in bl2_config.h
sed -i 's/#cmakedefine/\/\/#define/' mcuboot_config.h
sed -i 's/#define MCUBOOT_LOG_LEVEL/\/\/#define MCUBOOT_LOG_LEVEL/' mcuboot_config.h
unix2dos -q mcuboot_config.h
popd

# Create TF-M Mbed Crypto config file (from default config)
pushd ./trusted-firmware-m/lib/ext/mbedcrypto/mbedcrypto_config
cp -v  tfm_mbedcrypto_config_default.h tfm_mbedcrypto_config.h
popd

# Apply patches to TF-M
cd trusted-firmware-m
for f in ../trusted-firmware-m_patch/*.patch
  do
    git apply -v $f
done
cd ..

# Apply patches to TF-M tests
cd tf-m-tests
for f in ../tf-m-tests_patch/*.patch
  do
    git apply -v $f
done
cd ..

# Generate files from templates
export TFM_TEST_PATH="${PWD}/tf-m-tests/test"
python ./trusted-firmware-m/tools/tfm_parse_manifest_list.py \
  -o ./trusted-firmware-m \
  -m ./trusted-firmware-m/tools/tfm_manifest_list.yaml \
  -f ./trusted-firmware-m/tools/tfm_generated_file_list.yaml \
     ./trusted-firmware-m/platform/ext/target/mps2/an521/generated_file_list.yaml

# Copy generated files for TF-M tests
cp -vr ./trusted-firmware-m/test/test_services ./tf-m-tests/test

# Update linker scripts (TFM_IRQ_TEST_1_LINKER: tfm_enable_irq/tfm_disable_irq)
pushd ./trusted-firmware-m/platform/ext/common/armclang
for f in tfm_common_s.sct tfm_isolation_l3.sct
do
  sed -i '/TFM_IRQ_TEST_1_ATTR_FN/i*(:gdef:tfm_enable_irq)' $f
  sed -i '/TFM_IRQ_TEST_1_ATTR_FN/i*(:gdef:tfm_disable_irq)' $f
  unix2dos -q $f
done
popd

# Move files from TF-M tests to TF-M
mv -v  ./tf-m-tests/app/os_wrapper_cmsis_rtos_v2.c ./trusted-firmware-m/interface/src/

# Copy files from TF-M tests to TF-M (for building doxygen based documentation)
cp -vr ./tf-m-tests/test ./trusted-firmware-m

# Move/copy files from TF-M to TF-M tests
mkdir -p ./tf-m-tests/interface/include
mkdir -p ./tf-m-tests/interface/src
mkdir -p ./tf-m-tests/platform/ext/common
mkdir -p ./tf-m-tests/platform/include
mv -v  ./trusted-firmware-m/interface/include/tfm_ns_svc.h ./tf-m-tests/interface/include/
mv -v  ./trusted-firmware-m/interface/include/tfm_nspm_svc_handler.h ./tf-m-tests/interface/include/
mv -v  ./trusted-firmware-m/interface/src/tfm_nspm_api.c ./tf-m-tests/interface/src/
mv -v  ./trusted-firmware-m/interface/src/tfm_nspm_svc_handler.c ./tf-m-tests/interface/src/
cp -v  ./trusted-firmware-m/secure_fw/spm/include/tfm_boot_status.h ./tf-m-tests/interface/include/
cp -v  ./trusted-firmware-m/platform/ext/common/uart_stdout.c ./tf-m-tests/platform/ext/common/
cp -v  ./trusted-firmware-m/platform/ext/common/uart_stdout.h ./tf-m-tests/platform/ext/common/
cp -v  ./trusted-firmware-m/platform/include/region.h ./tf-m-tests/platform/include/
cp -v  ./trusted-firmware-m/platform/include/tfm_plat_crypto_keys.h ./tf-m-tests/platform/include/
cp -v  ./trusted-firmware-m/platform/include/tfm_plat_defs.h ./tf-m-tests/platform/include/
cp -v  ./trusted-firmware-m/platform/include/tfm_plat_ns.h ./tf-m-tests/platform/include/
cp -v  ./trusted-firmware-m/platform/include/tfm_plat_test.h ./tf-m-tests/platform/include/
cp -v  ./trusted-firmware-m/secure_fw/partitions/audit_logging/audit_core.h ./tf-m-tests/test/suites/audit/non_secure/
cp -v  ./trusted-firmware-m/secure_fw/partitions/initial_attestation/attest.h ./tf-m-tests/test/suites/attestation/
cp -v  ./trusted-firmware-m/secure_fw/partitions/initial_attestation/attest_eat_defines.h ./tf-m-tests/test/suites/attestation/
cp -v  ./trusted-firmware-m/secure_fw/partitions/initial_attestation/attest_token.h ./tf-m-tests/test/suites/attestation/

# Copy TF-M pack addon files
cp -vr ./trusted-firmware-m_addon/* ./trusted-firmware-m/

# Copy TF-M test pack addon files
cp -vr ./tf-m-tests_addon/* ./tf-m-tests/
