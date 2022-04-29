# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

"""
Class definitions to use as base for claim and verifier classes.
"""


import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BytesIO

from pycose.attributes import CoseAttrs
from pycose.sign1message import Sign1Message
from pycose.mac0message import Mac0Message

import cbor2
from cbor2 import CBOREncoder

logger = logging.getLogger('iat-verifiers')

_CBOR_MAJOR_TYPE_ARRAY = 4
_CBOR_MAJOR_TYPE_MAP = 5
_CBOR_MAJOR_TYPE_SEMANTIC_TAG = 6

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

    def __init__(self, *, verifier, necessity=MANDATORY):
        self.config = verifier.config
        self.verifier = verifier
        self.necessity = necessity
        self.verify_count = 0
        self.cross_claim_requirement_checker = None

    #
    # Abstract methods
    #

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

    #
    # Default methods that a derived class might override
    #

    def decode(self, value):
        """
        Decode the value of the claim if the value is an UTF-8 string
        """
        if type(self).is_utf_8():
            try:
                return value.decode()
            except UnicodeDecodeError as exc:
                msg = 'Error decodeing value for "{}": {}'
                self.verifier.error(msg.format(self.get_claim_name(), exc))
                return str(value)[2:-1]
        else:  # not a UTF-8 value, i.e. a bytestring
            return value

    def claim_found(self):
        """Return true if verify was called on tis claim instance"""
        return self.verify_count>0

    @classmethod
    def is_utf_8(cls):
        """Returns whether the value of this claim should be UTF-8"""
        return False

    def convert_map_to_token(self,
                             token_encoder,
                             token_map,
                             *, add_p_header,
                             name_as_key,
                             parse_raw_value):
        """Encode a map in cbor format using the 'token_encoder'"""
        # pylint: disable=unused-argument
        value = token_map
        if parse_raw_value:
            value = type(self).parse_raw(value)
        return token_encoder.encode(value)

    def parse_token(self, *, token, verify, check_p_header, lower_case_key):
        """Parse a token into a map

        This function is recursive for composite claims and for token verifiers.
        A big difference is that the parameter token should be a map for claim
        objects, and a 'bytes' object for verifiers. The entry point to this
        function is calling the parse_token function of a verifier.

        From some aspects it would be cleaner to have different functions for
        this in verifiers and claims, but that would require to do a type check
        in every recursive step to see which method to call. So instead the
        method name is the same, and the 'token' parameter is interpreted
        differently."""
        # pylint: disable=unused-argument
        if verify:
            self.verify(token)

        formatted = type(self).get_formatted_value(token)

        # If the formatted value is still a bytestring then try to decode
        if isinstance(formatted, bytes):
            formatted = self.decode(formatted)
        return formatted

    @classmethod
    def parse_raw(cls, raw_value):
        """Parse a raw value

        Takes a string, as it appears in a yaml file, and converts it to a
        numeric value according to the claim's definition.
        """
        return raw_value

    @classmethod
    def get_formatted_value(cls, value):
        """Format the value according to this claim"""
        if cls.is_utf_8():
            # this is an UTF-8 value, force string type
            return f'{value}'
        return value

    #
    # Helper functions to be called from derived classes
    #

    def _check_type(self, name, value, expected_type):
        """Check that a value's type is as expected"""
        if not isinstance(value, expected_type):
            msg = 'Invalid {}: must be a(n) {}: found {}'
            self.verifier.error(msg.format(name, expected_type, type(value)))
            return False
        return True

    def _validate_bytestring_length_equals(self, value, name, expected_len):
        """Check that a bytestring length is as expected"""
        self._check_type(name, value, bytes)

        value_len = len(value)
        if value_len != expected_len:
            msg = 'Invalid {} length: must be exactly {} bytes, found {} bytes'
            self.verifier.error(msg.format(name, expected_len, value_len))

    def _validate_bytestring_length_one_of(self, value, name, possible_lens):
        """Check that a bytestring length is as expected"""
        self._check_type(name, value, bytes)

        value_len = len(value)
        if value_len not in possible_lens:
            msg = 'Invalid {} length: must be one of {} bytes, found {} bytes'
            self.verifier.error(msg.format(name, possible_lens, value_len))

    def _validate_bytestring_length_between(self, value, name, min_len, max_len):
        """Check that a bytestring length is as expected"""
        self._check_type(name, value, bytes)

        value_len = len(value)
        if value_len < min_len or value_len > max_len:
            msg = 'Invalid {} length: must be between {} and {} bytes, found {} bytes'
            self.verifier.error(msg.format(name, min_len, max_len, value_len))

    def _validate_bytestring_length_is_at_least(self, value, name, minimal_length):
        """Check that a bytestring has a minimum length"""
        self._check_type(name, value, bytes)

        value_len = len(value)
        if value_len < minimal_length:
            msg = 'Invalid {} length: must be at least {} bytes, found {} bytes'
            self.verifier.error(msg.format(name, minimal_length, value_len))


