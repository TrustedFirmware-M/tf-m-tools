/*
 * Test purpose:
 *     to set an offset on psa_ps_get()
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
    static uint8_t whoNose_set_data\[\] = "@@012@10@@[a-z\ ]*[\.\?\!]";
    static uint32_t whoNose_set_length = \d+;
    static uint8_t whoNose_act_data\[2048\] = "[A-Z][a-z\ ]*[\.\?\!]";
    static size_t whoNose_act_length = \d+;
    (void)sst_status;
        /* "void" to prevent unused-variable warning, since the variable may not
         * be used in this particular test case.
         */

    crypto_status = psa_crypto_init();
    if (crypto_status != PSA_SUCCESS) {
        TEST_FAIL("Could not initialize Crypto.");
        return;
    }

    TEST_LOG("Test to set an offset on psa_ps_get()\n");


    /* PSA calls to test: */
    /\* Creating SST asset "whoNose," with data "@@012@10@@...". \*/
    sst_status = psa_ps_set\(@@@001@@@, whoNose_set_length, whoNose_set_data,
                            PSA_STORAGE_FLAG_[A-Z_]+\);
    if (sst_status != PSA_SUCCESS) {
        TEST_FAIL("psa_ps_set() expected PSA_SUCCESS.");
        return;
    }
    sst_status = psa_ps_get\(@@@001@@@, 10, \d+, whoNose_act_data,
                            &whoNose_act_length);
    if (sst_status != PSA_SUCCESS) {
        TEST_FAIL("psa_ps_get() expected PSA_SUCCESS.");
        return;
    }
    TEST_LOG(whoNose_act_data);


    /* Removing assets left over from testing: */
    sst_status = psa_ps_remove\(@@@001@@@\);
    if (sst_status != PSA_SUCCESS) {
        TEST_FAIL("Failed to tear down an SST asset upon test completion.");
        return;
    }

    /* Test completed */
    ret->val = TEST_PASSED;
}