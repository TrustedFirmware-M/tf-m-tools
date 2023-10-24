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

    sudo apt-get install python3-dev libmysqlclient-dev libncursesw6 libncurses6 libsqlite3-dev
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

    usage: code_size_analyze.py [-h] [--gnuarm | --armcc] [--db-name <data.db>]
                                [-u | -S | -s | -l | -o | -f | -d |
                                 --dump-sec <sec> | --dump-lib <lib> |
                                 --dump-obj <obj> | --dump-func <func> |
                                 --dump-data <data> | --search-func <func> |
                                 --search-data <data>]
                                [--sort-by-size | --sort-by-name |
                                 --sort-by-obj | --sort-by-lib |
                                 --sort-by-sec] [--desc | --asc]
                                 file_input

    positional arguments:
        file_input            map or database file

    optional arguments:
        -h, --help            show this help message and exit
        --gnuarm              GNUARM model
        --armcc               ARMCLANG model
        --db-name <data.db>   database name to save
        -u, --ui              start UI to analyze
        -S, --Summary         show summary message
        -s, --list-section    list section
        -l, --list-library    list library
        -o, --list-obj        list object file
        -f, --list-function   list function
        -d, --list-data       list data
        --dump-sec <sec>      dump section
        --dump-lib <lib>      dump library
        --dump-obj <obj>      dump object file
        --dump-func <func>    dump function
        --dump-data <data>    dump data
        --search-func <func>  search function
        --search-data <data>  search data
        --sort-by-size        list by size order
        --sort-by-name        list by name order
        --sort-by-obj         list by object file name order
        --sort-by-lib         list by library file name order
        --sort-by-sec         list by section name order
        --desc                sort with desc order
        --asc                 sort with asc order

Create database
===============

It is required to input map file path for the script before show the UI. One of
the options like ``--gnuarm`` or ``--armcc`` is required.

The default database name created is ``data.db``. Use ``--db-name`` to name the
output file if necessary. For example, saving two different databases to compare
later.

.. code-block:: bash

    $: python code_size_analyze.py tfm_s.map <--gnuarm|--armcc> --db-name tfm_s.db

UI mode
=======

The script ui.py supplies a menu to choose what developers may be interested.
You can enter UI mode by analyzing map file directly or by importing database
file path. The latter way is suggested as it runs more quickly.

.. code-block:: bash

    $: python code_size_analyze.py tfm_s.map <--gnuarm|--armcc> -u
    $: python code_size_analyze.py tfm_s.db -u

There are several keys to use UI.

* UP: Move UP, mouse scrolling up is same.
* DOWN: Move down, mouse scrolling down is same.
* RIGHT: Move right.
* LEFT: Move left.
* Enter: Move to next page if it can be unfolded.
* ``Q`` or ``q``: Escape to previous page or close script if it in top menu.
* ``s`` or ``S``: Enter output file name to save the content of current page.
* ``:`` : Start search and enter the function or data name.

Terminal mode
=============

In terminal mode, it is better to analyze database file rather than map file.

Dump detail information
-----------------------

You can get the list of all sections, libraries, object files, functions or
data. You can also dump the specific symbol with the name.

.. code-block:: bash

    $: python code_size_analyze.py tfm_s.map --armcc --db-name test.db -S
    ───────────────────────────────────────────────
    Code size       : 56676         55.35   KB
    -----------------------------------------------
    RO data         : 3732          3.64    KB
    RW data         : 204           0.20    KB
    ZI data         : 24588         24.01   KB
    Flash size      : 60612         59.19   KB = Code + RO + RW
    RAM size        : 24792         24.21   KB = RW + ZI
    ───────────────────────────────────────────────

    $: python code_size_analyze.py tfm_s.db -s
    $: python code_size_analyze.py tfm_s.db --dump-sec <sec>

Search specific function or data
--------------------------------

You can search the target with keyword in command line. For example:

.. code-block:: bash

    $: python code_size_analyze.py tfm_s.db --search-func <func>
    $: python code_size_analyze.py tfm_s.db --search-data <data>

Sort Table
----------

You can sort the messages in terminal mode. The script supplies five options and
two orders. For example:

.. code-block:: bash

    $: python code_size_analyze.py tfm_s.db -l --sort-by-size --asc
    ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    Name                                              Flash size  RAM size    Code        RO data     RW data     ZI data     Inc. data   Debug
    --------------------------------------------------------------------------------------------------------------------------------------------------
    libtfm_qcbor_s.a                                  758         0           758         0           0           0           4           17046
    libtfm_sprt.a                                     1016        0           1016        0           0           0           0           41004
    c_w.l                                             1248        96          1248        0           0           96          86          1892
    libtfm_psa_rot_partition_attestation.a            2497        557         2492        5           0           557         68          51865
    libtfm_spm.a                                      4112        657         3932        136         44          613         168         52958
    libtfm_psa_rot_partition_its.a                    5090        116         5030        32          28          88          28          49804
    libtfm_psa_rot_partition_crypto.a                 6062        3232        6062        0           0           3232        36          92472
    libplatform_s.a                                   6486        316         5582        780         124         192         404         94887
    libmbedcrypto.a                                   28408       2292        26138       2262        8           2284        1066        226489
    ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Not all symbols support to be sorted by the whole five options, refer to the
table to get more information.

+----------------+---------+---------+--------------+----------+------+
| Options        | Section | Library | Object files | Function | Data |
+================+=========+=========+==============+==========+======+
| --sort-by-size |    √    |    √    |       √      |    √     |   √  |
+----------------+---------+---------+--------------+----------+------+
| --sort-by-name |    √    |    √    |       √      |    √     |   √  |
+----------------+---------+---------+--------------+----------+------+
| --sort-by-sec  |    √    |         |              |    √     |   √  |
+----------------+---------+---------+--------------+----------+------+
| --sort-by-lib  |         |    √    |       √      |    √     |   √  |
+----------------+---------+---------+--------------+----------+------+
| --sort-by-obj  |         |         |       √      |    √     |   √  |
+----------------+---------+---------+--------------+----------+------+

*******************
Code size diff tool
*******************

Use ``code_size_diff.py`` to diff two diffrent build results with same compiler.

.. code-block:: bash

    usage: code_size_diff.py [-h] (-S | -f | -d | -o | -l) based_db compared_db

    positional arguments:
        based_db             based databse
        compared_db          compared databse

    optional arguments:
        -h, --help            show this help message and exit
        -S, --diff-Summary    diff summary
        -f, --diff-function   diff function
        -d, --diff-data       diff data
        -o, --diff-obj        diff object file
        -l, --diff-lib        diff library

Firstly, use ``code_size_analyze.py`` to prepare two different databases. Then
compare two database with the diff tool, the branch1 is base.

.. code-block:: bash

    $: python code_size_diff.py output/branch1.db output/branch2.db -S
    Code size:  +++         48928   B               47.78   KB
    RO data:    +++         29440   B               28.75   KB
    RW data:    ---         64      B               0.06    KB
    ZI data:    ---         500     B               0.49    KB
    Flash size: +++         78304   B               76.47   KB
    RAM size:   ---         564     B               0.55    KB

--------------

*Copyright (c) 2021-2022, Arm Limited. All rights reserved.*
