"""Shared command-line integration for verifier configuration."""

import argparse

from iatverifier.attest_token_verifier import VerifierConfiguration


def add_verifier_configuration_arguments(parser):
    """Add every verifier setting to an argument parser.

    Boolean settings use :class:`argparse.BooleanOptionalAction`, providing
    both ``--option`` and ``--no-option`` forms.  Argument names are derived
    from registry keys, so scripts need no changes when an exposed setting is
    added.
    """
    group = parser.add_argument_group("verifier configuration")
    for key, option in VerifierConfiguration.OPTIONS.items():
        flag = f"--{key.replace('_', '-')}"
        default = option["default"]
        kwargs = {
            "dest": key,
            # None distinguishes an omitted option from an explicit --no-...
            # so each script can supply its historical default.
            "default": None,
            "help": option["help"],
        }
        if isinstance(default, bool):
            kwargs["action"] = argparse.BooleanOptionalAction
        else:
            kwargs["type"] = type(default)
        group.add_argument(flag, **kwargs)


def configuration_from_arguments(args, script_defaults=None):
    """Build configuration, with explicit CLI values taking precedence."""
    values = dict(script_defaults or {})
    values.update({
        key: value
        for key in VerifierConfiguration.OPTIONS
        if (value := getattr(args, key)) is not None
    })
    return VerifierConfiguration(values)
