cmake_minimum_required(VERSION 3.12 FATAL_ERROR)

# Project metadata
project(SampleProject
    VERSION      0.0.1
    DESCRIPTION  "A sample header-only C++ library template"
    HOMEPAGE_URL "https://github.com/LPeter1997/CppLibraryTemplate"
)
set(PROJECT_LOGO   "${CMAKE_SOURCE_DIR}/logo.svg")
set(PROJECT_AUTHOR "Peter Lenkefi")
set(PROJECT_EMAIL  "lenkefi.peti@gmail.com")
set(PROJECT_TAGS   "conan" "sample" "header-only" "template")

# C++ configuration
set(CMAKE_CXX_STANDARD            17)
set(CMAKE_CXX_STANDARD_REQUIRED   ON)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Cache variables
option(${PROJECT_NAME}_GENERATE_DOCS  "Generate documentation from source"               OFF)
option(${PROJECT_NAME}_BUILD_EXAMPLES "Build the example programs"                       OFF)
option(${PROJECT_NAME}_BUILD_TESTS    "Build tests that are usable with ctest"           OFF)
option(${PROJECT_NAME}_COVERAGE       "Configure build for coverage"                     OFF)
option(${PROJECT_NAME}_DEPLOY_CONAN   "Deploy to conan (makes everything else disabled)" OFF)

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
