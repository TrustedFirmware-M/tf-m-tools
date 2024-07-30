/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef SST_ASSET_HPP
#define SST_ASSET_HPP

#include <stdint.h>
#include <string>
#include <iosfwd>

#include "psa_asset.hpp"

using namespace std;

class sst_asset : public psa_asset
{
public:  // (low value in hiding these behind setters and getters)
    // Data members:
    // Methods:
        bool set_uid (uint64_t uid);  // checks input UID value, returns true==success
        void set_literal_data (string literal_data);
           // if literal data, this sets both "data" string and "data_length"
        sst_asset (void);  // (constructor)
        ~sst_asset (void);

protected:
    // Data members:
    // Methods:

private:
    // Data members:
    // Methods:
};

#endif  // SST_ASSET_HPP
