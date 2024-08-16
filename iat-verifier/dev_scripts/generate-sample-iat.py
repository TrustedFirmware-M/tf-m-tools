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

token_map = {
  InstanceIdClaim.get_claim_key(): GUID,
  ImplementationIdClaim.get_claim_key(): ORIGIN,
  ChallengeClaim.get_claim_key(): NONCE,
  ClientIdClaim.get_claim_key(): 2,
  SecurityLifecycleClaim.get_claim_key(): 0x1000,
  ProfileIdClaim.get_claim_key(): 'http://example.com',
  BootSeedClaim.get_claim_key(): BOOT_SEED,
  SWComponentsClaim.get_claim_key(): [
        {
            # bootloader
            SWComponentTypeClaim.get_claim_key(): 'BL',
            SignerIdClaim.get_claim_key(): SIGNER_ID,
            SwComponentVersionClaim.get_claim_key(): '3.4.2',
            MeasurementValueClaim.get_claim_key(): MEASUREMENT,
            MeasurementDescriptionClaim.get_claim_key(): 'TF-M_SHA256MemPreXIP',
        },
        {
            # mod1
            SWComponentTypeClaim.get_claim_key(): 'M1',
            SignerIdClaim.get_claim_key(): SIGNER_ID,
            SwComponentVersionClaim.get_claim_key(): '3.4.2',
            MeasurementValueClaim.get_claim_key(): MEASUREMENT,
        },
        {
            # mod2
            SWComponentTypeClaim.get_claim_key(): 'M2',
            SignerIdClaim.get_claim_key(): SIGNER_ID,
            SwComponentVersionClaim.get_claim_key(): '3.4.2',
            MeasurementValueClaim.get_claim_key(): MEASUREMENT,
        },
        {
            # mod3
            SWComponentTypeClaim.get_claim_key(): 'M3',
            SignerIdClaim.get_claim_key(): SIGNER_ID,
            SwComponentVersionClaim.get_claim_key(): '3.4.2',
            MeasurementValueClaim.get_claim_key(): MEASUREMENT,
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
    with open(outfile, 'wb') as wfh:
        convert_map_to_token(token_map, verifier, wfh,
            name_as_key=False, parse_raw_value=False)
