# -----------------------------------------------------------------------------
# Copyright (c) 2022-2025, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import cbor2

from cryptography.hazmat.primitives import hashes
from pycose.headers import Algorithm
from pycose.algorithms import Es256, Es384, Es512
from pycose.keys import CoseKey

from iatverifier.attest_token_verifier import AttestationTokenVerifier as Verifier
from iatverifier.attest_token_verifier import AttestationClaim as Claim
from iatverifier.cca_claims import CCARealmChallengeClaim, CCARealmPersonalizationValue
from iatverifier.cca_claims import CCARealmProfileClaim
from iatverifier.cca_claims import CCA_REALM_PROFILE, CCA_REALM_PROFILE_LEGACY
from iatverifier.cca_claims import CCA_PLATFORM_PROFILE, CCA_PLATFORM_PROFILE_LEGACY
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
from iatverifier.util import ec2_cose_key_from_raw_ecdsa
from iatverifier.attest_token_verifier import _CBOR_MAJOR_TYPE_ARRAY

_algorithms = {
    Es256: 65,
    Es384: 97,
    Es512: 133,
}

COAP_CONTENT_INDICATOR = 263

def cca_check_type_indicator(verifier, token):
    if (isinstance(token, bytes)):
        # It can happen that the token is not a map structure, but an encoded cbor.
        # try to parse it:
        token = cbor2.loads(token)
    if not isinstance(token, list):
        msg = f'Expecting a type indicator (token must be a list)'
        verifier.error(msg)
    type_indicator_value = token[0]
    if not isinstance(type_indicator_value, int):
        msg = f'Expecting a type indicator value is not an int'
        verifier.error(msg)
    if type_indicator_value != COAP_CONTENT_INDICATOR:
        msg = f'Invalid type indicator: {type_indicator_value}'
        verifier.error(msg)
    return token[1]

def cca_encode_type_indicator(verifier, encoder):
    encoder.encode_length(_CBOR_MAJOR_TYPE_ARRAY, 2)
    encoder.encode_int(COAP_CONTENT_INDICATOR)

