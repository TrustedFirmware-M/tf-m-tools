# -----------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

"""Contains class for verifying PSA Attestation Token profile PSA_IOT_PROFILE_1"""

from pycose.headers import Algorithm

from iatverifier.attest_token_verifier import AttestationTokenVerifier as Verifier
from iatverifier.attest_token_verifier import AttestationClaim as Claim
from iatverifier.psa_iot_profile1_token_claims import ProfileIdClaim, ClientIdClaim
from iatverifier.psa_iot_profile1_token_claims import SecurityLifecycleClaim, ImplementationIdClaim
from iatverifier.psa_iot_profile1_token_claims import BootSeedClaim, HardwareVersionClaim
from iatverifier.psa_iot_profile1_token_claims import NoMeasurementsClaim, ChallengeClaim
from iatverifier.psa_iot_profile1_token_claims import InstanceIdClaim, VerificationServiceClaim
from iatverifier.psa_iot_profile1_token_claims import SWComponentsClaim, SWComponentTypeClaim
from iatverifier.psa_iot_profile1_token_claims import SwComponentVersionClaim, MeasurementValueClaim
from iatverifier.psa_iot_profile1_token_claims import MeasurementDescriptionClaim, SignerIdClaim

class PSAIoTProfile1TokenVerifier(Verifier):
    """Verifier class for PSA Attestation Token profile PSA_IOT_PROFILE_1"""

    def get_claim_key(self=None):
        return None  # In case of root tokens the key is not used.

    def get_claim_name(self=None):
        return 'PSA_IOT_PROFILE1_TOKEN'

    def _get_p_header(self):
        return {Algorithm: self._get_cose_alg()}

    def _get_wrapping_tag(self):
        return None

    def _parse_p_header(self, msg):
        alg = self._get_cose_alg()
        try:
            msg_alg = msg.get_attr(Algorithm)
        except AttributeError as exc:
            raise ValueError(f'Missing algorithm from protected header (expected {alg})') from exc
        if alg != msg_alg:
            raise ValueError(f'Unexpected algorithm in protected header (expected {alg} ' +
                f'instead of {msg_alg})')

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
            (HardwareVersionClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
            (SWComponentsClaim, {
                'verifier': self,
                'claims': sw_component_claims,
                'is_list': True,
                'necessity': Claim.OPTIONAL}),
            (NoMeasurementsClaim, {'verifier': self, 'necessity': Claim.OPTIONAL}),
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

    def verify(self, token_item):

        root_claims_token_item = token_item.value
        root_claims_dict = root_claims_token_item.value

        assert(isinstance(root_claims_dict, dict))

        sw_component_present = False
        no_measurement_present = False
        for claim_token_item in root_claims_dict.values():
            if (isinstance(claim_token_item.claim_type, SWComponentsClaim)):
                sw_component_present = True
            if (isinstance(claim_token_item.claim_type, NoMeasurementsClaim)):
                no_measurement_present = True

        if not sw_component_present and not no_measurement_present:
            self.error('Invalid IAT: no software measurements defined and '
                  'NO_MEASUREMENTS claim is not present.')