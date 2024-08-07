/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef SST_CALL_HPP
#define SST_CALL_HPP

#include <string>
#include <vector>
#include <cstdint>
#include <iosfwd>

#include "find_or_create_asset.hpp"
#include "psa_call.hpp"

class tf_fuzz_info;

using namespace std;

class sst_set_call : public sst_call
{
public:
    // Data members:
    // Methods:
        bool copy_call_to_asset (void);
        bool copy_asset_to_call (void);
        void fill_in_prep_code (void);
        void fill_in_command (void);
        sst_set_call (tf_fuzz_info *test_state, long &asset_ser_no,
                      asset_search how_asset_found);  // (constructor)
        ~sst_set_call (void);

protected:
    // Data members:
    // Methods:

private:
    // Data members:
    // Methods:
};


class sst_get_call : public sst_call
{
public:
    // Data members:
        uint32_t offset;
        uint32_t data_length;
        string data_var_name;
    // Methods:
        bool copy_call_to_asset (void);
        bool copy_asset_to_call (void);
        void fill_in_prep_code (void);
        void fill_in_command (void);
        sst_get_call (tf_fuzz_info *test_state, long &asset_ser_no,
                      asset_search how_asset_found);  // (constructor)
        ~sst_get_call (void);

protected:
    // Data members:
    // Methods:

private:
    // Data members:
    // Methods:
};

class sst_remove_call : public sst_call
{
public:
    // Data members:
    // Methods:
        bool copy_call_to_asset (void);
        bool copy_asset_to_call (void);
        void fill_in_prep_code (void);
        void fill_in_command (void);
        sst_remove_call (tf_fuzz_info *test_state, long &asset_ser_no,
                      asset_search how_asset_found);  // (constructor)
        ~sst_remove_call (void);

protected:
    // Data members:
    // Methods:

private:
    // Data members:
    // Methods:
};

#endif  // SST_CALL_HPP
