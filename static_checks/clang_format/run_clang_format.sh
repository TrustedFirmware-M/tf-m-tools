#!/bin/bash
#-------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

set -e
script_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

. "$script_path/../utils.sh"

TFM_PATH="$(fix_win_path $(get_full_path ./))"

# Check that script executed from root of git repository
if [ "$(git rev-parse --show-toplevel)/" != $TFM_PATH ]
then
    echo "[SCF ClangFormat: ERROR] Please execute script from root of git repository."
    exit 1
fi

echo "[SCF ClangFormat] Checking configuration..."
# Check that everything is configured correctly. Otherwise, run setup script.
if ! command -v clang-format &> /dev/null ||
   [ ! -f $script_path/clang-format-diff.py ] ||
   [ ! -f $TFM_PATH/.clang-format ]
then
    echo "[SCF ClangFormat] Missing configuration, running setup script."
    set -a && source $script_path/setup.sh
fi

echo "[SCF ClangFormat] Configuration complete."
echo ""

if [ ! -d "$TFM_PATH/checks_reports/" ]; then
    mkdir "checks_reports"
fi

out="checks_reports/clang-format.diff"

git diff -U0 --no-color HEAD^ | $script_path/clang-format-diff.py -p1 -style file  > "$TFM_PATH/$out"

if [ ! -s "$TFM_PATH$out" ] ; then
    echo "[SCF ClangFormat: PASS] No corrections to make."
    rm -f "$TFM_PATH$out"
    exit 0
else
    echo "[SCF ClangFormat: WARNING] Style errors found, please refer to $TFM_PATH$out."
    echo "[SCF ClangFormat] Use 'git apply $out' to apply the corrections."
    exit 1
fi
