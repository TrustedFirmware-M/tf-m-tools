/*
 * Copyright (c) 2021-2022, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */
#include <stdint.h>
#include <stddef.h>
#include "prof_common.h"
#include "prof_if_ns.h"

/* This file should be compiled with the non-secure side software */

/*
 * This calibrate function needs to be called from NS side.
 * `rounds` specifies how many timing logging calls are invoked for calculating
 * the calibration data. In theory, the more rounds the more accurate. But it
 * doesn't make sense to do too many rounds.
 * If `rounds` is 0, then reset the NS calibration data to 0.
 */
void prof_calibrate_ns(uint32_t rounds)
{
    uint32_t saved_rounds, cali;
    volatile uint32_t start, end;

    /* set `rounds` to 0 to reset the calibration data to 0 */
    if (rounds == 0) {
        prof_ns_set_cali_value(0);
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
    cali = ((start > end) ? (start - end) : (end - start)) / saved_rounds;
    prof_ns_set_cali_value(cali);
}
