# Test executable
add_executable(unit_tests
    main.cpp
    # Actual test source files
    sample_library/square.cpp
)

# TESTING
MESSAGE(STATUS "The C++ flags: " ${CMAKE_CXX_FLAGS})

# Make use of our merged library
target_link_libraries(unit_tests PUBLIC lib_header)

# Catch2
find_package(Catch2 REQUIRED)

include(CTest)
include(Catch)

target_link_libraries(unit_tests PUBLIC Catch2::Catch2)
catch_discover_tests(unit_tests)
