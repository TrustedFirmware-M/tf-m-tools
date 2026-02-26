#-------------------------------------------------------------------------------
# Copyright (c) 2020-2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

cmake_minimum_required(VERSION 3.21)

add_custom_target(docs)

project("Trusted Firmware M Tools. Documentation" LANGUAGES)

set(SPHINXCFG_SOURCE_PATH ${CMAKE_CURRENT_SOURCE_DIR})
set(SPHINXCFG_CONFIG_PATH ${CMAKE_CURRENT_SOURCE_DIR})
set(SPHINXCFG_OUTPUT_PATH ${CMAKE_CURRENT_BINARY_DIR}/html)

################################## SPHINX ######################################

file(GLOB_RECURSE SPHINXCFG_DOC_FILES ${SPHINXCFG_SOURCE_PATH}/*.rst ${SPHINXCFG_SOURCE_PATH}/*.md)

add_custom_target(tfm_tools_docs_userguide_html ALL
    COMMAND sphinx-build -b html -j 1 -c ${SPHINXCFG_CONFIG_PATH} ${SPHINXCFG_SOURCE_PATH} "${SPHINXCFG_OUTPUT_PATH}"
    WORKING_DIRECTORY ${SPHINXCFG_SOURCE_PATH}
    DEPENDS ${SPHINXCFG_DOC_FILES}
)
add_dependencies(docs tfm_tools_docs_userguide_html)
