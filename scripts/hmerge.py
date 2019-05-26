"""
 " hmerge.py
 "
 " Copyright (c) 2019 Peter Lenkefi
 " Distributed under the MIT License.
 "
 " A Python script to merge C++ header files into a single-header release.
 " Type hmerge --help or hmerge -h for options.
"""

import argparse
import datetime
import enum
import glob
import json
import os
import re
import sys

# Script version
VER_MAJOR = 0
VER_MINOR = 1
VER_PATCH = 0

__version__ = f'{VER_MAJOR}.{VER_MINOR}.{VER_PATCH}'

# REGEXES ######################################################################
# Helpers

# Newline
NEWLINE = r'((\r\n)|\r|\n)'
# Line continuation
LINE_CONTINUATION = fr'((\\|\?\?\/)( |\t)*{NEWLINE})'
# Optional continuation
OLC = fr'({LINE_CONTINUATION}*)'
# Inside of a string literal
STRING_LIT_INSIDE = fr'(([^\"\\\r\n]|(\\.)|{OLC})*?)'
# Hashmark character
HASHMARK = r'(#|\?\?=|%:)'
# Hash forrowed by line-continuation
DIRECTIVE = fr'{HASHMARK}( |\t|{LINE_CONTINUATION})*'

# Makes a literal sequence line-continuated
def lit_cont(str):
    res = r''
    for c in str:
        res += fr'({c}{OLC})'
    return fr'({res})'

# Makes a directive beginning
def dir_begginning(str):
    return fr'({DIRECTIVE}{lit_cont(str)})'

INCLUDE_PREFIX = fr'({dir_begginning("include")}( |\t|{OLC})*)'

# Actual tokens

# Single-line comment
SINGLELINE_COMMENT = re.compile(fr'\/{OLC}\/({LINE_CONTINUATION}|.)*')
# Multi-line comment
MULTILINE_COMMENT = re.compile(fr'\/{OLC}\*((.|\s)*?)\*{OLC}\/')
# Raw string literal
RAW_STRING_LIT = re.compile(r'R\"(?P<delim>[^\(\)\\ \f\n\r\t\v]*?)\((.|\s)*?\)(?P=delim)\"')
# String-literal
STRING_LIT = fr'\"(?P<literal>{STRING_LIT_INSIDE})\"'
# User include
USER_INCLUDE = re.compile(fr'{INCLUDE_PREFIX}{STRING_LIT}')
# System include
SYSTEM_INCLUDE = re.compile(fr'{INCLUDE_PREFIX}<(?P<literal>{STRING_LIT_INSIDE})>')

################################################################################

# Removes line-continuations from a string
def de_continuate(str):
    i = 0
    res = ''
    while i < len(str):
        m = re.match(OLC, str[i :])
        l = m.end() - m.start()
        if l == 0:
            res += str[i]
            i += 1
        else:
            i += l
    return res

# Tells if 'base' folder is above 'sub'
# (meaning base contains sub)
def is_base_path_of(base, sub):
    base = os.path.realpath(base)
    sub = os.path.realpath(sub)
    return os.path.commonprefix([base, sub]) == base

# Makes an identifier into a C-macro style identifier (all caps with underscore)
def c_macroify(ident):
    return re.sub(r'[^A-Z0-9]', '_', ident.upper())

# Collapses multiple newlines
def collapse_newlines(str):
    return re.sub(r'\n\n+', '\n\n', str).strip()

# Replaces backslashes with forward-slashes
def to_posix_path(path):
    return re.sub(r'\\', '/', path)

# Makes the include guard matchers for a particular file
def make_guard_matchers(libname, rootfile, fname):
    rootp = os.path.dirname(rootfile)
    relp = os.path.relpath(fname, rootp)
    guard_name = f'{c_macroify(libname)}_{c_macroify(relp)}'
    gnc = lit_cont(guard_name)
    ifnd = re.compile(fr'{dir_begginning("ifndef")}( |\t)+?{gnc}')
    defn = re.compile(fr'{dir_begginning("define")}( |\t)+?{gnc}')
    enif = re.compile(fr'{dir_begginning("endif")}( |\t)*\/{OLC}\*( |\t)*{gnc}( |\t)*\*{OLC}\/')
    return (ifnd, defn, enif)

# A partial C++ lexer looking for include directives
class IncludeLexer:
    def __init__(self, ifnd, defn, enif, source):
        self.ifndef_matcher = ifnd
        self.define_matcher = defn
        self.endif_matcher = enif
        self.source = source
        self.index = 0

    # Lexes the whole source
    def lex(self):
        res = []
        while True:
            t = self.next()
            if t == None:
                return res
            else:
                res.append(t)

    # Returns the next token
    def next(self):
        if self.is_eof():
            return None

        t = self.get_token(SINGLELINE_COMMENT, TokenType.OTHER)
        if t:
            return t
        t = self.get_token(MULTILINE_COMMENT, TokenType.OTHER)
        if t:
            return t
        t = self.get_token(RAW_STRING_LIT, TokenType.OTHER)
        if t:
            return t
        t = self.get_token(STRING_LIT, TokenType.OTHER)
        if t:
            return t
        t = self.get_token(USER_INCLUDE, TokenType.USER_INCLUDE)
        if t:
            return t
        t = self.get_token(SYSTEM_INCLUDE, TokenType.SYSTEM_INCLUDE)
        if t:
            return t
        t = self.get_token(self.ifndef_matcher, TokenType.GUARD_IFNDEF)
        if t:
            return t
        t = self.get_token(self.define_matcher, TokenType.GUARD_DEFINE)
        if t:
            return t
        t = self.get_token(self.endif_matcher, TokenType.GUARD_ENDIF)
        if t:
            return t

        # Something else
        t = Token(self.source[self.index : (self.index + 1)], TokenType.OTHER)
        self.index += 1
        return t

    # Applies a regex at the current position
    # Returns the token if it matched, None otherwise
    def get_token(self, regex, ty):
        m = re.match(regex, self.source[self.index :])
        if m:
            l = m.end() - m.start()
            src = self.source[self.index : (self.index + l)]
            self.index += l
            return Token(src, ty)
        else:
            return None

    def is_eof(self):
        return self.index >= len(self.source)

