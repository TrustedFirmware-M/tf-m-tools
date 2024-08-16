# -----------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

"""
This module contains a set of tokens that are used for testing features not used by current
token types.
"""

from pycose.headers import Algorithm
from pycose.algorithms import Es256

from iatverifier.attest_token_verifier import AttestationTokenVerifier as Verifier
from iatverifier.attest_token_verifier import AttestationClaim as Claim
from tests.synthetic_token_claims import SynClaimInt, SynBoxesClaim, BoxWidthClaim
from tests.synthetic_token_claims import BoxHeightClaim, BoxDepthClaim, BoxColorClaim

class SyntheticTokenVerifier(Verifier):
    """A test token that may contain other tokens"""
    def get_claim_key(self=None):
        return None  # In case of root tokens the key is not used.

    def get_claim_name(self=None):
        return 'SYNTHETIC_TOKEN'

    def _get_p_header(self):
        return {Algorithm: self._get_cose_alg()}

    def _get_wrapping_tag(self):
        return None

    def _parse_p_header(self, msg):
        alg = self._get_cose_alg()
        try:
            msg_alg = msg.get_attr(Algorithm)
        except AttributeError:
            raise ValueError('Missing alg from protected header (expected {})'.format(alg))
        if alg != msg_alg:
            raise ValueError('Unexpected alg in protected header (expected {} instead of {})'.format(alg, msg_alg))

    def __init__(self, *, method, cose_alg, signing_key, configuration, internal_signing_key):
        # First prepare the claim hierarchy for this token

        # Claims for the internal token:
        internal_box_claims = [
            (BoxWidthClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxHeightClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxDepthClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxColorClaim, {'verifier': self, 'necessity': Claim.MANDATORY}),
        ]

        internal_verifier_claims = [
            (SynClaimInt, {'verifier': self, 'necessity':Claim.MANDATORY}),
            (SynBoxesClaim, {
                'verifier': self,
                'claims': internal_box_claims,
                'is_list': True,
                'necessity':Claim.MANDATORY}),
        ]

        # Claims for the 'external' token
        box_claims = [
            (BoxWidthClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxHeightClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxDepthClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxColorClaim, {'verifier': self, 'necessity': Claim.MANDATORY}),
            (SyntheticInternalTokenVerifier, {'necessity': Claim.OPTIONAL,
                                              'method': Verifier.SIGN_METHOD_SIGN1,
                                              'cose_alg': Es256,
                                              'claims': internal_verifier_claims,
                                              'configuration': configuration,
                                              'signing_key': internal_signing_key}),
        ]

        verifier_claims = [
            (SynClaimInt, {'verifier': self, 'necessity':Claim.MANDATORY}),
            (SynBoxesClaim, {
                'verifier': self,
                'claims': box_claims,
                'is_list': True,
                'necessity':Claim.MANDATORY}),
        ]

        # initialise the base part of the token
        super().__init__(
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            claims=verifier_claims,
            configuration=configuration,
            necessity=Claim.MANDATORY)

class SyntheticTokenVerifier2(Verifier):
    """Another test token that may contain other tokens"""
    def get_claim_key(self=None):
        return None  # In case of root tokens the key is not used.

    def get_claim_name(self=None):
        return 'SYNTHETIC_TOKEN_2'

    def _get_p_header(self):
        return {Algorithm: self._get_cose_alg()}

    def _parse_p_header(self, msg):
        alg = self._get_cose_alg()
        try:
            msg_alg = msg.get_attr(Algorithm)
        except AttributeError as exc:
            raise ValueError(f'Missing alg from protected header (expected {alg})') from exc
        if alg != msg_alg:
            raise ValueError('Unexpected alg in protected header ' +
                f'(expected {alg} instead of {msg_alg})')

    def _get_wrapping_tag(self):
        return 0xaabb

    def __init__(self, *, method, cose_alg, signing_key, configuration, internal_signing_key):
        # First prepare the claim hierarchy for this token

        # Claims for the internal token:
        internal_box_claims = [
            (BoxWidthClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxHeightClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxDepthClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxColorClaim, {'verifier': self, 'necessity': Claim.MANDATORY}),
        ]

        internal_verifier_claims = [
            (SynClaimInt, {'verifier': self, 'necessity':Claim.MANDATORY}),
            (SynBoxesClaim, {
                'verifier': self,
                'claims': internal_box_claims,
                'is_list': True,
                'necessity':Claim.MANDATORY}),
        ]

        # Claims for the 'external' token
        box_claims = [
            (BoxWidthClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxHeightClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxDepthClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (BoxColorClaim, {'verifier': self, 'necessity': Claim.MANDATORY}),
            (SyntheticInternalTokenVerifier2, {'necessity': Claim.OPTIONAL,
                                               'method': Verifier.SIGN_METHOD_SIGN1,
                                               'cose_alg': Es256,
                                               'claims': internal_verifier_claims,
                                               'configuration': configuration,
                                               'signing_key': internal_signing_key}),
        ]

        verifier_claims = [
            (SynClaimInt, {'verifier': self, 'necessity':Claim.MANDATORY}),
            (SynBoxesClaim, {
                'verifier': self,
                'claims': box_claims,
                'is_list': True,
                'necessity':Claim.MANDATORY}),
        ]

        # initialise the base part of the token
        super().__init__(
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            claims=verifier_claims,
            configuration=configuration,
            necessity=Claim.MANDATORY)

class SyntheticInternalTokenVerifier(Verifier):
    """A Test token that is intended to use inside another token"""

    def get_claim_key(self=None):
        return 0x54a14e12

    def get_claim_name(self=None):
        return 'SYNTHETIC_INTERNAL_TOKEN'

    def _get_p_header(self):
        return {Algorithm: self._get_cose_alg()}

    def _parse_p_header(self, msg):
        alg = self._get_cose_alg()
        try:
            msg_alg = msg.get_attr(Algorithm)
        except AttributeError as exc:
            raise ValueError(f'Missing alg from protected header (expected {alg})') from exc
        if alg != msg_alg:
            raise ValueError('Unexpected alg in protected header ' +
                f'(expected {alg} instead of {msg_alg})')


    def _get_wrapping_tag(self):
        return None

    def __init__(
            self,
            *, method,
            cose_alg,
            signing_key,
            claims,
            configuration=None,
            necessity=Claim.MANDATORY):
        super().__init__(
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            claims=claims,
            configuration=configuration,
            necessity=necessity)

class SyntheticInternalTokenVerifier2(Verifier):
    """Another Test token that is intended to use inside another token"""

    def get_claim_key(self=None):
        return 0x54a14e13

    def get_claim_name(self=None):
        return 'SYNTHETIC_INTERNAL_TOKEN_2'

    def _get_p_header(self):
        return {Algorithm: self._get_cose_alg()}

    def _parse_p_header(self, msg):
        alg = self._get_cose_alg()
        try:
            msg_alg = msg.get_attr(Algorithm)
        except AttributeError:
            raise ValueError('Missing alg from protected header (expected {})'.format(alg))
        if alg != msg_alg:
            raise ValueError('Unexpected alg in protected header (expected {} instead of {})'.format(alg, msg_alg))

    def _get_wrapping_tag(self):
        return 0xbbaa

    def __init__(
            self,
            *, method,
            cose_alg,
            signing_key,
            claims,
            configuration=None,
            necessity=Claim.MANDATORY):
        super().__init__(
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key,
            claims=claims,
            configuration=configuration,
            necessity=necessity)
