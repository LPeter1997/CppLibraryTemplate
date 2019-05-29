#!/usr/bin/env python

"""
 " tidyup.py
 "
 " Copyright (c) 2019 Peter Lenkefi
 " Distributed under the MIT License.
 "
 " A Python script to invoke clang-tidy depending on the branch.
 " On a dev branch we invoke clang-tidy-diff.py and compare to master. On the
 " master branch we simply call run-clang-tidy.py to get a full static-analysis.
"""

import argparse
import datetime
import enum
import glob
import importlib
import json
import os
import re
import sys

# Our own common utilities
importlib.import_module('common.py')

# Script version
VER_MAJOR = 0
VER_MINOR = 1
VER_PATCH = 0

__version__ = f'{VER_MAJOR}.{VER_MINOR}.{VER_PATCH}'

def main():
    # Setting up command-line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version",
        action="version",
        version=f'%(prog)s {__version__}')

    # Optional arguments
    #parser.add_argument("-t", "--target",
    #    help="specifies the destination file where the merge happens",
    #    default="merged_header.hpp")
    #parser.add_argument("-e", "--exclude",
    #    help="specifies paths and files to exclude when merging",
    #    action='append',
    #    default=[])

    # Required arguments
    required_args = parser.add_argument_group('required arguments')
    #required_args.add_argument("-n", "--libname",
    #    help="specifies the name to use as include guard prefix",
    #    required=True)

    args = parser.parse_args()

    # We have all the arguments needed
    # TODO

# Start execution in main()
if __name__ == "__main__":
    main()
