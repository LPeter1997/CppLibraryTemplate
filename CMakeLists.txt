cmake_minimum_required(VERSION 3.12 FATAL_ERROR)

# Project metadata
project(
    SampleProject
    VERSION      0.0.1
    DESCRIPTION  "A sample header-only C++ library template"
    HOMEPAGE_URL "https://github.com/LPeter1997/CppLibraryTemplate"
    LANGUAGES    CXX
)
set(PROJECT_LOGO   "${CMAKE_SOURCE_DIR}/logo.svg")
set(PROJECT_AUTHOR "Peter Lenkefi")
set(PROJECT_EMAIL  "lenkefi.peti@gmail.com")
set(PROJECT_TAGS   "conan" "sample" "header-only" "template")

# Conan metadata
set(CONAN_USERNAME "LPeter1997")
set(CONAN_UPLOAD   "https://api.bintray.com/conan/lpeter1997/SampleRepo")

# Branching rules
set(ENV{BRANCH_RELEASE}     "^rel/(?P<version>\\d+\\.\\d+\\.\\d+)$")
set(ENV{BRANCH_DEVELOPMENT} "^dev/(?P<version>\\d+\\.\\d+\\.\\d+)$")

# C++ configuration
set(CMAKE_CXX_STANDARD            17)
set(CMAKE_CXX_STANDARD_REQUIRED   ON)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Cache variables
include(${CMAKE_SOURCE_DIR}/cmake/PrefixedVariable.cmake)
prefixed_option(GENERATE_DOCS  "Generate documentation from source"               OFF)
prefixed_option(BUILD_EXAMPLES "Build the example programs"                       OFF)
prefixed_option(BUILD_TESTS    "Build tests that are usable with ctest"           OFF)
prefixed_option(COVERAGE       "Configure build for coverage"                     OFF)
prefixed_option(DEPLOY_CONAN   "Deploy to conan (makes everything else disabled)" OFF)
prefixed_option(TIDY_CHECK     "Check the code with clang-tidy"                   OFF)

# Default to Debug
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

if (${${PROJECT_NAME}_COVERAGE})
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -g --coverage")
    # Extra safety
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-inline -fno-inline-small-functions -fno-default-inline")
endif()

# Merge our library
include(${CMAKE_SOURCE_DIR}/cmake/MergeSingleHeader.cmake)
merge_single_header(lib_header
    LIBNAME "sample library"
    ROOT    "src/sample_library/sample_library.hpp"
    PREFIX  "single_include/prefix.in"
    OUTPUT  "single_include/sample_library/sample_lib.hpp"
)

if (${${PROJECT_NAME}_BUILD_TESTS})
    # Only pull dependencies if we build the tests
    if(CONAN_EXPORTED)
        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup()
    else()
        include(${CMAKE_SOURCE_DIR}/cmake/Conan.cmake)
        conan_cmake_run(
            CONANFILE "deps/conanfile.txt"
            BASIC_SETUP
        )
    endif()

    # Tests
    enable_testing()
    add_subdirectory(tests)
endif()

if (${${PROJECT_NAME}_BUILD_EXAMPLES})
    # Examples
    add_subdirectory(examples)
endif()

if (${${PROJECT_NAME}_GENERATE_DOCS})
    # Docs
    add_subdirectory(docs)
endif()

if (${${PROJECT_NAME}_DEPLOY_CONAN})
    # Conan
    add_subdirectory(conan)
endif()

if (${${PROJECT_NAME}_TIDY_CHECK})
    # Tidy
    add_subdirectory(tidy)
endif()
