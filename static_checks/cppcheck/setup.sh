#!/bin/bash
#-------------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

set -e

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
else
  wget -q https://github.com/danmar/cppcheck/archive/refs/tags/2.3.tar.gz -O /tmp/cppcheck.tar.gz
  tar -xf /tmp/cppcheck.tar.gz -C /tmp
  cd /tmp/cppcheck-*
  make FILESDIR=/usr/share/cppcheck install
fi

