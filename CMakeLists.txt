cmake_minimum_required(VERSION 3.15.0)

project(cylinder LANGUAGES C CXX Fortran)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

add_subdirectory(cylinder)
