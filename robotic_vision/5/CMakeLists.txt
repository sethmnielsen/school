cmake_minimum_required(VERSION 3.4)
project(hw5)

set(CMAKE_BUILD_TYPE "Debug")

set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -lstdc++fs -std=c++17")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -lstdc++fs -O0")

find_package(OpenCV REQUIRED)
include_directories(
    ${OpenCV_INCLUDE_DIRS}
)

add_executable(optical_flow src/optical_flow.cpp)
target_link_libraries(optical_flow ${OpenCV_LIBS})

add_executable(feature_matching src/feature_matching.cpp)
target_link_libraries(feature_matching ${OpenCV_LIBS})

add_executable(multiframe_tracking src/multiframe_tracking.cpp)
target_link_libraries(multiframe_tracking ${OpenCV_LIBS})

add_executable(brendon src/brendon.cpp)
target_link_libraries(brendon ${OpenCV_LIBS})