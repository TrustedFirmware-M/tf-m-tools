# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022, Arm Limited. All rights reserved.
# Copyright (c) 2024, Linaro Limited. All rights reserved.
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
import yaml_include
from pycose.keys import CoseKey
from ecdsa.curves import NIST256p, NIST384p, NIST521p
from pycose.keys.curves import P256, P384, P521
from pycose.keys.keytype import KtyEC2
from pycose.algorithms import Es256, Es384, Es512, HMAC256
from ecdsa.keys import VerifyingKey
from iatverifier.attest_token_verifier import AttestationTokenVerifier
from cbor2 import CBOREncoder
from pycose.keys import CoseKey
from ecdsa.util import number_to_string

_logger = logging.getLogger("util")

_known_curves = {
    P256: Es256,
    P384: Es384,
    P521: Es512,
}

_ecdsa_to_cose_curve = {
    'NIST256p': 'P_256',
    'NIST384p': 'P_384',
    'NIST521p': 'P_512',
}

def ec2_cose_key_from_raw_ecdsa(k, alg):
    crv = alg.get_curve()
    hash_func = alg.get_hash_func()

    vk = VerifyingKey.from_string(k, curve=crv, hashfunc=hash_func)

    d = {
        'KTY': 'EC2',
        'CURVE': _ecdsa_to_cose_curve[crv.name],
        'ALG': alg.fullname,
        'X': number_to_string(vk.pubkey.point.x(), vk.curve.generator.order()),
        'Y': number_to_string(vk.pubkey.point.y(), vk.curve.generator.order()),
    }

    return CoseKey.from_dict(d)


def convert_map_to_token(token_map, verifier, wfh, *, name_as_key, parse_raw_value):
    """
    Convert a map to token and write the result to a file.
    """
    encoder = CBOREncoder(wfh)
    verifier.convert_map_to_token(
        encoder,
        token_map,
        name_as_key=name_as_key,
        parse_raw_value=parse_raw_value,
        root=True)


def read_token_map(file):
    """
    Read a yaml file and return a map
    """
    yaml.add_constructor("!inc", yaml_include.Constructor(base_dir='.'), Loader=yaml.SafeLoader)

    if hasattr(file, 'read'):
        raw = yaml.load(file, Loader=yaml.SafeLoader)
    else:
        with open(file, encoding="utf8") as file_obj:
            raw = yaml.load(file_obj, Loader=yaml.SafeLoader)

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

def get_cose_alg_from_key(key, default):
    """Extract the algorithm from the key if possible

    Returns the signature algorithm ID defined by COSE
    If key is None, default is returned.
    """
    if key is None:
        return default
    if key.kty is not KtyEC2:
        err_msg = 'Unexpected key type "{}"; must be KtyEC2'
        raise ValueError(err_msg.format(key.kty))
    if key.alg is not None:
        return key.alg
    return _known_curves[key.crv]

def _read_sign1_key(keyfile):
    with open(keyfile, 'rb') as file_obj:
        s = file_obj.read()
        raw_key = s.decode("utf-8") # assume PEM-encoded key
    try:
        key = CoseKey.from_pem_private_key(raw_key)
    except Exception as exc:
        signing_key_error = str(exc)

        try:
            key = CoseKey.from_pem_public_key(raw_key)
        except Exception as vexc:
            verifying_key_error = str(vexc)

            msg = 'Bad key file "{}":\n\tpubkey error: {}\n\tprikey error: {}'
            raise ValueError(msg.format(keyfile, verifying_key_error, signing_key_error)) from vexc
    return key


def _read_hmac_key(keyfile):
    k = open(keyfile, 'rb').read()
    d = {
        'KTY': 'SYMMETRIC',
        'ALG': HMAC256,
        'K': k,
    }
    return CoseKey.from_dict(d)