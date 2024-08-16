# -----------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

from pycose.headers import Algorithm

from iatverifier.attest_token_verifier import AttestationTokenVerifier as Verifier
from iatverifier.attest_token_verifier import AttestationClaim as Claim
from iatverifier.psa_2_0_0_token_claims import ProfileIdClaim, ClientIdClaim, SecurityLifecycleClaim
from iatverifier.psa_2_0_0_token_claims import ImplementationIdClaim, BootSeedClaim, CertificationReference
from iatverifier.psa_2_0_0_token_claims import ChallengeClaim
from iatverifier.psa_2_0_0_token_claims import InstanceIdClaim, VerificationServiceClaim, SWComponentsClaim
from iatverifier.psa_2_0_0_token_claims import SWComponentTypeClaim, SwComponentVersionClaim
from iatverifier.psa_2_0_0_token_claims import MeasurementValueClaim, MeasurementDescriptionClaim, SignerIdClaim

class PSA_2_0_0_TokenVerifier(Verifier):
    """Verifier class for PSA Attestation Token profile PSA_2_0_0"""

    def get_claim_key(self=None):
        return None  # In case of root tokens the key is not used.

    def get_claim_name(self=None):
        return 'PSA_2_0_0_TOKEN'

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

    def __init__(self, *, method, cose_alg, signing_key, configuration):

        # First prepare the claim hierarchy for this token
        sw_component_claims = [
            (SWComponentTypeClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (SwComponentVersionClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (MeasurementValueClaim, {'verifier': self, 'necessity': Claim.MANDATORY}),
            (MeasurementDescriptionClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (SignerIdClaim, {'verifier': self, 'necessity': Claim.RECOMMENDED}),
        ]

        verifier_claims = [
            (ProfileIdClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (ClientIdClaim, {'verifier': self, 'necessity': Claim.MANDATORY}),
            (SecurityLifecycleClaim, {'verifier': self, 'necessity': Claim.MANDATORY}),
            (ImplementationIdClaim, {'verifier': self, 'necessity': Claim.MANDATORY}),
            (BootSeedClaim, {'verifier': self, 'necessity': Claim.MANDATORY}),
            (CertificationReference, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (SWComponentsClaim, {'verifier': self, 'claims': sw_component_claims, 'is_list': True, 'necessity': Claim.MANDATORY}),
            (ChallengeClaim, {'verifier': self, 'necessity': Claim.MANDATORY}),
            (InstanceIdClaim, {'verifier': self, 'expected_len': 33, 'necessity': Claim.MANDATORY}),
            (VerificationServiceClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
        ]

        # initialise the base part of the token
        super().__init__(
            claims=verifier_claims,
            configuration=configuration,
            necessity=Claim.MANDATORY,
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key)

        # Set the properties of this token:
        self.signing_key_set = False # None is a valid value for signing_key
        self.signing_key = signing_key
