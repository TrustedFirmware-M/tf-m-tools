#!/bin/bash
# Copyright (c) 2020, Arm Limited. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# Generate TF-M documentation

# Make sure that path to PlantUML JAR is exported before running this script
#export PLANTUML_JAR_PATH=/c/plantuml/plantuml.jar

# Update link to reference manual
sed -i 's|https://ci.trustedfirmware.org/job/tf-m-build-docs/lastSuccessfulBuild/artifact/trusted-firmware-m/build/install/doc/|../|' ./trusted-firmware-m/docs/index.rst

# Create directory for reference manual
mkdir -p ./trusted-firmware-m/docs/reference_manual

pushd ./trusted-firmware-m/build_docs

# Create empty environment variable
echo "cmake_env = None" > tfm_env.py

# Generate reference and user manual
sphinx-build.exe . user_guide

# Move generated documentation
mv reference_manual/html ../docs/reference_manual
mv user_guide ../docs

popd

# Delete documentation tools
rm -rf ./trusted-firmware-m/tools/documentation

# Delete documentation sources
find ./trusted-firmware-m -name *.rst -delete
find ./trusted-firmware-m -name *.dox -delete
find ./tf-m-tests -name *.rst -delete
find ./tf-m-tests -name *.dox -delete
