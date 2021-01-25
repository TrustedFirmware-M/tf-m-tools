# CMSIS TF-M Packs

This repository contains tools and data to create TF-M [CMSIS-Packs](https://arm-software.github.io/CMSIS_5/Pack/html/index.html).

## Prerequisites
- bash compatible shell (under Windows, use for example [git bash](https://gitforwindows.org/))
- [Git](https://git-scm.com/downloads)
- [7-Zip](https://www.7-zip.org/download.html)
- [Python](https://www.python.org/downloads/) v3.6 or later
- [Doxygen](https://www.doxygen.nl/download.html) v1.8.0 or later (for building documentation)
- [Graphviz](https://graphviz.org/download/) v2.38.0 or later (for building documentation)
- [PlantUML](http://sourceforge.net/projects/plantuml/files/plantuml.jar/download) v1.2018.11 or later
  in PLANTUML_JAR_PATH (for building documentation)
- Java runtime environment 1.8 or later (for running PlantUML)
- CMSIS Pack installed in CMSIS_PACK_ROOT (for PackChk utility)

## Create packs

1. Open a bash compatible shell
2. Run `./setup.sh` script. The script will:
   - install the required python packages
   - clone the trusted-firmware-m repository
   - clone the tf-m-tests repository
   - clone the mcuboot repository
   - merge mcuboot into trusted-firmware-m
   - apply patches for trusted-firmware-m
   - apply patches for tf-m-tests
   - generate template based files
   - setup tf-m-tests (copy/move files from trusted-firmware-m)
   - merge addon files for trusted-firmware-m
   - merge addon files for tf-m-tests
3. Generate TF-M documentation:
   - setup path variable for PlantUML:
     `export PLANTUML_JAR_PATH=<plantuml_Path>/plantuml.jar`
   - run `gen_doc.sh` script
4. Generate CMSIS-Packs:
   - TFM:
     - go to `./trusted-firmware-m` directory
     - run `gen_pack.sh` script
     - generated pack is available in the `output` directory
   - TFM-Test:
     - go to `./tf-m-tests` directory
     - run `gen_pack.sh` script
     - generated pack is available in the `output` directory
   - V2M-MPS2_SSE_200_TFM-PF (TF-M Platform support for MPS2):
     - run `setup_mps2.sh` script
     - go to `./tf-m-platform-mps2` directory
     - run `gen_pack.sh` script
     - generated pack is available in the `output` directory
     - note: this pack should not be published and used only for testing TF-M
5. Run `./clean.sh` script to delete all intermediate and generated files
