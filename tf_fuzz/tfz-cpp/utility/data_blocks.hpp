/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include <stdint.h>
#include <string>
#include <vector>

class psa_asset;

enum class psa_asset_type;
class psa_call;

enum class asset_search;

/* These classes "cut down the clutter" by grouping together related data and
   associated methods (most importantly their constructors) used in template_
   line, psa_call, psa_asset (etc.). */

#ifndef DATA_BLOCKS_HPP
#define DATA_BLOCKS_HPP

using namespace std;

/// Possible values of return codes.
///
/// Intended to be used primarily through [expect_info]
enum class expected_return_code_t {
    /// This call should pass.
    Pass,
    /// This call should fail.
    Fail,
    /// This call should return a specific error code.
    SpecificFail,

    /// The outcome of this call is unknown and should be simulated.
    DontKnow,

    /// the return code does not matter, and checks for this should not take
    /// place.
    DontCare,
};

/**
 * expect_info is all about expected data and expected pass / fail information.
 *
 * The possible types of expected values returned from a PSA call are modelled
 * in [expected_return_codes].
 *
 * Expected data refers to psa-asset data values, generally after reading
 * them. Currently, they are limited to character strings, but that will
 * probably be generalized in the future.
 */
class expect_info
{
public:

    // (literal expected data specified)
    bool data_specified;

    string data;     // what test template expects data from reading an asset to be
    string data_var; // name of variable containing expected data
    int n_exp_vars;  // how many check-value variables have been created
    bool data_var_specified;  // check against a variable

    /* This indicates whether expected results have or have not already been
       copied to this call.  It's a "one-shot," so to speak, to copy only
       once when results are known good.  Since calls can be inserted into
       earlier points in the call sequence (not always appended), the call
       sequence has to be gone over for this process multiple times. */
    bool expected_results_saved;

    expect_info (void);  // (default constructor)
    ~expect_info (void);  // (destructor)

    /// Is simulation of the return code needed?
    bool simulation_needed(void);

    /// Sets the expected return code of the call to a pass.
    void expect_pass (void);

    /// Sets the expected return code of the call to a failure.
    void expect_failure (void);

    /// Sets the expected return code of the call to a specific error code.
    void expect_error_code (string error);

    /// Sets the expected return code of the call to "don't know".
    ///
    /// This will cause TF_Fuzz to later simulate this value.
    void clear_expected_code(void);

    /// Gets the expected return code.
    expected_return_code_t get_expected_return_code(void);

    /// When a specified error code is given, get that error code as a string.
    /// When any other return code is expected, std::logic_error is thrown.
    string get_expected_return_code_string(void);

    void disable_result_code_checking (void);
    void enable_result_code_checking (void);
    bool result_code_checking_enabled(void);

    void copy_expect_to_call (psa_call *the_call);

private:
    /* true if template specifies expected data, and that expected data
       agrees with that in the asset */
    bool data_matches_asset;
    string return_code_result_string;

    // The type of return code expected.
    expected_return_code_t expected_return_code;

    // if false, the return code does not matter, and checks for this should not
    // take place.
    bool result_code_checking_enabled_f;
};


/**********************************************************************************
  Class set_data_info addresses PSA-asset data values as affected, directly or
  indirctly/implicitly, by the template-line content.  "Directly," that is, by
  virtue of the template line stating verbatim what to set data to, or indirectly
  by virtue of telling TF-Fuzz to create random data for it.
**********************************************************************************/

class set_data_info
{
public:
    // Data members:
    bool string_specified;
    // true if a string of data is specified in template file
    bool random_data;  // true to generate random data for the asset
    bool file_specified;  // true if a file of expected data was specified
    bool literal_data_not_file;
    // true to use data strings rather than files as data source
    int n_set_vars;  // how many implicit set variables have been created
    string file_path;  // path to file, if specified
    string flags_string;
    // creation flags, nominally for SST but have to be in a vector of base-class
    uint32_t data_offset;  // offset into asset data
    // Methods:
    set_data_info (void);  // (default constructor)
    ~set_data_info (void);  // (destructor)
    void set (string set_val);
    void set_calculated (string set_val);
    void randomize (void);
    string get (void);
    bool set_file (string file_name);

protected:
    // Data members:
    string data;  // String describing asset data.
    // Methods:
    string rand_creation_flags (void);
};


/**********************************************************************************
  Class asset_name_id_info groups together and acts upon all information related to the
  human names (as reflected in the code variable names, etc.) for PSA assets.
**********************************************************************************/

