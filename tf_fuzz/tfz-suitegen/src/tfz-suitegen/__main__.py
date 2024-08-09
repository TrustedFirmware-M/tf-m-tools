#  Copyright (c) 2024 Arm Limited. All Rights Reserved.
#
#  SPDX-License-Identifier: BSD-3-Clause

import argparse
from pathlib import Path
import sys
import os
from jinja2 import Environment, PackageLoader, Template, select_autoescape
from tempfile import NamedTemporaryFile
from dataclasses import dataclass, field, asdict
import subprocess as sp
import re
from IPython import embed


@dataclass
class Test:
    """
    Template variables for a single test.

    For more details, see suite_templates/ns_test.c
    """

    fn_name: str
    c_file_name: str
    name: str = ""
    description: str = ""


@dataclass
class TestSuite:
    """
    Template variables for a test suite. The fields of this class are the
    top-level variables accessible from the template.

    For more details, see suite_templates/ns_test.c
    """

    tests: list[Test] = field(default_factory=lambda: list())


def main():
    parser = argparse.ArgumentParser(
        prog="python3 -m tfz-suitegen",
        description="TF-Fuzz Test Suite Generator for Trusted Firmware M",
        epilog="",
    )

    parser.add_argument("tfz_dir", help="Path to the tf_fuzz directory", type=Path)
    parser.add_argument(
        "input_dir",
        help="The directory containing test template files for the fuzzing tool",
        type=Path,
    )
    parser.add_argument(
        "target_dir",
        help="The output directory for the generated test suite",
        type=Path,
    )

    args = parser.parse_args()

    TFZ_DIR: Path = args.tfz_dir
    LIB_DIR: Path = TFZ_DIR / "lib"
    TFZ_EXECUTABLE: Path = args.tfz_dir / "bin" / "tfz"
    INPUT_DIR: Path = args.input_dir
    TARGET_DIR: Path = args.target_dir

    if not TFZ_DIR.is_dir():
        print(f"tfz_dir ({TFZ_DIR}) does not exist or is not a directory.")
        parser.print_help()
        sys.exit(1)

    if not LIB_DIR.is_dir():
        print(f"tfz_dir ({TFZ_DIR}) is invalid: cannot find lib/ subdirectory.")
        parser.print_help()
        sys.exit(1)

    if not TFZ_EXECUTABLE.is_file():
        print(f"Cannot find tfz executable at ({TFZ_EXECUTABLE}.")
        print(
            f"Ensure that tfz_dir ({TFZ_DIR} is valid, and make has been run"
            "to build the executable."
        )
        parser.print_help()
        sys.exit(1)

    if not INPUT_DIR.is_dir():
        print(f"template_dir ({INPUT_DIR}) does not exist or is not a directory.")
        parser.print_help()
        sys.exit(1)

    TARGET_DIR.mkdir(exist_ok=True)

    # env vars required by tfz
    os.environ["TF_FUZZ_LIB_DIR"] = str(LIB_DIR.absolute())

    if not os.getenv("TF_FUZZ_BPLATE"):
        os.environ["TF_FUZZ_BPLATE"] = "tfm_boilerplate.txt"

    jinja_env = Environment(
        loader=PackageLoader("tfz-suitegen", package_path="suite_templates"),
        autoescape=False,
    )

    test_suite: TestSuite = TestSuite()

    for i, test_input_path in enumerate(sorted(INPUT_DIR.glob("*.test"))):

        print(f"* Found test file {test_input_path}")

        c_file_name: str = f"{test_input_path.stem}.c"
        generated_test_path: Path = TARGET_DIR / f"{c_file_name}"

        process = sp.run(
            f"{TFZ_EXECUTABLE.absolute()} {test_input_path.absolute()} {generated_test_path.absolute()}",
            shell=True,
            text=True,
            stderr=sp.STDOUT,
            stdout=sp.PIPE,
        )

        if process.returncode != 0:
            print("  tfz invocation failed, skipping test")
            print("  Command output: ")
            for line in process.stdout.splitlines():
                print(f"    {line}")

            continue

        name: str = f"TFM_FUZZ_TEST_{test_input_path.stem.upper().replace(' ','_')}"

        # DESCRIPTION: use the purpose stored in the input test file.
        # This is in the syntax `purpose to <str>;`.
        description: str = ""
        with open(test_input_path) as f:
            _match = re.search(r"^purpose to\s+(.*);", f.read())
            if _match:
                description = _match[1]

        description = description.replace('"', '\\"')

        # FN_DEF / FN_NAME: the test function generated is always called
        # test_thread. This is given a unique name, `test_<i>` when it is
        # added to the suite.

        fn_name: str = f"test_tfz_generated_{i}"

        with open(generated_test_path, "r+") as generated_test_file:

            _contents = generated_test_file.read()
            generated_test_file.seek(0)
            generated_test_file.write(re.sub(r"test_thread", fn_name, _contents))

        test: Test = Test(fn_name, c_file_name, name, description)
        test_suite.tests.append(test)

    for template_name in jinja_env.list_templates():
        template: Template = jinja_env.get_template(template_name)
        with open(TARGET_DIR / template_name, "w") as f:
            f.write(template.render(asdict(test_suite)))


if __name__ == "__main__":
    main()
