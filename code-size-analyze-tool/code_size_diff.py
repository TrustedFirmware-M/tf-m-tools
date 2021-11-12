# -----------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import sqlite3
import argparse

def diff_summary():
    cursor1 = cur1.execute("select * from Summary")
    cursor2 = cur2.execute("select * from Summary")
    for row in cursor1:
        data1 = [row[0], row[1], row[2], row[3], row[4], row[5]]
    for row in cursor2:
        data2 = [row[0], row[1], row[2], row[3], row[4], row[5]]
    text = ["Code size:", "RO data:", "RW data:",
            "ZI data:", "Flash size:", "RAM size:"]

    for i in range(6):
        delta = data2[i] - data1[i]

        print("{:<12}{:<5}\t{:<8}B\t\t{:<8.2f}KB".
                    format(text[i],
                        "+++" if delta > 0 else "---",
                        abs(delta),
                        abs(delta)/1024))

def diff_function():
    cursor1 = cur1.execute("select * from Function")
    func_name_list = []
    total_code_change = 0
    for row in cursor1:
        func_name1 = row[0]
        func_size1 = row[2]
        func_obj_name1 = row[4]
        cursor2 = cur2.execute("select * from Function WHERE name = '{}' and obj_file = '{}'".
                               format(func_name1, func_obj_name1))
        if len(list(cursor2)) > 0:
            cursor2 = cur2.execute("select * from Function WHERE name = '{}' and obj_file = '{}'".
                                   format(func_name1, func_obj_name1))
            for row in cursor2:
                func_name2 = row[0]
                func_size2 = row[2]
                func_obj_name2 = row[4]
                delta = func_size2 - func_size1
                if delta != 0:
                    func_name_list.append({'name': func_name1,
                                           'delta': abs(delta),
                                           'sign': "+++" if delta > 0 else "---",
                                           'obj': func_obj_name1})
                    total_code_change += delta
        else:
            func_name_list.append({'name': func_name1,
                                   'delta': func_size1,
                                   'sign': "del",
                                   'obj': func_obj_name1})
            total_code_change -= func_size1

    cursor2 = cur2.execute("select * from Function")
    for row in cursor2:
        func_name2 = row[0]
        func_size2 = row[2]
        func_obj_name2 = row[4]
        cursor1 = cur1.execute("select * from Function WHERE name = '{}' and obj_file = '{}'".
                               format(func_name2, func_obj_name2))
        if len(list(cursor1)) == 0:
            func_name_list.append({'name': func_name2,
                                   'delta': func_size2,
                                   'sign': "new",
                                   'obj': func_obj_name2})
            total_code_change += func_size2

    func_name_list = sorted(func_name_list,
                            key=lambda i: i['delta'],
                            reverse=True)
    print("─" * 120)
    print("{:<50}{:<10}{:<10}{:<50}".format(
        "Function name", "Status", "Delta", "Object file"))
    print("─" * 120)
    for s in func_name_list:
        print("{:<50}{:<10}{:<10}{:<50}".format(
            s['name'], s['sign'], s['delta'], s['obj']))
    print("─" * 120)
    print("Total Function Size cahnge = {:<6} B\t= {:<8.2f} KB".format(
        total_code_change, total_code_change/1024))
    print("─" * 120)


def diff_data(data_type):
    cursor1 = cur1.execute("select * from Data where type = '{}'".format(data_type))
    data_name_list = []
    total_data_change = 0
    for row in cursor1:
        data_name1 = row[0]
        data_size1 = row[2]
        data_obj_name1 = row[5]
        cursor2 = cur2.execute("select * from Data WHERE name = '{}' and obj_file = '{}' and type = '{}'".
                               format(data_name1, data_obj_name1, data_type))
        if len(list(cursor2)) > 0:
            cursor2 = cur2.execute("select * from Data WHERE name = '{}' and obj_file = '{}' and type = '{}'".
                                   format(data_name1, data_obj_name1, data_type))
            for row in cursor2:
                data_name2 = row[0]
                data_size2 = row[2]
                data_obj_name2 = row[5]
                delta = data_size2 - data_size1
                if delta != 0:
                    data_name_list.append({'name': data_name1,
                                           'delta': abs(delta),
                                           'sign': "+++" if delta > 0 else "---",
                                           'obj': data_obj_name1})
                    total_data_change += delta
        else:
            data_name_list.append({'name': data_name1,
                                   'delta': data_size1,
                                   'sign': "del",
                                   'obj': data_obj_name1})
            total_data_change -= data_size1

    cursor2 = cur2.execute("select * from Data where type = '{}'".format(data_type))
    for row in cursor2:
        data_name2 = row[0]
        data_size2 = row[2]
        data_obj_name2 = row[5]
        cursor1 = cur1.execute("select * from Data WHERE name = '{}' and obj_file = '{}' and type = '{}'".
                               format(data_name2, data_obj_name2, data_type))
        if len(list(cursor1)) == 0:
            data_name_list.append({'name': data_name2,
                                   'delta': data_size2,
                                   'sign': "new",
                                   'obj': data_obj_name2})
            total_data_change += data_size2

    data_name_list = sorted(data_name_list,
                            key=lambda i: i['delta'],
                            reverse=True)
    print("─" * 130)
    print("{:<50}{:<10}{:<10}{:<50}{:<10}".format(
        "Data name", "Status", "Delta", "Object file", "Data Type"))
    print("─" * 130)
    for s in data_name_list:
        print("{:<50}{:<10}{:<10}{:<50}{:<10}".format(
            s['name'], s['sign'], s['delta'], s['obj'], data_type))
    print("─" * 130)
    print("Total {} Data change = {:<6} B\t= {:<8.2f} KB".format(
        data_type, total_data_change, total_data_change/1024))
    print("─" * 130)


