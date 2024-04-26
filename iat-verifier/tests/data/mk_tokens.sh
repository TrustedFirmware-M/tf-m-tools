#!/bin/bash
#-------------------------------------------------------------------------------
# Copyright (c) 2024, Linaro Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------
set -eux
set -o pipefail

compile_token \
    --token-type CCA-token \
    --platform-key cca_platform.pem \
    --realm-key cca_realm.pem \
    --method sign \
    --outfile cca_example_token.cbor \
    cca_example_token.yaml

check_iat \
    -t CCA-token \
    -k cca_platform.pem \
    -m sign \
    cca_example_token.cbor

compile_token \
    --token-type CCA-plat-token \
    --platform-key cca_platform.pem \
    --method sign \
    --outfile cca_example_platform_token.cbor \
    cca_example_platform_token.yaml

check_iat \
    -t CCA-plat-token \
    -k cca_platform.pem \
    -m sign \
    cca_example_platform_token.cbor