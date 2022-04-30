#-------------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

"""
This module contains a set of claims that are used for testing features not used by current
token types.
"""

from iatverifier.attest_token_verifier import AttestationClaim
from iatverifier.attest_token_verifier import CompositeAttestClaim

_SYNTHETIC_CLAIM_KEY_BASE = 0x754A0000 # Some made up number

class SynClaimInt(AttestationClaim):
    """A claim that should have an int as value."""
    def get_claim_key(self=None):
        return _SYNTHETIC_CLAIM_KEY_BASE + 0

    def get_claim_name(self=None):
        return 'SYN_CLAIM_INT'

    def verify(self, value):
        self._check_type(self.get_claim_name(), value, int)
        self.verify_count += 1

class SynBoxesClaim(CompositeAttestClaim):
    """A composite claim with a cross claim checker."""
    def __init__(self, verifier, *, claims, is_list, necessity=AttestationClaim.MANDATORY):
        super().__init__(
            verifier=verifier,
            claims=claims,
            cross_claim_requirement_checker=type(self).check_cross_claim_requirements,
            is_list=is_list,
            necessity=necessity)

    def get_claim_key(self=None):
        return _SYNTHETIC_CLAIM_KEY_BASE + 1

    def get_claim_name(self=None):
        return 'SYN_BOXES'

    @staticmethod
    def check_cross_claim_requirements(verifier, claims):
        """Checking the claims for a box.

        A box must have either all its dimensions defined, or none of them
        """
        box_size_prop_count = 0
        for c in [BoxWidthClaim, BoxHeightClaim, BoxDepthClaim]:
            if claims[c.get_claim_key()].claim_found():
                box_size_prop_count += 1

        if box_size_prop_count not in (0, 3):
            verifier.error('Invalid IAT: Box size must have all 3 dimensions')

class BoxWidthClaim(AttestationClaim):
    """A simple claim that has an int value."""
    def get_claim_key(self=None):
        return _SYNTHETIC_CLAIM_KEY_BASE + 2

    def get_claim_name(self=None):
        return 'BOX_WIDTH'

    def verify(self, value):
        self._check_type(self.get_claim_name(), value, int)
        self.verify_count += 1

class BoxHeightClaim(AttestationClaim):
    """A simple claim that has an int value."""
    def get_claim_key(self=None):
        return _SYNTHETIC_CLAIM_KEY_BASE + 3

    def get_claim_name(self=None):
        return 'BOX_HEIGHT'

    def verify(self, value):
        self._check_type(self.get_claim_name(), value, int)
        self.verify_count += 1

class BoxDepthClaim(AttestationClaim):
    """A simple claim that has an int value."""
    def get_claim_key(self=None):
        return _SYNTHETIC_CLAIM_KEY_BASE + 4

    def get_claim_name(self=None):
        return 'BOX_DEPTH'

    def verify(self, value):
        self._check_type(self.get_claim_name(), value, int)
        self.verify_count += 1

class BoxColorClaim(AttestationClaim):
    """A simple claim that has a string value."""
    def get_claim_key(self=None):
        return _SYNTHETIC_CLAIM_KEY_BASE + 5

    def get_claim_name(self=None):
        return 'BOX_COLOR'

    def verify(self, value):
        self._check_type(self.get_claim_name(), value, str)
        self.verify_count += 1

    @classmethod
    def is_utf_8(cls):
        return True
