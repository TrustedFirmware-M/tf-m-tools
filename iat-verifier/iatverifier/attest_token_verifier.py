# -----------------------------------------------------------------------------
# Copyright (c) 2019-2025, Arm Limited. All rights reserved.
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

from pycose.messages.sign1message import Sign1Message
from pycose.messages.mac0message import Mac0Message

import cbor2
from cbor2 import CBOREncoder
import _cbor2

logger = logging.getLogger('iat-verifiers')

_CBOR_MAJOR_TYPE_ARRAY = 4
_CBOR_MAJOR_TYPE_MAP = 5
_CBOR_MAJOR_TYPE_SEMANTIC_TAG = 6

class TokenItem:
    """This class represents an item in the token map

    The Field `claim_type` contains an AttestationClaim object, that determines how to interpret the
    `value` field.
    The field `value` contains either another TokenItem object or a representation of a claim value
    (list, dictionary, bytestring...) depending on the value of `claim_type`

    A TokenItem object might have extra fields beyond these as it might be necessary to store
    properties during parsing, that can aid verifying.
    """
    def __init__(self, *, value, claim_type):
        self.value = value # The value of the claim
        self.claim_type = claim_type # an AttestationClaim instance

    @classmethod
    def _call_verify_with_parents(cls, claim_type_class, claim_type, token_item, indent):
        for parent_class in claim_type_class.__bases__:
            cls._call_verify_with_parents(parent_class, claim_type, token_item, indent + 2)
        if "verify" in claim_type_class.__dict__:
            claim_type_class.verify(claim_type, token_item)

    def verify(self):
        """Calls claim_type's and its parents' verify method"""
        claim_type = self.claim_type
        self.__class__._call_verify_with_parents(claim_type.__class__, claim_type, self, 0)

    def get_token_map(self):
        return self.claim_type.get_token_map(self)

    def __repr__(self):
        return f"TokenItem({self.claim_type.__class__.__name__}, {self.value})"

class AttestationClaim(ABC):
    """
    This class represents a claim.

    This class is abstract. A concrete claim have to be derived from this class,
    and it have to implement all the abstract methods.

    This class contains methods that are not abstract. These are here as a
    default behavior, that a derived class might either keep, or override.
    """

    MANDATORY = 0
    RECOMMENDED = 1
    OPTIONAL = 2

    def __init__(self, *, verifier, necessity=MANDATORY):
        self.config = verifier.config
        self.verifier = verifier
        self.necessity = necessity

    #
    # Abstract methods
    #

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
        if self.__class__.is_utf_8():
            try:
                return value.decode()
            except UnicodeDecodeError as exc:
                msg = 'Error decodeing value for "{}": {}'
                self.verifier.error(msg.format(self.get_claim_name(), exc))
                return str(value)[2:-1]
        else:  # not a UTF-8 value, i.e. a bytestring
            return value

    @classmethod
    def is_utf_8(cls):
        """Returns whether the value of this claim should be UTF-8"""
        return False

    def convert_map_to_token(self,
                             token_encoder,
                             token_map,
                             *,name_as_key,
                             parse_raw_value):
        """Encode a map in cbor format using the 'token_encoder'"""
        # pylint: disable=unused-argument
        value = token_map
        if parse_raw_value:
            value = self.__class__.parse_raw(value)
        return token_encoder.encode(value)

    def parse_token(self, *, token, lower_case_key):
        """Parse a token into a map

        This function is recursive for composite claims and for token verifiers.

        The `token` parameter can be interpreted differently in derived classes:
        - as a raw token that is decoded by the CBOR parsing library
        - as CBOR encoded token in case of (nested) tokens.
        """
        return TokenItem(value=token, claim_type=self)

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

    def _validate_bytestrings_equal(self, value, name, expected):
        self._validate_bytestring_length_equals(value, name, len(expected))
        for i, (b1, b2) in enumerate(zip(value, expected)):
            if b1 != b2:
                msg = f'Invalid {name} byte at {i}: 0x{b1:02x} instead of 0x{b2:02x}'
                self.verifier.error(msg)

    def get_token_map(self, token_item):
        formatted = self.__class__.get_formatted_value(token_item.value)

        # If the formatted value is still a bytestring then try to decode
        if isinstance(formatted, bytes):
            formatted = self.decode(formatted)

        return formatted

