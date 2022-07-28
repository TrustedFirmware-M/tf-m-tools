# -----------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

from iatverifier.attest_token_verifier import AttestationTokenVerifier as Verifier
from iatverifier.attest_token_verifier import AttestationClaim as Claim
from iatverifier.cca_claims import CCARealmChallengeClaim, CCARealmPersonalizationValue
from iatverifier.cca_claims import CCARealmHashAlgorithmIdClaim, CCARealmPubKeyClaim
from iatverifier.cca_claims import CCARealmExtensibleMeasurementsClaim, CCARealmInitialMeasurementClaim
from iatverifier.cca_claims import CCARealmPubKeyHashAlgorithmIdClaim, CCAPlatformHashAlgorithmIdClaim
from iatverifier.cca_claims import CCAAttestationProfileClaim, CCAPlatformChallengeClaim
from iatverifier.cca_claims import CCAPlatformImplementationIdClaim, CCAPlatformInstanceIdClaim
from iatverifier.cca_claims import CCAPlatformConfigClaim, CCAPlatformLifecycleClaim
from iatverifier.cca_claims import CCAPlatformSwComponentsClaim, CCAPlatformVerificationServiceClaim
from iatverifier.cca_claims import CCASwCompHashAlgIdClaim, CCASwCompHashAlgIdClaim
from iatverifier.psa_iot_profile1_token_claims import SWComponentTypeClaim, SwComponentVersionClaim
from iatverifier.psa_iot_profile1_token_claims import MeasurementValueClaim, SignerIdClaim

class CCATokenVerifier(Verifier):

    def get_claim_key(self=None):
        return None  # In case of root tokens the key is not used.

    def get_claim_name(self=None):
        return 'CCA_TOKEN'

    def _get_p_header(self):
        None

    def _get_wrapping_tag(self):
        return 399

    def _parse_p_header(self, msg):
        pass

    def __init__(self, *,
            realm_token_method,
            realm_token_cose_alg,
            realm_token_key,
            platform_token_method,
            platform_token_cose_alg,
            platform_token_key,
            configuration):
        verifier_claims = [
            (CCARealmTokenVerifier, {'method': realm_token_method,
                                     'cose_alg': realm_token_cose_alg,
                                     'signing_key': realm_token_key,
                                     'configuration': configuration,
                                     'necessity': Claim.MANDATORY}),
            (CCAPlatformTokenVerifier, {'method': platform_token_method,
                                        'cose_alg': platform_token_cose_alg,
                                        'signing_key': platform_token_key,
                                        'configuration': configuration,
                                        'necessity': Claim.MANDATORY}),
        ]

        # initialise the base part of the token
        super().__init__(
            claims=verifier_claims,
            configuration=configuration,
            necessity=Claim.MANDATORY,
            method=Verifier.SIGN_METHOD_RAW,
            cose_alg=Verifier.COSE_ALG_ES256,
            signing_key=None)

    @staticmethod
    def check_cross_claim_requirements(verifier, claims):
        pass


class CCARealmTokenVerifier(Verifier):
    def get_claim_key(self=None):
        return 44241

    def get_claim_name(self=None):
        return 'CCA_REALM_DELEGATED_TOKEN'

    def _get_p_header(self):
        return {'alg': self._get_cose_alg()}

    def _get_wrapping_tag(self):
        return None

    def _parse_p_header(self, msg):
        alg = self._get_cose_alg()
        try:
            msg_alg = msg.protected_header['alg']
        except KeyError:
            raise ValueError('Missing alg from protected header (expected {})'.format(alg))
        if alg != msg_alg:
            raise ValueError('Unexpected alg in protected header (expected {} instead of {})'.format(alg, msg_alg))

    def __init__(self, *, method, cose_alg, signing_key, configuration, necessity):
        verifier_claims= [
            (CCARealmChallengeClaim, {'verifier':self, 'expected_challenge_byte': None, 'necessity': Claim.MANDATORY}),
            (CCARealmPersonalizationValue, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCARealmInitialMeasurementClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCARealmExtensibleMeasurementsClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCARealmHashAlgorithmIdClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCARealmPubKeyHashAlgorithmIdClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCARealmPubKeyClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
        ]

        # initialise the base part of the token
        super().__init__(
            claims=verifier_claims,
            configuration=configuration,
            necessity=necessity,
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key)

    @staticmethod
    def check_cross_claim_requirements(verifier, claims):
        pass


class CCAPlatformTokenVerifier(Verifier):
    def get_claim_key(self=None):
        return 44234 #0xACCA

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_TOKEN'

    def _get_p_header(self):
        return {'alg': self._get_cose_alg()}

    def _get_wrapping_tag(self):
        return None

    def _parse_p_header(self, msg):
        alg = self._get_cose_alg()
        try:
            msg_alg = msg.protected_header['alg']
        except KeyError:
            raise ValueError('Missing alg from protected header (expected {})'.format(alg))
        if alg != msg_alg:
            raise ValueError('Unexpected alg in protected header (expected {} instead of {})'.format(alg, msg_alg))

    def __init__(self, *, method, cose_alg, signing_key, configuration, necessity):

        # First prepare the claim hierarchy for this token

        sw_component_claims = [
            (SWComponentTypeClaim, {'verifier':self, 'necessity': Claim.OPTIONAL}),
            (MeasurementValueClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (SwComponentVersionClaim, {'verifier':self, 'necessity': Claim.OPTIONAL}),
            (SignerIdClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCASwCompHashAlgIdClaim, {'verifier':self, 'necessity': Claim.OPTIONAL}),
        ]

        verifier_claims = [
            (CCAAttestationProfileClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCAPlatformChallengeClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCAPlatformImplementationIdClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCAPlatformInstanceIdClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCAPlatformConfigClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCAPlatformLifecycleClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCAPlatformSwComponentsClaim, {'verifier':self, 'claims': sw_component_claims, 'is_list': True, 'cross_claim_requirement_checker':None, 'necessity': Claim.MANDATORY}),
            (CCAPlatformVerificationServiceClaim, {'verifier':self, 'necessity': Claim.OPTIONAL}),
            (CCAPlatformHashAlgorithmIdClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
        ]

        # initialise the base part of the token
        super().__init__(
            claims=verifier_claims,
            configuration=configuration,
            necessity=necessity,
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key)

    @staticmethod
    def check_cross_claim_requirements(verifier, claims):
        pass

