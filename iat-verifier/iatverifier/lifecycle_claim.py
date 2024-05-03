# -----------------------------------------------------------------------------
# Copyright (c) 2022-2024, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

from abc import ABC, abstractmethod
from iatverifier.attest_token_verifier import AttestationClaim

class GenericLifecycleClaim(AttestationClaim):

    @classmethod
    def parse_raw(cls, raw_value):
        try:
            int_value = int(raw_value, 16)
        except ValueError:
            # It is not a hex number. Try to decode known text values
            pass
        for text, min, max in cls.SL_VALUES:
            if raw_value.startswith(text.lower()):
                raw_value = raw_value[len(text):]
            else:
                continue
            if len(raw_value) == 0:
                return min
            assert raw_value.startswith("_0x")
            raw_value = raw_value[3:]
            int_value = int(raw_value, 16)
            assert(min <= int_value <= max)
            return int_value
        assert False

    @classmethod
    def get_formatted_value(cls, value):
        for text, min, max in cls.SL_VALUES:
            if min <= value <= max:
                return f"{text}_{value:04x}".lower()
        return f"INVALID_{value:04x}"

    def verify(self, token_item):
        self._check_type(self.get_claim_name, token_item.value, int)
        value_valid = False
        for _, min, max in self.SL_VALUES:
            if min <= token_item.value <= max:
                value_valid = True
                break
        if not value_valid:
            msg = 'Invalid Lifecycle claim "0x{:02x}"'
            self.verifier.error(msg.format(token_item.value))
