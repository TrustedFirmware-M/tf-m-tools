# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

"""Unittests for iat-verifier using PSAIoTProfile1TokenVerifier"""

import os
import tempfile
import unittest

from iatverifier.psa_iot_profile1_token_verifier import PSAIoTProfile1TokenVerifier
from iatverifier.util import read_token_map, convert_map_to_token, read_keyfile
from iatverifier.attest_token_verifier import VerifierConfiguration, AttestationTokenVerifier


THIS_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(THIS_DIR, 'data')
KEYFILE = os.path.join(DATA_DIR, 'key.pem')
KEYFILE_ALT = os.path.join(DATA_DIR, 'key-alt.pem')

def create_token(source_name, verifier):
    """Create a CBOR encoded token and save it to a temp file

    Return the name of the temp file."""
    source_path = os.path.join(DATA_DIR, source_name)
    temp_file, dest_path = tempfile.mkstemp()
    os.close(temp_file)

    token_map = read_token_map(source_path)
    with open(dest_path, 'wb') as wfh:
        convert_map_to_token(
            token_map,
            verifier,
            wfh,
            add_p_header=False,
            name_as_key=True,
            parse_raw_value=True)
    return dest_path

def read_iat(filename, verifier):
    """Parse a token file"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'rb') as token_file:
        return verifier.parse_token(
            token=token_file.read(),
            verify=True,
            check_p_header=False,
            lower_case_key=False)

def create_and_read_iat(source_name, verifier):
    """Create a cbor encoded token in a temp file and parse it back"""
    token_file = create_token(source_name, verifier)
    return read_iat(token_file, verifier)

class TestIatVerifier(unittest.TestCase):
    """A class used for testing iat-verifier.

    This class uses the claim and token definitions for PSA Attestation Token"""

    def setUp(self):
        self.config = VerifierConfiguration()

    def test_validate_signature(self):
        """Testing Signature validation"""
        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=AttestationTokenVerifier.COSE_ALG_ES256

        signing_key = read_keyfile(KEYFILE, method)
        verifier_good_sig = PSAIoTProfile1TokenVerifier(
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            configuration=self.config)
        good_sig = create_token('valid-iat.yaml', verifier_good_sig)

        signing_key = read_keyfile(KEYFILE_ALT, method)
        verifier_bad_sig = PSAIoTProfile1TokenVerifier(
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            configuration=self.config)
        bad_sig = create_token('valid-iat.yaml', verifier_bad_sig)

        #dump_file_binary(good_sig)

        with open(good_sig, 'rb') as wfh:
            verifier_good_sig.parse_token(
                token=wfh.read(),
                verify=True,
                check_p_header=False,
                lower_case_key=False)


        with self.assertRaises(ValueError) as test_ctx:
            with open(bad_sig, 'rb') as wfh:
                verifier_good_sig.parse_token(
                    token=wfh.read(),
                    verify=True,
                    check_p_header=False,
                    lower_case_key=False)

        self.assertIn('Bad signature', test_ctx.exception.args[0])

    def test_validate_iat_structure(self):
        """Testing IAT structure validation"""
        keep_going_conf = VerifierConfiguration(keep_going=True)
        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=AttestationTokenVerifier.COSE_ALG_ES256
        signing_key = read_keyfile(KEYFILE, method)

        create_and_read_iat(
            'valid-iat.yaml',
            PSAIoTProfile1TokenVerifier(method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            configuration=self.config))

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
                'invalid-profile-id.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
        self.assertIn('Invalid PROFILE_ID', test_ctx.exception.args[0])

        with self.assertRaises(ValueError) as test_ctx:
            read_iat(
                'malformed.cbor',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
        self.assertIn('Bad COSE', test_ctx.exception.args[0])

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
                'missing-claim.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
        self.assertIn('missing MANDATORY claim', test_ctx.exception.args[0])

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
                'submod-missing-claim.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
        self.assertIn('missing MANDATORY claim', test_ctx.exception.args[0])

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
                'missing-sw-comps.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
        self.assertIn('NO_MEASUREMENTS claim is not present',
                      test_ctx.exception.args[0])

        with self.assertLogs() as test_ctx:
            create_and_read_iat(
                'missing-signer-id.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
            self.assertIn('Missing RECOMMENDED claim "SIGNER_ID" from SW_COMPONENTS',
                         test_ctx.records[0].getMessage())

        with self.assertLogs() as test_ctx:
            create_and_read_iat(
                'invalid-type-length.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=keep_going_conf))
            self.assertIn("Invalid PROFILE_ID: must be a(n) <class 'str'>: found <class 'int'>",
                         test_ctx.records[0].getMessage())
            self.assertIn("Invalid SIGNER_ID: must be a(n) <class 'bytes'>: found <class 'str'>",
                         test_ctx.records[1].getMessage())
            self.assertIn("Invalid SIGNER_ID length: must be at least 32 bytes, found 12 bytes",
                         test_ctx.records[2].getMessage())
            self.assertIn("Invalid MEASUREMENT length: must be at least 32 bytes, found 28 bytes",
                         test_ctx.records[3].getMessage())

        with self.assertLogs() as test_ctx:
            create_and_read_iat(
                'invalid-hw-version.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=keep_going_conf))
            self.assertIn("Invalid HARDWARE_VERSION length; must be 13 digits, found 10 characters",
                         test_ctx.records[0].getMessage())
            self.assertIn("Invalid digit   at position 1",
                         test_ctx.records[1].getMessage())
            self.assertIn("Invalid digit - at position 4",
                         test_ctx.records[2].getMessage())
            self.assertIn("Invalid digit a at position 10",
                         test_ctx.records[3].getMessage())

    def test_binary_string_decoding(self):
        """Test binary_string decoding"""
        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=AttestationTokenVerifier.COSE_ALG_ES256
        signing_key = read_keyfile(KEYFILE, method)
        iat = create_and_read_iat(
            'valid-iat.yaml',
            PSAIoTProfile1TokenVerifier(method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            configuration=self.config))
        self.assertEqual(iat['SECURITY_LIFECYCLE'], 'SL_SECURED')

    def test_security_lifecycle_decoding(self):
        """Test security lifecycle decoding"""
        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=AttestationTokenVerifier.COSE_ALG_ES256
        signing_key = read_keyfile(KEYFILE, method)
        iat = create_and_read_iat(
            'valid-iat.yaml',
            PSAIoTProfile1TokenVerifier(method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            configuration=self.config))
        self.assertEqual(iat['SECURITY_LIFECYCLE'], 'SL_SECURED')
