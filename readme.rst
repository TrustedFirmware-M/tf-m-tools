########################
Trusted Firmware-M Tools
########################

Trusted Firmware-M Tools is a collection of helper tools used across the
Trusted Firmware-M(TF-M) ecosystem for development, validation, CI, and analysis.

.. important::
  This git contains the source code for Trusted Firmware-M. It is primarily
  hosted at `git.trustedfirmware.org`_ with a read-only mirror available on
  `GitHub`_.

Overview
========

This repository contains tools and utilities that complement TF-M development, including:

* CMSIS TF-M Packs utilities
* Code size analysis tooling
* FIH test tooling
* Initial Attestation verifier tooling
* IRQ test tooling
* Library dependency trace tooling
* Profiling helpers
* SQUAD metrics dashboard utilities
* Static checking framework (e.g. cppcheck, clang-format, checkpatch, header checks, git hooks)
* TF-Fuzz utilities
* TF-M Docker build helpers

For detailed documentation of each tool, see the TF-M Tools documentation on `Read the Docs`_.

Repository structure
====================

The repository is organized into multiple tool areas (each with its own scripts and in some
cases documentation). A typical layout includes:

* ``docs/``  - Sphinx documentation sources. The rendered version of the documentation
  is published on `Read the Docs`_
* Tool-specific directories and supporting libraries/scripts

(Exact layout may evolve as tools are added or reorganized.)

License
=======

This software is provided under the `BSD-3-Clause license <license.rst>`.
Contributions to this project are accepted under the same license,
with developer sign-off as described in the `Contribution guidelines`_.
Some files taken from external projects are licensed under `Apache-2.0 <apache-2.0.txt>`_

Links
=====

* `Trusted Firmware-M (TF-M) project homepage
  <https://www.trustedfirmware.org/projects/tf-m/>`_
* `TF-M documentation
  <https://trustedfirmware-m.readthedocs.io/en/latest/index.html>`_
* `TF-M Tools documentation (Read the Docs)
  <https://trustedfirmware-m.readthedocs.io/projects/tf-m-tools/en/latest>`_


Feedback and support
====================

Feedback can be submitted via email to the
`TF-M mailing list <tf-m@lists.trustedfirmware.org>`__.

.. _Contribution guidelines: https://trustedfirmware-m.readthedocs.io/en/latest/contributing/contributing_process.html
.. _trustedfirmware.org: https://www.trustedfirmware.org
.. _git.trustedfirmware.org: https://git.trustedfirmware.org/plugins/gitiles/TF-M/tf-m-tools
.. _GitHub: https://github.com/TrustedFirmware-M/tf-m-tools
.. _Read the Docs: https://trustedfirmware-m.readthedocs.io/projects/tf-m-tools/en/latest

*Copyright (c) 2026, Arm Limited. All rights reserved.*
