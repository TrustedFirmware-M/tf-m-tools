/*
 * Copyright (c) 2019-2022, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

/**********************************************************************************
   Functions in this file are exactly that:  functions, not methods of any class.
   That is, they are stand-alone, utility functions linked in to the executable,
   and available to whomever needs them.
**********************************************************************************/

// TODO: the key usages, algorithms, and types are currently incomplete.

#include "randomization.hpp"

/**
 * \brief Selects and returns a random key_usage_t value.
 *
 * \details
 *
 * \note
 *
 */
string rand_key_usage (void)
{
    switch (rand() % 6) {
        case 0:  return "PSA_KEY_USAGE_EXPORT";
        case 1:  return "PSA_KEY_USAGE_ENCRYPT";
        case 2:  return "PSA_KEY_USAGE_DECRYPT";
        case 3:  return "PSA_KEY_USAGE_SIGN_HASH";
        case 4:  return "PSA_KEY_USAGE_VERIFY_HASH";
        case 5:  return "PSA_KEY_USAGE_DERIVE";
    }
    return "";  /* placate compiler */
}

/**
 * \brief Selects and returns a random psa_algorithm_t value.
 *
 * \details
 *
 * \note
 *
 */
/* TODO:  Likely want to make additional versions of these specific for TLS,
   asymmetric, symmetric... */
string rand_key_algorithm (void)
{
    switch (rand() % 24) {
        case 0:  return "PSA_ALG_MD5";
        case 1:  return "PSA_ALG_RIPEMD160";
        case 2:  return "PSA_ALG_SHA_1";
        case 3:  return "PSA_ALG_SHA_224";
        case 4:  return "PSA_ALG_SHA_256";
        case 5:  return "PSA_ALG_SHA_384";
        case 6:  return "PSA_ALG_SHA_512";
        case 7:  return "PSA_ALG_SHA_512_224";
        case 8:  return "PSA_ALG_SHA_512_256";
        case 9:  return "PSA_ALG_SHA3_224";
        case 10:  return "PSA_ALG_SHA3_256";
        case 11:  return "PSA_ALG_SHA3_384";
        case 12:  return "PSA_ALG_SHA3_512";
        case 13:  return "PSA_ALG_ANY_HASH";
        case 14:  return "PSA_ALG_CBC_MAC";
        case 15:  return "PSA_ALG_CMAC";
        case 16:  return "PSA_ALG_CTR";
        case 17:  return "PSA_ALG_CFB";
        case 18:  return "PSA_ALG_OFB";
        case 19:  return "PSA_ALG_XTS";
        case 20:  return "PSA_ALG_CBC_NO_PADDING";
        case 21:  return "PSA_ALG_CBC_PKCS7";
        case 22:  return "PSA_ALG_CCM";
        case 23:  return "PSA_ALG_GCM";
    }
    return "";  /* placate compiler */
}


/**
 * \brief Selects and returns a random psa_key_type_t value.
 *
 * \details
 *
 * \note
 *
 */
string rand_key_type (void)
{
    switch (rand() % 9) {
        case 0:  return "PSA_KEY_TYPE_NONE";
        case 1:  return "PSA_KEY_TYPE_RAW_DATA";
        case 2:  return "PSA_KEY_TYPE_HMAC";
        case 3:  return "PSA_KEY_TYPE_DERIVE";
        case 4:  return "PSA_KEY_TYPE_AES";
        case 5:  return "PSA_KEY_TYPE_DES";
        case 6:  return "PSA_KEY_TYPE_CAMELLIA";
        case 7:  return "PSA_KEY_TYPE_RSA_PUBLIC_KEY";
        case 8:  return "PSA_KEY_TYPE_RSA_KEY_PAIR";
    }
    return "";  /* placate compiler */
}

