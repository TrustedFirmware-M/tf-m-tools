#!/bin/bash
#-------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

set -e

root_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$root_path/utils.sh"

TFM_PATH="$(fix_win_path $(get_full_path ./))"

if [ -d "$TFM_PATH/checks_reports/" ]; then
    echo "[SCF] Storing reports to $TFM_PATH/checks_reports/"
else
    mkdir "checks_reports"
    echo "[SCF] Storing reports to $TFM_PATH/checks_reports/"
fi

echo "[SCF] Running cppcheck"

. "$root_path/cppcheck/run_cppcheck.sh"

echo "[SCF] Running clang_format"

. "$root_path/clang_format/run_clang_format.sh"

# echo "[SCF] Running checkpatch"

# . "$root_path/checkpatch/run_checkpatch.sh"
exit 0
