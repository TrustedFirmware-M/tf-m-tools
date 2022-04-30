#-------------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

"""
This test is used to test features that are not used by the PSA IoT profile1
tokens
"""

import os
import unittest

from iatverifier.util import read_token_map, read_keyfile
from iatverifier.attest_token_verifier import VerifierConfiguration, AttestationTokenVerifier
from tests.synthetic_token_verifier import SyntheticTokenVerifier
from test_utils import create_and_read_iat, convert_map_to_token_bytes, bytes_equal_to_file


THIS_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(THIS_DIR, 'synthetic_data')
KEY_DIR = os.path.join(THIS_DIR, 'data')
KEYFILE = os.path.join(KEY_DIR, 'key.pem')
KEYFILE_ALT = os.path.join(KEY_DIR, 'key-alt.pem')

class TestSynthetic(unittest.TestCase):
    """Test iat-verifier's nested IAT feature"""
    def setUp(self):
        self.config = VerifierConfiguration()

    def test_composite(self):
        """Test cross claim checking in composite claim"""
        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=AttestationTokenVerifier.COSE_ALG_ES256
        signing_key = read_keyfile(KEYFILE, method)

        create_and_read_iat(
            DATA_DIR,
            'synthetic_token.yaml',
            SyntheticTokenVerifier(
                method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config,
                internal_signing_key=signing_key))

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
                DATA_DIR,
                'synthetic_token_missing_box_dim.yaml',
                SyntheticTokenVerifier(
                    method=method,
                    cose_alg=cose_alg,
                    signing_key=signing_key,
                    configuration=self.config,
                    internal_signing_key=signing_key))
            self.assertIn(
                'Invalid IAT: Box size must have all 3 dimensions', test_ctx.exception.args[0])

        create_and_read_iat(
            DATA_DIR,
            'synthetic_token_another_token.yaml',
            SyntheticTokenVerifier(
                method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config,
                internal_signing_key=signing_key))

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
                DATA_DIR,
                'synthetic_token_another_token_missing_box_dim.yaml',
                SyntheticTokenVerifier(method=method,
                    cose_alg=cose_alg,
                    signing_key=signing_key,
                    configuration=self.config,
                    internal_signing_key=signing_key))
            self.assertIn(
                'Invalid IAT: Box size must have all 3 dimensions', test_ctx.exception.args[0])

    def test_protected_header(self):
        """Test protected header detection"""
        source_path = os.path.join(DATA_DIR, 'synthetic_token_another_token.yaml')
        token_map = read_token_map(source_path)

        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=AttestationTokenVerifier.COSE_ALG_ES256
        signing_key = read_keyfile(KEYFILE, method)

        verifier = SyntheticTokenVerifier(
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            configuration=self.config,
            internal_signing_key=signing_key)

        token_p_header = convert_map_to_token_bytes(token_map, verifier, add_p_header=True)
        token_no_p_header = convert_map_to_token_bytes(token_map, verifier, add_p_header=False)

        self.assertTrue(
            bytes_equal_to_file(token_p_header, os.path.join(DATA_DIR, 'p_header_on.cbor')))
        self.assertTrue(
            bytes_equal_to_file(token_no_p_header, os.path.join(DATA_DIR, 'p_header_off.cbor')))
