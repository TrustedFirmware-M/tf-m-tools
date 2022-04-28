# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import logging
from abc import ABC, abstractmethod

import cbor2

logger = logging.getLogger('iat-verifiers')

class AttestationClaim(ABC):
    """
    This class represents a claim.

    This class is abstract. A concrete claim have to be derived from this class,
    and it have to implement all the abstract methods.

    This class contains methods that are not abstract. These are here as a
    default behavior, that a derived class might either keep, or override.

    A token is built up as a hierarchy of claim classes. Although it is
    important, that claim objects don't have a 'value' field. The actual parsed
    token is stored in a map structure. It is possible to execute operations
    on a token map, and the operations are defined by claim classes/objects.
    Such operations are for example verifying a token.
    """

    MANDATORY = 0
    RECOMMENDED = 1
    OPTIONAL = 2

    def __init__(self, verifier, *, necessity=MANDATORY):
        self.config = verifier.config
        self.verifier = verifier
        self.necessity = necessity
        self.verify_count = 0

    # Abstract methods

    @abstractmethod
    def verify(self, value):
        """Verify this claim

        Throw an exception if the claim is not valid"""
        raise NotImplementedError

    @abstractmethod
    def get_claim_key(self=None):
        """Get the key of this claim

        Returns the key of this claim. The implementation have to support
        calling this method with or without an instance as well."""
        raise NotImplementedError

    @abstractmethod
    def get_claim_name(self=None):
        """Get the name of this claim

        Returns the name of this claim. The implementation have to support
        calling this method with or without an instance as well."""
        raise NotImplementedError

    # Default methods that a derived class might override

    def get_contained_claim_key_list(self):
        """Return a dictionary of the claims that can be present in this claim

        Return a dictionary where keys are the claim keys (the same that is
        returned by get_claim_key), and the values are the claim classes for
        that key.
        """
        return {}

    def decode(self, value):
        """
        Decode the value of the claim if the value is an UTF-8 string
        """
        if self.is_utf_8():
            try:
                return value.decode()
            except UnicodeDecodeError as e:
                msg = 'Error decodeing value for "{}": {}'
                self.verifier.error(msg.format(self.get_claim_name(), e))
                return str(value)[2:-1]
        else:  # not a UTF-8 value, i.e. a bytestring
            return value

    def add_value_to_dict(self, token, value):
        """Add 'value' to the dict 'token'"""
        entry_name = self.get_claim_name()
        if isinstance(value, bytes):
            value = self.decode(value)
        token[entry_name] = value

    def claim_found(self):
        """Return true if verify was called on tis claim instance"""
        return self.verify_count>0

    def _check_type(self, name, value, expected_type):
        """Check that a value's type is as expected"""
        if not isinstance(value, expected_type):
            msg = 'Invalid {}: must be a(n) {}: found {}'
            self.verifier.error(msg.format(name, expected_type, type(value)))
            return False
        return True

    def _validate_bytestring_length_equals(self, value, name, expected_len):
        """Check that a bytestreams length is as expected"""
        self._check_type(name, value, bytes)

        value_len = len(value)
        if value_len != expected_len:
            msg = 'Invalid {} length: must be exactly {} bytes, found {} bytes'
            self.verifier.error(msg.format(name, expected_len, value_len))

    def _validate_bytestring_length_is_at_least(self, value, name, minimal_length):
        """Check that a bytestream has a minimum length"""
        self._check_type(name, value, bytes)

        value_len = len(value)
        if value_len < minimal_length:
            msg = 'Invalid {} length: must be at least {} bytes, found {} bytes'
            self.verifier.error(msg.format(name, minimal_length, value_len))

    @staticmethod
    def parse_raw(raw_value):
        """Parse a raw value

        As it appears in a yaml file
        """
        return raw_value

    @staticmethod
    def get_formatted_value(value):
        """Format the value according to this claim"""
        return value

    def is_utf_8(self):
        """Returns whether the value of this claim should be UTF-8"""
        return False

    def check_cross_claim_requirements(self):
        """Check whether the claims inside this claim satisfy requirements"""


