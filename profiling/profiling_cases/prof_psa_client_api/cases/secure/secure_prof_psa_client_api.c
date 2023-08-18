/*
 * Copyright (c) 2023, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include "secure_prof_psa_client_api.h"
#include "tfm_sp_log.h"
#include "prof_intf_s.h"

#define PROFILING_AVERAGE_DIFF(psa_api_name, cp_start, cp_end) \
        LOG_INFFMT("secure %s average is %d CPU cycles\r\n", psa_api_name, \
                   PROF_DATA_DIFF_AVG(cp_start, PSA_API_TOPIC, cp_end, PSA_API_TOPIC))

void secure_prof_psa_client_api()
{
    psa_handle_t handle;
    psa_status_t status;
    uint16_t i = 0;

    PROF_DO_CALIBRATE(PROF_CALIBRATION_ROUND);

    for (i = 0; i < TEST_LOOP_CNT; i++) {
        PROF_TIMING_LOG(CONNECT_CP_START, PSA_API_TOPIC);
        handle = psa_connect(PROFILING_SERVICE_SID, PROFILING_SERVICE_VERSION);
        PROF_TIMING_LOG(CONNECT_CP_END, PSA_API_TOPIC);

        if (!PSA_HANDLE_IS_VALID(handle)) {
            LOG_ERRFMT("PSA connect fail!");
            return;
        }

        PROF_TIMING_LOG(CALL_CP_START, PSA_API_TOPIC);
        status = psa_call(handle, PSA_IPC_CALL, NULL, 0, NULL, 0);
        PROF_TIMING_LOG(CALL_CP_END, PSA_API_TOPIC);

        if (status != PSA_SUCCESS) {
            LOG_ERRFMT("PSA call fail!");
            return;
        }

        PROF_TIMING_LOG(CLOSE_CP_START, PSA_API_TOPIC);
        psa_close(handle);
        PROF_TIMING_LOG(CLOSE_CP_END, PSA_API_TOPIC);

        /* Test stateless PSA call interface. */
        PROF_TIMING_LOG(STATELESS_CALL_CP_START, PSA_API_TOPIC);
        status = psa_call(PROFILING_STATELESS_SERVICE_HANDLE, PSA_IPC_CALL, NULL, 0, NULL, 0);
        PROF_TIMING_LOG(STATELESS_CALL_CP_END, PSA_API_TOPIC);

        if (status != PSA_SUCCESS) {
            LOG_ERRFMT("PSA stateless call fail!");
            return;
        }
    }

    PROFILING_AVERAGE_DIFF("psa_connect", CONNECT_CP_START, CONNECT_CP_END);
    PROFILING_AVERAGE_DIFF("psa_call", CALL_CP_START, CALL_CP_END);
    PROFILING_AVERAGE_DIFF("psa_close", CLOSE_CP_START, CLOSE_CP_END);
    PROFILING_AVERAGE_DIFF("psa_call stateless", STATELESS_CALL_CP_START, STATELESS_CALL_CP_END);
}
