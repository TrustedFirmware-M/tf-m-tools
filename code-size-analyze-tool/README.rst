######################
Code size analyze tool
######################

.. contents:: Table of Contents

These are scripts to dump ARMCLANG complie map file detail information and get
the change between two different build results. The features are:

* Get a database to implement data tables from ARMCLANG or GNUARM map file.
* Supply an UI for developers to scan sorted information of sections, libraries,
  object files, functions and data. It can help analyze the biggest or smallest
  targets in certain image. It can also help search functions or data to locate
  their address and detail information.
* Diff two databases to see the code size increasement or decreasement.

******************
Install dependency
******************

Linux
=====
Install curse and database.

.. code-block:: bash

    sudo apt-get install python3-dev libmysqlclient-dev libncursesw6 libncurses6
    pip install mysqlclient XlsxWriter

Windows
=======

In power shell, use pip to install packages.

.. code-block:: bash

    pip install mysqlclient XlsxWriter windows-curses

**********************
Code size analyze tool
**********************

The commands of code size analyze tool usage are:

.. code-block:: bash

    python3 code_size_analyze.py [-h] [-i MAP_FILE_INPUT] [-u]
                                 <--gnuarm|--armcc>
                                 [-a] [-s] [-l] [-o] [-f] [-d]
                                 [--dump_section SECTION_NAME]
                                 [--dump_library LIBRARY_NAME]
                                 [--dump_obj OBJ_NAME]
                                 [--dump_function DUMP_FUNCTION_NAME]
                                 [--dump_data DUMP_DATA_NAME]
                                 [--search_func FUNCTION_NAME]
                                 [--search_data DATA_NAME]

    options:
        -h, --help                          show this help message and exit
        -i MAP_FILE_INPUT                   map file path <path>/tfm_s.map
        -u, --ui                            show UI
        --gnuarm                            gnuarm map file input
        --armcc                             armclang map file input
        -a, --all                           show total
        -s, --list_section                  list section
        -l, --list_library                  list library
        -o, --list_obj                      list object file
        -f, --list_function                 list function
        -d, --list_data                     list data
        --dump_section SECTION_NAME         dump section
        --dump_library LIBRARY_NAME         dump library
        --dump_obj OBJ_NAME                 dump object file
        --dump_function DUMP_FUNCTION_NAME  dump function
        --dump_data DUMP_DATA_NAME          dump data
        --search_func FUNCTION_NAME         search function
        --search_data DATA_NAME             search data

Create database
===============

It is required to input map file path for the script before show the UI. One of
the options like ``--gnuarm`` or ``--armcc`` is required. Keep the compiler
option same from the beginning to the end.

.. code-block:: bash

    python3 code_size_analyze.py -i MAP_FILE_INPUT <--gnuarm|--armcc>

Show the UI
===========

The script ui.py supplies a menu to choose what developers may be interested.

.. code-block:: bash

    python3 code_size_analyze.py -u <--gnuarm|--armcc>

There are several keys to use UI.

* UP: Move UP, mouse scrolling up is same.
* DOWN: Move down, mouse scrolling down is same.
* RIGHT: Move right.
* LEFT: Move left.
* Enter: Move to next page if it can be unfolded.
* ``Q`` or ``q``: Escape to previous page or close script if it in top menu.
* ``s`` or ``S``: Enter output file name to save the content of current page.
* ``:`` : Start search and enter the function or data name.

Dump detail information
=======================

You can get the list of all sections, libraries, object files, functions or
data. You can also dump the specific symbol with the name.

.. code-block:: bash

    python3 code_size_analyze.py <--gnuarm|--armcc> -s
    python3 code_size_analyze.py <--gnuarm|--armcc> --dump_section SECTION_NAME


Search specific function or data
================================

You can search the target with keyword in command line. For example:

.. code-block:: bash

    python3 code_size_analyze.py <--gnuarm|--armcc> --search_func FUNCTION_NAME
    python3 code_size_analyze.py <--gnuarm|--armcc> --search_data DATA_NAME

*******************
Code size diff tool
*******************

Use ``code_size_diff.py`` to diff two diffrent build results with same compiler.
Firstly, use ``code_size_analyze.py`` to prepare two different databases. For
example:

.. code-block:: bash

    usage: code_size_diff.py [-h] -i [input_dbs [input_dbs ...]]
                             [-a] [-f] [-d] [-o] [-l]

    optional arguments:
    -h, --help            show this help message and exit
    -i [input_dbs [input_dbs ...]], --input [input_dbs [input_dbs ...]]
                          Input two different data base files
    -a, --diff_all        diff summary
    -f, --diff_function   diff function
    -d, --diff_data       diff data
    -o, --diff_obj        diff object file
    -l, --diff_lib        diff library

Then compare two database with the diff tool, the branch1 is base.

.. code-block:: bash

    python3 code_size_diff.py -i output/branch1.db output/branch2.db -a
    Code size:  +++         48928   B               47.78   KB
    RO data:    +++         29440   B               28.75   KB
    RW data:    ---         64      B               0.06    KB
    ZI data:    ---         500     B               0.49    KB
    Flash size: +++         78304   B               76.47   KB
    RAM size:   ---         564     B               0.55    KB

The summary information change will be printed. Enter ``-h`` to get more usages
of diff tool.

--------------

*Copyright (c) 2021-2022, Arm Limited. All rights reserved.*