class CCATokenVerifier(Verifier):

    def get_claim_key(self=None):
        return None  # In case of root tokens the key is not used.

    def get_claim_name(self=None):
        return 'CCA_TOKEN'

    def _get_p_header(self):
        return {Algorithm: self._get_cose_alg()}

    def _get_wrapping_tag(self):
        return 907

    def _parse_p_header(self, msg):
        alg = self._get_cose_alg()
        try:
            msg_alg = msg.get_attr(Algorithm)
        except AttributeError:
            raise ValueError('Missing alg from protected header (expected {})'.format(alg))
        if alg != msg_alg:
            raise ValueError('Unexpected alg in protected header (expected {} instead of {})'.format(alg, msg_alg))

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
            cose_alg=Es256,
            signing_key=None)

    def _check_profiles_coherence(self, platform_profile, realm_profile):
        if platform_profile == CCA_PLATFORM_PROFILE_LEGACY:
            self.warning(f'legacy profile {platform_profile} is deprecated')
            if realm_profile != CCA_REALM_PROFILE_LEGACY:
                self.error(f'unsupported profile combination: {platform_profile}, {realm_profile}')
        elif platform_profile == CCA_PLATFORM_PROFILE:
            if realm_profile != CCA_REALM_PROFILE:
                self.error(f'unsupported profile combination: {platform_profile}, {realm_profile}')
        else:
            self.error(f'unknown profile(s): {platform_profile}, {realm_profile}')

    def verify(self, token_item):
        cca_token_root_claims_item = token_item.value
        cca_platform_token_root_claims_item = cca_token_root_claims_item.value[CCAPlatformTokenVerifier.get_claim_name()].value
        cca_realm_delegated_token_root_claims_item = cca_token_root_claims_item.value[CCARealmTokenVerifier.get_claim_name()].value

        # Extract the platform profile
        cca_platform_profile_item = cca_platform_token_root_claims_item.value[CCAAttestationProfileClaim.get_claim_name()]
        cca_platform_profile = cca_platform_profile_item.value

        # Extract the realm profile
        cca_realm_profile = CCARealmTokenVerifier.get_profile(cca_realm_delegated_token_root_claims_item)

        self._check_profiles_coherence(cca_platform_profile, cca_realm_profile)

        # Extract the realm public key
        cca_realm_public_key_item = cca_realm_delegated_token_root_claims_item.value[CCARealmPubKeyClaim.get_claim_name()]
        cca_realm_public_key = cca_realm_public_key_item.value

        # Calculate the digest
        digest = hashes.Hash(hashes.SHA256())
        digest.update(cca_realm_public_key)
        cca_realm_public_key_hash = digest.finalize()

        # Get the challenge value from the platform token
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

    def __init__(self, *, method, cose_alg, signing_key=None, configuration, necessity, has_type_indicator=True):
        verifier_claims= [
            (CCARealmChallengeClaim, {'verifier':self, 'expected_challenge_byte': None, 'necessity': Claim.MANDATORY}),
            (CCARealmPersonalizationValue, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCARealmInitialMeasurementClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCARealmExtensibleMeasurementsClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCARealmHashAlgorithmIdClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCARealmPubKeyHashAlgorithmIdClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCARealmPubKeyClaim, {'verifier':self, 'necessity': Claim.MANDATORY}),
            (CCARealmProfileClaim, {'verifier':self, 'necessity': Claim.OPTIONAL}),
        ]

        # initialise the base part of the token
        super().__init__(
            claims=verifier_claims,
            configuration=configuration,
            necessity=necessity,
            method=method,
            cose_alg=cose_alg,
            signing_key=signing_key)

        if has_type_indicator:
            self.check_type_indicator = lambda token: cca_check_type_indicator(self, token)
            self.encode_type_indicator = lambda encoder: cca_encode_type_indicator(self, encoder)

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

        alg = token_item.protected_header[Algorithm]
        if alg not in _algorithms:
            self.error(f"Unknown alg '{alg.fullname}' in realm token's protected header.")
            return

        # encoding of the RAK depends on the profile
        profile_value = self.get_profile(cca_realm_delegated_token_root_claims_item)

        try:
            token_item.claim_type.signing_key = self._get_rak_as_cose_key(
                cca_realm_public_key, alg, profile_value
            )
        except Exception as e:
            self.error(f"invalid RAK value: {e}")
            return

        # call the '_get_cose_payload' of AttestationTokenVerifier to verify the
        # signature
        try:
            token_item.claim_type._get_cose_payload(
                        token_item.token,
                        verify_signature=True)
        except ValueError:
            self.error("Realm signature doesn't match Realm Public Key claim in Realm token.")

    @staticmethod
    def get_profile(realm_token):
        try:
            return realm_token.value[CCARealmProfileClaim.get_claim_name()].value
        except KeyError:
            # if profile is not found in the realm token, assume the legacy format
            return CCA_REALM_PROFILE_LEGACY

    def _get_rak_as_cose_key(self, rak, alg, profile):
        if profile == CCA_REALM_PROFILE:
            return CoseKey.decode(rak)

        if profile == CCA_REALM_PROFILE_LEGACY:
            expected_rak_len = _algorithms[alg]
            if len(rak) != expected_rak_len:
                e = f"Invalid realm public key length (alg: '{alg.fullname}'): " \
                    f"want {expected_rak_len} got {len(rak)} bytes"
                raise ValueError(e)
            return ec2_cose_key_from_raw_ecdsa(rak, alg)

        raise ValueError(f"unknown profile {profile}")

class CCAPlatformTokenVerifier(Verifier):
    def get_claim_key(self=None):
        return 44234 #0xACCA

    def get_claim_name(self=None):
        return 'CCA_PLATFORM_TOKEN'

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

    def __init__(self, *, method, cose_alg, signing_key, configuration, necessity, has_type_indicator=True):

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

        if has_type_indicator:
            self.check_type_indicator = lambda token: cca_check_type_indicator(self, token)
            self.encode_type_indicator = lambda encoder: cca_encode_type_indicator(self, encoder)

