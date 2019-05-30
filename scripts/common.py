"""
 " common.py
 "
 " Copyright (c) 2019 Peter Lenkefi
 " Distributed under the MIT License.
 "
 " Common utilities in the python scripts.
"""

import os
import re

def current_branch():
    branch = os.getenv('TRAVIS_BRANCH')
    if not branch:
        raise Exception('TRAVIS_BRANCH environment variable not defined (are you not releasing on Travis?)')
    return branch

def is_branch(rx_name):
    cb = current_branch()
    rx = os.getenv(rx_name)
    print(f'Current branch: {cb}')
    print(f'Pattern: {rx}')
    m = re.match(rx, cb)
    if m == None:
        return (False, '')
    else:
        ver = None
        try:
            ver = m.group('version')
        except IndexError:
            pass
        return (True, ver)

def is_dev_branch():
    return is_branch('BRANCH_DEVELOPMENT')

def is_rel_branch():
    return is_branch('BRANCH_RELEASE')

def is_master_branch():
    return is_branch('BRANCH_MASTER')
