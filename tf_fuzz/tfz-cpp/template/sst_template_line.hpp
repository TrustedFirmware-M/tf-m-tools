/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef SST_TEMPLATE_LINE_HPP
#define SST_TEMPLATE_LINE_HPP

#include <cstdlib>  // for rand()
#include <string>

#include "data_blocks.hpp"
#include "sst_call.hpp"
#include "template_line.hpp"
#include "tf_fuzz.hpp"

using namespace std;

class set_sst_template_line : public sst_template_line
{
public:
    // Data members:
    // Methods:
        void setup_call (set_data_info set_info, bool random_data,
                         bool fill_in_template, bool create_call,
                         template_line *temLin, tf_fuzz_info *rsrc) {
            define_call<sst_set_call> (set_info, random_data, fill_in_template,
                                       create_call, temLin, rsrc, add_to_end,
                                       dont_set_barrier);
        }
        set_sst_template_line (tf_fuzz_info *resources);  // (constructor)
        ~set_sst_template_line (void);

protected:
    // Data members:
    // Methods:
        string rand_creation_flags (void);  // choose a random set of creation flags

private:
    // Data members:
    // Methods:
};

class remove_sst_template_line : public sst_template_line
{
public:
    // Data members:
    // Methods:
        void setup_call (set_data_info set_info, bool random_data,
                         bool fill_in_template, bool create_call,
                         template_line *temLin, tf_fuzz_info *rsrc) {
            define_call<sst_remove_call> (set_info, random_data, fill_in_template,
                                       create_call, temLin, rsrc, add_to_end,
                                       dont_set_barrier);
        }
        remove_sst_template_line (tf_fuzz_info *resources);  // (constructor)
        ~remove_sst_template_line (void);

protected:
    // Data members:
    // Methods:

private:
    // Data members:
    // Methods:
};

class read_sst_template_line : public sst_template_line
{
public:
    // Data members:
    // Methods:
        void setup_call (set_data_info set_info, bool random_data,
                         bool fill_in_template, bool create_call,
                         template_line *temLin, tf_fuzz_info *rsrc) {
            define_call<sst_get_call> (set_info, random_data, fill_in_template,
                                       create_call, temLin, rsrc, add_to_end,
                                       dont_set_barrier);
        }
        read_sst_template_line (tf_fuzz_info *resources);  // (constructor)
        ~read_sst_template_line (void);

protected:
    // Data members:
    // Methods:

private:
    // Data members:
    // Methods:
};

#endif  // #ifndef SST_TEMPLATE_LINE_HPP
