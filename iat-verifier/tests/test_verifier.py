# -----------------------------------------------------------------------------
# Copyright (c) 2019-2025, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

"""Unittests for iat-verifier using PSAIoTProfile1TokenVerifier"""

import os
import unittest

from pycose.algorithms import Es256, Es384

from iatverifier.psa_iot_profile1_token_verifier import PSAIoTProfile1TokenVerifier
from iatverifier.cca_token_verifier import CCATokenVerifier, CCAPlatformTokenVerifier
from iatverifier.util import read_keyfile
from iatverifier.attest_token_verifier import AttestationClaim, VerifierConfiguration
from iatverifier.attest_token_verifier import AttestationTokenVerifier
from test_utils import create_and_read_iat, read_iat, create_token_tmp_file


THIS_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(THIS_DIR, 'data')
KEYFILE = os.path.join(DATA_DIR, 'key.pem')
KEYFILE_CCA_PLAT = os.path.join(DATA_DIR, 'cca_platform.pem')
KEYFILE_CCA_REALM = os.path.join(DATA_DIR, 'cca_realm.pem')
KEYFILE_CCA_REALM2= os.path.join(DATA_DIR, 'cca_realm2.pem')
KEYFILE_ALT = os.path.join(DATA_DIR, 'key-alt.pem')

