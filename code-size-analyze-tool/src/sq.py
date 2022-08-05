# ------------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# ------------------------------------------------------------------------------

import sqlite3
from xlsxwriter.workbook import Workbook

class SQ(object):
    """
    Class SQ is used to create a new sqlite3 database and search the information
    of functions, data, sections, libraries, object files from map file. Then
    store the result into the database for further usage.

    - Methods:
      - SQ().update()  - Create and update the database.

    - Variables:
      - SQ().armcc     - ARMCLANG option.
      - SQ().gnuarm    - GNUARM option.
      - SQ().map_file  - The map file path which detail information comes from.
      - SQ().db_name   - The database file name to be saved.
    """
    def __init__(self):
        """
        Initialize variables.
        """
        self.gnuarm = False
        self.armcc = False
        self.map_file = ""
        self.db_name = ""

        self.__gnuarm_info = []
        self.__sec_dict = {}
        self.__excel_name = ""

    def __new(self):
        """
        Create tables in a new empty database.
        """
        self.__con = sqlite3.connect(self.db_name)
        self.__cur = self.__con.cursor()
        self.__excel_name = self.db_name +'.xlsx'
        self.__cur.execute('''create table Summary
                             (Code               INT     NOT NULL,
                              RO_data            INT     NOT NULL,
                              RW_data            INT     NOT NULL,
                              ZI_data            INT     NOT NULL,
                              EXTRA_FLASH        INT     NOT NULL,
                              EXTRA_RAM          INT     NOT NULL,
                              Flash              INT     NOT NULL,
                              RAM                INT     NOT NULL);''')
        self.__cur.execute('''create table Section
                             (name               TEXT    NOT NULL,
                              size               INT     NOT NULL,
                              address            TEXT    NOT NULL,
                              pad_size           INT     NOT NULL);''')
        self.__cur.execute('''create table Function
                             (name               TEXT    NOT NULL,
                              section            TEXT    NOT NULL,
                              size               INT     NOT NULL,
                              base_addr          TEXT    NOT NULL,
                              obj_file           TEXT    NOT_NULL,
                              lib_file           TEXT    NOT_NULL);''')
        self.__cur.execute('''create table Data
                             (name               TEXT    NOT NULL,
                              section            TEXT    NOT NULL,
                              size               INT     NOT NULL,
                              base_addr          TEXT    NOT NULL,
                              type               TEXT    NOT NULL,
                              obj_file           TEXT    NOT_NULL,
                              lib_file           TEXT    NOT_NULL);''')
        self.__cur.execute('''create table Library
                             (name               TEXT    NOT NULL,
                              size               INT     NOT NULL,
                              ramsize            INT     NOT NULL,
                              code               INT     NOT NULL,
                              rodata             INT     NOT NULL,
                              rwdata             INT     NOT NULL,
                              zidata             INT     NOT NULL,
                              incdata            INT     NOT_NULL,
                              Debug              INT     NOT NULL);''')
        self.__cur.execute('''create table Object
                             (name               TEXT    NOT NULL,
                              lib_file           TEXT    NOT NULL,
                              size               INT     NOT NULL,
                              ramsize            INT     NOT NULL,
                              code               INT     NOT NULL,
                              rodata             INT     NOT NULL,
                              rwdata             INT     NOT NULL,
                              zidata             INT     NOT NULL,
                              incdata            INT     NOT_NULL,
                              Debug              INT     NOT NULL);''')
        self.__cur.execute('''create table Compiler
                             (Compiler           TEXT    NOT NULL,
                              flag               INT     NOT NULL);''')
        if self.gnuarm:
            self.__cur.execute('''create table Unknown
                             (name               TEXT    NOT NULL,
                              section            TEXT    NOT NULL,
                              size               INT     NOT NULL,
                              base_addr          TEXT    NOT NULL,
                              type               TEXT    NOT NULL,
                              obj_file           TEXT    NOT_NULL,
                              lib_file           TEXT    NOT_NULL);''')

    def __collect_compiler(self):
        if self.gnuarm:
            self.__cur.execute("insert into Compiler values (?, ?)", ("gnuarm", 1))
        if self.armcc:
            self.__cur.execute("insert into Compiler values (?, ?)", ("armcc", 0))

    def __collect_summary(self):
        code_size = ro_data = rw_data = zi_data = flash_size = ram_size = extra_ram = extra_flash = 0
        if self.gnuarm:
            max_ram_addr = max_flash_addr = max_addr_ram_sym_size = max_addr_flash_sym_size = 0
            flash_start_addr, x, ram_start_addr, y = self.__get_ram_and_flash_start_addr()
            for s in self.__gnuarm_info:
                if s[3] == "text":
                    code_size += s[1]
                if s[3] == "rodata":
                    ro_data += s[1]
                if s[3] == "data":
                    rw_data += s[1]
                if s[3] == "bss":
                    zi_data += s[1]
                if s[3] == "unknown_ram":
                    extra_ram += s[1]
                if s[3] == "unknown_flash":
                    extra_flash += s[1]

            for s in self.__sec_dict.keys():
                if self.__sec_dict[s]['type'] == 'ram':
                    max_ram_addr = max(max_ram_addr, int(self.__sec_dict[s]['addr'], 16))
                    max_addr_ram_sym_size = self.__sec_dict[s]['size']
                    ram_size = max_ram_addr - ram_start_addr + max_addr_ram_sym_size

                    """
                    Some special sections like 'psp_stack' or 'heap' are pre-allocated,
                    and filled with zero. They are belonging to bss/ZI part.
                    """
                    if self.__sec_dict[s]['size'] == self.__sec_dict[s]['fill']:
                        zi_data += self.__sec_dict[s]['size']
                if self.__sec_dict[s]['type'] == 'flash':
                    max_flash_addr = max(max_flash_addr, int(self.__sec_dict[s]['addr'], 16))
                    max_addr_flash_sym_size = self.__sec_dict[s]['size']
                    flash_size = max_flash_addr - flash_start_addr + max_addr_flash_sym_size

            """
            For Secure image, the TFM_DATA part is loaded from Flash.
            """
            for line in open(self.map_file, "r"):
                if line.find("load address") >= 0:
                    extra_flash_addr = int(line.split()[-1] ,16)
                    extra_flash_data = int(line.split()[-4], 16)
                    if extra_flash_addr == max_flash_addr + max_addr_flash_sym_size:
                        flash_size += extra_flash_data

        elif self.armcc:
            for line in open(self.map_file, "r"):
                if line.find("gram Size: Code=") > 0:
                    content = line.split()
                    code_size = int(content[2].split('=')[1])
                    ro_data = int(content[3].split('=')[1])
                    rw_data = int(content[4].split('=')[1])
                    zi_data = int(content[5].split('=')[1])
            flash_size = code_size + ro_data + rw_data
            ram_size = rw_data + zi_data

        self.__cur.execute("insert into Summary values (?,?,?,?,?,?,?,?)",
                            (code_size,
                            ro_data,
                            rw_data,
                            zi_data,
                            extra_flash,
                            extra_ram,
                            flash_size,
                            ram_size))

    def __collect_section(self):
        if self.gnuarm:
            for s in self.__gnuarm_info:
                if s[3] == "text":
                    self.__cur.execute("insert into Function values (?,?,?,?,?,?)",
                                (s[0], s[6], s[1], s[2], s[4], s[5]))
                elif s[3] == "rodata":
                    self.__cur.execute("insert into Data values (?,?,?,?,?,?,?)",
                                (s[0], s[6], s[1], s[2], "RO", s[4], s[5]))
                elif s[3] == "data":
                    self.__cur.execute("insert into Data values (?,?,?,?,?,?,?)",
                                (s[0], s[6], s[1], s[2], "RW", s[4], s[5]))
                elif s[3] == "bss":
                    self.__cur.execute("insert into Data values (?,?,?,?,?,?,?)",
                                (s[0], s[6], s[1], s[2], "ZI", s[4], s[5]))
                else:
                    self.__cur.execute("insert into Unknown values (?,?,?,?,?,?,?)",
                                (s[0], s[6], s[1], s[2], s[3], s[4], s[5]))
            for s in self.__sec_dict.keys():
                self.__cur.execute("insert into Section values (?,?,?,?)",
                                (self.__sec_dict[s]['name'],
                                 self.__sec_dict[s]['size'],
                                 self.__sec_dict[s]['addr'],
                                 self.__sec_dict[s]['fill']))
        elif self.armcc:
            line_idx, line_start = 0, 0
            section_name = ""
            section_addr = ""
            section_size = 0
            section_pad_size = 0
            for line in open(self.map_file, "r"):
                line_idx += 1

                if line.find("Execution Region") > 0:
                    if len(section_name) > 0:
                        self.__cur.execute("insert into Section values (?,?,?,?)",
                                            (section_name,
                                            section_size,
                                            section_addr,
                                            section_pad_size))
                    line_start = line_idx + 1

                    content = line.split()
                    if len(content) >= 10:
                        section_name = content[2]
                        section_addr = content[4][:-1]
                        section_size = int(content[6][:-1], 16)
                        section_pad_size = 0
                if line.find("PAD\n") > 0 and line_idx > line_start and line_start > 0:
                    section_pad_size += int(line.split()[1], 16)
                if line.find("  Code  ") > 0:
                    content = line.split()
                    if len(content) >= 7:
                        if line.find(" * ") > 0:
                            content.remove("*")
                        func_name = content[5].strip().split('.')[-1]
                        if content[6].find('(') > 0:
                            object_file = content[6][content[6].find('(') + 1: -1]
                            lib_file = content[6][:content[6].find('(')]
                        else:
                            object_file = lib_file = content[6]
                        self.__cur.execute("insert into Function values (?,?,?,?,?,?)",
                                            (func_name,
                                            section_name,
                                            int(content[1].strip(), 16),
                                            content[0].strip(),
                                            object_file,
                                            lib_file))
                if line.find("  Data  ") > 0 or line.find("  Zero  ") > 0:
                    content = line.split()
                    if len(content) == 7:
                        if content[2] == "Zero":
                            data_type = "ZI"
                        else:
                            data_type = content[3]
                        data_name = content[5].strip()
                        if content[6].find('(') > 0:
                            object_file = content[6][content[6].find('(') + 1: -1]
                            lib_file = content[6][:content[6].find('(')]
                        else:
                            object_file = lib_file = content[6]
                        self.__cur.execute("insert into Data values (?,?,?,?,?,?,?)",
                                            (data_name,
                                            section_name,
                                            int(content[1].strip(), 16),
                                            content[0].strip(),
                                            data_type,
                                            object_file,
                                            lib_file))

    def __collect_library(self):
        if self.gnuarm:
            lib_detail_list = self.__collect_set(5)
            for s in lib_detail_list:
                self.__cur.execute("insert into Library values (?,?,?,?,?,?,?,?,?)",
                                    (s['name'],
                                     s['Code']+ s['RO'] + s['RW'],
                                     s['RW'] + s['ZI'],
                                     s['Code'],
                                     s['RO'],
                                     s['RW'],
                                     s['ZI'],
                                     0, 0))

        elif self.armcc:
            line_idx, line_start = 0, 0
            for line in open(self.map_file, "r"):
                line_idx += 1
                if line.find("Code (inc. data)   RO Data    RW Data    ZI Data      Debug   Library Name") > 0:
                    line_start = line_idx + 1
                if line_idx > line_start and line_start > 0:
                    content = line.split()
                    if len(content) == 7:
                        self.__cur.execute("insert into Library values (?,?,?,?,?,?,?,?,?)",
                                            (content[6],
                                            int(content[0]) + int(content[2]) + int(content[3]),
                                            int(content[3]) + int(content[4]),
                                            content[0],
                                            content[2],
                                            content[3],
                                            content[4],
                                            content[1],
                                            content[5]))
                    else:
                        break

    def __collect_obj(self):
        if self.gnuarm:
            obj_lib = ""
            obj_detail_list = self.__collect_set(4)
            for s in obj_detail_list:
                for t in self.__gnuarm_info:
                    if t[4] == s['name']:
                        obj_lib = t[5]
                        break
                self.__cur.execute("insert into Object values (?,?,?,?,?,?,?,?,?,?)",
                                    (s['name'],
                                     obj_lib,
                                     s['Code']+ s['RO'] + s['RW'],
                                     s['RW'] + s['ZI'],
                                     s['Code'],
                                     s['RO'],
                                     s['RW'],
                                     s['ZI'],
                                     0, 0))
        elif self.armcc:
            line_idx, line_start = 0, 0
            for line in open(self.map_file, "r"):
                line_idx += 1
                if line.find("Code (inc. data)   RO Data    RW Data    ZI Data      Debug   Object Name") > 0:
                    line_start = line_idx + 1
                if line_idx > line_start and line_start > 0:
                    content = line.split()
                    if len(content) == 7:
                        self.__cur.execute("insert into Object values (?,?,?,?,?,?,?,?,?,?)",
                                            (content[6],
                                            "no library",
                                            int(content[0]) + int(content[2]) + int(content[3]),
                                            int(content[3]) + int(content[4]),
                                            content[0],
                                            content[2],
                                            content[3],
                                            content[4],
                                            content[1],
                                            content[5]))
                    else:
                        break
            line_idx, line_start = 0, 0
            for line in open(self.map_file, "r"):
                line_idx += 1
                if line.find("Code (inc. data)   RO Data    RW Data    ZI Data      Debug   Library Member Name") > 0:
                    line_start = line_idx + 1
                if line_idx > line_start and line_start > 0:
                    content = line.split()
                    if len(content) == 7:
                        obj_name = content[6]
                        library_file = ""
                        for line in open(self.map_file, "r"):
                            if line.find(obj_name) > 0:
                                ch_r = line[line.find(obj_name) + len(obj_name)]
                                ch_l = line[line.find(obj_name) - 1]
                                if ch_l == '(' and ch_r == ')':
                                    library_file = line.split()[6][:line.split()[6].find('(')]
                        if len(library_file) == 0:
                            library_file = "no library"
                        self.__cur.execute("insert into Object values (?,?,?,?,?,?,?,?,?,?)",
                                            (content[6],
                                            library_file,
                                            int(content[0]) + int(content[2]) + int(content[3]),
                                            int(content[3]) + int(content[4]),
                                            content[0],
                                            content[2],
                                            content[3],
                                            content[4],
                                            content[1],
                                            content[5]))
                    else:
                        break

    def __get_ram_and_flash_start_addr(self):
        start = False
        for line in open(self.map_file, "r"):
            if line.find('Memory Configuration') >= 0:
                start = True
            if line.find('Linker script and memory map') == 0:
                break
            if start:
                if line.find('FLASH') == 0:
                    flash_start_addr = int(line.split()[1].strip(), 16)
                    flash_end_addr = int(line.split()[1].strip(), 16) + int(line.split()[2].strip(), 16)
                if line.find('RAM') == 0:
                    ram_start_addr = int(line.split()[1].strip(), 16)
                    ram_end_addr = int(line.split()[1].strip(), 16) + int(line.split()[2].strip(), 16)
        return flash_start_addr, flash_end_addr, ram_start_addr, ram_end_addr

    def __get_info_from_gnuarm_map(self):
        def get_key_content():
                start, end, real_start = False, False, False
                content = ""
                for line in open(self.map_file, "r"):
                    if line.find('Linker script and memory map') >= 0:
                        start = True
                    if line.find('OUTPUT(') == 0:
                        end = True
                    if start and not real_start:
                        if(line[0] == '.'):
                            real_start = True
                    if real_start and not end:
                        content += line
                return content.split('\n')[:-2]

        def output_to_gnuarm_info():
            type_founded = False
            info = [cur_sym_name, cur_sym_size, cur_sym_addr, "type", obj, lib, cur_sec_name]
            for type in ["text", "data", "bss", "rodata"]:
                info[3] = type
                if cur_sym_name.find('.' + type) == 0:
                    if cur_sym_name.find('.' + type + '.') == 0:
                        info[0] = cur_sym_name[len(type)+2:]
                        self.__gnuarm_info.append(info)
                        type_founded = True
                        break
                    self.__gnuarm_info.append(info)
                    type_founded = True
            if not type_founded:
                if int(cur_sym_addr,16) >= flash_start_addr and int(cur_sym_addr,16) <= flash_end_addr:
                    info[3] = "unknown_flash"
                    self.__gnuarm_info.append(info)
                if int(cur_sym_addr,16) >= ram_start_addr and int(cur_sym_addr,16) <= ram_end_addr:
                    info[3] = "unknown_ram"
                    self.__gnuarm_info.append(info)

        def get_obj_and_lib(line):
            lib = line[line.rfind('/') + 1:line.rfind('.o') + 2]
            obj = lib[lib.find("(") + 1:lib.rfind('.o')] + '.o'
            if lib.find('(') > 0:
                lib = lib[:lib.find("(")]
            else:
                lib = "no library"
            return lib, obj

        def get_part_list(idx):
            ret = []
            while len(lines[idx]) > 0 and lines[idx].split()[0].find('0x0000') >= 0:
                if len(lines[idx].split()) == 2:
                    cur_addr = lines[idx].split()[0].strip()
                    cur_name = lines[idx].split()[1].strip()
                    if cur_sym_name.find(cur_name) >= 0:
                        break
                    else:
                        delta = -1
                        cur_idx = idx + 1
                        next_addr = ''
                        while len(lines[cur_idx]) >= 0:
                            if lines[cur_idx].find('0x0000') >= 0:
                                for s in lines[cur_idx].split():
                                    if s.find('0x0000') >= 0:
                                        next_addr = s.strip()
                                        delta = int(next_addr, 16) - int(cur_addr, 16)
                                if delta >= 0:
                                    break
                            cur_idx += 1
                        ret.append(['0x' + cur_addr[-8:], cur_sym_name+'.'+cur_name, delta])
                else:
                    break
                idx += 1
            return ret

        lines = get_key_content()
        i_max = len(lines)
        part_list = []
        cur_sym_name, cur_sym_addr, cur_sym_size, lib, obj = "", "", "", "", ""
        flash_start_addr , flash_end_addr , ram_start_addr , ram_end_addr = self.__get_ram_and_flash_start_addr()
        for i in range(i_max):
            lib, obj = "no_library", "no_object"
            if len(lines[i]) > 0 and lines[i][0] == '.':
                cur_sec_name = lines[i].split()[0][1:]
                if len(lines[i].split()) > 1:
                    cur_sec_addr = lines[i].split()[1]
                    cur_sec_size = lines[i].split()[2]
                else:
                    cur_sec_addr = lines[i+1].split()[0]
                    cur_sec_size = lines[i+1].split()[1]
                    if cur_sec_addr.find('0x00') < 0:
                        continue
                if int(cur_sec_addr,16) >= flash_start_addr and int(cur_sec_addr,16) <= flash_end_addr:
                    self.__sec_dict[cur_sec_name] = {'name': cur_sec_name,
                                                     'addr': '0x' + cur_sec_addr[-8:],
                                                     'fill': 0,
                                                     'size': int(cur_sec_size, 16),
                                                     'type': 'flash'}
                if int(cur_sec_addr,16) >= ram_start_addr and int(cur_sec_addr,16) <= ram_end_addr:
                    self.__sec_dict[cur_sec_name] = {'name': cur_sec_name,
                                                     'addr': '0x' + cur_sec_addr[-8:],
                                                     'fill': 0,
                                                     'size': int(cur_sec_size, 16),
                                                     'type': 'ram'}

            if len(lines[i]) > 0 and lines[i][0] == ' ' and lines[i][1] != ' ':
                cur_sym_name = lines[i].split()[0].strip()
                if len(lines[i].split()) > 2:
                    cur_sym_addr = lines[i].split()[1].strip()
                    cur_sym_size = lines[i].split()[2].strip()
                    if cur_sym_addr.find('0x00') == 0 and cur_sym_size.find('0x') == 0:
                        cur_sym_addr = '0x' + cur_sym_addr[-8:]
                        cur_sym_size = int(cur_sym_size, 16)
                        if lines[i].find('/') > 0:
                            lib, obj = get_obj_and_lib(lines[i])
                        part_list = get_part_list(i+1)
                    else:
                        continue

                elif len(lines[i+1]) > 0 and lines[i+1].split()[0].find('0x00') >= 0:
                    cur_sym_addr = lines[i+1].split()[0].strip()
                    cur_sym_size = lines[i+1].split()[1].strip()
                    if cur_sym_addr.find('0x00') == 0 and cur_sym_size.find('0x') == 0:
                        cur_sym_addr = '0x' + cur_sym_addr[-8:]
                        cur_sym_size = int(cur_sym_size, 16)
                        if lines[i+1].find('/') > 0:
                            lib, obj = get_obj_and_lib(lines[i+1])
                        part_list = get_part_list(i+2)
                    else:
                        continue
                else:
                    continue

                if cur_sym_name.find("*fill*") >= 0 and cur_sec_name in self.__sec_dict.keys():
                    self.__sec_dict[cur_sec_name]['fill'] += cur_sym_size
                    continue

                if len(part_list) > 0:
                    for s in part_list:
                        cur_sym_addr = s[0]
                        cur_sym_name = s[1]
                        cur_sym_size = s[2]
                        output_to_gnuarm_info()
                else:
                    output_to_gnuarm_info()

    def __output_to_excel(self):
        def transform_db_2_excel(table_name):
            worksheet = workbook.add_worksheet(name=table_name)
            cursor = self.__cur.execute('select * from {}'.format(table_name))
            names = list(map(lambda x: x[0], cursor.description))
            len_list = []
            for s in names:
                len_list.append(max(15, len(s)))
            for i in range(len(names)):
                worksheet.write(0, i, names[i], title_m)

            mysel = self.__cur.execute('select * from {}'.format(table_name))
            for i, row in enumerate(mysel):
                for j, value in enumerate(row):
                    len_list[j] = max(len_list[j], len(str(value)))
                    worksheet.write(i + 1, j, value, page_m)
                    worksheet.set_column(j, j, width=len_list[j])

        table_list = ["Summary", "Section", "Library", "Object", "Function", "Data"]
        if self.gnuarm:
            table_list.append("Unknown")
        workbook = Workbook(self.__excel_name)
        title_m = workbook.add_format({'bold': True,
                                       'align': 'left',
                                       'font_size': 12})
        page_m = workbook.add_format({'align': 'left',
                                      'font_size': 10})
        for table in table_list:
            transform_db_2_excel(table)
        workbook.close()

    def __collect_set(self, index):
        name_list = []
        detail_list = []
        for s in self.__gnuarm_info:
            if s[index] not in name_list:
                name_list.append(s[index])
                if s[3] == "text":
                    detail_list.append({'name': s[index], 'Code':s[1],'ZI':0, 'RO':0,'RW':0})
                if s[3] == "rodata":
                    detail_list.append({'name': s[index], 'Code':0,'ZI':0, 'RO':s[1],'RW':0})
                if s[3] == "data":
                    detail_list.append({'name': s[index], 'Code':0,'ZI':0, 'RO':0,'RW':s[1]})
                if s[3] == "bss":
                    detail_list.append({'name': s[index], 'Code':0,'ZI':s[1], 'RO':0,'RW':0})
            else:
                for t in detail_list:
                    if t['name'] == s[index]:
                        if s[3] == "text":
                            t['Code'] += s[1]
                        if s[3] == "rodata":
                            t['RO'] += s[1]
                        if s[3] == "data":
                            t['RW'] += s[1]
                        if s[3] == "bss":
                            t['ZI'] += s[1]
        return detail_list

    def update(self):
        """
        Create the database and collect information from map file, then store
        it into the database, and write to excel file for further usage.
        """
        self.__new()
        if self.gnuarm:
            self.__get_info_from_gnuarm_map()
        self.__collect_compiler()
        self.__collect_summary()
        self.__collect_section()
        self.__collect_library()
        self.__collect_obj()
        self.__con.commit()
        self.__output_to_excel()
        self.__con.close()
