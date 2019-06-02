include(${CMAKE_SOURCE_DIR}/cmake/InvokeTidy.cmake)

invoke_tidy(clang_tidy)

# TESTING
# Find the clang-format binary
find_program_required(CLANG_FORMAT clang-format)
# Find the clang-format helper script
#find_program_required(RUN_CLANG_FORMAT run-clang-format.py)
# Find the clang-format-diff script
message("CLANG FORMAT: ${CLANG_FORMAT}")
find_file(CLANG_FORMAT_DIFF clang-format-diff.py)
message("CLANG FORMAT DIFF: ${CLANG_FORMAT_DIFF}")
