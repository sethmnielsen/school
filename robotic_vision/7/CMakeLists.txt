cmake_minimum_required(VERSION 3.4)
project(hw6)

set(CMAKE_BUILD_TYPE "Debug")

set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -lstdc++fs -std=c++17")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -lstdc++fs -O0")

find_package(OpenCV REQUIRED)
include_directories(
    ${OpenCV_INCLUDE_DIRS}
)

add_executable(task1 src/task1.cpp)
target_link_libraries(task1 ${OpenCV_LIBS})

add_executable(task2 src/task2.cpp)
target_link_libraries(task2 ${OpenCV_LIBS})

add_executable(task3 src/task3.cpp)
target_link_libraries(task3 ${OpenCV_LIBS})

add_executable(b_task1 src/b_task1.cpp)
target_link_libraries(b_task1 ${OpenCV_LIBS})

