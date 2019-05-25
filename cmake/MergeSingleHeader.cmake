#[[
 # MergeSingleHeader.cmake
 #
 # Copyright (c) 2019 Peter Lenkefi
 # Distributed under the MIT License.
 #
 # A CMake wrapper for the python merge script.
 #
 # Usage:
 # merge_single_header(<target>
 #     [NOFOLDER]               # You don't want folder/header.hpp
 #     LIBNAME <library name>
 #     ROOT <root header file>
 #     PREFIX <prefix file>
 #     OUTPUT <output file>
 #     EXCLUDE <files and paths>
 # )
]]

include(${CMAKE_SOURCE_DIR}/cmake/PrefixedVariable.cmake)

# Create a configuration variable for the merge script
prefixed_variable(
    MERGE_SCRIPT FILEPATH
    "The path of the python merge script."
    "${CMAKE_SOURCE_DIR}/scripts/hmerge.py"
)

# Create a target that does the merge
function(merge_single_header target)
    cmake_parse_arguments(
        MSH
        "NOFOLDER"
        "LIBNAME;ROOT;PREFIX;OUTPUT"
        "EXCLUDE"
        ${ARGN}
    )

    # Need python 3.6 for the merge script
    find_package(PythonInterp 3.6 REQUIRED)

    # Check required arguments
    if(NOT DEFINED MSH_LIBNAME)
        message(FATAL_ERROR "Setting LIBNAME is required!")
    endif()
    if(NOT DEFINED MSH_ROOT)
        message(FATAL_ERROR "Setting ROOT is required!")
    endif()

    # Build the exclusion list
    set(EXCLUDE_LIST "")
    if(DEFINED MSH_EXCLUDE)
        foreach(ex ${MSH_EXCLUDE})
            set(EXCLUDE_LIST "${EXCLUDE_LIST};--exclude;${ex}")
        endforeach()
    endif()

    # Optional output file
    set(OUTPUT_FILE "merged_header.hpp")
    if(DEFINED MSH_OUTPUT)
        set(OUTPUT_FILE "${MSH_OUTPUT}")
    endif()

    # Set the prefix if any
    set(PREFIX_COMMAND "")
    if(DEFINED MSH_PREFIX)
        # Prefix variables
        string(TIMESTAMP MERGE_TIMESTAMP)
        get_filename_component(OUTPUT_FILE_NAME "${OUTPUT_FILE}" NAME)

        # Configure the prefix
        get_filename_component(PREFIX_FILE_NAME "${MSH_PREFIX}" NAME)
        configure_file(
            "${MSH_PREFIX}"
            "${CMAKE_BINARY_DIR}/${PREFIX_FILE_NAME}.prefx"
            @ONLY
        )

        # Set the command
        set(PREFIX_COMMAND "--prefix;${CMAKE_BINARY_DIR}/${PREFIX_FILE_NAME}.prefx")
    endif()

    # Set output file absolute
    set(OUTPUT_FILE "${CMAKE_SOURCE_DIR}/${OUTPUT_FILE}")

    # Invoke the actual script
    add_custom_command(
        COMMAND "${PYTHON_EXECUTABLE}" ${${PROJECT_NAME}_MERGE_SCRIPT}
            --libname ${MSH_LIBNAME}
            --root ${MSH_ROOT}
            --target ${OUTPUT_FILE}
            ${PREFIX_COMMAND}
            ${EXCLUDE_LIST}
        OUTPUT "${OUTPUT_FILE}"
               "${OUTPUT_FILE}__" # Just so we always run
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    )
    add_library(${target} INTERFACE)
    get_filename_component(INCL_DIR "${OUTPUT_FILE}" DIRECTORY)

    # If we want to wrap, modify include directory
    if(NOT ${MSH_NOFOLDER})
        set(INCL_DIR "${INCL_DIR}/../")
    endif()

    target_include_directories(${target}
        INTERFACE "${INCL_DIR}"
    )
    # target_sources(${target} INTERFACE "${CMAKE_SOURCE_DIR}/${OUTPUT_FILE}")
    add_custom_target(gen_header ALL DEPENDS "${OUTPUT_FILE}")
    add_dependencies(${target} gen_header)
endfunction(merge_single_header)
