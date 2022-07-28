# -----------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

from collections.abc import Iterable
import logging

from iatverifier.attest_token_verifier import AttestationClaim, NonVerifiedClaim, CompositeAttestClaim

logger = logging.getLogger('iat-verifiers')

class CCARealmChallengeClaim(AttestationClaim):
    def __init__(self, verifier, expected_challenge_byte, necessity=AttestationClaim.MANDATORY):
        super().__init__(verifier=verifier, necessity=necessity)
        self.expected_challenge_byte = expected_challenge_byte

    def get_claim_key(self=None):
        return 10

    def get_claim_name(self=None):
        return 'CCA_REALM_CHALLENGE'

    def verify(self, value):
        self._validate_bytestring_length_equals(value, self.get_claim_name(), 64)
        if self.expected_challenge_byte is not None:
            for i, b in enumerate(value):
                if b != self.expected_challenge_byte:
                    print (f'Challenge = {value}')
                    msg = 'Invalid CHALLENGE byte at {:d}: 0x{:02x} instead of 0x{:02x}'
                    self.verifier.error(msg.format(i, b, self.expected_challenge_byte))
                    break
        self.verify_count += 1

class CCARealmPersonalizationValue(AttestationClaim):
    def get_claim_key(self=None):
        return 44235

    def get_claim_name(self=None):
        return 'CCA_REALM_PERSONALIZATION_VALUE'

    def verify(self, value):
        self._validate_bytestring_length_equals(value, self.get_claim_name(), 64)
        self.verify_count += 1

class CCARealmInitialMeasurementClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 44238

    def get_claim_name(self=None):
        return 'CCA_REALM_INITIAL_MEASUREMENT'

    def verify(self, value):
        self._check_type(self.get_claim_name(), value, bytes)
        self.verify_count += 1

class CCARealmExtensibleMeasurementsClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 44239

    def get_claim_name(self=None):
        return 'CCA_REALM_EXTENSIBLE_MEASUREMENTS'

    def verify(self, value):
        min_measurement_count = 4
        max_measurement_count = 4
        if not isinstance(value, Iterable):
            msg = 'Invalid {:s}: Value must be a list.'
            self.verifier.error(msg.format(self.get_claim_name()))
        if len(value) < min_measurement_count or len(value) > max_measurement_count:
            msg = 'Invalid {:s}: Value must be a list of min {:d} elements and max {:d} elements.'
            self.verifier.error(msg.format(self.get_claim_name(), min_measurement_count,
                max_measurement_count))
        for v in value:
            self._validate_bytestring_length_one_of(v, self.get_claim_name()+f'[{str()}]', [32, 64])
        self.verify_count += 1

class CCARealmHashAlgorithmIdClaim(NonVerifiedClaim):
    def get_claim_key(self=None):
        return 44236

    def get_claim_name(self=None):
        return 'CCA_REALM_HASH_ALGM_ID'

    @classmethod
    def is_utf_8(cls):
        return True

class CCARealmPubKeyHashAlgorithmIdClaim(NonVerifiedClaim):
    def get_claim_key(self=None):
        return 44240

    def get_claim_name(self=None):
        return 'CCA_REALM_PUB_KEY_HASH_ALGO_ID'

    @classmethod
    def is_utf_8(cls):
        return True

class CCARealmPubKeyClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 44237

    def get_claim_name(self=None):
        return 'CCA_REALM_PUB_KEY'

    def verify(self, value):
        self._validate_bytestring_length_equals(value, self.get_claim_name(), 97)
        self.verify_count += 1

class CCAAttestationProfileClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 265

    def get_claim_name(self=None):
        return 'CCA_ATTESTATION_PROFILE'

    @classmethod
    def is_utf_8(cls):
        return True

    def verify(self, value):
        expected_value = "http://arm.com/CCA-SSD/1.0.0"
        self._check_type(self.get_claim_name(), value, str)
        if value != expected_value:
            msg = 'Invalid Attest profile "{}": must be "{}"'
            self.verifier.error(msg.format(value, expected_value))
        self.verify_count += 1

class CCAPlatformChallengeClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 10

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_CHALLENGE'

    def verify(self, value):
        self._validate_bytestring_length_one_of(value, self.get_claim_name(), [32, 48, 64])
        self.verify_count += 1

class CCAPlatformImplementationIdClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 2396

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_IMPLEMENTATION_ID'

    def verify(self, value):
        self._validate_bytestring_length_equals(value, self.get_claim_name(), 32)
        self.verify_count += 1

class CCAPlatformInstanceIdClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 256

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_INSTANCE_ID'

    def verify(self, value):
        self._validate_bytestring_length_between(value, self.get_claim_name(), 7, 33)
        if value[0] != 0x01:
            msg = 'Invalid Instance ID first byte "0x{:02x}": must be "0x01"'
            self.verifier.error(msg.format(value[0]))
        self.verify_count += 1

class CCAPlatformConfigClaim(AttestationClaim):
    def get_claim_key(self=None):
        return 2401

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_CONFIG'

    def verify(self, value):
        self._check_type(self.get_claim_name(), value, bytes)
        self.verify_count += 1

class CCAPlatformLifecycleClaim(AttestationClaim):

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

    @classmethod
    def parse_raw(cls, raw_value):
        try:
            int_value = int(raw_value, 16)
        except ValueError:
            # It is not a hex number. Try to decode known text values
            pass
        for text, min, max in cls.SL_VALUES:
            if raw_value.startswith(text.lower()):
                raw_value = raw_value[len(text):]
            else:
                continue
            if len(raw_value) == 0:
                return min
            assert raw_value.startswith("_0x")
            raw_value = raw_value[3:]
            int_value = int(raw_value, 16)
            assert(min <= int_value <= max)
            return int_value
        assert False

    @classmethod
    def get_formatted_value(cls, value):
        for text, min, max in cls.SL_VALUES:
            if min <= value <= max:
                return f"{text}_{value:04x}".lower()
        return f"INVALID_{value:04x}"

    def verify(self, value):
        self._check_type(self.get_claim_name, value, int)
        value_valid = False
        for _, min, max in CCAPlatformLifecycleClaim.SL_VALUES:
            if min <= value <= max:
                value_valid = True
                break
        if not value_valid:
            msg = 'Invalid Platform Lifecycle claim "0x{:02x}"'
            self.verifier.error(msg.format(value))
        self.verify_count += 1

class CCASwCompHashAlgIdClaim(NonVerifiedClaim):
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

class CCAPlatformVerificationServiceClaim(NonVerifiedClaim):
    def get_claim_key(self=None):
        return 2400

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_VERIFICATION_SERVICE'

    @classmethod
    def is_utf_8(cls):
        return True

class CCAPlatformHashAlgorithmIdClaim(NonVerifiedClaim):
    def get_claim_key(self=None):
        return 2402

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_HASH_ALGO_ID'

    @classmethod
    def is_utf_8(cls):
        return True