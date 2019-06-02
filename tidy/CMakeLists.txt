include(${CMAKE_SOURCE_DIR}/cmake/InvokeTidy.cmake)

invoke_tidy(clang_tidy)

# TESTING
# Find the clang-format binary
find_program_required(CLANG_FORMAT clang-format)
# Find the clang-format helper script
#find_program_required(RUN_CLANG_FORMAT run-clang-format.py)
# Find the clang-format-diff script
get_filename_component(CLANG_FORMAT_DIR "${CLANG_FORMAT}" DIRECTORY)
message("Directory: ${CLANG_FORMAT_DIR}")
file(GLOB DIR_CONT RELATIVE "${CLANG_FORMAT_DIR}" "{CLANG_FORMAT_DIR}/*.*")
message("Directory content: ${DIR_CONT}")
