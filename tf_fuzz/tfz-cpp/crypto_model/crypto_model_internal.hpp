/* Copyright (c) 2024 Arm Limited. All Rights Reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

// crypto_model_internal.hpp
#pragma once

/* Internal functions for the crypto model */

#include <map>
#include <string>
#include <vector>

namespace crypto_model {
class key_type;
class algorithm;
}

namespace crypto_model::internal {

    // helper functions for init_crypto_model
    // these are in the header file so that they can be declared as friends.
    void define_algorithm(std::string name, bool is_hash_algorithm,
                          bool requires_hash);

    void define_key_type(std::string name,
                         std::vector<uint> allowed_key_sizes_bits,
                         uint max_key_size_bits, uint min_key_size_bits);
}
