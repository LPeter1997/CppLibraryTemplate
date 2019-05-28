include(${CMAKE_SOURCE_DIR}/cmake/FindProgramRequired.cmake)
include(${CMAKE_SOURCE_DIR}/cmake/PrettyTidy.cmake)

# Find the clang-tidy binary
find_program_required(CLANG_TIDY clang-tidy-8)
# Find the clang-tidy helper script
find_program_required(RUN_CLANG_TIDY run-clang-tidy-8.py)

# Invoke
add_custom_target(clang_tidy
    COMMAND ${RUN_CLANG_TIDY}
        -clang-tidy-binary ${CLANG_TIDY}
        -header-filter=.*
        -quiet
        -export-fixes="${CMAKE_BINARY_DIR}/clang_tidy_diag.yml"
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

# Pretty-print
pretty_tidy(YAML "${CMAKE_BINARY_DIR}/clang_tidy_diag.yml")
