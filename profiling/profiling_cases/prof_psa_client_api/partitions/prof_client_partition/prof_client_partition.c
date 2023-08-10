/*
 * Copyright (c) 2023, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include "secure_prof_psa_client_api.h"
#include "psa/service.h"
#include "psa_manifest/prof_client_partition.h"

int32_t prof_client_init(void)
{
    secure_prof_psa_client_api();
    return 0;
}

psa_status_t secure_client_dummy_sfn(const psa_msg_t *msg)
{
    /* Not expected to be called by anyone */
    psa_panic();

    return 0;
}
