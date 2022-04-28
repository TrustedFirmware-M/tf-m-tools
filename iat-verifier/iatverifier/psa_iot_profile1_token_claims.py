# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import string

from iatverifier.attest_token_verifier import AttestationClaim, NonVerifiedClaim
from iatverifier.attest_token_verifier import CompositeAttestClaim

# IAT custom claims
ARM_RANGE = -75000

# SW component IDs
SW_COMPONENT_RANGE = 0

class InstanceIdClaim(AttestationClaim):
    def __init__(self, verifier, *, expected_len, necessity=AttestationClaim.MANDATORY):
        super().__init__(verifier, necessity=necessity)
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
    def get_claim_key(self=None):
        return ARM_RANGE - 3

    def get_claim_name(self=None):
        return 'IMPLEMENTATION_ID'


class HardwareVersionClaim(AttestationClaim):
    def verify(self, value):
        self._check_type('HARDWARE_VERSION', value, str)

        value_len = len(value)
        expected_len = 13
        if len(value) != expected_len:
            msg = 'Invalid HARDWARE_VERSION length; must be {} digits, found {} characters'
            self.verifier.error(msg.format(expected_len, value_len))
        for idx, character in enumerate(value):
            if character not in string.digits:
                msg = 'Invalid digit {} at position {}'
                self.verifier.error(msg.format(character, idx+1))

        self.verify_count += 1

    def get_claim_key(self=None):
        return ARM_RANGE - 5

    def get_claim_name(self=None):
        return 'HARDWARE_VERSION'

    def is_utf_8(self):
        return True


class SWComponentsClaim(CompositeAttestClaim):

    def get_claim_key(self=None):
        return ARM_RANGE - 6

    def get_claim_name(self=None):
        return 'SW_COMPONENTS'

class SWComponentTypeClaim(NonVerifiedClaim):
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 1

    def get_claim_name(self=None):
        return 'SW_COMPONENT_TYPE'

    def is_utf_8(self):
        return True


class NoMeasurementsClaim(NonVerifiedClaim):
    def get_claim_key(self=None):
        return ARM_RANGE - 7

    def get_claim_name(self=None):
        return 'NO_MEASUREMENTS'


class ClientIdClaim(AttestationClaim):
    def get_claim_key(self=None):
        return ARM_RANGE - 1

    def get_claim_name(self=None):
        return 'CLIENT_ID'

    def verify(self, value):
        self._check_type('CLIENT_ID', value, int)
        self.verify_count += 1

class SecurityLifecycleClaim(AttestationClaim):

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

    def add_value_to_dict(self, token, value):
        entry_name = self.get_claim_name()
        try:
            name_idx = (value >> SecurityLifecycleClaim.SL_SHIFT) - 1
            token[entry_name] = SecurityLifecycleClaim.SL_NAMES[name_idx]
        except IndexError:
            token[entry_name] = 'CUSTOM({})'.format(value)

    @staticmethod
    def parse_raw(raw_value):
        name_idx = SecurityLifecycleClaim.SL_NAMES.index(raw_value.upper())
        return (name_idx + 1) << SecurityLifecycleClaim.SL_SHIFT

    @staticmethod
    def get_formatted_value(value):
        return SecurityLifecycleClaim.SL_NAMES[(value >> SecurityLifecycleClaim.SL_SHIFT) - 1]


class ProfileIdClaim(AttestationClaim):
    def get_claim_key(self=None):
        return ARM_RANGE

    def get_claim_name(self=None):
        return 'PROFILE_ID'

    def verify(self, value):
        self._check_type('PROFILE_ID', value, str)
        self.verify_count += 1

    def is_utf_8(self):
        return True


class BootSeedClaim(AttestationClaim):
    def get_claim_key(self=None):
        return ARM_RANGE - 4

    def get_claim_name(self=None):
        return 'BOOT_SEED'

    def verify(self, value):
        self._validate_bytestring_length_is_at_least(value, 'BOOT_SEED', 32)
        self.verify_count += 1


class VerificationServiceClaim(NonVerifiedClaim):
    def get_claim_key(self=None):
        return ARM_RANGE - 10 # originator

    def get_claim_name(self=None):
        return 'VERIFICATION_SERVICE'

    def is_utf_8(self):
        return True


class SignerIdClaim(AttestationClaim):
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 5

    def get_claim_name(self=None):
        return 'SIGNER_ID'

    def verify(self, value):
        self._validate_bytestring_length_is_at_least(value, 'SIGNER_ID', 32)
        self.verify_count += 1


class SwComponentVersionClaim(NonVerifiedClaim):
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 4

    def get_claim_name(self=None):
        return 'SW_COMPONENT_VERSION'

    def is_utf_8(self):
        return True


class MeasurementValueClaim(AttestationClaim):
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 2

    def get_claim_name(self=None):
        return 'MEASUREMENT_VALUE'

    def verify(self, value):
        self._validate_bytestring_length_is_at_least(value, 'MEASUREMENT', 32)
        self.verify_count += 1


class MeasurementDescriptionClaim(NonVerifiedClaim):
    def get_claim_key(self=None):
        return SW_COMPONENT_RANGE + 6

    def get_claim_name(self=None):
        return 'MEASUREMENT_DESCRIPTION'

    def is_utf_8(self):
        return True