class TestIatVerifier(unittest.TestCase):
    """A class used for testing iat-verifier.

    This class uses the claim and token definitions for PSA Attestation Token"""

    def setUp(self):
        self.config = VerifierConfiguration()

    def test_validate_signature(self):
        """Testing Signature validation"""
        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=Es256

        signing_key = read_keyfile(KEYFILE, method)
        verifier_good_sig = PSAIoTProfile1TokenVerifier(
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            configuration=self.config)
        good_sig = create_token_tmp_file(DATA_DIR, 'valid-iat.yaml', verifier_good_sig)

        signing_key = read_keyfile(KEYFILE_ALT, method)
        verifier_bad_sig = PSAIoTProfile1TokenVerifier(
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            configuration=self.config)
        bad_sig = create_token_tmp_file(DATA_DIR, 'valid-iat.yaml', verifier_bad_sig)

        #dump_file_binary(good_sig)

        with open(good_sig, 'rb') as wfh:
            token_item = verifier_good_sig.parse_token(
                         token=wfh.read(),
                         lower_case_key=False)
            token_item.verify()

        with self.assertRaises(ValueError) as test_ctx:
            with open(bad_sig, 'rb') as wfh:
                token_item = verifier_good_sig.parse_token(
                    token=wfh.read(),
                    lower_case_key=False)
                token_item.verify()

        self.assertIn('Bad signature', test_ctx.exception.args[0])

    def test_validate_iat_structure(self):
        """Testing IAT structure validation"""
        keep_going_conf = VerifierConfiguration(keep_going=True)
        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=Es256
        signing_key = read_keyfile(KEYFILE, method)
        realm_token_key = read_keyfile(KEYFILE_CCA_REALM, method)
        realm_token_key2 = read_keyfile(KEYFILE_CCA_REALM2, method)
        platform_token_key = read_keyfile(KEYFILE_CCA_PLAT, method)

        create_and_read_iat(
            DATA_DIR,
            'valid-iat.yaml',
            PSAIoTProfile1TokenVerifier(
                method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))

        create_and_read_iat(
            DATA_DIR,
            'valid-cca-token.yaml',
            CCATokenVerifier(
                realm_token_method=method,
                realm_token_cose_alg=Es384,
                realm_token_key=realm_token_key,
                platform_token_method=method,
                platform_token_cose_alg=Es384,
                platform_token_key=platform_token_key,
                configuration=self.config))

        create_and_read_iat(
            DATA_DIR,
            'cca_platform_token.yaml',
            CCAPlatformTokenVerifier(
                method=method,
                cose_alg=Es384,
                signing_key=platform_token_key,
                configuration=self.config,
                necessity=AttestationClaim.MANDATORY,
                has_type_indicator=False))

        create_and_read_iat(
            DATA_DIR,
            'cca_platform_token.yaml',
            CCAPlatformTokenVerifier(
                method=method,
                cose_alg=Es384,
                signing_key=platform_token_key,
                configuration=self.config,
                necessity=AttestationClaim.MANDATORY,
                has_type_indicator=True))

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
                DATA_DIR,
                'cca-invalid-plat-challenge.yaml',
                CCATokenVerifier(
                    realm_token_method=method,
                    realm_token_cose_alg=Es384,
                    realm_token_key=realm_token_key,
                    platform_token_method=method,
                    platform_token_cose_alg=Es384,
                    platform_token_key=platform_token_key,
                    configuration=self.config))
        self.assertIn("Invalid CCA_PLATFORM_CHALLENGE byte at 16: 0x00 instead of 0xe4", test_ctx.exception.args[0])

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
                DATA_DIR,
                'valid-cca-token.yaml',
                CCATokenVerifier(
                    realm_token_method=method,
                    realm_token_cose_alg=Es384,
                    realm_token_key=realm_token_key2,
                    platform_token_method=method,
                    platform_token_cose_alg=Es384,
                    platform_token_key=platform_token_key,
                    configuration=self.config))
        self.assertIn("Realm signature doesn't match Realm Public Key claim in Realm token", test_ctx.exception.args[0])

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
            DATA_DIR,
                'invalid-profile-id.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
        self.assertIn('Invalid PROFILE_ID', test_ctx.exception.args[0])

        with self.assertRaises(ValueError) as test_ctx:
            read_iat(
                DATA_DIR,
                'malformed.cbor',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
        self.assertIn('Bad COSE', test_ctx.exception.args[0])

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
                DATA_DIR,
                'missing-claim.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
        self.assertIn('missing MANDATORY claim', test_ctx.exception.args[0])

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
                DATA_DIR,
                'submod-missing-claim.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
        self.assertIn('missing MANDATORY claim', test_ctx.exception.args[0])

        with self.assertRaises(ValueError) as test_ctx:
            create_and_read_iat(
                DATA_DIR,
                'missing-sw-comps.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
        self.assertIn('NO_MEASUREMENTS claim is not present',
                      test_ctx.exception.args[0])

        with self.assertLogs() as test_ctx:
            create_and_read_iat(
                DATA_DIR,
                'missing-signer-id.yaml',
                PSAIoTProfile1TokenVerifier(method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=self.config))
            self.assertIn('Missing RECOMMENDED claim "SIGNER_ID" from SW_COMPONENTS',
                         test_ctx.records[0].getMessage())

        with self.assertLogs() as test_ctx:
            create_and_read_iat(
                DATA_DIR,
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
                DATA_DIR,
                'invalid-hw-version.yaml',
                PSAIoTProfile1TokenVerifier(
                method=method,
                cose_alg=cose_alg,
                signing_key=signing_key,
                configuration=keep_going_conf))
            self.assertIn("Invalid HARDWARE_VERSION length; "
                            "must be 19 characters, found 10 characters",
                         test_ctx.records[0].getMessage())
            self.assertIn("Invalid character   at position 1",
                         test_ctx.records[1].getMessage())
            self.assertIn("Invalid character - at position 4",
                         test_ctx.records[2].getMessage())
            self.assertIn("Invalid character a at position 10",
                         test_ctx.records[3].getMessage())

    def test_binary_string_decoding(self):
        """Test binary_string decoding"""
        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=Es256
        signing_key = read_keyfile(KEYFILE, method)
        iat = create_and_read_iat(
            DATA_DIR,
            'valid-iat.yaml',
            PSAIoTProfile1TokenVerifier(method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            configuration=self.config)).get_token_map()
        self.assertEqual(iat['SECURITY_LIFECYCLE'], 'sl_secured_3000')

    def test_security_lifecycle_decoding(self):
        """Test security lifecycle decoding"""
        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        cose_alg=Es256
        signing_key = read_keyfile(KEYFILE, method)
        iat = create_and_read_iat(
            DATA_DIR,
            'valid-iat.yaml',
            PSAIoTProfile1TokenVerifier(method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            configuration=self.config)).get_token_map()
        self.assertEqual(iat['SECURITY_LIFECYCLE'], 'sl_secured_3000')

    def test_profiles(self):
        """
        Test that both legacy and new profiles are handled correctly.
        In particular, ensure that the different RAK encodings are accommodated,
        and that use of legacy profiles triggers a warning.
        """
        method=AttestationTokenVerifier.SIGN_METHOD_SIGN1
        realm_token_key = read_keyfile(KEYFILE_CCA_REALM, method)
        platform_token_key = read_keyfile(KEYFILE_CCA_PLAT, method)

        # change directory here to make !inc work
        os.chdir(DATA_DIR)

        create_and_read_iat(
            '.',
            'cca_example_token.yaml',
            CCATokenVerifier(
                realm_token_method=method,
                realm_token_cose_alg=Es384,
                realm_token_key=realm_token_key,
                platform_token_method=method,
                platform_token_cose_alg=Es384,
                platform_token_key=platform_token_key,
                configuration=self.config
            )
        )

        with self.assertLogs() as test_ctx:
            create_and_read_iat(
                '.',
                'cca_example_token_legacy.yaml',
                CCATokenVerifier(
                    realm_token_method=method,
                    realm_token_cose_alg=Es384,
                    realm_token_key=realm_token_key,
                    platform_token_method=method,
                    platform_token_cose_alg=Es384,
                    platform_token_key=platform_token_key,
                    configuration=self.config
                )
            )
        self.assertIn('legacy profile http://arm.com/CCA-SSD/1.0.0 is deprecated',
                      test_ctx.records[0].getMessage())
