# Find the clang-tidy binary
find_program(CLANG_TIDY clang-tidy-8)

# Invoke
add_custom_target(clang_tidy
    COMMAND ${CLANG_TIDY}
        -config="clang_tidy_config"
        #-quiet
)
