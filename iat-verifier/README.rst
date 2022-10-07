############################
Initial Attestation Verifier
############################
This is a set of utility scripts for working with PSA Initial Attestation
Token, the structure of which is described here:

   https://tools.ietf.org/html/draft-tschofenig-rats-psa-token-05

The following utilities are provided:

check_iat
   Verifies the structure, and optionally the signature, of a token.

compile_token
   Creates a (optionally, signed) token from a YAML descriptions of the claims.

decompile_token
   Generates a YAML descriptions of the claims contained within a token. (Note:
   this description can then be compiled back into a token using compile_token.)


************
Installation
************
You can install the script using pip:

.. code:: bash

   # Inside the directory containg this README
   pip3 install .

This should automatically install all the required dependencies. Please
see ``setup.py`` for the list of said dependencies.

*****
Usage
*****

.. note::
   You can use ``-h`` flag with any of the scripts to see their usage help.

check_iat
---------

After installing, you should have ``check_iat`` script in your ``PATH``. The
script expects two parameters:

* a path to the signed IAT in COSE format

* the token type

You can find an example in the ``sample`` directory.

The script will extract the COSE payload and make sure that it is a
valid IAT (i.e. all mandatory fields are present, and all known
fields have correct size/type):

.. code:: bash

   $ check_iat -t PSA-IoT-Profile1-token sample/cbor/iat.cbor
   Token format OK

If you want the script to verify the signature, you need to specify the
file containing the signing key in PEM format using -k option. The key
used to sign sample/iat.cbor is inside sample/key.pem.

::

   $ check_iat -t PSA-IoT-Profile1-token -k sample/key.pem sample/cbor/iat.cbor
   Signature OK
   Token format OK

You can add a -p flag to the invocation in order to have the script
print out the decoded IAT in JSON format. It should look something like
this:

.. code:: json

    {
        "INSTANCE_ID": "b'0107060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'",
        "IMPLEMENTATION_ID": "b'07060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'",
        "CHALLENGE": "b'07060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'",
        "CLIENT_ID": 2,
        "SECURITY_LIFECYCLE": "SL_SECURED",
        "PROFILE_ID": "http://example.com",
        "BOOT_SEED": "b'07060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'",
        "SW_COMPONENTS": [
            {
                "SW_COMPONENT_TYPE": "BL",
                "SIGNER_ID": "b'07060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'",
                "SW_COMPONENT_VERSION": "3.4.2",
                "MEASUREMENT_VALUE": "b'07060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'",
                "MEASUREMENT_DESCRIPTION": "TF-M_SHA256MemPreXIP"
            },
            {
                "SW_COMPONENT_TYPE": "M1",
                "SIGNER_ID": "b'07060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'",
                "SW_COMPONENT_VERSION": "1.2",
                "MEASUREMENT_VALUE": "b'07060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'"
            },
            {
                "SW_COMPONENT_TYPE": "M2",
                "SIGNER_ID": "b'07060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'",
                "SW_COMPONENT_VERSION": "1.2.3",
                "MEASUREMENT_VALUE": "b'07060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'"
            },
            {
                "SW_COMPONENT_TYPE": "M3",
                "SIGNER_ID": "b'07060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'",
                "SW_COMPONENT_VERSION": "1",
                "MEASUREMENT_VALUE": "b'07060504030201000F0E0D0C0B0A090817161514131211101F1E1D1C1B1A1918'"
            }
        ]
    }

compile_token
-------------

You can use this script to compile a YAML claims description into a COSE-wrapped
CBOR token:

.. code:: bash

   $ compile_token -t PSA-IoT-Profile1-token -k sample/key.pem sample/yaml/iat.yaml > sample_token.cbor

*No validation* is performed as part of this, so there is no guarantee that a
valid IAT will be produced.

You can omit the ``-k`` option, in which case, the resulting token will not be
signed, however it will still be wrapped in COSE "envelope". If you would like
to produce a pure CBOR encoding of the claims without a COSE wrapper, you can
use ``-r`` flag.


decompile_token
---------------

Decompile an IAT (or any COSE-wrapped CBOR object -- *no validation* is performed
as part of this) into a YAML description of its claims.


