/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

/* These classes "cut down the clutter" by grouping together related data and
   associated methods (most importantly their constructors) used in template_
   line, psa_call, psa_asset (etc.). */

#include <stdexcept>
#include <stdlib.h>
#include <string>
#include <vector>
#include <iostream>

#include "fill_in_policy.hpp"
#include "gibberish.hpp"
#include "data_blocks.hpp"
#include "find_or_create_asset.hpp"
#include "psa_call.hpp"



/**********************************************************************************
   Methods of class expect_info follow:
**********************************************************************************/

expect_info::expect_info (void)  // (default constructor)
{
    result_code_checking_enabled_f = true;
    return_code_result_string.assign ("");

    expected_return_code = expected_return_code_t::DontKnow;

    data.assign ("");
    data_var.assign ("");  // name of expected-data variable

    data_var_specified = false;
    data_specified = false;
    data_matches_asset = false;
    n_exp_vars = -1;  // so the first reference is 0 (no suffix), then _1, _2, ...
}

expect_info::~expect_info (void)  // (destructor)
{}

bool expect_info::simulation_needed(void) {
  if (result_code_checking_enabled_f &&
      expected_return_code == expected_return_code_t::DontKnow) {
    return true;
  }

    return false;
}

void expect_info::expect_pass (void)
{
    expected_return_code  = expected_return_code_t::Pass;
    return_code_result_string = "";
}

void expect_info::expect_failure(void)
{
    expected_return_code  = expected_return_code_t::Fail;
    return_code_result_string = "";
}

void expect_info::expect_error_code (string error)
{
    expected_return_code = expected_return_code_t::SpecificFail;
    return_code_result_string = error;
}


void expect_info::clear_expected_code (void)
{
    expected_return_code = expected_return_code_t::DontKnow;
}

expected_return_code_t expect_info::get_expected_return_code(void) {

    // NOTE: we do not store DontCare in expected_return_code, as this would erase
    // the value stored prior to checks being disabled. This way, when
    // enable_result_code_checking is called, it can use the value given by the
    // user previously.
    // ..
    // Despite this, having DontCare as a value is still useful: it allows user
    // code that uses expected return codes to just be a switch statement.

    if (result_code_checking_enabled_f) {
        return expected_return_code;
    }

    return expected_return_code_t::DontCare;
}

string expect_info::get_expected_return_code_string(void) {
    if (result_code_checking_enabled_f && expected_return_code == expected_return_code_t::SpecificFail) {
        return return_code_result_string;
    }
    throw std::logic_error("get_expected_return_code_string called when return code is not SpecificFail");
}

void expect_info::disable_result_code_checking (void)
{
    result_code_checking_enabled_f = false;
}

void expect_info::enable_result_code_checking (void)
{
    result_code_checking_enabled_f = true;
}

bool expect_info::result_code_checking_enabled (void) {
    return result_code_checking_enabled_f;
}

void expect_info::copy_expect_to_call (psa_call *the_call)
{
    the_call->exp_data = *this;
}

/**********************************************************************************
   End of methods of class expect_info.
**********************************************************************************/


/**********************************************************************************
   Class set_data_info methods regarding setting and getting asset-data values:
**********************************************************************************/

string set_data_info::rand_creation_flags (void)
{
    string result = "";
    const int most_flags = 2;
    int n_flags = (rand() % most_flags);

    for (int i = 0; i < n_flags;  ++i) {
        switch (rand() % 3) {
            case 0:
                result += "PSA_STORAGE_FLAG_NONE";
                break;
            case 1:
                result += "PSA_STORAGE_FLAG_NO_REPLAY_PROTECTION";
                break;
            case 2:
                result += "PSA_STORAGE_FLAG_NO_CONFIDENTIALITY";
                break;
        }
        if (i < n_flags-1)
            result += " | ";
    }
    if (result == "") result = "PSA_STORAGE_FLAG_NONE";

    return result;
}

set_data_info::set_data_info (void)  // (default constructor)
{
    literal_data_not_file = true;  // currently, not using files as data sources
    string_specified = false;
    data.assign ("");
    random_data = false;
    file_specified = false;
    file_path.assign ("");
    n_set_vars = -1;  // so the first reference is 0 (no suffix), then _1, _2, ...
    data_offset = 0;
    flags_string = rand_creation_flags();
}
set_data_info::~set_data_info (void)  // (destructor)
{}

/* set() establishes:
   *  An asset's data value from a template line (e.g., set sst snort data "data
      value"), and
   *  *That* such a value was directly specified, as opposed to no data value having
      been specified, or a random data value being requested.
   Arguably, this method "has side effects," in that it not only sets a value, but
   also "takes notes" about where that value came from.
*/
void set_data_info::set (string set_val)
{
    literal_data_not_file = true;  // currently, not using files as data sources
    string_specified = true;
    data.assign (set_val);
}

/* set_calculated() establishes:
   *  An asset's data value as *not* taken from a template line, and
   *  *That* such a value was not directly specified in any template line, such as
      if a random data value being requested.
   Arguably, this method "has side effects," in that it not only sets a value, but
   also "takes notes" about where that value came from.
*/
void set_data_info::set_calculated (string set_val)
{
    literal_data_not_file = true;  // currently, not using files as data sources
    string_specified = false;
    data.assign (set_val);
}

