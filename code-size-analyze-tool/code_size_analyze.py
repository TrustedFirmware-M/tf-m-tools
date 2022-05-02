# ------------------------------------------------------------------------------
# Copyright (c) 2021-2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# ------------------------------------------------------------------------------

import argparse
import os
import sys
import glob
sys.path.append("src")
from ui import UI
from sq import SQ

none_databse = "Cannot find database {}! Please use this command to create \
databse:\n\n\tpython3 code_size_analyze.py --map <map file path> \
--gnuarm/--armcc --db {}\n"

def reverse_terminal_text(items):
    line1 = "─" * 128
    tmp, ret = [], []
    for x in items:
        if x == line1:
            ret.append(tmp)
            tmp = []
        tmp.append(x)
    items = []
    for i in range(len(ret) - 1, -1, -1):
        items.extend(ret[i])
    items.append(line1)
    return items

def main(args):
    map_file, db_file = "", ""
    if args.file_input.find(".map") >= 0:
        map_file = args.file_input
    else:
        db_file = args.file_input
    """
    Class 'sq' is to create a sqlite3 database from map file of compiler.
    """
    if map_file:
        if not args.gnuarm_compiler and not args.armclang_compiler:
            print("Error: Need --gnuarm or --armcc to create database")
            exit(0)
        if os.path.exists(args.db_name):
            for infile in glob.glob(os.path.join(os.getcwd(), args.db_name)):
                os.remove(infile)
        sq = SQ()
        sq.gnuarm = True if args.gnuarm_compiler else False
        sq.armcc = True if args.armclang_compiler else False
        sq.map_file = map_file
        sq.db_name = args.db_name
        sq.update()

    if (db_file and os.path.exists(db_file)) or (map_file and os.path.exists(args.db_name)):
        """
        Class 'ui' is to show the ui in terminal or export plaintext.
        """
        ui = UI()
        ui.gnuarm = True if args.gnuarm_compiler else False
        ui.armcc = True if args.armclang_compiler else False
        if db_file:
            ui.db_file = db_file
        if map_file:
            ui.db_file = args.db_name
        ui.open_db()
        if args.sort_by_size:
            ui.sort = "size"
        if args.sort_by_name:
            ui.sort = "name"
        if args.sort_by_obj:
            ui.sort = "obj_file"
        if args.sort_by_lib:
            ui.sort = "lib_file"
        if args.sort_by_sec:
            ui.sort = "section"

        if args.desc:
            ui.order = "DESC"
        if args.asc:
            ui.order = "ASC"

        if args.ui_show:
            if args.sort_by_name or args.sort_by_obj or args.sort_by_lib or args.sort_by_sec:
                print("UI mode cannot support sort. Use it in terminal mode.")
                exit(0)
            ui.run()

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
            if args.sort_by_obj:
                ui.sort = "name"
            if args.sort_by_sec:
                print("Object files cannot sort by this option")
                exit(0)
            ui.draw_obj_page()

        if args.obj_name:
            ui.obj_file = args.obj_name
            ui.draw_obj_detail_page()
            ui.items = reverse_terminal_text(ui.items)

        if args.list_library:
            if args.sort_by_lib:
                ui.sort = "name"
            if args.sort_by_obj or args.sort_by_sec:
                print("Libraries cannot sort by this option")
                exit(0)
            ui.draw_library_page()

        if args.library_name:
            if args.sort_by_sec or args.sort_by_obj:
                print("Library dump cannot sort by this option")
                exit(0)
            ui.library_name = args.library_name
            ui.draw_library_detail_page()
            ui.items = reverse_terminal_text(ui.items)

        if args.list_section:
            if args.sort_by_sec:
                ui.sort = "name"
            if args.sort_by_lib or args.sort_by_obj:
                print("Sections cannot sort by this option")
                exit(0)
            ui.draw_section_page()

        if args.section_name:
            if args.sort_by_name or args.sort_by_obj or args.sort_by_lib or args.sort_by_sec:
                print("Section dump cannot support sort.")
                exit(0)
            ui.section_name = args.section_name
            ui.draw_section_lib()
            ui.items = reverse_terminal_text(ui.items)

        if "─" * 128 not in ui.items and "-" * 128 not in ui.items and ui.items:
            max_len = 0
            for x in ui.items:
                max_len = max(max_len, len(x))
            ui.items.insert(1, "-" * max_len)
            ui.items.insert(0, "─" * max_len)
            ui.items.append("─" * max_len)

        if ui.items and not args.ui_show:
            for s in ui.items:
                print(s)

    else:
        print(none_databse.format(db_file, db_file))

