/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include "data_blocks.hpp"
#include "psa_asset.hpp"
#include "psa_call.hpp"


/**********************************************************************************
   Methods of class psa_asset follow:
**********************************************************************************/

void psa_asset::set_name (string set_val)
{
    asset_info.name_specified = true;
    asset_name.assign (set_val);
}

string psa_asset::get_name (void)
{
    return asset_name;
}

bool psa_asset::simulate (void) {
    return false;
        // by default, assume that nothing changed; derived classes may override.
}

psa_asset::psa_asset (void)  // (default constructor)
{
    asset_info.asset_ser_no = unique_id_counter++;
}


psa_asset::~psa_asset (void)
{
    return;  // just to have something to pin a breakpoint onto
}

/**********************************************************************************
   End of methods of class psa_asset.
**********************************************************************************/
