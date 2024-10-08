/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include <stdexcept>
#include <stdlib.h>
#include <iostream>

#include "boilerplate.hpp"
#include "crypto_asset.hpp"
#include "string_ops.hpp"
#include "data_blocks.hpp"
#include "psa_asset.hpp"
#include "find_or_create_asset.hpp"
#include "tf_fuzz.hpp"
#include "psa_call.hpp"



/**********************************************************************************
   Methods of class psa_call follow:
**********************************************************************************/

//**************** psa_call methods ****************

psa_call::psa_call (tf_fuzz_info *test_state, long &call_ser_no,   // (constructor)
                    asset_search how_asset_found)
{
    this->test_state = test_state;
    this->asset_info.how_asset_found = how_asset_found;
    set_data.string_specified = false;
    set_data.set ("");  // actual data
    assign_data_var.assign ("");  // name of variable assigned (dumped) to
    assign_data_var_specified = false;
    set_data.file_specified = false;
    set_data.file_path.assign ("");
    this->call_ser_no = call_ser_no = unique_id_counter++;
    // These will be set in the lower-level constructors, but...
    prep_code = call_code = check_code = "";
    print_data = hash_data = false;
    barrier = target_barrier = "";  // not (yet) any barrier for re-ordering calls
    call_description = "";
}

psa_call::~psa_call (void)
{
    return;  // just to have something to pin a breakpoint onto
}

void psa_call::write_out_prep_code (ofstream &test_file)
{
    test_file << prep_code;
}

void psa_call::write_out_command (ofstream &test_file)
{
    test_file << call_code;
}

void psa_call::write_out_check_code (ofstream &test_file)
{
    if (exp_data.result_code_checking_enabled()) {
        test_file << check_code;
    } else {
        test_file << "    /* (No checks for this PSA call.) */" << endl;
    }
}

bool psa_call::simulate(void) {
    return false;
}

void psa_call::copy_policy_to_call(void) {

    if (policy.get_policy_info_from == ""){
        return;
    }

    string asset_name = policy.get_policy_info_from;

    vector<psa_asset*>::iterator found_asset;
    long x; // doesnt matter
    asset_search status = test_state->find_or_create_policy_asset(psa_asset_search::name,psa_asset_usage::all,asset_name,0,x,dont_create_asset,found_asset);

    switch (status) {

    case asset_search::found_active:
    case asset_search::found_deleted:
    case asset_search::found_invalid: {
        string handle = policy.handle_str;
        string asset_2_name = policy.asset_2_name;
        string asset_3_name = policy.asset_3_name;

        policy = found_asset[0]->policy;
        policy.handle_str = handle;
        policy.asset_2_name = asset_2_name;
        policy.asset_3_name = asset_3_name;
        return;
    }
    default:
        break;
    }

    status = test_state->find_or_create_key_asset(psa_asset_search::name,psa_asset_usage::all,asset_name,0,x,dont_create_asset,found_asset);

    switch (status) {

    case asset_search::found_active:
    case asset_search::found_deleted:
    case asset_search::found_invalid: {
        string handle = policy.handle_str;
        string asset_2_name = policy.asset_2_name;
        string asset_3_name = policy.asset_3_name;

        policy = found_asset[0]->policy;
        policy.handle_str = handle;
        policy.asset_2_name = asset_2_name;
        policy.asset_3_name = asset_3_name;
        break;
    }
    default:
        break;
    }

}

/**********************************************************************************
   End of methods of class psa_call.
**********************************************************************************/


/**********************************************************************************
   Methods of class sst_call follow:
**********************************************************************************/

/* calc_result_code() fills in the check_code string member with the correct
   result code (e.g., "PSA_SUCCESS" or whatever).

   This is a big part of where the target modeling -- error modeling -- occurs,
   so lots of room for further refinement here. */
