cmake_minimum_required(VERSION 3.4)
project(hw6)

set(CMAKE_BUILD_TYPE "Debug")

set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -lstdc++fs -std=c++17")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -lstdc++fs -O0")

set(PYBIND11_CPP_STANDARD -std=c++17)
find_package(pybind11)

find_package(OpenCV REQUIRED)
include_directories(
    ${OpenCV_INCLUDE_DIRS}
)

# add_executable(task1 src/task1.cpp)
# target_link_libraries(task1 ${OpenCV_LIBS})

# add_executable(task2 src/task2.cpp)
# target_link_libraries(task2 ${OpenCV_LIBS})

# add_executable(task3 src/task3.cpp)
# target_link_libraries(task3 ${OpenCV_LIBS})

add_executable(b_task3 src/b_task3.cpp)
target_link_libraries(b_task3 ${OpenCV_LIBS})

pybind11_add_module(task1_py 
    src/task1.cpp 
)
target_link_libraries(task1_py PUBLIC ${OpenCV_LIBS})
set_target_properties(task1_py PROPERTIES
    PREFIX ""
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/python/"
)

pybind11_add_module(task3_py 
    src/task3.cpp 
)
target_link_libraries(task3_py PUBLIC ${OpenCV_LIBS})
set_target_properties(task3_py PROPERTIES
    PREFIX ""
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/python/"
)
