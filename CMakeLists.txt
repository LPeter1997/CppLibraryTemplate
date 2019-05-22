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
set(PROJECT_TAGS   "sample" "header-only" "template")

# C++ configuration
set(CMAKE_CXX_STANDARD            17)
set(CMAKE_CXX_STANDARD_REQUIRED   ON)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Dependencies with conan
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

# Merge our library
include(${CMAKE_SOURCE_DIR}/cmake/MergeSingleHeader.cmake)
merge_single_header(lib_header
    LIBNAME "sample library"
    ROOT    "src/sample_library/sample_library.hpp"
    PREFIX  "single_include/prefix.in"
    OUTPUT  "single_include/sample_library/sample_lib.hpp"
)

# Tests
enable_testing()
add_subdirectory(tests)

# Examples
add_subdirectory(examples)

# Docs
add_subdirectory(docs)

# Conan
add_subdirectory(conan)
