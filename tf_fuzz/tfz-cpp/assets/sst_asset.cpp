/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include "data_blocks.hpp"
#include "sst_asset.hpp"



/**********************************************************************************
   Methods of class sst_asset follow:
**********************************************************************************/

bool sst_asset::set_uid (uint64_t uid)
{
    /* TODO:  What are the limits upon UIDs?  I don't necessarily not want to be
              able to set an illegal value, but if it is illegal, I might want to
              set some flag appropriately to generate expected results. */
    asset_info.set_id_n (uid);
    return true;
}

sst_asset::sst_asset (void)  // (default constructor)
{
    return;  // just to have something to pin a breakpoint onto
}


sst_asset::~sst_asset (void)  // (destructor)
{
    return;  // just to have something to pin a breakpoint onto
}

/**********************************************************************************
   End of methods of class sst_asset.
**********************************************************************************/
