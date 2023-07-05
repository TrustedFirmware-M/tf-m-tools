/*
 * Copyright (c) 2021-2022, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include <stdint.h>
#include <stdbool.h>
#include "profiler.h"
#include "prof_common.h"
#include "prof_if_s.h"
#include "prof_hal.h"

#define DIFF(a, b) (((a) > (b)) ? ((a) - (b)) : ((b) - (a)))
#define DO_CALI(diff, cali) (((diff) > (cali)) ? ((diff) - (cali)) : 0)

/* Database */
static struct prof_dataset prof_database[PROF_DB_MAX] = {0};
static uint32_t prof_db_idx = 0;
static uint32_t prof_dump_idx = 0;

/* Global calibration data */
static uint32_t g_prof_cali_data[PROF_MAX_CALI_SETS] = {0};

/* Initialize the database for performance data */
static bool prof_data_init(void);

/* Save the a performance data set to the database */
static void prof_data_save(uint32_t tag, uint32_t count);

/* Get the data by matching the tag pattern */
static bool prof_get_data_by_tag(uint32_t *tag, uint32_t *data,
                                 uint32_t tag_pattern, uint32_t tag_mask);

/* Initialize the hardware, database, etc. */
bool prof_init(void)
{
    if(!prof_data_init()) {
        return false;
    }

    if(!prof_hal_init()) {
        return false;
    }

    return true;
}

/* Log the timing of a checkpoint */
uint32_t prof_timing_cp(uint32_t tag)
{
    uint32_t count = prof_hal_get_count();

    prof_data_save(tag, count);

    return count;
}

/*
 * Optional. It's for caculating the cost of profiler. For SPE only.
 * This function is wrappered by the macros. Should not be called directly.
 */
void prof_calibrate(uint32_t index, uint32_t rounds, uint32_t cali_data)
{
    uint32_t saved_rounds;
    volatile uint32_t start, end;

    /*
     * set `rounds` to 0 to manually specify the calibration data from the
     * input parameter.
     */
    if (rounds == 0) {
        g_prof_cali_data[index] = cali_data;
        return;
    }

    /* Save the start point */
    start = PROF_TIMING_CALIBRATE();
    saved_rounds = rounds;

    /*
     * To get the cost of one profiler function call, we do a few rounds dummy
     * actions. Then get the total cost.
     * "total cost" / "rounds" = the average cost of one function call
     */
    while (rounds--) {
        end = PROF_TIMING_CALIBRATE();
    }

    /* Support increase/decrease way of the counter */
    g_prof_cali_data[index] = ((start > end)?
            (start - end) : (end - start)) / saved_rounds;
}

/* Interface for getting the calibration data */
uint32_t prof_get_cali_value(uint32_t index)
{
    if (index >= PROF_MAX_CALI_SETS) {
        return 0;
    } else {
        return g_prof_cali_data[index];
    }
}

/* Initialize the database for performance data */
static bool prof_data_init(void)
{
    prof_db_idx = 0;
    return true;
}

/* Save the performance data set to the database */
static void prof_data_save(uint32_t tag, uint32_t count)
{
    if (prof_db_idx >= PROF_DB_MAX) {
        return;
    }

    prof_database[prof_db_idx].tag = tag;
    prof_database[prof_db_idx].count = count;

    /* Increase the index if it's not calibration data */
    if (PROF_GET_TYPE_FROM_TAG(tag) != PROF_TYPE_TIMING_CALI) {
        prof_db_idx++;
    }
}

/* Get the datas by matching the tag pattern */
static bool prof_get_data_by_tag(uint32_t *tag, uint32_t *data,
                                 uint32_t tag_pattern, uint32_t tag_mask)
{
    /* Look for the first dataset which matches the tag pattern */
    for (; prof_dump_idx < prof_db_idx; prof_dump_idx++) {
        if((prof_database[prof_dump_idx].tag & tag_mask) == tag_pattern) {
            *tag = prof_database[prof_dump_idx].tag;
            *data = prof_database[prof_dump_idx].count;
            prof_dump_idx++;
            return true;
        }
    }

    return false;
}

/* Search the data from the beginning of the database */
bool prof_get_data_start(uint32_t *tag, uint32_t *data, uint32_t tag_pattern,
                        uint32_t tag_mask)
{
    /* Reset the search index */
    prof_dump_idx = 0;
    return prof_get_data_by_tag(tag, data, tag_pattern, tag_mask);

}

/* Search the data from the last found dataset */
bool prof_get_data_continue(uint32_t *tag, uint32_t *data, uint32_t tag_pattern,
                            uint32_t tag_mask)
{
    return prof_get_data_by_tag(tag, data, tag_pattern, tag_mask);
}

/* Data analysis operations */
uint32_t prof_data_diff(uint32_t tag_pattern_a, uint32_t tag_pattern_b)
{
    uint32_t diff = 0;
    uint32_t dataA, dataB, tagA, tagB;
    uint32_t cali = 0;

    /* Reset the search index */
    prof_dump_idx = 0;
    if (!prof_get_data_by_tag(&tagA, &dataA, tag_pattern_a, PROF_MASK_FULL_TAG)) {
        return 0;
    }
    if (!prof_get_data_by_tag(&tagB, &dataB, tag_pattern_b, PROF_MASK_FULL_TAG)) {
        return 0;
    }

    diff = DIFF(dataA, dataB);
    /*
     * When two tags have same cali index, tag_pattern_b cali is same with
     * tag_pattern_a cali and they are the precise values. When two tags have
     * different cali indexes, it cannot get the precise cali value but
     * tag_pattern_b cali is more precise.
     */
    cali = PROF_GET_CALI_VALUE_FROM_TAG(tag_pattern_b);

    /* Do the calibration */
    return DO_CALI(diff, cali);
}

