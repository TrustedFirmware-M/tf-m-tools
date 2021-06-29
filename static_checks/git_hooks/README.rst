#########
Git Hooks
#########

This directory is aimed at providing **code snippets** which can be inserted
to developer's git hooks, and allow them to run the Static Check Framework
before pushing a patch.

For full description and capabilities, please refer to the official
documentation for `Git SCM Hooks`_ .

*************
Adding a hook
*************

To use a specific hook, please manually copy the snippet to the file with
matching name, located at

.. code-block:: bash

    TF-M-ROOT/.git/hooks/{HOOK_FILENAME}


********
Pre-Push
********

Enabling SCF requires adding the snippet on the pre-push hook. This is so that
the check can be performed **BEFORE** a developer pushes a new patch to Gerrit
and *ONLY IF* requested by the user.

With the aim of making the functionality unintrusive, the
following environment variables are required.

- `SCF_ORG`: To set the Organisation for the purposes of Header/Copyright check.
- `SCF_ENABLE`: To enable checking before pushing a patch.

_If not set SCF_ORG defaults to 'arm'_

**********************
Custom directory paths
**********************

By default the reference code assumes the standard directory structure for
TF-M and dependencies.

.. code-block:: bash
    └── dev-dir
        ├── tf-m
        ├── tf-m-tools

The user can override this by setting the `TFM_ROOT_PATH`, `SCF_TEST_PATH`,
`SCF_TEST_APP` environment variables, to match his needs.

*********
Using SCP
*********

Assuming the developer has already set-up trusted-firmware-m and tf-m-tools
and has already copied the snippet over to `<TF-M-ROOT>/.git/hooks/pre-push`

.. code-block:: bash

    cd <TF-M-ROOT>
    env SCF_ENABLE=1 git push origin HEAD:refs/for/master


.. _Git SCM Hooks: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks

*Copyright (c) 2021, Arm Limited. All rights reserved.*
*SPDX-License-Identifier: BSD-3-Clause*
