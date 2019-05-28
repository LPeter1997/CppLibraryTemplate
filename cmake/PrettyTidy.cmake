#[[
 # MergeSingleHeader.cmake
 #
 # Copyright (c) 2019 Peter Lenkefi
 # Distributed under the MIT License.
 #
 # A CMake wrapper for the python clang-tidy pretty-printer.
 #
 # Usage:
 # pretty_tidy(
 #     YAML <yaml output of clang-tidy>
 # )
]]

include(${CMAKE_SOURCE_DIR}/cmake/PrefixedVariable.cmake)

# Create a configuration variable for the tidy script
prefixed_variable(
    PRETTY_TIDY_SCRIPT FILEPATH
    "The path of the python pretty-tidy script."
    "${CMAKE_SOURCE_DIR}/scripts/tidyup.py"
)

function(pretty_tidy)
    cmake_parse_arguments(
        PTD
        ""
        "YAML"
        ""
        ${ARGN}
    )

    # Need python 3.6 for the merge script
    find_package(PythonInterp 3.6 REQUIRED)

    # Check required arguments
    if(NOT DEFINED PTD_YAML)
        message(FATAL_ERROR "Setting YAML is required!")
    endif()

    # Invoke the actual script
    add_custom_command(
        COMMAND "${PYTHON_EXECUTABLE}" ${${PROJECT_NAME}_PRETTY_TIDY_SCRIPT}
            --yaml ${PTD_YAML}
        #DEPENDS "${PTD_YAML}" # We need the file specified as an output...
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    )
endfunction(pretty_tidy)
