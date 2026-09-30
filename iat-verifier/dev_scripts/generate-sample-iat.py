#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2024, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

"""
Generate a sample token, signing it with the specified key, and writing
the output to the specified file.

This script is deprecated - use ``compile_token`` (see above) instead.
"""
import struct

from iatverifier.util import convert_map_to_token, read_keyfile
from iatverifier.attest_token_verifier import AttestationTokenVerifier
from iatverifier.psa_iot_profile1_token_claims import InstanceIdClaim, ImplementationIdClaim
from iatverifier.psa_iot_profile1_token_claims import ChallengeClaim, ClientIdClaim
from iatverifier.psa_iot_profile1_token_claims import SecurityLifecycleClaim, ProfileIdClaim
from iatverifier.psa_iot_profile1_token_claims import BootSeedClaim, SWComponentsClaim
from iatverifier.psa_iot_profile1_token_claims import SWComponentTypeClaim, SignerIdClaim
from iatverifier.psa_iot_profile1_token_claims import SwComponentVersionClaim
from iatverifier.psa_iot_profile1_token_claims import MeasurementValueClaim
from iatverifier.psa_iot_profile1_token_claims import MeasurementDescriptionClaim
from iatverifier.psa_iot_profile1_token_verifier import PSAIoTProfile1TokenVerifier
from pycose.algorithms import Es256, Es384, Es512

# First byte indicates "GUID"
GUID = b'\x01' + struct.pack('QQQQ', 0x0001020304050607, 0x08090A0B0C0D0E0F,
                             0x1011121314151617, 0x18191A1B1C1D1E1F)
NONCE = struct.pack('QQQQ', 0X0001020304050607, 0X08090A0B0C0D0E0F,
                    0X1011121314151617, 0X18191A1B1C1D1E1F)
ORIGIN = struct.pack('QQQQ', 0X0001020304050607, 0X08090A0B0C0D0E0F,
                     0X1011121314151617, 0X18191A1B1C1D1E1F)
BOOT_SEED = struct.pack('QQQQ', 0X0001020304050607, 0X08090A0B0C0D0E0F,
                        0X1011121314151617, 0X18191A1B1C1D1E1F)
SIGNER_ID = struct.pack('QQQQ', 0X0001020304050607, 0X08090A0B0C0D0E0F,
                        0X1011121314151617, 0X18191A1B1C1D1E1F)
MEASUREMENT = struct.pack('QQQQ', 0X0001020304050607, 0X08090A0B0C0D0E0F,
                          0X1011121314151617, 0X18191A1B1C1D1E1F)

def create_token_map(verifier):
    """Build the sample using claim instances owned by the verifier."""
    claims = {}

    def collect_claims(container):
        for claim_instance in container._get_contained_claims():
            claims[type(claim_instance)] = claim_instance
            if hasattr(claim_instance, '_get_contained_claims'):
                collect_claims(claim_instance)

    def claim(claim_type):
        return claims[claim_type]

    collect_claims(verifier.claims)

    return {
        claim(InstanceIdClaim).get_claim_key(): GUID,
        claim(ImplementationIdClaim).get_claim_key(): ORIGIN,
        claim(ChallengeClaim).get_claim_key(): NONCE,
        claim(ClientIdClaim).get_claim_key(): 2,
        claim(SecurityLifecycleClaim).get_claim_key(): 0x1000,
        claim(ProfileIdClaim).get_claim_key(): 'http://example.com',
        claim(BootSeedClaim).get_claim_key(): BOOT_SEED,
        claim(SWComponentsClaim).get_claim_key(): [
        {
            # bootloader
            claim(SWComponentTypeClaim).get_claim_key(): 'BL',
            claim(SignerIdClaim).get_claim_key(): SIGNER_ID,
            claim(SwComponentVersionClaim).get_claim_key(): '3.4.2',
            claim(MeasurementValueClaim).get_claim_key(): MEASUREMENT,
            claim(MeasurementDescriptionClaim).get_claim_key(): 'TF-M_SHA256MemPreXIP',
        },
        {
            # mod1
            claim(SWComponentTypeClaim).get_claim_key(): 'M1',
            claim(SignerIdClaim).get_claim_key(): SIGNER_ID,
            claim(SwComponentVersionClaim).get_claim_key(): '3.4.2',
            claim(MeasurementValueClaim).get_claim_key(): MEASUREMENT,
        },
        {
            # mod2
            claim(SWComponentTypeClaim).get_claim_key(): 'M2',
            claim(SignerIdClaim).get_claim_key(): SIGNER_ID,
            claim(SwComponentVersionClaim).get_claim_key(): '3.4.2',
            claim(MeasurementValueClaim).get_claim_key(): MEASUREMENT,
        },
        {
            # mod3
            claim(SWComponentTypeClaim).get_claim_key(): 'M3',
            claim(SignerIdClaim).get_claim_key(): SIGNER_ID,
            claim(SwComponentVersionClaim).get_claim_key(): '3.4.2',
            claim(MeasurementValueClaim).get_claim_key(): MEASUREMENT,
        },
        ],
    }


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} KEYFILE OUTFILE')
        sys.exit(1)
    keyfile = sys.argv[1]
    outfile = sys.argv[2]

    key = read_keyfile(keyfile,
                       method=AttestationTokenVerifier.SIGN_METHOD_SIGN1)
    verifier = PSAIoTProfile1TokenVerifier(signing_key=key,
                                           method=AttestationTokenVerifier.SIGN_METHOD_SIGN1,
                                           cose_alg=Es256,
                                           configuration=None)
    token_map = create_token_map(verifier)
    with open(outfile, 'wb') as wfh:
        convert_map_to_token(token_map, verifier, wfh,
            name_as_key=False, parse_raw_value=False)
