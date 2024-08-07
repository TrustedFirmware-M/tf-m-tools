/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

/* Objects typed to subclasses of the these classes are constructed and filled in
   by the parser as it parses the test template.  Although these objects do largely
   correspond to template lines, there's no real correlation to lines in the
   generated code. */

#ifndef SECURE_TEMPLATE_LINE_HPP
#define SECURE_TEMPLATE_LINE_HPP

#include "data_blocks.hpp"
#include "security_call.hpp"
#include "template_line.hpp"
#include "tf_fuzz.hpp"

class psa_call;

using namespace std;

/* Note:  The following are sub-classed from security (above). */

class security_hash_template_line : public security_template_line
{
public:
    // Data members:
    // Methods:
        void setup_call (set_data_info set_data, bool random_data,
                         bool fill_in_template, bool create_call,
                         template_line *temLin, tf_fuzz_info *rsrc)
        {
            define_call<hash_call> (set_data, random_data, fill_in_template,
                                    create_call, temLin, rsrc,
                                    add_to_end, yes_set_barrier);
        }
        bool copy_template_to_call (psa_call *the_call);
        security_hash_template_line (tf_fuzz_info *resources);  // (constructor)
        ~security_hash_template_line (void);

protected:
    // Data members:
    // Methods:

private:
    // Data members:
    // Methods:
};

#endif // #ifndef SECURE_TEMPLATE_LINE_HPP