/* randomize() establishes:
   *  An asset's data value as *not* taken from a template line, and
   *  *That* such a value was randomized.
   Arguably, this method "has side effects," in that it not only sets a value, but
   also "takes notes" about where that value came from.
*/
void set_data_info::randomize (void)
{
    gibberish gib;
    char gib_buff[4096];  // spew gibberish into here
    int rand_data_length = 0;

    string_specified = false;
    random_data = true;
    literal_data_not_file = true;
    rand_data_length = 40 + (rand() % 256);
    /* Note:  Multiple assets do get different random data */
    gib.sentence (gib_buff, gib_buff + rand_data_length - 1);
    data = gib_buff;
}

/* Getter for protected member, data.  Protected so that it can only be set by
   set() or set_calculated(), above, to establish not only its value but
   how it came about. */
string set_data_info::get (void)
{
    return data;
}

/* Currently, files as data sources aren't used, so this whole method is not "of
   use," but that might change at some point. */
bool set_data_info::set_file (string file_name)
{
    literal_data_not_file = true;
    string_specified = false;
    data.assign ("");
    file_specified = true;
    // Remove the ' ' quotes around the file name:
    file_name.erase (0, 1);
    file_name.erase (file_name.length()-1, 1);
    file_path = file_name;
    return true;
}

/**********************************************************************************
   End of methods of class set_data_info.
**********************************************************************************/


/**********************************************************************************
   Class asset_name_id_info methods regarding setting and getting asset-data values:
**********************************************************************************/

asset_name_id_info::asset_name_id_info (void)  // (default constructor)
{
    id_n_not_name = false;  // (arbitrary)
    id_n = 100LL + ((uint64_t) rand() % 10000);  // default to random ID#
    asset_name.assign ("");
    id_n_specified = name_specified = false;  // no ID info yet
    asset_type = psa_asset_type::unknown;
    how_asset_found = asset_search::not_found;
    the_asset = nullptr;
    asset_ser_no = -1;
}
asset_name_id_info::~asset_name_id_info (void)
{
    asset_name_vector.clear();
    asset_id_n_vector.clear();
}

/* set_name() establishes:
   *  An asset's "human" name from a template line, and
   *  *That* that name was directly specified, as opposed to the asset being defined
      by ID only, or a random name being requested.
   Arguably, this method "has side effects," in that it not only sets a name, but
   also "takes notes" about where that name came from.
*/
void asset_name_id_info::set_name (string set_val)
{
    /* Use this to set the name as specified in the template file.  Call this only
       if the template file does indeed define a name. */
    name_specified = true;
    asset_name.assign (set_val);
}

/* set_calc_name() establishes:
   *  An asset's "human" name *not* from a template line, and
   *  *That* that name was *not* directly specified in any template line.
   Arguably, this method "has side effects," in that it not only sets a name, but
   also "takes notes" about where that name came from.
*/
void asset_name_id_info::set_calc_name (string set_val)
{
    name_specified = false;
    asset_name.assign (set_val);
}

// set_just_name() sets an asset's "human" name, without noting how that name came up.
void asset_name_id_info::set_just_name (string set_val)
{
    asset_name.assign (set_val);
}

/* Getter for protected member, asset_name.  Protected so that it can only be set by
   set_name() or set_calc_name(), above, to establish not only its value but
   how it came about. */
string asset_name_id_info::get_name (void)
{
    return asset_name;
}

// Asset IDs can be set directly from a uint64_t or converted from a string:
void asset_name_id_info::set_id_n (string set_val)
{
    id_n = stol (set_val, 0, 0);
}
void asset_name_id_info::set_id_n (uint64_t set_val)
{
    id_n = set_val;
}

// Create ID-based name:
string asset_name_id_info::make_id_n_based_name (uint64_t id_n)
{
    string result;

    switch (asset_type) {
        case psa_asset_type::sst:
            result = "SST_ID_";
            break;
        case psa_asset_type::key:
            result = "Key_ID_";
            break;
        case psa_asset_type::policy:
            result = "Policy_ID_";
            break;
        default:
            cerr << "\nError:  Tool-internal:  Please report error "
                << "#1223 to the TF-Fuzz developers." << endl;
            exit(1223);
    }
    result.append(to_string(id_n));
    return result;
}

/**********************************************************************************
   End of methods of class asset_name_id_info.
**********************************************************************************/


/**********************************************************************************
   Class key_policy_info methods:
**********************************************************************************/

key_policy_info::key_policy_info (void)  // (default constructor)
{
    generate_get_policy_from_key_call = false;
    copy_key = false;  // not copying one key to another
    exportable = false;
    copyable = false;
    can_encrypt = false;
    can_decrypt = false;
    can_sign = false;
    can_verify = false;
    derivable= false;
    persistent= false;

    get_policy_info_from = "";
    key_type = "";
    key_algorithm = "";
    n_bits = 0;

    usage_string.assign ("");
    print_usage_true_string.assign ("");
    print_usage_false_string.assign ("");

    gibberish *gib = new gibberish;
    char buffer[256];
    char *end;
    int buf_len = 5ULL + (uint64_t) (rand() % 10);
    end = gib->word (false, buffer, buffer + buf_len);
    *end = '\0';
    buffer[buf_len] = '\0';
    handle_str = buffer;
    gib->sentence (buffer, buffer + (40ULL + (uint64_t) (rand() % 200)));
    key_data = buffer;
    delete gib;

}

key_policy_info key_policy_info::create_random() {
    key_policy_info policy;
    fill_in_policy(policy,false);
    return policy;
}

key_policy_info::~key_policy_info (void)  // (destructor)
{
    return;  // (even if only to have something to pin a breakpoint on)
}


/**********************************************************************************
   End of methods of class key_policy_info.
**********************************************************************************/
