/*
 * Copyright (c) 2023-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include "cmsis.h"

/*
 * From CoreSight version 3.0 onwards, implementation of the Software lock
 * mechanism that is controlled by LAR and LSR is deprecated and their
 * definitions may not be available.
 * Explicitly define them here.
 */
#define DWT_LAR (uint32_t *)(DWT_BASE + 0xFB0UL)
#define DWT_LSR (uint32_t *)(DWT_BASE + 0xFB4UL)

#define LSR_SLI_Pos  0U /*!< LSR, SLI: Software Lock Implemented */
#define LSR_SLI_Mask (1UL /* << LSR_SLI_Pos */)

/* Initialize the timer/cycle counter hardware for profiling */
void prof_hal_init(void)
{
    DCB->DEMCR       = DCB_DEMCR_TRCENA_Msk; /* Enable DWT. */

    if((*DWT_LSR & LSR_SLI_Mask) > 0) {
        /* Software Lock is implemented, enable write access to DWT unit */
        *DWT_LAR = 0xC5ACCE55;
    }

    DWT->CTRL        = DWT_CTRL_CYCCNTENA_Msk;     /* Enable CYCCNT. */
    DWT->CYCCNT      = 0x0;                        /* Reset the processor cycle counter. */
}

/* Interface for retrieving the timer/cycle count */
uint32_t prof_hal_get_count(void)
{
    return (uint32_t)DWT->CYCCNT;
}
