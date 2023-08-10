/*
 * Copyright (c) 2023, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include "cmsis.h"

/* Initialize the timer/cycle counter hardware for profiling */
void prof_hal_init(void)
{
    CoreDebug->DEMCR = CoreDebug_DEMCR_TRCENA_Msk; /* Enable DWT. */
    DWT->CTRL        = DWT_CTRL_CYCCNTENA_Msk;     /* Enable CYCCNT. */
    DWT->CYCCNT      = 0x0;                        /* Reset the processor cycle counter. */
}

/* Interface for retrieving the timer/cycle count */
uint32_t prof_hal_get_count(void)
{
    return (uint32_t)DWT->CYCCNT;
}
