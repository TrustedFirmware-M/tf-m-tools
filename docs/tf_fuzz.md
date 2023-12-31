# TF_Fuzz

.../tf_fuzz directory contents:

assets       calls               demo      parser    tests        regression
backupStuff  class_forwards.hpp  lib       README    tf_fuzz.cpp  utility
boilerplate  commands            Makefile  template  tf_fuzz.hpp  visualStudio

TF-Fuzz root directory.

--------------------------------------------------------------------------------

TF-Fuzz is a TF-M fuzzing tool, at the PSA-call level.  At the time of writing
this at least, presentations available at:

    https://www.trustedfirmware.org/docs/TF-M_Fuzzing_Tool_TFOrg.pdf
    https://zoom.us/rec/share/1dxZcZit111IadadyFqFU7IoP5X5aaa8gXUdr_UInxmMbyLzEqEmXQdx79-IWQ9p
(These presentation materials may not be viewable by all parties.)

--------------------------------------------------------------------------------

To build TF-Fuzz, simply type "make" in this directory.  Executable, called
"tfz", is placed in this directory.

To run tfz, two environment variables must first be assigned.  In bash syntax:

    export TF_FUZZ_LIB_DIR=<path to this TF-M installation>/tf-m-tools/tf_fuzz/lib
    export TF_FUZZ_BPLATE=tfm_boilerplate.txt

Examples of usage can be found in the demo directory.

--------------------------------------------------------------------------------

To generate a testsuite for TF-M from a set of template files, use
generate_test_suite.sh.

.. code-block:: bash

    Usage: generate_test_suite.sh <template_dir> <suites_dir>

    Where:
        template_dir: The directory containing template files for the
                    fuzzing tool
        suites_dir: The suites directory in the TF-M working copy.
                    i.e.: $TF-M_ROOT/test/suites
    Example:
        cd tf-m-tools/tf_fuzz
        ./generate_test_suite.sh $TF-M_ROOT/../tf-m-tools/tf_fuzz/tests/  $TF-M_ROOT/../tf-m-tests/test/suites/


After the test suite is generated, the new test suite needs to be added to the
TF-M build by providing the following options to the CMake generate command
(The path needs to be aligned with the test suite dir provided for the shell
script above):

.. code-block:: bash

    -DTFM_FUZZER_TOOL_TESTS=1
    -DTFM_FUZZER_TOOL_TESTS_CMAKE_INC_PATH=$TF-M_ROOT/../tf-m-tests/test/suites/tf_fuzz

--------------------------------------------------------------------------------

To help understand the code, below is a C++-class hierarchy used in this code
base.  They are explained further in the READMEs in their respective direc-
tories, so the file names where the classes are defined is listed below (this,
very roughly in order of functional interactions, of chronological usage during
execution, and of most-to-least importance):

    template_line                        ./template/template_line.hpp
        sst_template_line                ./template/template_line.hpp
            read_sst_template_line       ./template/sst_template_line.hpp
            remove_sst_template_line     ./template/sst_template_line.hpp
            set_sst_template_line        ./template/sst_template_line.hpp
        policy_template_line             ./template/template_line.hpp
            read_policy_template_line    ./template/crypto_template_line.hpp
            set_policy_template_line     ./template/crypto_template_line.hpp
        key_template_line                ./template/template_line.hpp
            read_key_template_line       ./template/crypto_template_line.hpp
            remove_key_template_line     ./template/crypto_template_line.hpp
            set_key_template_line        ./template/crypto_template_line.hpp
        security_template_line           ./template/template_line.hpp
            security_hash_template_line  ./template/secure_template_line.hpp

    psa_call                             ./calls/psa_call.hpp
        crypto_call                      ./calls/psa_call.hpp
            policy_call                  ./calls/crypto_call.hpp
                policy_get_call          ./calls/crypto_call.hpp
                policy_set_call          ./calls/crypto_call.hpp
            key_call                     ./calls/crypto_call.hpp
                get_key_info_call        ./calls/crypto_call.hpp
                set_key_call             ./calls/crypto_call.hpp
                destroy_key_call         ./calls/crypto_call.hpp
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

    crc32                                ./utility/compute.hpp

    gibberish                            ./utility/gibberish.hpp

    expect_info                          ./utility/data_blocks.hpp
    set_data_info                        ./utility/data_blocks.hpp
    asset_name_id_info                   ./utility/data_blocks.hpp

--------------------------------------------------------------------------------

There are currently two especially annoying warts on the design of TF-Fuzz:
*   Need better management of variables in the generated code.  Currently,
    for example, upon "read"ing a value from a PSA asset more than once, it
    creates a same-named (i.e., duplicate) variable for each such time, which
    is obviously not right.
*   Upon adding the ability to do "do any N of these PSA calls at random,"
    in hindsight, a fundamental flaw was uncovered in the top-level flow of
    how TF-Fuzz generates the code.  High-level summary:
  *   It should have completely distinct Parse, Simulate, then Code-generation
      stages.
  *   Currently, the Parse and Simulate stages aren't really completely
      distinct, so there's a bunch of complicated Boolean flags traffic-
      copping between what in hindsight should be completely-separate Parse
      vs. Code-generation functionality.
    The function, interpret_template_line(), currently in
    .../tf_fuzz/parser/tf_fuzz_grammar.y (which may be moved to the its own file
    with randomize_template_lines()), has the lion's share of such Booleans,
    such as fill_in_template, create_call_bool, and create_asset_bool.
    The way it *should* work is:
  *   The parser in .../tf_fuzz_grammar.y should generate an STL vector (or
      list) of psa_call-subclass "tracker" objects.  It should not generate
      PSA-asset tracker objects (subclasses of psa_asset).
  *   There should then be an organized Simulate stage, that sequences through
      the psa_call-subclass list, creating and accumulating/maintaining current
      state in psa_asset-subclass objects, using that current state to
      determine expected results of each PSA call, which get annotated back
      into the psa_call-tracker objects.
  *   Finally, there already is, and should continue to be, a Code-generation
      phase that writes out the code, based upon text substitutions of
      "boilerplate" code snippets.
  *   Currently, (hindsight obvious) the Parse and Simulate phases got somewhat
      muddled together.  This shouldn't be super-hard to fix.
    That final Code-generation phase, conceptually at least, could be replaced
    instead with simply executing those commands directly, for targets that
    sufficient space to run TF-Fuzz in real-time.

--------------

*Copyright (c) 2019-2020, Arm Limited. All rights reserved.*