class NonVerifiedClaim(AttestationClaim):
    """An abstract claim type for which verify() always passes.

    Can be used for claims for which no verification is implemented."""
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

    def __init__(self,
                 *, verifier,
                 claims,
                 is_list,
                 cross_claim_requirement_checker,
                 necessity=AttestationClaim.MANDATORY):
        """ Initialise a composite claim.

        In case 'is_list' is False, the expected type of value is a dictionary,
        containing the necessary claims determined by the 'claims' list.
        In case 'is_list' is True, the expected type of value is a list,
        containing a number of dictionaries, each one containing the necessary
        claims determined by the 'claims' list.
        """
        super().__init__(verifier=verifier, necessity=necessity)
        self.is_list = is_list
        self.claims = claims
        self.cross_claim_requirement_checker = cross_claim_requirement_checker

    def _get_contained_claims(self):
        claims = []
        for claim, args in self.claims:
            try:
                claims.append(claim(**args))
            except TypeError as exc:
                raise TypeError(f"Failed to instantiate '{claim}' with args '{args}' in token " +
                                f"{type(self.verifier)}\nSee error in exception above.") from exc
        return claims


    def verify(self, value):
        self.verify_count += 1

    def _parse_token_dict(self, *, entry_number, token, verify, check_p_header, lower_case_key):
        ret = {}

        if verify:
            self.verify(token)
            if not self._check_type(self.get_claim_name(), token, dict):
                return None
        else:
            if not isinstance(token, dict):
                return token

        claims = {val.get_claim_key(): val for val in self._get_contained_claims()}
        for key, val in token.items():
            if key not in claims.keys():
                if verify and self.config.strict:
                    msg = 'Unexpected {} claim: {}'
                    self.verifier.error(msg.format(self.get_claim_name(), key))
                else:
                    continue
            try:
                claim = claims[key]
                name = claim.get_claim_name()
                if lower_case_key:
                    name = name.lower()
                ret[name] = claim.parse_token(
                    token=val,
                    verify=verify,
                    check_p_header=check_p_header,
                    lower_case_key=lower_case_key)
            except Exception:
                if not self.config.keep_going:
                    raise

        if verify:
            self._check_claims_necessity(entry_number, claims)
            if self.cross_claim_requirement_checker is not None:
                self.cross_claim_requirement_checker(self.verifier, claims)

        return ret

    def _check_claims_necessity(self, entry_number, claims):
        for claim in claims.values():
            if not claim.claim_found():
                if claim.necessity==AttestationClaim.MANDATORY:
                    msg = (f'Invalid IAT: missing MANDATORY claim "{claim.get_claim_name()}" '
                        f'from {self.get_claim_name()}')
                    if entry_number is not None:
                        msg += f' at index {entry_number}'
                    self.verifier.error(msg)
                elif claim.necessity==AttestationClaim.RECOMMENDED:
                    msg = (f'Missing RECOMMENDED claim "{claim.get_claim_name()}" '
                        f'from {self.get_claim_name()}')
                    if entry_number is not None:
                        msg += f' at index {entry_number}'
                    self.verifier.warning(msg)

    def parse_token(self, *, token, verify, check_p_header, lower_case_key):
        """This expects a raw token map as 'token'"""

        if self.is_list:
            ret = []
            if verify:
                if not self._check_type(self.get_claim_name(), token, list):
                    return None
            else:
                if not isinstance(token, list):
                    return token
            for entry_number, entry in enumerate(token):
                ret.append(self._parse_token_dict(
                    entry_number=entry_number,
                    check_p_header=check_p_header,
                    token=entry,
                    verify=verify,
                    lower_case_key=lower_case_key))
            return ret
        return self._parse_token_dict(
            entry_number=None,
            check_p_header=check_p_header,
            token=token,
            verify=verify,
            lower_case_key=lower_case_key)


    def _encode_dict(self, token_encoder, token_map, *, add_p_header, name_as_key, parse_raw_value):
        token_encoder.encode_length(_CBOR_MAJOR_TYPE_MAP, len(token_map))
        if name_as_key:
            claims = {claim.get_claim_name().lower():
                claim for claim in self._get_contained_claims()}
        else:
            claims = {claim.get_claim_key(): claim for claim in self._get_contained_claims()}
        for key, val in token_map.items():
            try:
                claim = claims[key]
                key = claim.get_claim_key()
                token_encoder.encode(key)
                claim.convert_map_to_token(
                    token_encoder,
                    val,
                    add_p_header=add_p_header,
                    name_as_key=name_as_key,
                    parse_raw_value=parse_raw_value)
            except KeyError:
                if self.config.strict:
                    if not self.config.keep_going:
                        raise
                else:
                    token_encoder.encode(key)
                    token_encoder.encode(val)

    def convert_map_to_token(
            self,
            token_encoder,
            token_map,
            *, add_p_header,
            name_as_key,
            parse_raw_value):
        if self.is_list:
            token_encoder.encode_length(_CBOR_MAJOR_TYPE_ARRAY, len(token_map))
            for item in token_map:
                self._encode_dict(
                    token_encoder,
                    item,
                    add_p_header=add_p_header,
                    name_as_key=name_as_key,
                    parse_raw_value=parse_raw_value)
        else:
            self._encode_dict(
                token_encoder,
                token_map,
                add_p_header=add_p_header,
                name_as_key=name_as_key,
                parse_raw_value=parse_raw_value)