def parse_args():
    """
    List the arguments for program.
    """
    parser = argparse.ArgumentParser()

    compiler_group = parser.add_mutually_exclusive_group()
    compiler_group.add_argument('--gnuarm',
                                dest='gnuarm_compiler',
                                action='store_true',
                                help='GNUARM model')
    compiler_group.add_argument('--armcc',
                                dest='armclang_compiler',
                                action='store_true',
                                help='ARMCLANG model')

    parser.add_argument('file_input', help='map or database file')
    parser.add_argument('--db-name',
                        dest='db_name',
                        metavar='<data.db>',
                        default='data.db',
                        help='database name to save')

    terminal_opt = parser.add_mutually_exclusive_group()
    terminal_opt.add_argument('-u', '--ui',
                              dest='ui_show',
                              action='store_true',
                              help='start UI to analyze')
    terminal_opt.add_argument('-S', '--Summary',
                              dest='all',
                              action='store_true',
                              help='show summary message')
    terminal_opt.add_argument('-s', '--list-section',
                              dest='list_section',
                              action='store_true',
                              help='list section')
    terminal_opt.add_argument('-l', '--list-library',
                              dest='list_library',
                              action='store_true',
                              help='list library')
    terminal_opt.add_argument('-o', '--list-obj',
                              dest='list_obj',
                              action='store_true',
                              help='list object file')
    terminal_opt.add_argument('-f', '--list-function',
                              dest='list_function',
                              action='store_true',
                              help='list function')
    terminal_opt.add_argument('-d', '--list-data',
                              dest='list_data',
                              action='store_true',
                              help='list data')
    terminal_opt.add_argument('--dump-sec',
                              dest='section_name',
                              metavar='<sec>',
                              help='dump section')
    terminal_opt.add_argument('--dump-lib',
                              dest='library_name',
                              metavar='<lib>',
                              help='dump library')
    terminal_opt.add_argument('--dump-obj',
                              dest='obj_name',
                              metavar='<obj>',
                              help='dump object file')
    terminal_opt.add_argument('--dump-func',
                              dest='dump_function_name',
                              metavar='<func>',
                              help='dump function')
    terminal_opt.add_argument('--dump-data',
                              dest='dump_data_name',
                              metavar='<data>',
                              help='dump data')
    terminal_opt.add_argument('--search-func',
                              dest='function_name',
                              metavar='<func>',
                              help='search function')
    terminal_opt.add_argument('--search-data',
                              dest='data_name',
                              metavar='<data>',
                              help='search data')

    sort_opt = parser.add_mutually_exclusive_group()
    sort_opt.add_argument('--sort-by-size',
                          dest='sort_by_size',
                          action='store_true',
                          default=True,
                          help='list by size order')
    sort_opt.add_argument('--sort-by-name',
                          dest='sort_by_name',
                          action='store_true',
                          default=False,
                          help='list by name order')
    sort_opt.add_argument('--sort-by-obj',
                          dest='sort_by_obj',
                          action='store_true',
                          default=False,
                          help='list by object file name order')
    sort_opt.add_argument('--sort-by-lib',
                          dest='sort_by_lib',
                          action='store_true',
                          default=False,
                          help='list by library file name order')
    sort_opt.add_argument('--sort-by-sec',
                          dest='sort_by_sec',
                          action='store_true',
                          default=False,
                          help='list by section name order')

    sort_ord = parser.add_mutually_exclusive_group()
    sort_ord.add_argument('--desc',
                          dest='desc',
                          action='store_true',
                          default=True,
                          help='sort with desc order')
    sort_ord.add_argument('--asc',
                          dest='asc',
                          action='store_true',
                          default=False,
                          help='sort with asc order')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main(parse_args())
    exit(0)
