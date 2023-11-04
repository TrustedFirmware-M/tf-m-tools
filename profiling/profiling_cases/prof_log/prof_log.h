/*
 * Copyright (c) 2023, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef __PROF_LOG_H__
#define __PROF_LOG_H__

#include "prof_log_raw.h"
#include "uart_stdout.h"

/* Functions and macros in this file is for 'thread mode' usage. */

#define LOG_MSG(...) prof_log_printf(__VA_ARGS__)

#define LOG_ERRMSG(...) prof_log_printf(__VA_ARGS__)

#endif /* __PROF_LOG_H__ */
