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
from tests.synthetic_token_verifier import SyntheticTokenVerifier2, SyntheticTokenVerifier
from test_utils import read_iat, create_and_read_iat, convert_map_to_token_bytes, bytes_equal_to_file


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
        config = VerifierConfiguration(keep_going=True, strict=True)

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

        with self.assertLogs() as test_ctx:
            read_iat(
                DATA_DIR,
                'inverted_p_header.cbor',
                SyntheticTokenVerifier(method=method,
                    cose_alg=cose_alg,
                    signing_key=signing_key,
                    configuration=config,
                    internal_signing_key=signing_key),
                check_p_header=True)
        self.assertEquals(2, len(test_ctx.output))
        self.assertIn('Unexpected protected header', test_ctx.output[0])
        self.assertIn('Missing alg from protected header (expected ES256)', test_ctx.output[1])

        with self.assertLogs() as test_ctx:
            read_iat(
                DATA_DIR,
                'inverted_p_header2.cbor',
                SyntheticTokenVerifier2(method=method,
                    cose_alg=cose_alg,
                    signing_key=signing_key,
                    configuration=config,
                    internal_signing_key=signing_key),
                check_p_header=True)
        self.assertEquals(2, len(test_ctx.output))
        self.assertIn('Missing alg from protected header (expected ES256)', test_ctx.output[0])
        self.assertIn('Unexpected protected header', test_ctx.output[1])

    def test_tagging_support(self):
        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=AttestationTokenVerifier.COSE_ALG_ES256

        signing_key = read_keyfile(KEYFILE, method)
        config = VerifierConfiguration(keep_going=True, strict=True)

        # test with unexpected tag
        with self.assertLogs() as test_ctx:
            read_iat(
                DATA_DIR,
                'unexpected_tags.cbor',
                SyntheticTokenVerifier(method=method,
                    cose_alg=cose_alg,
                    signing_key=signing_key,
                    configuration=config,
                    internal_signing_key=signing_key))
        self.assertEquals(2, len(test_ctx.output))
        self.assertIn('Unexpected tag (0xcdcd) in token SYNTHETIC_TOKEN', test_ctx.output[0])
        self.assertIn('Unexpected tag (0xabab) in token SYNTHETIC_INTERNAL_TOKEN', test_ctx.output[1])

        # test with missing tag
        with self.assertLogs() as test_ctx:
            read_iat(
                DATA_DIR,
                'missing_tags.cbor',
                SyntheticTokenVerifier2(method=method,
                    cose_alg=cose_alg,
                    signing_key=signing_key,
                    configuration=config,
                    internal_signing_key=signing_key))
        self.assertEquals(2, len(test_ctx.output))
        self.assertIn('token SYNTHETIC_TOKEN_2 should be wrapped in tag 0xaabb', test_ctx.output[0])
        self.assertIn('token SYNTHETIC_INTERNAL_TOKEN_2 should be wrapped in tag 0xbbaa', test_ctx.output[1])

        # Test Invalid tag values
        with self.assertLogs() as test_ctx:
            read_iat(
                DATA_DIR,
                'invalid_tags.cbor',
                SyntheticTokenVerifier2(method=method,
                    cose_alg=cose_alg,
                    signing_key=signing_key,
                    configuration=config,
                    internal_signing_key=signing_key))
        self.assertEquals(2, len(test_ctx.output))
        self.assertIn('token SYNTHETIC_TOKEN_2 is wrapped in tag 0xabab instead of 0xaabb', test_ctx.output[0])
        self.assertIn('token SYNTHETIC_INTERNAL_TOKEN_2 is wrapped in tag 0xbaba instead of 0xbbaa', test_ctx.output[1])

        # Test proper tagging
        read_iat(
            DATA_DIR,
            'correct_tagging.cbor',
            SyntheticTokenVerifier2(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config,
                internal_signing_key=signing_key))

    def test_unknown_claims(self):

        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=AttestationTokenVerifier.COSE_ALG_ES256
        signing_key = read_keyfile(KEYFILE, method)
        config = VerifierConfiguration(keep_going=True, strict=False)

        test_verifier=SyntheticTokenVerifier2(method=method,
                    cose_alg=cose_alg,
                    signing_key=signing_key,
                    configuration=config,
                    internal_signing_key=signing_key)

        with self.assertLogs() as test_ctx:
            read_iat(
                DATA_DIR,
                'unknown_claims.cbor',
                test_verifier)
        self.assertEquals(4, len(test_ctx.output))
        self.assertIn('Unexpected TOKEN_ROOT_CLAIMS claim: 9901, skipping', test_ctx.output[0])
        self.assertIn('Unexpected SYN_BOXES claim: 9902, skipping', test_ctx.output[1])
        self.assertIn('Unexpected TOKEN_ROOT_CLAIMS claim: 9903, skipping', test_ctx.output[2])
        self.assertIn('Unexpected SYN_BOXES claim: 9904, skipping', test_ctx.output[3])

        config = VerifierConfiguration(keep_going=True, strict=True)

        test_verifier=SyntheticTokenVerifier2(method=method,
                    cose_alg=cose_alg,
                    signing_key=signing_key,
                    configuration=config,
                    internal_signing_key=signing_key)

        with self.assertLogs() as test_ctx:
            read_iat(
                DATA_DIR,
                'unknown_claims.cbor',
                test_verifier)
        self.assertEquals(4, len(test_ctx.output))
        self.assertIn('ERROR:iat-verifiers:Unexpected TOKEN_ROOT_CLAIMS claim: 9901', test_ctx.output[0])
        self.assertIn('ERROR:iat-verifiers:Unexpected SYN_BOXES claim: 9902', test_ctx.output[1])
        self.assertIn('ERROR:iat-verifiers:Unexpected TOKEN_ROOT_CLAIMS claim: 9903', test_ctx.output[2])
        self.assertIn('ERROR:iat-verifiers:Unexpected SYN_BOXES claim: 9904', test_ctx.output[3])

        config = VerifierConfiguration(keep_going=False, strict=False)

        test_verifier=SyntheticTokenVerifier2(method=method,
                    cose_alg=cose_alg,
                    signing_key=signing_key,
                    configuration=config,
                    internal_signing_key=signing_key)

        with self.assertLogs() as test_ctx:
            read_iat(
                DATA_DIR,
                'unknown_claims.cbor',
                test_verifier)
        self.assertIn('Unexpected TOKEN_ROOT_CLAIMS claim: 9901, skipping', test_ctx.output[0])
        self.assertIn('Unexpected SYN_BOXES claim: 9902, skipping', test_ctx.output[1])
        self.assertIn('Unexpected TOKEN_ROOT_CLAIMS claim: 9903, skipping', test_ctx.output[2])
        self.assertIn('Unexpected SYN_BOXES claim: 9904, skipping', test_ctx.output[3])

        config = VerifierConfiguration(keep_going=False, strict=True)

        test_verifier=SyntheticTokenVerifier2(method=method,
                    cose_alg=cose_alg,
                    signing_key=signing_key,
                    configuration=config,
                    internal_signing_key=signing_key)

        with self.assertRaises(ValueError) as test_ctx:
            read_iat(
                DATA_DIR,
                'unknown_claims.cbor',
                test_verifier)
        self.assertIn(
                'Unexpected TOKEN_ROOT_CLAIMS claim: 9901', test_ctx.exception.args[0])
