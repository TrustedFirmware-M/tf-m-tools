/*
 * Copyright (c) 2021-2022, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef __PROF_IF_NS_H__
#define __PROF_IF_NS_H__

/* This file defines all API that should be called by non-secure side */

#include <stdint.h>
#include <stddef.h>
#include "prof_common.h"

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Topic based timing logging
 */
#define PROF_TIMING_LOG(cp_id, topic_id)                                \
        prof_timing_cp_veneer(                                          \
        PROF_MAKE_TIMING_TAG((cp_id), (topic_id), PROF_CALI_IDX_NS,     \
        PROF_TYPE_TIMING_LOG))

/*
 * Get the timing value for further calibration
 * The difference with checkpoint is that the calibration item doesn't increase
 * the index in database. So, the calibration item can be overwritten by other
 * items. The reason of keeping writing calibration data into database is that
 * we want to make a full cycle of saving an item into the database to more
 * accurately reflect the latency.
 */
#define PROF_TIMING_CALIBRATE()         prof_timing_cp_veneer(          \
        PROF_MAKE_TIMING_TAG(0, 0, 0,                                   \
        PROF_TYPE_TIMING_CALI))

/*
 * Non-secure side can call this macro to do/redo calibration
 * Suggest to do/redo calibration before running the profiling. It's because the
 * latency introduced by the profiler may be changed in the system lifecycle.
 * For example, enable caches, change CPU frequency, etc.
 * 'rounds' sets how many rounds executed for the calibration. In theory, "more
 * rounds" is more accurate.
 * Set `rounds` to `0` to reset the calibration value to 0.
 */
#define PROF_DO_CALIBRATE(rounds)     prof_calibrate_ns(rounds)

/*
 * Get the calibration value from the tag.
 * The calibrated counter is
 * "current_counter" - "previous_counter" - "current_cali_value"
 * "current_cali_value" = PROF_GET_CALI_VALUE_FROM_TAG(current_tag)
 */
#define PROF_GET_CALI_VALUE_FROM_TAG(tag) prof_get_cali_value_veneer(   \
                                          PROF_GET_CALI_IDX_FROM_TAG(tag))

/* Get data */
#define PROF_FETCH_DATA_START(tag, data, tag_pattern, tag_mask)         \
        prof_get_data_start_veneer(tag, data, tag_pattern, tag_mask)

#define PROF_FETCH_DATA_CONTINUE(tag, data, tag_pattern, tag_mask)      \
        prof_get_data_continue_veneer(tag, data, tag_pattern, tag_mask)

#define PROF_FETCH_DATA_BY_TOPIC_START(tag, data, topic)                \
        prof_get_data_start_veneer(tag, data,                           \
        PROF_MAKE_TIMING_TAG(0, topic, 0, 0), PROF_MASK_TOPIC)

#define PROF_FETCH_DATA_BY_TOPIC_CONTINUE(tag, data, topic)             \
        prof_get_data_continue_veneer(tag, data,                        \
        PROF_MAKE_TIMING_TAG(0, topic, 0, 0), PROF_MASK_TOPIC)

#define PROF_FETCH_DATA_BY_CP_START(tag, data, cp, topic)               \
        prof_get_data_start_veneer(tag, data,                           \
        PROF_MAKE_TIMING_TAG(cp, topic, 0, 0), PROF_MASK_TOPIC_CP)

#define PROF_FETCH_DATA_BY_CP_CONTINUE(tag, data, cp, topic)            \
        prof_get_data_continue_veneer(tag, data,                        \
        PROF_MAKE_TIMING_TAG(cp, topic, 0, 0), PROF_MASK_TOPIC_CP)

void prof_calibrate_ns(uint32_t rounds);

#ifdef __cplusplus
}
#endif

#endif /* __PROF_IF_NS_H__ */
