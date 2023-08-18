/*
 * Copyright (c) 2023, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include "tfm_ns_profiling.h"
#include "non_secure_prof_psa_client_api.h"

/*
 * The entry of TF-M NS profiling.
 *
 * NOTE: This is a thread function for CMISI RTOS2. It could NOT be called by
 * other functions.
 */
void tfm_ns_profiling(void *args)
{
    non_secure_prof_psa_client_api();

    /* End of profiling */
    for (;;) {
    }
}
