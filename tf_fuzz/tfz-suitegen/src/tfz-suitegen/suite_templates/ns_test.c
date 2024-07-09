{#
/*
 * Copyright (c) 2024 Arm Limited. All Rights Reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 * ---------------------------------------------------------------------------
 *
 * Each generated test is placed in an individual .c file placed in the same
 * directory as this file. This file registers the tests as a suite, filling in
 * the name, description, and function pointer for each test.
 *
 * VARIABLES: the tests variable provides a list of tests, each with
 * the following values:
 *
 *     - fn_name: the name of the function that implements the test, suitable
 *         for use as a function pointer.
 *
 *     - name: the display name of the test, used in tester output.
 *
 *     - description: a small description of the test, used in tester output.
 *         This is derived from the purpose given in the test specification.
 *
 *     - c_file_name: name of the generated C file, relative to this directory
 *         (including file extension). Used in CMake templates.
 *
 * ---------------------------------------------------------------------------
 *  TEST FUNCTIONS: Test functions use the following format, as required by the
 *   regression tester:
 *
 *      void ns_test(struct test_result_t *ret) {
 *          ret->val = TEST_PASSED;
 *      }
 */
#}

#include "extra_ns_tests.h"

{% for test in tests -%}
extern void {{ test.fn_name }} (struct test_result_t *ret);
{% endfor %}

static struct test_t plat_ns_t[] = {
    {% for test in tests -%}
    {&{{test.fn_name}}, "{{test.name}}", "{{test.description}}"},
    {% endfor %}
};

void register_testsuite_extra_ns_interface(struct test_suite_t *p_test_suite)
{
    uint32_t list_size;

    list_size = (sizeof(plat_ns_t) /
                 sizeof(plat_ns_t[0]));

    set_testsuite("TF-Fuzz Non-Secure interface tests",plat_ns_t, list_size, p_test_suite);
}