uint32_t prof_data_diff_min(uint32_t tag_pattern_a, uint32_t tag_pattern_b)
{
    uint32_t diff = 0, min = UINT32_MAX;
    uint32_t dataA, dataB, tagA, tagB;
    uint32_t cali = 0;

    /* Reset the search index */
    prof_dump_idx = 0;
    cali = PROF_GET_CALI_VALUE_FROM_TAG(tag_pattern_b);
    while (1) {
        if (!prof_get_data_by_tag(&tagA, &dataA, tag_pattern_a, PROF_MASK_FULL_TAG)) {
            break;
        }
        if (!prof_get_data_by_tag(&tagB, &dataB, tag_pattern_b, PROF_MASK_FULL_TAG)) {
            break;
        }
        diff = DO_CALI(DIFF(dataA, dataB), cali);
        min = (diff < min) ? diff : min;
    }

    return min;
}

uint32_t prof_data_diff_max(uint32_t tag_pattern_a, uint32_t tag_pattern_b)
{
    uint32_t diff = 0, max = 0;
    uint32_t dataA, dataB, tagA, tagB;
    uint32_t cali = 0;

    /* Reset the search index */
    prof_dump_idx = 0;
    cali = PROF_GET_CALI_VALUE_FROM_TAG(tag_pattern_b);
    while (1) {
        if (!prof_get_data_by_tag(&tagA, &dataA, tag_pattern_a, PROF_MASK_FULL_TAG)) {
            break;
        }
        if (!prof_get_data_by_tag(&tagB, &dataB, tag_pattern_b, PROF_MASK_FULL_TAG)) {
            break;
        }
        diff = DO_CALI(DIFF(dataA, dataB), cali);
        max = (diff > max) ? diff : max;
    }

    return max;
}

uint32_t prof_data_diff_avg(uint32_t tag_pattern_a, uint32_t tag_pattern_b)
{
    uint32_t diff = 0, sum = 0, num = 0;
    uint32_t dataA, dataB, tagA, tagB;
    uint32_t cali = 0;

    /* Reset the search index */
    prof_dump_idx = 0;
    cali = PROF_GET_CALI_VALUE_FROM_TAG(tag_pattern_b);
    while (1) {
        if (!prof_get_data_by_tag(&tagA, &dataA, tag_pattern_a, PROF_MASK_FULL_TAG)) {
            break;
        }
        if (!prof_get_data_by_tag(&tagB, &dataB, tag_pattern_b, PROF_MASK_FULL_TAG)) {
            break;
        }
        diff = DO_CALI(DIFF(dataA, dataB), cali);
        num++;
        sum += diff;
    }

    if (num == 0) {
        return 0;
    } else {
        return sum/num;
    }
}

#ifndef PROF_SELF_TEST
/* For non-secure side */
__profiler_secure_gateway_attributes__
void prof_ns_set_cali_value(uint32_t cali)
{
   prof_calibrate(PROF_CALI_IDX_NS, 0, cali);
}

__profiler_secure_gateway_attributes__
uint32_t prof_timing_cp_veneer(uint32_t tag)
{
    return prof_timing_cp(tag);
}

__profiler_secure_gateway_attributes__
uint32_t prof_get_cali_value_veneer(uint32_t index)
{
    return prof_get_cali_value(index);
}

__profiler_secure_gateway_attributes__
bool prof_get_data_start_veneer(uint32_t *tag, uint32_t *data,
                            uint32_t tag_pattern, uint32_t tag_mask)
{
    return prof_get_data_start(tag, data, tag_pattern, tag_mask);
}

__profiler_secure_gateway_attributes__
bool prof_get_data_continue_veneer(uint32_t *tag, uint32_t *data,
                            uint32_t tag_pattern, uint32_t tag_mask)
{
    return prof_get_data_continue(tag, data, tag_pattern, tag_mask);
}

__profiler_secure_gateway_attributes__
uint32_t prof_data_diff_veneer(uint32_t tag_pattern_a, uint32_t tag_pattern_b)
{
    return prof_data_diff(tag_pattern_a, tag_pattern_b);
}

__profiler_secure_gateway_attributes__
uint32_t prof_data_diff_min_veneer(uint32_t tag_pattern_a, uint32_t tag_pattern_b)
{
    return prof_data_diff_min(tag_pattern_a, tag_pattern_b);
}

__profiler_secure_gateway_attributes__
uint32_t prof_data_diff_max_veneer(uint32_t tag_pattern_a, uint32_t tag_pattern_b)
{
    return prof_data_diff_max(tag_pattern_a, tag_pattern_b);
}

__profiler_secure_gateway_attributes__
uint32_t prof_data_diff_avg_veneer(uint32_t tag_pattern_a, uint32_t tag_pattern_b)
{
    return prof_data_diff_avg(tag_pattern_a, tag_pattern_b);
}

#endif
