/*
 * Test purpose:
 *     to remove something that doesn't exist
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
    static uint8_t george_set_data\[\] = "@@002@10@@[a-z\ ]*[\.\?\!]";
    static uint32_t george_set_length = \d+;
    (void)sst_status;
        /* "void" to prevent unused-variable warning, since the variable may not
         * be used in this particular test case.
         */

    crypto_status = psa_crypto_init();
    if (crypto_status != PSA_SUCCESS) {
        TEST_FAIL("Could not initialize Crypto.");
        return;
    }

    TEST_LOG("Test to remove something that doesn't exist\n");


    /* PSA calls to test: */
    /\* Creating SST asset "george," with data "@@002@10@@...". \*/
    sst_status = psa_ps_set\(@@@001@@@, george_set_length, george_set_data,
                            PSA_STORAGE_FLAG_[A-Z_]+\);
    if (sst_status != PSA_SUCCESS) {
        TEST_FAIL("psa_ps_set() expected PSA_SUCCESS.");
        return;
    }
    sst_status = psa_ps_remove\(\d+\);
    if (sst_status != PSA_ERROR_DOES_NOT_EXIST) {
        TEST_FAIL("psa_ps_remove() expected PSA_ERROR_DOES_NOT_EXIST.");
        return;
    }


    /* Removing assets left over from testing: */
    sst_status = psa_ps_remove\(@@@001@@@\);
    if (sst_status != PSA_SUCCESS) {
        TEST_FAIL("Failed to tear down an SST asset upon test completion.");
        return;
    }

    /* Test completed */
    ret->val = TEST_PASSED;
}
