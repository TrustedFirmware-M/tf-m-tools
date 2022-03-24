# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import argparse
import json
import logging
import sys

from iatverifier.util import extract_iat_from_cose, recursive_bytes_to_strings
from iatverifier.psa_iot_profile1_token_verifier import PSAIoTProfile1TokenVerifier
from iatverifier.util import recursive_bytes_to_strings
from iatverifier.verifiers import VerifierConfiguration, AttestationTokenVerifier

logger = logging.getLogger('iat-verify')

def main():
    parser = argparse.ArgumentParser(
        description='''
        Validates a signed Initial Attestation Token (IAT), checking
        that the signature is valid, the token contian the required
        fields, and those fields are in a valid format.
        ''')
    parser.add_argument('-k', '--keyfile',
                        help='''
                        Path to a file containing signing key in PEM format.
                         ''')
    parser.add_argument('tokenfile',
                        help='''
                        path to a file containing a signed IAT.
                        ''')
    parser.add_argument('-K', '--keep-going', action='store_true',
                        help='''
                        Do not stop upon encountering a validation error.
                        ''')
    parser.add_argument('-p', '--print-iat', action='store_true',
                        help='''
                        Print the decoded token in JSON format.
                        ''')
    parser.add_argument('-s', '--strict', action='store_true',
                        help='''
                        Report failure if unknown claim is encountered.
                        ''')
    parser.add_argument('-m', '--method', choices=['sign', 'mac'], default='sign',
                        help='''
                        Specify how this token is wrapped -- whether Sign1Message or
                        Mac0Message COSE structure is used.
                        ''')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    config = VerifierConfiguration(keep_going=args.keep_going, strict=args.strict)
    verifier = PSAIoTProfile1TokenVerifier.get_verifier(config)
    if args.method == 'mac':
        verifier.method = AttestationTokenVerifier.SIGN_METHOD_MAC0
        verifier.cose_alg = AttestationTokenVerifier.COSE_ALG_HS256

    try:
        raw_iat = extract_iat_from_cose(args.keyfile, args.tokenfile, verifier)
        if args.keyfile:
            print('Signature OK')
    except ValueError as e:
        logger.error('Could not extract IAT from COSE:\n\t{}'.format(e))
        sys.exit(1)

    try:
        token = verifier.decode_and_validate_iat(raw_iat)
        if not verifier.seen_errors:
            print('Token format OK')
    except ValueError as e:
        logger.error('Could not validate IAT:\n\t{}'.format(e))
        sys.exit(1)

    if args.print_iat:
        print('Token:')
        json.dump(recursive_bytes_to_strings(token, in_place=True),
                  sys.stdout, indent=4)
        print('')