class TokenType(enum.Enum):
    USER_INCLUDE   = 0
    SYSTEM_INCLUDE = 1
    GUARD_IFNDEF   = 2
    GUARD_DEFINE   = 3
    GUARD_ENDIF    = 4
    OTHER          = 5

# Represents a token (at least the relevant part)
class Token:
    def __init__(self, source, ty):
        self.source = source
        self.type = ty

    # Ask the path if a user include
    def user_include_path(self):
        dec = de_continuate(self.source)
        assert dec[-1] == '"'
        dec = dec[0 : -1]
        fst = dec.index('"')
        return dec[(fst + 1) : ]


# Shortcut for lex-all
def lex_source(libname, rootfile, fname):
    ifnd, defn, enif = make_guard_matchers(libname, rootfile, fname)
    with open(fname, 'r') as f:
        return IncludeLexer(ifnd, defn, enif, f.read()).lex()

# Creates a filter function that tells if a certain file needs to be excluded
def make_exclude_filter(excludes):
    excluded_files = set()
    excluded_paths = set()

    for ex in excludes:
        ex = os.path.realpath(ex)
        if os.path.isfile(ex):
            excluded_files.add(ex)
        elif os.path.isdir(ex):
            excluded_paths.add(ex)
        else:
            print(f'warning: exclude {ex} is neither a file nor a directory')

    return lambda fpath: ((os.path.realpath(fpath) in excluded_files)
              or (any(is_base_path_of(base, fpath) for base in excluded_paths)))

def process_file(libname, rootfile, fname, processed, is_excluded):
    # Sanitize input
    fname = os.path.realpath(fname)
    # Check if processed
    if fname in processed:
        return ''
    # Check if exists and file
    if not os.path.isfile(fname):
        raise Exception(f'"{fname}" is not a file or does not exist')
    # Check if excluded
    if is_excluded(fname):
        return ''
    # Register as processed
    processed.add(fname)
    # Tokenize source
    toks = lex_source(libname, rootfile, fname)
    # Find ifnded
    ifnd_i = next(i for i, v in enumerate(toks) if v.type == TokenType.GUARD_IFNDEF)
    toks = toks[(ifnd_i + 1) : ]
    # Find define
    defn_i = next(i for i, v in enumerate(toks) if v.type == TokenType.GUARD_DEFINE)
    toks = toks[(defn_i + 1) : ]
    # Find endif
    enif_i = next(i for i, v in enumerate(toks) if v.type == TokenType.GUARD_ENDIF)
    toks = toks[ : enif_i]
    # Keep the relevant part
    result = ''
    # Helper info
    current_root = os.path.dirname(fname)
    absroot = os.path.dirname(rootfile)
    for t in toks:
        if t.type == TokenType.USER_INCLUDE:
            incf = os.path.realpath(os.path.join(current_root, t.user_include_path()))
            if is_excluded(incf):
                inrel = to_posix_path(os.path.relpath(incf, absroot))
                result += f'#include "{inrel}"\n'
            else:
                result += process_file(libname, rootfile, incf, processed, is_excluded)
                result += '\n'
        else:
            result += t.source
    return result

def wrap_in_guars(libname, c):
    ln = c_macroify(libname)
    return f'#ifndef {ln}\n#define {ln}\n\n{c}\n\n#endif /* {ln} */\n'

def main():
    # Setting up command-line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version",
        action="version",
        version=f'%(prog)s {__version__}')

    # Optional arguments
    parser.add_argument("-p", "--prefix",
        help="specifies a file to use as a prefix for the merged header")
    parser.add_argument("-t", "--target",
        help="specifies the destination file where the merge happens",
        default="merged_header.hpp")
    parser.add_argument("-e", "--exclude",
        help="specifies paths and files to exclude when merging",
        action='append',
        default=[])

    # Required arguments
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument("-n", "--libname",
        help="specifies the name to use as include guard prefix",
        required=True)
    required_args.add_argument("-r", "--root",
        help="specifies the root header file where everything is included",
        required=True)

    args = parser.parse_args()

    # We have all the arguments needed, now we pre-process them
    libname = args.libname
    excluded = make_exclude_filter(args.exclude)
    rootf = args.root

    # Merge
    content = process_file(libname, rootf, rootf, set(), excluded)

    # Add guards
    content = wrap_in_guars(libname, content)

    # Add prefix if needed
    if args.prefix:
        with open(args.prefix, 'r') as f:
            prefx = f.read()
            content = prefx + '\n\n' + content

    # Collapse the newlines
    content = collapse_newlines(content)

    targ = os.path.realpath(args.target)

    # Check if file already exists
    if os.path.isfile(targ):
        with open(targ, 'r') as f:
            old_content = f.read()
            # If equals, exit
            if old_content == content:
                print(f'file "{to_posix_path(targ)}" already up to date')
                return

    # Write it to destination file
    with open(targ, 'w') as f:
        f.write(content)

    # Friendly message
    print(f'file successfully merged into "{to_posix_path(targ)}"')

# Start execution in main()
if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f'An error occured during merge:\n{err}')
        sys.exit(1)
