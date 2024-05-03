# -----------------------------------------------------------------------------
# Copyright (c) 2019-2024, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

"""
This module contains classes that represent claims for PSA IoT Profile1 Attestation token.
"""

import string

from iatverifier.attest_token_verifier import AttestationClaim
from iatverifier.attest_token_verifier import CompositeAttestClaim
from iatverifier.lifecycle_claim import GenericLifecycleClaim

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

    def verify(self, token_item):
        self._validate_bytestring_length_equals(token_item.value, 'INSTANCE_ID', self.expected_len)
        if token_item.value[0] != 0x01:
            msg = 'Invalid INSTANCE_ID: first byte must be 0x01, found: 0x{}'
            self.verifier.error(msg.format(token_item.value[0]))


class ChallengeClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Challenge claim"""
    HASH_SIZES = [32, 48, 64]

    def get_claim_key(self=None):
        return ARM_RANGE - 8  # nonce

    def get_claim_name(self=None):
        return 'CHALLENGE'

    def verify(self, token_item):
        self._check_type('CHALLENGE', token_item.value, bytes)

        value_len = len(token_item.value)
        if value_len not in ChallengeClaim.HASH_SIZES:
            msg = 'Invalid CHALLENGE length; must one of {}, found {} bytes'
            self.verifier.error(msg.format(ChallengeClaim.HASH_SIZES, value_len))


class ImplementationIdClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Implementation ID claim"""
    def get_claim_key(self=None):
        return ARM_RANGE - 3

    def get_claim_name(self=None):
        return 'IMPLEMENTATION_ID'


class HardwareVersionClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Hardware version claim"""
    def verify(self, token_item):
        self._check_type('HARDWARE_VERSION', token_item.value, str)

        value_len = len(token_item.value)
        expected_len = 19 # 'EAN13-Version' 13 + 1 + 5. e.g.:0604565272829-10010
        if len(token_item.value) != expected_len:
            msg = 'Invalid HARDWARE_VERSION length; must be {} characters, found {} characters'
            self.verifier.error(msg.format(expected_len, value_len))
        for idx, character in enumerate(token_item.value):
            if character not in string.digits:
                if idx != 13 or character not in '-':
                    msg = 'Invalid character {} at position {}'
                    self.verifier.error(msg.format(character, idx+1))


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

class SWComponentTypeClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Software Component Measurement Type claim"""
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 1

    def get_claim_name(self=None):
        return 'SW_COMPONENT_TYPE'

    @classmethod
    def is_utf_8(cls):
        return True


class NoMeasurementsClaim(AttestationClaim):
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

    def verify(self, token_item):
        self._check_type('CLIENT_ID', token_item.value, int)

class SecurityLifecycleClaim(GenericLifecycleClaim):
    """Class representing a PSA Attestation Token Security Lifecycle claim"""
    SL_VALUES= [
        ("SL_UNKNOWN", 0x0000, 0x00ff),
        ("SL_ASSEMBLY_AND_TEST", 0x1000, 0x10ff),
        ("SL_PSA_ROT_PROVISIONING", 0x2000, 0x20ff),
        ("SL_SECURED", 0x3000, 0x30ff),
        ("SL_NON_PSA_ROT_DEBUG", 0x4000, 0x40ff),
        ("SL_RECOVERABLE_PSA_ROT_DEBUG", 0x5000, 0x50ff),
        ("SL_DECOMMISSIONED", 0x6000, 0x60ff),
    ]

    def get_claim_key(self=None):
        return ARM_RANGE - 2

    def get_claim_name(self=None):
        return 'SECURITY_LIFECYCLE'

class ProfileIdClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Profile Definition claim"""
    def get_claim_key(self=None):
        return ARM_RANGE

    def get_claim_name(self=None):
        return 'PROFILE_ID'

    def verify(self, token_item):
        self._check_type('PROFILE_ID', token_item.value, str)

    @classmethod
    def is_utf_8(cls):
        return True


class BootSeedClaim(AttestationClaim):
    """Class representing a PSA Attestation Token Boot Seed claim"""
    def get_claim_key(self=None):
        return ARM_RANGE - 4

    def get_claim_name(self=None):
        return 'BOOT_SEED'

    def verify(self, token_item):
        self._validate_bytestring_length_is_at_least(token_item.value, 'BOOT_SEED', 32)


class VerificationServiceClaim(AttestationClaim):
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

    def verify(self, token_item):
        self._validate_bytestring_length_is_at_least(token_item.value, 'SIGNER_ID', 32)


class SwComponentVersionClaim(AttestationClaim):
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

    def verify(self, token_item):
        self._validate_bytestring_length_is_at_least(token_item.value, 'MEASUREMENT', 32)


class MeasurementDescriptionClaim(AttestationClaim):
    """Class representing PSA Attestation Token Software Component Measurement description claim"""
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 6

    def get_claim_name(self=None):
        return 'MEASUREMENT_DESCRIPTION'

    @classmethod
    def is_utf_8(cls):
        return True
