/* Copyright (c) 2024 Arm Limited. All Rights Reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "crypto_model.hpp"
#include <algorithm>
#include <cmath>
#include <map>
#include <numeric>
#include <stdexcept>

using namespace crypto_model;
using namespace crypto_model::internal;
using namespace std;

std::map<std::string,crypto_model::key_type> key_types;
std::map<std::string,crypto_model::algorithm> algorithms;
std::vector<std::string> hash_algorithms;

// From PSA_VENDOR_RSA_MAX_KEY_BITS
const uint RSA_KEY_MAX_SIZE = 4096;

// From PSA_VENDOR_RSA_MIN_KEY_BITS
const uint RSA_KEY_MIN_SIZE = 1024;

// From PSA_MAX_KEY_BITS
const uint MAX_KEY_SIZE = 0xfff8;

// Size cannot be 0
const uint MIN_KEY_SIZE = 1;

const std::vector<std::pair<string, string>> key_type_allowed_with_algorithm = {
    {"PSA_KEY_TYPE_AES","PSA_ALG_CBC_MAC"},
    {"PSA_KEY_TYPE_AES","PSA_ALG_CMAC"},
    {"PSA_KEY_TYPE_AES","PSA_ALG_CTR"},
    {"PSA_KEY_TYPE_AES","PSA_ALG_CFB"},
    {"PSA_KEY_TYPE_AES","PSA_ALG_OFB"},
    {"PSA_KEY_TYPE_AES","PSA_ALG_CBC_NO_PADDING"},
    {"PSA_KEY_TYPE_AES","PSA_ALG_CBC_PKCS7"},
    {"PSA_KEY_TYPE_AES","PSA_ALG_ECB_NO_PADDING"},
    {"PSA_KEY_TYPE_AES","PSA_ALG_CCM"},
    {"PSA_KEY_TYPE_AES","PSA_ALG_GCM"},

    {"PSA_KEY_TYPE_ARC4","PSA_ALG_STREAM_CIPHER"},

    {"PSA_KEY_TYPE_ARIA","PSA_ALG_CBC_MAC"},
    {"PSA_KEY_TYPE_ARIA","PSA_ALG_CMAC"},
    {"PSA_KEY_TYPE_ARIA","PSA_ALG_CTR"},
    {"PSA_KEY_TYPE_ARIA","PSA_ALG_CFB"},
    {"PSA_KEY_TYPE_ARIA","PSA_ALG_OFB"},
    {"PSA_KEY_TYPE_ARIA","PSA_ALG_CBC_NO_PADDING"},
    {"PSA_KEY_TYPE_ARIA","PSA_ALG_CBC_PKCS7"},
    {"PSA_KEY_TYPE_ARIA","PSA_ALG_ECB_NO_PADDING"},
    {"PSA_KEY_TYPE_ARIA","PSA_ALG_CCM"},
    {"PSA_KEY_TYPE_ARIA","PSA_ALG_GCM"},

    {"PSA_KEY_TYPE_CAMELLIA","PSA_ALG_CBC_MAC"},
    {"PSA_KEY_TYPE_CAMELLIA","PSA_ALG_CMAC"},
    {"PSA_KEY_TYPE_CAMELLIA","PSA_ALG_CTR"},
    {"PSA_KEY_TYPE_CAMELLIA","PSA_ALG_CFB"},
    {"PSA_KEY_TYPE_CAMELLIA","PSA_ALG_OFB"},
    {"PSA_KEY_TYPE_CAMELLIA","PSA_ALG_CBC_NO_PADDING"},
    {"PSA_KEY_TYPE_CAMELLIA","PSA_ALG_CBC_PKCS7"},
    {"PSA_KEY_TYPE_CAMELLIA","PSA_ALG_ECB_NO_PADDING"},
    {"PSA_KEY_TYPE_CAMELLIA","PSA_ALG_CCM"},
    {"PSA_KEY_TYPE_CAMELLIA","PSA_ALG_GCM"},

    {"PSA_KEY_TYPE_CHACHA20","PSA_ALG_STREAM_CIPHER"},
    {"PSA_KEY_TYPE_CHACHA20","PSA_ALG_CHACHA20_POLY1305"},

    {"PSA_KEY_TYPE_DES","PSA_ALG_CMAC"},
    {"PSA_KEY_TYPE_DES","PSA_ALG_CTR"},
    {"PSA_KEY_TYPE_DES","PSA_ALG_CFB"},
    {"PSA_KEY_TYPE_DES","PSA_ALG_OFB"},
    {"PSA_KEY_TYPE_DES","PSA_ALG_CBC_NO_PADDING"},
    {"PSA_KEY_TYPE_DES","PSA_ALG_CBC_PKCS7"},
    {"PSA_KEY_TYPE_DES","PSA_ALG_ECB_NO_PADDING"},

    {"PSA_KEY_TYPE_HMAC","PSA_ALG_HMAC"},

    {"PSA_KEY_TYPE_DERIVE","PSA_ALG_HKDF"},
    {"PSA_KEY_TYPE_DERIVE","PSA_ALG_TLS12_PRF"},
    {"PSA_KEY_TYPE_DERIVE","PSA_ALG_TLS12_PSK_TO_MS"},

    {"PSA_KEY_TYPE_PASSWORD_HASH","PSA_ALG_PBKDF2_HMAC"},
    {"PSA_KEY_TYPE_PASSWORD_HASH","PSA_ALG_PBKDF2_AES_CMAC_PRF_128"},

    {"PSA_KEY_TYPE_PASSWORD","PSA_ALG_PBKDF2_HMAC"},
    {"PSA_KEY_TYPE_PASSWORD","PSA_ALG_PBKDF2_AES_CMAC_PRF_128"},

    {"PSA_KEY_TYPE_PEPPER","PSA_ALG_PBKDF2_HMAC"},
    {"PSA_KEY_TYPE_PEPPER","PSA_ALG_PBKDF2_AES_CMAC_PRF_128"},

    {"PSA_KEY_TYPE_RAW_DATA","PSA_ALG_HKDF"},
    {"PSA_KEY_TYPE_RAW_DATA","PSA_ALG_TLS12_PRF"},
    {"PSA_KEY_TYPE_RAW_DATA","PSA_ALG_TLS12_PSK_TO_MS"},

    {"PSA_KEY_TYPE_RSA_KEY_PAIR","PSA_ALG_RSA_OAEP"},
    {"PSA_KEY_TYPE_RSA_KEY_PAIR","PSA_ALG_RSA_PKCS1V15_CRYPT"},
    {"PSA_KEY_TYPE_RSA_KEY_PAIR","PSA_ALG_RSA_PKCS1V15_SIGN"},
    {"PSA_KEY_TYPE_RSA_KEY_PAIR","PSA_ALG_RSA_PKCS1V15_SIGN_RAW"},

    {"PSA_KEY_TYPE_RSA_PUBLIC_KEY","PSA_ALG_RSA_OAEP"},
    {"PSA_KEY_TYPE_RSA_PUBLIC_KEY","PSA_ALG_RSA_PKCS1V15_CRYPT"},
    {"PSA_KEY_TYPE_RSA_PUBLIC_KEY","PSA_ALG_RSA_PKCS1V15_SIGN"},
    {"PSA_KEY_TYPE_RSA_PUBLIC_KEY","PSA_ALG_RSA_PKCS1V15_SIGN_RAW"},
};

// See tf-m/lib/ext/mbed-crypto/mbed_crypto_config
const std::vector<string> disabled_key_types = {
    "PSA_KEY_TYPE_ARIA",
    "PSA_KEY_TYPE_ARC4",
    "PSA_KEY_TYPE_CAMELLIA",
    "PSA_KEY_TYPE_CHACHA20",
    "PSA_KEY_TYPE_DES"
};

// See tf-m/lib/ext/mbed-crypto/mbed_crypto_config
const std::vector<string> disabled_algorithms = {
    "PSA_ALG_CBC_MAC",
    "PSA_ALG_CHACHA20_POLY1305",
    "PSA_WANT_ALG_ECB_NO_PADDING",
    "PSA_ALG_MD5",
    "PSA_ALG_OFB",
    "PSA_ALG_SHA_1",
    "PSA_ALG_PBKDF2_HMAC",
    "PSA_ALG_RIPEMD160",
    "PSA_ALG_STREAM_CIPHER",
};

// for readability
const bool doesnt_require_hash = false;
const bool requires_hash = true;
const bool hash_alg = true;
const bool not_hash_alg = false;

void crypto_model::init_crypto_model(void) {

    // Key type definitions.

    define_key_type("PSA_KEY_TYPE_AES", {128, 192, 256}, MAX_KEY_SIZE,
                    MIN_KEY_SIZE);
    define_key_type("PSA_KEY_TYPE_ARC4", {},40,2048);
    define_key_type("PSA_KEY_TYPE_CAMELLIA", {128, 192, 256}, MAX_KEY_SIZE,
                    MIN_KEY_SIZE);
    define_key_type("PSA_KEY_TYPE_CHACHA20", {256}, 256, 256);
    define_key_type("PSA_KEY_TYPE_DES", {64, 128, 192}, MAX_KEY_SIZE,
                    MIN_KEY_SIZE);
    define_key_type("PSA_KEY_TYPE_DERIVE", {}, MAX_KEY_SIZE, MIN_KEY_SIZE);
    define_key_type("PSA_KEY_TYPE_HMAC", {}, MAX_KEY_SIZE, MIN_KEY_SIZE);
    define_key_type("PSA_KEY_TYPE_RAW_DATA", {}, MAX_KEY_SIZE, MIN_KEY_SIZE);
    define_key_type("PSA_KEY_TYPE_PASSWORD", {}, MAX_KEY_SIZE, MIN_KEY_SIZE);
    define_key_type("PSA_KEY_TYPE_PASSWORD_HASH", {}, MAX_KEY_SIZE,
                    MIN_KEY_SIZE);

    define_key_type("PSA_KEY_TYPE_PEPPER", {}, MAX_KEY_SIZE, MIN_KEY_SIZE);
    define_key_type("PSA_KEY_TYPE_RSA_KEY_PAIR", {}, RSA_KEY_MAX_SIZE,
                    RSA_KEY_MIN_SIZE);

    define_key_type("PSA_KEY_TYPE_RSA_PUBLIC_KEY", {}, RSA_KEY_MAX_SIZE,
                    RSA_KEY_MIN_SIZE);

    // Algorithm definitions
    define_algorithm("PSA_ALG_CCM",not_hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_GCM",not_hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_CHACHA20_POLY1305",not_hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_RSA_PKCS1V15_CRYPT",not_hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_RSA_OAEP", not_hash_alg, requires_hash);
    define_algorithm("PSA_ALG_RSA_PKCS1V15_SIGN", not_hash_alg, requires_hash);
    define_algorithm("PSA_ALG_RSA_PKCS1V15_SIGN_RAW", not_hash_alg, doesnt_require_hash);
    define_algorithm("PSA_ALG_STREAM_CIPHER", not_hash_alg, doesnt_require_hash);
    define_algorithm("PSA_ALG_CTR", not_hash_alg, doesnt_require_hash);
    define_algorithm("PSA_ALG_CCM_STAR_NO_TAG", not_hash_alg, doesnt_require_hash);
    define_algorithm("PSA_ALG_CFB", not_hash_alg, doesnt_require_hash);
    define_algorithm("PSA_ALG_OFB", not_hash_alg, doesnt_require_hash);
    define_algorithm("PSA_ALG_ECB_NO_PADDING", not_hash_alg, doesnt_require_hash);
    define_algorithm("PSA_ALG_CBC_NO_PADDING", not_hash_alg, doesnt_require_hash);
    define_algorithm("PSA_ALG_CBC_PKCS7", not_hash_alg, doesnt_require_hash);

    define_algorithm("PSA_ALG_MD5",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_RIPEMD160",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA_1",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA_224",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA_256",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA_384",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA_512",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA_512_224",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA_512_256",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA3_224",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA3_256",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA3_384",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA3_512",hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_SHA3_512",hash_alg,doesnt_require_hash);

    define_algorithm("PSA_ALG_FFDH",not_hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_ECDH",not_hash_alg,doesnt_require_hash);

    define_algorithm("PSA_ALG_HKDF",not_hash_alg,requires_hash);
    define_algorithm("PSA_ALG_TLS12_PRF",not_hash_alg,requires_hash);
    define_algorithm("PSA_ALG_TLS12_PSK_TO_MS",not_hash_alg,requires_hash);
    define_algorithm("PSA_ALG_HKDF_EXTRACT",not_hash_alg,requires_hash);
    define_algorithm("PSA_ALG_HKDF_EXPAND",not_hash_alg,requires_hash);
    define_algorithm("PSA_ALG_TLS12_ECJPAKE_TO_PMS",not_hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_PBKDF2_HMAC",not_hash_alg,requires_hash);
    define_algorithm("PSA_ALG_PBKDF2_AES_CMAC_PRF_128",not_hash_alg,doesnt_require_hash);

    define_algorithm("PSA_ALG_HMAC",not_hash_alg,requires_hash);
    define_algorithm("PSA_ALG_CBC_MAC",not_hash_alg,doesnt_require_hash);
    define_algorithm("PSA_ALG_CMAC",not_hash_alg,doesnt_require_hash);

    // Load the data tables into the right places
    for (auto &kt: disabled_key_types) {
        key_types[kt].enabled = false;
    }

    for (auto &alg: disabled_algorithms) {
        algorithms[alg].enabled = false;
    }

    for (auto pair: key_type_allowed_with_algorithm) {
        key_type &kt = key_types[pair.first];
        algorithm &alg = algorithms[pair.second];

        if (!kt.is_enabled() || !alg.is_enabled()) {
            continue;
        }

        alg.allowed_key_types.push_back(kt.get_string());
        kt.allowed_algorithms.push_back(alg.get_string());
    }

}

void crypto_model::internal::define_key_type(
    std::string name, std::vector<uint> allowed_key_sizes_bits,
    uint max_key_size_bits, uint min_key_size_bits) {

    key_type kt;
    kt.name = name;
    kt.allowed_key_sizes_bits = allowed_key_sizes_bits;
    kt.max_key_size_bits = max_key_size_bits;
    kt.min_key_size_bits = min_key_size_bits;

    key_types[name] = kt;
}

void crypto_model::internal::define_algorithm(std::string name,
                                              bool is_hash_algorithm,
                                              bool requires_hash) {
    algorithm a;
    a.name = name;
    a.is_hash_algorithm_flag = is_hash_algorithm;
    a.requires_hash_flag = requires_hash;

    if (is_hash_algorithm) {
        hash_algorithms.push_back(name);
    }

    algorithms[name] = a;
}

namespace crypto_model {

uint get_random_key_size() {
    int lower = std::floor(MIN_KEY_SIZE/ 8);
    int higher = std::floor(MAX_KEY_SIZE/8);
    return ((rand() % (higher - lower)) + lower) * 8;
}

algorithm& get_algorithm(std::string name) {

    // turn hash algs of form PSA_ALG_FOO(PSA_ALG_BAR) into PSA_ALG_FOO.
    int index = name.find("(");
    if (index != string::npos) {
        name = name.substr(index);
    }

    return algorithms[name];
}


key_type& get_key_type(std::string name) {
    return key_types[name];
}

algorithm& get_random_algorithm() {
    // to randomise:
    //  get random index.
    //  if it is a disabled alg, repeat
    std::vector<int> v(algorithms.size());
    std::iota(v.begin(),v.end(),0);
    std::random_shuffle(v.begin(),v.end());
    auto it = algorithms.begin();
    for (int i:v) {
        auto it = algorithms.begin();
        std::advance(it,i);
        algorithm& alg = it->second;
        if (alg.is_enabled()) {
            return alg;
        }
    }
    throw std::logic_error("No enabled algorithms");
}

key_type& get_random_key_type() {
    // to randomise:
    //  get random index.
    //  if it is a disabled key type, repeat
    std::vector<int> v(key_types.size());
    std::iota(v.begin(),v.end(),0);
    std::random_shuffle(v.begin(),v.end());
    auto it = key_types.begin();
    for (int i:v) {
        auto it = key_types.begin();
        std::advance(it,i);
        key_type& kt = it->second;
        if (kt.is_enabled()) {
            return kt;
        }
    }
    throw std::logic_error("No enabled key types");
}

algorithm& get_random_hash_algorithm() {
    std::random_shuffle(hash_algorithms.begin(),hash_algorithms.end());
    for (int i=0;i<hash_algorithms.size();i++) {
        if (algorithms[hash_algorithms[i]].is_enabled()) {
            return algorithms[hash_algorithms[i]];
        }
    }

    throw std::logic_error("No enabled hash algorithms");
}

algorithm::algorithm() {

};

algorithm::~algorithm() {

};

string algorithm::get_string() {
    return name;
};

bool algorithm::is_enabled() {
    return enabled;
}

std::string algorithm::get_string_with_hash() {
    string out = name;
    if (requires_hash()) {
        algorithm& hash_alg = get_random_hash_algorithm();
        out += "(";
        out += hash_alg.name;
        out += ")";
    }

    return out;
}

bool algorithm::valid_for_key_type(key_type& kt) {
    if (std::find(allowed_key_types.begin(),allowed_key_types.end(),kt.get_string()) != allowed_key_types.end()) {
        return true;
    }
    return false;
}

bool algorithm::requires_hash() {
    return requires_hash_flag;
}

bool algorithm::is_hash_algorithm() {
    return is_hash_algorithm_flag;
}

key_type& algorithm::random_valid_key_type() {
    if (allowed_key_types.size() == 0) {
        throw std::logic_error("No allowed key types for algorithm");
    }
    std::random_shuffle(allowed_key_types.begin(),allowed_key_types.end());
    return key_types[allowed_key_types[0]];

}
key_type::key_type() {

};

key_type::~key_type() {

};

string key_type::get_string() {
    return name;
}

bool key_type::is_enabled() {
    return enabled;
}

algorithm& key_type::random_allowed_algorithm() {
    if (allowed_algorithms.size() == 0) {
        throw std::logic_error("Key type has no allowed algorithms");
    }
    std::random_shuffle(allowed_algorithms.begin(),allowed_algorithms.end());
    return algorithms[allowed_algorithms[0]];

}

bool key_type::is_allowed_algorithm(algorithm& algorithm) {
    if (std::find(allowed_algorithms.begin(),allowed_algorithms.end(),algorithm.get_string()) != allowed_algorithms.end()) {
        return true;
    }
    return false;
}

bool key_type::is_valid_key_size(uint size) {
    // (MbedTLS): size is always byte aligned
    if (size % 8 != 0) {
        return false;
    }

    if (size > max_key_size_bits) {
        return false;
    }

    if (size < min_key_size_bits) {
        return false;
    }

    // some keys only allow a fixed set of values
    if (!allowed_key_sizes_bits.empty()) {
        if (std::find(allowed_key_sizes_bits.begin(),
                      allowed_key_sizes_bits.end(),
                      size) == allowed_key_sizes_bits.end()) {
            return false;
        }
    }
    return true;
}

uint key_type::get_random_valid_key_size() {
    if (!allowed_key_sizes_bits.empty()) {
        std::random_shuffle(allowed_key_sizes_bits.begin(),allowed_key_sizes_bits.end());
        return allowed_key_sizes_bits[0];
    }

    int lower = floor(min_key_size_bits/ 8);
    int higher = floor(max_key_size_bits/8);

    return ((rand() % (higher - lower)) + lower) * 8;
}

} // namespace crypto_model
