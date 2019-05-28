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
import termcolor
import yaml

# Script version
VER_MAJOR = 0
VER_MINOR = 1
VER_PATCH = 0

__version__ = f'{VER_MAJOR}.{VER_MINOR}.{VER_PATCH}'

class LineEntry:
    def __init__(self, offs, cont):
        self.offset = offs
        self.content = cont.strip()
        self.length = len(self.content)
        self.end_offset = self.offset + self.length

    def contains(self, idx):
        return self.offset <= idx < self.end_offset

    def column_of_idx(self, idx):
        if self.contains(idx):
            return idx - self.offset
        return len(self.content)

class FileEntry:
    def __init__(self, cont):
        self.content = cont
        self.lines = []
        temp_lines = self.content.splitlines(True)
        offs = 0
        for l in temp_lines:
            self.lines.append(LineEntry(offs, l))
            offs += len(l)

    def line_idx_of(self, idx):
        lo = 0
        hi = len(self.lines)
        # Just a bsearch
        while lo <= hi:
            mi = (lo + hi) // 2
            ml = self.lines[mi]

            if ml.contains(idx):
                return mi
            elif ml.offset < idx:
                lo = mi + 1
            else:
                hi = mi - 1
        return len(self.lines)

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

def node_initial(nodet, diagname, fpath, line, col):
    fpath = os.path.relpath(fpath)
    posinfo = f'in file "{fpath}", at line {line + 1}, column {col + 1}'
    if nodet == NodeType.OTHER:
        return f'Info ({diagname}) {posinfo}'
    elif nodet == NodeType.ERROR:
        return termcolor.colored(f'Error ({diagname}) {posinfo}', 'red')
    else:
        return termcolor.colored(f'Warning ({diagname}) {posinfo}', 'yellow')

def make_arrow(col_num):
    if col_num < 3:
        # From the right
        return ' ' * col_num + '^' + '_' * 10
    else:
        # From the left
        return '_' * col_num + '^'

def process_yaml_node(node, file_cache):
    diag_name = node['DiagnosticName']
    diag_msg  = node['Message']
    diag_pos  = node['FileOffset']
    diag_file = node['FilePath']
    diag_repl = node['Replacements']

    nodet = NodeType.OTHER
    if 'error' in diag_name:
        nodet = NodeType.ERROR
    elif 'warning' in diag_name:
        nodet = NodeType.WARNING

    file = file_from_cache(diag_file, file_cache)
    line_num = file.line_idx_of(diag_pos)
    line = file.lines[line_num]
    col_num = line.column_of_idx(diag_pos)

    initial = node_initial(nodet, diag_name, diag_file, line_num, col_num)
    print(f'{initial}: {diag_msg}')
    print(line.content)

    # Arrow
    print(make_arrow(col_num))

    # If we can fix it, show it how
    if diag_repl:
        print(f'{termcolor.colored('Note', 'green')}: You can fix it like so:')
        print(termcolor.colored(diag_repl, 'green'))

    # Arrow
    print(make_arrow(col_num))

    return nodet

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
