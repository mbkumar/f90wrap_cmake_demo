#cmake_minimum_required(VERSION 3.17)

#project(cylinder VERSION 1.0 LANGUAGES C CXX Fortran)
#list(APPEND CMAKE_MODULE_PATH "/home/mbkumar/anaconda3/envs/testv/lib/python3.8/site-packages/skbuild/resources/cmake")
#list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

find_package(PythonExtensions REQUIRED)
find_package(NumPy REQUIRED)
find_package(F2PY REQUIRED)
find_package(F90Wrap REQUIRED)

function(preprocess_fortran outvar)
   message(STATUS "preprocess_fortran arguments: ${outvar}, followed by ${ARGN}")
   set(srcs)
   foreach(f ${ARGN})
     # is it a Fortran file?
     if(f MATCHES "\\.[Ff](9[05])?")
       message(STATUS "Got fortran file: ${f}")
       # construct output filename
       if(NOT IS_ABSOLUTE "${f}")
         get_filename_component(f "${f}" ABSOLUTE)
       endif()
       file(RELATIVE_PATH r "${CMAKE_CURRENT_SOURCE_DIR}" "${f}")
       get_filename_component(e "${r}" EXT)
       get_filename_component(n "${r}" NAME_WE)
       get_filename_component(p "${r}" PATH)
       set(of "${CMAKE_CURRENT_BINARY_DIR}/${n}_fpp${e}")
       message(STATUS "Output name: ${of}")
       # preprocess the thing
       add_custom_command(OUTPUT "${of}"
         #COMMAND ${FPP_EXE} ${incflags} "${defflags}" "${f}" "${of}"
         COMMAND ${CMAKE_Fortran_COMPILER} -E -cpp "${f}" -o "${of}"
         IMPLICIT_DEPENDS Fortran "${f}"
         COMMENT "Preprocessing ${f}"
         VERBATIM
       )
       list(APPEND srcs "${of}")
     #else()
     #  list(APPEND srcs "${f}")
     endif()
   endforeach()
   # return the (preprocessed) sources
   set(${outvar} "${srcs}" PARENT_SCOPE)
endfunction()

set(fortran_src_file ${CMAKE_CURRENT_SOURCE_DIR}/DNAD.f90
                     ${CMAKE_CURRENT_SOURCE_DIR}/DNADHeaders.h
                     ${CMAKE_CURRENT_SOURCE_DIR}/cyldnad.f90
 )
message(STATUS "fortran_src_file is ${fortran_src_file}")
preprocess_fortran(fpp_files ${fortran_src_file})
message(STATUS "fpp_files is ${fpp_files}")

add_library(cyl_lib SHARED ${fpp_files})

function(f90wrap_outputs outvar)
    message(STATUS "process f90 files with f90wrap")
    set(srcs)
    foreach(f ${ARGN})
        # is it a Fortran file?
        if(f MATCHES "\\.[Ff](9[05])?")
            message(STATUS "Got fortran file: ${f}")
            # construct output filename
            if(NOT IS_ABSOLUTE "${f}")
                get_filename_component(f "${f}" ABSOLUTE)
            endif()
            file(RELATIVE_PATH r "${CMAKE_CURRENT_BINARY_DIR}" "${f}")
            get_filename_component(e "${r}" EXT)
            get_filename_component(n "${r}" NAME_WE)
            get_filename_component(p "${r}" PATH)
            set(of "${CMAKE_CURRENT_BINARY_DIR}/f90wrap_${n}${e}")
            message(STATUS "Output name: ${of}")
       
            list(APPEND srcs "${of}")
        #else()
        #  list(APPEND srcs "${f}")
        endif()
    endforeach()
    # return the (preprocesysed) sources
    set(${outvar} "${srcs}" PARENT_SCOPE)
endfunction()

f90wrap_outputs(f90wrap_output_files ${fpp_files})

set(kind_map_file ${CMAKE_CURRENT_SOURCE_DIR}/kind_map)
set(python_mod_name cyl)
set(python_mod_file ${CMAKE_CURRENT_BINARY_DIR}/${python_mod_name}.py)

add_custom_command(OUTPUT ${python_mod_file} ${f90wrap_output_files}
    COMMAND "${F90Wrap_EXECUTABLE}" -m "${python_mod_name}" ${fpp_files} -k "${kind_map_file}"
    #IMPLICIT_DEPENDS Fortran ${fpp_files}
    DEPENDS ${fpp_files} ${kind_map_file}
    COMMENT "Executing F90Wrap for" ${fpp_files}
    VERBATIM
)

add_custom_target(${python_mod_name} 
  DEPENDS ${python_mod_file} ${f90wrap_output_files} 
)

#file(GLOB f90wrap_output_files CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/f90wrap_*.f90")
set(f2py_module_name "_cyl")
set(generated_module_file ${CMAKE_CURRENT_BINARY_DIR}/${f2py_module_name}${PYTHON_EXTENSION_MODULE_SUFFIX})
message(STATUS "Python exten suffix expansion: ${PYTHON_EXTENSION_MODULE_SUFFIX}")
message(STATUS "f90_wrap_output_files: "  ${f90wrap_output_files})
message(STATUS "f2py_module_name: ${f2py_module_name}")
message(STATUS "generated_module_name: ${generated_module_file}")

#set(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE)
set(CMAKE_INSTALL_RPATH "$ORIGIN")
#set(CMAKE_SKIP_BUILD_PATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH ON)
#set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}")
#set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
include_directories("${NumPy_INCLUDE_DIRS}" "${F2PY_INCLUDE_DIRS}" "${CMAKE_CURRENT_BINARY_DIR}")
add_custom_target(${f2py_module_name} ALL
  #DEPENDS ${generated_module_file} ${python_mod_name} cyl_lib ${f90wrap_output_files}
  DEPENDS ${generated_module_file} cyl_lib ${f90wrap_output_files}
)

add_custom_command(
    OUTPUT ${generated_module_file}
    COMMAND ${F2PY_EXECUTABLE} 
        -m ${f2py_module_name} 
        --build-dir ${CMAKE_CURRENT_BINARY_DIR} 
        -c 
        -L. -lcyl_lib --verbose
        ${f90wrap_output_files} 
    #IMPLICIT_DEPENDS Fortran ${f90wrap_output_files}
    DEPENDS cyl_lib ${f90wrap_output_files}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)

install(FILES ${python_mod_file} ${generated_module_file} ${CMAKE_CURRENT_SOURCE_DIR}/__init__.py
        DESTINATION cylinder
)
install(TARGETS cyl_lib 
        LIBRARY 
            DESTINATION cylinder
)