def add_array(array1, array2):
    if len(array2) == len(array1):
        for i in range(len(array1)):
            array1[i] += array2[i]
        return array1


def diff_obj():
    cursor1 = cur1.execute("select * from Object")
    obj_name_list = []
    for row in cursor1:
        obj_name1 = row[0]
        obj_flash_size1 = row[2]
        obj_ram_size1 = row[3]
        obj_code_size1 = row[4]
        obj_rodata_size1 = row[5]
        obj_rwdata_size1 = row[6]
        obj_zidata_size1 = row[7]
        cursor2 = cur2.execute("select * from Object WHERE name = '{}'".
                               format(obj_name1))
        if len(list(cursor2)) > 0:
            cursor2 = cur2.execute("select * from Object WHERE name = '{}'".
                                   format(obj_name1))
            for row in cursor2:
                obj_name2 = row[0]
                if row[2] != obj_flash_size1 or \
                        row[3] != obj_ram_size1 or \
                        row[4] != obj_code_size1 or \
                        row[5] != obj_rodata_size1 or \
                        row[6] != obj_rwdata_size1 or \
                        row[7] != obj_zidata_size1:
                    obj_name_list.append({'name': obj_name1,
                                          'sign': "+/-",
                                          'delta_array': [row[2] - obj_flash_size1,
                                                          row[3] - obj_ram_size1,
                                                          row[4] - obj_code_size1,
                                                          row[5] - obj_rodata_size1,
                                                          row[6] - obj_rwdata_size1,
                                                          row[7] - obj_zidata_size1]})
        else:
            obj_name_list.append({'name': obj_name1,
                                  'sign': "del",
                                  'delta_array': [0-obj_flash_size1,
                                                  0-obj_ram_size1,
                                                  0-obj_code_size1,
                                                  0-obj_rodata_size1,
                                                  0-obj_rwdata_size1,
                                                  0-obj_zidata_size1]})
    cursor2 = cur2.execute("select * from Object")
    for row in cursor2:
        obj_name2 = row[0]
        cursor1 = cur1.execute("select * from Object WHERE name = '{}'".
                               format(obj_name2))
        if len(list(cursor1)) == 0:
            obj_name_list.append({'name': obj_name2,
                                  'sign': "new",
                                  'delta_array': [row[2], row[3],
                                                  row[4], row[5],
                                                  row[6], row[7]]})
    total_change = [0, 0, 0, 0, 0, 0]
    obj_name_list = sorted(obj_name_list,
                           key=lambda i: abs(
                               i['delta_array'][0]) + abs(i['delta_array'][1]),
                           reverse=True)
    print("─" * 120)
    print("{:<50}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
        "Object File name", "Status", "Flash", "RAM", "Code", "RO", "RW", "ZI"))
    print("─" * 120)
    for s in obj_name_list:
        total_change = add_array(total_change, s['delta_array'])
        print("{:<50}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(s['name'],
                                                                        s['sign'],
                                                                        s['delta_array'][0],
                                                                        s['delta_array'][1],
                                                                        s['delta_array'][2],
                                                                        s['delta_array'][3],
                                                                        s['delta_array'][4],
                                                                        s['delta_array'][5]))
    key_word = ["Flash", "RAM", "Code size", "RO Data", "RW Data", "ZI Data"]
    print("─" * 120)
    for i in range(6):
        print("{:<27}= {:<6} B\t= {:<8.2f} KB".format("Total obj {} change".format(
            key_word[i]), total_change[i], total_change[i]/1024))
    print("─" * 120)


