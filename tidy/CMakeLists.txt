include(${CMAKE_SOURCE_DIR}/cmake/FindProgramRequired.cmake)

# Find the clang-tidy binary
find_program_required(CLANG_TIDY clang-tidy-8)
# Find the clang-tidy helper script
find_program_required(RUN_CLANG_TIDY run-clang-tidy-8.py)

# Invoke
add_custom_target(clang_tidy
    COMMAND ${RUN_CLANG_TIDY}
        -clang-tidy-binary ${CLANG_TIDY}
        -header-filter=.*
        -config="${CMAKE_CURRENT_SOURCE_DIR}/.clang_tidy"
        --
        -dump-config
        #-quiet
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)
