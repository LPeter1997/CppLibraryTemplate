import os
import re

from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    # Release (stable) branch pattern
    re_stable = r'^rel/\d+\.\d+\.\d+$'
    # Development (nightly release) branch pattern
    re_devel  = r'^dev/\d+\.\d+\.\d+$'

    projname = os.getenv('CONAN_PACKAGE_NAME')
    if not projname:
        raise Exception('CONAN_PACKAGE_NAME environment variable not defined')
    username = os.getenv('CONAN_USERNAME')
    if not username:
        raise Exception('CONAN_USERNAME environment variable not defined')
    branch = os.getenv('TRAVIS_BRANCH')
    if not branch:
        raise Exception('TRAVIS_BRANCH environment variable not defined (are you not releasing on Travis?)')

    channel = None
    projver = None

    if re.match(re_stable, branch):
        channel = 'stable'
        projver = branch.replace('rel/', '')
    elif re.match(re_devel, branch):
        channel = 'nightly'
        projver = branch.replace('dev/', '')

    if channel and projver:
        reference = f'{projname}/{projver}@{username}/{channel}'

        builder = ConanMultiPackager(reference=reference)

        builder.add({}, {}, {}, {})
        builder.run()
    else:
        print('Not release or development branch, ignoring release!')
