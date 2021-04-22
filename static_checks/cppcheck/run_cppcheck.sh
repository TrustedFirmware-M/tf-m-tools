#!/bin/bash
#-------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

set -e

script_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

. "$script_path/../utils.sh"

TFM_PATH="$(fix_win_path $(get_full_path ./))"
RAW_OUTPUT=0
FAIL=0

while getopts "hr" opt ; do
  case "$opt" in
    h)
      echo "[SCF cppcheck] Usage: $(basename -- "$0") [-h] [-r] [git_hash]"
      echo "[SCF cppcheck] -r, Raw output. (Default is to create xml reports)."
      echo "[SCF cppcheck] -h, Script help"
      exit 0
      ;;
    r)
      RAW_OUTPUT=1
      ;;
  esac
done


if command -v cppcheck &> /dev/null
then
    echo "[SCF cppcheck] Using $(cppcheck --version)"
else
    echo "[SCF cppcheck] cppcheck not found - installing cppcheck"
    source "$script_path/setup.sh"
fi

cd "$TFM_PATH"

#Library file for cppcheck
library_file="$(fix_win_path $(get_full_path $script_path))/config/arm-cortex-m.cfg"
suppress_file="$(fix_win_path $(get_full_path $script_path))/config/tfm-suppress-list.txt"
toolchain_file="$TFM_PATH/toolchain_GNUARM.cmake"

compile_commands_path="$TFM_PATH/build-cppcheck/compile_commands.json"

if [ -f "$compile_commands_path" ]; then
    echo "[SCF cppcheck] $compile_commands_path already generated"
else
    echo "[SCF cppcheck] generating $compile_commands_path"
    generate_project "$TFM_PATH" " ./" "cppcheck" "-DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DTFM_PLATFORM=arm/mps2/an521 -DTFM_TOOLCHAIN_FILE=$toolchain_file"
    sed -i 's/\\\\\\\"/\\\"/g' $compile_commands_path
fi

function cppcheck_failed {
    echo "[SCF cppcheck: ERROR] cppcheck failed, errors detected. Please check" \
       "logs for details."
    exit 1
}

function check_ouput {
    if grep -q "<error id" $TFM_PATH/checks_reports/cppchk-config.xml; then
        cppcheck_failed
    fi

    if grep -q "<error id" $TFM_PATH/checks_reports/cppchk-src.xml; then
        cppcheck_failed
    fi

    echo "[SCF cppcheck: PASS] cppcheck complete"
    exit 0
}

EXTRA_ARGS="--error-exitcode=1"
if [ "$RAW_OUTPUT" != "1" ] ; then
  # If not in raw output mode, use xml output.
  EXTRA_ARGS="--xml"
fi

trap cppcheck_failed ERR

CPPCHECK_ARGS="$EXTRA_ARGS --enable=all --library="$library_file" --project=$compile_commands_path --suppressions-list="$suppress_file" --inline-suppr"

if [ -d "$TFM_PATH/checks_reports/" ]; then
    echo "[SCF cppcheck] Storing cppcheck reports to $TFM_PATH/checks_reports/"
else
    mkdir "$TFM_PATH/checks_reports"
    echo "[SCF cppcheck] Storing cppcheck reports to $TFM_PATH/checks_reports/"
fi

#Now run cppcheck.
echo
echo '[SCF cppcheck] Checking cppcheck configuration'
echo

if [ "$RAW_OUTPUT" == "1" ] ; then
    cppcheck $CPPCHECK_ARGS --check-config > /dev/null
else
    cppcheck $CPPCHECK_ARGS --check-config 2>checks_reports/cppchk-config.xml
fi

echo
echo '[SCF cppcheck] analyzing files with cppcheck'
echo
if [ "$RAW_OUTPUT" == "1" ] ; then
    cppcheck $CPPCHECK_ARGS > /dev/null
    echo '[SCF cppcheck : PASS] cppcheck complete'
    exit 0
else
    cppcheck $CPPCHECK_ARGS 2>checks_reports/cppchk-src.xml
    check_ouput
fi

