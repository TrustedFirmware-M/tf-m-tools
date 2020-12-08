# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

set_default()
{
    if test -z "$(eval echo '$'$1)"
    then
        eval export $1='$2'
    fi
}

info()
{
    printf "[INF] $1\n" 1>&2
}
warn()
{
    printf "\e[33m[WRN] $1\e[0m\n" 1>&2
}
error()
{
    printf "\e[31m[ERR] $1\e[0m\n" 1>&2
    if test -n "$2"
    then
        exit $2
    else
        exit 1
    fi
}
