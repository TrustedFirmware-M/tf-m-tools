/*  Copyright (c) 2024 Arm Limited. All Rights Reserved.
 *
 *  SPDX-License-Identifier: BSD-3-Clause
 */

#ifndef FILL_IN_POLICY_HPP
#define FILL_IN_POLICY_HPP

#include "data_blocks.hpp"

/** Fill in all blank fields of policy_info with random values.
 *
 * If policy_must_be_valid is true, random valid values will be given, and
 * TF-Fuzz will error if there is no satisfying values for the policy.
 *
 * For a policy to be valid:
 *
 *  * The key type and algorithm are not disabled.
 *  * The key type and algorithm are compatible with eachother.
 *  * The key size is compatible with the key size.
 *
 * This is more stringent than the requirements of psa_generate_key(), which
 * does not require that the key type and algorithm are compatible. However, a
 * policy of this kind is functionally useless, so to improve test usefulness,
 * this requirement is enforced here anyways.
 *
 */
void fill_in_policy(key_policy_info &policy_info, bool policy_must_be_valid);

#endif // FILL_IN_POLICY_HPP
