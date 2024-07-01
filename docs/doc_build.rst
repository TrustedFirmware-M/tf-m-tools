##########################
Building the documentation
##########################

******************************
Tools and building environment
******************************

These tools are used to generate TF-M Tools documentation:

    - Graphviz dot v2.38.0 or later
    - PlantUML v1.2018.11 or later
    - Java runtime environment v1.8 or later (for running PlantUML)
    - Sphinx and other python modules, listed in ``docs/requirements.txt``


To prepare your building environment execute the following steps:

.. tabs::

    .. group-tab:: Linux

        Install the required tools:

        .. code-block:: bash

            sudo apt-get install -y graphviz default-jre
            mkdir ~/plantuml
            curl -L http://sourceforge.net/projects/plantuml/files/plantuml.jar/download --output ~/plantuml/plantuml.jar

            # Install the required Python modules
            pip3 install --upgrade pip
            cd <tf-m-tools base folder>
            pip3 install -r docs/requirements.txt

        Set the environment variables:

        .. code-block:: bash

            export PLANTUML_JAR_PATH=~/plantuml/plantuml.jar

    .. group-tab:: Windows

        Download and install the following tools:

            - `Graphviz 2.38 <https://graphviz.gitlab.io/_pages/Download/windows/graphviz-2.38.msi>`__
            - The Java runtime is part of the Arm DS installation or can be downloaded from `here <https://www.java.com/en/download/>`__
            - `PlantUML <http://sourceforge.net/projects/plantuml/files/plantuml.jar/download>`__

        Set the environment variables, assuming that:

            - dot binaries are available on the PATH.
            - Java JVM is used from Arm DS installation.

        .. code-block:: bash

            set PLANTUML_JAR_PATH=<plantuml_Path>\plantuml.jar
            set PATH=$PATH;<ARM_DS_PATH>\sw\java\bin

            # Install the required Python modules
            pip3 install --upgrade pip
            cd <tf-m-tools base folder>
            pip3 install -r docs\requirements.txt


*********************
Build TF-M Tools Docs
*********************

From the root directory of this repository, run:

.. code-block:: bash

   sphinx-build -M html docs build_docs

The generated HTML documentation can be found in `build_docs/html`.


*Copyright (c) 2024, Arm Limited. All rights reserved.*

