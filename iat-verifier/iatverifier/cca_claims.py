# -----------------------------------------------------------------------------
# Copyright (c) 2022-2024, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

from collections.abc import Iterable
import logging

from iatverifier.attest_token_verifier import AttestationClaim, CompositeAttestClaim
from iatverifier.lifecycle_claim import GenericLifecycleClaim

logger = logging.getLogger('iat-verifiers')

CCA_PLATFORM_PROFILE = "tag:arm.com,2023:cca_platform#1.0.0"
CCA_REALM_PROFILE = "tag:arm.com,2023:realm#1.0.0"
CCA_PLATFORM_PROFILE_LEGACY = "http://arm.com/CCA-SSD/1.0.0"
CCA_REALM_PROFILE_LEGACY = None

class CCARealmProfileClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 265

    def get_claim_name(self=None):
        return 'CCA_REALM_PROFILE'

    @classmethod
    def is_utf_8(cls):
        return True

    def verify(self, token_item):
        expected_value = CCA_REALM_PROFILE
        self._check_type(self.get_claim_name(), token_item.value, str)
        if token_item.value != expected_value:
            msg = 'Invalid Realm profile "{}": must be "{}"'
            self.verifier.error(msg.format(token_item.value, expected_value))

class CCARealmChallengeClaim(AttestationClaim):
    def __init__(self, verifier, expected_challenge_byte, necessity=AttestationClaim.MANDATORY):
        super().__init__(verifier=verifier, necessity=necessity)
        self.expected_challenge_byte = expected_challenge_byte

    def get_claim_key(self=None):
        return 10

    def get_claim_name(self=None):
        return 'CCA_REALM_CHALLENGE'

    def verify(self, token_item):
        self._validate_bytestring_length_equals(token_item.value, self.get_claim_name(), 64)
        if self.expected_challenge_byte is not None:
            for i, b in enumerate(token_item.value):
                if b != self.expected_challenge_byte:
                    print (f'Challenge = {token_item.value}')
                    msg = 'Invalid CHALLENGE byte at {:d}: 0x{:02x} instead of 0x{:02x}'
                    self.verifier.error(msg.format(i, b, self.expected_challenge_byte))
                    break


class CCARealmPersonalizationValue(AttestationClaim):
    def get_claim_key(self=None):
        return 44235

    def get_claim_name(self=None):
        return 'CCA_REALM_PERSONALIZATION_VALUE'

    def verify(self, token_item):
        self._validate_bytestring_length_equals(token_item.value, self.get_claim_name(), 64)

class CCARealmInitialMeasurementClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 44238

    def get_claim_name(self=None):
        return 'CCA_REALM_INITIAL_MEASUREMENT'

    def verify(self, token_item):
        self._check_type(self.get_claim_name(), token_item.value, bytes)

class CCARealmExtensibleMeasurementsClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 44239

    def get_claim_name(self=None):
        return 'CCA_REALM_EXTENSIBLE_MEASUREMENTS'

    def verify(self, token_item):
        min_measurement_count = 4
        max_measurement_count = 4
        if not isinstance(token_item.value, Iterable):
            msg = 'Invalid {:s}: Value must be a list.'
            self.verifier.error(msg.format(self.get_claim_name()))
        if len(token_item.value) < min_measurement_count or len(token_item.value) > max_measurement_count:
            msg = 'Invalid {:s}: Value must be a list of min {:d} elements and max {:d} elements.'
            self.verifier.error(msg.format(self.get_claim_name(), min_measurement_count,
                max_measurement_count))
        for v in token_item.value:
            self._validate_bytestring_length_one_of(v, self.get_claim_name()+f'[{str()}]', [32, 64])

class CCARealmHashAlgorithmIdClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 44236

    def get_claim_name(self=None):
        return 'CCA_REALM_HASH_ALGM_ID'

    @classmethod
    def is_utf_8(cls):
        return True

class CCARealmPubKeyHashAlgorithmIdClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 44240

    def get_claim_name(self=None):
        return 'CCA_REALM_PUB_KEY_HASH_ALGO_ID'

    @classmethod
    def is_utf_8(cls):
        return True

class CCARealmPubKeyClaim(AttestationClaim):
    # At the point of verifying this claim, it is not possible to get the
    # signing algorithm. So the realm public key length is checked in the
    # Realm Token's verify function.

    def get_claim_key(self=None):
        return 44237

    def get_claim_name(self=None):
        return 'CCA_REALM_PUB_KEY'

class CCAAttestationProfileClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 265

    def get_claim_name(self=None):
        return 'CCA_ATTESTATION_PROFILE'

    @classmethod
    def is_utf_8(cls):
        return True

    def verify(self, token_item):
        # allow legacy too when decoding
        allowed_profiles = [ CCA_PLATFORM_PROFILE, CCA_PLATFORM_PROFILE_LEGACY ]

        for allowed_profile in allowed_profiles:
            self._check_type(self.get_claim_name(), token_item.value, str)
            if token_item.value == allowed_profile:
                return

        msg = 'Invalid Platform profile "{}": must be one of "{}"'
        self.verifier.error(msg.format(token_item.value, ','.join(allowed_profiles)))

class CCAPlatformChallengeClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 10

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_CHALLENGE'

    def verify(self, token_item):
        self._validate_bytestring_length_one_of(token_item.value, self.get_claim_name(), [32, 48, 64])

class CCAPlatformImplementationIdClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 2396

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_IMPLEMENTATION_ID'

    def verify(self, token_item):
        self._validate_bytestring_length_equals(token_item.value, self.get_claim_name(), 32)

class CCAPlatformInstanceIdClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 256

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_INSTANCE_ID'

    def verify(self, token_item):
        self._validate_bytestring_length_between(token_item.value, self.get_claim_name(), 7, 33)
        if token_item.value[0] != 0x01:
            msg = 'Invalid Instance ID first byte "0x{:02x}": must be "0x01"'
            self.verifier.error(msg.format(token_item.value[0]))

class CCAPlatformConfigClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 2401

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_CONFIG'

    def verify(self, token_item):
        self._check_type(self.get_claim_name(), token_item.value, bytes)

class CCAPlatformLifecycleClaim(GenericLifecycleClaim):

    SL_VALUES= [
        ("UNKNOWN", 0x0000, 0x00ff),
        ("ASSEMBLY_AND_TEST", 0x1000, 0x10ff),
        ("CCA_PLATFORM_ROT_PROVISIONING", 0x2000, 0x20ff),
        ("SECURED", 0x3000, 0x30ff),
        ("NON_CCA_PLATFORM_ROT_DEBUG", 0x4000, 0x40ff),
        ("RECOVERABLE_CCA_PLATFORM_ROT_DEBUG", 0x5000, 0x50ff),
        ("DECOMMISSIONED", 0x6000, 0x60ff),
    ]

    def get_claim_key(self=None):
        return 2395

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_LIFECYCLE'

class CCASwCompHashAlgIdClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 6

    def get_claim_name(self=None):
        return 'CCA_SW_COMPONENT_HASH_ID'

    @classmethod
    def is_utf_8(cls):
        return True


class CCAPlatformSwComponentsClaim(CompositeAttestClaim):
    def get_claim_key(self=None):
        return 2399

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_SW_COMPONENTS'

class CCAPlatformVerificationServiceClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 2400

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_VERIFICATION_SERVICE'

    @classmethod
    def is_utf_8(cls):
        return True

class CCAPlatformHashAlgorithmIdClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 2402

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_HASH_ALGO_ID'

    @classmethod
    def is_utf_8(cls):
        return True
