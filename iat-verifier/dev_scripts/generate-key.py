#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Copyright (c) 2019, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import argparse

from ecdsa import SigningKey, NIST256p, NIST384p
from pycose.keys import EC2Key, CoseKey
from ecdsa.curves import curve_by_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='generate an ECDSA key')

    parser.add_argument('outfile', type=str, help='output file')
    parser.add_argument('--crv', type=str, help='ECDSA curve',
                        choices=[NIST256p.name, NIST384p.name], default='NIST256p')
    parser.add_argument('--fmt', type=str, help='key format',
                        choices=['PEM', 'COSE'], default='PEM')

    args = parser.parse_args()

    sk = SigningKey.generate(curve_by_name(args.crv))

    pem_key = sk.to_pem().decode('utf-8')

    if args.fmt == 'PEM':
        o = pem_key
    elif args.fmt == 'COSE':
        o = CoseKey.from_pem_private_key(pem_key)

    with open(args.outfile, 'wb') as wfh:
        wfh.write(o.encode())