@dataclass
class VerifierConfiguration:
    """A class storing the configuration of the verifier.

    At the moment this determines what should happen if a problem is found
    during verification.
    """
    keep_going: bool = False
    strict: bool = False

class AttestTokenRootClaims(CompositeAttestClaim):
    """A claim type that is used to represent the claims in a token.

    It is instantiated by AttestationTokenVerifier, and shouldn't be used
    outside this module."""
    def get_claim_key(self=None):
        return None

    def get_claim_name(self=None):
        return None

# This class inherits from NonVerifiedClaim. The actual claims in the token are
# checked by the AttestTokenRootClaims object owned by this verifier. The
# verify() function of the AttestTokenRootClaims object is called during
# traversing the claim tree.
class AttestationTokenVerifier(NonVerifiedClaim):
    """Abstract base class for attestation token verifiers"""

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

    @abstractmethod
    def _get_p_header(self):
        """Return the protected header for this Token

        Return a dictionary if p_header should be present, and None if the token
        doesn't defines a protected header.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_wrapping_tag(self):
        """The value of the tag that the token is wrapped in.

        The function should return None if the token is not wrapped.
        """
        return None

    @abstractmethod
    def _parse_p_header(self, msg):
        """Throw exception in case of error"""

    @staticmethod
    @abstractmethod
    def check_cross_claim_requirements(verifier, claims):
        """Throw exception in case of error"""

    def _get_cose_alg(self):
        return self.cose_alg

    def _get_method(self):
        return self.method

    def _get_signing_key(self):
        return self.signing_key

    def __init__(
            self,
            *, method,
            cose_alg,
            signing_key,
            claims,
            configuration=None,
            necessity=AttestationClaim.MANDATORY):
        self.method = method
        self.cose_alg = cose_alg
        self.signing_key=signing_key
        self.config = configuration if configuration is not None else VerifierConfiguration()
        self.seen_errors = False
        self.claims = AttestTokenRootClaims(
                verifier=self,
                claims=claims,
                is_list=False,
                cross_claim_requirement_checker=type(self).check_cross_claim_requirements,
                necessity=necessity)

        super().__init__(verifier=self, necessity=necessity)

    def _sign_token(self, token, add_p_header):
        """Signs a token"""
        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_RAW:
            return token
        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_SIGN1:
            return self._sign_eat(token, add_p_header)
        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_MAC0:
            return self._hmac_eat(token, add_p_header)
        err_msg = 'Unexpected method "{}"; must be one of: raw, sign, mac'
        raise ValueError(err_msg.format(self.method))

    def _sign_eat(self, token, add_p_header):
        protected_header = CoseAttrs()
        p_header=self._get_p_header()
        key=self._get_signing_key()
        if add_p_header and p_header is not None and key:
            protected_header.update(p_header)
        signed_msg = Sign1Message(p_header=protected_header)
        signed_msg.payload = token
        if key:
            signed_msg.key = key
            signed_msg.signature = signed_msg.compute_signature(alg=self._get_cose_alg())
        return signed_msg.encode()


    def _hmac_eat(self, token, add_p_header):
        protected_header = CoseAttrs()
        p_header=self._get_p_header()
        key=self._get_signing_key()
        if add_p_header and p_header is not None and key:
            protected_header.update(p_header)
        hmac_msg = Mac0Message(payload=token, key=key, p_header=protected_header)
        hmac_msg.compute_auth_tag(alg=self.cose_alg)
        return hmac_msg.encode()


    def _get_cose_sign1_payload(self, cose, *, check_p_header, verify_signature):
        msg = Sign1Message.decode(cose)
        if verify_signature:
            key = self._get_signing_key()
            if check_p_header:
                self._parse_p_header(msg)
            msg.key = key
            msg.signature = msg.signers
            try:
                msg.verify_signature(alg=self._get_cose_alg())
            except Exception as exc:
                raise ValueError(f'Bad signature ({exc})') from exc
        return msg.payload


    def _get_cose_mac0_payload(self, cose, *, check_p_header, verify_signature):
        msg = Mac0Message.decode(cose)
        if verify_signature:
            key = self._get_signing_key()
            if check_p_header:
                self._parse_p_header(msg)
            msg.key = key
            try:
                msg.verify_auth_tag(alg=self._get_cose_alg())
            except Exception as exc:
                raise ValueError(f'Bad signature ({exc})') from exc
        return msg.payload


    def _get_cose_payload(self, cose, *, check_p_header, verify_signature):
        """Return the payload of a COSE envelope"""
        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_SIGN1:
            return self._get_cose_sign1_payload(
                cose,
                check_p_header=check_p_header,
                verify_signature=verify_signature)
        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_MAC0:
            return self._get_cose_mac0_payload(
                cose,
                check_p_header=check_p_header,
                verify_signature=verify_signature)
        err_msg = f'Unexpected method "{self._get_method()}"; must be one of: sign, mac'
        raise ValueError(err_msg)


    def convert_map_to_token(
            self,
            token_encoder,
            token_map,
            *, add_p_header,
            name_as_key,
            parse_raw_value,
            root=False):
        with BytesIO() as b_io:
            # Create a new encoder instance
            encoder = CBOREncoder(b_io)

            # Add tag if necessary
            wrapping_tag = self._get_wrapping_tag()
            if wrapping_tag is not None:
                # TODO: this doesn't saves the string references used up to the
                # point that this tag is added (see encode_semantic(...) in cbor2's
                # encoder.py). This is not a problem as far the tokens don't use
                # string references (which is the case for now).
                encoder.encode_length(_CBOR_MAJOR_TYPE_SEMANTIC_TAG, wrapping_tag)

            # Encode the token payload
            self.claims.convert_map_to_token(
                encoder,
                token_map,
                add_p_header=add_p_header,
                name_as_key=name_as_key,
                parse_raw_value=parse_raw_value)

            token = b_io.getvalue()

            # Sign and pack in a COSE envelope if necessary
            signed_token = self._sign_token(token, add_p_header=add_p_header)

            # Pack as a bstr if necessary
            if root:
                token_encoder.write(signed_token)
            else:
                token_encoder.encode_bytestring(signed_token)

    def parse_token(self, *, token, verify, check_p_header, lower_case_key):
        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_RAW:
            payload = token
        else:
            try:
                payload = self._get_cose_payload(
                    token,
                    check_p_header=check_p_header,
                    verify_signature=(verify and self._get_signing_key() is not None))
            except Exception as exc:
                msg = f'Bad COSE: {exc}'
                raise ValueError(msg) from exc

        try:
            raw_map = cbor2.loads(payload)
        except Exception as exc:
            msg = f'Invalid CBOR: {exc}'
            raise ValueError(msg) from exc

        wrapping_tag = self._get_wrapping_tag()
        if wrapping_tag is not None:
            if verify and wrapping_tag != raw_map.tag:
                msg = 'Invalid token: token is wrapped in tag {} instead of {}'
                raise ValueError(msg.format(raw_map.tag, wrapping_tag))
            raw_map = raw_map.value

        if verify:
            self.verify(token)

        return self.claims.parse_token(
            token=raw_map,
            check_p_header=check_p_header,
            verify=verify,
            lower_case_key=lower_case_key)

    def error(self, message):
        """Act on an error depending on the configuration of this verifier"""
        self.seen_errors = True
        if self.config.keep_going:
            logger.error(message)
        else:
            raise ValueError(message)

    def warning(self, message):
        """Print a warning with the logger of this verifier"""
        logger.warning(message)
