#!/bin/bash
#------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#------------------------------------------------------------------------------

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo $SCRIPT_DIR
set -a && source $SCRIPT_DIR/../config/Linux/container_cfg

usage() { echo "Usage: $0 [-i <gnu|armclang|docs|all>]" 1>&2; exit 1; }

eula_accept() {
    while true; do
        read -p "To build this armclang docker image, the arm compiler will be used (https://developer.arm.com/tools-and-software/embedded/arm-compiler/downloads/version-6). Do you confirm that you have read and understood the contained EULA and that you agree to it ? (Y/[N])" yn
        case $yn in
            [Yy]* ) break;;
            [Nn]* ) exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

while getopts ":i:" o; do
    case "${o}" in
        i)
            image=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
if [ "$image" = "gnu" ];
then
    docker build -t $CORE_IMG_NAME     --build-arg build_dir=$BUILD_DIR -f $SCRIPT_DIR/../source/TFM_core/Dockerfile  $SCRIPT_DIR/../config/
elif [ "$image" = "docs" ];
then
    docker build -t $CORE_IMG_NAME     --build-arg build_dir=$BUILD_DIR -f $SCRIPT_DIR/../source/TFM_core/Dockerfile  $SCRIPT_DIR/../config/
    docker build -t $DOCS_IMG_NAME     --build-arg docs_dir=$DOCS_DIR -f $SCRIPT_DIR/../source/doc/Dockerfile       $SCRIPT_DIR/../config/
elif [ "$image" = "armclang" ];
then
    eula_accept
    docker build -t $CORE_IMG_NAME     --build-arg build_dir=$BUILD_DIR -f $SCRIPT_DIR/../source/TFM_core/Dockerfile  $SCRIPT_DIR/../config/
    docker build -t $ARMCLANG_IMG_NAME --build-arg license=$ARMLMD_LICENSE_FILE --build-arg build_dir=$BUILD_DIR -f $SCRIPT_DIR../source/TFM_CLANG/Dockerfile $SCRIPT_DIR/../config/
elif [ "$image" = "all" ];
then
    # eula_accept
    docker build -t $CORE_IMG_NAME     --build-arg build_dir=$BUILD_DIR -f $SCRIPT_DIR/../source/TFM_core/Dockerfile  $SCRIPT_DIR/../config/
    docker build -t $ARMCLANG_IMG_NAME --build-arg license=$ARMLMD_LICENSE_FILE --build-arg build_dir=$BUILD_DIR -f $SCRIPT_DIR/../source/TFM_CLANG/Dockerfile $SCRIPT_DIR/../config/
    docker build -t $DOCS_IMG_NAME     --build-arg docs_dir=$DOCS_DIR -f $SCRIPT_DIR/../source/doc/Dockerfile       $SCRIPT_DIR/../config/
fi
