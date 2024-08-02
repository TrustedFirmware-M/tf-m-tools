/*  Copyright (c) 2024 Arm Limited. All Rights Reserved.
 *
 *  SPDX-License-Identifier: BSD-3-Clause
 */


#include <cstring>
#include <string>

#include "fill_in_policy.hpp"
#include "crypto_model.hpp"

void fill_in_policy(key_policy_info &policy_info, bool policy_must_be_valid) {

  // for set key <NAME> policy <POLICY> calls, we want to model based on the
  // policy asset given.

  // in this scenario, the policy cant be filled out now, and the information
  // should be copied over later.
  if (!policy_info.get_policy_from_policy.empty()) {
        return;
  }

  if (policy_must_be_valid) {

        crypto_model::key_type& kt = crypto_model::get_random_key_type();
        if (policy_info.key_type.empty() && policy_info.key_algorithm.empty()) {
            policy_info.key_type = kt.get_string();
            policy_info.key_algorithm = kt.random_allowed_algorithm().get_string_with_hash();

        } else if (policy_info.key_algorithm.empty() && !policy_info.key_type.empty()) {
            kt = crypto_model::get_key_type(policy_info.key_type);
            policy_info.key_algorithm = kt.random_allowed_algorithm().get_string_with_hash();

        } else if (policy_info.key_type.empty() && !policy_info.key_algorithm.empty()) {
            crypto_model::algorithm& alg = crypto_model::get_algorithm(policy_info.key_algorithm);
            kt = alg.random_valid_key_type();
            policy_info.key_type = kt.get_string();
        }

        if (policy_info.n_bits == 0) {
            policy_info.n_bits = kt.get_random_valid_key_size();
        }

    } else {
        if (policy_info.key_type.empty()) {
            policy_info.key_type = crypto_model::get_random_key_type().get_string();
        }

        if (policy_info.key_algorithm.empty()) {
            policy_info.key_algorithm= crypto_model::get_random_algorithm().get_string_with_hash();
        }

        if (policy_info.n_bits == 0) {
            policy_info.n_bits = crypto_model::get_random_key_size();
        }
    }

    // randomise usage flags and persistence if they arn't explicitly turned on or off.
    if (!policy_info.exportable && !policy_info.no_exportable) policy_info.exportable= (rand() % 2);
    if (!policy_info.copyable && !policy_info.no_copyable) policy_info.copyable= (rand() %2);
    if (!policy_info.can_encrypt && !policy_info.no_can_encrypt) policy_info.can_encrypt= (rand() %2);
    if (!policy_info.can_decrypt && !policy_info.no_can_decrypt) policy_info.can_decrypt= (rand() %2);
    if (!policy_info.can_verify && !policy_info.no_can_verify) policy_info.can_verify= (rand() % 2);
    if (!policy_info.can_sign && !policy_info.no_can_sign) policy_info.can_sign= (rand() %2);
    if (!policy_info.derivable && !policy_info.no_derivable) policy_info.derivable= (rand() %2);

    // TODO: persistence seems to be a little bit broken, so disable for now..

    // if (!policy_info.persistent && !policy_info.no_persistent) policy_info.persistent= (rand() %2);

}
