import os
import re

from cpt.packager import ConanMultiPackager

# Our own common utilities
importlib.import_module('../scripts/common.py')

if __name__ == "__main__":
    projname = os.getenv('CONAN_PACKAGE_NAME')
    if not projname:
        raise Exception('CONAN_PACKAGE_NAME environment variable not defined')
    username = os.getenv('CONAN_USERNAME')
    if not username:
        raise Exception('CONAN_USERNAME environment variable not defined')
    branch = os.getenv('TRAVIS_BRANCH')
    if not branch:
        raise Exception('TRAVIS_BRANCH environment variable not defined (are you not releasing on Travis?)')

    matched, projver = is_dev_branch()
    channel = 'nightly'
    if not matched:
        matched, projver = is_rel_branch()
        channel = 'stable'

    if matched:
        reference = f'{projname}/{projver}@{username}/{channel}'

        builder = ConanMultiPackager(reference=reference)

        builder.add({}, {}, {}, {})
        builder.run()
    else:
        print('Not release or development branch, ignoring release!')
