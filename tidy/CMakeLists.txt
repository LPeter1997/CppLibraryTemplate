include(${CMAKE_SOURCE_DIR}/cmake/FindProgramRequired.cmake)

# Find the clang-tidy binary
find_program_required(CLANG_TIDY clang-tidy-8)
# Find the clang-tidy helper script
find_program_required(RUN_CLANG_TIDY run-clang-tidy-8.py)

# Read the config file
file(READ "${CMAKE_CURRENT_SOURCE_DIR}/.clang-tidy" TIDY_CONFIG)
# Remove newlines
string(REPLACE "\n" " " TIDY_CONFIG "${TIDY_CONFIG}")
string(REPLACE "\r" " " TIDY_CONFIG "${TIDY_CONFIG}")

# Invoke
add_custom_target(clang_tidy
    COMMAND ${RUN_CLANG_TIDY}
        -clang-tidy-binary ${CLANG_TIDY}
        -header-filter=.*
        -config="{${TIDY_CONFIG}}"
        #-quiet
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)
