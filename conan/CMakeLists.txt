
# Source and target
set(CONANFILE_IN  ${CMAKE_CURRENT_SOURCE_DIR}/conanfile.in)
set(CONANFILE_OUT ${CMAKE_CURRENT_SOURCE_DIR}/conanfile.py)

# Create the tag list
set(PROJECT_TAGS_STR_LIST "")
set(delim "")
foreach(elem ${PROJECT_TAGS})
    set(PROJECT_TAGS_STR_LIST "${PROJECT_TAGS_STR_LIST}${delim}\"${elem}\"")
    set(delim ", ")
endforeach()

# Configure conanfile.py
configure_file(
    ${CONANFILE_IN}
    ${CONANFILE_OUT}
    @ONLY
)

add_custom_target(conanfile ALL
    SOURCES "${CONANFILE_OUT}"
)

set(CONAN_ENV_VARS
    CONAN_PACKAGE_NAME="${PROJECT_NAME}"
    CONAN_USERNAME="${CONAN_USERNAME}"
    CONAN_LOGIN_USERNAME="${CONAN_USERNAME}"
    CONAN_UPLOAD="${CONAN_UPLOAD}"
    CONAN_HEADER_ONLY="${CONAN_HEADER_ONLY}"
    CONAN_UPLOAD_ONLY_WHEN_STABLE="False"
    CONAN_CONANFILE="conanfile.py"
    CONAN_TEST_FOLDER="test_package"
)

add_custom_target(conan_user ALL
    COMMAND ${CMAKE_COMMAND} -E env ${CONAN_ENV_VARS} conan user
    DEPENDS "${CONANFILE_OUT}"
)

add_custom_target(conan_build ALL
    COMMAND ${CMAKE_COMMAND} -E env ${CONAN_ENV_VARS} python "conan/build.py"
)
