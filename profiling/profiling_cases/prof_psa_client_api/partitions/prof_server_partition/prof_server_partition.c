/*
 * Copyright (c) 2023, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include "psa/service.h"
#include "psa_manifest/prof_server_partition.h"

psa_status_t profiling_service_sfn(const psa_msg_t* msg)
{
    switch (msg->type) {
    case PSA_IPC_CONNECT:
        break;
    case PSA_IPC_CALL:
        break;
    case PSA_IPC_DISCONNECT:
        break;
    default:
        return PSA_ERROR_PROGRAMMER_ERROR;
        break;
    }

    return PSA_SUCCESS;
}

psa_status_t profiling_stateless_service_sfn(const psa_msg_t* msg)
{
    switch (msg->type) {
    case PSA_IPC_CALL:
        break;
    default:
        return PSA_ERROR_PROGRAMMER_ERROR;
        break;
    }

    return PSA_SUCCESS;
}
