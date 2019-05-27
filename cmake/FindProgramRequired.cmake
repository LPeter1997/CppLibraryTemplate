#[[
 # FindProgramRequired.cmake
 #
 # Copyright (c) 2019 Peter Lenkefi
 # Distributed under the MIT License.
 #
 # A find_program wrapper to automatically fail if the program is not found.
 #
 # Usage:
 # find_program_required(ARGS...)
]]

macro(find_program_required varname)
    find_program(${ARGV})
    message("ARGV is ${ARGV} and varname is ${${varname}}")
    if(NOT ${varname})
        message(FATAL_ERROR "Could not find program ${varname}!")
    endif()
endmacro(find_program_required)
