# ------------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# ------------------------------------------------------------------------------

import sqlite3
import curses
import curses.textpad

class UI(object):
    """
    Class UI is used to show the data in the terminal with library curses. It
    contains two main diffrent functions, one is to control the UI and show the
    message in the terminal, the other is to search the information and then
    transform it into a string varible called items[]. This can be showed or
    exported as a plaintext. These functions to fill items[] are PUBLIC.

    - Methods:
      - UI().run()              - Run the UI in terminal.
      - UI.draw_<symbol>_page() - Get the information of specific symbol
      - UI.open_db()            - Open database.

    - Variables:
      - UI().items              - The result searched from database.
      - UI().armcc              - ARMCLANG option.
      - UI().gnuarm             - GNUARM option.
      - UI().con                - Database handler.
      - UI().function_name      - Specific function name.
      - UI().data_name          - Specific data name.
      - UI().section_name       - Specific section name.
      - UI().library_name       - Specific library name.
      - UI().obj_file           - Specific object file name.
      - UI().db_file            - Database file.
      - UI().sort               - Database list order: size, name and so on.
      - UI().order              - Database sort order: DESC and ASC.
    """

    def __init__(self):
        """
        Initialize variables.
        """
        self.function_name = ""
        self.data_name = ""
        self.section_name = ""
        self.library_name = ""
        self.obj_file = ""
        self.gnuarm = False
        self.armcc = False
        self.items = []
        self.db_file = ""
        self.sort = "size"
        self.order = "DESC"

        self.__window = None
        self.__width = 0
        self.__height = 0
        self.__menu_depth = 0
        self.__detail = 0
        self.__section_detail = 0
        self.__UP = -1
        self.__DOWN = 1
        self.__line1 = "─" * 128
        self.__line2 = "-" * 128
        self.__cmd_file="Enter the file name:"
        self.__cmd_func="Enter the function name:"
        self.__cmd_data="Enter the data name:"

    def open_db(self):
        self.con = sqlite3.connect(self.db_file)
        self.__cur = self.con.cursor()
        cursor = self.__cur.execute("select * from Compiler")
        for row in cursor:
            compiler = row[1]
            if compiler == 1:
                self.gnuarm = True
            elif compiler == 0:
                self.armcc = True

    def __init_curses(self):
        """
        Setup the curses
        """
        self.__window = curses.initscr()
        self.__window.keypad(True)

        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.__current = curses.color_pair(2)
        self.__height, self.__width = self.__window.getmaxyx()

        self.__max_lines = curses.LINES - 1
        self.__top = 0

        self.__bottom = len(self.items)
        self.__current = 0
        self.__current_x = 0

    def __input_stream(self):
        """
        Waiting an input and run a proper method according to type of input
        """
        while True:
            self.__display()

            ch = self.__window.getch()
            if ch == curses.KEY_UP:
                self.__scroll(self.__UP)
            elif ch == curses.KEY_DOWN:
                self.__scroll(self.__DOWN)
            elif ch == curses.KEY_LEFT:
                self.__current_x = max(self.__current_x - 1, 0)
            elif ch == curses.KEY_RIGHT:
                self.__current_x = self.__current_x + 1
            elif ch ==  ord('q') or ch == ord('Q'):
                """
                If press 'q' or 'Q', escape this page
                """
                if self.__menu_depth == 0:
                    break
                self.__menu_depth = max(self.__menu_depth - 1, 0)
                self.__draw_page()
            elif ch == 10:
                """
                If press ENTER, get into next page if it exists
                """
                self.__get_menu_choose()
                self.__menu_depth = self.__menu_depth + 1
                self.__draw_page()
            elif ch == 58:
                """
                If press ':', get target name form input line to search
                functions or data
                """
                if self.__menu_depth == 1:
                    if self.__detail == 3:
                        self.draw_function_page(self.__get_input_line_msg(self.__cmd_func))
                    if self.__detail == 4:
                        self.draw_data_page(self.__get_input_line_msg(self.__cmd_data))
            elif ch == ord('s') or ch == ord('S'):
                """
                If press 's' or 'S', save to file
                """
                self.__save_file(self.__get_input_line_msg(self.__cmd_file))

    def __get_input_line_msg(self, cmd):
        """
        Get message from input line.
        """
        self.__window.addstr(self.__height - 1, 0, cmd, curses.color_pair(2))
        self.input_line = curses.newwin(1, curses.COLS - 2 - len(cmd), curses.LINES-1, len(cmd) + 1)
        self.input_box = curses.textpad.Textbox(self.input_line)
        self.__window.refresh()
        self.input_box.edit()
        ret = self.input_box.gather()[:len(self.input_box.gather())-1]
        self.__display()
        self.input_line.clear()
        return ret

    def __save_file(self, output_file_name):
        """
        Save to files
        """
        fo = open(output_file_name + '.txt', "w")
        for s in self.items:
            fo.write(s + '\n')
        fo.close()

    def __scroll(self, direction):
        """
        Scrolling the window when pressing up/down arrow keys
        """
        next_line = self.__current + direction
        if (direction == self.__UP) and (self.__top > 0 and self.__current == 0):
            self.__top += direction
            return
        if (direction == self.__DOWN) and (next_line == self.__max_lines) and \
                (self.__top + self.__max_lines < self.__bottom):
            self.__top += direction
            return
        if (direction == self.__UP) and (self.__top > 0 or self.__current > 0):
            self.__current = next_line
            return
        if (direction == self.__DOWN) and (next_line < self.__max_lines) and \
                (self.__top + next_line < self.__bottom):
            self.__current = next_line
            return

    def __display(self):
        """
        Display the items on window
        """
        self.__window.erase()
        for idx, item in enumerate(self.items[self.__top:self.__top + self.__max_lines]):
            if idx == self.__current:
                self.__window.addstr(idx, 0, item[self.__current_x:self.__current_x + self.__width], curses.color_pair(2))
            else:
                self.__window.addstr(idx, 0, item[self.__current_x:self.__current_x + self.__width], curses.color_pair(1))
        self.__window.refresh()

    def __draw_page(self):
        """
        Draw different page with menu_depth, detail and section_detail.
        """
        if self.__menu_depth == 0:
            self.__draw_welcome_page()
        elif self.__menu_depth == 1:
            if self.__detail == 1:
                self.draw_summary_page()
            if self.__detail == 2:
                self.draw_section_page()
            if self.__detail == 3:
                self.draw_function_page("")
            if self.__detail == 4:
                self.draw_data_page("")
            if self.__detail == 5:
                self.draw_library_page()
            if self.__detail == 6:
                self.draw_obj_page()
        elif self.__menu_depth == 2:
            if self.__detail == 2:
                self.draw_section_detail_page()
            if self.__detail == 3:
                self.draw_function_detail_page()
            if self.__detail == 4:
                self.draw_data_detail_page()
            if self.__detail == 5:
                self.draw_library_detail_page()
            if self.__detail == 6:
                self.draw_obj_detail_page()
        elif self.__menu_depth == 3 and self.__detail == 2:
            """
            Draw section detail menu, here self.__detail is 2
            """
            if self.__section_detail == 1:
                self.draw_section_lib()
            if self.__section_detail == 2:
                self.draw_section_func()
            if self.__section_detail == 3:
                self.draw_section_data()
        elif self.__menu_depth == 4:
            """
            Only section detail menu can move to menu depth 5, here function
            detail and data detail are also supported.
            """
            if self.__section_detail == 2:
                self.draw_function_detail_page()
            if self.__section_detail == 3:
                self.draw_data_detail_page()

        self.__bottom = len(self.items)
        self.__current = 0
        self.__current_x = 0
        self.__top = 0

    def __get_menu_choose(self):
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
        It will change the self.__detail's value in range 1 - 6
        """
        if self.__menu_depth == 0:
            if self.__current + self.__top > 0:
                self.__detail = self.__current
            else:
                """
                Except first line
                """
                self.__menu_depth = self.__menu_depth - 1
        if self.__menu_depth == 1:
            if self.__current + self.__top > 0:
                if self.__detail == 2:
                    """
                    Get section name which will be used to draw its detail page
                    in __draw_page() function.
                    """
                    self.section_name = self.items[self.__top + self.__current].split()[0]
                elif self.__detail == 3:
                    """
                    Get function name and its object file to avoid same name
                    situation. Function name will be used to draw its detail
                    page in __draw_page() function.
                    """
                    self.function_name = self.items[self.__top + self.__current].split()[0]
                    self.obj_file = self.items[self.__top + self.__current].split()[4]
                elif self.__detail == 4:
                    """
                    Get data name and its object file name to avoid same name
                    situation. Data name will be used to draw its detail page in
                    __draw_page() function.
                    """
                    self.data_name = self.items[self.__top + self.__current].split()[0]
                    self.obj_file = self.items[self.__top + self.__current].split()[5]
                elif self.__detail == 5:
                    """
                    Get library name which will be used to draw its detail page
                    in __draw_page() function.
                    """
                    self.library_name = self.items[self.__top + self.__current].split()[0]
                elif self.__detail == 6:
                    """
                    Get object file name which will be used to draw its detail
                    page in __draw_page() function.
                    """
                    self.obj_file = self.items[self.__top + self.__current].split()[0]
                else:
                    """
                    Other invalid choose will not change menu depth.
                    """
                    self.__menu_depth = self.__menu_depth - 1
            else:
                """
                Except first line
                """
                self.__menu_depth = self.__menu_depth - 1
        """
        Section detail page, menu_depth = 1
            =============================
            Name :TFM_UNPRIV_CODE           Size :155544
            1. Summary           -->
            2. Function          -->
            3. Data              -->
            =============================
        It will change the self.__section_detail's value in range 1 - 3
        """
        if self.__menu_depth == 2:
            if self.__current + self.__top > 0:
                if self.__detail == 2:
                    self.__section_detail = self.__current
                else:
                    self.__menu_depth = self.__menu_depth - 1
            else:
                self.__menu_depth = self.__menu_depth - 1
        if self.__menu_depth == 3:
            if self.__current + self.__top > 0:
                if self.__section_detail == 2:
                    self.function_name = self.items[self.__top + self.__current].split()[0]
                    self.obj_file = self.items[self.__top + self.__current].split()[4]
                elif self.__section_detail == 3:
                    self.data_name = self.items[self.__top + self.__current].split()[0]
                    self.obj_file = self.items[self.__top + self.__current].split()[5]
                else:
                    self.__menu_depth = self.__menu_depth - 1
            else:
                self.__menu_depth = self.__menu_depth - 1
        if self.__menu_depth == 4:
            self.__menu_depth = self.__menu_depth - 1

    def __draw_welcome_page(self):
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
        cursor = self.__cur.execute("select * from Summary")
        if self.gnuarm:
            for row in cursor:
                self.items = [self.__line1,
                              "Total usage(include all symbols and \"fill or pad\"):",
                              "Flash size\t: {:<8}\t{:<4.2f}\tKB".
                              format(row[6], row[6]/1024),
                              "RAM size\t: {:<8}\t{:<4.2f}\tKB".
                              format(row[7], row[7]/1024),
                              self.__line2,
                              "These data are collected from functions, stacks or arrays sizes without \"fill or pad\" part!",
                              "Text size\t: {:<8}\t{:<4.2f}\tKB".
                              format(row[0], row[0]/1024),
                              "Read-only data\t: {:<8}\t{:<4.2f}\tKB".
                              format(row[1], row[1]/1024),
                              "Read-write data\t: {:<8}\t{:<4.2f}\tKB".
                              format(row[2], row[2]/1024),
                              "BSS data\t: {:<8}\t{:<4.2f}\tKB".
                              format(row[3], row[3]/1024),
                              self.__line2,
                              "Some other unknown type symbols locate in flash or ram:",
                              "Total unknown type symbols in flash: {:<8}\t{:<4.2f}\tKB".
                              format(row[4], row[4]/1024),
                              "Total unknown type symbols in RAM  : {:<8}\t{:<4.2f}\tKB".
                              format(row[5], row[5]/1024),
                              self.__line1]
                break
        if self.armcc:
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
                              format(row[6], row[6]/1024),
                              "RAM size\t: {:<8}\t{:<4.2f}\tKB = RW + ZI".
                              format(row[7], row[7]/1024)]
                break

    def draw_section_page(self):
        """
        Get section info from database and save into self.items.
        """
        self.items = ["{:<50}{:<16}{:<16}{:<16}".
                      format("Name", "Size", "Address", "PAD size")]

        cursor = self.__cur.execute("select * from Section ORDER BY {} {}".format(self.sort, self.order))
        for row in cursor:
            self.items.append("{:<50}{:<16}{:<16}{:<16}".
                              format(row[0], row[1], row[2], row[3]))

    def draw_section_detail_page(self):
        """
        Section detail page with a menu.
        """
        cursor = self.__cur.execute("select * from Section WHERE name = '{}'".
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
        cursor = self.__cur.execute("select * from Function WHERE section = '{}' ORDER BY lib_file DESC".
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

        cursor = self.__cur.execute("select * from Data WHERE section = '{}' ORDER BY lib_file DESC".
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
                          key=lambda i: i['RO'] + i['Code'] + i['RW'] + i['ZI'],
                          reverse=True)
        for s in obj_dict.keys():
            obj_list.append({'Name': s,
                             'RO': obj_dict[s]['RO'],
                             'RW': obj_dict[s]['RW'],
                             'Code': obj_dict[s]['Code'],
                             'Lib': obj_dict[s]['Lib'],
                             'ZI': obj_dict[s]['ZI']})
        obj_list = sorted(obj_list,
                          key=lambda i: i['RO'] + i['Code'] + i['RW'] + i['ZI'],
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
            self.items.append(self.__line2)
            self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format("Summary",
                                     ret['Flash'],
                                     ret['Ram'],
                                     ret['Code'],
                                     ret['RO'],
                                     ret['RW'],
                                     ret['ZI'],
                                     ret['Total']))
            self.items.append(self.__line1)
            return ret

        def insert_column_line(title):
            """
            Quickly insert column line.
            """
            self.items.append(title)
            self.items.append(self.__line2)
            self.items.append(colums_name)
            self.items.append(self.__line2)

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
        self.items = [self.__line1]
        insert_column_line(" " * ((128 - len("Section libraries"))//2) + "Section libraries")
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
        insert_column_line(" " * ((128 - len("Section object files"))//2) + "Section object files")
        for s in obj_list:
            quick_insert_data_line(s)
        ret = sum_data(obj_list)
        total_flash_size, total_ram_size = ret['Flash'], ret['Ram']

        """
        Dump NOT-IN-LIBRARY object file information.
        """
        if exsit_no_lib_obj:
            insert_column_line(" " * ((128 - len("Section NOT-IN-LIBRARY object files"))//2) +
                "Section NOT-IN-LIBRARY object files")
            tmp_list = []
            for s in lib_list:
                if s['Name'].find(".o") > 0:
                    tmp_list.append(s)
                    quick_insert_data_line(s)
            sum_data(tmp_list)

        """
        Insert the summary information at the top of this page.
        """
        cursor = self.__cur.execute(
            "select * from Section WHERE name = '{}'".format(self.section_name))
        for row in cursor:
            self.items.insert(0, "Section Name :{}\tTotal Size :{}\tFlash : {}\tRAM : {:<6}\tPad size = {}".
                              format(self.section_name, row[1], total_flash_size, total_ram_size, row[3]))
            break
        self.items.insert(0, self.__line2)
        self.items.insert(0, " " * ((128 - len("Section information"))//2) + "Section information")
        self.items.insert(0, self.__line1)

        """
        Dump detail information of the section.
        """
        index = 4 * ' '
        self.items.append(" " * ((128 - len("Detail information"))//2) + "Detail information")
        self.items.append(self.__line2)
        for s in lib_list:
            self.items.append("{} Code Size = {} RO Data = {} RW Data = {} ZI Data = {}".
                              format(s['Name'], s['Code'], s['RO'], s['RW'], s['ZI']))
            for t in obj_list:
                if t['Lib'] == s['Name']:
                    self.items.append(index + "{} Code Size = {} RO Data = {} RW Data = {} ZI Data = {}".format(
                        t['Name'], t['Code'], t['RO'], t['RW'], t['ZI']))
                    count = 0
                    cursor = self.__cur.execute("select * from Function WHERE section = '{}' and lib_file = '{}' and obj_file = '{}' ORDER BY {} {}".
                                                format(self.section_name,
                                                       s['Name'],
                                                       t['Name'],
                                                       self.sort,
                                                       self.order))
                    for row in cursor:
                        if row and count == 0:
                            self.items.append(index * 2 + "Code size = {}".
                                              format(t['Code']))
                            count = count + 1
                        self.items.append(index * 3 + "{:<6} {} ".
                                          format(row[2], row[0]))

                    def get_certain_data(type_name, s, t):
                        count = 0
                        cursor = self.__cur.execute("select * from Data WHERE section = '{}' and lib_file = '{}' and obj_file = '{}'  and type = '{}' ORDER BY {} {}".
                                                    format(self.section_name,
                                                           s['Name'],
                                                           t['Name'],
                                                           type_name,
                                                           self.sort,
                                                           self.order))
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
            self.items.append(self.__line2)
        self.items[-1] = self.__line1

    def draw_section_func(self):
        self.items = ["{:<50}{:<32}{:<10}{:<16}{:<40}{:<40}".
                      format("Name",
                             "Section",
                             "Size",
                             "Address",
                             "Object File",
                             "Library")]
        cursor = self.__cur.execute("select * from Function WHERE section = '{}' ORDER BY {} {}".
                                  format(self.section_name, self.sort, self.order))
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

        cursor = self.__cur.execute("select * from Data WHERE section = '{}' ORDER BY {} {}".
                                  format(self.section_name, self.sort, self.order))
        for row in cursor:
            data_name = row[0]
            if len(data_name) >= 50:
                data_name = data_name[:40] + "-->"
            self.items.append("{:<50}{:<32}{:<10}{:<16}{:<16}{:<40}{:<40}".
                              format(data_name, row[1], row[2], row[3], row[4], row[5], row[6]))

    def __quick_append(self):
        self.items.append(self.__line1)

        self.items.append("{:<50}{:<32}{:<10}{:<16}{:<40}".
                          format("Name",
                                 "Section",
                                 "Size",
                                 "Type",
                                 "Object File"))
        self.items.append(self.__line2)

    def __quick_append_data(self, cursor):
        flag = False
        for row in cursor:
            if not flag:
                self.__quick_append()
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

        cursor = self.__cur.execute(
            "select * from Library ORDER BY {} {}".format(self.sort, self.order))
        for row in cursor:
            self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    def draw_library_detail_page(self):
        flag = False
        """
        Draw title.
        """
        self.items = [self.__line1, "{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                      format("Name",
                             "Flash size",
                             "RAM size",
                             "Code",
                             "RO data",
                             "RW data",
                             "ZI data",
                             "Inc. data"),
                      self.__line2]

        cursor = self.__cur.execute("select * from Library WHERE name = '{}'".
                                  format(self.library_name))
        for row in cursor:
            self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            break

        """
        Draw object files.
        """
        self.items.append(self.__line1)
        self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                          format("Name",
                                 "Flash size",
                                 "RAM size",
                                 "Code",
                                 "RO data",
                                 "RW data",
                                 "ZI data",
                                 "Inc. data"))
        self.items.append(self.__line2)

        cursor = self.__cur.execute("select * from Object WHERE lib_file = '{}' ORDER BY {} {}".
                                  format(self.library_name, self.sort, self.order))
        for row in cursor:
            self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

        """
        Draw functions.
        """
        cursor = self.__cur.execute("select * from Function WHERE lib_file = '{}' ORDER BY {} {}".
                                  format(self.library_name, self.sort, self.order))
        for row in cursor:
            if not flag:
                self.__quick_append()
            self.items.append("{:<50}{:<32}{:<10}{:<16}{:<40}".
                              format(row[0], row[1], row[2], "Code", row[4]))
            flag = True

        """
        Draw RO data.
        """
        cursor = self.__cur.execute("select * from Data WHERE type = 'RO' and lib_file = '{}' ORDER BY {} {}".
                                  format(self.library_name, self.sort, self.order))
        self.__quick_append_data(cursor)

        """
        Draw RW data.
        """
        cursor = self.__cur.execute("select * from Data WHERE type = 'RW' and lib_file = '{}' ORDER BY {} {}".
                                  format(self.library_name, self.sort, self.order))
        self.__quick_append_data(cursor)

        """
        Draw ZI data.
        """
        cursor = self.__cur.execute("select * from Data WHERE type = 'ZI' and lib_file = '{}' ORDER BY {} {}".
                                  format(self.library_name, self.sort, self.order))
        self.__quick_append_data(cursor)
        self.items.append(self.__line1)

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
        cursor = self.__cur.execute("select * from Object WHERE lib_file = 'no library' ORDER BY {} {}".format(self.sort, self.order))
        for row in cursor:
            self.items.append("{:<50}{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
        cursor = self.__cur.execute(
            "select * from Object WHERE lib_file != 'no library' ORDER BY {} {}".format(self.sort, self.order))
        for row in cursor:
            self.items.append("{:<50}{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

    def draw_obj_detail_page(self):
        flag = False
        self.items = [self.__line1,
                      "{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                      format("Name",
                             "Flash size",
                             "RAM size",
                             "Code",
                             "RO data",
                             "RW data",
                             "ZI data",
                             "Inc. data"),
                      self.__line2]

        cursor = self.__cur.execute("select * from Object WHERE name = '{}'".
                                  format(self.obj_file))
        for row in cursor:
            self.items.append("{:<50}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}{:<12}".
                              format(row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
            break

        cursor = self.__cur.execute("select * from Function WHERE obj_file = '{}' ORDER BY {} {}".
                                  format(self.obj_file, self.sort, self.order))
        for row in cursor:
            if not flag:
                self.__quick_append()
            self.items.append("{:<50}{:<32}{:<10}{:<16}{:<40}".
                              format(row[0], row[1], row[2], "Code", row[4]))
            flag = True

        cursor = self.__cur.execute("select * from Data WHERE type = 'RO' and obj_file = '{}' ORDER BY {} {}".
                                  format(self.obj_file, self.sort, self.order))
        self.__quick_append_data(cursor)

        cursor = self.__cur.execute("select * from Data WHERE type = 'RW' and obj_file = '{}' ORDER BY {} {}".
                                  format(self.obj_file, self.sort, self.order))
        self.__quick_append_data(cursor)

        cursor = self.__cur.execute("select * from Data WHERE type = 'ZI' and obj_file = '{}' ORDER BY {} {}".
                                  format(self.obj_file, self.sort, self.order))
        self.__quick_append_data(cursor)
        self.items.append(self.__line1)

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
            cursor = self.__cur.execute("select * from Function WHERE name LIKE '%{}%'".
                                      format(search_func))
        else:
            cursor = self.__cur.execute("select * from Function ORDER BY {} {}".format(self.sort, self.order))
        for row in cursor:
            self.items.append("{:<50}{:<50}{:<10}{:<16}{:<40}{:<40}".
                              format(row[0], row[1], row[2], row[3], row[4], row[5]))

    def draw_function_detail_page(self):
        if self.obj_file:
            cursor = self.__cur.execute("select * from Function WHERE name = '{}' and obj_file = '{}'".
                                    format(self.function_name, self.obj_file))
        else:
            cursor = self.__cur.execute("select * from Function WHERE name = '{}'".
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
            cursor = self.__cur.execute("select * from Data WHERE name LIKE '%{}%'".
                                      format(search_data))
        else:
            cursor = self.__cur.execute("select * from Data ORDER BY {} {}".format(self.sort, self.order))
        for row in cursor:
            data_name = row[0]
            if len(data_name) >= 50:
                data_name = data_name[:40] + "-->"
            self.items.append("{:<50}{:<50}{:<10}{:<16}{:<16}{:<40}{:<40}".
                              format(data_name, row[1], row[2], row[3], row[4], row[5], row[6]))

    def draw_data_detail_page(self):
        if self.obj_file:
            cursor = self.__cur.execute("select * from Data WHERE name = '{}' and obj_file = '{}'".
                                  format(self.data_name, self.obj_file))
        else:
            cursor = self.__cur.execute("select * from Data WHERE name = '{}'".
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

    def run(self):
        """
        Continue running the TUI until get interrupted
        """
        self.open_db()
        self.__init_curses()
        try:
            self.__draw_page()
            self.__input_stream()
        except KeyboardInterrupt:
            pass
        finally:
            self.con.close()
            curses.endwin()