def diff_lib():
    cursor1 = cur1.execute("select * from Library")
    lib_name_list = []
    for row in cursor1:
        lib_name1 = row[0]
        lib_flash_size1 = row[1]
        lib_ram_size1 = row[2]
        lib_code_size1 = row[3]
        lib_rodata_size1 = row[4]
        lib_rwdata_size1 = row[5]
        lib_zidata_size1 = row[6]
        cursor2 = cur2.execute("select * from Library WHERE name = '{}'".
                               format(lib_name1))
        if len(list(cursor2)) > 0:
            cursor2 = cur2.execute("select * from Library WHERE name = '{}'".
                                   format(lib_name1))
            for row in cursor2:
                lib_name2 = row[0]
                if row[1] != lib_flash_size1 or \
                        row[2] != lib_ram_size1 or \
                        row[3] != lib_code_size1 or \
                        row[4] != lib_rodata_size1 or \
                        row[5] != lib_rwdata_size1 or \
                        row[6] != lib_zidata_size1:
                    lib_name_list.append({'name': lib_name1,
                                          'sign': "+/-",
                                          'delta_array': [row[1] - lib_flash_size1,
                                                          row[2] - lib_ram_size1,
                                                          row[3] - lib_code_size1,
                                                          row[4] - lib_rodata_size1,
                                                          row[5] - lib_rwdata_size1,
                                                          row[6] - lib_zidata_size1]})
        else:
            lib_name_list.append({'name': lib_name1,
                                  'sign': "del",
                                  'delta_array': [0-lib_flash_size1,
                                                  0-lib_ram_size1,
                                                  0-lib_code_size1,
                                                  0-lib_rodata_size1,
                                                  0-lib_rwdata_size1,
                                                  0-lib_zidata_size1]})
    cursor2 = cur2.execute("select * from Library")
    for row in cursor2:
        lib_name2 = row[0]
        cursor1 = cur1.execute("select * from Library WHERE name = '{}'".
                               format(lib_name2))
        if len(list(cursor1)) == 0:
            lib_name_list.append({'name': lib_name2,
                                  'sign': "new",
                                  'delta_array': [row[1], row[2],
                                                  row[3], row[4],
                                                  row[5], row[6]]})
    total_change = [0, 0, 0, 0, 0, 0]
    lib_name_list = sorted(lib_name_list,
                           key=lambda i: abs(
                               i['delta_array'][0]) + abs(i['delta_array'][1]),
                           reverse=True)
    print("─" * 120)
    print("{:<50}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
        "Library name", "Status", "Flash", "RAM", "Code", "RO", "RW", "ZI"))
    print("─" * 120)
    for s in lib_name_list:
        total_change = add_array(total_change, s['delta_array'])
        print("{:<50}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(s['name'],
                                                                        s['sign'],
                                                                        s['delta_array'][0],
                                                                        s['delta_array'][1],
                                                                        s['delta_array'][2],
                                                                        s['delta_array'][3],
                                                                        s['delta_array'][4],
                                                                        s['delta_array'][5]))
    key_word = ["Flash", "RAM", "Code size", "RO Data", "RW Data", "ZI Data"]
    print("─" * 120)
    for i in range(6):
        print("{:<31}= {:<6} B\t= {:<8.2f} KB".format("Total Library {} change".format(key_word[i]), total_change[i], total_change[i]/1024))
    print("─" * 120)

def main(args):
    global con1, cur1, con2, cur2
    if args.input_dbs:
        if len(args.input_dbs) == 2:
            con1 = sqlite3.connect(args.input_dbs[0])
            cur1 = con1.cursor()
            con2 = sqlite3.connect(args.input_dbs[1])
            cur2 = con2.cursor()
        else:
            print("Error! Two database files shall be input.")
    if args.diff_function:
        diff_function()
    if args.diff_data:
        diff_data("ZI")
        print()
        print()
        diff_data("RO")
        print()
        print()
        diff_data("RW")
    if args.diff_obj:
        diff_obj()
    if args.diff_lib:
        diff_lib()
    if args.diff_all:
        diff_summary()

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        dest='input_dbs',
                        nargs='*',
                        required=True,
                        metavar='input_dbs',
                        help='Input two different data base files')
    parser.add_argument('-a', '--diff_all',
                        dest='diff_all',
                        action='store_true',
                        help='diff summary')
    parser.add_argument('-f', '--diff_function',
                        dest='diff_function',
                        action='store_true',
                        help='diff function')
    parser.add_argument('-d', '--diff_data',
                        dest='diff_data',
                        action='store_true',
                        help='diff data')
    parser.add_argument('-o', '--diff_obj',
                        dest='diff_obj',
                        action='store_true',
                        help='diff object file')
    parser.add_argument('-l', '--diff_lib',
                        dest='diff_lib',
                        action='store_true',
                        help='diff library')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main(parse_args())
    exit(0)
