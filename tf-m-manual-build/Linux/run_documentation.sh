#!/bin/bash
#------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#------------------------------------------------------------------------------

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

set -a && source $SCRIPT_DIR/../config/Linux/container_cfg

command="cmake -S . -B $DOCS_DIR -DTFM_PLATFORM=$PLATFORM -DTFM_TOOLCHAIN_FILE=toolchain_GNUARM.cmake && cmake --build $DOCS_DIR -- tfm_docs_userguide_html "

docker run -it --rm --user $(id -u):$(id -g) -v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro -v /etc/shadow:/etc/shadow:ro -v $LOCAL_TFM_REPO:/opt/trusted-firmware-m $DOCS_IMG_NAME "$command"