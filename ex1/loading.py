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

from sys import argv
from os import path
from importlib import import_module
from importlib.metadata import version, PackageNotFoundError

DEPENDENCIES = {
    "pandas": "Data manipulation",
    "numpy": "Numerical computation",
    "matplotlib": "Visualization",
    "requests": "Network access",
}


def check_dependencies():
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
        program_name = argv[0]
        pip_requirements = path.join(
            path.dirname(program_name), "requirements.txt"
        )
        print()
        print("Missing packages should be installed")
        print()
        print("For pip, type:")
        print("-----------------")
        print(f"pip install -r {pip_requirements}")
        # print(f"pip install -r {path.dirname(program_name)}/requirements.txt")
        print(f"python3 {program_name}")

        print()
        print("For Poetry, type:")
        print("-----------------")
        print("poetry install")
        # print("poetry install -P ex1")
        # print("poetry install -C ex1")
        print(f"poetry run python {program_name}")


def main():
    print()
    print("LOADING STATUS: Loading programs...")

    check_dependencies()


if __name__ == "__main__":
    main()
