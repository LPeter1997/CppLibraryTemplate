cmake_minimum_required(VERSION 3.6 FATAL_ERROR)

project(SampleProject VERSION 0.0.1)
set(PROJECT_BRIEF "A sample header-only C++ library template")
set(PROJECT_LOGO "${CMAKE_SOURCE_DIR}/logo.svg")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(${CMAKE_SOURCE_DIR}/cmake/MergeSingleHeader.cmake)

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
merge_single_header(lib_header
    LIBNAME "sample library"
    ROOT "src/sample_library/sample_library.hpp"
    PREFIX "single_include/prefix.hpp"
    OUTPUT "single_include/sample_library/sample_lib.hpp"
)

# Tests
enable_testing()
add_subdirectory(tests)

# Docs
find_package(Doxygen 1.8)
if(DOXYGEN_FOUND)
    add_subdirectory(docs)
endif()
