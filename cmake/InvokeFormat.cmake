#[[
 # InvokeFormat.cmake
 #
 # Copyright (c) 2019 Peter Lenkefi
 # Distributed under the MIT License.
 #
 # A CMake wrapper for the python formatter script.
 #
 # Usage:
 # invoke_tidy(<target>)
]]

include(${CMAKE_SOURCE_DIR}/cmake/FindProgramRequired.cmake)
include(${CMAKE_SOURCE_DIR}/cmake/PrefixedVariable.cmake)

# Create a configuration variable for the script
prefixed_variable(
    FORMAT_SCRIPT FILEPATH
    "The path of the python format script."
    "${CMAKE_SOURCE_DIR}/scripts/formatter.py"
)

# TODO: Maybe have a version setter for the Clang tools?

function(invoke_format target)
    # Need python 3.6 for the merge script
    find_package(PythonInterp 3.6 REQUIRED)

    # Find the clang-tidy binary
    find_program_required(CLANG_FORMAT clang-format)
    # Find the clang-tidy helper script
    find_program_required(CLANG_FORMAT_DIFF clang-format-diff-8)

    set(FORMAT_ENV_VARS
        BRANCH_MASTER=${BRANCH_MASTER}
        BRANCH_RELEASE=${BRANCH_RELEASE}
        BRANCH_DEVELOPMENT=${BRANCH_DEVELOPMENT}
    )

    # Invoke the actual script
    add_custom_command(
        COMMAND ${CMAKE_COMMAND} -E env ${FORMAT_ENV_VARS}
            "${PYTHON_EXECUTABLE}" ${${PROJECT_NAME}_FORMAT_SCRIPT}
                --format-bin "${CLANG_FORMAT}"
                --run-diff "${CLANG_FORMAT_DIFF}"
        OUTPUT ".nonesuch__" # Just so we always run
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        VERBATIM
    )
    add_custom_target(${target} ALL DEPENDS ".nonesuch__")
endfunction(invoke_format)
