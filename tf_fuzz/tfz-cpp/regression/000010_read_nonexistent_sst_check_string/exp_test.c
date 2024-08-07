/*
 * Test purpose:
 *     to show what happens when you 'read' a non-existent asset
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <stdint.h>

#include "extra_ns_tests.h"
#include "psa/protected_storage.h"
#include "psa/crypto.h"

/* This is not yet right for how to run a test;  need to register tests, etc. */

void test_thread (struct test_result_t *ret) {
    psa_status_t crypto_status;  /* result from Crypto calls */
    psa_status_t sst_status;
    /* Variables (etc.) to initialize and check PSA assets: */
    static uint8_t napoleon_exp_data[] = "this won't work";
    static uint8_t napoleon_act_data\[2048\] = "[A-Z][a-z ]*[\.\?\!]";
    static size_t napoleon_act_length = \d+;
    (void)sst_status;
        /* "void" to prevent unused-variable warning, since the variable may not
         * be used in this particular test case.
         */

    crypto_status = psa_crypto_init();
    if (crypto_status != PSA_SUCCESS) {
        TEST_FAIL("Could not initialize Crypto.");
        return;
    }

    TEST_LOG("Test to show what happens when you 'read' a non-existent asset\n");


    /* PSA calls to test: */
    sst_status = psa_ps_get\(\d+, 0, \d+, napoleon_act_data
                            &napoleon_act_length);
    if (sst_status != PSA_ERROR_DOES_NOT_EXIST) {
        TEST_FAIL("psa_ps_get() expected PSA_ERROR_DOES_NOT_EXIST.");
        return;
    }
    /* Check that the data is correct */

    if \(\d+ > 0 && memcmp\(napoleon_act_data, napoleon_exp_data, napoleon_act_length\) == 0\) {
        TEST_FAIL("Read data should not be equal to result data");
        return;
    }


    /* Removing assets left over from testing: */

    /* Test completed */
    ret->val = TEST_PASSED;
}
