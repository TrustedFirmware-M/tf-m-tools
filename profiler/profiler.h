/*
 * Copyright (c) 2022, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef __PROFILER_H__
#define __PROFILER_H__

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Dataset structure */
struct prof_dataset {
    uint32_t tag;
    uint32_t count;
};

#ifdef __cplusplus
}
#endif

#endif /* __PROFILER_H__ */
