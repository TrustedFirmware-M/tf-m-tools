/*
 * Copyright (c) 2019-2020, Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#ifndef BL2_CONFIG_H
#define BL2_CONFIG_H

//-------- <<< Use Configuration Wizard in Context Menu >>> --------------------

// <h>MCUboot Configuration

//   <o>Upgrade Strategy
//     <1=> Overwrite Only  <2=> Swap  <3=> Direct XIP <4=> RAM Loading
#define MCUBOOT_UPGRADE_STRATEGY    1

//   <o>Signature Type
//     <1=> RSA-3072 <2=> RSA-2048
#define MCUBOOT_SIGNATURE_TYPE      1

//   <c>Encrypt Images
#define MCUBOOT_ENC_IMAGES
//   </c>

//   <o>Number of Images
//     <1=> 1 <2=> 2
//   <i> 1: Single Image, secure and non-secure images are signed and updated together.
//   <i> 2: Mulitple Image, secure and non-secure images are signed and updatable independently.
#define MCUBOOT_IMAGE_NUMBER        2

//   <c>Hardware Key
#define MCUBOOT_HW_KEY
//   </c>

// <o>Logging Level
//   <0=> Off  <1=> Error  <2=> Warning  <3=> Info  <4=> Debug
#define MCUBOOT_LOG_LEVEL           3

// </h>

//------------- <<< end of configuration section >>> ---------------------------

#if    (MCUBOOT_UPGRADE_STRATEGY == 1)
#define MCUBOOT_OVERWRITE_ONLY
#elif  (MCUBOOT_UPGRADE_STRATEGY == 2)
#define MCUBOOT_SWAP_USING_MOVE
#elif  (MCUBOOT_UPGRADE_STRATEGY == 3)
#define MCUBOOT_DIRECT_XIP
#elif  (MCUBOOT_UPGRADE_STRATEGY == 4)
#define MCUBOOT_RAM_LOADING
#else
#error "MCUboot Configuration: Invalid Upgrade Strategy!"
#endif

#if    (MCUBOOT_SIGNATURE_TYPE == 1)
#define MCUBOOT_SIGN_RSA
#define MCUBOOT_SIGN_RSA_LEN 3072
#elif  (MCUBOOT_SIGNATURE_TYPE == 2)
#define MCUBOOT_SIGN_RSA
#define MCUBOOT_SIGN_RSA_LEN 2048
#else
#error "MCUboot Configuration: Invalid Signature Type!"
#endif

#ifdef  MCUBOOT_ENC_IMAGES
#define MCUBOOT_ENCRYPT_RSA
#endif

#if   ((MCUBOOT_IMAGE_NUMBER != 1) && (MCUBOOT_IMAGE_NUMBER != 2))
#error "MCUboot Configuration: Invalid number of Images!"
#endif

#if   ((MCUBOOT_UPGRADE_STRATEGY == 3) || (MCUBOOT_UPGRADE_STRATEGY == 4))
#if    (MCUBOOT_IMAGE_NUMBER != 1)
#error "MCUboot Configuration: Direct XIP and RAM Loading Upgrade Strategy supports only single image!"
#endif
#ifdef MCUBOOT_ENC_IMAGES
#error "MCUboot Configuration: Image encryption is not supported for Direct XIP and RAM Loading Upgrade Strategy!"
#endif
#endif

#define MCUBOOT_HW_ROLLBACK_PROT
#define MCUBOOT_MEASURED_BOOT

#endif /* BL2_CONFIG_H */
