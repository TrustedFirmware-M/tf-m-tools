IAT Verifier
============

A Python tool for verifying, compiling, and decompiling Initial Attestation Tokens (IAT) used in Trusted Firmware-M (TF-M). Supports PSA IoT Profile 1, PSA 2.0.0, and CCA token formats encoded as COSE/CBOR.

Installation
------------

Requires Python >= 3.10 && <= 3.13 and `uv <https://docs.astral.sh/uv/>`_.

.. code-block:: bash

   uv sync

Commands
--------

``check_iat`` — Verify a token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validates a signed IAT: checks the signature, required fields, and field formats.

.. code-block::

   uv run check_iat -t TOKEN_TYPE -k KEY tokenfile [options]

+------------------------------+-----------------------------------------------------------------------------------+
| Option                       | Description                                                                       |
+==============================+===================================================================================+
| ``tokenfile``                | Path to the CBOR token file                                                       |
+------------------------------+-----------------------------------------------------------------------------------+
| ``-t``, ``--token-type``     | Token type (see below)                                                            |
+------------------------------+-----------------------------------------------------------------------------------+
| ``-k``, ``--key``            | Public or private key in PEM format (optional — skips signature check if omitted) |
+------------------------------+-----------------------------------------------------------------------------------+
| ``-p``, ``--print-iat``      | Print decoded token as JSON                                                       |
+------------------------------+-----------------------------------------------------------------------------------+
| ``-K``, ``--keep-going``     | Continue validation despite errors                                                |
+------------------------------+-----------------------------------------------------------------------------------+
| ``-s``, ``--strict``         | Fail on unknown claims                                                            |
+------------------------------+-----------------------------------------------------------------------------------+
| ``-m``, ``--method``         | COSE wrapping: ``sign`` (default), ``mac``, or ``raw``                            |
+------------------------------+-----------------------------------------------------------------------------------+
| ``--expect-token-indicator`` | Expect a token indicator in the CBOR                                              |
+------------------------------+-----------------------------------------------------------------------------------+

**Example:**

.. code-block:: bash

   uv run check_iat -t PSA-IoT-Profile1-token -k iak_pub.pem -p -K token.cbor

----

``compile_token`` — Compile a token from YAML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates a signed CBOR token from a YAML source file.

.. code-block::

   uv run compile_token -t TOKEN_TYPE source [options]

+---------------------------+--------------------------------------------------------+
| Option                    | Description                                            |
+===========================+========================================================+
| ``source``                | Token source in YAML format                            |
+---------------------------+--------------------------------------------------------+
| ``-t``, ``--token-type``  | Token type (see below)                                 |
+---------------------------+--------------------------------------------------------+
| ``-o``, ``--outfile``     | Output file (stdout if omitted)                        |
+---------------------------+--------------------------------------------------------+
| ``-k``, ``--key``         | Signing key in PEM format                              |
+---------------------------+--------------------------------------------------------+
| ``--platform-key``        | Platform token signing key (CCA tokens)                |
+---------------------------+--------------------------------------------------------+
| ``--realm-key``           | Realm token signing key (CCA tokens)                   |
+---------------------------+--------------------------------------------------------+
| ``-m``, ``--method``      | COSE wrapping: ``sign`` (default), ``mac``, or ``raw`` |
+---------------------------+--------------------------------------------------------+
| ``--gen-token-indicator`` | Add token indicator to CBOR                            |
+---------------------------+--------------------------------------------------------+

**Example:**

.. code-block:: bash

   uv run compile_token -t PSA-IoT-Profile1-token -k iak_priv.pem -o token.cbor token.yaml

----

``decompile_token`` — Decompile a token to YAML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parses a CBOR token and outputs its claims in YAML format.

.. code-block::

   uv run decompile_token -t TOKEN_TYPE source [options]

+------------------------------+--------------------------------------+
| Option                       | Description                          |
+==============================+======================================+
| ``source``                   | CBOR token file                      |
+------------------------------+--------------------------------------+
| ``-t``, ``--token-type``     | Token type (see below)               |
+------------------------------+--------------------------------------+
| ``-o``, ``--outfile``        | Output file (stdout if omitted)      |
+------------------------------+--------------------------------------+
| ``--expect-token-indicator`` | Expect a token indicator in the CBOR |
+------------------------------+--------------------------------------+

**Example:**

.. code-block:: bash

   uv run decompile_token -t PSA-IoT-Profile1-token -o token.yaml token.cbor

----

Supported token types
---------------------

+----------------------------+------------------------------------------------------------+
| Value                      | Description                                                |
+============================+============================================================+
| ``PSA-IoT-Profile1-token`` | PSA IoT Profile 1 attestation token                        |
+----------------------------+------------------------------------------------------------+
| ``PSA-2.0.0-token``        | PSA attestation token v2.0.0                               |
+----------------------------+------------------------------------------------------------+
| ``CCA-token``              | Confidential Compute Architecture token (platform + realm) |
+----------------------------+------------------------------------------------------------+
| ``CCA-plat-token``         | CCA platform token only                                    |
+----------------------------+------------------------------------------------------------+

Key generation
--------------

Generate an ECDSA key pair (NIST P-256 by default):

.. code-block:: bash

   # Private key
   uv run python dev_scripts/generate-key.py iak_priv.pem

   # Public key (from the private key)
   openssl ec -in iak_priv.pem -pubout -out iak_pub.pem

License
-------

SPDX-FileCopyrightText: Copyright The TrustedFirmware-M Contributors

SPDX-License-Identifier: BSD-3-Clause
