/*
 * Copyright (c) 2021-2022, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef __PROF_COMMON_H__
#define __PROF_COMMON_H__

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Supported maximum items in database */
#ifndef PROF_DB_MAX
#define PROF_DB_MAX         2048
#endif

/*
 * The database is consisted of "items".
 * Each item has 32-bit "tag" followed by 32-bit data.
 *
 * The tag is the metadata of the value in the item. The lower 4-bit of the tag
 * identifies the "type" of the item.
 * -------------------------
 * |Type defined field|Type|
 * -------------------------
 *     28-bit          4-bit
 * Currently, only "timing" types are supported.
 *
 * Generic tag format of the timing types
 * ------------------------------------------
 * |Checkpoint ID|Topic ID| Cali |Res. |Type|
 * ------------------------------------------
 *     16-bit       8-bit   2-bit 2-bit 4-bit
 * Checkpiont ID: Identifies the point logged the timing
 * Topic ID: Topic is used to group a set of checkpoints.
 * Cali: Specifies the calibration value index used for this item. The
 *          calibration value was measured by calling calibration functions.
 * Res.: Reserved
 */

/* Define the type of the performance data tag */
#define PROF_TYPE_TIMING_CALI           (0x0)
#define PROF_TYPE_TIMING_LOG            (0x1)

/* Calibration data index */
#define PROF_CALI_IDX_S                 (0x0)
#define PROF_CALI_IDX_NS                (0x3)
#define PROF_MAX_CALI_SETS              (4)

/* Masks */
#define PROF_MASK_CP                    (0xffff0000)
#define PROF_MASK_TOPIC                 (0x0000ff00)
#define PROF_MASK_TOPIC_CP              (PROF_MASK_CP | PROF_MASK_TOPIC)
#define PROF_MASK_FULL_TAG              (0xffffffff)
#define PROF_MASK_NONE                  (0)

#define PROF_MAKE_TIMING_TAG(cp_id, topic_id, cali, type)               \
                            ((((cp_id) & 0xffff) << 16)                 \
                            | (((topic_id) & 0xff) << 8)                \
                            | (((cali) & 0x3) << 6)                     \
                            | ((type) & 0xf))

#define PROF_GET_TYPE_FROM_TAG(tag)             ((tag) & 0xf)
#define PROF_GET_CALI_IDX_FROM_TAG(tag)         (((tag) >> 6) & 0x3)
#define PROF_GET_TOPIC_ID_FROM_TAG(tag)         (((tag) >> 8) & 0xff)
#define PROF_GET_CP_ID_FROM_TAG(tag)            (((tag) >> 16) & 0xffff)

/* Initialize the hardware, database, etc. */
bool prof_init(void);

/* Optional. It's for caculating the cost of profiler */
void prof_calibrate(uint32_t index, uint32_t rounds, uint32_t cali_data);
void prof_ns_set_cali_value(uint32_t cali);
uint32_t prof_get_cali_value(uint32_t index);

/* Log timing of a checkpoint. */
uint32_t prof_timing_cp(uint32_t tag);

/* Dump data */
bool prof_get_data_start(uint32_t *tag, uint32_t *data, uint32_t tag_pattern,
                         uint32_t tag_mask);
bool prof_get_data_continue(uint32_t *tag, uint32_t *data, uint32_t tag_pattern,
                            uint32_t tag_mask);
/* Data analysis */
uint32_t prof_data_diff(uint32_t tag_pattern_a, uint32_t tag_pattern_b);
uint32_t prof_data_diff_min(uint32_t tag_pattern_a, uint32_t tag_pattern_b);
uint32_t prof_data_diff_max(uint32_t tag_pattern_a, uint32_t tag_pattern_b);
uint32_t prof_data_diff_avg(uint32_t tag_pattern_a, uint32_t tag_pattern_b);

/* Non-secure side veneer */
uint32_t prof_timing_cp_veneer(uint32_t tag);
uint32_t prof_get_cali_value_veneer(uint32_t index);
bool prof_get_data_start_veneer(uint32_t *tag, uint32_t *data,
                                uint32_t tag_pattern, uint32_t tag_mask);
bool prof_get_data_continue_veneer(uint32_t *tag, uint32_t *data,
                                   uint32_t tag_pattern, uint32_t tag_mask);
uint32_t prof_data_diff_veneer(uint32_t tag_pattern_a, uint32_t tag_pattern_b);
uint32_t prof_data_diff_min_veneer(uint32_t tag_pattern_a, uint32_t tag_pattern_b);
uint32_t prof_data_diff_max_veneer(uint32_t tag_pattern_a, uint32_t tag_pattern_b);
uint32_t prof_data_diff_avg_veneer(uint32_t tag_pattern_a, uint32_t tag_pattern_b);

#if !defined(__ARMCC_VERSION) && !defined(__ICCARM__)
/*
 * GNUARM requires noclone attribute to protect gateway function symbol from
 * being renamed and cloned
 */
#define __profiler_secure_gateway_attributes__ \
        __attribute__((cmse_nonsecure_entry, noclone))
#else
#define __profiler_secure_gateway_attributes__ \
        __attribute__((cmse_nonsecure_entry))
#endif /* !__ARMCC_VERSION */

#ifdef __cplusplus
}
#endif

#endif /* __PROF_COMMON_H__ */
