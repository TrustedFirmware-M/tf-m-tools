{#
 # Copyright (c) 2024 Arm Limited. All Rights Reserved.
 #
 # SPDX-License-Identifier: BSD-3-Clause
 #
 # ---------------------------------------------------------------------------
 #
 # For information on template variables, see ns_test.c.
#}

target_sources(tfm_test_suite_extra_ns
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/ns_test.c
        {% for test in tests -%}
        ${CMAKE_CURRENT_SOURCE_DIR}/{{test.c_file_name}}
        {% endfor %}
)
