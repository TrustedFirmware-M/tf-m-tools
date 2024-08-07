/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include <string>
#include <vector>

#include "data_blocks.hpp"
#include "find_or_create_asset.hpp"
#include "psa_call.hpp"
#include "security_call.hpp"

class tf_fuzz_info;



/**********************************************************************************
   Methods of class hash_call follow:
**********************************************************************************/

hash_call::hash_call (tf_fuzz_info *test_state,    // (constructor)
                          long &call_ser_no,
                          asset_search how_asset_found)
                             : security_call(test_state, call_ser_no, how_asset_found)
{
    call_description = "hash call";
}
hash_call::~hash_call (void)
{
    // Nothing further to delete.
    return;  // just to have something to pin a breakpoint onto
}

bool hash_call::copy_call_to_asset (void)
{
    // The assets are not directly involved in this call.
    return true;
}

bool hash_call::copy_asset_to_call (void)
{
    // The assets are not directly involved in this call.
    return true;
}

/* Note:  These functions are overridden in all subclasses, but they still need to be
          defined, or the linker gives the error "undefined reference to `vtable... */
void hash_call::fill_in_prep_code (void)
{
    // No prep code for hash comparisons.
}

void hash_call::fill_in_command (void)
{
    if (asset_info.asset_name_vector.size() > 1) {  // nothing to compare with less than 2
        // Fill in preceding comment:
        // Fill in the hash-comparison code itself:
        for (auto outer = asset_info.asset_name_vector.begin();
             outer < asset_info.asset_name_vector.end();
             ++outer) {
            for (auto inner = outer+1;
                 inner < asset_info.asset_name_vector.end();
                 ++inner) {
                call_code.append ("    if (" + *outer + "_hash == " + *inner + "_hash) {\n");
                call_code.append (  "        TEST_FAIL(\"Probable data leak between assets "
                                  + *outer + " and " + *inner + ".\\n\");\n");
                call_code.append ("        return;\n");
                call_code.append ("    }\n");
                // TODO:  Pull this from boilerplate!!
            }
        }
    } else {
        call_code.assign ("    /* Cannot compare hashes;  only one asset specified. */\n");

    }
}

/**********************************************************************************
   End of methods of class hash_call.
**********************************************************************************/
