#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Copyright (c) 2024, Linaro Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

"""
Convert a PEM key into an equivalent COSE_Key, and optionally compute the CCA hash-lock claims.
The default is to strip the private part off the transformed key.  Pass the '--no-strip-private'
argument if the desired behaviour is to convert a private key as-is.  Note that this mode is
incompatible with CCA claims generation.

Examples:
    ./pem2cose.py -h
    ./pem2cose.py --no-strip-private ../tests/data/cca_realm.pem cca_realm.cbor
    ./pem2cose.py --hash-alg sha-256 ../tests/data/cca_realm.pem - > hashlock-claims.yaml

"""
import sys
import argparse

from iatverifier.util import read_keyfile
from iatverifier.attest_token_verifier import AttestationTokenVerifier
from hashlib import sha256, sha384, sha512
from base64 import b64encode
from pycose.keys import CoseKey
from pycose.keys.keyparam import EC2KpD


hash_algorithms = {
    'sha-256': sha256,
    'sha-384': sha384,
    'sha-512': sha512,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='convert a PEM key into an equivalent COSE_Key; optionally compute the CCA hash-lock claims')

    parser.add_argument('pemfile', type=str, help='input PEM file')
    parser.add_argument(
        'cosefile', type=str, help='output COSE_Key file (pass "-" to write to stdout)')
    parser.add_argument('--hash-alg', type=str, help='compute the hash lock using the specified algorithm',
                        choices=hash_algorithms.keys())
    parser.add_argument('--no-strip-private', help='do not strip the private key',
                        dest='strip_private', action='store_false')

    args = parser.parse_args()

    cose_key = read_keyfile(
        args.pemfile, AttestationTokenVerifier.SIGN_METHOD_SIGN1).encode()

    if not args.strip_private and args.hash_alg is not None:
        print('Private key conversion and CCA claims generation are mutually exclusive')
        sys.exit(1)

    if args.strip_private:
        tmp = CoseKey.decode(cose_key)
        try:
            del tmp[EC2KpD]
        except KeyError:
            pass
        cose_key = CoseKey.encode(tmp)

    if args.cosefile == '-':
        b64_cose_key = b64encode(cose_key).decode()
        print(f'cca_realm_pub_key: !!binary {b64_cose_key}')
    else:
        with open(args.cosefile, 'wb') as f:
            f.write(cose_key)

    if args.hash_alg is not None:
        h = hash_algorithms[args.hash_alg]()
        h.update(cose_key)
        b64_hash_lock = b64encode(h.digest()).decode()
        print(f'cca_platform_challenge: !!binary {b64_hash_lock}')
        print(f'cca_realm_pub_key_hash_algo_id: {args.hash_alg}')
