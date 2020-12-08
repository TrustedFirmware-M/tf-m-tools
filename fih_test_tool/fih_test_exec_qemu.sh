#!/usr/bin/env bash
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

qemu-system-arm \
    -M mps2-an521 \
    -kernel ${BUILD_DIR}/bin/bl2.axf \
    -device loader,file=${BUILD_DIR}/bin/tfm_s_ns_signed.bin,addr=0x10080000 \
    -pidfile ${QEMU_PIDFILE} \
    -drive file=${QEMU_VHD},id=disk,format=qcow2 \
    -d guest_errors \
    -D /tmp/qemu.log \
    -display none \
    -s -S \
    -chardev file,id=char0,path=/dev/null \
    -monitor pipe:${QEMU_MON_FIFO} \
    -daemonize
