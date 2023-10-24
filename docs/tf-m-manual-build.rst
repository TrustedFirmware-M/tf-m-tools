##########################
Using docker to build TF-M
##########################

This tool has been made to provide an easy way to build the trusted firmware m
project without having to set up a whole working environment.The only tool
necessary is docker.

************************
Configuration Parameters
************************

The config file /config/container_cfg is used to set up the tool. the following
parameters are available :

- CORE_IMG_NAME : Name of the main docker image running GNUARM
- ARMCLANG_IMG_NAME : Name of the image using ARMCLANG. This image is based
  on the core image.
- DOCS_IMG_NAME : Name of the image used to build the documentation. This
  image is based on the core image.
- BUILD_DIR : Name of the directory where the build files will be generated. If
  your current TFM repository has a directory named the same, it will be
  deleted.
- DOCS_DIR : Name of the directory where the documentation files will be
  generated. If your current TFM repository has a directory named the same,
  it will be deleted.

- LOCAL_TFM_REPO : path to your local tfm repository. this parameter is
  mandatory
- PLATFORM : Name of the platform used for the TFM build.
- ADDITIONNAL_PARAMETERS (optionnal) : additionnal parameters for the TFM
  build.

*****************
Building an image
*****************

To build the docker images (TFM_Core, TFM_Armclang and TFM_documentation),
launch the build_images.sh script.

****************
Running an image
****************

To launch a container, launch the corresponding run_xxx.sh script. Your local
TFM repo will be mounted in the containerand the generated files will be
available in your local TFM repo after the build.

To launch a container and build TFM manually, use the following command :

docker run -it --rm --user $(id -u):$(id -g) -v /etc/group:/etc/group:ro \
  -v /etc/passwd:/etc/passwd:ro -v /etc/shadow:/etc/shadow:ro -v \
  $LOCAL_TFM_REPO:/opt/trusted-firmware-m --entrypoint /bin/bash $CORE_IMG_NAME

Note : Armclang currently uses the ARMLTD_LICENSE_FILE variable which should
point to a license server.

--------------

*Copyright (c) 2021, Arm Limited. All rights reserved.*
*SPDX-License-Identifier: BSD-3-Clause*
