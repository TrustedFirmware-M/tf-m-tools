/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef SECURITY_CALL_HPP
#define SECURITY_CALL_HPP

#include <string>
#include <vector>
#include <iosfwd>

#include "find_or_create_asset.hpp"
#include "psa_call.hpp"

class tf_fuzz_info;

using namespace std;

class hash_call : public security_call
{
public:
    // Data members:  // (low value in hiding these behind setters and getters)
    // Methods:
        bool copy_call_to_asset (void);
        bool copy_asset_to_call (void);
        void fill_in_prep_code (void);
        void fill_in_command (void);
        /* Hash checks are different from the rest in that there's a single "call" --
           not a PSA call though -- for all of the assets cited in the template line.
           In other cases, create a single call for each asset cited by the template
           line, but in this case it's a single call for all of them. */
        hash_call (tf_fuzz_info *test_state, long &asset_ser_no,
                    asset_search how_asset_found);  // (constructor)
        ~hash_call (void);

protected:
    // Data members:
    // Methods:
//        void calc_result_code (void);  for *now* keep this in security_call::

private:
    // Data members:
    // Methods:
};

#endif // #ifndef SECURITY_CALL_HPP
