/*
 * Copyright (c) 2023, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef __PROF_PSA_CLIENT_API_COMMON_H__
#define __PROF_PSA_CLIENT_API_COMMON_H__

#include "psa/client.h"
#include "psa_manifest/sid.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Profiling calibration rounds. More rounds, more accurate. */
#define PROF_CALIBRATION_ROUND      50

#define TEST_LOOP_CNT               20

#define PSA_API_TOPIC               0

#define CONNECT_CP_START            0
#define CONNECT_CP_END              1
#define CALL_CP_START               2
#define CALL_CP_END                 3
#define CLOSE_CP_START              5
#define CLOSE_CP_END                6
#define STATELESS_CALL_CP_START     7
#define STATELESS_CALL_CP_END       8

#ifdef __cplusplus
}
#endif

#endif /* __PROF_PSA_CLIENT_API_COMMON_H__ */
