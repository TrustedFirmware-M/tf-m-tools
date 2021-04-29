:: --------------------------------------------------------------------------
:: Copyright (c) 2021, Arm Limited. All rights reserved.
::
:: SPDX-License-Identifier: BSD-3-Clause
::
:: --------------------------------------------------------------------------

@ECHO OFF

SET script_path=%~dp0

call %script_path%\..\config\Windows\container_cfg.cmd

set command="cmake -S . -B %BUILD_DIR% -DTFM_PLATFORM=%PLATFORM% -DTFM_TOOLCHAIN_FILE=toolchain_ARMCLANG.cmake && cmake --build %BUILD_DIR%  -- install"

docker run -it --rm -v %LOCAL_TFM_REPO%:/opt/trusted-firmware-m %ARMCLANG_IMG_NAME% %command%
PAUSE