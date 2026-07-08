#!/usr/bin/env python3

# try:
#     import sys
#     import importlib
#     import pandas
#     import numpy
#     import matplotlib
# except ImportError as e:
#     help(sys.exit)
#     sys.exit(f"Got an import error: {e}")

from sys import argv, exit
from importlib import import_module
from importlib.metadata import version, PackageNotFoundError

DEPENDENCIES = {
    "pandas": "Data manipulation",
    "numpy": "Numerical computation",
    "matplotlib": "Visualization",
    "requests": "Network access",
}


def check_dependencies() -> None:
    print()
    print("Checking dependencies:")
    has_missing = False
    for package, description in DEPENDENCIES.items():
        try:
            import_module(package)
            ver = version(package)
            print(f"[OK] {package} ({ver}) - {description} ready")
        except ImportError:
            has_missing = True
            print(f"[MISSING] {package} - {description}")

    if has_missing:
        error_message = "\n".join(
            [
                "",
                "Missing packages should be installed",
                "",
                "For pip, type:",
                "-----------------",
                "pip install -r ./requirements.txt",
                f"python3 {argv[0]}",
                "",
                "For Poetry, type:",
                "-----------------",
                "poetry install",
                # "poetry install -P ex1",
                # "poetry install -C ex1",
                f"poetry run python {argv[0]}",
            ]
        )
        exit(error_message)


def main():
    print()
    print("LOADING STATUS: Loading programs...")

    check_dependencies()


if __name__ == "__main__":
    main()