class NonVerifiedClaim(AttestationClaim):
    def verify(self, value):
        self.verify_count += 1

class CompositeAttestClaim(AttestationClaim):
    """
    This class represents composite claim.

    This class is still abstract, but can contain other claims. This means that
    a value representing this claim is a dictionary. This claim contains further
    claims which represent the possible key-value pairs in the value for this
    claim.
    """

    def __init__(self, verifier, *, claims, is_list, necessity=AttestationClaim.MANDATORY):
        """ Initialise a composite claim.

        In case 'is_list' is False, the expected type of value is a dictionary,
        containing the necessary claims determined by the 'claims' list.
        In case 'is_list' is True, the expected type of value is a list,
        containing a number of dictionaries, each one containing the necessary
        claims determined by the 'claims' list.
        """
        super().__init__(verifier, necessity=necessity)
        self.is_list = is_list
        self.claims = claims

    def _get_contained_claims(self):
        return [claim(self.verifier, **args) for claim, args in self.claims]

    def get_contained_claim_key_list(self):
        ret = {}
        for claim in self._get_contained_claims():
            ret[claim.get_claim_key()] = claim.__class__
        return ret

    def _verify_dict(self, entry_number, value):
        if not self._check_type(self.get_claim_name(), value, dict):
            return

        claims = {v.get_claim_key(): v for v in self._get_contained_claims()}
        for k, v in value.items():
            if k not in claims.keys():
                if self.config.strict:
                    msg = 'Unexpected {} claim: {}'
                    self.verifier.error(msg.format(self.get_claim_name(), k))
                else:
                    continue
            try:
                claims[k].verify(v)
            except Exception:
                if not self.config.keep_going:
                    raise

        # Check claims' necessity
        for claim in claims.values():
            if not claim.claim_found():
                if claim.necessity==AttestationClaim.MANDATORY:
                    msg = ('Invalid IAT: missing MANDATORY claim "{}" '
                        'from {}').format(claim.get_claim_name(),
                                    self.get_claim_name())
                    if entry_number is not None:
                        msg += ' at index {}'.format(entry_number)
                    self.verifier.error(msg)
                elif claim.necessity==AttestationClaim.RECOMMENDED:
                    msg = ('Missing RECOMMENDED claim "{}" '
                        'from {}').format(claim.get_claim_name(),
                                    self.get_claim_name())
                    if entry_number is not None:
                        msg += ' at index {}'.format(entry_number)
                    self.verifier.warning(msg)

    def verify(self, value):
        """
        Verify a composite claim.
        """
        if self.is_list:
            if not self._check_type(self.get_claim_name(), value, list):
                return

            for entry_number, entry in enumerate(value):
                self._verify_dict(entry_number, entry)
        else:
            self._verify_dict(None, value)

        self.verify_count += 1

    def _decode_dict(self, raw_dict):
        decoded_dict = {}
        names = {claim.get_claim_key(): claim.get_claim_name() for claim in self._get_contained_claims()}
        for k, v in raw_dict.items():
            if isinstance(v, bytes):
                v = self.decode(v)
            try:
                decoded_dict[names[k]] = v
            except KeyError:
                if self.config.strict:
                    if not self.config.keep_going:
                        raise
                else:
                    decoded_dict[k] = v
        return decoded_dict

    def add_value_to_dict(self, token, value):
        entry_name = self.get_claim_name()
        try:
            token[entry_name] = []
            for raw_dict in value:
                decoded_dict = self._decode_dict(raw_dict)
                token[entry_name].append(decoded_dict)
        except TypeError:
            self.verifier.error('Invalid {} value: {}'.format(self.get_claim_name(), value))



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
            claim.add_value_to_dict(token, value)

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
