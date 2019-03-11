cmake_minimum_required(VERSION 3.4)
project(hw4)

set( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -std=gnu++11 -O3 -DNDEBUG")
set( CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0")

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(3dmeasure 3dmeasure.cpp)
target_link_libraries(3dmeasure ${OpenCV_LIBS})