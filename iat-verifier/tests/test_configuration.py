# -----------------------------------------------------------------------------
# Copyright (c) 2026, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
# -----------------------------------------------------------------------------

"""Tests for verifier configuration and its automatic CLI integration."""

import argparse
import unittest

from iatverifier.attest_token_verifier import VerifierConfiguration
from scripts.configuration import add_verifier_configuration_arguments
from scripts.configuration import configuration_from_arguments


class TestVerifierConfiguration(unittest.TestCase):
    def test_defaults_and_overrides(self):
        configuration = VerifierConfiguration({
            VerifierConfiguration.VERIFIER_STRICT: True,
        })

        self.assertTrue(configuration.get_config(VerifierConfiguration.VERIFIER_STRICT))
        self.assertFalse(configuration.get_config(VerifierConfiguration.VERIFIER_KEEP_GOING))
        self.assertTrue(configuration.get_config(
            VerifierConfiguration.CCA_VERIFIER_HAS_TYPE_INDICATOR))
        self.assertFalse(configuration.get_config(
            VerifierConfiguration.CCA_VERIFIER_LEGACY_TAG))

    def test_cli_arguments_are_generated_from_option_registry(self):
        parser = argparse.ArgumentParser()
        add_verifier_configuration_arguments(parser)
        args = parser.parse_args(["--verifier-strict"])
        configuration = configuration_from_arguments(args)

        self.assertTrue(configuration.get_config(VerifierConfiguration.VERIFIER_STRICT))

        default_arguments = vars(parser.parse_args([]))
        self.assertTrue(set(VerifierConfiguration.OPTIONS).issubset(default_arguments))
        self.assertIsNone(default_arguments[
            VerifierConfiguration.CCA_VERIFIER_HAS_TYPE_INDICATOR
        ])

    def test_cli_arguments_override_script_defaults(self):
        parser = argparse.ArgumentParser()
        add_verifier_configuration_arguments(parser)
        args = parser.parse_args(["--no-verifier-strict"])
        configuration = configuration_from_arguments(args, {
            VerifierConfiguration.VERIFIER_STRICT: True,
        })

        self.assertFalse(configuration.get_config(VerifierConfiguration.VERIFIER_STRICT))

    def test_script_defaults_override_configuration_defaults(self):
        parser = argparse.ArgumentParser()
        add_verifier_configuration_arguments(parser)
        configuration = configuration_from_arguments(parser.parse_args([]), {
            VerifierConfiguration.VERIFIER_STRICT: True,
        })

        self.assertTrue(configuration.get_config(VerifierConfiguration.VERIFIER_STRICT))

    def test_unknown_option_is_rejected(self):
        with self.assertRaises(ValueError):
            VerifierConfiguration({"not_a_registered_option": True})


if __name__ == "__main__":
    unittest.main()
