/*
 * Copyright (c) 2023, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include "cmsis_compiler.h"
#include "non_secure_prof_psa_client_api.h"
#include "prof_log.h"
#include "tfm_plat_ns.h"

/*
 * Fixes with Armclang compiler.
 */
#if defined(__ARMCC_VERSION)
#if (__ARMCC_VERSION == 6110004)
/*
 * Workaround needed for a bug in Armclang 6.11, more details at:
 * http://www.keil.com/support/docs/4089.htm
 */
__attribute__((section(".gnu.linkonce")))
#endif

/* Avoids the semihosting issue */
#if (__ARMCC_VERSION >= 6010050)
__asm("  .global __ARM_use_no_argv\n");
#endif
#endif

/*
 * Platform peripherals and devices initialization. Can be overridden for
 * platform specific initialization.
 *
 * return 0 if the initialization succeeds
 */
__WEAK int32_t tfm_ns_platform_init(void)
{
    stdio_init();

    return 0;
}

/*
 * main() function.
 */
#ifndef __GNUC__
__attribute__((noreturn))
#endif
int main(void)
{
    if (tfm_ns_platform_init() != 0) {
        /* Avoid undefined behavior if platform init failed */
        while(1);
    }

    LOG_MSG("Non-Secure system starting...\r\n");

    /* The entry of TF-M NS profiling cases. */
    non_secure_prof_psa_client_api();

    /* Output EOT char for test environments like FVP. */
    LOG_MSG("\x04");

    /* End of profiling */
    for (;;) {
    }
}
