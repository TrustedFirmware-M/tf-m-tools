#!/bin/bash
#-------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

set -e

script_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$script_path/utils.sh"

TFM_PATH="$(fix_win_path $(get_full_path ./))"

if [ -d "$TFM_PATH/checks_reports/" ]; then
    echo "[SCF] Storing reports to $TFM_PATH/checks_reports/"
else
    mkdir "checks_reports"
    echo "[SCF] Storing reports to $TFM_PATH/checks_reports/"
fi

echo "[SCF] Running cppcheck"

. "$script_path/cppcheck/run_cppcheck.sh"

# echo "[SCF] Running clang_format"

# . "$script_path/clang_format/run_clang_format.sh"

# echo "[SCF] Running checkpatch"

# . "$script_path/checkpatch/run_checkpatch.sh"

exit 0