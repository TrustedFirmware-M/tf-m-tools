################
Source Structure
################

.. toctree::
    :maxdepth: 1
    :glob:

    *

*************
Code Overview
*************
To help understand the code, below is a C++-class hierarchy used in this code
base.  They are explained further in the documents in their respective
directories, so the file names where the classes are defined is listed below (this,
very roughly in order of functional interactions, of chronological usage during
execution, and of most-to-least importance):

.. code-block:: bash

    template_line                         ./template/template_line.hpp
        sst_template_line                 ./template/template_line.hpp
            read_sst_template_line        ./template/sst_template_line.hpp
            remove_sst_template_line      ./template/sst_template_line.hpp
            set_sst_template_line         ./template/sst_template_line.hpp
        policy_template_line              ./template/template_line.hpp
            read_policy_template_line     ./template/crypto_template_line.hpp
            set_policy_template_line      ./template/crypto_template_line.hpp
        key_template_line                 ./template/template_line.hpp
            read_key_template_line        ./template/crypto_template_line.hpp
            remove_key_template_line      ./template/crypto_template_line.hpp
            set_key_template_line         ./template/crypto_template_line.hpp
        security_template_line            ./template/template_line.hpp
            security_hash_template_line   ./template/secure_template_line.hpp

    psa_call                              ./calls/psa_call.hpp
        crypto_call                       ./calls/psa_call.hpp
            policy_call                   ./calls/crypto_call.hpp
                init_policy_call          ./calls/crypto_call.hpp
                reset_policy_call         ./calls/crypto_call.hpp
                add_policy_usage_call     ./calls/crypto_call.hpp
                set_policy_lifetime_call  ./calls/crypto_call.hpp
                set_policy_type_call      ./calls/crypto_call.hpp
                set_policy_algorithm_call ./calls/crypto_call.hpp
                set_policy_usage_call     ./calls/crypto_call.hpp
                get_policy_lifetime_call  ./calls/crypto_call.hpp
                get_policy_type_call      ./calls/crypto_call.hpp
                get_policy_algorithm_call ./calls/crypto_call.hpp
                get_policy_usage_call     ./calls/crypto_call.hpp
                get_policy_size_call      ./calls/crypto_call.hpp
                get_policy_call           ./calls/crypto_call.hpp
            key_call                      ./calls/crypto_call.hpp
                generate_key_call         ./calls/crypto_call.hpp
                create_key_call           ./calls/crypto_call.hpp
                copy_key_call             ./calls/crypto_call.hpp
                read_key_data_call        ./calls/crypto_call.hpp
                remove_key_call           ./calls/crypto_call.hpp
        sst_call                         ./calls/psa_call.hpp
            sst_remove_call              ./calls/sst_call.hpp
            sst_get_call                 ./calls/sst_call.hpp
            sst_set_call                 ./calls/sst_call.hpp
        security_call                    ./calls/psa_call.hpp
            hash_call                    ./calls/security_call.hpp

    boilerplate                          ./boilerplate/boilerplate.hpp

    psa_asset                            ./assets/psa_asset.hpp
        crypto_asset                     ./assets/crypto_asset.hpp
            policy_asset                 ./assets/crypto_asset.hpp
            key_asset                    ./assets/crypto_asset.hpp
        sst_asset                        ./assets/sst_asset.hpp

    tf_fuzz_info                         ./tf_fuzz.hpp

    variables                            ./utility/variables.hpp
    crc32                                ./utility/compute.hpp

    gibberish                            ./utility/gibberish.hpp

    expect_info                          ./utility/data_blocks.hpp
    set_data_info                        ./utility/data_blocks.hpp
    asset_name_id_info                   ./utility/data_blocks.hpp


TF-Fuzz now has better-organized management of variables in the generated code.
In particular, it maintains a list of variables named in the test template, and
implicit in the code, notably variables assets are ``read`` into.  It also now has
completely separate execution phases to parse the test template, simulate the
sequence of PSA calls generated, and write out the expected results.  That
simulation is only in enough detail to predict expected results.  Since TF-Fuzz
currently mostly addresses only SST calls, that simulation is very simple in
nature -- just tracking data movement.

--------------

*Copyright (c) 2024, Arm Limited. All rights reserved.*
