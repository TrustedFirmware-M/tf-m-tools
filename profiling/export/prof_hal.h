/*
 * Copyright (c) 2021-2022, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */
#ifndef __PROF_HAL_H__
#define __PROF_HAL_H__

#include <stdint.h>

/* Platform must implement these functions */

#ifdef __cplusplus
extern "C" {
#endif

/* Initialize the timer/cycle counter hardware for profiling */
bool prof_hal_init(void);

/* Interface for retrieving the timer/cycle count */
uint32_t prof_hal_get_count(void);

#ifdef __cplusplus
}
#endif

#endif /* __PROF_HAL_H__ */
