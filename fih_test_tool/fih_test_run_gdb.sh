#!/usr/bin/env bash
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

set_default QEMU_UART_FIFO ${BUILD_DIR}/qemu_uart
set_default QEMU_MON_FIFO  ${BUILD_DIR}/qemu_mon
set_default QEMU_PIDFILE   ${BUILD_DIR}/qemu_pid
set_default QEMU_VHD       ${BUILD_DIR}/qemu_vhd

rm ${QEMU_MON_FIFO}.* ${QEMU_UART_FIFO}.* ${QEMU_VHD} ${QEMU_PID}

mkfifo ${QEMU_UART_FIFO}.in ${QEMU_UART_FIFO}.out
mkfifo ${QEMU_MON_FIFO}.in ${QEMU_MON_FIFO}.out

rm ${BUILD_DIR}/results.json

# The disk image is used to store snapshots, to allow easier recreation of test
# state
qemu-img create -f qcow2 ${QEMU_VHD} 50M

pushd ${BUILD_DIR}

gdb-multiarch --ex "set architecture armv8-m.main" \
              --ex "set confirm off" \
              --ex "set pagination off" \
              --ex "set target-async on" \
              --ex "file ${BUILD_DIR}/bin/bl2.axf" \
              --ex "add-symbol-file ${BUILD_DIR}/bin/tfm_s.axf  0x00080000" \
              --ex "add-symbol-file ${BUILD_DIR}/bin/tfm_ns.axf 0x00100400" \
              --ex "source ${SCRIPT_DIR}/gdb-tool/fih_test_gdb_python_script.py"

popd

kill $(cat ${QEMU_PIDFILE})

rm -f ${QEMU_MON_FIFO}.* ${QEMU_UART_FIFO}.* ${QEMU_VHD} ${QEMU_PIDFILE}
