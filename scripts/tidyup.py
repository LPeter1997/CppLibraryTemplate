#!/usr/bin/env python

"""
 " tidyup.py
 "
 " Copyright (c) 2019 Peter Lenkefi
 " Distributed under the MIT License.
 "
 " A simple CLI tool that prints out a YAML file produced by clang-tidy. Mainly
 " to beautify outputs and simplify checks on CI.
"""

import argparse
import enum
import os
import sys
import yaml

# Script version
VER_MAJOR = 0
VER_MINOR = 1
VER_PATCH = 0

__version__ = f'{VER_MAJOR}.{VER_MINOR}.{VER_PATCH}'

class FileEntry:
    def __init__(self, cont):
        self.content = cont
        self.lines = self.content.splitlines(True)

    def line_of(self, idx):
        # TODO: We could do bsearch instead with an accumulated length list
        n = 0
        lid = 0
        for l in self.lines:
            if n + len(l) > idx:
                return lid
            n += len(l)
            lid += 1
        return len(self.lines)

    def get_line(self, idx):
        return self.lines[idx].strip()

def file_from_cache(fname, file_cache):
    fname = os.path.realpath(fname)
    if fname in file_cache:
        return file_cache[fname]
    else:
        with open(fname, 'r') as f:
            content = f.read()
            fe = FileEntry(content)
            file_cache[fname] = fe
            return fe

class NodeType(enum.Enum):
    WARNING = 0
    ERROR   = 1
    OTHER   = 2

def process_yaml_node(node, file_cache):
    diag_name = node['DiagnosticName']
    diag_msg  = node['Message']
    diag_pos  = node['FileOffset']
    diag_file = node['FilePath']
    diag_repl = node['Replacements']

    file = file_from_cache(diag_file, file_cache)
    line_num = file.line_of(diag_pos)
    print(file.get_line(line_num))

    return NodeType.OTHER
    # TODO: Do things with it

def process_yaml(fname, werr):
    warn_cnt = 0
    err_cnt = 0
    file_cache = {}

    content = file_from_cache(fname, file_cache).content
    root = yaml.safe_load(content)

    if 'Diagnostics' in root:
        for node in root['Diagnostics']:
            res = process_yaml_node(node, file_cache)
            if res == NodeType.WARNING:
                warn_cnt += 1
            elif res == NodeType.ERROR:
                err_cnt += 1

    if err_cnt > 0 or (warn_cnt > 0 and werr):
        return 1
    else:
        return 0

def main():
    # Setting up command-line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version",
        action="version",
        version=f'%(prog)s {__version__}')

    # Optional arguments
    parser.add_argument("-e", "--werror",
        help="treat warnings as errors",
        default=False)

    # Required arguments
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument("-y", "--yaml",
        help="specifies the YAML file that contains the diagnostic messages",
        required=True)

    args = parser.parse_args()

    ex_code = process_yaml(args.yaml, args.werror)
    sys.exit(ex_code)

if __name__ == "__main__":
    main()
