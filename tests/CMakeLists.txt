include(CTest)
include(${CMAKE_SOURCE_DIR}/deps/catch2/Catch.cmake)

add_executable(unit_tests
    main.cpp
    # Actual test source files
    sample_library/square.cpp
)

# Make use of our merged library
target_link_libraries(unit_tests PUBLIC lib_header)

# Catch2
target_include_directories(unit_tests PRIVATE ${CMAKE_SOURCE_DIR}/deps)
catch_discover_tests(unit_tests)
