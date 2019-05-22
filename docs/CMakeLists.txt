
find_package(Doxygen 1.8)
if(NOT DOXYGEN_FOUND)
    return()
endif()

# Where to get the doxyfile template and where to put the configured one
set(DOXY_CONFIG_IN ${CMAKE_CURRENT_SOURCE_DIR}/doxy.in)
set(DOXY_CONFIG_OUT ${CMAKE_CURRENT_BINARY_DIR}/doxy.cfg)

# Set the configuration variables
set(DOXYGEN_SRC_DIR ${CMAKE_SOURCE_DIR}/src)
set(DOXYGEN_OUT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/gen)

# Configure the doxyfile
configure_file(
    ${DOXY_CONFIG_IN}
    ${DOXY_CONFIG_OUT}
    @ONLY
)

# Actually do generation
add_custom_target(docs ALL
    COMMAND ${DOXYGEN_EXECUTABLE} ${DOXY_CONFIG_OUT}
    SOURCES ${DOXY_CONFIG_IN}
)
