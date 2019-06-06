include(${CMAKE_SOURCE_DIR}/cmake/InvokeFormat.cmake)

invoke_format(clang_format)

find_program_required(RUN_CLANG_FORMAT run-clang-format)
