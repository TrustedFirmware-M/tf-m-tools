# -----------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import sqlite3
import argparse
import os
import glob
import curses
import curses.textpad

line1 = "─" * 128
line2 = "-" * 128
none_databse = "Cannot find database file! Please use this command to create \
databse:\n\n\tpython3 code_size_analyze.py -i <map file path>\n"
cmd_file="Enter the file name:"
cmd_func="Enter the function name:"
cmd_data="Enter the data name:"

class UI(object):
    UP, DOWN = -1, 1

    def __init__(self):
        """
        Initialize variables.
        """
        self.con = sqlite3.connect("data.db")
        self.cur = self.con.cursor()

        # Window variables
        self.window = None
        self.width = 0
        self.height = 0

        # Page variables
        self.items = []

        # Menu variables
        self.menu_depth = 0
        self.detail = 0
        self.section_detail = 0

        # Internal variables
        self.file_name = ""
        self.function_name = ""
        self.data_name = ""
        self.section_name = ""
        self.library_name = ""
        self.obj_file = ""

    def init_curses(self):
        """
        Setup the curses
        """
        self.window = curses.initscr()
        self.window.keypad(True)

        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.current = curses.color_pair(2)
        self.height, self.width = self.window.getmaxyx()

        self.max_lines = curses.LINES - 1
        self.top = 0

        self.bottom = len(self.items)
        self.current = 0
        self.current_x = 0
        self.page = self.bottom // self.max_lines

    def run(self):
        """
        Continue running the TUI until get interrupted
        """
        # Create window.
        self.init_curses()
        try:
            self.draw_page()
            self.input_stream()     # Get keys input
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()

    def input_stream(self):
        """
        Waiting an input and run a proper method according to type of input
        """
        while True:
            self.display()

            ch = self.window.getch()
            if ch == curses.KEY_UP:
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif ch == curses.KEY_LEFT:
                self.current_x = max(self.current_x - 1, 0)
            elif ch == curses.KEY_RIGHT:
                self.current_x = self.current_x + 1
            # If press 'q' or 'Q', escape this page
            elif ch ==  ord('q') or ch == ord('Q'):
                if self.menu_depth == 0:
                    break
                self.menu_depth = max(self.menu_depth - 1, 0)
                self.draw_page()
            # If press ENTER, get into next page if it exists
            elif ch == 10:
                self.get_menu_choose()
                self.menu_depth = self.menu_depth + 1
                self.draw_page()
            # If press ':', get target name form input line
            elif ch == 58:
                if self.menu_depth == 1:
                    # Search functions or data
                    if self.detail == 3:
                        self.draw_function_page(self.get_input_line_msg(cmd_func))
                    if self.detail == 4:
                        self.draw_data_page(self.get_input_line_msg(cmd_data))
            # If press 's' or 'S', save to file
            elif ch == ord('s') or ch == ord('S'):
                self.save_file(self.get_input_line_msg(cmd_file))

    def get_input_line_msg(self, cmd):
        """
        Get message from input line.
        """
        self.window.addstr(self.height - 1, 0,
                           cmd,
                           curses.color_pair(2))
        self.input_line = curses.newwin(1,
                                        curses.COLS - 2 - len(cmd),
                                        curses.LINES-1,
                                        len(cmd) + 1)
        self.input_box = curses.textpad.Textbox(self.input_line)
        self.window.refresh()
        self.input_box.edit()
        ret = self.input_box.gather()[:len(self.input_box.gather())-1]
        self.display()
        self.input_line.clear()
        return ret

    def save_file(self, output_file_name):
        """
        Save to files
        """
        fo = open(output_file_name + '.txt', "w")
        for s in self.items:
            fo.write(s + '\n')
        fo.close()

    def scroll(self, direction):
        """
        Scrolling the window when pressing up/down arrow keys
        """
        next_line = self.current + direction
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        if (direction == self.DOWN) and (next_line == self.max_lines) and \
                (self.top + self.max_lines < self.bottom):
            self.top += direction
            return
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        if (direction == self.DOWN) and (next_line < self.max_lines) and \
                (self.top + next_line < self.bottom):
            self.current = next_line
            return

    def paging(self, direction):
        """
        Paging the window when pressing left/right arrow keys
        """
        current_page = (self.top + self.current) // self.max_lines
        next_page = current_page + direction
        if next_page == self.page:
            self.current = min(self.current, self.bottom % self.max_lines - 1)
        if (direction == self.UP) and (current_page > 0):
            self.top = max(0, self.top - self.max_lines)
            return
        if (direction == self.DOWN) and (current_page < self.page):
            self.top += self.max_lines
            return

    def display(self):
        """
        Display the items on window
        """
        self.window.erase()
        for idx, item in enumerate(self.items[self.top:self.top +
                                              self.max_lines]):
            if idx == self.current:
                self.window.addstr(idx, 0,
                                   item[self.current_x:self.current_x +
                                        self.width],
                                   curses.color_pair(2))
            else:
                self.window.addstr(idx, 0,
                                   item[self.current_x:self.current_x +
                                        self.width],
                                   curses.color_pair(1))
        self.window.refresh()

    def draw_page(self):
        """
        Draw different page with menu_depth, detail and section_detail.
        """
        if self.menu_depth == 0:
            self.draw_file_page()
        elif self.menu_depth == 1:
            if self.detail == 1:
                self.draw_summary_page()
            if self.detail == 2:
                self.draw_section_page()
            if self.detail == 3:
                self.draw_function_page("")
            if self.detail == 4:
                self.draw_data_page("")
            if self.detail == 5:
                self.draw_library_page()
            if self.detail == 6:
                self.draw_obj_page()
        elif self.menu_depth == 2:
            if self.detail == 2:
                self.draw_section_detail_page()
            if self.detail == 3:
                self.draw_function_detail_page()
            if self.detail == 4:
                self.draw_data_detail_page()
            if self.detail == 5:
                self.draw_library_detail_page()
            if self.detail == 6:
                self.draw_obj_detail_page()
        # Draw section detail menu, here self.detail is 2
        elif self.menu_depth == 3 and self.detail == 2:
            if self.section_detail == 1:
                self.draw_section_lib()
            if self.section_detail == 2:
                self.draw_section_func()
            if self.section_detail == 3:
                self.draw_section_data()
        # Only section detail menu can move to menu depth 5, here function
        # detail and data detail are also supported.
        elif self.menu_depth == 4:
            if self.section_detail == 2:
                self.draw_function_detail_page()
            if self.section_detail == 3:
                self.draw_data_detail_page()

        # Refresh page variables
        self.bottom = len(self.items)
        self.current = 0
        self.current_x = 0
        self.top = 0
        self.page = self.bottom // self.max_lines

    def get_menu_choose(self):
        """
        Get options from menus or specific objects like function, data, library
        or object files.
        """

        """
        First page, menu_depth = 1
            =============================
            Current file: tfm_s.axf
            1. Summary Info          -->
            2. Section Module        -->
            3. Function detail       -->
            4. Data detail           -->
            5. Library Summary       -->
            6. Object files Summary  -->
            =============================
        It will change the self.detail's value in range 1 - 6
        """
        if self.menu_depth == 0:
            if self.current + self.top > 0:
                self.detail = self.current
            else:
                # Except first line
                self.menu_depth = self.menu_depth - 1
        if self.menu_depth == 1:
            if self.current + self.top > 0:
                # Get section name which will be used to draw its detail page in
                # draw_page() function.
                if self.detail == 2:
                    self.section_name = \
                        self.items[self.top + self.current].split()[0]
                # Get function name and its object file to avoid same name
                # situation. Function name will be used to draw its detail page
                # in draw_page() function.
                elif self.detail == 3:
                    self.function_name = \
                        self.items[self.top + self.current].split()[0]
                    self.obj_file = \
                        self.items[self.top + self.current].split()[4]
                # Get data name and its object file name to avoid same name
                # situation. Data name will be used to draw its detail page in
                # draw_page() function.
                elif self.detail == 4:
                    self.data_name = \
                        self.items[self.top + self.current].split()[0]
                    self.obj_file = \
                        self.items[self.top + self.current].split()[5]
                # Get library name which will be used to draw its detail page in
                # draw_page() function.
                elif self.detail == 5:
                    self.library_name = \
                        self.items[self.top + self.current].split()[0]
                # Get object file name which will be used to draw its detail
                # page in draw_page() function.
                elif self.detail == 6:
                    self.obj_file = \
                        self.items[self.top + self.current].split()[0]
                else:
                    # Other invalid choose will not change menu depth.
                    self.menu_depth = self.menu_depth - 1
            else:
                # Except first line
                self.menu_depth = self.menu_depth - 1
        """
        Section detail page, menu_depth = 1
            =============================
            Name :TFM_UNPRIV_CODE           Size :155544
            1. Summary           -->
            2. Function          -->
            3. Data              -->
            =============================
        It will change the self.section_detail's value in range 1 - 3
        """
        if self.menu_depth == 2:
            if self.current + self.top > 0:
                if self.detail == 2:
                    self.section_detail = self.current
                else:
                    # Only section page's detail can change menu depth.
                    self.menu_depth = self.menu_depth - 1
            else:
                # Except first line
                self.menu_depth = self.menu_depth - 1
        if self.menu_depth == 3:
            if self.current + self.top > 0:
                # Get function name and its object file to avoid same name
                # situation. Function name will be used to draw its detail page
                # in draw_page() function.
                if self.section_detail == 2:
                    self.function_name = \
                        self.items[self.top + self.current].split()[0]
                    self.obj_file = \
                        self.items[self.top + self.current].split()[4]
                # Get data name and its object file name to avoid same name
                # situation. Data name will be used to draw its detail page in
                # draw_page() function.
                elif self.section_detail == 3:
                    self.data_name = \
                        self.items[self.top + self.current].split()[0]
                    self.obj_file = \
                        self.items[self.top + self.current].split()[5]
                else:
                    # Other invalid choose will not change menu depth.
                    self.menu_depth = self.menu_depth - 1
            else:
                # Except first line
                self.menu_depth = self.menu_depth - 1
        if self.menu_depth == 4:
            # Max menu depth.
            self.menu_depth = self.menu_depth - 1

    def draw_file_page(self):
        self.items = ["Code Size Analysis Tool for Map File",
                      "1. Summary Info          -->",
                      "2. Section Module        -->",
                      "3. Function detail       -->",
                      "4. Data detail           -->",
                      "5. Library Summary       -->",
                      "6. Object files Summary  -->"]

    def draw_summary_page(self):
        """
        Get summary info from database and save into self.items.
        """
        cursor = self.cur.execute("select * from Summary")
        for row in cursor:
            self.items = ["Code size\t: {:<8}\t{:<4.2f}\tKB".
                          format(row[0], row[0]/1024),
                          "RO data\t\t: {:<8}\t{:<4.2f}\tKB".
                          format(row[1], row[1]/1024),
                          "RW data\t\t: {:<8}\t{:<4.2f}\tKB".
                          format(row[2], row[2]/1024),
                          "ZI data\t\t: {:<8}\t{:<4.2f}\tKB".
                          format(row[3], row[3]/1024),
                          "Flash size\t: {:<8}\t{:<4.2f}\tKB = Code + RO + RW".
                          format(row[4], row[4]/1024),
                          "RAM size\t: {:<8}\t{:<4.2f}\tKB = RW + ZI".
                          format(row[5], row[5]/1024)]
            break

    def draw_section_page(self):
        """
        Get section info from database and save into self.items.
        """
        self.items = ["{:<50}{:<16}{:<16}{:<16}".
                      format("Name", "Size", "Address", "PAD size")]

        cursor = self.cur.execute("select * from Section ORDER BY size DESC")
        for row in cursor:
            self.items.append("{:<50}{:<16}{:<16}{:<16}".
                              format(row[0], row[1], row[2], row[3]))

    def draw_section_detail_page(self):
        """
        Section detail page with a menu.
        """
        cursor = self.cur.execute("select * from Section WHERE name = '{}'".
                                  format(self.section_name))
        for row in cursor:
            self.items = ["Name :{}\t\tSize :{}".
                          format(self.section_name, row[1]),
                          "1. Summary           -->",
                          "2. Function          -->",
                          "3. Data              -->"]
            break

    def draw_section_lib(self):
        lib_dict, obj_dict = {}, {}
        lib_list, obj_list = [], []
        exsit_no_lib_obj = False
        tmp_list = []
        colums_name = "{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".format(
            "Name", "Flash", "RAM", "Code", "RO data", "RW data", "ZI data", "Total")
        count = 0

        """
        Get detail information with functions and data from tables in database
        with a dictionary in python.
        """
        cursor = self.cur.execute("select * from Function WHERE section = '{}' ORDER BY lib_file DESC".
                                  format(self.section_name))
        for row in cursor:
            lib_name = row[5]
            if lib_name in lib_dict.keys():
                lib_dict[lib_name]['Code'] += row[2]
            else:
                lib_dict[lib_name] = {'RO': 0, 'RW': 0,
                                      'Code': row[2], 'ZI': 0}

            obj_name = row[4]
            if obj_name in obj_dict.keys():
                obj_dict[obj_name]['Code'] += row[2]
            else:
                obj_dict[obj_name] = {'RO': 0, 'RW': 0,
                                      'Code': row[2], 'Lib': lib_name, 'ZI': 0}

        cursor = self.cur.execute("select * from Data WHERE section = '{}' ORDER BY lib_file DESC".
                                  format(self.section_name))
        for row in cursor:
            lib_name = row[6]
            if lib_name in lib_dict.keys():
                lib_dict[lib_name][row[4]] += row[2]
            else:
                lib_dict[lib_name] = {'RO': 0, 'RW': 0, 'Code': 0, 'ZI': 0}
                lib_dict[lib_name][row[4]] = row[2]

            obj_name = row[5]
            if obj_name in obj_dict.keys():
                obj_dict[obj_name][row[4]] += row[2]
            else:
                obj_dict[obj_name] = {'RO': 0,  'RW': 0,
                                      'Code': 0, 'Lib': lib_name, 'ZI': 0}
                obj_dict[obj_name][row[4]] = row[2]

        """
        Transform the dictionary to a dictionary list in python and sort the
        elements with total size.
        """
        for s in lib_dict.keys():
            lib_list.append({'Name': s,
                             'RO': lib_dict[s]['RO'],
                             'RW': lib_dict[s]['RW'],
                             'Code': lib_dict[s]['Code'],
                             'ZI': lib_dict[s]['ZI']})
        lib_list = sorted(lib_list,
                          key=lambda i: i['RO'] +
                          i['Code'] + i['RW'] + i['ZI'],
                          reverse=True)
        for s in obj_dict.keys():
            obj_list.append({'Name': s,
                             'RO': obj_dict[s]['RO'],
                             'RW': obj_dict[s]['RW'],
                             'Code': obj_dict[s]['Code'],
                             'Lib': obj_dict[s]['Lib'],
                             'ZI': obj_dict[s]['ZI']})
        obj_list = sorted(obj_list,
                          key=lambda i: i['RO'] +
                          i['Code'] + i['RW'] + i['ZI'],
                          reverse=True)

        def sum_data(data_list):
            """
            Calculate the sum of libraries or object files, and implement total
            data line. It will be added into self.items.
            """
            ret = {'RO': 0, 'RW': 0, 'Code': 0, 'ZI': 0,
                   'Flash': 0, 'Ram': 0, 'Total': 0}
            if len(data_list) > 0:
                for s in data_list:
                    ret['Code'] += s['Code']
                    ret['RO'] += s['RO']
                    ret['RW'] += s['RW']
                    ret['ZI'] += s['ZI']
                    ret['Flash'] += s['Code'] + s['RO'] + s['RW']
                    ret['Ram'] += s['RW'] + s['ZI']
            ret['Total'] = ret['Flash'] + ret['ZI']
            self.items.append(line2)
            self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format("Summary",
                                     ret['Flash'],
                                     ret['Ram'],
                                     ret['Code'],
                                     ret['RO'],
                                     ret['RW'],
                                     ret['ZI'],
                                     ret['Total']))
            self.items.append(line1)
            return ret

        def insert_column_line(title):
            """
            Quickly insert column line.
            """
            self.items.append(title)
            self.items.append(line2)
            self.items.append(colums_name)
            self.items.append(line2)

        def quick_insert_data_line(s):
            """
            Quickly insert a single data line.
            """
            self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(s['Name'],
                                     s['Code'] + s['RO'] + s['RW'],
                                     s['RW'] + s['ZI'],
                                     s['Code'],
                                     s['RO'],
                                     s['RW'],
                                     s['ZI'],
                                     s['Code'] + s['RO'] + s['RW'] + s['ZI']))
        """
        Dump library information.
        """
        self.items = [line1]
        insert_column_line("\t\t\t\t\t\t\tSection libraries")
        for s in lib_list:
            if s['Name'].find(".o") > 0:
                exsit_no_lib_obj = True
            else:
                tmp_list.append(s)
                quick_insert_data_line(s)
        sum_data(tmp_list)

        """
        Dump object file information.
        """
        insert_column_line("\t\t\t\t\t\t\tSection object files")
        for s in obj_list:
            quick_insert_data_line(s)
        ret = sum_data(obj_list)
        total_flash_size, total_ram_size = ret['Flash'], ret['Ram']

        """
        Dump NOT-IN-LIBRARY object file information.
        """
        if exsit_no_lib_obj:
            insert_column_line(
                "\t\t\t\t\t\t\tSection NOT-IN-LIBRARY object files")
            tmp_list = []
            for s in lib_list:
                if s['Name'].find(".o") > 0:
                    tmp_list.append(s)
                    quick_insert_data_line(s)
            sum_data(tmp_list)

        """
        Insert the summary information at the top of this page.
        """
        cursor = self.cur.execute(
            "select * from Section WHERE name = '{}'".format(self.section_name))
        for row in cursor:
            self.items.insert(0, "Section Name :{}\tTotal Size :{}\tFlash : {}\tRAM : {:<6}\tPad size = {}".
                              format(self.section_name, row[1], total_flash_size, total_ram_size, row[3]))
            break
        self.items.insert(0, line2)
        self.items.insert(0, "\t\t\t\t\t\t\tSection information")
        self.items.insert(0, line1)

        """
        Dump detail information of the section.
        """
        index = 4 * ' '
        self.items.append("\t\t\t\t\t\t\tDetail information")
        self.items.append(line2)
        for s in lib_list:
            self.items.append("{} Code Size = {} RO Data = {} RW Data = {} ZI Data = {}".
                              format(s['Name'], s['Code'], s['RO'], s['RW'], s['ZI']))
            for t in obj_list:
                if t['Lib'] == s['Name']:
                    self.items.append(index + "{} Code Size = {} RO Data = {} RW Data = {} ZI Data = {}".format(
                        t['Name'], t['Code'], t['RO'], t['RW'], t['ZI']))
                    count = 0
                    cursor = self.cur.execute("select * from Function WHERE section = '{}' and lib_file = '{}' and obj_file = '{}' ORDER BY size DESC".
                                              format(self.section_name,
                                                     s['Name'],
                                                     t['Name']))
                    for row in cursor:
                        if row and count == 0:
                            self.items.append(index * 2 + "Code size = {}".
                                              format(t['Code']))
                            count = count + 1
                        self.items.append(index * 3 + "{:<6} {} ".
                                          format(row[2], row[0]))

                    def get_certain_data(type_name, s, t):
                        count = 0
                        cursor = self.cur.execute("select * from Data WHERE section = '{}' and lib_file = '{}' and obj_file = '{}'  and type = '{}' ORDER BY size DESC".
                                                  format(self.section_name,
                                                         s['Name'],
                                                         t['Name'],
                                                         type_name))
                        for row in cursor:
                            if row and count == 0:
                                self.items.append(index * 2 + "{} Data = {}".
                                                  format(type_name, t[type_name]))
                                count = count + 1
                            self.items.append(index * 3 + "{:<6} {}".
                                              format(row[2], row[0]))

                    get_certain_data('RO', s, t)
                    get_certain_data('RW', s, t)
                    get_certain_data('ZI', s, t)
            self.items.append(line2)

    def draw_section_func(self):
        self.items = ["{:<50}{:<32}{:<10}{:<16}{:<40}{:<40}".
                      format("Name",
                             "Section",
                             "Size",
                             "Address",
                             "Object File",
                             "Library")]
        cursor = self.cur.execute("select * from Function WHERE section = '{}' ORDER BY size DESC".
                                  format(self.section_name))
        for row in cursor:
            self.items.append("{:<50}{:<32}{:<10}{:<16}{:<40}{:<40}".
                              format(row[0], row[1], row[2], row[3], row[4], row[5]))

    def draw_section_data(self):
        self.items = ["{:<50}{:<32}{:<10}{:<16}{:<16}{:<40}{:<40}".
                      format("Name",
                             "Section",
                             "Size",
                             "Address",
                             "Type",
                             "Object File",
                             "Library")]

        cursor = self.cur.execute("select * from Data WHERE section = '{}' ORDER BY size DESC".
                                  format(self.section_name))
        for row in cursor:
            data_name = row[0]
            if len(data_name) >= 50:
                data_name = data_name[:40] + "-->"
            self.items.append("{:<50}{:<32}{:<10}{:<16}{:<16}{:<40}{:<40}".
                              format(data_name, row[1], row[2], row[3], row[4], row[5], row[6]))

    def quick_append(self):
        self.items.append(line1)

        self.items.append("{:<50}{:<32}{:<10}{:<16}{:<40}".
                          format("Name",
                                 "Section",
                                 "Size",
                                 "Type",
                                 "Object File"))
        self.items.append(line2)

    def quick_append_data(self, cursor):
        flag = False
        for row in cursor:
            if not flag:
                self.quick_append()
            data_name = row[0]
            if len(data_name) >= 50:
                data_name = data_name[:40] + "-->"
            self.items.append("{:<50}{:<32}{:<10}{:<16}{:<40}".
                              format(data_name, row[1], row[2], row[4], row[5]))
            flag = True

    def draw_library_page(self):
        self.items = ["{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                      format("Name",
                             "Flash size",
                             "RAM size",
                             "Code",
                             "RO data",
                             "RW data",
                             "ZI data",
                             "Inc. data",
                             "Debug")]

        cursor = self.cur.execute(
            "select * from Library ORDER BY flashsize DESC")
        for row in cursor:
            self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    def draw_library_detail_page(self):
        flag = False
        """
        Draw title.
        """
        self.items = [line1, "{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                      format("Name",
                             "Flash size",
                             "RAM size",
                             "Code",
                             "RO data",
                             "RW data",
                             "ZI data",
                             "Inc. data"),
                      line2]

        cursor = self.cur.execute("select * from Library WHERE name = '{}'".
                                  format(self.library_name))
        for row in cursor:
            self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            break

        """
        Draw object files.
        """
        self.items.append(line1)
        self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                          format("Name",
                                 "Flash size",
                                 "RAM size",
                                 "Code",
                                 "RO data",
                                 "RW data",
                                 "ZI data",
                                 "Inc. data"))
        self.items.append(line2)

        cursor = self.cur.execute("select * from Object WHERE library = '{}' ORDER BY flashsize DESC".
                                  format(self.library_name))
        for row in cursor:
            self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

        """
        Draw functions.
        """
        cursor = self.cur.execute("select * from Function WHERE lib_file = '{}' ORDER BY size DESC".
                                  format(self.library_name))
        for row in cursor:
            if not flag:
                self.quick_append()
            self.items.append("{:<50}{:<32}{:<10}{:<16}{:<40}".
                              format(row[0], row[1], row[2], "Code", row[4]))
            flag = True

        """
        Draw RO data.
        """
        cursor = self.cur.execute("select * from Data WHERE type = 'RO' and lib_file = '{}' ORDER BY size DESC".
                                  format(self.library_name))
        self.quick_append_data(cursor)

        """
        Draw RW data.
        """
        cursor = self.cur.execute("select * from Data WHERE type = 'RW' and lib_file = '{}' ORDER BY size DESC".
                                  format(self.library_name))
        self.quick_append_data(cursor)

        """
        Draw ZI data.
        """
        cursor = self.cur.execute("select * from Data WHERE type = 'ZI' and lib_file = '{}' ORDER BY size DESC".
                                  format(self.library_name))
        self.quick_append_data(cursor)
        self.items.append(line1)

    def draw_obj_page(self):
        self.items = ["{:<50}{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                      format("Name",
                             "Library",
                             "Flash size",
                             "RAM size",
                             "Code",
                             "RO data",
                             "RW data",
                             "ZI data",
                             "Inc. data",
                             "Debug")]
        cursor = self.cur.execute(
            "select * from Object WHERE library = 'no library' ORDER BY flashsize DESC")
        for row in cursor:
            self.items.append("{:<50}{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
        cursor = self.cur.execute(
            "select * from Object WHERE library != 'no library' ORDER BY flashsize DESC")
        for row in cursor:
            self.items.append("{:<50}{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

    def draw_obj_detail_page(self):
        flag = False
        self.items = [line1,
                      "{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                      format("Name",
                             "Flash size",
                             "RAM size",
                             "Code",
                             "RO data",
                             "RW data",
                             "ZI data",
                             "Inc. data"),
                      line2]

        cursor = self.cur.execute("select * from Object WHERE name = '{}'".
                                  format(self.obj_file))
        for row in cursor:
            self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
            break

        cursor = self.cur.execute("select * from Function WHERE obj_file = '{}' ORDER BY size DESC".
                                  format(self.obj_file))
        for row in cursor:
            if not flag:
                self.quick_append()
            self.items.append("{:<50}{:<32}{:<10}{:<16}{:<40}".
                              format(row[0], row[1], row[2], "Code", row[4]))
            flag = True

        cursor = self.cur.execute("select * from Data WHERE type = 'RO' and obj_file = '{}' ORDER BY size DESC".
                                  format(self.obj_file))
        self.quick_append_data(cursor)

        cursor = self.cur.execute("select * from Data WHERE type = 'RW' and obj_file = '{}' ORDER BY size DESC".
                                  format(self.obj_file))
        self.quick_append_data(cursor)

        cursor = self.cur.execute("select * from Data WHERE type = 'ZI' and obj_file = '{}' ORDER BY size DESC".
                                  format(self.obj_file))
        self.quick_append_data(cursor)
        self.items.append(line1)

    def draw_function_page(self, search_func):
        self.items = []
        self.items.append("{:<50}{:<50}{:<10}{:<16}{:<40}{:<40}".
                          format("Name",
                                 "Section",
                                 "Size",
                                 "Address",
                                 "Object File",
                                 "Library"))
        if search_func:
            cursor = self.cur.execute("select * from Function WHERE name LIKE '%{}%'".
                                      format(search_func))
        else:
            cursor = self.cur.execute(
                "select * from Function ORDER BY size DESC")
        for row in cursor:
            self.items.append("{:<50}{:<50}{:<10}{:<16}{:<40}{:<40}".
                              format(row[0], row[1], row[2], row[3], row[4], row[5]))

    def draw_function_detail_page(self):
        if self.obj_file:
            cursor = self.cur.execute("select * from Function WHERE name = '{}' and obj_file = '{}'".
                                    format(self.function_name, self.obj_file))
        else:
            cursor = self.cur.execute("select * from Function WHERE name = '{}'".
                                    format(self.function_name))
        for row in cursor:
            self.items = ["=================================================",
                          "Name\t\t\t: {}".format(row[0]),
                          "Symbol type\t\t: Function",
                          "Section\t\t\t: {}".format(row[1]),
                          "Size\t\t\t: {}".format(row[2]),
                          "Base address\t\t: {}".format(row[3]),
                          "Object file\t\t: {}".format(row[4]),
                          "Library\t\t\t: {}".format(row[5]),
                          "================================================="]
            self.items.append("Called symbol:")
            content = row[6].split('|')
            for s in content:
                self.items.append("\t"+s)
            self.items.append("Dst symbol:")
            content = row[7].split('|')
            for s in content:
                self.items.append("\t"+s)

    def draw_data_page(self, search_data):
        self.items = ["{:<50}{:<50}{:<10}{:<16}{:<16}{:<40}{:<40}".
                      format("Name",
                             "Section",
                             "Size",
                             "Address",
                             "Type",
                             "Object File",
                             "Library")]
        if search_data:
            cursor = self.cur.execute("select * from Data WHERE name LIKE '%{}%'".
                                      format(search_data))
        else:
            cursor = self.cur.execute("select * from Data ORDER BY size DESC")
        for row in cursor:
            data_name = row[0]
            if len(data_name) >= 50:
                data_name = data_name[:40] + "-->"
            self.items.append("{:<50}{:<50}{:<10}{:<16}{:<16}{:<40}{:<40}".
                              format(data_name, row[1], row[2], row[3], row[4], row[5], row[6]))

    def draw_data_detail_page(self):
        if self.obj_file:
            cursor = self.cur.execute("select * from Data WHERE name = '{}' and obj_file = '{}'".
                                  format(self.data_name, self.obj_file))
        else:
            cursor = self.cur.execute("select * from Data WHERE name = '{}'".
                                  format(self.data_name))


        for row in cursor:
            self.items = ["=================================================",
                          "Name\t\t\t: {}".format(row[0]),
                          "Symbol type\t\t: {}".format(row[4]),
                          "Section\t\t\t: {}".format(row[1]),
                          "Size\t\t\t: {}".format(row[2]),
                          "Base address\t\t: {}".format(row[3]),
                          "Object file\t\t: {}".format(row[5]),
                          "Library\t\t\t: {}".format(row[6]),
                          "================================================="]
            self.items.append("Called symbol:")
            content = row[7].split('|')
            for s in content:
                self.items.append("\t"+s)
            self.items.append("Dst symbol:")
            content = row[8].split('|')
            for s in content:
                self.items.append("\t"+s)

def collect_summary():
    """
    Program Size: Code=181622 RO-data=26226 RW-data=3128 ZI-data=79364
    """
    cur.execute('''create table Summary
                (Code       INT     NOT NULL,
                 RO_data    INT     NOT NULL,
                 RW_data    INT     NOT NULL,
                 ZI_data    INT     NOT NULL,
                 Flash      INT     NOT NULL,
                 RAM        INT     NOT NULL
                );''')
    code_size = ro_data = rw_data = zi_data = flash_size = ram_size = 0
    if gnuarm:
        for s in gnuarm_info:
            if s[3] == "text":
                code_size += s[1]
            if s[3] == "rodata":
                ro_data += s[1]
            if s[3] == "data":
                rw_data += s[1]
            if s[3] == "bss":
                zi_data += s[1]
    elif armcc:
        for line in open(file_path, "r"):
            if line.find("gram Size: Code=") > 0:
                content = line.split()
                code_size = int(content[2].split('=')[1])
                ro_data = int(content[3].split('=')[1])
                rw_data = int(content[4].split('=')[1])
                zi_data = int(content[5].split('=')[1])
    flash_size = code_size + ro_data + rw_data
    ram_size = rw_data + zi_data
    cur.execute("insert into Summary values (?,?,?,?,?,?)",
                (code_size, ro_data, rw_data, zi_data, flash_size, ram_size))

def collect_section():
    cur.execute('''create table Section
                (name               TEXT                NOT NULL,
                 size               INT                 NOT NULL,
                 address            TEXT                NOT NULL,
                 pad_size           INT                 NOT NULL
                );''')
    cur.execute('''create table Function
                (name               TEXT                NOT NULL,
                 section            TEXT                NOT NULL,
                 size               INT                 NOT NULL,
                 base_addr          TEXT                NOT NULL,
                 obj_file           TEXT                NOT_NULL,
                 lib_file           TEXT                NOT_NULL,
                 called_symbol      STRING              NOT_NULL,
                 dst_symbol         STRING              NOT_NULL
                );''')
    cur.execute('''create table Data
                (name               TEXT                NOT NULL,
                 section            TEXT                NOT NULL,
                 size               INT                 NOT NULL,
                 base_addr          TEXT                NOT NULL,
                 type               TEXT                NOT NULL,
                 obj_file           TEXT                NOT_NULL,
                 lib_file           TEXT                NOT_NULL,
                 called_symbol      TEXT                NOT_NULL,
                 dst_symbol         TEXT                NOT_NULL
                );''')
    if gnuarm:
        for s in gnuarm_info:
            if s[3] == "text":
                cur.execute("insert into Function values (?, ?, ?, ?, ?, ?, ?, ?)",
                            (s[0], "Unknown", s[1], s[2], s[4], s[5], "", ""))
            if s[3] == "rodata":
                cur.execute("insert into Data values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (s[0], "Unknown", s[1], s[2], "RO", s[4], s[5], "", ""))
            if s[3] == "data":
                cur.execute("insert into Data values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (s[0], "Unknown", s[1], s[2], "RW", s[4], s[5], "", ""))
            if s[3] == "bss":
                cur.execute("insert into Data values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (s[0], "Unknown", s[1], s[2], "ZI", s[4], s[5], "", ""))
    elif armcc:
        """
        Execution Region TFM_UNPRIV_CODE (Base: 0x10085360, Size: 0x000327e0, Max: 0xffffffff, ABSOLUTE)

        Base Addr    Size         Type   Attr      Idx    E Section Name        Object

        0x10085360   0x00000008   Code   RO         3759  * !!!main             c_w.l(__main.o)
        0x10085368   0x00000034   Code   RO         4234    !!!scatter          c_w.l(__scatter.o)
        0x1008539c   0x0000005a   Code   RO         4232    !!dczerorl2         c_w.l(__dczerorl2.o)
        """
        line_idx, line_start = 0, 0
        section_name = ""
        section_addr = ""
        section_size = 0
        section_pad_size = 0
        for line in open(file_path, "r"):
            line_idx += 1

            if line.find("Execution Region") > 0:
                if len(section_name) > 0:
                    cur.execute("insert into Section values (?, ?, ?, ?)",
                                (section_name, section_size, section_addr, section_pad_size))
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
                    dst_symbol, called_symbol = "", ""
                    if content[6].find('(') > 0:
                        object_file = content[6][content[6].find(
                            '(') + 1: -1]
                        lib_file = content[6][:content[6].find(
                            '(')]
                    else:
                        object_file = lib_file = content[6]
                    for line in open(file_path, "r"):
                        if line.find(func_name) > 0:
                            if line.find("refers to {}({}".format(object_file, content[5].strip())) > 0 or line.find("refers (Special) to {}({}".format(object_file, content[5].strip())) > 0:
                                dst_symbol = dst_symbol + get_dst(line, func_name)
                            elif line.find("{}({}) refers to".format(object_file, content[5].strip())) > 0 or \
                                    line.find('{}({}) refers (Special) to'.format(object_file, content[5].strip())) > 0:
                                called_symbol = called_symbol + \
                                    get_src(line, func_name)
                    cur.execute("insert into Function values (?, ?, ?, ?, ?, ?, ?, ?)",
                                (func_name,
                                section_name,
                                int(content[1].strip(), 16),
                                content[0].strip(),
                                object_file,
                                lib_file,
                                called_symbol,
                                dst_symbol))
            if line.find("  Data  ") > 0 or line.find("  Zero  ") > 0:
                content = line.split()
                if len(content) == 7:
                    dst_symbol, called_symbol = "", ""
                    if content[2] == "Zero":
                        data_type = "ZI"
                    else:
                        data_type = content[3]
                    data_name = content[5].strip()
                    if content[6].find('(') > 0:
                        object_file = content[6][content[6].find(
                            '(') + 1: -1]
                        lib_file = content[6][:content[6].find(
                            '(')]
                    else:
                        object_file = lib_file = content[6]
                    for line in open(file_path, "r"):
                        if line.find(data_name) > 0:
                            if line.find("refers to {}({}".format(object_file, data_name)) > 0 or line.find("refers (Special) to {}({}".format(object_file, data_name)) > 0:
                                dst_symbol = dst_symbol + get_dst(line, data_name)
                            elif line.find("{}({}) refers to".format(object_file, data_name)) > 0 or \
                                    line.find('{}({}) refers (Special) to'.format(object_file, data_name)) > 0:
                                called_symbol = called_symbol + \
                                    get_src(line, data_name)
                    cur.execute("insert into Data values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (data_name,
                                section_name,
                                int(content[1].strip(), 16),
                                content[0].strip(),
                                data_type,
                                object_file,
                                lib_file,
                                called_symbol,
                                dst_symbol))

def format_info(content):
    if content:
        object_file = content[0:content.find('(')]
        target = content[content.find('(') + 1:content.find(')')]
        return "{:<50}".format(object_file) + ' : ' + target + '|'

def get_dst(line, target):
    ret = ""
    content = []
    if line.find('refers to') > 0:
        content = line.split('refers to')
    if line.find('refers (Special) to') > 0:
        content = line.split('refers (Special) to')
    if content and content[1].find(target) > 0:
        ret = format_info(content[0].strip())
    return ret

def get_src(line, target):
    ret = ""
    content = []
    if line.find('refers to') > 0:
        content = line.split('refers to')
    if line.find('refers (Special) to') > 0:
        content = line.split('refers (Special) to')
    if content and content[0].find(target) > 0:
        ret = format_info(content[1].strip())
    return ret

def collect_set(index):
    name_list = []
    detail_list = []
    for s in gnuarm_info:
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

def collect_library():
    cur.execute('''create table Library
                (name               TEXT                NOT NULL,
                 flashsize          INT                 NOT NULL,
                 ramsize            INT                 NOT NULL,
                 code               INT                 NOT NULL,
                 rodata             INT                 NOT NULL,
                 rwdata             INT                 NOT NULL,
                 zidata             INT                 NOT NULL,
                 incdata            INT                 NOT_NULL,
                 Debug              INT                 NOT NULL
                );''')
    if gnuarm:
        lib_detail_list = collect_set(5)
        for s in lib_detail_list:
            cur.execute("insert into Library values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (s['name'],
                                s['Code']+ s['RO'] + s['RW'],
                                s['RW'] + s['ZI'],
                                s['Code'],
                                s['RO'],
                                s['RW'],
                                s['ZI'],
                                0, 0))

    elif armcc:
        """
        Code (inc. data)   RO Data    RW Data    ZI Data      Debug   Library Name

        1520          0          0          0       1152        284   libtfm_app_rot_partition_core_test_2.a
         300         48          0          0       1032         64   libtfm_app_rot_partition_flih_test.a
         462          0          0          0        772         40   libtfm_app_rot_partition_ipc_client.a
        4364          6         20         28       6729       1312   libtfm_app_rot_partition_ps.a
        """
        line_idx, line_start = 0, 0
        for line in open(file_path, "r"):
            line_idx += 1
            if line.find("Code (inc. data)   RO Data    RW Data    ZI Data      Debug   Library Name") > 0:
                line_start = line_idx + 1
            if line_idx > line_start and line_start > 0:
                content = line.split()
                if len(content) == 7:
                    cur.execute("insert into Library values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
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

def collect_obj():
    cur.execute('''create table Object
                (name               TEXT                NOT NULL,
                 library            TEXT                NOT NULL,
                 flashsize          INT                 NOT NULL,
                 ramsize            INT                 NOT NULL,
                 code               INT                 NOT NULL,
                 rodata             INT                 NOT NULL,
                 rwdata             INT                 NOT NULL,
                 zidata             INT                 NOT NULL,
                 incdata            INT                 NOT_NULL,
                 Debug              INT                 NOT NULL
                );''')
    if gnuarm:
        obj_lib = ""
        obj_detail_list = collect_set(4)
        for s in obj_detail_list:
            for t in gnuarm_info:
                if t[4] == s['name']:
                    obj_lib = t[5]
                    break
            cur.execute("insert into Object values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (s['name'],
                                obj_lib,
                                s['Code']+ s['RO'] + s['RW'],
                                s['RW'] + s['ZI'],
                                s['Code'],
                                s['RO'],
                                s['RW'],
                                s['ZI'],
                                0, 0))
    elif armcc:
        """
        Code (inc. data)   RO Data    RW Data    ZI Data      Debug   Object Name

        0          0         48          0        328          0   load_info_idle_sp.o
        0          0         48          0         72          0   load_info_ns_agent.o
        0          0         83          0         92          0   load_info_tfm_crypto.o

        Code (inc. data)   RO Data    RW Data    ZI Data      Debug   Library Member Name

       90          0          0          0          0          0   __dczerorl2.o
        8          0          0          0          0         68   __main.o
        0          0          0          0          0          0   __rtentry.o
        """
        line_idx, line_start = 0, 0
        for line in open(file_path, "r"):
            line_idx += 1
            if line.find("Code (inc. data)   RO Data    RW Data    ZI Data      Debug   Object Name") > 0:
                line_start = line_idx + 1
            if line_idx > line_start and line_start > 0:
                content = line.split()
                if len(content) == 7:
                    cur.execute("insert into Object values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
        for line in open(file_path, "r"):
            line_idx += 1
            if line.find("Code (inc. data)   RO Data    RW Data    ZI Data      Debug   Library Member Name") > 0:
                line_start = line_idx + 1
            if line_idx > line_start and line_start > 0:
                content = line.split()
                if len(content) == 7:
                    obj_name = content[6]
                    library_file = ""
                    for line in open(file_path, "r"):
                        if line.find(obj_name) > 0:
                            ch_r = line[line.find(obj_name) + len(obj_name)]
                            ch_l = line[line.find(obj_name) - 1]
                            if ch_l == '(' and ch_r == ')':
                                library_file = line.split(
                                )[6][:line.split()[6].find('(')]
                    if len(library_file) == 0:
                        library_file = "no library"
                    cur.execute("insert into Object values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (content[6],
                                library_file,
                                int(content[0]) + int(content[2]) +
                                int(content[3]),
                                int(content[3]) + int(content[4]),
                                content[0],
                                content[2],
                                content[3],
                                content[4],
                                content[1],
                                content[5]))
                else:
                    break

def get_info_from_gnuarm_map():
    """
    Collect information from GNUARM map file.
    """
    text = os.popen('cat ' + file_path).read()
    text = text[text.find('Linker script and memory map\n'):]

    for type in ["text", "data", "bss", "rodata"]:
        values = []
        i = 0
        key_type = '.' + type + '.'
        i_max = text.rfind(key_type) + text[text.rfind(key_type):].find(')') + 2
        while (i < i_max) & (text[i:].find(key_type) != -1):
            temp = ''
            i = len(text[:i]) + text[i:].find(key_type)
            while (text[i-2] != '.' or text[i-1] != 'o' ) or (text[i] != '\n' and text[i] != ')'):
                temp = temp + text[i]
                i += 1
                if(i >= i_max):
                    break
            temp = temp.replace('\n', ' ').replace('\t', ' ')
            if (temp.find('0x') >= 0):
                values.append(temp)
            i += 1

        """
        Get detail data from lines.
        """
        for line in values:
            sym = line[line.find(key_type):line.find("0x")].replace('\n', '').replace('\t', '').replace(' ', '').replace(key_type, '')
            addr = "0x" + line.split()[1][-10:]
            pos = line.find("0x", line.find('0x') + 1)
            if (pos == -1):
                continue
            line = line[pos:]
            size = int(line.split(' ')[0], 16)
            lib = line[line.rfind('/') + 1:line.rfind('.o') + 2]
            obj = lib[lib.find("(") + 1:lib.rfind('.o')]
            if lib.find('(') > 0:
                lib = lib[:lib.find("(")]
            else:
                lib = "no library"
            gnuarm_info.append([sym, size, addr, type, obj + ".o", lib])

    """
    Read some common symbols from GNUARM map file. These symbols are bss data.
    """
    text = os.popen('cat ' + file_path).read()
    text = text[text.find("Allocating common symbols") + len("Allocating common symbols"):text.find("Discarded input sections")]
    common_symbol_list = text.split()[4:]
    for i in range(int(len(common_symbol_list) / 3)):
        common_symbol = common_symbol_list[3 * i]
        for line in open(file_path, "r"):
            if line.find(common_symbol) > 0 and line.find("0x0000") > 0:
                addr = "0x" + line.split()[0][-10:]
        common_symbol_size = int(common_symbol_list[3 * i + 1], 16)
        temp = common_symbol_list[3 * i + 2]
        lib = temp[temp.rfind('/') + 1:temp.rfind('.o') + 2]
        obj = lib[lib.find("(") + 1:lib.rfind('.o')]
        if lib.find('(') > 0:
            lib = lib[:lib.find("(")]
        else:
            lib = "no library"
        gnuarm_info.append([common_symbol, common_symbol_size, addr, "bss", obj + ".o", lib])

def main(args):
    output = ""
    if args.map_file_input:
        if args.gnuarm_compiler and args.armclang_compiler:
            print("Error: Need \'--gnuarm\' or \'--armcc\'")
        if args.gnuarm_compiler or args.armclang_compiler:
            global cur, file_path, gnuarm_info, gnuarm, armcc
            gnuarm = armcc = False
            for infile in glob.glob(os.path.join(os.getcwd(), '*.db')):
                os.remove(infile)
            file_path = args.map_file_input
            con = sqlite3.connect("data.db")
            cur = con.cursor()
            if args.gnuarm_compiler:
                gnuarm_info = []
                gnuarm = True
                get_info_from_gnuarm_map()
            else:
                armcc = True
            collect_summary()
            collect_section()
            collect_library()
            collect_obj()
            con.commit()
            con.close()
        else:
            print("Error: Need \'--gnuarm\' or \'--armcc\'")

    if args.ui_show:
        if os.path.exists('data.db'):
            ui = UI()
            ui.run()
            ui.con.close()
        else:
            print(none_databse)

    if args.all:
        if os.path.exists('data.db'):
            ui = UI()
            ui.draw_summary_page()
            output = ui.items
        else:
            print(none_databse)

    if args.list_function:
        if os.path.exists('data.db'):
            ui = UI()
            ui.draw_function_page("")
            output = ui.items
        else:
            print(none_databse)

    if args.function_name:
        if os.path.exists('data.db'):
            ui = UI()
            ui.draw_function_page(args.function_name)
            output = ui.items
        else:
            print(none_databse)

    if args.dump_function_name:
        if os.path.exists('data.db'):
            ui = UI()
            ui.function_name = args.dump_function_name
            ui.draw_function_detail_page()
            output = ui.items
        else:
            print(none_databse)

    if args.list_data:
        if os.path.exists('data.db'):
            ui = UI()
            ui.draw_data_page("")
            output = ui.items
        else:
            print(none_databse)

    if args.data_name:
        if os.path.exists('data.db'):
            ui = UI()
            ui.draw_data_page(args.data_name)
            output = ui.items
        else:
            print(none_databse)

    if args.dump_data_name:
        if os.path.exists('data.db'):
            ui = UI()
            ui.data_name = args.dump_data_name
            ui.draw_data_detail_page()
            output = ui.items
        else:
            print(none_databse)

    if args.list_obj:
        if os.path.exists('data.db'):
            ui = UI()
            ui.draw_obj_page()
            output = ui.items
        else:
            print(none_databse)

    if args.obj_name:
        if os.path.exists('data.db'):
            ui = UI()
            ui.obj_file = args.obj_name
            ui.draw_obj_detail_page()
            output = ui.items
        else:
            print(none_databse)

    if args.list_library:
        if os.path.exists('data.db'):
            ui = UI()
            ui.draw_library_page()
            output = ui.items
        else:
            print(none_databse)

    if args.library_name:
        if os.path.exists('data.db'):
            ui = UI()
            ui.library_name = args.library_name
            ui.draw_library_detail_page()
            output = ui.items
        else:
            print(none_databse)
    if args.list_section:
        if os.path.exists('data.db'):
            ui = UI()
            ui.draw_section_page()
            output = ui.items
        else:
            print(none_databse)

    if args.section_name:
        if os.path.exists('data.db'):
            ui = UI()
            ui.section_name = args.section_name
            ui.draw_section_lib()
            output = ui.items
        else:
            print(none_databse)

    if output:
        for s in output:
            print(s)

def parse_args():
    """
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

    parser.add_argument('-f', '--list_function',
                        dest='list_function',
                        action='store_true',
                        help='list function')
    parser.add_argument('--search_func',
                        dest='function_name',
                        help='search function')
    parser.add_argument('--dump_function',
                        dest='dump_function_name',
                        help='dump function')

    parser.add_argument('-d', '--list_data',
                        dest='list_data',
                        action='store_true',
                        help='list data')
    parser.add_argument('--search_data',
                        dest='data_name',
                        help='search data')
    parser.add_argument('--dump_data',
                        dest='dump_data_name',
                        help='dump data')

    parser.add_argument('-o', '--list_obj',
                        dest='list_obj',
                        action='store_true',
                        help='list object file')
    parser.add_argument('--dump_obj',
                        dest='obj_name',
                        help='dump object file')

    parser.add_argument('-l', '--list_library',
                        dest='list_library',
                        action='store_true',
                        help='list library')
    parser.add_argument('--dump_library',
                        dest='library_name',
                        help='dump library')

    parser.add_argument('-s', '--list_section',
                        dest='list_section',
                        action='store_true',
                        help='list section')
    parser.add_argument('--dump_section',
                        dest='section_name',
                        help='dump section')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main(parse_args())
    exit(0)
