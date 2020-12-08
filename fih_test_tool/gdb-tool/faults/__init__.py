# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from .skip import skip_fault
from .register import register_fault

fault_types = [
            [register_fault(reg="r" + str(x)) for x in range(16)],
            [register_fault(reg="r" + str(x), val=0) for x in range(16)],
            [skip_fault(size=x * 2) for x in range(8)],
        ]

# Flatten the list
fault_types = sum(fault_types, [])
