# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import logging

import cbor2

logger = logging.getLogger('iat-verifiers')

class AttestationClaim:
    MANDATORY = 0
    RECOMMENDED = 1
    OPTIONAL = 2

    def __init__(self, verifier, necessity=MANDATORY):
        self.config = verifier.config
        self.verifier = verifier
        self.necessity = necessity
        self.verify_count = 0

    def verify(self, value):
        raise NotImplementedError

    def get_claim_key(self=None):
        raise NotImplementedError

    def get_claim_name(self=None):
        raise NotImplementedError

    def get_contained_claim_key_list(self):
        return {}

    def decode(self, value):
        if self.is_utf_8():
            try:
                return value.decode()
            except UnicodeDecodeError as e:
                msg = 'Error decodeing value for "{}": {}'
                self.verifier.error(msg.format(self.get_claim_name(), e))
                return str(value)[2:-1]
        else:  # not a UTF-8 value, i.e. a bytestring
            return value

    def add_tokens_to_dict(self, token, value):
        entry_name = self.get_claim_name()
        if isinstance(value, bytes):
            value = self.decode(value)
        token[entry_name] = value

    def claim_found(self):
        return self.verify_count>0

    def _check_type(self, name, value, expected_type):
        if not isinstance(value, expected_type):
            msg = 'Invalid {}: must be a(n) {}: found {}'
            self.verifier.error(msg.format(name, expected_type, type(value)))
            return False
        return True

    def _validate_bytestring_length_equals(self, value, name, expected_len):
        self._check_type(name, value, bytes)

        value_len = len(value)
        if value_len != expected_len:
            msg = 'Invalid {} length: must be exactly {} bytes, found {} bytes'
            self.verifier.error(msg.format(name, expected_len, value_len))

    def _validate_bytestring_length_is_at_least(self, value, name, minimal_length):
        self._check_type(name, value, bytes)

        value_len = len(value)
        if value_len < minimal_length:
            msg = 'Invalid {} length: must be at least {} bytes, found {} bytes'
            self.verifier.error(msg.format(name, minimal_length, value_len))

    @staticmethod
    def parse_raw(raw_value):
        return raw_value

    @staticmethod
    def get_formatted_value(value):
        return value

    def is_utf_8(self):
        return False

    def check_cross_claim_requirements(self):
        pass


class NonVerifiedClaim(AttestationClaim):
    def verify(self, value):
        self.verify_count += 1

    def get_claim_key(self=None):
        raise NotImplementedError

    def get_claim_name(self=None):
        raise NotImplementedError


class VerifierConfiguration:
    def __init__(self, keep_going=False, strict=False):
        self.keep_going=keep_going
        self.strict=strict

class AttestationTokenVerifier:

    all_known_claims = {}

    SIGN_METHOD_SIGN1 = "sign"
    SIGN_METHOD_MAC0 = "mac"
    SIGN_METHOD_RAW = "raw"

    COSE_ALG_ES256="ES256"
    COSE_ALG_ES384="ES384"
    COSE_ALG_ES512="ES512"
    COSE_ALG_HS256_64="HS256/64"
    COSE_ALG_HS256="HS256"
    COSE_ALG_HS384="HS384"
    COSE_ALG_HS512="HS512"

    def __init__(self, method, cose_alg, configuration=None):
        self.method = method
        self.cose_alg = cose_alg
        self.config = configuration if configuration is not None else VerifierConfiguration()
        self.claims = []

        self.seen_errors = False

    def add_claims(self, claims):
        for claim in claims:
            key = claim.get_claim_key()
            if key not in AttestationTokenVerifier.all_known_claims:
                AttestationTokenVerifier.all_known_claims[key] = claim.__class__

            AttestationTokenVerifier.all_known_claims.update(claim.get_contained_claim_key_list())
        self.claims.extend(claims)

    def check_cross_claim_requirements(self):
        pass

    def decode_and_validate_iat(self, encoded_iat):
        try:
            raw_token = cbor2.loads(encoded_iat)
        except Exception as e:
            msg = 'Invalid CBOR: {}'
            raise ValueError(msg.format(e))

        claims = {v.get_claim_key(): v for v in self.claims}

        token = {}
        while not hasattr(raw_token, 'items'):
            # TODO: token map is not a map. We are assuming that it is a tag
            raw_token = raw_token.value
        for entry in raw_token.keys():
            value = raw_token[entry]

            try:
                claim = claims[entry]
            except KeyError:
                if self.config.strict:
                    self.error('Invalid IAT claim: {}'.format(entry))
                token[entry] = value
                continue

            claim.verify(value)
            claim.add_tokens_to_dict(token, value)

        # Check claims' necessity
        for claim in claims.values():
            if not claim.claim_found():
                if claim.necessity==AttestationClaim.MANDATORY:
                    msg = 'Invalid IAT: missing MANDATORY claim "{}"'
                    self.error(msg.format(claim.get_claim_name()))
                elif claim.necessity==AttestationClaim.RECOMMENDED:
                    msg = 'Missing RECOMMENDED claim "{}"'
                    self.warning(msg.format(claim.get_claim_name()))

            claim.check_cross_claim_requirements()

        self.check_cross_claim_requirements()

        return token


    def get_wrapping_tag(self=None):
        """The value of the tag that the token is wrapped in.

        The function should return None if the token is not wrapped.
        """
        return None

    def error(self, message):
        self.seen_errors = True
        if self.config.keep_going:
            logger.error(message)
        else:
            raise ValueError(message)

    def warning(self, message):
        logger.warning(message)
