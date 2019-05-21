
add_executable(clisquare clisquare.cpp)

# Make use of our merged library
target_link_libraries(clisquare PUBLIC lib_header)
