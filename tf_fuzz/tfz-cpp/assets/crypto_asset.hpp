/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef CRYPTO_ASSET_HPP
#define CRYPTO_ASSET_HPP

#include <vector>
#include <cstdint>

#include "data_blocks.hpp"
#include "psa_asset.hpp"

class key_asset;

using namespace std;

class crypto_asset : public psa_asset
{
public:
    // Data members:
        key_policy_info policy;
    // Methods:
        crypto_asset (void);  // (constructor)
        ~crypto_asset (void);

protected:
    // Data members:
    // Methods:

private:
    // Data members:
    // Methods:
};

class policy_asset : public crypto_asset
{
public:
    // Data members:
        vector<key_asset*> keys;  // keys that use this policy
    // Methods:
        policy_asset (void);  // (constructor)
        ~policy_asset (void);

protected:
    // Data members:
    // Methods:

private:
    // Data members:
    // Methods:
};

class key_asset : public crypto_asset
{
public:
    // Methods:
        bool set_key_id (int id_n);  // checks key-ID value, returns true==success
        key_asset (void);  // (constructor)
        ~key_asset (void);

protected:
    // Data members:
        uint64_t key_id;
    // Methods:

private:
    // Data members:
    // Methods:
};

#endif  // CRYPTO_ASSET_HPP
