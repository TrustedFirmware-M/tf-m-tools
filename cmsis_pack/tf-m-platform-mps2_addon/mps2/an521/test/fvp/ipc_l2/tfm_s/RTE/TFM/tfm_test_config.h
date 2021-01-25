/*
 * Copyright (c) 2019-2020, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef TFM_TEST_CONFIG_H
#define TFM_TEST_CONFIG_H

//-------- <<< Use Configuration Wizard in Context Menu >>> --------------------

// <h>Crypto

//   <c>Test CBC Cryptography Mode
#define TFM_CRYPTO_TEST_ALG_CBC
//   </c>

//   <c>Test CCM Cryptography Mode
#define TFM_CRYPTO_TEST_ALG_CCM
//   </c>

//   <c>Test CFB Cryptography Mode
#define TFM_CRYPTO_TEST_ALG_CFB
//   </c>

//   <c>Test CTR Cryptography Mode
#define TFM_CRYPTO_TEST_ALG_CTR
//   </c>

//   <c>Test GCM Cryptography Mode
#define TFM_CRYPTO_TEST_ALG_GCM
//   </c>

//   <c>Test SHA-512 Cryptography Algorithm
#define TFM_CRYPTO_TEST_ALG_SHA_512
//   </c>

//   <c>Test HKDF (HMAC Key Derivation Function)
#define TFM_CRYPTO_TEST_HKDF
//   </c>

// </h>

//------------- <<< end of configuration section >>> ---------------------------

#endif /* TFM_TEST_CONFIG_H */
