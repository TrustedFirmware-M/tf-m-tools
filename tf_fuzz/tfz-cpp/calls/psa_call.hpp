/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef PSA_CALL_HPP
#define PSA_CALL_HPP

#include <string>
#include <iosfwd>
#include <vector>

#include "data_blocks.hpp"

class psa_asset;
enum class psa_asset_usage;
class tf_fuzz_info;

using namespace std;

class psa_call
{
public:
    string call_description;  // description of the call, just for tracing
    expect_info exp_data;  // everything about expected results
    set_data_info set_data;  // everything about setting PSA-asset-data values
    asset_name_id_info asset_info;  // everything about the asset(s) for this line
    key_policy_info policy;  // (specific to crypto, but have to put this here)
    string asset_2_name;  // if there's a 2nd asset, then this is its name
    string asset_3_name;  // if there's a 3rd asset, then this is its name
    psa_asset_usage random_asset;
        /* if asked to use some random asset from active or deleted, this says
           which.  psa_asset_usage::all if not using this feature. */
    bool assign_data_var_specified;  // asset data to/from named variable
    string assign_data_var;  // name of variable to dump (assign) data into
    // Expected-result info:
    bool print_data;  // true to print asset data to test log
    bool hash_data;  // true to hash data for later comparison
    string id_string;  // not all PSA calls involve an ID, but a diverse set do
    long call_ser_no;  // unique serial# for this psa_call (see note in tf_fuzz.hpp)
    tf_fuzz_info *test_state;  // the big blob with pointers to everything going on
    string barrier;
        /* "barrier" is used for template-line operations that resolve a series of
           PSA calls.  In particular, with respect to the fact that TF-Fuzz strives
           to randomize these multiple calls where possible, meaning interspersing
           them among other, earlier commands.  However, for example, calls to set
           the aspects of a policy can't be pushed too far back, such as in among
           calls setting that same policy for a previous operation!  "barrier" is
           either "", in which case this call does not care whether you place calls
           before it, or it contains the name of an asset that, calls related to
           which must be placed *after* this call. */
    string target_barrier;
        /* asset to tell the psa_call objects to set and search barrier to when
           re-ordering PSA calls.  For key policies, this is not necessarily the
           nominal asset of that call.  For a policy call, it is that policy asset,
           so that later re-settings of the same policy don't pollute the current
           setting of that policy.  However, for key sets and reads, it is not the
           key asset, but its policy. */

    virtual vector<psa_asset*>::iterator resolve_asset (bool create_asset_bool,
                                                        psa_asset_usage where) = 0;

    /// Updates asset based on call information.
    ///
    /// WARNING: previously, this used to be the place to do call simulation
    /// logic such as modifiying assets. Code that does simulation or in any
    /// way mutates the state should now instead go in simulate().
    virtual bool copy_call_to_asset (void) = 0;

    /// Updates call based on asset information.
    virtual bool copy_asset_to_call (void) = 0;

    /// Simulates the effect of the call, returning true if a change has been
    /// made.
    ///
    /// This is called before asset simulatio takes place. For more details on
    /// control flow, see simulate_calls().
    ///
    /// If no return code for the call was given in the template, this should be
    /// updated here. However, if a return code is already present, it should
    /// never be overwritten.
    virtual bool simulate (void);

    // Update policy information in the call based on the policy or key
    // asset specified in policy.get_policy_info_from. If this is unset,
    // the existing values are used as-is.
    //
    // This enables the simulation time setting of the policy.
    //
    // See `key_policy_info.get_policy_info_from`.
    void copy_policy_to_call(void);

    // TODO: move simulation and error modelling code code into simulate().
    // once this is done, remove default impl so that simulate is mandatory for
    // calls.
    // ..
    // In particular, need to move code from:
    // ..
    // - copy_call_to_asset
    // ..
    // - fill_in_command
    // ..
    // - fill_in_result_code

    virtual void fill_in_prep_code (void) = 0;

    /// WARNING: Previously, this used to also contain expected value
    /// modelling code (alongside fill_in_command), and some error code
    /// modelling may still be left over here. New expected value modelling code
    /// should be put in simulate() where possible. Doing this gives a much
    /// nicer split between the simulation step (simulate()), and the code
    /// generation step (which this method is part of).
    virtual void fill_in_command (void) = 0;

    void write_out_prep_code (ofstream &test_file);
    void write_out_command (ofstream &test_file);
    void write_out_check_code (ofstream &test_file);
    psa_call (tf_fuzz_info *test_state, long &asset_ser_no,
              asset_search how_asset_found);  // (constructor)
    ~psa_call (void);

protected:
    string prep_code;  // declarations and such prior to all of the calls
    string call_code;  // for the call itself
    string check_code;  // for the code to check success of the call
    static long unique_id_counter;  // counts off unique IDs for assets

    /// Fill in expected result checks.
    ///
    /// WARNING: Previously, this used to also contain expected value
    /// modelling code (alongside fill_in_command), and some error code
    /// modelling may still be left over here. New expected value modelling code
    /// should be put in simulate() where possible. Doing this gives a much
    /// nicer split between the simulation step (simulate()), and the code
    /// generation step (which this method is part of).
    virtual void fill_in_result_code (void) = 0;

private:
    // Data members:
    // Methods:
};


class sst_call : public psa_call
{
public:
    // Data members:  // (low value in hiding these behind setters and getters)
    // Methods:
        vector<psa_asset*>::iterator resolve_asset (bool create_asset_bool,
                                                    psa_asset_usage where);
        sst_call (tf_fuzz_info *test_state, long &asset_ser_no,
                  asset_search how_asset_found);  // (constructor)
        ~sst_call (void);

protected:
    // Data members:
        void fill_in_result_code (void);

private:
    // Data members:
    // Methods:
};

class crypto_call : public psa_call
{
public:
    // Data members:  // (low value in hiding these behind setters and getters)
    // Methods:
        bool copy_asset_to_call (void) override;
        virtual bool simulate() override;
        crypto_call (tf_fuzz_info *test_state, long &asset_ser_no,
                    asset_search how_asset_found);  // (constructor)
        ~crypto_call (void);

protected:
    // Data members:
    // Methods:
        void fill_in_result_code (void) override;
           // for now, the method-overide buck stops here, but that'll probably change
        bool simulate_ret_code(void);


private:
};

class security_call : public psa_call
   /* Strictly speaking, these don't really correspond to PSA calls, so it's a little
      iffy to subclass them from psa_call.  However, the calling patterns work out
      right. */
{
public:
    // Data members:  // (low value in hiding these behind setters and getters)
    // Methods:
        vector<psa_asset*>::iterator resolve_asset (bool create_asset_bool,
                                                    psa_asset_usage where);
        security_call (tf_fuzz_info *test_state, long &asset_ser_no,
                       asset_search how_asset_found);  // (constructor)
        ~security_call (void);

protected:
    // Data members:
    // Methods:
        void fill_in_result_code (void);
           // Should never be invoked, since security calls generate no PSA calls.

private:
    // Data members:
    // Methods:
};

#endif  // PSA_CALL_HPP