void sst_call::fill_in_result_code (void)
{

    string formalized;  // "proper" result string
    switch (exp_data.get_expected_return_code()) {
    case expected_return_code_t::DontCare: // Do not generate checks
        return;

    case expected_return_code_t::Pass:
        find_replace_all ("$expect",
                          test_state->bplate->bplate_string[sst_pass_string],
                          check_code);

        // `check "foo"`
        find_replace_all ("$check_expect",
                          "0",
                          check_code);

        break;

    case expected_return_code_t::Fail:
        // If the command is `... check "foo" expect fail;`, the fail
        // binds to the check, not the command itself.
        if (exp_data.data_specified) {
          // expect a pass for the sst call itself.
          find_replace_all ("$expect",
                            test_state->bplate->bplate_string[sst_pass_string],
                            check_code);

          // expect a failure for the check.
          find_replace_all ("!= $check_expect",
                            "== 0",
                            check_code);

          find_replace_1st ("should be equal", "should not be equal",
                            check_code);
          } else {
          // Check for not-success:
          find_replace_1st ("!=", "==",
                            check_code);
          find_replace_all ("$expect",
                            test_state->bplate->bplate_string[sst_pass_string],
                            check_code);
          find_replace_1st ("expected ", "expected not ",
                            check_code);
        }
        break;

    case expected_return_code_t::SpecificFail:
        formalized = formalize (exp_data.get_expected_return_code_string(), "PSA_ERROR_");
        find_replace_all ("$expect", formalized, check_code);

        // NOTE: Assumes that the variable used to store the actual
        // value initialised to a different value than the expected
        // value.
        find_replace_all ("!= $check_expect","== 0",check_code);
        find_replace_1st ("should be equal", "should not be equal",
                          check_code);
        break;

    // TODO: move error code simulation into simulate().
    case expected_return_code_t::DontKnow: // Simulate
        // Figure out what the message should read:
        switch (asset_info.how_asset_found) {
            case asset_search::found_active:
            case asset_search::created_new:
                find_replace_all ("$expect",
                                  test_state->bplate->
                                      bplate_string[sst_pass_string],
                                  check_code);

                find_replace_all ("$check_expect","0",check_code);
                break;
            case asset_search::found_deleted:
            case asset_search::not_found:
                find_replace_all ("$expect",
                                  test_state->bplate->
                                      bplate_string[sst_fail_removed],
                                  check_code);

                // NOTE: Assumes that the variable used to store the actual
                // value initialised to a different value than the expected
                // value.
                find_replace_all ("!= $check_expect","== 0",check_code);
                find_replace_1st ("should be equal", "should not be equal",
                                  check_code);
                break;
            default:
                find_replace_1st ("!=", "==",
                                  check_code);  // like "fail", just make sure...

                find_replace_all ("$expect",
                                  test_state->bplate->
                                      bplate_string[sst_pass_string],
                                  check_code);  // ... it's *not* PSA_SUCCESS

                // NOTE: Assumes that the variable used to store the actual
                // value initialised to a different value than the expected
                // value.
                find_replace_all ("!= $check_expect","== 0",check_code);
                find_replace_1st ("should be equal", "should not be equal",
                                  check_code);
                break;
            }
            break;
        }
}

vector<psa_asset*>::iterator sst_call::resolve_asset (bool create_asset_bool,
                                                      psa_asset_usage where) {
    vector<psa_asset*>::iterator found_asset;
    vector<psa_asset*> *asset_vector;
    int asset_pick;

    if (random_asset != psa_asset_usage::all) {
        // != psa_asset_usage::all means to choose some known asset at random:
        if (random_asset == psa_asset_usage::active) {
            asset_vector = &(test_state->active_sst_asset);
            asset_info.how_asset_found = asset_search::found_active;
        } else if (random_asset == psa_asset_usage::deleted) {
            asset_vector = &(test_state->deleted_sst_asset);
            asset_info.how_asset_found = asset_search::found_deleted;
        } else {
            // "invalid" assets are not currently used.
            cerr << "\nError:  Tool-internal:  Please report error 1101 to " << endl
                 << "TF-Fuzz developers."
                 << endl;
            exit(1101);
        }
        if (asset_vector->size() > 0) {
            /* Pick an active or deleted asset at random: */
            asset_pick = rand() % asset_vector->size();
            found_asset = asset_vector->begin() + asset_pick;
            /* Copy asset information into template tracker: */
            asset_info.id_n = (*found_asset)->asset_info.id_n;
            asset_info.asset_ser_no
                    = (*found_asset)->asset_info.asset_ser_no;
        } else {
            if (random_asset == psa_asset_usage::active) {
                cerr << "\nError:  An sst call asks for a "
                     << "randomly chosen active asset, when none " << endl
                     << "is currently defined." << endl;
                exit(1008);
            } else if (random_asset == psa_asset_usage::deleted) {
                cerr << "\nError:  An sst call asks for a "
                     << "randomly chosen deleted asset, when none " << endl
                     << "is currently defined." << endl;
                exit(1009);
            }  // "invalid" assets are not currently used.
        }
    } else {
        // Find the asset by name:
        asset_info.how_asset_found = test_state->find_or_create_sst_asset (
                            psa_asset_search::name, where,
                            asset_info.get_name(), 0, asset_info.asset_ser_no,
                            create_asset_bool, found_asset );
        if (   asset_info.how_asset_found == asset_search::unsuccessful
            || asset_info.how_asset_found == asset_search::something_wrong ) {
            cerr << "\nError:  Tool-internal:  Please report error 108 to " << endl
                 << "TF-Fuzz developers."
                 << endl;
            exit(108);
        }
    }
    return found_asset;
}

