#!/usr/bin/env python

"""
 " formatter.py
 "
 " Copyright (c) 2019 Peter Lenkefi
 " Distributed under the MIT License.
 "
 " A Python script to invoke clang-format depending on the branch.
 " On a dev branch we invoke clang-format-diff.py and compare to master. On the
 " master branch we simply call clang-format to fully format.
"""

import argparse
import glob
import os
import sys

from common import *

# Script version
VER_MAJOR = 0
VER_MINOR = 1
VER_PATCH = 0

__version__ = f'{VER_MAJOR}.{VER_MINOR}.{VER_PATCH}'

def is_included_source(s):
    return s in ['examples', 'single_include', 'src']

def collect_source_files():
    # Get current directory's content
    dircont = os.listdir('.')
    # Filter it
    dircont = (x for x in dirconf if is_included_source(x))
    # Glob each
    # TODO
    for p in dircont:
        print(f'Looking at: {p}')

    return None

def run_full_format(script):
    files = collect_source_files()
    retval = os.system(f'({script} *.cpp *.h *.hpp) > format_out.txt')
    with open('format_out.txt', 'r') as f:
        content = f.read()
        #m = re.match(r'Enabled checks:(\r\n?|\n)(\s+.*(\r\n?|\n))*', content)
        #end = len(m.group())
        #content = content[end :]
        print(content)
    retval = os.WEXITSTATUS(retval)
    sys.exit(retval)

def run_diff_format(script):
    # TODO
    # retval = os.system(f'(git diff -U0 --no-color HEAD^ | {script} -p1) > format_out.txt')
    os.system('')

def run_format_branch(full_format, diff_format):
    matched, projver = is_rel_branch()
    matched2, projver = is_master_branch()
    if matched or matched2:
        # Run full
        print('On master or release branch, running full format!')
        run_full_format(full_format)
    else:
        # Run diff
        print('Not on master or release branch, running differential format!')
        run_diff_format(diff_format)

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
    required_args.add_argument("-b", "--format-bin",
        help="specifies the path to the clang-format binary",
        required=True)
    required_args.add_argument("-d", "--run-diff",
        help="specifies the path to the clang-format-diff.py script",
        required=True)

    args = parser.parse_args()

    # We have all the arguments needed
    run_format_branch(args.format_bin, args.run_diff)

# Start execution in main()
if __name__ == "__main__":
    main()
