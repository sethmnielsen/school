cmake_minimum_required(VERSION 3.4)
project(hw1)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(live_video live_video.cpp)
target_link_libraries(live_video ${OpenCV_LIBS})

add_executable(feature_detect feature_detect.cpp)
target_link_libraries(feature_detect ${OpenCV_LIBS})

# add_executable(ball_detect ball_detect.cpp)
# target_link_libraries(ball_detect ${OpenCV_LIBS})
