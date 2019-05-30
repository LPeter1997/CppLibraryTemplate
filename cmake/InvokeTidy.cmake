#[[
 # InvokeTidy.cmake
 #
 # Copyright (c) 2019 Peter Lenkefi
 # Distributed under the MIT License.
 #
 # A CMake wrapper for the python tidyup script.
 #
 # Usage:
 # invoke_tidy(<target>)
]]

include(${CMAKE_SOURCE_DIR}/cmake/FindProgramRequired.cmake)
include(${CMAKE_SOURCE_DIR}/cmake/PrefixedVariable.cmake)

# Create a configuration variable for the script
prefixed_variable(
    TIDY_SCRIPT FILEPATH
    "The path of the python tidy script."
    "${CMAKE_SOURCE_DIR}/scripts/tidyup.py"
)

# TODO: Maybe have a version setter for the Clang tools?

function(invoke_tidy target)
    # Need python 3.6 for the merge script
    find_package(PythonInterp 3.6 REQUIRED)

    # Find the clang-tidy binary
    find_program_required(CLANG_TIDY clang-tidy-8)
    # Find the clang-tidy helper script
    find_program_required(RUN_CLANG_TIDY run-clang-tidy-8.py)
    # Find the clang-tidy-diff script
    find_program_required(CLANG_TIDY_DIFF clang-tidy-diff-8.py)

    set(TIDY_ENV_VARS
        BRANCH_MASTER="${BRANCH_MASTER}"
        BRANCH_RELEASE="${BRANCH_RELEASE}"
        BRANCH_DEVELOPMENT="${BRANCH_DEVELOPMENT}"
    )

    # Invoke the actual script
    add_custom_command(
        COMMAND ${CMAKE_COMMAND} -E env ${TIDY_ENV_VARS}
            "${PYTHON_EXECUTABLE}" ${${PROJECT_NAME}_TIDY_SCRIPT}
                --tidy-bin "${CLANG_TIDY}"
                --run-tidy "${RUN_CLANG_TIDY}"
                --run-diff "${CLANG_TIDY_DIFF}"
        OUTPUT ".nonesuch__" # Just so we always run
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )
    add_custom_target(${target} ALL DEPENDS ".nonesuch__")
endfunction(invoke_tidy)