class asset_name_id_info
{
public:
    // Data members (not much value in "hiding" these behind getters)
    psa_asset *the_asset;
    psa_asset_type asset_type;  // SST vs. key vs. policy (etc.)
    bool id_n_not_name;  // true to create a PSA asset by ID
    bool name_specified;  // true iff template supplied human name
    bool id_n_specified;  // true iff template supplied ID #
    vector<string> asset_name_vector;
    vector<int> asset_id_n_vector;
    long asset_ser_no;  // unique ID for psa asset needed to find data string
    /* Note:  The original theory is that we can't save away iterators to
                      assets, because STL vectors could get relocated.  However,
                      we've switched over to lists, which don't get moved around, so
                      we should be safe now. */
    asset_search how_asset_found;
    uint64_t id_n;  // asset ID# (e.g., SST UID).
    /* Note:  This is just a holder to pass ID from template-line to call.  The
               IDs for a given template line are in asset_info.asset_id_n_vector. */
    // Methods:
    asset_name_id_info (void);  // (default constructor)
    ~asset_name_id_info (void);  // (destructor)
    void set_name (string set_val);
    void set_calc_name (string set_val);
    void set_just_name (string set_val);
    string get_name (void);
    void set_id_n (string set_val);
    void set_id_n (uint64_t set_val);
    string make_id_n_based_name (uint64_t id_n);
    // create UID-based asset name

protected:
    // Data members:
    string asset_name;  // parsed from template, assigned to psa_asset object
};


/**********************************************************************************
  Class key_policy_info collects together the aspects of a Crypto key attributes
  ("policies").  These include aspects that can affect TF-Fuzz's test-generation.
**********************************************************************************/

class key_policy_info
{
public:
  /* if true, then we must get generate a call to get policy info from a stated
    key. */
  bool generate_get_policy_from_key_call;

  // If set, the policy or key asset specified should be used to fill in the
  // policy at simulation time. This overwrites the other values in the object.
  //
  // If blank, the values in the object are used as-is.
  //
  // See `psa_call::copy_policy_to_call`
  string get_policy_info_from;

  /* if true, then the key was defined with policy specifications, but not
   a named policy, meaning that we have to create an implicit policy. */
  bool implicit_policy;
  bool copy_key = false; // true to indicate copying one key to another
  bool exportable =
      false; // key data can be exported (viewed - fail exports if not).
  bool copyable = false;    // can be copied (fail key-copies if not).
  bool can_encrypt = false; // OK for encryption (fail other uses).
  bool can_decrypt = false; // OK for decryption (fail other uses).
  bool can_sign = false;    // OK for signing (fail other operations).
  bool can_verify =
      false; // OK for verifying a message signature (fail other uses).
  bool derivable = false;  // OK for derive other keys (fail other uses).
  bool persistent = false; // must be deleted at the end of test.

  // no_<flag> denotes that <flag> must not be set in the key.
  //
  // For the above flags, truth means "must be set" and false means "don't
  // care". Setting no_<flag> means "must not be set". no_<flag> takes
  // presedence over <flag>.

  bool no_exportable = false;  // true to indicate that exportable must not be
                               // set during randomisation
  bool no_copyable = false;    // true to indicate that copyable must not be set
                               // during randomisation
  bool no_can_encrypt = false; // true to indicate that can_encrypt must not be
                               // set during randomisation
  bool no_can_decrypt = false; // true to indicate that can_decrypt must not be
                               // set during randomisation
  bool no_can_sign = false;    // true to indicate that can_sign must not be set
                               // during randomisation
  bool no_can_verify = false;  // true to indicate that can_verify must not be
                               // set during randomisation
  bool no_derivable = false;  // true to indicate that derivable must not be set
                              // during randomisation
  bool no_persistent = false; // true to indicate that persistent must not be
                              // set during randomisation

  string usage_string;
  /* This string is set to a PSA_KEY_USAGE_* value in the template
             immediately prior to making define_call<add_policy_usage_call>.
             The copy_template_to_call() therein sets the corresponding string
             in the call, and that is copied into the code in the
     fill_in_command() invocation. */
  string print_usage_true_string;
  /* For printing out policy usage, this states how to describe the usage
             if it can be used this way.  This is managed similarly with, and
     used in conjunction with usage_string above.  NOTE:  THIS ALSO SERVES AS AN
             INDICATOR WHETHER OR NOT TO PRINT ON A GET-USAGE CALL.  "" means
     not to print. */
  string print_usage_false_string;
  /* Also for printing out policy usage, this is how to describe usage if
             it cannot be used this way. */
  string key_type; // AES, DES, RSA pair, DS public, etc.
  string key_algorithm;

  // The key size. If <0, this will be re-generated by fill_in_policy.
  int n_bits=-1;
  // for get_key_info call (possibly others) exected key size in bits
  string handle_str; // the text name of the key's "handle"
  string key_data;   // the key data as best we can know it.
  string asset_2_name;
  // if there's a 2nd asset, such as policy on key call, this is its name
  string asset_3_name; // if there's a 3rd asset, then this is its name

  // Methods:
  key_policy_info(void);  // (default constructor)
  ~key_policy_info(void); // (destructor)

  /** Creates a random, but not necessarily valid, policy */
  static key_policy_info create_random();


protected:

    /* The following settings are not necessarily being randomized in mutually-
       consistent ways, for two reasons:  First, the template should set all that
       matter, and second, testing TF response to nonsensical settings is also
       valuable. */
    // Data members:
    bool data_matches_asset;
    /* true if template specifies expected data, and that expected data
               agrees with that in the asset */
};



#endif // DATA_BLOCKS_HPP
