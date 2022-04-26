# -----------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

from iatverifier.verifiers import AttestationTokenVerifier as Verifier
from iatverifier.verifiers import AttestationClaim as Claim
from iatverifier.verifiers import ProfileIdClaim, ClientIdClaim, SecurityLifecycleClaim
from iatverifier.verifiers import ImplementationIdClaim, BootSeedClaim, HardwareVersionClaim
from iatverifier.verifiers import NoMeasurementsClaim, ChallengeClaim
from iatverifier.verifiers import InstanceIdClaim, VerificationServiceClaim, SWComponentsClaim
from iatverifier.verifiers import SWComponentTypeClaim, SwComponentVersionClaim
from iatverifier.verifiers import MeasurementValueClaim, MeasurementDescriptionClaim, SignerIdClaim

class PSAIoTProfile1TokenVerifier(Verifier):
    @staticmethod
    def get_verifier(configuration=None):
        verifier = PSAIoTProfile1TokenVerifier(
            method=Verifier.SIGN_METHOD_SIGN1,
            cose_alg=Verifier.COSE_ALG_ES256,
            configuration=configuration)

        sw_component_claims = [
            (SWComponentTypeClaim, (Claim.OPTIONAL, )),
            (SwComponentVersionClaim, (Claim.OPTIONAL, )),
            (MeasurementValueClaim, (Claim.MANDATORY, )),
            (MeasurementDescriptionClaim, (Claim.OPTIONAL, )),
            (SignerIdClaim, (Claim.RECOMMENDED, )),
        ]

        verifier.add_claims([
            ProfileIdClaim(verifier, Claim.OPTIONAL),
            ClientIdClaim(verifier, Claim.MANDATORY),
            SecurityLifecycleClaim(verifier, Claim.MANDATORY),
            ImplementationIdClaim(verifier, Claim.MANDATORY),
            BootSeedClaim(verifier, Claim.MANDATORY),
            HardwareVersionClaim(verifier, Claim.OPTIONAL),
            SWComponentsClaim(verifier, sw_component_claims, Claim.OPTIONAL),
            NoMeasurementsClaim(verifier, Claim.OPTIONAL),
            ChallengeClaim(verifier, Claim.MANDATORY),
            InstanceIdClaim(verifier, 33, Claim.MANDATORY),
            VerificationServiceClaim(verifier, Claim.OPTIONAL),
        ])
        return verifier

    def check_cross_claim_requirements(self):
        claims = {v.get_claim_key(): v for v in self.claims}

        if SWComponentsClaim.get_claim_key() in claims:
            sw_component_present = claims[SWComponentsClaim.get_claim_key()].verify_count > 0
        else:
            sw_component_present = False

        if NoMeasurementsClaim.get_claim_key() in claims:
            no_measurement_present = claims[NoMeasurementsClaim.get_claim_key()].verify_count > 0
        else:
            no_measurement_present = False

        if not sw_component_present and not no_measurement_present:
            self.error('Invalid IAT: no software measurements defined and '
                  'NO_MEASUREMENTS claim is not present.')

