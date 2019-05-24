
# Source and target
set(CONANFILE_IN  ${CMAKE_CURRENT_SOURCE_DIR}/conanfile.in)
set(CONANFILE_OUT ${CMAKE_CURRENT_SOURCE_DIR}/conanfile.py)

# Create the tag list
set(PROJECT_TAGS_STR_LIST "")
set(delim "")
foreach(elem ${PROJECT_TAGS})
    set(PROJECT_TAGS_STR_LIST "${PROJECT_TAGS_STR_LIST}${delim}\"${elem}\"")
    set(delim ", ")
endforeach()

# Configure conanfile.py
configure_file(
    ${CONANFILE_IN}
    ${CONANFILE_OUT}
    @ONLY
)

add_custom_target(conanfile ALL
    SOURCES ${CONANFILE_OUT}
)

# TODO: Invoke actual deployment