.. code:: bash

    $ decompile_token -t PSA-IoT-Profile1-token sample/cbor/iat.cbor
    boot_seed: !!binary |
      BwYFBAMCAQAPDg0MCwoJCBcWFRQTEhEQHx4dHBsaGRg=
    challenge: !!binary |
      BwYFBAMCAQAPDg0MCwoJCBcWFRQTEhEQHx4dHBsaGRg=
    client_id: 2
    implementation_id: !!binary |
      BwYFBAMCAQAPDg0MCwoJCBcWFRQTEhEQHx4dHBsaGRg=
    instance_id: !!binary |
      AQcGBQQDAgEADw4NDAsKCQgXFhUUExIREB8eHRwbGhkY
    profile_id: http://example.com
    security_lifecycle: SL_SECURED
    sw_components:
    - measurement_description: TF-M_SHA256MemPreXIP
      measurement_value: !!binary |
        BwYFBAMCAQAPDg0MCwoJCBcWFRQTEhEQHx4dHBsaGRg=
      signer_id: !!binary |
        BwYFBAMCAQAPDg0MCwoJCBcWFRQTEhEQHx4dHBsaGRg=
      sw_component_type: BL
      sw_component_version: 3.4.2
    - measurement_value: !!binary |
        BwYFBAMCAQAPDg0MCwoJCBcWFRQTEhEQHx4dHBsaGRg=
      signer_id: !!binary |
        BwYFBAMCAQAPDg0MCwoJCBcWFRQTEhEQHx4dHBsaGRg=
      sw_component_type: M1
      sw_component_version: '1.2'
    - measurement_value: !!binary |
        BwYFBAMCAQAPDg0MCwoJCBcWFRQTEhEQHx4dHBsaGRg=
      signer_id: !!binary |
        BwYFBAMCAQAPDg0MCwoJCBcWFRQTEhEQHx4dHBsaGRg=
      sw_component_type: M2
      sw_component_version: 1.2.3
    - measurement_value: !!binary |
        BwYFBAMCAQAPDg0MCwoJCBcWFRQTEhEQHx4dHBsaGRg=
      signer_id: !!binary |
        BwYFBAMCAQAPDg0MCwoJCBcWFRQTEhEQHx4dHBsaGRg=
      sw_component_type: M3
      sw_component_version: '1'

This description can then be compiled back into CBOR using ``compile_token``.


***********
Mac0Message
***********

By default, the expectation is that the message will be wrapped using
Sign1Message  COSE structure, however, the alternative Mac0Message structure
that uses HMAC with SHA256 algorithm rather than a signature is supported via
the ``-m mac`` flag:

::

    $ check_iat -t PSA-IoT-Profile1-token -m mac -k sample/hmac.key sample/iat-hmac.cbor
    Signature OK
    Token format OK

*******
Testing
*******
Tests can be run using ``nose2``:

.. code:: bash

   pip install nose2

Then run by executing ``nose2`` in the root directory.


*******************
Development Scripts
*******************
The following utility scripts are contained within ``dev_scripts``
subdirectory and were utilized in development of this tool. They are not
need to use the iat-verifier script, and can generally be ignored.

.. code:: bash

   ./dev_scripts/generate-key.py OUTFILE

Generate an ECDSA (NIST256p curve) signing key and write it in PEM
format to the specified file.

.. code:: bash

   ./dev_scripts/generate-sample-iat.py KEYFILE OUTFILE

Generate a sample token, signing it with the specified key, and writing
the output to the specified file.

.. note::
   This script is deprecated -- use ``compile_token`` (see above) instead.

*********************
Adding new token type
*********************

#. Create a file with the claims for the new token type in
   `tf-m-tools/iat-verifier/iatverifier`.

   * For each claim a new class must be created that inherits from
     ``AttestationClaim`` or from one of its descendants

   * ``CompositeAttestClaim`` is descendants of ``AttestationClaim``, for
     details on how to use it see the documentation in the class definition.

   * For each claim, the methods ``get_claim_key(self=None)``,
     ``get_claim_name(self=None)`` must be implemented.

   * Other methods of ``AttestationClaim`` are optional to override.

   * Any claim that inherits from ``AttestationClaim`` might have a ``verify``
     method (``def verify(self, token_item):``). This method is called when the
     ``verify()`` method of a ``TokenItem`` object is called. ``TokenItem``'s
     ``verify()`` method walks up the inheritance tree of the ``claim_type``
     object's class in that ``TokenItem``. If a class in the walk path has a
     ``verify()`` method, calls it. For further details see ``TokenItem``'s
     ``_call_verify_with_parents()`` method.

     Any verify method needs to call ``AttestationClaim``'s ``error()`` or
     ``warning()`` in case of a problem. If the actual class inherits from
     ``AttestationTokenVerifier`` this can be done like
     ``self.error('Meaningful error message.')``. In other cases
     ``self.verifier.error('Meaningful error message.')``

#. Create a file for the new token in `tf-m-tools/iat-verifier/iatverifier`.

   * Create a new class for the token type. It must inherit from the class
     ``AttestationTokenVerifier``.

   * Implement ``get_claim_key(self=None)`` and ``get_claim_name(self=None)``

   * Implement the ``__init__(self, ...)`` function. This function must create a
     list with the claims that are accepted by this token. (Note that the
     ``AttestationTokenVerifier`` class inherits from ``AttestationClaim``. this
     makes it possible to create nested token). Each item is the list is a
     tuple:

     * first element is the class of the claim

     * Second is a dictionary containing the ``__init__`` function parameters
       for the claim

       * the key is the name of the parameter

       * the value is the value of the parameter

     The list of claims must be passed to the init function of the base class.

     For example see *iat-verifier/iatverifier/cca_token_verifier.py*.

#. Add handling of the new token type to the ``check_iat``, ``decompile_token``,
   and ``compile_token`` scripts.

--------------

*Copyright (c) 2019-2022, Arm Limited. All rights reserved.*
