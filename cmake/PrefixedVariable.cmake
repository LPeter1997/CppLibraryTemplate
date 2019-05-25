#[[
 # PrefixedVariable.cmake
 #
 # Copyright (c) 2019 Peter Lenkefi
 # Distributed under the MIT License.
 #
 # A helper to define a cache variable with two aliases:
 #  - ${PROJECT_NAME}_<var>
 #  - <var>
 #
 # The one with truthy value is assigned to ${PROJECT_NAME}_<var>, no matter
 # which one was the truthy one. If both are truthy, ${PROJECT_NAME}_<var> is
 # prioritized.
 #
 # Usage:
 # prefixed_variable(name type docstring default)
]]

function(prefixed_variable name type docstring default)
    set(${name} "${default}" CACHE ${type} ${docstring})
    set("${PROJECT_NAME}_${name}" "${default}" CACHE ${type} "${docstring}")

    if(NOT "${${PROJECT_NAME}_${name}}")
        if("${${name}}")
            set("${PROJECT_NAME}_${name}" "${${name}}" CACHE ${type} "${docstring}" FORCE)
        endif()
    endif()
endfunction(prefixed_variable)

# Alias for prefixed_variable with type BOOL
function(prefixed_option name docstring default)
    prefixed_variable("${name}" BOOL "${docstring}" "${default}")
endfunction()
