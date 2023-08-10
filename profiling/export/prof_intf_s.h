/*
 * Copyright (c) 2021-2022, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef __PROF_INTF_S_H__
#define __PROF_INTF_S_H__

/* This file defines all API that should be called by secure side */

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include "prof_common.h"

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Topic based timing logging
 */
#define PROF_TIMING_LOG(cp_id, topic_id)                                \
        prof_timing_cp(                                                 \
        PROF_MAKE_TIMING_TAG((cp_id), (topic_id), PROF_CALI_IDX_S,      \
        PROF_TYPE_TIMING_LOG))

/*
 * Secure side can call this macro to do/redo calibration
 * Suggest to do/redo calibration before running the profiling. It's because the
 * latency introduced by the profiler may be changed in the system lifecycle.
 * For example, enable caches, change CPU frequency, etc.
 * 'rounds' sets how many rounds executed for the calibration. In theory, "more
 * rounds" is more accurate.
 * Set `rounds` to `0` to reset the calibration value to 0.
 */
#define PROF_DO_CALIBRATE(rounds)     prof_calibrate(                   \
        PROF_CALI_IDX_S, rounds, 0)

/* Get the calibration value from the tag. */
#define PROF_GET_CALI_VALUE_FROM_TAG(tag) prof_get_cali_value(          \
                                          PROF_GET_CALI_IDX_FROM_TAG(tag))

/*
 * Get data, not calibrated.
 * The calibrated counter (diff) is
 * "current_counter" - "previous_counter" - "current_cali_value"
 * "current_cali_value" = PROF_GET_CALI_VALUE_FROM_TAG(current_tag)
 *
 * "tag" and "data" are outputs which should be pointers.
 * "tag" is used to get calibration data.
 */
#define PROF_FETCH_DATA_START(tag, data, cp, topic)                     \
        prof_get_data_start(tag, data,                                  \
        PROF_MAKE_TIMING_TAG(cp, topic, 0, 0), PROF_MASK_TOPIC_CP)

#define PROF_FETCH_DATA_CONTINUE(tag, data, cp, topic)                  \
        prof_get_data_continue(tag, data,                               \
        PROF_MAKE_TIMING_TAG(cp, topic, 0, 0), PROF_MASK_TOPIC_CP)

#define PROF_FETCH_DATA_BY_TOPIC_START(tag, data, topic)                \
        prof_get_data_start(tag, data,                                  \
        PROF_MAKE_TIMING_TAG(0, topic, 0, 0), PROF_MASK_TOPIC)

#define PROF_FETCH_DATA_BY_TOPIC_CONTINUE(tag, data, topic)             \
        prof_get_data_continue(tag, data,                               \
        PROF_MAKE_TIMING_TAG(0, topic, 0, 0), PROF_MASK_TOPIC)

/* Data analysis with calibration */
#define PROF_DATA_DIFF(cp_a, topic_a, cp_b, topic_b)                    \
        prof_data_diff(PROF_MAKE_TIMING_TAG((cp_a), (topic_a),          \
                                            PROF_CALI_IDX_S,            \
                                            PROF_TYPE_TIMING_LOG),      \
                       PROF_MAKE_TIMING_TAG((cp_b), (topic_b),          \
                                            PROF_CALI_IDX_S,            \
                                            PROF_TYPE_TIMING_LOG))

#define PROF_DATA_DIFF_MIN(cp_a, topic_a, cp_b, topic_b)                \
        prof_data_diff_min(PROF_MAKE_TIMING_TAG((cp_a), (topic_a),      \
                                            PROF_CALI_IDX_S,            \
                                            PROF_TYPE_TIMING_LOG),      \
                           PROF_MAKE_TIMING_TAG((cp_b), (topic_b),      \
                                            PROF_CALI_IDX_S,            \
                                            PROF_TYPE_TIMING_LOG))

#define PROF_DATA_DIFF_MAX(cp_a, topic_a, cp_b, topic_b)                \
        prof_data_diff_max(PROF_MAKE_TIMING_TAG((cp_a), (topic_a),      \
                                            PROF_CALI_IDX_S,            \
                                            PROF_TYPE_TIMING_LOG),      \
                           PROF_MAKE_TIMING_TAG((cp_b), (topic_b),      \
                                            PROF_CALI_IDX_S,            \
                                            PROF_TYPE_TIMING_LOG))

#define PROF_DATA_DIFF_AVG(cp_a, topic_a, cp_b, topic_b)                \
        prof_data_diff_avg(PROF_MAKE_TIMING_TAG((cp_a), (topic_a),      \
                                            PROF_CALI_IDX_S,            \
                                            PROF_TYPE_TIMING_LOG),      \
                           PROF_MAKE_TIMING_TAG((cp_b), (topic_b),      \
                                            PROF_CALI_IDX_S,            \
                                            PROF_TYPE_TIMING_LOG))

#ifdef __cplusplus
}
#endif

#endif /* __PROF_INTF_S_H__ */