class CompositeAttestClaim(AttestationClaim):
    """
    This class represents composite claim.

    This class is still abstract, but can contain other claims. This means that
    a value representing this claim is a dictionary, or a list of dictionaries.
    This claim contains further claims which represent the possible key-value
    pairs in the value for this claim.

    It is possible that there are requirement that the claims in this claim must
    satisfy, but this can't be checked in the `verify` function of a claim.

    For example the composite claim can contain a claim type `A`, and a claim
    type `B`, exactly one of the two can be present.

    In this case the class inheriting from this class can have its own verify()
    method.
    """

    def __init__(self,
                 *, verifier,
                 claims,
                 is_list,
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

    def _get_contained_claims(self):
        for claim, args in self.claims:
            try:
                yield claim(**args)
            except TypeError as exc:
                raise TypeError(f"Failed to instantiate '{claim}' with args '{args}' in token " +
                                f"{type(self.verifier)}\nSee error in exception above.") from exc


    def _verify_dict(self, claim_type, entry_number, dictionary):
        if not isinstance(dictionary, dict):
            if self.config.strict:
                msg = 'The values in token {} must be a dict.'
                self.verifier.error(msg.format(claim_type.get_claim_name()))
            else:
                msg = 'The values in token {} must be a dict, skipping'
                self.verifier.warning(msg.format(claim_type.get_claim_name()))
                return

        claim_names = [val.get_claim_name() for val in claim_type._get_contained_claims()]
        for claim_name, _ in dictionary.items():
            if claim_name not in claim_names:
                if self.config.strict:
                    msg = 'Unexpected {} claim: {}'
                    self.verifier.error(msg.format(claim_type.get_claim_name(), claim_name))
                else:
                    msg = 'Unexpected {} claim: {}, skipping.'
                    self.verifier.warning(msg.format(claim_type.get_claim_name(), claim_name))
                    continue

        claims = {val.get_claim_key(): val for val in claim_type._get_contained_claims()}
        self._check_claims_necessity(entry_number, claims, dictionary)
        for token_item in dictionary.values():
            if isinstance(token_item, TokenItem):
                token_item.verify()
            else:
                # the parse of this token item failed. So it cannot be verified.
                # Warning had been reported during parsing.
                pass

    def verify(self, token_item):
        if self.is_list:
            if not isinstance(token_item.value, list):
                if self.config.strict:
                    msg = 'The value of this token {} must be a list.'
                    self.verifier.error(msg.format(self.get_claim_name()))
                else:
                    msg = 'The value of this token {} must be a list, skipping'
                    self.verifier.warning(msg.format(self.get_claim_name()))
                    return
            for entry_number, list_item in enumerate(token_item.value):
                self._verify_dict(token_item.claim_type, entry_number, list_item)
        else:
            self._verify_dict(token_item.claim_type, None, token_item.value)

    def _parse_token_dict(self, *, entry_number, token, lower_case_key):
        claim_value = {}

        if not isinstance(token, dict):
            claim_value = token
        else:
            claims = {val.get_claim_key(): val for val in self._get_contained_claims()}
            for key, val in token.items():
                try:
                    claim = claims[key]
                    name = claim.get_claim_name()
                    if lower_case_key:
                        name = name.lower()
                    claim_value[name] = claim.parse_token(
                        token=val,
                        lower_case_key=lower_case_key)
                except KeyError:
                    claim_value[key] = val
                except Exception:
                    if not self.config.keep_going:
                        raise
        return claim_value

    def _check_claims_necessity(self, entry_number, claims, dictionary):
        mandatory_claim_names = [claim.get_claim_name() for claim in claims.values() if claim.necessity == AttestationClaim.MANDATORY]
        recommended_claim_names = [claim.get_claim_name() for claim in claims.values() if claim.necessity == AttestationClaim.RECOMMENDED]
        dictionary_claim_names = dictionary.keys()

        for mandatory_claim_name in mandatory_claim_names:
            if mandatory_claim_name not in dictionary_claim_names:
                msg = (f'Invalid IAT: missing MANDATORY claim "{mandatory_claim_name}" '
                    f'from {self.get_claim_name()}')
                if entry_number is not None:
                    msg += f' at index {entry_number}'
                self.verifier.error(msg)

        for recommended_claim_name in recommended_claim_names:
            if recommended_claim_name not in dictionary_claim_names:
                msg = (f'Missing RECOMMENDED claim "{recommended_claim_name}" '
                    f'from {self.get_claim_name()}')
                if entry_number is not None:
                    msg += f' at index {entry_number}'
                self.verifier.warning(msg)

    def parse_token(self, *, token, lower_case_key):
        """This expects a raw token map as 'token'"""

        if self.is_list:
            claim_value = []
            if not isinstance(token, list):
                claim_value = token
            else:
                for entry_number, entry in enumerate(token):
                    claim_value.append(self._parse_token_dict(
                            entry_number=entry_number,
                            token=entry,
                            lower_case_key=lower_case_key))
        else:
            claim_value = self._parse_token_dict(
                entry_number=None,
                token=token,
                lower_case_key=lower_case_key)
        return TokenItem(value=claim_value, claim_type=self)


    def _encode_dict(self, token_encoder, token_map, *, name_as_key, parse_raw_value):
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
            *, name_as_key,
            parse_raw_value):
        if self.is_list:
            token_encoder.encode_length(_CBOR_MAJOR_TYPE_ARRAY, len(token_map))
            for item in token_map:
                self._encode_dict(
                    token_encoder,
                    item,
                    name_as_key=name_as_key,
                    parse_raw_value=parse_raw_value)
        else:
            self._encode_dict(
                token_encoder,
                token_map,
                name_as_key=name_as_key,
                parse_raw_value=parse_raw_value)

    def get_token_map(self, token_item):
        if self.is_list:
            ret = []
            for token_item_dict in token_item.value:
                token_dict = {}
                for key, claim_token_item in token_item_dict.items():
                    if isinstance(claim_token_item, TokenItem):
                        token_dict[key] = claim_token_item.get_token_map()
                    else:
                        # The claim was not recognised, so just adding it as it
                        # was in the map:
                        token_dict[key] = claim_token_item
                ret.append(token_dict)
            return ret
        else:
            token_dict = {}
            for key, claim_token_item in token_item.value.items():
                if isinstance(claim_token_item, TokenItem):
                    token_dict[key] = claim_token_item.get_token_map()
                else:
                    # The claim was not recognised, so just adding it as it
                    # was in the map:
                    token_dict[key] = claim_token_item
            return token_dict

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
        return "TOKEN_ROOT_CLAIMS"

