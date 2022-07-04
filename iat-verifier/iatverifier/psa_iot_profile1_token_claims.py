# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

"""
This module contains classes that represent claims for PSA IoT Profile1 Attestation token.
"""

import string

from iatverifier.attest_token_verifier import AttestationClaim, NonVerifiedClaim
from iatverifier.attest_token_verifier import CompositeAttestClaim

# IAT custom claims
ARM_RANGE = -75000

# SW component IDs
SW_COMPONENT_RANGE = 0

class InstanceIdClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Instance ID claim"""
    def __init__(self, *, verifier, expected_len, necessity=AttestationClaim.MANDATORY):
        super().__init__(verifier=verifier, necessity=necessity)
        self.expected_len = expected_len

    def get_claim_key(self=None):
        return ARM_RANGE - 9  # UEID

    def get_claim_name(self=None):
        return 'INSTANCE_ID'

    def verify(self, value):
        self._validate_bytestring_length_equals(value, 'INSTANCE_ID', self.expected_len)
        if value[0] != 0x01:
            msg = 'Invalid INSTANCE_ID: first byte must be 0x01, found: 0x{}'
            self.verifier.error(msg.format(value[0]))
        self.verify_count += 1


class ChallengeClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Challenge claim"""
    HASH_SIZES = [32, 48, 64]

    def get_claim_key(self=None):
        return ARM_RANGE - 8  # nonce

    def get_claim_name(self=None):
        return 'CHALLENGE'

    def verify(self, value):
        self._check_type('CHALLENGE', value, bytes)

        value_len = len(value)
        if value_len not in ChallengeClaim.HASH_SIZES:
            msg = 'Invalid CHALLENGE length; must one of {}, found {} bytes'
            self.verifier.error(msg.format(ChallengeClaim.HASH_SIZES, value_len))
        self.verify_count += 1


class ImplementationIdClaim(NonVerifiedClaim):
    """Class representing a PSA Attestation Token Implementation ID claim"""
    def get_claim_key(self=None):
        return ARM_RANGE - 3

    def get_claim_name(self=None):
        return 'IMPLEMENTATION_ID'


class HardwareVersionClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Hardware version claim"""
    def verify(self, value):
        self._check_type('HARDWARE_VERSION', value, str)

        value_len = len(value)
        expected_len = 19 # 'EAN13-Version' 13 + 1 + 5. e.g.:0604565272829-10010
        if len(value) != expected_len:
            msg = 'Invalid HARDWARE_VERSION length; must be {} characters, found {} characters'
            self.verifier.error(msg.format(expected_len, value_len))
        for idx, character in enumerate(value):
            if character not in string.digits:
                if idx != 13 or character not in '-':
                    msg = 'Invalid character {} at position {}'
                    self.verifier.error(msg.format(character, idx+1))

        self.verify_count += 1

    def get_claim_key(self=None):
        return ARM_RANGE - 5

    def get_claim_name(self=None):
        return 'HARDWARE_VERSION'

    @classmethod
    def is_utf_8(cls):
        return True


class SWComponentsClaim(CompositeAttestClaim):
    """Class representing a PSA Attestation Token Software Components claim"""
    def get_claim_key(self=None):
        return ARM_RANGE - 6

    def get_claim_name(self=None):
        return 'SW_COMPONENTS'

class SWComponentTypeClaim(NonVerifiedClaim):
    """Class representing a PSA Attestation Token Software Component Measurement Type claim"""
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 1

    def get_claim_name(self=None):
        return 'SW_COMPONENT_TYPE'

    @classmethod
    def is_utf_8(cls):
        return True


class NoMeasurementsClaim(NonVerifiedClaim):
    """Class representing a PSA Attestation Token No Software Measurements claim"""
    def get_claim_key(self=None):
        return ARM_RANGE - 7

    def get_claim_name(self=None):
        return 'NO_MEASUREMENTS'


class ClientIdClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Client ID claim"""
    def get_claim_key(self=None):
        return ARM_RANGE - 1

    def get_claim_name(self=None):
        return 'CLIENT_ID'

    def verify(self, value):
        self._check_type('CLIENT_ID', value, int)
        self.verify_count += 1

class SecurityLifecycleClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Security Lifecycle claim"""
    SL_SHIFT = 12

    SL_NAMES = [
        'SL_UNKNOWN',
        'SL_PSA_ROT_PROVISIONING',
        'SL_SECURED',
        'SL_NON_PSA_ROT_DEBUG',
        'SL_RECOVERABLE_PSA_ROT_DEBUG',
        'SL_PSA_LIFECYCLE_DECOMMISSIONED',
    ]

    # Security Lifecycle claims
    SL_UNKNOWN = 0x1000
    SL_PSA_ROT_PROVISIONING = 0x2000
    SL_SECURED = 0x3000
    SL_NON_PSA_ROT_DEBUG = 0x4000
    SL_RECOVERABLE_PSA_ROT_DEBUG = 0x5000
    SL_PSA_LIFECYCLE_DECOMMISSIONED = 0x6000

    def get_claim_key(self=None):
        return ARM_RANGE - 2

    def get_claim_name(self=None):
        return 'SECURITY_LIFECYCLE'

    def verify(self, value):
        self._check_type('SECURITY_LIFECYCLE', value, int)
        self.verify_count += 1

    @classmethod
    def parse_raw(cls, raw_value):
        name_idx = cls.SL_NAMES.index(raw_value.upper())
        return (name_idx + 1) << cls.SL_SHIFT

    @classmethod
    def get_formatted_value(cls, value):
        return cls.SL_NAMES[(value >> cls.SL_SHIFT) - 1]


class ProfileIdClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Profile Definition claim"""
    def get_claim_key(self=None):
        return ARM_RANGE

    def get_claim_name(self=None):
        return 'PROFILE_ID'

    def verify(self, value):
        self._check_type('PROFILE_ID', value, str)
        self.verify_count += 1

    @classmethod
    def is_utf_8(cls):
        return True


class BootSeedClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Boot Seed claim"""
    def get_claim_key(self=None):
        return ARM_RANGE - 4

    def get_claim_name(self=None):
        return 'BOOT_SEED'

    def verify(self, value):
        self._validate_bytestring_length_is_at_least(value, 'BOOT_SEED', 32)
        self.verify_count += 1


class VerificationServiceClaim(NonVerifiedClaim):
    """Class representing a PSA Attestation Token Verification Service Indicator claim"""
    def get_claim_key(self=None):
        return ARM_RANGE - 10 # originator

    def get_claim_name(self=None):
        return 'VERIFICATION_SERVICE'

    @classmethod
    def is_utf_8(cls):
        return True


class SignerIdClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Software Component Signer ID claim"""
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 5

    def get_claim_name(self=None):
        return 'SIGNER_ID'

    def verify(self, value):
        self._validate_bytestring_length_is_at_least(value, 'SIGNER_ID', 32)
        self.verify_count += 1


class SwComponentVersionClaim(NonVerifiedClaim):
    """Class representing a PSA Attestation Token Software Component Version claim"""
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 4

    def get_claim_name(self=None):
        return 'SW_COMPONENT_VERSION'

    @classmethod
    def is_utf_8(cls):
        return True


class MeasurementValueClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Software Component Measurement value claim"""
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 2

    def get_claim_name(self=None):
        return 'MEASUREMENT_VALUE'

    def verify(self, value):
        self._validate_bytestring_length_is_at_least(value, 'MEASUREMENT', 32)
        self.verify_count += 1


class MeasurementDescriptionClaim(NonVerifiedClaim):
    """Class representing PSA Attestation Token Software Component Measurement description claim"""
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 6

    def get_claim_name(self=None):
        return 'MEASUREMENT_DESCRIPTION'

    @classmethod
    def is_utf_8(cls):
        return True
