#!/bin/bash
#-------------------------------------------------------------------------------
# Copyright (c) 2018-2019, Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

##
##@file
##@brief Common utility functions used by CMake related build and utility scripts
##
##This file can be "sourced" from other scripts to get access to variables and functions
##defined here.
##Example \code{.sh}. <path-to-tfm-ci-repo>/util_cmake.sh\endcode
##or \code{.sh}source <path-to-tfm-ci-repo>/util_cmake.sh\endcode
##

##@fn fix_win_path(string path)
##@brief Convert cygwin and msys path to windows like.
##@param[in] path
##@returns path in windows format
##
##This function converts MSYS and cygwin paths to windows like path. Can be used
##to print paths in error message which can be used withouth conversion. This
##way for example you can get "clickable" path in Eclipse error window.
##
##Usage:
##  Assuming current directory is <i>c:/somedir1/somedir2</i>
##  command | result
##  --------|-------
##  fix_win_path "/cygdrive/c/foo/bar"| c:/foo/bar
##  fix_win_path "/c/foo/bar"| c:/foo/bar
##  fix_win_path "../somedir1/foo/bar"| ../somedir1/foo/bar
##  fix_win_path `get_full_path "../somedir1/foo/bar"` | c:/somedir1/foo/bar
##
#This iis needed for doxygen for now.
#!void fix_win_path(string path){};
#
function fix_win_path() {
    local path="$@"
    #See if we run on windows
    if [ -e "c:/" ]
    then
        #sed:
        # 1. match /cygdrive/c/ like paths and convert to the c:/ format
        # 2. if 1 did not match conver /c/ path to c:/ format
        path=`builtin echo "$path"|sed "s/\/cygdrive\/\([a-zA-Z]\)\//\1:\//;tx;s/\/\([a-zA-Z]\)\//\1:\//;:x"`
    fi
    builtin echo "$path"
}

##@fn get_full_path(string path)
##@brief Convert the passed path to full path.
##@param[in] path
##@returns path converted to absolute full path.
##
##This function converts a path to absolute full path. The function will return
##execution environment specific path (/cygdrive/ under Cygwin c:/ under MSys
##and /foo/bar under Linux).
##The patch to conver may or may not contain a file name.
##
##Usage:
##  Assuming current directory is <i>c:/somedir1/somedir2</i>
##  environment | command | result
##  --------|--------|-------
## Cygwin|get_full_path "."| /cygdrive/c/somedir1/somedir2
## MSys|get_full_path "."| c:/somedir1/somedir2
## Linux|get_full_path "."| /somedir1/somedir2
##
#This iis needed for doxygen for now.
#!void get_full_path(string path){};
#
function get_full_path {
    local file=""
    local dir=$1
    #If the paramether is a file, split it to directory and file name component.
    if [ -f "$dir" ]
    then
        dir=`dirname "$1"`
        file=`basename "$1"`
    fi

    if [ -z "$dir" ]
    then
        dir="."
    fi

    #Enter the directory to get it's full path
    pushd "$dir" >/dev/null
    local path=$PWD
    popd >/dev/null

    #On windows further fixing is needed to get a windows path
    case "$os_name" in
    CYGWIN)
        path=`cygpath -m $path`
        ;;
    MSYS)
        path=`echo $path| sed "s/^\/\([a-zA-Z]\)\//\1:\//"`
        ;;
    esac

    echo "$path/$file"
}


##@fn make_build_dir_name(path build_base_dir, string build_config_name)
##@brief Create the location for the a build.
##@param[in] build_base_dir
##@param[in] build_config_name
##@returns The generated path.
##
##This function will generate the name for a build directory. The generated name
##follow the pattern "<build_base_dir>/build-<build_config_name>".
##The generted path will be absolute.
##
##Usage:
##  Assuming CMakeList.txt file is in /foo/bar directory.
##  command | result
##  --------|-------
##  make_build_dir_name "/foo/bar" "test_build_st32" | Return /foo/bar/build-test_build_st32
##
#This iis needed for doxygen for now.
#!void make_build_dir_name(path build_base_dir, string build_config_name){};
#
function make_build_dir_name() {
    local build_base_dir=$(get_full_path $1)
    local build_config_name=$2
    echo "${build_base_dir}build-$build_config_name"
}