class AttestationTokenVerifier(AttestationClaim):
    """Abstract base class for attestation token verifiers"""

    SIGN_METHOD_SIGN1 = "sign"
    SIGN_METHOD_MAC0 = "mac"
    SIGN_METHOD_RAW = "raw"

    @abstractmethod
    def _get_p_header(self):
        """Return the protected header for this Token"""
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
                necessity=necessity)

        super().__init__(verifier=self, necessity=necessity)

    def _sign_token(self, token):
        """Signs a token"""
        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_RAW:
            return token
        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_SIGN1:
            return self._sign_eat(token)
        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_MAC0:
            return self._hmac_eat(token)
        err_msg = 'Unexpected method "{}"; must be one of: raw, sign, mac'
        raise ValueError(err_msg.format(self.method))

    def _sign_eat(self, token):
        p_header=self._get_p_header()
        key=self._get_signing_key()
        signed_msg = Sign1Message(payload=token, key=key, phdr=p_header)
        return signed_msg.encode()


    def _hmac_eat(self, token):
        p_header=self._get_p_header()
        key=self._get_signing_key()
        hmac_msg = Mac0Message(payload=token, key=key, phdr=p_header)
        return hmac_msg.encode()

    def check_type_indicator(self, *, token):
        # By default no type indication is expected
        return token

    def encode_type_indicator(self, *, encoder):
        # By default no type indication is added
        pass

    def _get_cose_sign1_payload(self, cose, *, verify_signature):
        msg = Sign1Message.decode(cose)
        if verify_signature:
            key = self._get_signing_key()
            try:
                self._parse_p_header(msg)
            except Exception as exc:
                self.error(f'Invalid Protected header: {exc}', exception=exc)
            msg.key = key
            if not msg.verify_signature():
                raise ValueError('Bad signature')
        return msg.payload, msg.phdr


    def _get_cose_mac0_payload(self, cose, *, verify_signature):
        msg = Mac0Message.decode(cose)
        if verify_signature:
            key = self._get_signing_key()
            try:
                self._parse_p_header(msg)
            except Exception as exc:
                self.error(f'Invalid Protected header: {exc}', exception=exc)
            msg.key = key
            if not msg.verify_tag(alg=self._get_cose_alg()):
                raise ValueError('Bad signature')
        return msg.payload, msg.phdr


    def _get_cose_payload(self, cose, *, verify_signature):
        """Return the payload of a COSE envelope"""
        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_SIGN1:
            return self._get_cose_sign1_payload(
                cose,
                verify_signature=verify_signature)
        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_MAC0:
            return self._get_cose_mac0_payload(
                cose,
                verify_signature=verify_signature)
        err_msg = f'Unexpected method "{self._get_method()}"; must be one of: sign, mac'
        raise ValueError(err_msg)

    def convert_map_to_token(
            self,
            token_encoder,
            token_map,
            *, name_as_key,
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
                name_as_key=name_as_key,
                parse_raw_value=parse_raw_value)

            token = b_io.getvalue()

            # Sign and pack in a COSE envelope if necessary
            signed_token = self._sign_token(token)

            self.encode_type_indicator(encoder=token_encoder)

            if 'encode_type_indicator' in self.__dict__:
                # If the current verifier has its own encode_type_indicator
                # implemented, then the signed token needs to be encoded as a
                # bytestring, and passed to the type indicator encoding like
                # that:
                token_encoder.encode_bytestring(signed_token)
            else:
                # Otherwise encoding depends on the 'root' parameter
                if root:
                    token_encoder.write(signed_token)
                else:
                    token_encoder.encode_bytestring(signed_token)

    def parse_token(self, *, token, lower_case_key):

        token = self.check_type_indicator(token=token)

        if self._get_method() == AttestationTokenVerifier.SIGN_METHOD_RAW:
            payload = token
            protected_header = None
        else:
            verify_signature = False
            try:
                payload, protected_header = self._get_cose_payload(
                    token,
                    # signature verification is done in the verify function
                    verify_signature=verify_signature)
            except Exception as exc:
                msg = f'Parse (verify_signature={verify_signature}): Bad COSE: {exc}'
                self.error(msg)

        try:
            raw_map = cbor2.loads(payload)
        except Exception as exc:
            msg = f'Invalid CBOR: {exc}'
            self.error(msg)

        if isinstance(raw_map, _cbor2.CBORTag):
            raw_map_tag = raw_map.tag
            raw_map = raw_map.value
        else:
            raw_map_tag = None

        token_items = self.claims.parse_token(
            token=raw_map,
            lower_case_key=lower_case_key)

        ret = TokenItem(value=token_items, claim_type=self)
        ret.wrapping_tag = raw_map_tag
        ret.token = token
        ret.protected_header = protected_header
        return ret

    def verify(self, token_item):
        if self._get_method() != AttestationTokenVerifier.SIGN_METHOD_RAW:
            verify_signature = self._get_signing_key() is not None
            try:
                self._get_cose_payload(
                    token_item.token,
                    verify_signature=verify_signature)
            except Exception as exc:
                msg = f'Verify (verify_signature={verify_signature}): Bad COSE: {exc}'
                raise ValueError(msg) from exc

        wrapping_tag = self._get_wrapping_tag()
        if token_item.wrapping_tag is not None:
            if wrapping_tag is None:
                msg = f'Invalid token: Unexpected tag (0x{token_item.wrapping_tag:x}) in token {self.get_claim_name()}'
                self.error(msg)
            else:
                if wrapping_tag != token_item.wrapping_tag:
                    msg = f'Invalid token: token {self.get_claim_name()} is wrapped in tag 0x{token_item.wrapping_tag:x} instead of 0x{wrapping_tag:x}'
                    self.error(msg)
        else:
            if wrapping_tag is not None:
                msg = f'Invalid token: token {self.get_claim_name()} should be wrapped in tag 0x{wrapping_tag:x}'
                self.error(msg)

        token_item.value.verify()

    def get_token_map(self, token_item):
        return self.claims.get_token_map(token_item.value)

    def error(self, message, *, exception=None):
        """Act on an error depending on the configuration of this verifier"""
        self.seen_errors = True
        if self.config.keep_going:
            logger.error(message)
        else:
            if exception is None:
                raise ValueError(message)
            else:
                raise ValueError(message) from Exception

    def warning(self, message):
        """Print a warning with the logger of this verifier"""
        logger.warning(message)
