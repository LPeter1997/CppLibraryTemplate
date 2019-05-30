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

from common import *

# Script version
VER_MAJOR = 0
VER_MINOR = 1
VER_PATCH = 0

__version__ = f'{VER_MAJOR}.{VER_MINOR}.{VER_PATCH}'

def run_tidy(script):
    pass

def run_tidy_branch(tidy_bin, diff_tidy, full_tidy):
    matched, projver = is_rel_branch()
    matched2, projver = is_master_branch()
    if (not matched) and (not matched2):
        # Run diff
        print('Not on master or release branch, running differential tidy-check!')
        run_tidy(diff_tidy)
    else:
        # Run full
        print('On master or release branch, running full tidy-check!')
        run_tidy(full_tidy)

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
    required_args.add_argument("-b", "--tidy-bin",
        help="specifies the path to the clang-tidy binary",
        required=True)
    required_args.add_argument("-r", "--run-tidy",
        help="specifies the path to the run-clang-tidy.py script",
        required=True)
    required_args.add_argument("-d", "--run-diff",
        help="specifies the path to the clang-tidy-diff.py script",
        required=True)

    args = parser.parse_args()

    # We have all the arguments needed
    run_tidy_branch(args.tidy_bin, args.run_tidy, args.run_diff)

# Start execution in main()
if __name__ == "__main__":
    main()