##@fn generate_project(string src_dir, string build_base_dir, string build_config_name, string cmake_params)
##@brief Execute CMake generation phase for a project
##@param[in] src_dir
##@param[in] build_base_dir
##@param[in] build_config_name
##@param[in] cmake_params
##@returns N/A
##
##This function will create a build directory named "build-<build_config_name>"
##under the passed <build_base_dir> directory, and execute CMake inside to
##generate "Unix Makefiles".
##CMake output is saved to <build_base_dir>/build-<build_config_name>/build.log
##
##Usage:
##  Assuming CMakeList.txt file is in /foo/bar directory.
##  command | result
##  --------|-------
## generate_project "/foo/bar" "/tmp/build" "test_build_st32" "-DCMAKE_BUILD_TYPE=Debug"| Generate makefiles under /tmp/buid/build-test_build_st32 for project /foo/bar/CMakeLists.txt
##
#This iis needed for doxygen for now.
#!void generate_project(string dir, string build_base_dir, string build_config_name, string cmake_params){};
#
function generate_project {
    local src_dir=$1
    local build_base_dir=$2
    local bcfg_name=$3
    local cm_params=$4
    local bdir=$(make_build_dir_name "$build_base_dir" "$bcfg_name")
    local error=0

    #If build ditrectory exists, clear it
    if [ -e "$bdir" ]
    then
        rm -rf $bdir/*
    else
        #Create build directory
        mkdir $bdir
    fi
    #Enter build directory
    if pushd $bdir >/dev/null
    then
        #Start cmake to generate makefiles and start the build
        cmake -G"Unix Makefiles" CMAKE_MAKE_PROGRAM=$CMAKE_MAKE_PROGRAM $cm_params "$src_dir" 2>&1 | tee -a build.log
        error=$(( ${PIPESTATUS[0]} + ${PIPESTATUS[1]} ))
        #Back to original location
        popd >/dev/null
    else
        error=1
    fi
    return $error
}

##@fn build_project(string src_dir, string build_base_dir, string build_config_name, string cmake_params)
##@brief Build a CMake project with gnumake.
##@param[in] src_dir
##@param[in] build_base_dir
##@param[in] build_config_name
##@param[in] cmake_params
##@returns N/A
##
##This function will call \ref generate_project to generate makefiles with CMake
##and will execute make to build the project.
##Make output is saved to <dir>/build-<build_config_name>/build.log
##
##Usage:
##  Assuming CMakeList.txt file is in /foo/bar directory.
##  command | result
##  --------|-------
##  build_project "/foo/bar" "test_build_st32" "-DCMAKE_BUILD_TYPE=Debug"| Generate makefiles under /foo/bar/build-test_build_st32 for project /foo/bar/CMakeLists.txt
##
#This iis needed for doxygen for now.
#!void build_project(string src_dir, string build_base_dir, string build_config_name, string cmake_params){};
#
function build_project {
    local src_dir=$1
    local build_base_dir=$2
    local bcfg_name=$3
    local cm_params=$4
    local error=0

    if generate_project "$src_dir" "$build_base_dir" "$bcfg_name" "$cm_params"
    then
        local bdir=$(make_build_dir_name "$build_base_dir" "$bcfg_name")
        if pushd "$bdir" >/dev/null
        then
            cmake --build . -- -j VERBOSE=1 2>&1 | tee -a build.log
            error=$(( ${PIPESTATUS[0]} + ${PIPESTATUS[1]} ))
        fi
        #Back to original location
        popd >/dev/null
    else
        error=1
    fi
    return $error
}

##@fn proj_dir_to_name(path proj_dir)
##@brief Convert a project directory to project name
##@param[in] proj_dir
##@returns The converted name.
##
##This function will convert a project path to project name. Conversion rules:
##  * the leading "./" is removed
##  * all '/' (directory separator's) are replaced by '-'
##  * if the result is empty, the name "top_level" is used.
##
##project_list.
##
##Usage:
##  Assuming CMakeList.txt file is in /foo/bar directory.
##  command | result
##  --------|-------
##  project_list=(./ app secure_fw test ); proj_dir_to_name "test_build_st32" "-DCMAKE_BUILD_TYPE=Debug" project_list | Build all projects listed in project_list array.
##
#This iis needed for doxygen for now.
#!void proj_dir_to_name(path proj_dir){};
#
function proj_dir_to_name {
    local proj=$1
    local name=$(echo "$proj" | sed 's/^\.\///;s/\//-/g')
    if [ -z "$name" ]
    then
        name="top_level"
    fi
    echo "$name"
}

##@fn build_proj_set(path build_base_dir, string build_config_name, string cmake_params, path project_list[])
##@brief Build a CMake project with gnumake.
##@param[in] build_base_dir
##@param[in] build_config_name
##@param[in] cmake_params
##@param[in] project_list
##@returns N/A
##
##This function will call \ref build_project for all CMake projects listed in
##project_list.
##
##Usage:
##  Assuming CMakeList.txt file is in /foo/bar directory.
##  command | result
##  --------|-------
##  project_list=(./ app secure_fw test ); build_proj_set "test_build_st32" "-DCMAKE_BUILD_TYPE=Debug" project_list | Build all projects listed in project_list array.
##
#This iis needed for doxygen for now.
#!void build_proj_set(path build_base_dir, string build_config_name, string cmake_params, path project_list[]){};
#
function build_proj_set {
    local build_base_dir=$1
    local bcfg_name=$2
    local cm_params=$3
    local -n ref_project_list
    ref_project_list=$4
    local error=0
    #For all projects in the list
    for proj in "${ref_project_list[@]}"
    do
        #Convert the project location to a name.
        local bcfg_name_ext="${bcfg_name}"_$(proj_dir_to_name "$proj")
        #Convert project location to absolute path.
        proj=$(get_full_path "$proj")
        echo "build_project $proj $build_base_dir $bcfg_name_ext $cm_params"
        #Build the project
        build_project "$proj" "$build_base_dir" "$bcfg_name_ext" "$cm_params" || error=1
    done
    return $error
}