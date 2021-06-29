#!/bin/bash
#-------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

CHECKPATCH_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CHECKPATCH_REPO="https://raw.githubusercontent.com/torvalds/linux/v5.9/scripts"

download_file() {
    F_PATH="$CHECKPATCH_PATH/$1"
    curl "$CHECKPATCH_REPO/$1" --output "$F_PATH" &>/dev/null

    if [ $? != 0 ]; then
        echo "[SCF checkpatch] Error downloading file $1"
        exit 1
    else
        if [ "$1" = "checkpatch.pl" ]; then
            echo "[SCF checkpatch] $F_PATH --> chmod 740"
            chmod 750 "$F_PATH"
        else
            echo "[SCF checkpatch] $F_PATH --> chmod 640"
            chmod 640 "$F_PATH"
        fi
    fi
}

# Download required files
download_file checkpatch.pl
download_file const_structs.checkpatch
download_file spelling.txt
