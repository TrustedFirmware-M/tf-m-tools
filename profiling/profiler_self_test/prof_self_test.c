/*
 * Copyright (c) 2022, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include "prof_common.h"
#include "prof_intf_s.h"
#include "prof_hal.h"

#define TEST_TOPIC_ID           (0x1)
#define TEST_CP_ID_BASE         (0x200)
#define TEST_LOG_INTERVAL       (0x11)
#define TEST_LOOPS              (20)

void prof_sleep(uint16_t tick);
bool prof_test_timing(void);

uint32_t g_sim_tick = 0;

int main(void)
{
    if (!prof_init()) {
        printf("prof_init failed\r\n");
        return -1;
    }

    printf("TF-M profiler Self-Test starts:\r\n");

    if (prof_test_timing()) {
        printf("TF-M profiler Self-Test passed!\r\n");
    } else {
        printf("TF-M profiler Self-Test failed!\r\n");
    }

    printf("TF-M profiler Self-Test ends\r\n");

    return 0;
}

/* Initialize the timer/cycle counter hardware for profiling */
bool prof_hal_init(void)
{
    g_sim_tick = 0;
    return true;
}

/* Interface for retrieving the timer/cycle count */
uint32_t prof_hal_get_count(void)
{
    return g_sim_tick;
}

void prof_sleep(uint16_t tick)
{
    g_sim_tick += tick;
}

bool prof_test_timing(void)
{
    uint32_t val = 0;
    uint32_t tag = 0;
    g_sim_tick = 0;

    printf("------Start: Timing Log Test------\r\n");
    for (uint32_t i = 0; i < TEST_LOOPS; i++) {
        prof_sleep(TEST_LOG_INTERVAL);
        PROF_TIMING_LOG(TEST_CP_ID_BASE + i, TEST_TOPIC_ID);
    }

    printf("------Verify Data By TOPIC------\r\n");
    for (uint32_t i = 0; i < TEST_LOOPS; i++) {
        if (i == 0) {
            if (!PROF_FETCH_DATA_BY_TOPIC_START(&tag, &val, TEST_TOPIC_ID)) {
                printf("No dataset matches the search condition!\r\n");
                return false;
            }
        } else {
            if (!PROF_FETCH_DATA_BY_TOPIC_CONTINUE(&tag, &val, TEST_TOPIC_ID)) {
                printf("No dataset matches the search condition!\r\n");
                return false;
            }
        }

        printf("tag: 0x%x, type: 0x%x, cali_idx: 0x%x\r\n", tag,
               PROF_GET_TYPE_FROM_TAG(tag),
               PROF_GET_CALI_IDX_FROM_TAG(tag));
        printf("topic_id: 0x%x, checkpoint_id: 0x%x\r\n",
               PROF_GET_TOPIC_ID_FROM_TAG(tag), PROF_GET_CP_ID_FROM_TAG(tag));

        if (PROF_GET_TYPE_FROM_TAG(tag) != PROF_TYPE_TIMING_LOG) {
            printf("Tag wrong: type, expect: 0x%x, actual: 0x%x\r\n",
                  PROF_TYPE_TIMING_LOG, PROF_GET_TYPE_FROM_TAG(tag));
            return false;
        }

        if (PROF_GET_TOPIC_ID_FROM_TAG(tag) != TEST_TOPIC_ID) {
            printf("Tag wrong: topic_id, expect: 0x%x, actual: 0x%x\r\n",
                  TEST_TOPIC_ID, PROF_GET_TOPIC_ID_FROM_TAG(tag));
            return false;
        }

        if (PROF_GET_CP_ID_FROM_TAG(tag) != (TEST_CP_ID_BASE + i)) {
            printf("Tag wrong: cp_id, expect: 0x%x, actual: 0x%x\r\n",
                  (TEST_CP_ID_BASE + i), PROF_GET_CP_ID_FROM_TAG(tag));
            return false;
        }

        if (val != (TEST_LOG_INTERVAL * (i + 1))) {
            printf("Test data wrong @ %d, expect: %d, actual: %d\r\n", i,
                TEST_LOG_INTERVAL * (i + 1), val);
            return false;
        } else {
            printf("Test data correct @ %d, expect: %d, actual: %d\r\n", i,
                TEST_LOG_INTERVAL * (i + 1), val);
        }
    }

    printf("------Verify Data By Checkpoint------\r\n");
    for (uint32_t i = 0; i < TEST_LOOPS; i++) {
        if (i == 0) {
            if (!PROF_FETCH_DATA_START(&tag, &val, TEST_CP_ID_BASE + i,
                                       TEST_TOPIC_ID)) {
                printf("No dataset matches the search condition!\r\n");
                return false;
            }
        } else {
            if (!PROF_FETCH_DATA_CONTINUE(&tag, &val, TEST_CP_ID_BASE + i,
                                          TEST_TOPIC_ID)) {
                printf("No dataset matches the search condition!\r\n");
                return false;
            }
        }

        printf("tag: 0x%x, type: 0x%x, cali_idx: 0x%x\r\n", tag,
               PROF_GET_TYPE_FROM_TAG(tag),
               PROF_GET_CALI_IDX_FROM_TAG(tag));
        printf("topic_id: 0x%x, checkpoint_id: 0x%x\r\n",
               PROF_GET_TOPIC_ID_FROM_TAG(tag), PROF_GET_CP_ID_FROM_TAG(tag));

        if (PROF_GET_TYPE_FROM_TAG(tag) != PROF_TYPE_TIMING_LOG) {
            printf("Tag wrong: type, expect: 0x%x, actual: 0x%x\r\n",
                  PROF_TYPE_TIMING_LOG, PROF_GET_TYPE_FROM_TAG(tag));
            return false;
        }

        if (PROF_GET_TOPIC_ID_FROM_TAG(tag) != TEST_TOPIC_ID) {
            printf("Tag wrong: topic_id, expect: 0x%x, actual: 0x%x\r\n",
                  TEST_TOPIC_ID, PROF_GET_TOPIC_ID_FROM_TAG(tag));
            return false;
        }

        if (PROF_GET_CP_ID_FROM_TAG(tag) != (TEST_CP_ID_BASE + i)) {
            printf("Tag wrong: cp_id, expect: 0x%x, actual: 0x%x\r\n",
                  (TEST_CP_ID_BASE + i), PROF_GET_CP_ID_FROM_TAG(tag));
            return false;
        }

        if (val != (TEST_LOG_INTERVAL * (i + 1))) {
            printf("Test data wrong @ %d, expect: %d, actual: %d\r\n", i,
                TEST_LOG_INTERVAL * (i + 1), val);
            return false;
        } else {
            printf("Test data correct @ %d, expect: %d, actual: %d\r\n", i,
                TEST_LOG_INTERVAL * (i + 1), val);
        }
    }

    printf("------End: Timing Log Test------\r\n");

    return true;
}
