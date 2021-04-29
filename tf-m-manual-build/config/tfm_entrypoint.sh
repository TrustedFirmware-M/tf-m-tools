#!/bin/bash
#------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#------------------------------------------------------------------------------

dos2unix /opt/trusted-firmware-m/lib/ext/mbedcrypto/*.patch

if [ -z "$1" ]
then
    echo "No argument given - launching a terminal"
    /bin/bash --init-file /opt/setup_env.sh
else
    source /opt/setup_env.sh
    if [[ -v DOCS_DIR ]];
    then
        rm -rf /opt/trusted-firmware-m/${DOCS_DIR}/
    elif [[ -v BUILD_DIR ]];
    then
        rm -rf /opt/trusted-firmware-m/${BUILD_DIR}/
    fi

    cd /opt/trusted-firmware-m
    eval "$1"
fi

