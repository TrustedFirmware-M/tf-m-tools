/*
 * Copyright (c) 2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

/* This file defines information to track regarding variables in the generated test
   code. */

#include <stdlib.h>
#include <string>

#include "find_or_create_asset.hpp"
#include "variables.hpp"
#include "gibberish.hpp"

using namespace std;


/**********************************************************************************
   Methods of class variable_info follow:
**********************************************************************************/

variable_info::variable_info (void)  // (default constructor)
{
    gibberish *gib = new gibberish;

    hash_declared = value_known = false;
    name = "";
    length = 100 + (rand() % 800);
    gib->sentence ((char*) value, (char*) value + length);
        // TODO:  Sizes of random data neesds to be strategized better
    type = psa_asset_type::unknown;
    delete gib;
}

variable_info::variable_info (string var_name, psa_asset_type var_type)
{  // (constructor with known name and type)
    gibberish *gib = new gibberish;

    hash_declared = value_known = false;
    name.assign (var_name);
    length = 100 + (rand() % 800);
    gib->sentence ((char*) value, (char*) value + length);
        // TODO:  Sizes of random data needs to be strategized better
    type = var_type;
    delete gib;
}

variable_info::~variable_info (void)  // (destructor)
{}


/**********************************************************************************
   End of methods of class variable_info.
**********************************************************************************/
