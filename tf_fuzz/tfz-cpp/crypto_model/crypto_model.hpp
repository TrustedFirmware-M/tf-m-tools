/* Copyright (c) 2024 Arm Limited. All Rights Reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

// crypto_model.hpp
#pragma once

#include <string>
#include <vector>
#include "crypto_model_internal.hpp"

/*
 * `crypto_model` contains information about crypto key types, algorithms, and
 * attributes, and their compatabilities with each-other.
 */
namespace crypto_model {

// forward declarations
class key_type;
class algorithm;

algorithm& get_algorithm(std::string);
key_type& get_key_type(std::string);

algorithm& get_random_hash_algorithm();

algorithm& get_random_algorithm();

key_type& get_random_key_type();

uint get_random_key_size();

//! Initialises the crypto model.
void init_crypto_model();


// Classes to hold data.
class algorithm {
    friend void crypto_model::init_crypto_model();
    friend void crypto_model::internal::define_algorithm(std::string,bool,bool);

public:
    algorithm();
    ~algorithm();

    std::string get_string();

    // Gets the header value form of the algorithm, with a random hash function
    // filled in if needed.
    std::string get_string_with_hash();
    bool is_enabled();

    bool is_hash_algorithm();
    bool requires_hash();

    bool valid_for_key_type(key_type&);
    key_type& random_valid_key_type();

private:

    std::string name;
    std::vector<std::string> allowed_key_types;
    bool requires_hash_flag;
    bool is_hash_algorithm_flag;
    bool enabled=true;
};

class key_type {
    friend void crypto_model::init_crypto_model();
    friend void crypto_model::internal::define_key_type(std::string, std::vector<uint>, uint, uint);

public:
    key_type();
    ~key_type();

    std::string get_string();
    bool is_enabled();

    bool is_allowed_algorithm(algorithm&);
    algorithm& random_allowed_algorithm();
    bool is_valid_key_size(uint size);
    uint get_random_valid_key_size();


private:

    std::string name;

    // If non empty, the key size must be one of the values in this vector.
    std::vector<uint> allowed_key_sizes_bits;
    uint max_key_size_bits;
    uint min_key_size_bits;

    std::vector<std::string> allowed_algorithms;

    bool enabled=true;
};

} // namespace crypto_model
