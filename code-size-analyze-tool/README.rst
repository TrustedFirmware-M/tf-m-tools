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

***************
Install sqlite3
***************

Linux
=====
Install sqlite3 for python.

.. code-block:: bash

    sudo apt-get install python3-dev libmysqlclient-dev
    pip install mysqlclient


*****
Usage
*****

The command is:

.. code-block:: bash

    python3 code_size_analyze.py -i <map file path> --gnuarm
    python3 code_size_analyze.py -i <map file path> --armcc
    python3 code_size_analyze.py --ui

It is required to input map file path for the script before show the UI. While
input the map file, compiler information such as ``--gnuarm`` or ``--armcc``
is required.

keys
====

The script ui.py supplies a menu to choose what developers may be interested.
There are several keys to move cursor.

* UP: Move UP, mouse scrolling up is same.
* DOWN: Move down, mouse scrolling down is same.
* RIGHT: Move right.
* LEFT: Move left.
* Enter: Move to next page if it can be unfolded.
* ``Q`` or ``q``: Escape to previous page or close script if it in top menu.

Search
======

In ``Function detail`` and ``library detail`` pages, developers can search for
specific target with key word of target name. Press ``:`` to start search and
enter the name in the last line of window. All the targets with key word will
be given.

You can also search or dump the target in command line without Ui, for example:
.. code-block:: bash

    python3 code_size_analyze.py --search_func <func_name>

All the features provided by UI can be used in command line too. Enter ``-h`` to
get the help information and choose the option to use.

Save
====

In any page, press ``s`` or ``S`` to start enter output file name to save the
content of this page.

Diff
====

Use ``code_size_diff.py`` to diff two diffrent build results with same compiler.
Firstly, use ``code_size_analyze.py`` to prepare two different databases. For
example:

.. code-block:: bash

    cd <TF-M workspace>
    git checkout branch1
    # Build with ARMCLANG
    python3 code_size_analyze.py -i <map file 1> --armcc
    mv data.db output/branch1.db

    # Do the same steps to create branch2.db

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

*Copyright (c) 2021, Arm Limited. All rights reserved.*
