# ------------------------------------------------------------------------------
# Copyright (c) 2021-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# ------------------------------------------------------------------------------

import argparse
import os
import sys
sys.path.append("src")
from ui import UI
from sq import SQ

none_databse = "Cannot find database file! Please use this command to create \
databse:\n\n\tpython3 code_size_analyze.py -i <map file path> --gnuarm/--armcc\n"

def main(args):
    """
    It is required to input only one of '--gnuarm' and '--armcc'.
    """
    if (args.gnuarm_compiler and args.armclang_compiler) or \
        (not args.gnuarm_compiler and not args.armclang_compiler):
        print("Error: Need \'--gnuarm\' or \'--armcc\'")
        exit(0)

    """
    Class 'sq' is to create a sqlite3 database from map file of compiler.
    """
    if args.map_file_input:
        sq = SQ()
        sq.gnuarm = True if args.gnuarm_compiler else False
        sq.armcc = True if args.armclang_compiler else False
        sq.file_path = args.map_file_input
        sq.update()

    if os.path.exists('data.db'):
        """
        Class 'ui' is to show the ui in terminal or export plaintext.
        """
        ui = UI()
        ui.gnuarm = True if args.gnuarm_compiler else False
        ui.armcc = True if args.armclang_compiler else False
        output = ""
        if args.ui_show:
            ui.run()
        else:
            if args.all:
                ui.draw_summary_page()

            if args.list_function:
                ui.draw_function_page("")

            if args.function_name:
                ui.draw_function_page(args.function_name)

            if args.dump_function_name:
                ui.function_name = args.dump_function_name
                ui.draw_function_detail_page()

            if args.list_data:
                ui.draw_data_page("")

            if args.data_name:
                ui.draw_data_page(args.data_name)

            if args.dump_data_name:
                ui.data_name = args.dump_data_name
                ui.draw_data_detail_page()

            if args.list_obj:
                ui.draw_obj_page()

            if args.obj_name:
                ui.obj_file = args.obj_name
                ui.draw_obj_detail_page()

            if args.list_library:
                ui.draw_library_page()

            if args.library_name:
                ui.library_name = args.library_name
                ui.draw_library_detail_page()

            if args.list_section:
                ui.draw_section_page()

            if args.section_name:
                ui.section_name = args.section_name
                ui.draw_section_lib()

            output = ui.items
            if output:
                for s in output:
                    print(s)
        ui.con.close()
    else:
        print(none_databse)

def parse_args():
    """
    List the arguments for program.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        dest='map_file_input',
                        help='map file path <path>/tfm_s.map')
    parser.add_argument('-u', '--ui',
                        dest='ui_show',
                        action='store_true',
                        help='show UI')
    parser.add_argument('--gnuarm',
                        dest='gnuarm_compiler',
                        action='store_true',
                        help='gnuarm map file input')
    parser.add_argument('--armcc',
                        dest='armclang_compiler',
                        action='store_true',
                        help='armclang map file input')
    parser.add_argument('-a', '--all',
                        dest='all',
                        action='store_true',
                        help='show total')
    parser.add_argument('-s', '--list_section',
                        dest='list_section',
                        action='store_true',
                        help='list section')
    parser.add_argument('-l', '--list_library',
                        dest='list_library',
                        action='store_true',
                        help='list library')
    parser.add_argument('-o', '--list_obj',
                        dest='list_obj',
                        action='store_true',
                        help='list object file')
    parser.add_argument('-f', '--list_function',
                        dest='list_function',
                        action='store_true',
                        help='list function')
    parser.add_argument('-d', '--list_data',
                        dest='list_data',
                        action='store_true',
                        help='list data')
    parser.add_argument('--dump_section',
                        dest='section_name',
                        help='dump section')
    parser.add_argument('--dump_library',
                        dest='library_name',
                        help='dump library')
    parser.add_argument('--dump_obj',
                        dest='obj_name',
                        help='dump object file')
    parser.add_argument('--dump_function',
                        dest='dump_function_name',
                        help='dump function')
    parser.add_argument('--dump_data',
                        dest='dump_data_name',
                        help='dump data')
    parser.add_argument('--search_func',
                        dest='function_name',
                        help='search function')
    parser.add_argument('--search_data',
                        dest='data_name',
                        help='search data')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main(parse_args())
    exit(0)
