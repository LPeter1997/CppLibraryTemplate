import os

from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    login_uname = os.getenv('CONAN_LOGIN_USERNAME')
    uname       = os.getenv('CONAN_USERNAME')
    package_ver = os.getenv('CONAN_PACKAGE_VERSION', os.getenv('TRAVIS_BRANCH'))
    package_ver = package_ver.replace('release/', '')
    package_nam = os.getenv('CONAN_PACKAGE_NAME')
    reference   = f'{package_nam}/{package_ver}'
    channel     = os.getenv('CONAN_CHANNEL', 'dev')
    upload      = os.getenv('CONAN_UPLOAD')
    branch_pat  = os.getenv('CONAN_STABLE_BRANCH_PATTERN', r'release/\d+\.\d+\.\d+.*')
    test_folder = os.getenv('CONAN_TEST_FOLDER', os.path.join('conan', 'test_package'))
    only_stable = os.getenv('CONAN_UPLOAD_ONLY_WHEN_STABLE', True)
    header_only = os.getenv('CONAN_HEADER_ONLY', False)
    pure_c      = os.getenv('CONAN_PURE_C', False)

    builder = ConanMultiPackager(
        username                = uname,
        login_username          = login_uname,
        reference               = reference,
        channel                 = channel,
        upload                  = upload,
        stable_branch_pattern   = branch_pat,
        upload_only_when_stable = only_stable,
        test_folder             = test_folder
    )

    if header_only == "False":
        builder.add_common_builds(pure_c=pure_c)
    else:
        builder.add()

    builder.run()
