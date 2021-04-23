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

# Copy clang-format config file to tfm root directory
if [ ! -f "$TFM_PATH/.clang-format" ]
then
    echo "[SCF ClangFormat] File .clang-format not found in tf-m directory"
    echo "[SCF ClangFormat] Copying .clang-format to tf-m directory"
    cp "$script_path/.clang-format" "$TFM_PATH"
fi

# Install clang-format if not already present
if ! command -v clang-format &> /dev/null
then
    echo "[SCF ClangFormat: ERROR] clang-format not found. Please install clang-format first."
    exit 1
else
    echo "[SCF ClangFormat] Found clang-format: $(command -v clang-format)"
fi

if [ ! -f $script_path/clang-format-diff.py ]
then
    echo "[SCF ClangFormat] File clang-format-diff.py not found. Downloading."
    # download clang-format-diff.py
    wget https://raw.githubusercontent.com/llvm/llvm-project/main/clang/tools/clang-format/clang-format-diff.py -P $script_path
    # make it executable
    chmod +x $script_path/clang-format-diff.py
fi

exit 0
