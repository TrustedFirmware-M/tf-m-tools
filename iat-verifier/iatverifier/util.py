# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

"""Helper utilities for CLI tools and tests"""

from collections.abc import Iterable
from copy import deepcopy
import logging

import base64
import yaml
from ecdsa import SigningKey, VerifyingKey
from iatverifier.attest_token_verifier import AttestationTokenVerifier
from cbor2 import CBOREncoder

_logger = logging.getLogger("util")

_known_curves = {
    "NIST256p": AttestationTokenVerifier.COSE_ALG_ES256,
    "NIST384p": AttestationTokenVerifier.COSE_ALG_ES384,
    "NIST521p": AttestationTokenVerifier.COSE_ALG_ES512,
}

def convert_map_to_token(token_map, verifier, wfh, *, add_p_header, name_as_key, parse_raw_value):
    """
    Convert a map to token and write the result to a file.
    """
    encoder = CBOREncoder(wfh)
    verifier.convert_map_to_token(
        encoder,
        token_map,
        add_p_header=add_p_header,
        name_as_key=name_as_key,
        parse_raw_value=parse_raw_value,
        root=True)


def read_token_map(file):
    """
    Read a yaml file and return a map
    """
    if hasattr(file, 'read'):
        raw = yaml.safe_load(file)
    else:
        with open(file, encoding="utf8") as file_obj:
            raw = yaml.safe_load(file_obj)

    return raw


def recursive_bytes_to_strings(token, in_place=False):
    """
    Transform the map in 'token' by changing changing bytes to base64 encoded form.

    if 'in_place' is True, 'token' is modified, a new map is returned otherwise.
    """
    if in_place:
        result = token
    else:
        result = deepcopy(token)

    if hasattr(result, 'items'):
        for key, value in result.items():
            result[key] = recursive_bytes_to_strings(value, in_place=True)
    elif (isinstance(result, Iterable) and
            not isinstance(result, (str, bytes))):
        result = [recursive_bytes_to_strings(r, in_place=True)
                  for r in result]
    elif isinstance(result, bytes):
        result = str(base64.b16encode(result))

    return result


def read_keyfile(keyfile, method=AttestationTokenVerifier.SIGN_METHOD_SIGN1):
    """
    Read a keyfile and return the key
    """
    if keyfile:
        if method == AttestationTokenVerifier.SIGN_METHOD_SIGN1:
            return _read_sign1_key(keyfile)
        if method == AttestationTokenVerifier.SIGN_METHOD_MAC0:
            return _read_hmac_key(keyfile)
        err_msg = 'Unexpected method "{}"; must be one of: sign, mac'
        raise ValueError(err_msg.format(method))

    return None

def get_cose_alg_from_key(key):
    """Extract the algorithm from the key if possible

    Returns the signature algorithm ID defined by COSE
    """
    if not hasattr(key, "curve"):
        raise ValueError("Key has no curve specified in it.")
    return _known_curves[key.curve.name]

def _read_sign1_key(keyfile):
    with open(keyfile, 'rb') as file_obj:
        raw_key = file_obj.read()
    try:
        key = SigningKey.from_pem(raw_key)
    except Exception as exc:
        signing_key_error = str(exc)

        try:
            key = VerifyingKey.from_pem(raw_key)
        except Exception as vexc:
            verifying_key_error = str(vexc)

            msg = 'Bad key file "{}":\n\tpubkey error: {}\n\tprikey error: {}'
            raise ValueError(msg.format(keyfile, verifying_key_error, signing_key_error)) from vexc
    return key


def _read_hmac_key(keyfile):
    return open(keyfile, 'rb').read()