sst_call::sst_call (tf_fuzz_info *test_state, long &call_ser_no,   // (constructor)
                    asset_search how_asset_found)
                        : psa_call(test_state, call_ser_no, how_asset_found)
{
    asset_info.the_asset = nullptr;
    return;  // just to have something to pin a breakpoint onto
}
sst_call::~sst_call (void)
{
    return;  // just to have something to pin a breakpoint onto
}

/**********************************************************************************
   End of methods of class sst_call.
**********************************************************************************/


/**********************************************************************************
   Methods of class crypto_call follow:
**********************************************************************************/

bool crypto_call::simulate(void) {
    bool has_changed = false;
    has_changed |= simulate_ret_code();

    return has_changed;
}



bool crypto_call::simulate_ret_code(void) {
    if (!exp_data.simulation_needed()) {
        return false;
    }
    switch (asset_info.how_asset_found) {
        case asset_search::found_active:
        case asset_search::created_new:
            exp_data.expect_pass();
            return true;
        case asset_search::not_found:
        case asset_search::found_deleted:
            exp_data.expect_failure();
            return true;
        default:
            exp_data.expect_failure();
            return true;
    }
}

/* calc_result_code() fills in the check_code string member with the correct
   result code (e.g., "PSA_SUCCESS" or whatever).  This "modeling" needs to be
   improved and expanded upon *massively* more or less mirroring what is seen in
   .../test/suites/crypto/crypto_tests_common.c in the psa_key_interface_test()
   method, (starting around line 20ish). */
void crypto_call::fill_in_result_code (void)
{
    string formalized;  // "proper" result string

    switch (exp_data.get_expected_return_code()) {

    case expected_return_code_t::DontCare:
        return;

    case expected_return_code_t::Pass:
        find_replace_all ("$expect",
                          test_state->bplate->bplate_string[sst_pass_string],
                          check_code);
        break;

    case expected_return_code_t::Fail:
        // Check for not-success:
        find_replace_1st ("!=", "==",
                          check_code);
        find_replace_all ("$expect",
                          test_state->bplate->bplate_string[sst_pass_string],
                          check_code);
        find_replace_1st ("expected ", "expected not ",
                          check_code);
        break;

    case expected_return_code_t::SpecificFail:
        formalized = formalize (exp_data.get_expected_return_code_string(), "PSA_ERROR_");
        find_replace_all ("$expect", formalized, check_code);
        break;

    case expected_return_code_t::DontKnow: // Simulate -- SHOULD NEVER HAPPEN
        throw std::logic_error("Crypto call fill_in_result_code: return code is don't know");
    }
}


bool crypto_call::copy_asset_to_call (void)
{
    if (asset_info.the_asset == nullptr) {
        return false;
    } else {
        // Get updated asset info from the asset:
        asset_info.asset_ser_no = asset_info.the_asset->asset_info.asset_ser_no;
        asset_info.id_n = asset_info.the_asset->asset_info.id_n;
        exp_data.n_exp_vars = asset_info.the_asset->exp_data.n_exp_vars;
        exp_data.data = asset_info.the_asset->exp_data.data;
        return true;
    }
}


crypto_call::crypto_call (tf_fuzz_info *test_state, long &call_ser_no,  // (constructor)
                          asset_search how_asset_found)
                             : psa_call(test_state, call_ser_no, how_asset_found)
{
    policy = key_policy_info::create_random();
    return;  // just to have something to pin a breakpoint onto
}
crypto_call::~crypto_call (void)
{
    // Nothing further to delete.
    return;  // just to have something to pin a breakpoint onto
}

/**********************************************************************************
   End of methods of class crypto_call.
**********************************************************************************/


/**********************************************************************************
   Methods of class security_call follow:
**********************************************************************************/

security_call::security_call (tf_fuzz_info *test_state, long &call_ser_no,  // (constructor)
                          asset_search how_asset_found)
                             : psa_call(test_state, call_ser_no, how_asset_found)
{
    // Nothing further to initialize.
    return;  // just to have something to pin a breakpoint onto
}
security_call::~security_call (void)
{
    // Nothing further to delete.
    return;  // just to have something to pin a breakpoint onto
}

// resolve_asset() doesn't do anything for security_calls, since there's no asset involved.
vector<psa_asset*>::iterator security_call::resolve_asset (bool create_asset_bool,
                                                           psa_asset_usage where)
{
    return test_state->active_sst_asset.end();  // (anything)
}

/* calc_result_code() fills in the check_code string member with the correct result
   code (e.g., "PSA_SUCCESS" or whatever).

   Since there are no actual PSA calls associated with security calls (so far at least),
   this should never be invoked. */
void security_call::fill_in_result_code (void)
{
    // Currently should not be invoked.
    cerr << "\nError:  Internal:  Please report error #205 to TF-Fuzz developers." << endl;
    exit (205);
}

/**********************************************************************************
   End of methods of class security_call.
**********************************************************************************/
