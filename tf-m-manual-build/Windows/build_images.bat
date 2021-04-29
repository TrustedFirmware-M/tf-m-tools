:: --------------------------------------------------------------------------
:: Copyright (c) 2021, Arm Limited. All rights reserved.
::
:: SPDX-License-Identifier: BSD-3-Clause
::
:: --------------------------------------------------------------------------

@ECHO OFF

SET script_path=%~dp0

call %script_path%\..\config\Windows\container_cfg.cmd

if "%~1"=="" goto usage
if "%~1"=="gnu" goto gnu
if "%~1"=="docs" goto docs
if "%~1"=="armclang" goto armclang
if "%~1"=="all" goto all

:gnu
docker build -t %CORE_IMG_NAME%     --build-arg build_dir=%BUILD_DIR% -f ../source/TFM_core/Dockerfile  ../config/
cmd /k

:docs
docker build -t %CORE_IMG_NAME%     --build-arg build_dir=%BUILD_DIR% -f ../source/TFM_core/Dockerfile  ../config/
docker build -t %DOCS_IMG_NAME%     --build-arg docs_dir=%DOCS_DIR% -f ../source/doc/Dockerfile       ../config/
cmd /k

:armclang
docker build -t %CORE_IMG_NAME%     --build-arg build_dir=%BUILD_DIR% -f ../source/TFM_core/Dockerfile  ../config/
:eula_warning
SET /P PROMPT="To build this armclang docker image, the arm compiler will be used (https://developer.arm.com/tools-and-software/embedded/arm-compiler/downloads/version-6). Do you confirm that you have read and understood the contained EULA and that you agree to it ? (Y/[N])"
IF /I "%PROMPT%" NEQ "Y" GOTO END
docker build -t %ARMCLANG_IMG_NAME% --build-arg license=%ARMLMD_LICENSE_FILE% --build-arg build_dir=%BUILD_DIR% -f ../source/TFM_CLANG/Dockerfile ../config/
cmd /k

:all
docker build -t %CORE_IMG_NAME%     --build-arg build_dir=%BUILD_DIR% -f ../source/TFM_core/Dockerfile  ../config/
docker build -t %DOCS_IMG_NAME%     --build-arg docs_dir=%DOCS_DIR% -f ../source/doc/Dockerfile       ../config/
goto eula_warning

:usage
ECHO "Usage: %script_path%\build_images.bat <gnu|armclang|docs|all>"
cmd /k

:END
cmd /k