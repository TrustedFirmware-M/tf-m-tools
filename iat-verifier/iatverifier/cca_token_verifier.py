# -----------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

from cryptography.hazmat.primitives import hashes
from ecdsa.keys import VerifyingKey
from ecdsa.curves import NIST384p
from hashlib import sha1

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

_algorithms = {
    Verifier.COSE_ALG_ES384: NIST384p
}

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
            realm_token_key = None, # Signing key is only necessary for token compile operation
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

    def verify(self, token_item):
        # Extract the realm public key
        cca_token_root_claims_item = token_item.value
        cca_realm_delegated_token_root_claims_item = cca_token_root_claims_item.value[CCARealmTokenVerifier.get_claim_name()].value
        cca_realm_public_key_item = cca_realm_delegated_token_root_claims_item.value[CCARealmPubKeyClaim.get_claim_name()]
        cca_realm_public_key = cca_realm_public_key_item.value

        # Calculate the digest
        digest = hashes.Hash(hashes.SHA256())
        digest.update(cca_realm_public_key)
        cca_realm_public_key_hash = digest.finalize()

        # Get the challenge value from the platform token
        cca_platform_token_root_claims_item = cca_token_root_claims_item.value[CCAPlatformTokenVerifier.get_claim_name()].value
        cca_platform_challenge_item = cca_platform_token_root_claims_item.value[CCAPlatformChallengeClaim.get_claim_name()]
        cca_platform_challenge = cca_platform_challenge_item.value

        # Do the validation
        self._validate_bytestrings_equal(cca_platform_challenge, 'CCA_PLATFORM_CHALLENGE', cca_realm_public_key_hash)

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

    def __init__(self, *, method, cose_alg, signing_key=None, configuration, necessity):
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

    def verify(self, token_item):
        # Realm token was not checked against the realm public key as it needs
        # to be extracted from the realm token itself.

        # Extract the public key
        cca_realm_delegated_token_root_claims_item = token_item.value
        cca_realm_public_key_item = cca_realm_delegated_token_root_claims_item.value[CCARealmPubKeyClaim.get_claim_name()]
        cca_realm_public_key = cca_realm_public_key_item.value

        # The 'parse_token' method of the AttestationTokenVerifier adds a 'token'
        # field to the TokenItem.
        assert hasattr(token_item, "token")

        if not token_item.protected_header:
            # parsing protected header failed, there is no way to deduce the curve used.
            self.error("No protected header in realm token, failed to parse signature curve.")
            return

        alg = token_item.protected_header['alg']
        if alg not in _algorithms:
            self.error(f"Unknown alg '{alg}' in realm token's protected header.")
            return

        # Set the signing key in the parsed CCARealmTokenVerifier object
        token_item.claim_type.signing_key = VerifyingKey.from_string(
            cca_realm_public_key,
            curve=_algorithms[alg],
            hashfunc=sha1)

        # call the '_get_cose_payload' of AttestationTokenVerifier to verify the
        # signature
        try:
            token_item.claim_type._get_cose_payload(
                        token_item.token,
                        check_p_header=False, # already done in the parent's verify
                        verify_signature=True)
        except ValueError:
            self.error("Realm signature doesn't match Realm Public Key claim in Realm token.")

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
            (CCAPlatformSwComponentsClaim, {'verifier':self, 'claims': sw_component_claims, 'is_list': True, 'necessity': Claim.MANDATORY}),
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
