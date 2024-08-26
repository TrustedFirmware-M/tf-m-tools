#!/bin/bash
#-------------------------------------------------------------------------------
# Copyright (c) 2024, Linaro Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------
set -eux
set -o pipefail

k=cca_platform.pem

for t in cca_example_platform_token cca_example_platform_token_legacy; do

    compile_token \
        --token-type CCA-plat-token \
        --platform-key $k \
        --method sign \
        --outfile $t.cbor \
        $t.yaml

    check_iat \
        -t CCA-plat-token \
        -k $k \
        -m sign \
        $t.cbor

done

for t in cca_example_token cca_example_token_legacy; do

    compile_token \
        --token-type CCA-token \
        --platform-key cca_platform.pem \
        --realm-key cca_realm.pem \
        --method sign \
        --outfile $t.cbor \
        $t.yaml

    check_iat \
        -t CCA-token \
        -k $k \
        -m sign \
        $t.cbor

done
