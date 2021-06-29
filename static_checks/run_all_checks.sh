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

echo ""
echo "[SCF] Running cppcheck"
echo ""

bash "$root_path/cppcheck/run_cppcheck.sh"

echo ""
echo "[SCF] Running clang_format"
echo ""

bash "$root_path/clang_format/run_clang_format.sh"

echo ""
echo "[SCF] Running checkpatch"
echo ""

bash "$root_path/checkpatch/run_checkpatch.sh"

echo ""
echo "[SCF] Running copyright header check"
echo ""

python3 "$root_path/header_check/run_header_check.py" $1
exit 0
