#  Copyright (c) 2024 Arm Limited. All Rights Reserved.
#
#  SPDX-License-Identifier: BSD-3-Clause


###############################
#        USER COMMANDS        #
###############################

## all: build all TF-Fuzz binaries.
.PHONY: all
all: tfz

## tfz: build the tfz binary.
.PHONY: tfz
tfz: bin/tfz

## clean: remove all build files.
.PHONY: clean
clean:
	rm -rf bin
	$(MAKE) -C tfz-cpp clean

## help: get help.
.PHONY: help
help: Makefile
	@sed -n 's/^## //p' $<


#############################
#        BUILD RULES        #
#############################
bin:
	mkdir -p bin

.PHONY: bin/tfz
bin/tfz: | bin
	$(MAKE) -C tfz-cpp
	cp -f tfz-cpp/tfz bin/tfz
