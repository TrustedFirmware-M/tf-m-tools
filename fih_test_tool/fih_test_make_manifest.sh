#!/usr/bin/env bash
# Copyright (c) 2021-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


set_default AXF_FILE ${BUILD_DIR}/bin/tfm_s.axf
set_default OBJDUMP arm-none-eabi-objdump
set_default GDB gdb-multiarch

if ! test -f ${AXF_FILE}
then
    error "no such file ${AXF_FILE}"
fi

# Check if the ELF file specified is compatible
if  ! file ${AXF_FILE} | grep "ELF.*32.*ARM" &>/dev/null
then
    error "Incompatible file: ${AXF_FILE}"
fi

#TODO clean this up, and use less regex

# Dump all objects that have a name containing FIH_LABEL
ADDRESSES=$($OBJDUMP $AXF_FILE -t | grep "FIH_LABEL")
# strip all data except "address, label_name"
ADDRESSES=$(echo "$ADDRESSES" | sed "s/\([[:xdigit:]]*\).*\(FIH_LABEL_.*\)_[0-9]*_[0-9]*/0x\1, \2/g")
# Sort by address in ascending order
ADDRESSES=$(echo "$ADDRESSES" | sort)
# In the case that there is a START followed by another START take the first one
ADDRESSES=$(echo "$ADDRESSES" | sed "N;s/\(.*START.*\)\n\(.*START.*\)/\1/;P;D")
# Same for END except take the second one
ADDRESSES=$(echo "$ADDRESSES" | sed "N;s/\(.*END.*\)\n\(.*END.*\)/\2/;P;D")

# Output in CSV format with a label
echo "Address, Type" > ${BUILD_DIR}/fih_manifest.csv

# Dump all objects that have a name containing FUNCTION
if [ -n "$FUNCTION" ];then
    if [ -n "$(echo "$ADDRESSES" | grep "$FUNCTION")" ];then
        IFS_OLD=$IFS
        IFS=$'\n'
        next_line=0
        for line in $ADDRESSES;
        do
            if [ -n "$(echo "$line" | grep "CRITICAL_POINT")" ] || [ -n "$(echo "$line" | grep "FAILURE_LOOP")" ];then
                echo "$line" >> ${BUILD_DIR}/fih_manifest.csv
                continue
            fi
            if [ -n "$(echo "$line" | grep "$FUNCTION")" ];then
                echo "$line" >> ${BUILD_DIR}/fih_manifest.csv
                next_line=1
                continue
            fi
            if [ $next_line -eq 1 ];then
                echo "$line" >> ${BUILD_DIR}/fih_manifest.csv
                next_line=0
            fi
        done
        IFS=$IFS_OLD
    else
        echo "Function $FUNCTION is not found in TF-M!"
        exit
    fi
else
    echo "$ADDRESSES" >> ${BUILD_DIR}/fih_manifest.csv
fi
