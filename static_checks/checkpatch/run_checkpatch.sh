#!/bin/bash
#-------------------------------------------------------------------------------
# Copyright (c) 2018-2021, Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

# Capture the path the script is at
CHECKPATCH_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

. "$CHECKPATCH_PATH/../utils.sh"
TFM_PATH="$(fix_win_path $(get_full_path ./))"

# Set the output file to common output directory
OUTPUT_FILE_PATH="$TFM_PATH/checks_reports/checkpatch_report.log"

# Set the chechpatch executable
CHECKPATCH_APP="$CHECKPATCH_PATH/checkpatch.pl"


# Parse the configuration file
CHECKPATCH_CONFG="$(grep -o '^[^#]*' $CHECKPATCH_PATH/checkpatch.conf)"

# Directories which are ignored either because they contain external code
# or documentation/ 3rd party tools

# Please keep it in sync with the excluded directories the CI uses
# https://git.trustedfirmware.org/next/ci/tf-m-ci-scripts.git/tree/run-checkpatch.sh?h=refs/heads/master
SKIP_PATHS='./build-\*:./platform/\*:*/tz_\*:./lib/\*:./platform/ext/\*:./bl2/ext/\*:./docs/\*:./tools/\*'


# Find the intersection of the files changed in the commit, with the union
# of the files in the project, exclding everything in the SKIP_PATHS

# Please keep it in sync with the excluded directories the CI uses
# https://git.trustedfirmware.org/next/ci/tf-m-ci-scripts.git/tree/run-checkpatch.sh?h=refs/heads/master
FIND_CMD="find $TFM_PATH -name '*.[ch]' -a -not \( -path "${SKIP_PATHS//:/ -o -path }" \)"
CARE_LIST=$(eval $FIND_CMD | grep "$(git diff HEAD~1 --name-only)" -)

# Check that script executed from root of git repository
if [ "$(git rev-parse --show-toplevel)/" != $TFM_PATH ]
then
    echo "[SCF checkpatch] Please execute script from root of TF-M repository."
    exit 1
fi

# Only run checkpatch if there are files to check
if [ -z "$CARE_LIST" ]; then
    echo "[SCF checkpatch] Could not find any files of interest in this commit"
    exit 0
fi

# Run Checkpatch
git diff HEAD~1 -- $CARE_LIST | $CHECKPATCH_APP $CHECKPATCH_CONFG - | tee -a "$OUTPUT_FILE_PATH"

# Evaluate the result
if [ ${PIPESTATUS[1]} -eq 0 ]; then
   echo  "[SCF checkpatch: PASS] No new issues have been introduced"
   exit 0
else
   echo  "[SCF checkpatch: WARNING] Raised some Warnings/Errors"
   echo "[SCF checkpatch] Output report located at: \"$OUTPUT_FILE_PATH\""
   exit 1
fi
