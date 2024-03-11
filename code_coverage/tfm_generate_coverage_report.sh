#!/bin/bash

# Copyright (c) 2024, Arm Limited. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

error()
{
    printf "\e[31m[ERR] $1\e[0m\n" 1>&2
    if test -n "$2"
    then
        exit $2
    else
        exit 1
    fi
}

usage() {
    echo "$0 --source_dir <source_dir> --build_dir <build_dir> --output_dir <output_dir> data_file [data_file ...]"
}

set -ex

SCRIPT_DIR="$( dirname "${BASH_SOURCE[0]}")"

# Parse arguments
while test $# -gt 0; do
    case $1 in
        -s|--source_dir)
        SOURCE_DIR="$2"
        shift
        shift
        ;;
        -b|--build_dir)
        BUILD_DIR="$2"
        shift
        shift
        ;;
        -b|--output_dir)
        OUTPUT_DIR="$2"
        shift
        shift
        ;;
        -h|--help)
        usage
        exit 0
        ;;
        *)
        break
        ;;
    esac
done

if test -z "$SOURCE_DIR"
then
    usage
    error "No source dir specified"
fi

if test -z "$BUILD_DIR"
then
    usage
    error "No build dir specified"
fi

if test -z "$OUTPUT_DIR"
then
    usage
    error "No output dir specified"
fi

if ! test $# -gt 0
then
    usage
    error "At least one data file must be input"
fi

info_dir=$(mktemp -d)

for x in "$@"
do
    tmpdir=$(mktemp -d)

    if ${SCRIPT_DIR}/ingest_tarmac.py \
            --input_file "$x" \
            --output_file "${tmpdir}/$(basename "$x").data"
    then
        input_file="${tmpdir}/$(basename "$x").data"
    else
        input_file="$x"
    fi


    ${SCRIPT_DIR}/generate_report_config_json.py \
        --source_dir "${SOURCE_DIR}" \
        --build_dir "${BUILD_DIR}" \
        --output_config_file "${tmpdir}/$(basename "$x")_config.json" \
        --output_intermediate_file "${tmpdir}/$(basename "$x")_intermediate.json" \
        "$input_file"

    python3 ${SCRIPT_DIR}/qa-tools/coverage-tool/coverage-reporting/intermediate_layer.py \
            --config-json "${tmpdir}/$(basename "$x")_config.json"

    python3 ${SCRIPT_DIR}/qa-tools/coverage-tool/coverage-reporting/generate_info_file.py \
            --workspace ${SOURCE_DIR} \
            --json "${tmpdir}/$(basename "$x")_intermediate.json" \
            --info ${info_dir}/${RANDOM}${RANDOM}.info
done

info_file="$(mktemp).info"

if test $(find "$info_dir" -type f | wc -l) -gt 1
then
    arguments=$(find "$info_dir" -type f | xargs -I{} echo "-a {}")

    python3 ${SCRIPT_DIR}/qa-tools/coverage-tool/coverage-reporting/merge.py \
        $arguments \
        -o ${info_file}
else
    info_file=$(find "$info_dir" -type f)
fi

genhtml --branch-coverage "${info_file}" --output-directory "$OUTPUT_DIR"
