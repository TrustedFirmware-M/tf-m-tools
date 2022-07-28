#-------------------------------------------------------------------------------
# Copyright (c) 2022, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
#-------------------------------------------------------------------------------

"""This module contains utility functions for tests."""

import os
import tempfile
from io import BytesIO
from cbor2 import CBOREncoder
from iatverifier.util import read_token_map

def bytes_equal_to_file(data, filepath):
    """
    return compare a bytestring and the content of a file and return whether they are the same
    """
    with open(filepath, 'rb') as file:
        file_data = file.read()
        if len(file_data) != len(data):
            return False
        for bytes1, bytes2 in zip(data, file_data):
            if bytes1 != bytes2:
                return False
    return True

def convert_map_to_token_bytes(token_map, verifier, add_p_header):
    """Converts a map to cbor token"""
    with BytesIO() as bytes_io:
        encoder = CBOREncoder(bytes_io)
        verifier.convert_map_to_token(
            encoder,
            token_map,
            add_p_header=add_p_header,
            name_as_key=True,
            parse_raw_value=True,
            root=True)
        return bytes_io.getvalue()

def create_token(data_dir, source_name, verifier, add_p_header):
    """Creats a cbor token from a yaml file."""
    source_path = os.path.join(data_dir, source_name)
    token_map = read_token_map(source_path)
    return convert_map_to_token_bytes(token_map, verifier, add_p_header)

def create_token_file(data_dir, source_name, verifier, dest_path, *, add_p_header=False):
    """Create a cbor token from a yaml file and write it to a file
    """
    token = create_token(
        data_dir=data_dir,
        source_name=source_name,
        verifier=verifier,
        add_p_header=add_p_header)

    with open(dest_path, 'wb') as wfh:
        wfh.write(token)

def create_token_tmp_file(data_dir, source_name, verifier):
    """Create a cbor token from a yaml file and write it to a temp file. Return the name of the temp
    file
    """
    temp_file, dest_path = tempfile.mkstemp()
    os.close(temp_file)
    create_token_file(data_dir, source_name, verifier, dest_path)
    return dest_path


def read_iat(data_dir, filename, verifier, *, check_p_header=False):
    """Read a cbor file and returns the parsed dictionary"""
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'rb') as file:
        return verifier.parse_token(
            token=file.read(),
            verify=True,
            check_p_header=check_p_header,
            lower_case_key=False)

def create_and_read_iat(data_dir, source_name, verifier):
    """Read a yaml file, compile it into a cbor token, and read it back"""
    token_file = create_token_tmp_file(data_dir, source_name, verifier)
    return read_iat(data_dir, token_file, verifier)
