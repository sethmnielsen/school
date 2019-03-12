cmake_minimum_required(VERSION 3.4)
project(hw4)

set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -lstdc++fs -std=c++17")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
# set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -lstdc++fs -O0")

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(3dmeasure src/3dmeasure.cpp)
target_link_libraries(3dmeasure ${OpenCV_LIBS})

add_executable(tracking src/tracking.cpp)
target_link_libraries(tracking ${OpenCV_LIBS} "stdc++fs")

add_executable(estimate_trajectory src/estimate_trajectory.cpp)
target_link_libraries(estimate_trajectory ${OpenCV_LIBS})